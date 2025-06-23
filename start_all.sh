#!/usr/bin/env bash
set -e

uvicorn services/context_aggregator/app:app    --reload --port 8001 &
uvicorn services/profile_service/app:app       --reload --port 8002 &
uvicorn services/delay_explainer/app:app       --reload --port 8003 &
uvicorn services/rules_policy/app:app          --reload --port 8004 &
uvicorn services/options_builder_agent/app:app --reload --port 8005 &
uvicorn services/cost_evaluator/app:app        --reload --port 8006 &
uvicorn services/sentiment_escalation/app:app  --reload --port 8007 &
uvicorn services/trace_api/app:app              --reload --port 8008 &

uvicorn services/mcp_agent/app:app             --reload --port 8000 &

streamlit run frontend/multiturn_withcolours.py