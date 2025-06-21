from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()
DB_PATH = os.getenv("DB_PATH", "acdc.db")


class Ctx(BaseModel):
    flight_ctx: dict


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.post("/build_options")
def build_options(ctx: Ctx):
    dep = ctx.flight_ctx.get("dep")
    conn = get_db()
    # find UA & LH flights next 12h
    cur = conn.execute("""
      SELECT flight_id, dep_time, arr_time, airline
      FROM flights
      WHERE dep = ? AND dep_time BETWEEN datetime('now') AND datetime('now','+12 hours')
        AND airline IN ('UA','LH')
      LIMIT 5
    """, (dep,))
    flights = [dict(r) for r in cur.fetchall()]

    # join hotels & lounges simply
    options = []
    for f in flights:
        # pick one hotel
        hcur = conn.execute("SELECT * FROM hotels WHERE airport_code = ? LIMIT 1", (f["arr"],))
        hotel = dict(hcur.fetchone() or {})
        lcur = conn.execute("SELECT * FROM lounges WHERE airport_code = ? LIMIT 1", (f["arr"],))
        lounge = dict(lcur.fetchone() or {})
        options.append({"flight": f, "hotel": hotel, "lounge": lounge})

    conn.close()
    return options