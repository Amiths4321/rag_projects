from retriever import retrieve, client
from llm import generate_answer


def run_rag(query, product):

    # 1. Retrieve relevant chunks
    results = retrieve(query, product)

    # 2. Check retrieval
    if not results:
        return {
            "answer": "No sufficiently relevant information found.",
            "sources": []
        }

    # 3. Build context
    context_parts = []

    for rank, result in enumerate(results, start=1):

        context_parts.append(
            f"""
Source {rank}
Document: {result.payload['document']}
Section: {result.payload['section']}
Chunk ID: {result.payload['chunk_id']}

Evidence:
{result.payload['text']}
"""
        )

    context = "\n".join(context_parts)

    # 4. Generate answer
    answer = generate_answer(query, context)

    # 5. Prepare sources
    sources = []

    for result in results:

        sources.append({
            "document": result.payload["document"],
            "document_type": result.payload["document_type"],
            "policy_version": result.payload["policy_version"],
            "effective_date": result.payload["effective_date"],
            "section": result.payload["section"],
            "chunk_id": result.payload["chunk_id"],
            "score": result.score,
            "text": result.payload["text"]
})

    return {
        "answer": answer,
        "sources": sources
    }