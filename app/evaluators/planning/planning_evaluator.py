from app.evaluators.base import BaseEvaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore
from app.dto.metrics import PlanningMetrics

class PlanningEvaluator(BaseEvaluator):
    """
    Evaluates multi-step planning and workflow execution:
    - Step ordering correctness
    - Missing workflow steps
    - Extra redundant steps
    - Sequential workflow DAG logic
    """

    @property
    def name(self) -> str:
        return "planning"

    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        violations: list[str] = []
        expected_plan = context.test_case.expected_plan
        actual_plan = context.planning_steps

        if not expected_plan and not actual_plan:
            return MetricScore(
                evaluator_name=self.name,
                score=100.0,
                weight=self.weight,
                weighted_score=round(100.0 * self.weight, 2),
                violations=[],
                details=PlanningMetrics(
                    step_ordering_score=100.0,
                    missing_steps=[],
                    extra_steps=[],
                    workflow_correctness=100.0,
                ).model_dump()
            )

        # 1. Missing & Extra Steps
        missing_steps = [step for step in expected_plan if step not in actual_plan]
        extra_steps = [step for step in actual_plan if step not in expected_plan]

        if missing_steps:
            violations.append(f"Missing required planning steps: {', '.join(missing_steps)}")
        if extra_steps:
            violations.append(f"Extra unplanned steps executed: {', '.join(extra_steps)}")

        # 2. Step Ordering Score (Sequence Alignment)
        ordering_score = 100.0
        if expected_plan and actual_plan:
            last_idx = -1
            out_of_order = []
            for step in expected_plan:
                if step in actual_plan:
                    current_idx = actual_plan.index(step)
                    if current_idx < last_idx:
                        out_of_order.append(step)
                    last_idx = max(last_idx, current_idx)
            if out_of_order:
                ordering_score = max(0.0, 100.0 - (len(out_of_order) * 25.0))
                violations.append(f"Steps executed out of order: {', '.join(out_of_order)}")

        # 3. Overall Workflow Correctness
        total_expected = len(expected_plan)
        if total_expected > 0:
            coverage = ((total_expected - len(missing_steps)) / total_expected) * 100.0
            workflow_score = (coverage * 0.6) + (ordering_score * 0.4)
        else:
            workflow_score = 100.0 if not actual_plan else 70.0

        final_score = max(0.0, min(100.0, workflow_score))

        metrics = PlanningMetrics(
            step_ordering_score=round(ordering_score, 2),
            missing_steps=missing_steps,
            extra_steps=extra_steps,
            workflow_correctness=round(final_score, 2),
        )

        return MetricScore(
            evaluator_name=self.name,
            score=round(final_score, 2),
            weight=self.weight,
            weighted_score=round(final_score * self.weight, 2),
            violations=violations,
            details=metrics.model_dump()
        )
