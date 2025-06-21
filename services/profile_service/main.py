from fastapi import FastAPI
import sqlite3
import os

app = FastAPI()
DB_PATH = os.getenv("DB_PATH", "acdc.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/profile/{pax_id}")
def get_profile(pax_id: str):
    conn = get_db()
    cur  = conn.execute("SELECT * FROM profiles WHERE pax_id = ?", (pax_id,))
    row  = cur.fetchone()
    profile = dict(row) if row else {}
    # compute priority
    tier = profile.get("tier_score", 0)
    tags = profile.get("tags", "").split(",")
    prio = 0.6*tier + 0.4*(1 if "MED_SURGERY" in tags else 0)
    profile["priority_score"] = prio
    conn.close()
    return profile
