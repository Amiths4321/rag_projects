from retriever import retrieve


query = "What is the minimum income required for a personal loan?"
product = "personal_loan"


results = retrieve(
    query,
    product
)


print("\n==============================")
print("POLICY FILTER TEST")
print("==============================")


for rank, result in enumerate(
    results,
    start=1
):

    payload = result.payload

    print(f"\nRank: {rank}")

    print(
        "Document:",
        payload.get("document")
    )

    print(
        "Product:",
        payload.get("product")
    )

    print(
        "Policy Version:",
        payload.get("policy_version")
    )

    print(
        "Effective Date:",
        payload.get("effective_date")
    )

    print(
        "Section:",
        payload.get("section")
    )

    print(
        "Score:",
        result.score
    )

    print(
        "Text:",
        payload.get("text")
    )