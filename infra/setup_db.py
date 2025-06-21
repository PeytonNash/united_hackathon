import sqlite3
import pandas as pd
import glob

DB = "acdc.db"
conn = sqlite3.connect(DB)

for tbl in ["flights", "lounges", "hotels", "profiles"]:
    df = pd.read_csv(f"data/{tbl}.csv")
    df.to_sql(tbl, conn, if_exists="replace", index=False)

# load docs and FTS
conn.execute("CREATE TABLE IF NOT EXISTS docs(id INTEGER PRIMARY KEY, content TEXT)")
txts = glob.glob("data/sop_docs/*.txt")
for i, path in enumerate(txts, start=1):
    with open(path) as f:
        conn.execute("INSERT INTO docs VALUES (?,?)", (i, f.read()))
conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(content)")
conn.execute("INSERT INTO docs_fts(rowid, content) SELECT id, content FROM docs")

# trace table
conn.execute("""
  CREATE TABLE IF NOT EXISTS decision_trace(
    trace_id TEXT PRIMARY KEY,
    payload JSON
  )
""")
conn.commit()
conn.close()
print("Database initialized:", DB)