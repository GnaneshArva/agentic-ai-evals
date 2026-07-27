from app.evaluators.base import BaseEvaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore
from app.dto.metrics import CostMetrics

class CostEvaluator(BaseEvaluator):
    """
    Evaluates token usage economy and cost efficiency:
    - Input tokens
    - Output tokens
    - Embedding tokens
    - Total estimated cost (USD)
    - Average cost per token
    """

    INPUT_TOKEN_PRICE_PER_1K = 0.0015
    OUTPUT_TOKEN_PRICE_PER_1K = 0.0020
    EMBEDDING_TOKEN_PRICE_PER_1K = 0.0001
    MAX_BUDGET_PER_REQUEST_USD = 0.05

    @property
    def name(self) -> str:
        return "cost"

    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        violations: list[str] = []
        cost_m = context.cost_metrics

        input_tokens = cost_m.input_tokens
        output_tokens = cost_m.output_tokens
        embedding_tokens = cost_m.embedding_tokens

        # Calculate unit costs
        input_cost = (input_tokens / 1000.0) * self.INPUT_TOKEN_PRICE_PER_1K
        output_cost = (output_tokens / 1000.0) * self.OUTPUT_TOKEN_PRICE_PER_1K
        emb_cost = (embedding_tokens / 1000.0) * self.EMBEDDING_TOKEN_PRICE_PER_1K

        total_cost = input_cost + output_cost + emb_cost
        total_tokens = input_tokens + output_tokens + embedding_tokens
        avg_cost_per_token = (total_cost / total_tokens) if total_tokens > 0 else 0.0

        score = 100.0

        if total_cost > self.MAX_BUDGET_PER_REQUEST_USD:
            excess = total_cost - self.MAX_BUDGET_PER_REQUEST_USD
            penalty = min(50.0, (excess / self.MAX_BUDGET_PER_REQUEST_USD) * 100.0)
            score -= penalty
            violations.append(f"Request cost (${total_cost:.4f}) exceeded threshold budget of ${self.MAX_BUDGET_PER_REQUEST_USD:.4f}.")

        final_score = max(0.0, min(100.0, score))

        metrics = CostMetrics(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            embedding_tokens=embedding_tokens,
            total_cost_usd=round(total_cost, 6),
            average_cost_per_token_usd=round(avg_cost_per_token, 6),
        )

        return MetricScore(
            evaluator_name=self.name,
            score=round(final_score, 2),
            weight=self.weight,
            weighted_score=round(final_score * self.weight, 2),
            violations=violations,
            details=metrics.model_dump()
        )
