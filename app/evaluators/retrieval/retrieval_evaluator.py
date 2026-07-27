from app.evaluators.base import BaseEvaluator
from app.dto.context import EvaluationContext
from app.dto.result import MetricScore
from app.dto.metrics import RetrievalEvaluationResult

class RetrievalEvaluator(BaseEvaluator):
    """
    Evaluates RAG retrieval performance:
    - Context relevance
    - Retrieved documents recall/precision vs expected doc IDs
    - Citation accuracy
    - Top-K correctness
    - Grounding quality
    """

    @property
    def name(self) -> str:
        return "retrieval"

    async def evaluate(self, context: EvaluationContext) -> MetricScore:
        violations: list[str] = []
        expected_docs = context.test_case.expected_retrieval_docs
        actual_docs = context.retrieved_doc_ids
        retrieved_contexts = context.retrieved_contexts

        if not expected_docs and not actual_docs:
            return MetricScore(
                evaluator_name=self.name,
                score=100.0,
                weight=self.weight,
                weighted_score=round(100.0 * self.weight, 2),
                violations=[],
                details=RetrievalEvaluationResult(
                    context_relevance=100.0,
                    retrieved_documents_recall=100.0,
                    citation_accuracy=100.0,
                    top_k_correctness=100.0,
                    grounding_quality=100.0,
                ).model_dump()
            )

        # 1. Document Recall & Precision
        if expected_docs:
            matched_docs = [doc for doc in expected_docs if doc in actual_docs]
            recall = (len(matched_docs) / len(expected_docs)) * 100.0
            missing_docs = set(expected_docs) - set(matched_docs)
            if missing_docs:
                violations.append(f"Missing expected RAG documents: {', '.join(missing_docs)}")
        else:
            recall = 100.0

        # 2. Top-K Correctness (Check if first expected document is in top 1 or top K)
        if expected_docs and actual_docs:
            top_1_correct = actual_docs[0] == expected_docs[0]
            top_k_score = 100.0 if top_1_correct else (70.0 if expected_docs[0] in actual_docs else 0.0)
            if not top_1_correct:
                violations.append(f"Top-1 retrieved document '{actual_docs[0]}' did not match expected top document '{expected_docs[0]}'.")
        else:
            top_k_score = 100.0

        # 3. Context Relevance
        context_relevance = 90.0 if retrieved_contexts else (50.0 if expected_docs else 100.0)

        # 4. Citation Accuracy & Grounding
        citations = context.citations
        agent_resp = context.agent_response.lower()
        if citations:
            valid_citations = [c for c in citations if c.lower() in agent_resp or any(c in doc for doc in actual_docs)]
            citation_accuracy = (len(valid_citations) / len(citations)) * 100.0
        else:
            citation_accuracy = 90.0

        grounding_quality = (recall * 0.5) + (context_relevance * 0.5)

        final_score = (recall * 0.35) + (top_k_score * 0.25) + (context_relevance * 0.20) + (citation_accuracy * 0.10) + (grounding_quality * 0.10)
        final_score = max(0.0, min(100.0, final_score))

        metrics = RetrievalEvaluationResult(
            context_relevance=round(context_relevance, 2),
            retrieved_documents_recall=round(recall, 2),
            citation_accuracy=round(citation_accuracy, 2),
            top_k_correctness=round(top_k_score, 2),
            grounding_quality=round(grounding_quality, 2),
        )

        return MetricScore(
            evaluator_name=self.name,
            score=round(final_score, 2),
            weight=self.weight,
            weighted_score=round(final_score * self.weight, 2),
            violations=violations,
            details=metrics.model_dump()
        )
