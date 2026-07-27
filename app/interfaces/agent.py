from abc import ABC, abstractmethod
from app.dto.dataset import TestCaseDTO
from app.dto.context import EvaluationContext

class AgentInterface(ABC):
    """
    Interface for System Under Test (SUT).
    Decouples the evaluation platform from target agent implementation.
    """

    @property
    @abstractmethod
    def agent_name(self) -> str:
        pass

    @abstractmethod
    async def execute(self, test_case: TestCaseDTO) -> EvaluationContext:
        """Executes a test case against the target agent and returns execution context trace."""
        pass
