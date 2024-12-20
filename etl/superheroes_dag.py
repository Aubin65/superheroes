"""
DAG de test pour la création d'une collection de super-héros à partir d'un fichier csv téléchargé sur Kaggle
"""

# Import des librairies nécessaires
from airflow.decorators import dag, task
import pendulum
import pymongo
import pandas as pd
import os


# Définition des fonctions de DAG
@dag(schedule="@once", start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), catchup=False, tags=["superheroes_dag"])
def superheroes_etl():
    """DAG global d'import des données des super héros depuis le fichier csv des données brutes vers la base de données MongoDB"""

    @task()
    def extract(path: str) -> pd.DataFrame:
        """Tâche d'extraction des données

        Parameters
        ----------
        path : str
            chemin vers le fichier csv

        Returns
        -------
        pd.DataFrame
            DataFrame issu de la lecture du fichier
        """

        return pd.read_csv(path)

    @task()
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        """
        Parameters
        ----------
        df_persons : pd.DataFrame
            DataFrame issu de l'étape d'extraction, contenant les données brutes.

        Returns
        -------
        pd.DataFrame
            DataFrame transformé

            Les transformations sont les suivantes :
                * Extraction du poids à la bonne unité
                * Extraction de la taille à la bonne unité
                * Suppression des lignes qui ne sont pas correctement définies

        """

        # --------------------------------------------------------------------------------------------- #
        # POIDS ET TAILLE :

        # Extraction des unités
        df["unit_height"] = df["height"].map(lambda x: x.split("'")[-2].split(" ")[1])
        df["unit_weight"] = df["weight"].map(lambda x: x.split("'")[-2].split(" ")[1])

        # Extraction des valeurs :
        df["height(cm)"] = df["height"].map(lambda x: x.split("'")[-2].split(" ")[0].replace(",", "."))
        df["weight(kg)"] = df["weight"].map(lambda x: x.split("'")[-2].split(" ")[0].replace(",", "."))

        # Suppression des valeurs incohérentes
        indexes_to_remove_height = df[~df["unit_height"].isin(["cm", "meters"])].index
        indexes_to_remove_weight = df[~df["unit_weight"].isin(["kg", "tons"])].index

        for id in [indexes_to_remove_height, indexes_to_remove_weight]:
            df.drop(id, inplace=True)

        # Convertion m -> cm
        df[df["unit_height"] == "meters"]["height(cm)"] = df[df["unit_height"] == "meters"]["height(cm)"] * 10

        # Convertion t -> kg
        df[df["unit_weight"] == "tons"]["weight(kg)"] = df[df["unit_weight"] == "tons"]["weight(kg)"] * 1000

        # Suppression des colonnes inutiles
        df.drop(columns=["height", "weight", "unit_weight", "unit_height"], axis=1, inplace=True)

        # --------------------------------------------------------------------------------------------- #
        # CHANGEMENT DES TYPES

        df[["height(cm)", "weight(kg)"]] = df[["height(cm)", "weight(kg)"]].astype(float)

        return df

    @task()
    def load(transformed_df: pd.DataFrame) -> None:
        """Tâche de chargement des données dans la base MongoDB locale

        Parameters
        ----------
        transformed_df : pd.DataFrame
            DataFrame issu de la transformation effectuée dans la fonction transform()
        """

        mongo_uri = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(mongo_uri)

        # Sélection de la base de données et de la collection
        db = client["superheroes"]
        collection = db["info"]

        # Insertion des données dans MongoDB
        collection.insert_many(transformed_df.to_dict(orient="records"))

        # Fermeture de la connexion
        client.close()

    @task()
    def load_csv(transformed_df: pd.DataFrame, transformed_data_csv_path: str) -> None:
        """Tâche de chargement des données vers un fichier csv qui sera utilisé dans les tests de l'outil Power BI

        Parameters
        ----------
        transformed_df : pd.DataFrame
            DataFrame issu de la transformation effectuée dans la fonction transform()
        transformed_data_csv_path : str
            chemin de destination du fichier csv transformé
        """

        transformed_df.to_csv(transformed_data_csv_path)

    # ---------------------------------------------------------------------------------------------------------------------#
    # Extraction des variables nécessaires au lancement du DAG

    # Obtenir le chemin du fichier dag.py
    dag_file_path = os.path.abspath(__file__)

    # Remonter au dossier "superheroes_project"
    project_root = os.path.dirname(os.path.dirname(dag_file_path))

    # Construire le chemin vers "raw_data/superheroes_data.csv"
    csv_file_path = os.path.join(project_root, "raw_data", "superheroes_data.csv")

    # Construire le chemin vers le fichier destination pour la partie csv
    transformed_data_csv_path = os.path.join(project_root, "transformed_data", "transformed_superheroes_data.csv")

    # ---------------------------------------------------------------------------------------------------------------------#
    # Lancement de la tâche d'extraction
    df = extract(csv_file_path)

    # ---------------------------------------------------------------------------------------------------------------------#
    # Lancement de la tâche de transformation
    transformed_df = transform(df)

    # ---------------------------------------------------------------------------------------------------------------------#
    # Lancement de la tâche de chargement

    # Partie CSV
    load_csv(transformed_df, transformed_data_csv_path)

    # Partie MongoDB
    load(transformed_df)


superheroes_etl()
