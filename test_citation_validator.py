from citation_validator import validate_citations


evidence = [
    {
        "evidence_id": "E001",
        "document": "banking_policy_v2.txt",
        "section": "Eligibility"
    },
    {
        "evidence_id": "E002",
        "document": "banking_policy_v2.txt",
        "section": "Documents"
    }
]


answer = """
The minimum monthly income required is ₹60,000. [E9001]
"""


result = validate_citations(
    answer,
    evidence
)


print("\n==============================")
print("CITATION VALIDATION")
print("==============================")

print("Answer:", answer)
print("Cited IDs:", result["cited_ids"])
print("Valid IDs:", result["valid_ids"])
print("Invalid IDs:", result["invalid_ids"])
print("Valid:", result["valid"])