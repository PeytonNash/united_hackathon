import os
import sqlite3
import pytest


@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "acdc_test.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # 1. flights
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
      ('UA100','SFO','ORD','2025-06-20 10:00','2025-06-20 16:00','MX',5),
      ('UA200','LAX','DEN','2025-06-21 09:00','2025-06-21 13:00','WX',8)
    """)

    # 2. profiles
    cur.execute("""
      CREATE TABLE profiles(
        pax_id TEXT PRIMARY KEY,
        tier_score REAL,
        tags TEXT,
        past_CSAT REAL
      )
    """)
    cur.execute("""
      INSERT INTO profiles VALUES
      ('UA100',0.9,'MED_SURGERY',4.5),
      ('UA200',0.3,'',3.8)
    """)

    # 3. hotels
    cur.execute("""
      CREATE TABLE hotels(
        airport_code TEXT,
        hotel_name TEXT,
        rooms_open INTEGER,
        corp_rate REAL
      )
    """)
    cur.execute("""
      INSERT INTO hotels VALUES
      ('ORD','Hilton','10',150.0),
      ('DEN','Marriott','5',120.0)
    """)

    # 4. lounges
    cur.execute("""
      CREATE TABLE lounges(
        airport_code TEXT,
        lounge_type TEXT,
        location TEXT,
        open TEXT, close TEXT,
        amenities_flags TEXT
      )
    """)
    cur.execute("""
      INSERT INTO lounges VALUES
      ('ORD','United Club','Terminal 1','05:00','22:00','wifi|bar'),
      ('DEN','United Club','Concourse A','06:00','20:00','snacks|coffee')
    """)

    # 5. docs + FTS index
    cur.execute("CREATE TABLE docs(id INTEGER PRIMARY KEY, content TEXT)")
    cur.execute("""
      INSERT INTO docs VALUES
      (1,'§259 compensation rule applies here'),
      (2,'Weather advisory SIGMET text')
    """)
    cur.execute("CREATE VIRTUAL TABLE docs_fts USING fts5(content)")
    cur.execute("INSERT INTO docs_fts(rowid,content) SELECT id,content FROM docs")

    # 6. decision_trace
    cur.execute("""
      CREATE TABLE decision_trace(
        trace_id TEXT PRIMARY KEY,
        payload JSON
      )
    """)

    conn.commit()
    conn.close()
    return str(db_file)


# ensure every service uses this test DB
@pytest.fixture(autouse=True)
def patch_db_path(monkeypatch, test_db_path):
    monkeypatch.setenv("DB_PATH", test_db_path)
