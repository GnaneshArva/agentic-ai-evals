from typing import Any
from pydantic import BaseModel, Field

from app.dto.dataset import TestCaseDTO
from app.dto.metrics import (
    ResponseMetrics,
    ToolEvaluationResult,
    RetrievalEvaluationResult,
    PlanningMetrics,
    GuardrailMetrics,
    PerformanceMetrics,
    CostMetrics,
    StructuredOutputMetrics,
)

class EvaluationContext(BaseModel):
    test_case: TestCaseDTO = Field(description="Associated test case specification")
    agent_response: str = Field(default="", description="Text response produced by target agent")
    tool_calls: list[dict[str, Any]] = Field(default_factory=list, description="Actual tool calls made by target agent")
    retrieved_contexts: list[str] = Field(default_factory=list, description="Context documents retrieved during RAG")
    retrieved_doc_ids: list[str] = Field(default_factory=list, description="IDs of retrieved documents")
    citations: list[str] = Field(default_factory=list, description="Citations referenced in agent response")
    planning_steps: list[str] = Field(default_factory=list, description="Planning steps executed by agent")
    structured_output: dict[str, Any] | None = Field(default=None, description="Structured output payload if applicable")
    
    # Execution metrics collected from agent trace
    response_metrics: ResponseMetrics = Field(default_factory=ResponseMetrics)
    tool_metrics: ToolEvaluationResult = Field(default_factory=ToolEvaluationResult)
    retrieval_metrics: RetrievalEvaluationResult = Field(default_factory=RetrievalEvaluationResult)
    planning_metrics: PlanningMetrics = Field(default_factory=PlanningMetrics)
    guardrail_metrics: GuardrailMetrics = Field(default_factory=GuardrailMetrics)
    performance_metrics: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    cost_metrics: CostMetrics = Field(default_factory=CostMetrics)
    structured_output_metrics: StructuredOutputMetrics = Field(default_factory=StructuredOutputMetrics)
