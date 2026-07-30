import httpx
from app.interfaces.agent import AgentInterface
from app.dto.dataset import TestCaseDTO
from app.dto.context import EvaluationContext
from app.dto.metrics import (
    PerformanceMetrics,
    CostMetrics,
)
from app.utils.logger import get_logger

logger = get_logger("http_agent_client")


class HttpAgentClient(AgentInterface):
    """
    AgentInterface implementation that calls the real travel-agent-service
    via HTTP POST /api/v1/travel/evaluate and maps the trace response
    into an EvaluationContext for the evaluation pipeline.
    """

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @property
    def agent_name(self) -> str:
        return "TravelPlannerAgent-v2-HTTP"

    async def execute(self, test_case: TestCaseDTO) -> EvaluationContext:
        logger.info(f"Sending eval request to {self.base_url} for test case: {test_case.id}")

        # Build the eval request payload
        payload = {
            "user_prompt": test_case.user_prompt,
            "is_jailbreak_attempt": test_case.is_jailbreak_attempt,
        }
        if test_case.schema_definition:
            payload["schema_definition"] = test_case.schema_definition

        # Call the real agent
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/travel/evaluate",
                json=payload,
            )
            response.raise_for_status()
            trace = response.json()

        logger.info(f"Received trace response for test case: {test_case.id}")

        # Map the trace response → EvaluationContext
        perf = trace.get("performance", {})
        cost = trace.get("cost", {})

        context = EvaluationContext(
            test_case=test_case,
            agent_response=trace.get("agent_response", ""),
            tool_calls=trace.get("tool_calls", []),
            retrieved_contexts=trace.get("retrieved_contexts", []),
            retrieved_doc_ids=trace.get("retrieved_doc_ids", []),
            citations=trace.get("citations", []),
            planning_steps=trace.get("planning_steps", []),
            structured_output=trace.get("structured_output"),
            performance_metrics=PerformanceMetrics(
                total_latency_ms=perf.get("total_latency_ms", 0.0),
                llm_latency_ms=perf.get("llm_latency_ms", 0.0),
                tool_latency_ms=perf.get("tool_latency_ms", 0.0),
                retrieval_latency_ms=perf.get("retrieval_latency_ms", 0.0),
            ),
            cost_metrics=CostMetrics(
                input_tokens=cost.get("input_tokens", 0),
                output_tokens=cost.get("output_tokens", 0),
                embedding_tokens=cost.get("embedding_tokens", 0),
                total_cost_usd=cost.get("total_cost_usd", 0.0),
                average_cost_per_token_usd=cost.get("average_cost_per_token_usd", 0.0),
            ),
        )

        return context
