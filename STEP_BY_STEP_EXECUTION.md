# Step-by-Step Execution Architecture (`agentic-ai-evals`)

## Purpose
`agentic-ai-evals` is an offline evaluation platform. It systematically benchmarks Agentic AI applications across 8 quality dimensions (response quality, tool selection, RAG grounding, planning, security guardrails, performance, cost, and structured output compliance) without embedding test logic inside the agent.

---

## Step-by-Step Evaluation Flow

```
Dataset JSON ──► [1. Test Case Ingestion] ──► [2. SUT Execution] ──► [3. 8-Dim Pipeline] ──► [4. Score Aggregation] ──► [5. Report Export]
```

### Step 1: Benchmark Dataset Loading
- `DatasetLoader` parses benchmark test cases (`TestCaseDTO`) from `datasets/travel_planner_eval_dataset.json`.
- Each test case defines expected tools, required keywords, RAG reference docs, planning sequences, and JSON output schemas.

### Step 2: System Under Test (SUT) Invocation
- `EvaluationRunner` calls `travel-agent-service` endpoint `POST /api/v1/travel/evaluate`.
- Captures full `EvalTraceResponse` containing agent output, tool calls, RAG documents, latency, token usage, and cost metrics.

### Step 3: Concurrent 8-Dimension Evaluation Pipeline
Runs evaluators in parallel:
1. **`ResponseEvaluator`**: Measures relevance, completeness, and tone against expected keywords.
2. **`ToolEvaluator`**: Evaluates tool selection accuracy, extra tool calls, and execution status.
3. **`RagEvaluator`**: Measures RAG context relevance, faithfulness, and grounding scores.
4. **`PlanningEvaluator`**: Verifies step-by-step plan sequence ordering.
5. **`GuardrailEvaluator`**: Checks whether security guardrails allowed or blocked response appropriately.
6. **`PerformanceCostEvaluator`**: Assesses latency bounds and token cost efficiency.
7. **`StructuredOutputEvaluator`**: Validates JSON schema compliance.

### Step 4: Weighted Score Aggregation
- `ScoreAggregator` calculates normalized metric scores (0-100) using configured weight settings (`weights.py`).
- Determines overall pass/fail status based on threshold rules.

### Step 5: Report Generation & Export
- `ReportGenerator` exports structured results to `evaluation-results/`:
  - **JSON Report**: Machine-readable diagnostic logs.
  - **Excel Report (`.xlsx`)**: Multi-tab summary and detailed failure breakdowns.
