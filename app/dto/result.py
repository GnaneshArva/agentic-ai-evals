from typing import Any
from pydantic import BaseModel, Field

class MetricScore(BaseModel):
    evaluator_name: str = Field(description="Name of the evaluator dimension")
    score: float = Field(description="Score between 0 and 100")
    weight: float = Field(default=0.0, description="Configured weight for this evaluator (0-1)")
    weighted_score: float = Field(default=0.0, description="Score * weight")
    violations: list[str] = Field(default_factory=list, description="List of rule violations or failures")
    details: dict[str, Any] = Field(default_factory=dict, description="Detailed diagnostic metrics")

class EvaluationResult(BaseModel):
    test_case_id: str = Field(description="Test case ID")
    overall_score: float = Field(default=0.0, description="Unweighted average score (0-100)")
    weighted_score: float = Field(default=0.0, description="Final weighted score (0-100)")
    passed: bool = Field(default=True, description="Whether test case met passing threshold")
    metric_scores: dict[str, MetricScore] = Field(default_factory=dict, description="Metric scores indexed by evaluator name")
    violations: list[str] = Field(default_factory=list, description="All accumulated violations for test case")
    execution_time_ms: float = Field(default=0.0, description="Time taken to evaluate this test case")
