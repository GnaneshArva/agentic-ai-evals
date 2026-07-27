from datetime import datetime
from pydantic import BaseModel, Field
from app.dto.result import EvaluationResult

class DimensionSummaryDTO(BaseModel):
    evaluator_name: str = Field(description="Name of the evaluator dimension")
    average_score: float = Field(description="Average score across all test cases (0-100)")
    weight: float = Field(description="Dimension weight in overall aggregation")
    weighted_average_score: float = Field(description="Weighted average score contribution")

class EvaluationReportDTO(BaseModel):
    title: str = Field(default="Agentic AI Evaluation Report")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    target_agent: str = Field(default="Travel Planner Agent")
    total_test_cases: int = Field(default=0)
    passed_test_cases: int = Field(default=0)
    failed_test_cases: int = Field(default=0)
    pass_rate_percentage: float = Field(default=0.0)
    overall_weighted_score: float = Field(default=0.0)
    dimension_summaries: list[DimensionSummaryDTO] = Field(default_factory=list)
    results: list[EvaluationResult] = Field(default_factory=list)
    total_violations_count: int = Field(default=0)
    total_duration_ms: float = Field(default=0.0)
