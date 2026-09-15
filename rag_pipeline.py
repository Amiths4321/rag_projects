from hybrid_retriever import hybrid_retrieve
from reranker import rerank
from llm import generate_answer
from query_rewriter import rewrite_query


def run_rag(
    query,
    product,
    conversation_history=None
):

    # -----------------------------
    # 1. Query rewriting
    # -----------------------------

    rewritten_query = rewrite_query(
        query,
        product,
        conversation_history
    )

    print("\n==============================")
    print("QUERY REWRITE")
    print("==============================")

    print("Original Query:")
    print(query)

    print("\nRewritten Query:")
    print(rewritten_query)


    # -----------------------------
    # 2. Hybrid retrieval
    # -----------------------------

    candidates = hybrid_retrieve(
        rewritten_query,
        product
    )


    if not candidates:

        return {
            "answer": "No sufficiently relevant information found.",
            "sources": []
        }


    # -----------------------------
    # 3. Reranking
    # -----------------------------

    results = rerank(
        rewritten_query,
        candidates,
        top_k=3
    )


    # -----------------------------
    # 4. Build evidence context
    # -----------------------------

    context_parts = []

    for rank, result in enumerate(
        results,
        start=1
    ):

        document = result["document"]

        context_parts.append(
            f"""
Source {rank}
Document: {document.get('document')}
Product: {document.get('product')}
Section: {document.get('section')}
Chunk ID: {document.get('chunk_id')}
Reranker Score: {result.get('reranker_score'):.4f}

Evidence:
{document.get('text')}
"""
        )


    retrieved_context = "\n".join(
        context_parts
    )


    # -----------------------------
    # 5. Conversation history
    # -----------------------------

    history_text = ""

    if conversation_history:

        for item in conversation_history:

            history_text += (
                f"\nUser: {item['question']}"
                f"\nAssistant: {item['answer']}\n"
            )


    # -----------------------------
    # 6. LLM context
    # -----------------------------

    llm_context = f"""
Conversation History:
{history_text}

Retrieved Evidence:
{retrieved_context}
"""


    # -----------------------------
    # 7. Generate answer
    # -----------------------------

    answer = generate_answer(
        query,
        llm_context
    )


    # -----------------------------
    # 8. Return sources
    # -----------------------------

    sources = []

    for result in results:

        document = result["document"]

        sources.append({
            "document": document.get("document"),
            "product": document.get("product"),
            "section": document.get("section"),
            "chunk_id": document.get("chunk_id"),
            "reranker_score": result.get(
                "reranker_score"
            ),
            "text": document.get("text")
        })


    return {
        "answer": answer,
        "sources": sources
    }