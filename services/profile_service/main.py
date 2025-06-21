from fastapi import FastAPI
from services.bigquery_client import CLIENT, table_ref
from google.cloud import bigquery

app = FastAPI()

@app.get("/profile/{customer_id}")
def get_profile(customer_id: str):
    q = f"""
      SELECT c.*, b.flight.iata AS last_flight, COUNT(b.customer_id) AS total_bookings
      FROM {table_ref('customers')} AS c
      LEFT JOIN {table_ref('bookings')} AS b
        ON c.customer_id = b.customer_id
      WHERE c.customer_id = @customer_id
      GROUP BY c.customer_id, c.tier_score, c.tags, c.past_CSAT, b.flight.iata
    """
    job = CLIENT.query(
        q,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("customer_id","STRING",customer_id)
            ]
        )
    )
    rec = [dict(row) for row in job.result()]
    if not rec:
        return {}
    profile = rec[0]
    # compute priority on the fly
    tier = profile.get("tier_score", 0)
    tags = profile.get("tags","").split(",")
    profile["priority_score"] = 0.6 * tier + 0.4 * (1 if "MED_SURGERY" in tags else 0)
    return profile
