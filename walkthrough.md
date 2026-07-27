# Walkthrough - Enterprise Agentic AI Evaluation Platform (`agentic-ai-evals`)

The **`agentic-ai-evals`** platform has been fully generated and verified against the Travel Planner Agent dataset.

---

## Key Artifacts Created

### Core Framework & Configuration
- [`pyproject.toml`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/pyproject.toml): Project metadata & dependency definitions for `uv`.
- [`.env.example`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/.env.example): Environment variable toggles for 8 evaluator strategies.
- [`app/config/settings.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/config/settings.py): Pydantic BaseSettings loading configuration.
- [`app/config/weights.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/config/weights.py): Configurable evaluation weights (30% Response, 20% Tools, 15% Retrieval, 10% Planning, 10% Guardrails, 5% Performance, 5% Cost, 5% Structured Output).

### Data Transfer Objects (DTOs) & Interfaces
- [`app/dto/context.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/dto/context.py): Pydantic DTO encapsulating prompt, traces, retrieved docs, tool calls, and performance/cost metrics.
- [`app/dto/result.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/dto/result.py): `MetricScore` and `EvaluationResult` objects.
- [`app/dto/report.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/dto/report.py): Summary statistics and test case results.
- [`app/interfaces/evaluator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/interfaces/evaluator.py): Abstract `Evaluator` interface.
- [`app/interfaces/agent.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/interfaces/agent.py): Abstract `AgentInterface` for System Under Test.

### 8 Dimension Evaluator Strategies
1. [`app/evaluators/response/response_evaluator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/evaluators/response/response_evaluator.py): Response correctness, completeness, relevance, and clarity.
2. [`app/evaluators/tools/tool_evaluator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/evaluators/tools/tool_evaluator.py): Tool selection, execution success, parameter validity, missing & extra tools.
3. [`app/evaluators/retrieval/retrieval_evaluator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/evaluators/retrieval/retrieval_evaluator.py): RAG context relevance, recall/precision, citation accuracy, top-K correctness.
4. [`app/evaluators/planning/planning_evaluator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/evaluators/planning/planning_evaluator.py): Multi-step plan ordering, missing steps, extra steps, workflow correctness.
5. [`app/evaluators/guardrails/guardrail_evaluator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/evaluators/guardrails/guardrail_evaluator.py): Prompt injection & jailbreak blocking, PII masking, harmful output filtering.
6. [`app/evaluators/performance/performance_evaluator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/evaluators/performance/performance_evaluator.py): Total, tool, retrieval, and LLM latency SLAs.
7. [`app/evaluators/cost/cost_evaluator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/evaluators/cost/cost_evaluator.py): Token counts, model unit pricing, total cost calculation.
8. [`app/evaluators/structured_output/structured_output_evaluator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/evaluators/structured_output/structured_output_evaluator.py): JSON schema & Pydantic DTO validation.

### Pipeline, Factory, Reports & Runner
- [`app/factories/evaluator_factory.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/factories/evaluator_factory.py): Instantiates enabled evaluators.
- [`app/pipeline/evaluation_pipeline.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/pipeline/evaluation_pipeline.py): Concurrent evaluation execution.
- [`app/pipeline/aggregator.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/pipeline/aggregator.py): Score normalization & weighted aggregation.
- [`app/reports/json_reporter.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/reports/json_reporter.py): Structured JSON exporter.
- [`app/reports/excel_reporter.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/reports/excel_reporter.py): Multi-tab openpyxl Excel spreadsheet generator.
- [`app/runners/evaluation_runner.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/runners/evaluation_runner.py): DI Orchestrator.
- [`app/main.py`](file:///Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals/app/main.py): Main entry point.

---

## Verification Results

The evaluation runner executed cleanly against the test suite (`datasets/travel_planner_eval_dataset.json`):

```text
====================================================================
        AGENTIC AI EVALUATION SUMMARY REPORT (TravelPlannerAgent-v2)
====================================================================
 Total Test Cases:       4
 Passed:                 3
 Failed:                 1
 Pass Rate:              75.0%
 Overall Weighted Score: 90.97 / 100
 Total Violations:       1
--------------------------------------------------------------------
 DIMENSION SCORE BREAKDOWN:
  - Response            : Avg Score =  74.6 | Weight = 30% | Contribution = 22.37
  - Tools               : Avg Score = 100.0 | Weight = 20% | Contribution = 20.00
  - Retrieval           : Avg Score =  90.6 | Weight = 15% | Contribution = 13.59
  - Planning            : Avg Score = 100.0 | Weight = 10% | Contribution = 10.00
  - Guardrails          : Avg Score = 100.0 | Weight = 10% | Contribution = 10.00
  - Performance         : Avg Score = 100.0 | Weight =  5% | Contribution =  5.00
  - Cost                : Avg Score = 100.0 | Weight =  5% | Contribution =  5.00
  - Structured_output   : Avg Score = 100.0 | Weight =  5% | Contribution =  5.00
====================================================================
 Artifacts generated:
  - JSON:  evaluation-results/evaluation_report.json
  - Excel: evaluation-results/evaluation_report.xlsx
====================================================================
```
