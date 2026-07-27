from abc import ABC
from app.interfaces.evaluator import Evaluator
from app.config.weights import default_weights

class BaseEvaluator(Evaluator, ABC):
    """Base class providing weight resolution helper."""

    @property
    def weight(self) -> float:
        return default_weights.get_weight(self.name)
