import asyncio
import time
from app.interfaces.evaluator import Evaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore, EvaluationResult
from app.pipeline.aggregator import EvaluationScoreAggregator
from app.utils.logger import get_logger

logger = get_logger("evaluation_pipeline")

class EvaluationPipeline:
    """
    Evaluation Pipeline that executes evaluator strategies independently
    and aggregates scores into a single EvaluationResult.
    """

    def __init__(
        self,
        evaluators: list[Evaluator],
        aggregator: EvaluationScoreAggregator | None = None
    ):
        self.evaluators = evaluators
        self.aggregator = aggregator or EvaluationScoreAggregator()

    async def execute(self, context: EvaluationContext) -> EvaluationResult:
        start_time = time.perf_counter()
        logger.info(f"Running evaluation pipeline for test case '{context.test_case.id}' across {len(self.evaluators)} evaluators...")

        # Concurrently execute all configured evaluators independently
        tasks = [evaluator.evaluate(context) for evaluator in self.evaluators]
        metric_scores: list[MetricScore] = await asyncio.gather(*tasks)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Aggregate metric scores
        result = self.aggregator.aggregate(
            test_case_id=context.test_case.id,
            metric_scores=metric_scores,
            execution_time_ms=elapsed_ms
        )

        logger.info(f"Evaluation pipeline completed for '{context.test_case.id}': Weighted Score={result.weighted_score}, Passed={result.passed}")
        return result
