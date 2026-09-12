from rag_pipeline import run_rag, client
from product_detector import detect_product


# ==========================================
# SESSION CONTEXT
# ==========================================

current_product = None


print("\nBanking RAG Assistant")
print("Type 'exit' to quit.")


while True:

    query = input("\nYou: ").strip()


    # --------------------------------------
    # Exit
    # --------------------------------------

    if query.lower() == "exit":
        break


    # --------------------------------------
    # Detect product
    # --------------------------------------

    detected_product = detect_product(query)


    if detected_product:

        current_product = detected_product

        print(
            f"Product selected: {current_product}"
        )


    # --------------------------------------
    # Check product context
    # --------------------------------------

    if current_product is None:

        print(
            "\nPlease mention the loan product first."
        )

        continue


    # --------------------------------------
    # Run RAG
    # --------------------------------------

    result = run_rag(
        query,
        current_product
    )


    # --------------------------------------
    # Answer
    # --------------------------------------

    print("\nAssistant:")
    print(result["answer"])


    # --------------------------------------
    # Evidence
    # --------------------------------------

    print("\nEvidence:")

    for source in result["sources"]:

        print(
            f"- {source['document']} | "
            f"{source['section']} | "
            f"Chunk {source['chunk_id']} | "
            f"Score {source['score']:.4f}"
        )


client.close()