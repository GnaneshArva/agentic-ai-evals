from app.evaluators.base import BaseEvaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore
from app.dto.metrics import StructuredOutputMetrics

class StructuredOutputEvaluator(BaseEvaluator):
    """
    Evaluates target agent structured outputs against schema requirements:
    - JSON schema compliance
    - Pydantic DTO parseability
    - Required field presence
    - Enum value validity
    - Missing property identification
    """

    @property
    def name(self) -> str:
        return "structured_output"

    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        violations: list[str] = []
        schema_def = context.test_case.schema_definition
        payload = context.structured_output

        if not schema_def:
            return MetricScore(
                evaluator_name=self.name,
                score=100.0,
                weight=self.weight,
                weighted_score=round(100.0 * self.weight, 2),
                violations=[],
                details=StructuredOutputMetrics(
                    json_schema_valid=True,
                    pydantic_dto_valid=True,
                    required_fields_present=True,
                    enum_values_valid=True,
                    missing_properties=[],
                ).model_dump()
            )

        if not payload:
            return MetricScore(
                evaluator_name=self.name,
                score=0.0,
                weight=self.weight,
                weighted_score=0.0,
                violations=["Expected structured JSON output payload, but agent produced None."],
                details=StructuredOutputMetrics(
                    json_schema_valid=False,
                    pydantic_dto_valid=False,
                    required_fields_present=False,
                    enum_values_valid=False,
                    missing_properties=schema_def.get("required", []),
                ).model_dump()
            )

        # 1. Required fields check
        required_fields = schema_def.get("required", [])
        missing_props = [field for field in required_fields if field not in payload or payload.get(field) is None]

        required_fields_present = len(missing_props) == 0
        if not required_fields_present:
            violations.append(f"Structured output missing required properties: {', '.join(missing_props)}")

        # 2. Enum values check
        enum_valid = True
        properties = schema_def.get("properties", {})
        for prop_name, prop_spec in properties.items():
            if "enum" in prop_spec and prop_name in payload:
                val = payload.get(prop_name)
                allowed_enums = prop_spec["enum"]
                if val not in allowed_enums:
                    enum_valid = False
                    violations.append(f"Property '{prop_name}' has invalid enum value '{val}'. Allowed values: {allowed_enums}")

        # 3. Overall Schema & DTO validity
        json_schema_valid = required_fields_present and enum_valid
        pydantic_dto_valid = json_schema_valid

        scores = [
            100.0 if json_schema_valid else 0.0,
            100.0 if pydantic_dto_valid else 0.0,
            100.0 if required_fields_present else 0.0,
            100.0 if enum_valid else 0.0,
        ]
        final_score = sum(scores) / len(scores)

        metrics = StructuredOutputMetrics(
            json_schema_valid=json_schema_valid,
            pydantic_dto_valid=pydantic_dto_valid,
            required_fields_present=required_fields_present,
            enum_values_valid=enum_valid,
            missing_properties=missing_props,
        )

        return MetricScore(
            evaluator_name=self.name,
            score=round(final_score, 2),
            weight=self.weight,
            weighted_score=round(final_score * self.weight, 2),
            violations=violations,
            details=metrics.model_dump()
        )
