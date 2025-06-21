# services/trace_api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import bigquery
import os
import uuid
import json
from services.bigquery_client import CLIENT, table_ref

app = FastAPI()

class Trace(BaseModel):
    trace_id: str | None = None
    payload: dict

@app.post("/trace")
def log_trace(t: Trace):
    tid = t.trace_id or str(uuid.uuid4())
    table = CLIENT.get_table(table_ref("decision_trace"))
    CLIENT.insert_rows_json(table, [{"trace_id": tid, "payload": t.payload}])
    return {"trace_id": tid}

@app.get("/trace/{trace_id}")
def get_trace(trace_id: str):
    q = f"""
      SELECT payload
      FROM {table_ref('decision_trace')}
      WHERE trace_id = @trace_id
      LIMIT 1
    """
    job = CLIENT.query(
        q,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("trace_id","STRING",trace_id)
            ]
        )
    )
    rows = list(job.result())
    return rows[0].payload if rows else {}
