from fastapi import FastAPI
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from bigquery_client import CLIENT, table_ref
from google.cloud import bigquery

app = FastAPI()

@app.get("/context/{flight_iata}")
def get_context(flight_iata: str):
    q_flight = f"""
      SELECT f.*, b.n_party, b.conf_code
      FROM {table_ref('flights')} AS f
      LEFT JOIN {table_ref('bookings')} AS b
        ON f.flight_iata = b.flight_iata
      WHERE f.flight_iata = @flight_iata
    """
    job = CLIENT.query(
        q_flight,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("flight_iata", "STRING", flight_iata)
            ]
        )
    )
    flight_rec = [dict(row) for row in job.result()]

    q_docs = f"""
      SELECT content
      FROM {table_ref('pdf_rules')}
      --WHERE REGEXP_CONTAINS(content, @flight_iata)
      LIMIT 3
    """
    docs_job = CLIENT.query(
        q_docs,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("flight_iata", "STRING", flight_iata)
            ]
        )
    )
    docs = [row.content for row in docs_job]

    return {"flight_ctx": flight_rec[0] if flight_rec else {}, "docs": docs}