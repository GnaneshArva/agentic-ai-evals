from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ENABLE_RESPONSE_EVALUATION: bool = Field(default=True)
    ENABLE_TOOL_EVALUATION: bool = Field(default=True)
    ENABLE_RETRIEVAL_EVALUATION: bool = Field(default=True)
    ENABLE_PLANNING_EVALUATION: bool = Field(default=True)
    ENABLE_GUARDRAIL_EVALUATION: bool = Field(default=True)
    ENABLE_PERFORMANCE_EVALUATION: bool = Field(default=True)
    ENABLE_COST_EVALUATION: bool = Field(default=True)
    ENABLE_STRUCTURED_OUTPUT_EVALUATION: bool = Field(default=True)
    ENABLE_COHERENCE_EVALUATION: bool = Field(default=True)

    RESULTS_DIR: str = Field(default="evaluation-results")
    DATASET_PATH: str = Field(default="datasets/travel_planner_eval_dataset.json")
    LOG_LEVEL: str = Field(default="INFO")

    # Agent connection mode: "simulated" (default) or "http" (calls real agent)
    AGENT_MODE: str = Field(default="simulated", description="simulated or http")
    AGENT_BASE_URL: str = Field(default="http://localhost:8000", description="Base URL of travel-agent-service")

settings = Settings()
