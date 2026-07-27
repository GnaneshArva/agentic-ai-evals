from abc import ABC, abstractmethod
from app.dto.report import EvaluationReportDTO

class ReportGeneratorInterface(ABC):
    """Interface for report exporters (JSON, Excel, etc.)."""

    @abstractmethod
    async def generate_report(self, report: EvaluationReportDTO, output_dir: str) -> str:
        """Persists evaluation report and returns file path."""
        pass
