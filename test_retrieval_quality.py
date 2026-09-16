from retrieval_quality import check_retrieval_quality


good_results = [
    {
        "reranker_score": 6.28
    },
    {
        "reranker_score": 2.15
    }
]


bad_results = [
    {
        "reranker_score": -6.7
    }
]


print("GOOD RESULTS:")
print(check_retrieval_quality(good_results))


print("\nBAD RESULTS:")
print(check_retrieval_quality(bad_results))


print("\nEMPTY RESULTS:")
print(check_retrieval_quality([]))