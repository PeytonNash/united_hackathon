from fastapi import FastAPI
from services.bigquery_client import CLIENT, table_ref
from google.cloud import bigquery

app = FastAPI()


@app.get("/context/{flight_iata}")
def get_context(flight_iata: str):
    # 1) Structured: flight + booking count + empty seats
    q_flight = f"""
      SELECT f.*, b.n_party, b.conf_code
      FROM {table_ref('flights')} AS f
      LEFT JOIN {table_ref('bookings')} AS b
        ON f.flight_iata = b.flight.iata
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

    # 2) Unstructured: pull top-3 SOP/docs entries if stored in BigQuery
    q_docs = f"""
      SELECT content
      FROM {table_ref('docs')}
      WHERE REGEXP_CONTAINS(content, @flight_iata)
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