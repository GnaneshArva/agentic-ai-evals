from abc import ABC, abstractmethod
from app.dto.dataset import TestCaseDTO

class DatasetLoaderInterface(ABC):
    """Interface for dataset loaders."""

    @abstractmethod
    async def load_dataset(self, file_path: str) -> list[TestCaseDTO]:
        """Loads test cases from specified dataset source."""
        pass
