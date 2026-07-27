from app.evaluators.base import BaseEvaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore
from app.dto.metrics import PerformanceMetrics

class PerformanceEvaluator(BaseEvaluator):
    """
    Evaluates execution latency against performance SLAs:
    - Total latency
    - Tool latency
    - Retrieval latency
    - LLM latency
    """

    MAX_TOTAL_LATENCY_MS = 5000.0  # 5 second SLA threshold
    MAX_LLM_LATENCY_MS = 3000.0    # 3 second LLM SLA

    @property
    def name(self) -> str:
        return "performance"

    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        violations: list[str] = []
        perf = context.performance_metrics

        total_lat = perf.total_latency_ms
        llm_lat = perf.llm_latency_ms
        tool_lat = perf.tool_latency_ms
        retrieval_lat = perf.retrieval_latency_ms

        score = 100.0

        if total_lat > self.MAX_TOTAL_LATENCY_MS:
            excess = total_lat - self.MAX_TOTAL_LATENCY_MS
            penalty = min(50.0, (excess / 1000.0) * 10.0)
            score -= penalty
            violations.append(f"Total latency ({total_lat:.1f}ms) exceeded SLA limit of {self.MAX_TOTAL_LATENCY_MS}ms.")

        if llm_lat > self.MAX_LLM_LATENCY_MS:
            excess = llm_lat - self.MAX_LLM_LATENCY_MS
            penalty = min(30.0, (excess / 1000.0) * 10.0)
            score -= penalty
            violations.append(f"LLM latency ({llm_lat:.1f}ms) exceeded SLA limit of {self.MAX_LLM_LATENCY_MS}ms.")

        final_score = max(0.0, min(100.0, score))

        metrics = PerformanceMetrics(
            total_latency_ms=round(total_lat, 2),
            tool_latency_ms=round(tool_lat, 2),
            retrieval_latency_ms=round(retrieval_lat, 2),
            llm_latency_ms=round(llm_lat, 2),
        )

        return MetricScore(
            evaluator_name=self.name,
            score=round(final_score, 2),
            weight=self.weight,
            weighted_score=round(final_score * self.weight, 2),
            violations=violations,
            details=metrics.model_dump()
        )
