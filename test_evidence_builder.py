import json

from hybrid_retriever import hybrid_retrieve
from reranker import rerank
from evidence_builder import build_evidence


query = "What is the minimum income required for a home loan?"

product = "home_loan"


candidates = hybrid_retrieve(
    query,
    product
)


results = rerank(
    query,
    candidates,
    top_k=3
)


evidence = build_evidence(
    results
)


print("\n==============================")
print("STRUCTURED EVIDENCE")
print("==============================")


print(
    json.dumps(
        evidence,
        indent=4,
        ensure_ascii=False
    )
)