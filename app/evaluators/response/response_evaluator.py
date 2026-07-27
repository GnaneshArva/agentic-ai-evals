from app.evaluators.base import BaseEvaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore
from app.dto.metrics import ResponseMetrics

class ResponseEvaluator(BaseEvaluator):
    """
    Evaluates quality of target agent text response across:
    - Correctness (expected keywords present)
    - Completeness (covers prompt expectations)
    - Relevance (topical alignment)
    - Clarity (structure & readability)
    """

    @property
    def name(self) -> str:
        return "response"

    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        violations: list[str] = []
        response_text = context.agent_response.strip()
        expected_keywords = context.test_case.expected_keywords

        if not response_text:
            return MetricScore(
                evaluator_name=self.name,
                score=0.0,
                weight=self.weight,
                weighted_score=0.0,
                violations=["Agent returned empty response."],
                details={"correctness": 0, "completeness": 0, "relevance": 0, "clarity": 0}
            )

        # 1. Correctness (Keyword Coverage)
        found_keywords = [kw for kw in expected_keywords if kw.lower() in response_text.lower()]
        if expected_keywords:
            correctness_score = (len(found_keywords) / len(expected_keywords)) * 100.0
            missing_kw = set(expected_keywords) - set(found_keywords)
            if missing_kw:
                violations.append(f"Missing expected keywords: {', '.join(missing_kw)}")
        else:
            correctness_score = 100.0

        # 2. Completeness (Length & Detail heuristic)
        word_count = len(response_text.split())
        completeness_score = min(100.0, (word_count / 30.0) * 100.0)
        if word_count < 15:
            violations.append("Response is overly brief / incomplete.")

        # 3. Relevance (Prompt terms present in response)
        prompt_words = [w.lower() for w in context.test_case.user_prompt.split() if len(w) > 3]
        relevant_matches = [w for w in prompt_words if w in response_text.lower()]
        relevance_score = (len(relevant_matches) / len(prompt_words) * 100.0) if prompt_words else 100.0
        relevance_score = min(100.0, max(50.0, relevance_score))

        # 4. Clarity (Formatting & Sentence structure)
        clarity_score = 90.0 if any(char in response_text for char in [".", "\n", "- ", "1."]) else 70.0

        # Aggregated dimension score (0-100)
        final_score = (correctness_score * 0.40) + (completeness_score * 0.30) + (relevance_score * 0.20) + (clarity_score * 0.10)
        final_score = max(0.0, min(100.0, final_score))

        metrics = ResponseMetrics(
            correctness_score=round(correctness_score, 2),
            completeness_score=round(completeness_score, 2),
            relevance_score=round(relevance_score, 2),
            clarity_score=round(clarity_score, 2),
        )

        return MetricScore(
            evaluator_name=self.name,
            score=round(final_score, 2),
            weight=self.weight,
            weighted_score=round(final_score * self.weight, 2),
            violations=violations,
            details=metrics.model_dump()
        )
