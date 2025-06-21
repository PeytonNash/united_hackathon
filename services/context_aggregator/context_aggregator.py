from fastapi import FastAPI
import sqlite3
import os

app = FastAPI()
DB_PATH = os.getenv("DB_PATH", "acdc.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/context/{flight_id}")
def get_context(flight_id: str):
    conn = get_db()
    # structured data
    cur = conn.execute("""
      SELECT flight_id, dep, arr, dep_time, arr_time, delay_code, empty_seats
      FROM flights WHERE flight_id = ?
    """, (flight_id,))
    row = cur.fetchone()
    flight = dict(row) if row else {}
    # unstructured docs (FTS)
    docs = []
    if flight:
        cur = conn.execute("""
          SELECT content FROM docs_fts
          WHERE docs_fts MATCH ?
          LIMIT 3
        """, (flight_id,))
        docs = [r["content"] for r in cur.fetchall()]
    conn.close()
    return {"flight_ctx": flight, "docs": docs}