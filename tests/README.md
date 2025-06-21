# ACDC System Testing

## Overview

Tests are written using `pytest` and validate each microservice independently.

## Setup Test Environment

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install testing dependencies:

```bash
pip install pytest httpx
```

Ensure you have the necessary environment variables set, such as `DB_PATH` and `OPENAI_KEY`, to allow tests to run against the correct database and API.

Ensure a clean test database is prepared via `tests/conftest.py`.

## Running Tests

Execute all tests with:

```bash
pytest -q
```

## Test Structure

- Tests reside in the `tests/` directory.
- Each microservice has a dedicated test file:
    - `test_event_listener.py`
    - `test_context_aggregator.py`
    - `test_delay_explainer.py`
    - `test_rules_policy.py`
    - `test_profile_service.py`
    - `test_options_builder.py`
    - `test_cost_evaluator.py`
    - `test_sentiment_escalation.py`
    - `test_trace_api.py`
    - `test_ui_streamlit.py`
