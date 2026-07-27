from pydantic import BaseModel, Field

class ResponseMetrics(BaseModel):
    correctness_score: float = Field(default=0.0)
    completeness_score: float = Field(default=0.0)
    relevance_score: float = Field(default=0.0)
    clarity_score: float = Field(default=0.0)

class ToolEvaluationResult(BaseModel):
    tool_selection_accuracy: float = Field(default=0.0)
    execution_success_rate: float = Field(default=0.0)
    parameter_accuracy: float = Field(default=0.0)
    total_tool_calls: int = Field(default=0)
    missing_tools: list[str] = Field(default_factory=list)
    unnecessary_tools: list[str] = Field(default_factory=list)

class RetrievalEvaluationResult(BaseModel):
    context_relevance: float = Field(default=0.0)
    retrieved_documents_recall: float = Field(default=0.0)
    citation_accuracy: float = Field(default=0.0)
    top_k_correctness: float = Field(default=0.0)
    grounding_quality: float = Field(default=0.0)

class PlanningMetrics(BaseModel):
    step_ordering_score: float = Field(default=0.0)
    missing_steps: list[str] = Field(default_factory=list)
    extra_steps: list[str] = Field(default_factory=list)
    workflow_correctness: float = Field(default=0.0)

class GuardrailMetrics(BaseModel):
    prompt_injection_blocked: bool = Field(default=True)
    jailbreak_blocked: bool = Field(default=True)
    pii_masked: bool = Field(default=True)
    harmful_output_blocked: bool = Field(default=True)

class PerformanceMetrics(BaseModel):
    total_latency_ms: float = Field(default=0.0)
    tool_latency_ms: float = Field(default=0.0)
    retrieval_latency_ms: float = Field(default=0.0)
    llm_latency_ms: float = Field(default=0.0)

class CostMetrics(BaseModel):
    input_tokens: int = Field(default=0)
    output_tokens: int = Field(default=0)
    embedding_tokens: int = Field(default=0)
    total_cost_usd: float = Field(default=0.0)
    average_cost_per_token_usd: float = Field(default=0.0)

class StructuredOutputMetrics(BaseModel):
    json_schema_valid: bool = Field(default=True)
    pydantic_dto_valid: bool = Field(default=True)
    required_fields_present: bool = Field(default=True)
    enum_values_valid: bool = Field(default=True)
    missing_properties: list[str] = Field(default_factory=list)
