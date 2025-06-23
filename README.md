# United Airlines Hackathon: ACDC System
### Agentic Complimentary Disruption Concierge (ACDC)
A collaborative project developed during the United Airlines / ADSP Hackathon 

## [✈️ Demo Video](https://uchicago.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=85375ab5-0e76-41ef-b4c2-b305009413b0)

## ✈️ Overview

The ACDC system automates passenger assistance during flight disruptions by combining structured and unstructured data to generate personalised recovery options. It provides:
* Real-time disruption monitoring
* Automated decision-making based on policies and profiles
* Transparent decision traceability
* Scalable architecture for integration into airline operations

## ✈️ Project Architecture

The system consists of multiple independent microservices that communicate via REST APIs and share data through a central SQLite database (`acdc.db`).

Core components include:
* **Event Listener** – Monitors flight event streams
* **Context Aggregator** – Gathers passenger and disruption context
* **Delay Explainer** – Generates human-readable explanations
* **Rules and Policy Engine** – Applies recovery policies and business rules
* **Profile Service** – Retrieves passenger profiles and preferences
* **Options Builder** – Generates alternative recovery options
* **Cost Evaluator** – Assesses financial impact of recovery options
* **Sentiment + Escalation Manager** – Incorporates customer sentiment into decision-making
* **Decision Trace API** – Logs and audits decisions
* **Streamlit UI** – Interactive interface for demo and testing

## ✈️ Local Development Setup

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

## ✈️ Running Tests

Run all unit tests:

```bash
pytest -q
```

Check you have a clean test database setup via `tests/conftest.py`.
