from hybrid_retriever import hybrid_retrieve
from reranker import rerank
from evidence_builder import build_evidence
from prompt import build_rag_prompt


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


prompt = build_rag_prompt(
    query,
    evidence
)


print("\n==============================")
print("EVIDENCE-BASED PROMPT")
print("==============================")

print(prompt)