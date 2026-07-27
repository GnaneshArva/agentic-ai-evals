import time
import asyncio
from app.interfaces.agent import AgentInterface
from app.dto.dataset import TestCaseDTO
from app.dto.context import EvaluationContext
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
from app.utils.logger import get_logger

logger = get_logger("travel_planner_agent")

class TravelPlannerAgent(AgentInterface):
    """
    Simulated System Under Test (SUT): Travel Planner Agent.
    Executes input queries, invokes simulated tools (search_flights, search_hotels, etc.),
    retrieves context documents, generates structured itineraries, and captures execution traces.
    """

    @property
    def agent_name(self) -> str:
        return "TravelPlannerAgent-v2"

    async def execute(self, test_case: TestCaseDTO) -> EvaluationContext:
        logger.info(f"TravelPlannerAgent processing prompt: '{test_case.user_prompt}' (ID: {test_case.id})")
        start_time = time.perf_counter()

        # Simulate execution time delay
        await asyncio.sleep(0.05)

        # Handle specific test case simulations
        if test_case.is_jailbreak_attempt:
            # Safe agent response refusing attack
            response_text = "I cannot comply with prompt injection requests or disclose system prompt instructions. I can only assist with travel planning."
            tool_calls = []
            retrieved_docs = []
            retrieved_doc_ids = []
            citations = []
            plan_steps = ["block_adversarial_prompt"]
            structured_out = None
        else:
            # Normal travel planner agent response trace
            response_text = f"Here is your customized travel itinerary for your trip to {', '.join(test_case.expected_keywords or ['Tokyo', 'Kyoto'])}. " \
                            f"We have reserved flights via search_flights and hotels via search_hotels."
            
            tool_calls = [
                {"name": tool_name, "status": "success", "args": {"destination": "Japan", "dates": "2026-08-10"}}
                for tool_name in test_case.expected_tools
            ]
            
            retrieved_doc_ids = test_case.expected_retrieval_docs or ["doc-japan-flights-01", "doc-kyoto-hotels-02"]
            retrieved_docs = [f"Retrieved content for {doc_id}" for doc_id in retrieved_doc_ids]
            citations = [f"Source: {doc_id}" for doc_id in retrieved_doc_ids]
            plan_steps = test_case.expected_plan or ["search_flights", "search_hotels", "generate_itinerary"]
            
            if test_case.schema_definition:
                structured_out = {
                    "destination": "Tokyo, Japan",
                    "duration_days": 5,
                    "estimated_budget_usd": 2500,
                    "status": "CONFIRMED"
                }
            else:
                structured_out = None

        total_lat = (time.perf_counter() - start_time) * 1000.0 + 350.0  # Simulated 350ms base SLA

        context = EvaluationContext(
            test_case=test_case,
            agent_response=response_text,
            tool_calls=tool_calls,
            retrieved_contexts=retrieved_docs,
            retrieved_doc_ids=retrieved_doc_ids,
            citations=citations,
            planning_steps=plan_steps,
            structured_output=structured_out,
            performance_metrics=PerformanceMetrics(
                total_latency_ms=total_lat,
                llm_latency_ms=220.0,
                tool_latency_ms=80.0,
                retrieval_latency_ms=50.0,
            ),
            cost_metrics=CostMetrics(
                input_tokens=450,
                output_tokens=320,
                embedding_tokens=150,
                total_cost_usd=0.0015,
                average_cost_per_token_usd=0.0000016,
            )
        )
        return context
