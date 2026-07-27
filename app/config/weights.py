from pydantic import BaseModel, Field

class EvaluatorWeights(BaseModel):
    response: float = Field(default=0.30, description="Weight for Response Evaluator (0-1)")
    tools: float = Field(default=0.20, description="Weight for Tool Evaluator (0-1)")
    retrieval: float = Field(default=0.15, description="Weight for Retrieval Evaluator (0-1)")
    planning: float = Field(default=0.10, description="Weight for Planning Evaluator (0-1)")
    guardrails: float = Field(default=0.10, description="Weight for Guardrail Evaluator (0-1)")
    performance: float = Field(default=0.05, description="Weight for Performance Evaluator (0-1)")
    cost: float = Field(default=0.05, description="Weight for Cost Evaluator (0-1)")
    structured_output: float = Field(default=0.05, description="Weight for Structured Output Evaluator (0-1)")

    def get_weight(self, evaluator_name: str) -> float:
        mapping = {
            "response": self.response,
            "tools": self.tools,
            "retrieval": self.retrieval,
            "planning": self.planning,
            "guardrails": self.guardrails,
            "performance": self.performance,
            "cost": self.cost,
            "structured_output": self.structured_output,
        }
        return mapping.get(evaluator_name.lower(), 0.0)

default_weights = EvaluatorWeights()
