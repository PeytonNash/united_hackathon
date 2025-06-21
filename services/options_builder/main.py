from fastapi import FastAPI
from pydantic import BaseModel
from services.bigquery_client import CLIENT, table_ref
from google.cloud import bigquery

app = FastAPI()

class Ctx(BaseModel):
    flight_ctx: dict

@app.post("/build_options")
def build_options(ctx: Ctx):
    dep = ctx.flight_ctx["departure_iata"]
    q = f"""
      WITH candidate_flights AS (
        SELECT flight_iata, departure_scheduled, arrival_iata
        FROM {table_ref('flights')}
        WHERE departure_iata = @dep
          AND TIMESTAMP_DIFF(departure_scheduled, CURRENT_TIMESTAMP(), HOUR) BETWEEN 0 AND 12
          AND airline_iata IN ('UA','LH')
        LIMIT 5
      )
      SELECT f.*, h.hotel_name, h.stars, l.amenities_flags
      FROM candidate_flights AS f
      LEFT JOIN {table_ref('hotels')} AS h
        ON f.arrival_iata = h.airport_iata
      LEFT JOIN {table_ref('lounges')} AS l
        ON f.arrival_iata = l.airport_code
    """
    job = CLIENT.query(
        q,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("dep","STRING",dep)
            ]
        )
    )
    opts = [dict(row) for row in job.result()]
    return opts
