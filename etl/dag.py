"""
DAG de test 
"""

# Import des librairies nécessaires
from airflow.decorators import dag, task
import pendulum
import pymongo  # noqa
import pandas as pd  # noqa
import os  # noqa


@dag(schedule="@once", start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), catchup=False, tags=["superheroes_dag"])
def superheroes_etl():
    """DAG global d'import des données des super héros depuis le fichier csv des données brutes vers la base de données MongoDB"""

    @task()
    def extract(path: str) -> pd.DataFrame:
        """
        Tâche d'extraction des héros
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
                * Changement du type des alias de str vers list (peut être une liste vide)
                * Suppression des lignes qui ne sont pas correctement définies

        """

        # --------------------------------------------------------------------------------------------- #
        # POIDS ET TAILLE :

        # Extraction des unités
        df["unit_height"] = df["height"].map(lambda x: x.split("'")[-2].split(" ")[1])
        df["unit_weight"] = df["weight"].map(lambda x: x.split("'")[-2].split(" ")[1])

        # Extraction des valeurs :
        df["height(cm)"] = df["height"].map(lambda x: x.split("'")[-2].split(" ")[0])
        df["weight(kg)"] = df["weight"].map(lambda x: x.split("'")[-2].split(" ")[0])

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

        df["aliases"].astype(list)
        df[["height(cm)", "weight(kg)"]].astype(float)

        return df

    @task()
    def load(transformed_df: pd.DataFrame) -> None:

        mongo_uri = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(mongo_uri)

        # Sélection de la base de données et de la collection
        db = client["superheroes"]
        collection = db["info"]

        # Insertion des données dans MongoDB
        collection.insert_many(transformed_df.to_dict(orient="records"))

        # Fermeture de la connexion
        client.close()

    # Déterminer le chemin absolu du DAG
    dag_folder = os.path.dirname(__file__)  # Chemin du fichier DAG
    csv_path = os.path.join(os.path.dirname(dag_folder), "data.csv")  # Fichier dans le même dossier

    df = extract(csv_path)
    transformed_df = transform(df)
    load(transformed_df)


superheroes_etl()
