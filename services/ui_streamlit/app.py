# THIS IS NOT WORKING YET, JUST A PLACEHOLDER


import streamlit as st
import requests
import os

API = os.getenv("API_BASE","http://localhost:8000")

st.title("ACDC Disruption Concierge Demo")
flight = st.text_input("Flight ID", "")
if st.button("Start Recovery") and flight:
    ctx = requests.get(f"{API}/context/{flight}").json()
    st.subheader("Delay Explanation")
    expl = requests.post(f"{API}/delay_explainer", json=ctx).json()
    st.write(expl["explanation"])

    # fetch profile
    # assume pax_id = flight for demo
    prof = requests.get(f"{API}/profile/{flight}").json()

    # rules
    rp   = requests.post(f"{API}/rules_policy", json={**ctx, "profile":prof}).json()
    st.write("Baseline Offer:", rp["baseline_offer"])

    # options
    opts = requests.post(f"{API}/build_options", json={"flight_ctx":ctx["flight_ctx"]}).json()

    # score
    scored = requests.post(f"{API}/score_options", json={"options":opts, "priority_score":prof["priority_score"]}).json()
    for o in scored:
        if st.button(f"Book {o['flight']['flight_id']} (score {o['score']:.2f})"):
            # simulate user message
            se = requests.post(f"{API}/sentiment", json={"user_msg":"Please hurry!", "priority_score":prof["priority_score"]}).json()
            trace = requests.post(f"{API}/trace", json={"payload": {"flight":flight,"option":o,**se}}).json()
            st.success(f"Booked! Trace ID: {trace['trace_id']}")
            if st.button("View Trace"):
                tr = requests.get(f"{API}/trace/{trace['trace_id']}").json()
                st.json(tr)