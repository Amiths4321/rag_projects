from rrf import reciprocal_rank_fusion


vector_results = [
    {
        "id": 1,
        "text": "Minimum monthly income is ₹60,000."
    },
    {
        "id": 3,
        "text": "Applicant age must be at least 21 years."
    },
    {
        "id": 2,
        "text": "Valid identity proof is required."
    }
]


keyword_results = [
    {
        "id": 2,
        "text": "Valid identity proof is required."
    },
    {
        "id": 1,
        "text": "Minimum monthly income is ₹60,000."
    },
    {
        "id": 4,
        "text": "Income proof is required."
    }
]


results = reciprocal_rank_fusion(
    vector_results,
    keyword_results
)


print("\n==============================")
print("RRF RESULTS")
print("==============================")


for rank, result in enumerate(results, start=1):

    print(f"\nRank: {rank}")
    print(f"ID: {result['id']}")
    print(f"RRF Score: {result['rrf_score']:.6f}")
    print(f"Text: {result['document']['text']}")