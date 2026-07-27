from abc import ABC, abstractmethod
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore

class Evaluator(ABC):
    """
    Common Abstract Interface for all quality evaluators.
    Every evaluator must implement async evaluate(context) -> MetricScore.
    No evaluator should know about another evaluator.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns unique identifier for evaluator dimension."""
        pass

    @abstractmethod
    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        """Evaluates given context and returns MetricScore (0-100)."""
        pass
