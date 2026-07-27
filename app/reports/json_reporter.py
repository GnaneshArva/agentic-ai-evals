import json
from pathlib import Path
from app.interfaces.reporter import ReportGeneratorInterface
from app.dto.report import EvaluationReportDTO
from app.utils.logger import get_logger

logger = get_logger("json_reporter")

class JSONReportGenerator(ReportGeneratorInterface):
    """Generates and exports evaluation report as formatted JSON."""

    async def generate_report(self, report: EvaluationReportDTO, output_dir: str) -> str:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        file_path = out_path / "evaluation_report.json"

        report_dict = report.model_dump()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, indent=2)

        logger.info(f"JSON evaluation report saved to: {file_path.resolve()}")
        return str(file_path.resolve())
