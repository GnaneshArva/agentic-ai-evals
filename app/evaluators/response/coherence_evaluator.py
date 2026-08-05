import re
from app.evaluators.base import BaseEvaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore
from app.dto.metrics import CoherenceMetrics


class CoherenceEvaluator(BaseEvaluator):
    """
    Evaluates logical coherence, paragraph flow, day-by-day sequential continuity,
    and structural non-contradiction across LLM generated agent responses.
    """

    @property
    def name(self) -> str:
        return "coherence"

    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        violations: list[str] = []
        response_text = context.agent_response.strip()

        if not response_text:
            metrics = CoherenceMetrics(
                sequential_continuity_score=0.0,
                structural_flow_score=0.0,
                non_contradiction_score=0.0,
                coherence_score=0.0,
                issues_detected=["Response text is empty."]
            )
            return MetricScore(
                evaluator_name=self.name,
                score=0.0,
                weight=self.weight,
                weighted_score=0.0,
                violations=["Agent returned empty response."],
                details=metrics.model_dump()
            )

        # 1. Sequential Continuity Check (Day numbers sequence)
        day_numbers = [int(m) for m in re.findall(r"(?:Day|day)\s*(\d+)", response_text)]
        sequence_issues: list[str] = []
        sequential_score = 100.0

        if day_numbers:
            for i in range(1, len(day_numbers)):
                prev_d = day_numbers[i - 1]
                curr_d = day_numbers[i]
                if curr_d < prev_d:
                    sequence_issues.append(f"Out-of-order timeline jump: Day {curr_d} follows Day {prev_d}.")
                elif curr_d > prev_d + 2:
                    sequence_issues.append(f"Timeline gap detected: Jumped from Day {prev_d} directly to Day {curr_d}.")

            if sequence_issues:
                sequential_score = max(0.0, 100.0 - (len(sequence_issues) * 50.0))
                violations.extend(sequence_issues)

        # 2. Structural Flow & Formatting
        paragraphs = [p.strip() for p in response_text.split("\n\n") if p.strip()]
        flow_score = 100.0
        if len(paragraphs) == 1 and len(response_text.split()) > 150:
            flow_score = 70.0
            violations.append("Monolithic block text without logical section paragraph breaks.")

        # 3. Non-contradiction Heuristic
        contradiction_issues: list[str] = []
        non_contradiction_score = 100.0
        
        # Check if single short response claims contradictory timeline or distant location jumps without explanation
        cities = re.findall(r"\b(?:Tokyo|Paris|Rome|London|New York|Zurich|Bern|Geneva)\b", response_text, re.IGNORECASE)
        unique_cities = set([c.lower() for c in cities])
        if len(unique_cities) > 3 and "day 1" in response_text.lower() and "day 2" not in response_text.lower():
            contradiction_issues.append("Unrealistic distant location jumps within single day timeframe.")
            non_contradiction_score = 50.0
            violations.extend(contradiction_issues)

        # Aggregated Coherence Score (0-100)
        coherence_score = (sequential_score * 0.50) + (flow_score * 0.30) + (non_contradiction_score * 0.20)
        coherence_score = round(max(0.0, min(100.0, coherence_score)), 2)

        all_issues = sequence_issues + ([ "Monolithic paragraph block." ] if flow_score < 100.0 else []) + contradiction_issues

        metrics = CoherenceMetrics(
            sequential_continuity_score=round(sequential_score, 2),
            structural_flow_score=round(flow_score, 2),
            non_contradiction_score=round(non_contradiction_score, 2),
            coherence_score=coherence_score,
            issues_detected=all_issues
        )

        return MetricScore(
            evaluator_name=self.name,
            score=coherence_score,
            weight=self.weight,
            weighted_score=round(coherence_score * self.weight, 2),
            violations=violations,
            details=metrics.model_dump()
        )
