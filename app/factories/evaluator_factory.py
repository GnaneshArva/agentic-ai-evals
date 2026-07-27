from app.interfaces.evaluator import Evaluator
from app.config.settings import Settings, settings as default_settings
from app.evaluators.response.response_evaluator import ResponseEvaluator
from app.evaluators.tools.tool_evaluator import ToolEvaluator
from app.evaluators.retrieval.retrieval_evaluator import RetrievalEvaluator
from app.evaluators.planning.planning_evaluator import PlanningEvaluator
from app.evaluators.guardrails.guardrail_evaluator import GuardrailEvaluator
from app.evaluators.performance.performance_evaluator import PerformanceEvaluator
from app.evaluators.cost.cost_evaluator import CostEvaluator
from app.evaluators.structured_output.structured_output_evaluator import StructuredOutputEvaluator
from app.utils.logger import get_logger

logger = get_logger("evaluator_factory")

class EvaluatorFactory:
    """
    Factory for instantiating evaluation strategies based on feature toggles.
    Allows easy extension by registering new evaluators.
    """

    def __init__(self, settings_cfg: Settings | None = None):
        self.settings = settings_cfg or default_settings

    def create_evaluators(self) -> list[Evaluator]:
        evaluators: list[Evaluator] = []

        if self.settings.ENABLE_RESPONSE_EVALUATION:
            evaluators.append(ResponseEvaluator())
        if self.settings.ENABLE_TOOL_EVALUATION:
            evaluators.append(ToolEvaluator())
        if self.settings.ENABLE_RETRIEVAL_EVALUATION:
            evaluators.append(RetrievalEvaluator())
        if self.settings.ENABLE_PLANNING_EVALUATION:
            evaluators.append(PlanningEvaluator())
        if self.settings.ENABLE_GUARDRAIL_EVALUATION:
            evaluators.append(GuardrailEvaluator())
        if self.settings.ENABLE_PERFORMANCE_EVALUATION:
            evaluators.append(PerformanceEvaluator())
        if self.settings.ENABLE_COST_EVALUATION:
            evaluators.append(CostEvaluator())
        if self.settings.ENABLE_STRUCTURED_OUTPUT_EVALUATION:
            evaluators.append(StructuredOutputEvaluator())

        logger.info(f"EvaluatorFactory initialized {len(evaluators)} active evaluators: {[e.name for e in evaluators]}")
        return evaluators
