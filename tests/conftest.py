import os
import sqlite3
import tempfile
import pytest


# Create a temp SQLite DB with needed tables and seed data
@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "acdc_test.db"
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # flights
    cur.execute("""
      CREATE TABLE flights(
        flight_id TEXT PRIMARY KEY,
        dep TEXT, arr TEXT,
        dep_time TEXT, arr_time TEXT,
        delay_code TEXT, empty_seats INTEGER
      )
    """)
    cur.execute("""
      INSERT INTO flights VALUES
      ('UA100','SFO','ORD','2025-06-20 10:00','2025-06-20 16:00','MX',5)
    """)

    # profiles
    cur.execute("""
      CREATE TABLE profiles(
        pax_id TEXT PRIMARY KEY,
        tier_score REAL, tags TEXT, past_CSAT REAL
      )
    """)
    cur.execute("""
      INSERT INTO profiles VALUES
      ('UA100',0.9,'MED_SURGERY',4.5)
    """)

    # hotels & lounges
    cur.execute("""
      CREATE TABLE hotels(airport_code TEXT, hotel_name TEXT, rooms_open INTEGER, corp_rate REAL)
    """)
    cur.execute("INSERT INTO hotels VALUES('ORD','Hilton',10,150.0)")
    cur.execute("""
      CREATE TABLE lounges(
        airport_code TEXT, lounge_type TEXT, location TEXT,
        open TEXT, close TEXT, amenities_flags TEXT
      )
    """)
    cur.execute("INSERT INTO lounges VALUES('ORD','United Club','Terminal 1','05:00','22:00','wifi|bar')")

    # docs + FTS
    cur.execute("CREATE TABLE docs(id INTEGER PRIMARY KEY, content TEXT)")
    cur.execute("INSERT INTO docs VALUES(1,'§259 compensation rule')")
    cur.execute("CREATE VIRTUAL TABLE docs_fts USING fts5(content)")
    cur.execute("INSERT INTO docs_fts(rowid, content) SELECT id, content FROM docs")

    # trace table
    cur.execute("CREATE TABLE decision_trace(trace_id TEXT PRIMARY KEY, payload JSON)")
    conn.commit()
    conn.close()
    return str(path)


# Monkeypatch DB_PATH for all services
@pytest.fixture(autouse=True)
def set_db_path_env(test_db_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", test_db_path)