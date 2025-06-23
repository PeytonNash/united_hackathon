#!/usr/bin/env bash
set -e

uvicorn services.context_aggregator.main:app    --reload --port 8001 &
uvicorn services.profile_service.main:app       --reload --port 8002 &
uvicorn services.delay_explainer.agent:app      --reload --port 8003 &
uvicorn services.rules_policy.engine:app        --reload --port 8004 &
uvicorn services.options_builder_agent.app:app  --reload --port 8005 &
uvicorn services.cost_evaluator.main:app        --reload --port 8006 &
uvicorn services.sentiment_escalation.main:app  --reload --port 8007 &
uvicorn services.trace_api.main:app             --reload --port 8008 &

uvicorn services.mcp_agent.app:app               --reload --port 8000 &

streamlit run frontend/chat_app.py