"""
DAG de test 
"""

# Import des librairies nécessaires
from airflow.decorators import dag, task
import pendulum
import pymongo
import pandas as pd
import os


@dag(schedule="@once", start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), catchup=False, tags=["superhesors_dag"])
def superhesors_etl():
    """DAG global d'import des données des super héros depuis le fichier csv des données brutes vers la base de données MongoDB"""

    @task()
    def extract(path: str = "../raw_data/superheroes_data.csv") -> pd.DataFrame:
        """
        Tâche d'extraction des héros
        """

        return pd.read_csv(path)
