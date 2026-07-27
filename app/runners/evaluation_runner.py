import time
from app.interfaces.loader import DatasetLoaderInterface
from app.interfaces.agent import AgentInterface
from app.interfaces.reporter import ReportGeneratorInterface
from app.pipeline.evaluation_pipeline import EvaluationPipeline
from app.dto.report import EvaluationReportDTO, DimensionSummaryDTO
from app.dto.result import EvaluationResult
from app.config.weights import default_weights
from app.utils.logger import get_logger

logger = get_logger("evaluation_runner")

class EvaluationRunner:
    """
    Evaluation Runner orchestrates the execution of test cases:
    1. Loads evaluation dataset using DatasetLoader
    2. Executes target agent (System Under Test)
    3. Invokes EvaluationPipeline for multi-dimensional evaluation
    4. Aggregates global scores and dimension metrics
    5. Dispatches EvaluationReportDTO to ReportGenerator
    """

    def __init__(
        self,
        dataset_loader: DatasetLoaderInterface,
        agent: AgentInterface,
        pipeline: EvaluationPipeline,
        report_generator: ReportGeneratorInterface,
    ):
        self.dataset_loader = dataset_loader
        self.agent = agent
        self.pipeline = pipeline
        self.report_generator = report_generator

    async def run_suite(self, dataset_path: str, output_dir: str) -> EvaluationReportDTO:
        start_time = time.perf_counter()
        logger.info(f"Starting evaluation suite execution on dataset: {dataset_path}")

        # 1. Load dataset
        test_cases = await self.dataset_loader.load_dataset(dataset_path)

        # 2. Execute test cases against agent and pipeline
        results: list[EvaluationResult] = []
        for test_case in test_cases:
            context = await self.agent.execute(test_case)
            eval_result = await self.pipeline.execute(context)
            results.append(eval_result)

        # 3. Calculate summary metrics
        total_cases = len(results)
        passed_cases = sum(1 for r in results if r.passed)
        failed_cases = total_cases - passed_cases
        pass_rate = (passed_cases / total_cases * 100.0) if total_cases > 0 else 0.0
        avg_weighted_score = sum(r.weighted_score for r in results) / total_cases if total_cases > 0 else 0.0
        total_violations = sum(len(r.violations) for r in results)

        # 4. Dimension Summaries
        dimension_scores: dict[str, list[float]] = {}
        for r in results:
            for dim_name, m_score in r.metric_scores.items():
                if dim_name not in dimension_scores:
                    dimension_scores[dim_name] = []
                dimension_scores[dim_name].append(m_score.score)

        dimension_summaries: list[DimensionSummaryDTO] = []
        for dim_name, scores in dimension_scores.items():
            avg_score = sum(scores) / len(scores) if scores else 0.0
            weight = default_weights.get_weight(dim_name)
            dimension_summaries.append(
                DimensionSummaryDTO(
                    evaluator_name=dim_name,
                    average_score=round(avg_score, 2),
                    weight=weight,
                    weighted_average_score=round(avg_score * weight, 2),
                )
            )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # 5. Build Report DTO
        report = EvaluationReportDTO(
            target_agent=self.agent.agent_name,
            total_test_cases=total_cases,
            passed_test_cases=passed_cases,
            failed_test_cases=failed_cases,
            pass_rate_percentage=round(pass_rate, 2),
            overall_weighted_score=round(avg_weighted_score, 2),
            dimension_summaries=dimension_summaries,
            results=results,
            total_violations_count=total_violations,
            total_duration_ms=round(elapsed_ms, 2)
        )

        # 6. Export Report Artifacts
        await self.report_generator.generate_report(report, output_dir)

        logger.info(
            f"Evaluation suite finished in {elapsed_ms:.1f}ms. Total: {total_cases}, Passed: {passed_cases}, Pass Rate: {pass_rate:.1f}%, Overall Score: {avg_weighted_score:.2f}"
        )
        return report
