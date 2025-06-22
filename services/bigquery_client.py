import os
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT_ID = os.getenv("BQ_PROJECT", "sky1-462619")
CLIENT = bigquery.Client(project=PROJECT_ID)
DATASET = os.getenv("BQ_DATASET", "United_Tables")

def table_ref(table_name: str):
    return f"`{PROJECT_ID}`.`{DATASET}`.`{table_name}`"