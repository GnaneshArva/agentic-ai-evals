# agentic-ai-evals Handbook

## Universal Rules
- **Git Push Approval Rule**: NEVER run `git push` automatically. Always present implemented changes and unit test verification results, and wait for explicit user confirmation before executing any `git push` command.
- **Python Virtualenv Path**: All unit tests must be executed using:
  `/Users/gnanesh_arva/Downloads/travel-planner-v2/travel-agent-service/.venv/bin/pytest`

## Repository Standards
- **Port**: `8008` (Default)
- **Role**: AI Evaluation Platform evaluating LLM responses, RAG retrieval accuracy, and guardrail compliance (RAGAS, DeepEval, Coherence, A/B testing).

## Relevant Task Playbooks (`skills/`)
- `run-evals-benchmark`: Playbook for executing RAGAS, DeepEval, Coherence, and A/B evaluations on agentic-ai-evals.
