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

@app.post("/flight_options")
def build_options(ctx: Ctx):
    dep = ctx.flight_ctx["departure_iata"]
    arr = ctx.flight_ctx["arrival_iata"]
    q = f"""
      SELECT  flight_iata,
              departure_iata,
              departure_scheduled,
              arrival_iata,
              arrival_scheduled
      FROM {table_ref('flights')}
      WHERE departure_iata = @dep AND
        arrival_iata = @arr AND
        TIMESTAMP_DIFF(departure_scheduled, CURRENT_TIMESTAMP(), HOUR) BETWEEN 0 AND 12 AND -- DATA IS STATIC NEED TO UPDATE TO BE THE TIME WHEN THE API WAS CALLED
        airline_iata = 'UA'
    """
    job = CLIENT.query(
        q,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("dep","STRING",dep),
                bigquery.ScalarQueryParameter("arr","STRING",arr)
            ]
        )
    )
    opts = [dict(row) for row in job.result()]
    return opts

@app.post("/lounge_options")
def build_options(ctx: Ctx):
    dep = ctx.flight_ctx["departure_iata"]
    q = f"""
      SELECT  airport, type, location, open, close, day_0, day_1, day_2, day_3, day_4, day_5, day_6,
              full_bar, full_buffet, full_service_bar, grab_and_go_snacks, light_snacks, pre_flight_dining, quiet suites, self_service_bar, showers, wi_fi
      FROM {table_ref('lounges')}
      WHERE airport = @dep
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

@app.post("/hotel_options")
def build_options(ctx: Ctx):
    dep = ctx.flight_ctx["departure_iata"]
    q = f"""
      SELECT  airport_iata, hotel_name, stars, distance, rooms_available      
      FROM {table_ref('hotels')}
      WHERE airport_iata = @dep
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