from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import json
import os
import uuid

app = FastAPI()
DB_PATH = os.getenv("DB_PATH", "acdc.db")


class Trace(BaseModel):
    trace_id: str | None = None
    payload: dict


@app.post("/trace")
def log_trace(t: Trace):
    conn = sqlite3.connect(DB_PATH)
    tid = t.trace_id or str(uuid.uuid4())
    conn.execute("INSERT INTO decision_trace(trace_id, payload) VALUES(?,?)",
                 (tid, json.dumps(t.payload)))
    conn.commit()
    conn.close()
    return {"trace_id": tid}


@app.get("/trace/{trace_id}")
def get_trace(trace_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT payload FROM decision_trace WHERE trace_id = ?", (trace_id,))
    row = cur.fetchone()
    conn.close()
    return json.loads(row[0]) if row else {}