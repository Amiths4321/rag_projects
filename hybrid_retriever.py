from retriever import retrieve
from keyword_retriever import keyword_search
from document_loader import load_documents
from rrf import reciprocal_rank_fusion


TOP_K = 5


def hybrid_retrieve(query, product):

    # -----------------------------
    # Vector retrieval
    # -----------------------------

    vector_results = retrieve(
        query,
        product
    )

    vector_documents = []

    for result in vector_results:

        vector_documents.append({
            "id": (
                result.payload["document"],
                result.payload["chunk_id"]
            ),
            "score": result.score,
            "document": {
                "document": result.payload["document"],
                "product": result.payload["product"],
                "section": result.payload["section"],
                "chunk_id": result.payload["chunk_id"],
                "text": result.payload["text"]
            }
        })


    # -----------------------------
    # Keyword retrieval
    # -----------------------------

    all_documents = load_documents()

    product_documents = [
        document
        for document in all_documents
        if document["product"] == product
    ]

    keyword_results = keyword_search(
        query,
        product_documents,
        top_k=TOP_K
    )


    keyword_documents = []

    for result in keyword_results:

        document = result["document"]

        keyword_documents.append({
            "id": (
                document["document"],
                document["chunk_id"]
            ),
            "score": result["score"],
            "document": document
        })


    # -----------------------------
    # RRF
    # -----------------------------

    fused_results = reciprocal_rank_fusion(
        vector_documents,
        keyword_documents
    )


    return fused_results[:TOP_K]