from hybrid_retriever import hybrid_retrieve
from reranker import rerank


query = "What is the minimum income required for a home loan?"

product = "home_loan"


# Step 1: Hybrid retrieval
candidates = hybrid_retrieve(
    query,
    product
)


print("\n==============================")
print("BEFORE RERANKING")
print("==============================")


for rank, result in enumerate(
    candidates,
    start=1
):

    document = result["document"]

    print(f"\nRank: {rank}")
    print(f"RRF Score: {result['rrf_score']:.6f}")
    print(f"Text: {document.get('text', 'N/A')}")


# Step 2: Reranking
results = rerank(
    query,
    candidates,
    top_k=3
)


print("\n==============================")
print("AFTER RERANKING")
print("==============================")


for rank, result in enumerate(
    results,
    start=1
):

    document = result["document"]

    print(f"\nRank: {rank}")
    print(
        f"Reranker Score: "
        f"{result['reranker_score']:.4f}"
    )
    # Fixed with .get() to prevent KeyError
    print(f"Text: {document.get('text', 'N/A')}")