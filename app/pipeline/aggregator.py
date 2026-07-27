from app.dto.result import MetricScore, EvaluationResult
from app.config.weights import EvaluatorWeights, default_weights

class EvaluationScoreAggregator:
    """
    Aggregates metric scores across evaluator strategies using configurable weights.
    Calculates both unweighted average score and normalized weighted overall score.
    """

    def __init__(self, weights: EvaluatorWeights | None = None):
        self.weights = weights or default_weights

    def aggregate(
        self,
        test_case_id: str,
        metric_scores: list[MetricScore],
        execution_time_ms: float = 0.0,
        pass_threshold: float = 70.0
    ) -> EvaluationResult:
        if not metric_scores:
            return EvaluationResult(
                test_case_id=test_case_id,
                overall_score=0.0,
                weighted_score=0.0,
                passed=False,
                metric_scores={},
                violations=["No metric scores provided for aggregation."],
                execution_time_ms=execution_time_ms
            )

        scores_dict: dict[str, MetricScore] = {}
        all_violations: list[str] = []
        total_raw_score = 0.0
        total_weighted_score = 0.0
        total_active_weight = 0.0

        for metric in metric_scores:
            scores_dict[metric.evaluator_name] = metric
            all_violations.extend(metric.violations)
            total_raw_score += metric.score

            weight = self.weights.get_weight(metric.evaluator_name)
            total_weighted_score += metric.score * weight
            total_active_weight += weight

        # Normalize weighted score if active evaluators don't sum to 1.0 (e.g. when some are disabled)
        if total_active_weight > 0.0:
            final_weighted_score = total_weighted_score / total_active_weight
        else:
            final_weighted_score = 0.0

        overall_unweighted_score = total_raw_score / len(metric_scores)
        passed = final_weighted_score >= pass_threshold and len(all_violations) == 0

        return EvaluationResult(
            test_case_id=test_case_id,
            overall_score=round(overall_unweighted_score, 2),
            weighted_score=round(final_weighted_score, 2),
            passed=passed,
            metric_scores=scores_dict,
            violations=all_violations,
            execution_time_ms=round(execution_time_ms, 2)
        )
