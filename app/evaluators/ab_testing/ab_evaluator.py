from app.evaluators.base import BaseEvaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore


class ABEvaluationStrategy(BaseEvaluator):
    """Evaluates side-by-side prompt variant model outputs to perform A/B quality benchmark comparisons."""

    @property
    def name(self) -> str:
        return "ab_evaluation"

    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        variant_a = context.agent_response.strip()
        variant_b = context.test_case.metadata.get("variant_b_response", "").strip()

        score_a = min(100.0, len(variant_a.split()) * 2.0)
        score_b = min(100.0, len(variant_b.split()) * 2.0) if variant_b else 0.0

        winner = "Variant A" if score_a >= score_b else "Variant B"

        return MetricScore(
            evaluator_name=self.name,
            score=round(score_a, 2),
            weight=self.weight,
            weighted_score=round(score_a * self.weight, 2),
            violations=[] if score_a >= 70.0 else ["Variant A scored below 70 benchmark threshold."],
            details={
                "variant_a_score": score_a,
                "variant_b_score": score_b,
                "winning_variant": winner
            }
        )
