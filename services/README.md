# ACDC Microservices Overview

## Services Description

Each microservice in the ACDC project follows SRP:

- **Event Listener**: Captures flight disruption events and forwards them to the context aggregator.
- **Context Aggregator**: Aggregates structured flight data and retrieves relevant documents.
- **Delay Explainer**: Converts delay codes into understandable messages.
- **Rules and Policy Engine**: Determines baseline rebooking options according to business rules and regulatory requirements.
- **Profile Service**: Retrieves passenger profiles and computes priority scores.
- **Options Builder**: Generates a list of viable rebooking options.
- **Cost Evaluator**: Ranks rebooking options using an external LLM scoring model.
- **Sentiment and Escalation Manager**: Assesses passenger sentiment and decides escalation paths.
- **Decision Trace API**: Stores and retrieves comprehensive decision traces for auditing purposes.
- **Streamlit Demo UI**: Provides a user-friendly interface for demonstrating system capabilities.

## Running Microservices

Ensure each service has access to the `acdc.db` database and required environment variables set (e.g., `DB_PATH`, `OPENAI_KEY`).

Example for running a single service:

```bash
uvicorn services/context_aggregator/main:app –port 8001
```

## Environment Variables

Common variables include:
- `DB_PATH`: Path to the SQLite database.
- `OPENAI_KEY`: API key for OpenAI integration.
- `SLACK_WEBHOOK`: Slack webhook URL for escalations.

Set these variables appropriately before running each service.
