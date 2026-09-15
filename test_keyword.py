from keyword_retriever import keyword_search


documents = [
    {
        "document": "banking_policy.txt",
        "text": "Applicants must have a minimum monthly income of ₹50,000."
    },
    {
        "document": "banking_policy.txt",
        "text": "Applicants must be at least 21 years old."
    },
    {
        "document": "banking_policy_v2.txt",
        "text": "Applicants must have a minimum monthly income of ₹60,000."
    },
    {
        "document": "personal_loan_policy.txt",
        "text": "Applicants must have a minimum monthly income of ₹30,000."
    }
]


query = "minimum monthly income"


results = keyword_search(
    query,
    documents,
    top_k=3
)


print("\n==============================")
print("KEYWORD SEARCH")
print("==============================")


for rank, result in enumerate(results, start=1):

    print(f"\nRank: {rank}")
    print(f"Score: {result['score']:.4f}")
    print(f"Document: {result['document']['document']}")
    print(f"Text: {result['document']['text']}")