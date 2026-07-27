from app.evaluators.base import BaseEvaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore
from app.dto.metrics import ToolEvaluationResult

class ToolEvaluator(BaseEvaluator):
    """
    Evaluates tool usage accuracy, missing/extra tool calls, parameter validity,
    and tool execution success rates.
    """

    @property
    def name(self) -> str:
        return "tools"

    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        violations: list[str] = []
        expected_tools = context.test_case.expected_tools
        actual_calls = context.tool_calls

        called_tool_names = [call.get("name") for call in actual_calls if isinstance(call, dict) and "name" in call]
        
        # 1. Tool Selection Accuracy
        missing_tools = [tool for tool in expected_tools if tool not in called_tool_names]
        unnecessary_tools = [tool for tool in called_tool_names if tool not in expected_tools]

        if missing_tools:
            violations.append(f"Missing expected tool calls: {', '.join(missing_tools)}")
        if unnecessary_tools:
            violations.append(f"Unnecessary / unexpected tool calls: {', '.join(unnecessary_tools)}")

        total_expected = len(expected_tools)
        if total_expected > 0:
            correct_count = total_expected - len(missing_tools)
            selection_accuracy = max(0.0, (correct_count / total_expected) * 100.0)
            if unnecessary_tools:
                selection_accuracy = max(0.0, selection_accuracy - (len(unnecessary_tools) * 10.0))
        else:
            selection_accuracy = 100.0 if not called_tool_names else 50.0

        # 2. Execution Success Rate
        successful_calls = [c for c in actual_calls if c.get("status") == "success" or c.get("success") is True]
        if actual_calls:
            execution_rate = (len(successful_calls) / len(actual_calls)) * 100.0
            failed_calls = [c.get("name") for c in actual_calls if c not in successful_calls]
            if failed_calls:
                violations.append(f"Tool execution failed for: {', '.join(failed_calls)}")
        else:
            execution_rate = 100.0 if not expected_tools else 0.0

        # 3. Parameter Accuracy
        param_score = 100.0
        for c in actual_calls:
            if not c.get("args") and not c.get("parameters"):
                param_score -= 15.0
                violations.append(f"Tool '{c.get('name')}' called without parameters.")
        param_score = max(0.0, param_score)

        final_score = (selection_accuracy * 0.50) + (execution_rate * 0.30) + (param_score * 0.20)
        final_score = max(0.0, min(100.0, final_score))

        metrics = ToolEvaluationResult(
            tool_selection_accuracy=round(selection_accuracy, 2),
            execution_success_rate=round(execution_rate, 2),
            parameter_accuracy=round(param_score, 2),
            total_tool_calls=len(actual_calls),
            missing_tools=missing_tools,
            unnecessary_tools=unnecessary_tools,
        )

        return MetricScore(
            evaluator_name=self.name,
            score=round(final_score, 2),
            weight=self.weight,
            weighted_score=round(final_score * self.weight, 2),
            violations=violations,
            details=metrics.model_dump()
        )
