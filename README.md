# `agentic-ai-evals`: Enterprise Agentic AI Evaluation Platform

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Architecture](https://img.shields.io/badge/architecture-Clean%20%2F%20SOLID-green)
![License](https://img.shields.io/badge/license-Enterprise-purple)

**`agentic-ai-evals`** is an enterprise-grade, domain-agnostic evaluation platform designed to systematically measure the quality, correctness, security, performance, cost, and reliability of Agentic AI applications.

The initial implementation targets the **Travel Planner Agent** system under test, but the core architecture is decoupled and domain-agnostic to evaluate any multi-step AI agent application without structural modifications.

---

## Architecture Overview

The platform is decoupled from agent logic, treating the target agent as an external **System Under Test (SUT)**.

```
Evaluation Dataset (JSON)
        │
        ▼
Evaluation Runner
        │
        ▼
Travel Planner Agent (SUT)
        │ (returns EvaluationContext)
        ▼
Evaluation Pipeline
        │
 ┌──────┼──────────────────────────────────────────────┐
 ▼      ▼      ▼         ▼          ▼        ▼         ▼
Resp   Tool   RAG     Planning   Guard   Perf/Cost   Struct
Eval   Eval   Eval      Eval     rail      Eval      Output
 └──────┴──────┴─────────┴──────────┴────────┴─────────┘
        │
        ▼
Evaluation Score Aggregator (Weighted Normalization)
        │
        ▼
Report Generator (JSON & Multi-Tab Excel Artifacts)
```

---

## Design Principles & Patterns

1. **Clean Architecture**: Clear separation between Domain DTOs, Strategy Evaluators, Application Services, Pipeline Execution, and Infrastructure Exporters.
2. **SOLID Principles**: Single-responsibility evaluators, open-closed design for adding new quality metrics without editing existing code.
3. **Strategy Pattern**: Abstract `Evaluator` interface allows independent evaluation strategies across 8 dimensions.
4. **Factory Pattern**: `EvaluatorFactory` constructs active evaluators dynamically based on configuration flags.
5. **Dependency Injection**: Dataset loaders, pipeline components, agent SUT, and report generators are injected into the `EvaluationRunner`.
6. **Configuration-Driven Execution**: Evaluators can be enabled/disabled via `.env` environment variables and custom weights.

---

## Project Folder Structure

```
agentic-ai-evals/
├── app/
│   ├── config/             # Settings, feature flags & evaluation weight models
│   │   ├── settings.py
│   │   └── weights.py
│   ├── dto/                # Pydantic v2 Data Transfer Objects (Strict typing)
│   │   ├── context.py
│   │   ├── dataset.py
│   │   ├── metrics.py
│   │   ├── report.py
│   │   └── result.py
│   ├── evaluators/         # 8 Quality Dimension Evaluator Strategies
│   │   ├── base.py
│   │   ├── response/
│   │   ├── retrieval/
│   │   ├── tools/
│   │   ├── planning/
│   │   ├── guardrails/
│   │   ├── performance/
│   │   ├── cost/
│   │   └── structured_output/
│   ├── factories/          # EvaluatorFactory instantiator
│   ├── interfaces/         # Abstract Base Classes (Evaluator, Agent, Loader, Reporter)
│   ├── pipeline/           # EvaluationPipeline & ScoreAggregator
│   ├── reports/            # JSON, openpyxl Excel & Composite Report Generators
│   ├── runners/            # EvaluationRunner orchestrator
│   ├── services/           # System Under Test (Travel Planner Agent implementation)
│   ├── utils/              # Structured logging & helpers
│   └── main.py             # CLI Entry point
├── datasets/               # JSON Evaluation Benchmark Test Cases
│   └── travel_planner_eval_dataset.json
├── evaluation-results/     # Output JSON and Excel reports
├── .env.example            # Environment configuration template
├── pyproject.toml          # uv package manager specification
└── README.md               # Enterprise documentation
```

---

## Evaluated Quality Dimensions (8 Dimensions)

| Dimension | Evaluator Class | Evaluated Criteria | Default Weight |
|---|---|---|---|
| **Response** | `ResponseEvaluator` | Correctness (keyword coverage), Completeness, Relevance, Clarity | 30% |
| **Tool Usage** | `ToolEvaluator` | Selection accuracy, execution success, parameter validity, missing/extra tool calls | 20% |
| **Retrieval (RAG)** | `RetrievalEvaluator` | Context relevance, document recall/precision, citation accuracy, top-K correctness | 15% |
| **Planning** | `PlanningEvaluator` | Multi-step ordering, missing steps, extra steps, workflow DAG logic | 10% |
| **Guardrails** | `GuardrailEvaluator` | Prompt injection blocking, jailbreak resistance, unmasked PII detection, harmful output filtering | 10% |
| **Performance** | `PerformanceEvaluator` | Total latency, tool latency, retrieval latency, LLM latency against SLAs | 5% |
| **Cost** | `CostEvaluator` | Input/output/embedding token count, estimated request cost ($), unit economics | 5% |
| **Structured Output**| `StructuredOutputEvaluator` | JSON schema validation, Pydantic DTO compliance, required fields, enum values | 5% |

---

## Dataset Format

Benchmark test cases are defined in structured JSON files (`datasets/travel_planner_eval_dataset.json`):

```json
{
  "id": "travel-001",
  "user_prompt": "Plan a five day trip to Japan visiting Tokyo and Kyoto with flight and hotel bookings.",
  "expected_tools": ["search_flights", "search_hotels"],
  "expected_keywords": ["Tokyo", "Kyoto", "flights", "hotels"],
  "expected_plan": ["search_flights", "search_hotels", "generate_itinerary"],
  "expected_retrieval_docs": ["doc-japan-flights-01", "doc-kyoto-hotels-02"],
  "is_jailbreak_attempt": false
}
```

---

## How to Run

### Prerequisite
Ensure Python 3.12+ and [`uv`](https://github.com/astral-sh/uv) package manager are installed.

### 1. Synchronize Dependencies
```bash
uv sync
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env` to customize feature toggles:
```bash
cp .env.example .env
```

### 3. Run Evaluation Suite
```bash
uv run python app/main.py
```

---

## Configuration Toggles

Individual evaluators can be dynamically enabled or disabled via environment variables:

```env
ENABLE_RESPONSE_EVALUATION=true
ENABLE_TOOL_EVALUATION=true
ENABLE_RETRIEVAL_EVALUATION=true
ENABLE_PLANNING_EVALUATION=true
ENABLE_GUARDRAIL_EVALUATION=true
ENABLE_PERFORMANCE_EVALUATION=true
ENABLE_COST_EVALUATION=true
ENABLE_STRUCTURED_OUTPUT_EVALUATION=true
```

When an evaluator is disabled, `EvaluationScoreAggregator` automatically re-normalizes the remaining active evaluators so total weights sum to 100%.

---

## Adding a New Evaluator

To add a new quality evaluator (e.g. `ToneAndStyleEvaluator`):

1. **Implement `Evaluator` Interface**:
   Create `app/evaluators/style/tone_evaluator.py`:
   ```python
   from app.evaluators.base import BaseEvaluator
   from app.dto.context import EvaluationContext
   from app.dto.result import MetricScore

   class ToneAndStyleEvaluator(BaseEvaluator):
       @property
       def name(self) -> str:
           return "tone_and_style"

       async def evaluate(self, context: EvaluationContext) -> MetricScore:
           # Custom evaluation logic
           return MetricScore(evaluator_name=self.name, score=95.0, weight=0.05)
   ```

2. **Register in `EvaluatorFactory`**:
   Add condition to `app/factories/evaluator_factory.py`.

3. **Enable in Configuration**:
   Add `ENABLE_TONE_EVALUATION=true` in `.env`.

*No existing evaluator files require modification.*

---

## Output Artifacts

Execution generates reports in `evaluation-results/`:
- **`evaluation_report.json`**: Full machine-readable evaluation report with complete metadata and violations.
- **`evaluation_report.xlsx`**: Executive dashboard Excel spreadsheet featuring 3 tabs:
  1. *Executive Summary*: Pass rates, weighted overall score, and dimension breakdowns.
  2. *Test Case Results*: Color-coded pass/fail status per test case with violation details.
  3. *Dimension Metrics*: Detailed scores and sub-metrics across all 8 evaluators.