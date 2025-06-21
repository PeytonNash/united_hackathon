# united_hackathon
United Airlines/ADSP hackathon collaboration  ✈️

## Overview -- AI written slop for now

The Agentic Complimentary Disruption Concierge (ACDC) system automates passenger assistance during flight disruptions. It integrates structured and unstructured data, personalized recovery options, and provides transparent auditing of decisions.

## Project Architecture

The system consists of multiple independent microservices that communicate via REST APIs and share data through a central SQLite database (`acdc.db`).

- Event Listener
- Context Aggregator
- Delay Explainer
- Rules and Policy Engine
- Profile Service
- Options Builder
- Cost Evaluator
- Sentiment and Escalation Manager
- Decision Trace API
- Streamlit Demo UI

## Local Development Setup

1. Clone repository:

```bash 
git clone 
cd united_hackathon
```

2. Setup Python environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ensure you have Python 3.8+ installed. 

3. Setup SQLite Database:

```bash
python infra/setup_db.py
```

4. Run services individually (example):

```bash
# Terminal 1
uvicorn services/event_listener/main:app --port 8000

# Terminal 2
uvicorn services/context_aggregator/main:app --port 8001

# Terminal 3
uvicorn services/delay_explainer/agent:app --port 8002

# Terminal 4
uvicorn services/rules_policy/engine:app --port 8003

# Terminal 5
uvicorn services/profile_service/main:app --port 8004

# Terminal 6
uvicorn services/options_builder/main:app --port 8005

# Terminal 7
uvicorn services/cost_evaluator/main:app --port 8006

# Terminal 8
uvicorn services/sentiment_escalation/main:app --port 8007

# Terminal 9
uvicorn services/trace_api/main:app --port 8008
```

5. Run Streamlit UI:

```bash
streamlit run services/ui_streamlit/app.py –server.port 8501
```

## Running Tests

Run all unit tests:

```bash
pytest -q
```

Check you have a clean test database setup via `tests/conftest.py`.
