import pytest
from app.dto.context import EvaluationContext
from app.dto.dataset import TestCaseDTO
from app.evaluators.response.coherence_evaluator import CoherenceEvaluator

@pytest.mark.anyio
async def test_coherence_evaluator_high_score():
    evaluator = CoherenceEvaluator()
    test_case = TestCaseDTO(
        id="tc1",
        user_prompt="Plan a trip to Rome",
        expected_keywords=["Rome", "Colosseum"]
    )
    context = EvaluationContext(
        test_case=test_case,
        agent_response="Day 1: Arrive in Rome.\n\nDay 2: Tour the Colosseum.\n\nDay 3: Departure."
    )
    res = await evaluator.evaluate(context)

    assert res.evaluator_name == "coherence"
    assert res.score >= 80.0
    assert len(res.violations) == 0

@pytest.mark.anyio
async def test_coherence_evaluator_out_of_order():
    evaluator = CoherenceEvaluator()
    test_case = TestCaseDTO(
        id="tc2",
        user_prompt="Plan a trip to Rome",
        expected_keywords=[]
    )
    context = EvaluationContext(
        test_case=test_case,
        agent_response="Day 3: Return flight.\n\nDay 1: Arrive in Rome."
    )
    res = await evaluator.evaluate(context)

    assert res.evaluator_name == "coherence"
    assert res.score < 80.0
    assert len(res.violations) > 0
