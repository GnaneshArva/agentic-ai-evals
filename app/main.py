import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config.settings import settings
from app.factories.evaluator_factory import EvaluatorFactory
from app.pipeline.evaluation_pipeline import EvaluationPipeline
from app.datasets.loader import JSONDatasetLoader
from app.services.travel_planner_agent import TravelPlannerAgent
from app.reports.composite_reporter import CompositeReportGenerator
from app.runners.evaluation_runner import EvaluationRunner
from app.utils.logger import get_logger

logger = get_logger("main")

async def main():
    logger.info("=========================================================")
    logger.info("  Starting Agentic AI Evaluation Platform (agentic-ai-evals) ")
    logger.info("=========================================================")

    # 1. Dependency Injection Setup
    dataset_loader = JSONDatasetLoader()
    agent_under_test = TravelPlannerAgent()

    evaluator_factory = EvaluatorFactory(settings)
    evaluators = evaluator_factory.create_evaluators()

    pipeline = EvaluationPipeline(evaluators=evaluators)
    report_generator = CompositeReportGenerator()

    runner = EvaluationRunner(
        dataset_loader=dataset_loader,
        agent=agent_under_test,
        pipeline=pipeline,
        report_generator=report_generator
    )

    # 2. Run Evaluation Suite
    report = await runner.run_suite(
        dataset_path=settings.DATASET_PATH,
        output_dir=settings.RESULTS_DIR
    )

    # 3. Output Summary Dashboard to Console
    print("\n" + "=" * 68)
    print(f"        AGENTIC AI EVALUATION SUMMARY REPORT ({report.target_agent})")
    print("=" * 68)
    print(f" Timestamp:              {report.timestamp}")
    print(f" Total Test Cases:       {report.total_test_cases}")
    print(f" Passed:                 {report.passed_test_cases}")
    print(f" Failed:                 {report.failed_test_cases}")
    print(f" Pass Rate:              {report.pass_rate_percentage:.1f}%")
    print(f" Overall Weighted Score: {report.overall_weighted_score:.2f} / 100")
    print(f" Total Violations:       {report.total_violations_count}")
    print("-" * 68)
    print(" DIMENSION SCORE BREAKDOWN:")
    for dim in report.dimension_summaries:
        print(f"  - {dim.evaluator_name.capitalize():<20}: Avg Score = {dim.average_score:>5.1f} | Weight = {dim.weight*100:>2.0f}% | Contribution = {dim.weighted_average_score:>5.2f}")
    print("=" * 68)
    print(f" Artifacts generated in: {Path(settings.RESULTS_DIR).resolve()}")
    print("  - JSON:  evaluation_report.json")
    print("  - Excel: evaluation_report.xlsx")
    print("=" * 68 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
