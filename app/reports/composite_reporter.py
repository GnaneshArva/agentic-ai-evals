from app.interfaces.reporter import ReportGeneratorInterface
from app.dto.report import EvaluationReportDTO
from app.reports.json_reporter import JSONReportGenerator
from app.reports.excel_reporter import ExcelReportGenerator
from app.utils.logger import get_logger

logger = get_logger("composite_reporter")

class CompositeReportGenerator(ReportGeneratorInterface):
    """Combines JSON and Excel report generators to produce all required report formats."""

    def __init__(self, reporters: list[ReportGeneratorInterface] | None = None):
        self.reporters = reporters or [JSONReportGenerator(), ExcelReportGenerator()]

    async def generate_report(self, report: EvaluationReportDTO, output_dir: str) -> str:
        paths = []
        for reporter in self.reporters:
            path = await reporter.generate_report(report, output_dir)
            paths.append(path)
        logger.info(f"Generated {len(paths)} evaluation reports in '{output_dir}'.")
        return ", ".join(paths)
