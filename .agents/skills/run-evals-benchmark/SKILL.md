---
name: run-evals-benchmark
description: Playbook for executing RAGAS, DeepEval, Coherence, and A/B evaluations on agentic-ai-evals.
---

# RAG & Agent Evaluation Benchmark Playbook

This skill provides step-by-step procedures for running production evaluation benchmarks using `agentic-ai-evals`.

## Evaluation Pipeline Steps

1. **Verify Test Suite**:
   ```bash
   cd /Users/gnanesh_arva/Downloads/travel-planner-v2/agentic-ai-evals
   /Users/gnanesh_arva/Downloads/travel-planner-v2/travel-agent-service/.venv/bin/pytest
   ```

2. **Evaluators Supported**:
   - `FaithfulnessEvaluator`: Validates hallucination score against retrieved RAG context.
   - `AnswerRelevancyEvaluator`: Measures answer alignment with user travel intent.
   - `ContextPrecisionEvaluator` & `ContextRecallEvaluator`: Assesses vector retrieval accuracy.
   - `CoherenceEvaluator`: Verifies logical daily sequence and transition smoothness.
   - `ABEvaluationStrategy`: Compares side-by-side prompt variant scores.

3. **Report Generation**:
   Evaluation reports are saved to `agentic-ai-evals/evaluation-results/evaluation_report.json`.
