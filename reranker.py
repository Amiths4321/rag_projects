from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(MODEL_NAME)


def rerank(query, results, top_k=3):

    if not results:
        return []

    pairs = []

    for result in results:
        document = result.get("document", {})
        text = document.get("text", "")

        pairs.append(
            [query, text]
        )

    scores = reranker.predict(pairs)

    reranked_results = []

    for result, score in zip(results, scores):

        result["reranker_score"] = float(score)

        reranked_results.append(result)

    reranked_results.sort(
        key=lambda x: x["reranker_score"],
        reverse=True
    )

    return reranked_results[:top_k]