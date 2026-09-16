from hybrid_retriever import hybrid_retrieve
from reranker import rerank
from failure_analysis import analyze_retrieval_failure


query = "What is the minimum income required for a home loan?"

product = "home_loan"

expected_document = "banking_policy_v2.txt"
expected_section = "Eligibility"


print("\n==============================")
print("RETRIEVAL FAILURE ANALYSIS")
print("==============================")


# Hybrid retrieval
candidates = hybrid_retrieve(
    query,
    product
)

print("\nCandidates:", len(candidates))


# Reranking
if candidates:

    results = rerank(
        query,
        candidates,
        top_k=3
    )

else:

    results = []


print("Reranked results:", len(results))


# Analyze
analysis = analyze_retrieval_failure(
    candidates,
    results,
    expected_document,
    expected_section
)


print("\n==============================")
print("FAILURE ANALYSIS RESULT")
print("==============================")

print("Status:", analysis["status"])
print("Stage:", analysis["stage"])
print("Reason:", analysis["reason"])