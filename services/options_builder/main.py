from fastapi import FastAPI
from pydantic import BaseModel
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from bigquery_client import CLIENT, table_ref
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
      SELECT      f.*, h.hotel_name, h.stars, 
                  l.full_bar, l.full_buffet, l.full_service_bar, grab_and_go_snacks, light_snacks, pre_flight_dining, quiet_suites, self_service_bar, showers, wi_fi
      FROM        candidate_flights AS f
      LEFT JOIN   {table_ref('hotels')} AS h
        ON f.arrival_iata = h.airport_iata
      LEFT JOIN   {table_ref('lounges')} AS l
        ON f.arrival_iata = l.airport
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
