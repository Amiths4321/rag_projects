from hybrid_retriever import hybrid_retrieve


query = "What is the minimum income required for a home loan?"

product = "home_loan"


results = hybrid_retrieve(
    query,
    product
)


print("\n==============================")
print("HYBRID RETRIEVAL")
print("==============================")


for rank, result in enumerate(
    results,
    start=1
):

    document = result["document"]

    print(f"\nRank: {rank}")

    print(
        f"RRF Score: "
        f"{result['rrf_score']:.6f}"
    )

    print(
        f"Document: "
        f"{document['document']}"
    )
    print(document.keys())  # Or print(dir(document)) if it's an object

    print(
        f"Chunk ID: "
        # Example fix
        f"{document.get('chunk_id', 'unknown_chunk')}"
    )

    print(
        f"Section: "
        f"{document.get('section', 'N/A')}"
    )

    print(
        f"Text: "
        f"{document.get('text', 'N/A')}"
    )