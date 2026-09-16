import json

from hybrid_retriever import hybrid_retrieve
from reranker import rerank
from evidence_builder import build_evidence
from response_builder import build_rag_response


query = "What is the minimum income required for a home loan?"

product = "home_loan"


# Retrieve
candidates = hybrid_retrieve(
    query,
    product
)


# Rerank
results = rerank(
    query,
    candidates,
    top_k=3
)


# Build evidence
evidence = build_evidence(
    results
)


# Temporary answer for this practical
answer = "The minimum monthly income required is ₹60,000."


# Build final response
response = build_rag_response(
    answer=answer,
    status="COMPLETED",
    confidence={
        "score": 5.2,
        "margin": 2.1,
        "level": "HIGH"
    },
    review_required=False,
    review_reason=None,
    evidence=evidence
)


print("\n==============================")
print("FINAL STRUCTURED RESPONSE")
print("==============================")


print(
    json.dumps(
        response,
        indent=4,
        ensure_ascii=False
    )
)