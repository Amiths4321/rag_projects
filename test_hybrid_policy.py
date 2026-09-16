from hybrid_retriever import hybrid_retrieve


query = "What is the minimum income required for a home loan?"

results = hybrid_retrieve(
    query,
    "home_loan"
)

print("\n==============================")
print("CURRENT POLICY VERIFICATION")
print("==============================")

for rank, result in enumerate(results, start=1):

    document = result.get("document", {})

    print(f"\nRank {rank}")
    print("Document:", document.get("document"))
    print("Product:", document.get("product"))
    print("Policy Version:", document.get("policy_version"))
    print("Effective Date:", document.get("effective_date"))
    print("Section:", document.get("section"))
    print("Chunk:", document.get("chunk_id"))
    print("Text:", document.get("text"))