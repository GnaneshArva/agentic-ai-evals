from typing import Any
from pydantic import BaseModel, Field

class TestCaseDTO(BaseModel):
    id: str = Field(description="Unique identifier for the test case")
    user_prompt: str = Field(description="User prompt or query for the agent under test")
    expected_tools: list[str] = Field(default_factory=list, description="Expected tool names to be called")
    expected_keywords: list[str] = Field(default_factory=list, description="Expected keywords in final response")
    expected_plan: list[str] = Field(default_factory=list, description="Expected planning steps ordering")
    expected_retrieval_docs: list[str] = Field(default_factory=list, description="Expected retrieved document IDs")
    schema_definition: dict[str, Any] | None = Field(default=None, description="Expected JSON schema for structured output evaluation")
    is_jailbreak_attempt: bool = Field(default=False, description="Flag indicating if prompt is a security attack attempt")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional domain metadata")
