# Technical Implementation Plan - Enterprise Agentic AI Evaluation Platform (`agentic-ai-evals`)

Build an enterprise-grade, domain-agnostic Agentic AI Evaluation Platform named **`agentic-ai-evals`** in Python 3.12+. The platform evaluates Agentic AI applications (starting with a Travel Planner Agent system under test) across 8 dimensions: Response Quality, Tool Usage, RAG Retrieval, Planning, Guardrails, Performance, Cost, and Structured Output.

---

## Technical Architecture & Principles

- **Clean Architecture & SOLID Principles**: Decoupled domain layer, DTOs, evaluator strategies, factory instantiators, DI runners, and pluggable report generators.
- **Design Patterns**:
  - **Strategy Pattern**: Abstract `Evaluator` interface for independent quality evaluators.
  - **Factory Pattern**: `EvaluatorFactory` constructs enabled evaluators based on environment configuration.
  - **Dependency Injection**: Dataset loaders, pipeline components, target agent client, and report generators injected into `EvaluationRunner`.
- **Domain Agnostic Core**: Core pipeline operates purely on generic `EvaluationContext` DTOs and abstract `AgentInterface`.
- **No Paid APIs / External DB Dependencies**: Uses Pydantic v2 for DTO validation, pandas/openpyxl for Excel output, and mock token/latency traces for cost/performance metrics.

---

## Project Structure & File Mapping

```
agentic-ai-evals/
├── app/
│   ├── config/
│   │   ├── settings.py
│   │   └── weights.py
│   ├── dto/
│   │   ├── context.py
│   │   ├── dataset.py
│   │   ├── metrics.py
│   │   ├── report.py
│   │   └── result.py
│   ├── evaluators/
│   │   ├── base.py
│   │   ├── response/response_evaluator.py
│   │   ├── retrieval/retrieval_evaluator.py
│   │   ├── tools/tool_evaluator.py
│   │   ├── planning/planning_evaluator.py
│   │   ├── guardrails/guardrail_evaluator.py
│   │   ├── performance/performance_evaluator.py
│   │   ├── cost/cost_evaluator.py
│   │   └── structured_output/structured_output_evaluator.py
│   ├── factories/
│   │   └── evaluator_factory.py
│   ├── interfaces/
│   │   ├── agent.py
│   │   ├── evaluator.py
│   │   ├── loader.py
│   │   └── reporter.py
│   ├── pipeline/
│   │   ├── aggregator.py
│   │   └── evaluation_pipeline.py
│   ├── reports/
│   │   ├── composite_reporter.py
│   │   ├── excel_reporter.py
│   │   └── json_reporter.py
│   ├── runners/
│   │   └── evaluation_runner.py
│   ├── services/
│   │   └── travel_planner_agent.py
│   ├── utils/
│   │   └── logger.py
│   └── main.py
├── datasets/
│   └── travel_planner_eval_dataset.json
├── evaluation-results/
├── .env.example
├── pyproject.toml
└── README.md
```

---

## Evaluators Breakdown (8 Dimensions)

1. **ResponseEvaluator**: Evaluates correctness (keyword coverage), completeness, relevance, and clarity (0-100 scale).
2. **ToolEvaluator**: Evaluates tool selection accuracy, execution success rate, parameter validity, missing and unnecessary tool calls.
3. **RetrievalEvaluator**: Evaluates RAG context relevance, document recall/precision, citation accuracy, top-K correctness, and grounding quality.
4. **PlanningEvaluator**: Evaluates step ordering correctness, missing steps, extra steps, and workflow DAG logic.
5. **GuardrailEvaluator**: Evaluates prompt injection detection/blocking, jailbreak resistance, PII masking, and harmful content filtering.
6. **PerformanceEvaluator**: Measures total latency, tool latency, retrieval latency, and LLM latency against SLAs.
7. **CostEvaluator**: Measures input tokens, output tokens, embedding tokens, calculates model pricing costs and unit economy metrics.
8. **StructuredOutputEvaluator**: Validates payload against expected JSON schema / Pydantic DTOs, required fields, enum value constraints, and missing properties.

---

## Verification Plan

### Automated Verification
- Run `uv sync` to ensure dependencies are installed.
- Run `python app/main.py` to execute the full evaluation suite against the Travel Planner Agent dataset.
- Validate that output artifacts are generated in `evaluation-results/`:
  - `evaluation-results/evaluation_report.json`
  - `evaluation-results/evaluation_report.xlsx`
