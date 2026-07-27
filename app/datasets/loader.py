import json
from pathlib import Path
from app.interfaces.loader import DatasetLoaderInterface
from app.dto.dataset import TestCaseDTO
from app.utils.logger import get_logger

logger = get_logger("dataset_loader")

class JSONDatasetLoader(DatasetLoaderInterface):
    """
    Extensible JSON dataset loader that parses evaluation benchmark test cases into TestCaseDTO objects.
    """

    async def load_dataset(self, file_path: str) -> list[TestCaseDTO]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found at path: {file_path}")

        logger.info(f"Loading dataset from: {file_path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict) and "test_cases" in data:
            raw_cases = data["test_cases"]
        elif isinstance(data, list):
            raw_cases = data
        else:
            raise ValueError("Invalid JSON dataset format. Expected list of test cases or dict with 'test_cases'.")

        test_cases = [TestCaseDTO.model_validate(item) for item in raw_cases]
        logger.info(f"Successfully loaded {len(test_cases)} test cases.")
        return test_cases
