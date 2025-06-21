import os
from google.cloud import bigquery

PROJECT_ID = os.getenv("BQ_PROJECT", "sky1")
CLIENT = bigquery.Client(project=PROJECT_ID)
DATASET = os.getenv("BQ_DATASET", "acdc_ds")

def table_ref(table_name: str):
    return f"`{PROJECT_ID}`.`{DATASET}`.`{table_name}`"
