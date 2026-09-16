from citation_support_validator import (
    validate_citation_support
)


evidence = [
    {
        "evidence_id": "E001",
        "text": (
            "Applicants must have a minimum "
            "monthly income of ₹60,000."
        )
    }
]


answer = (
    "The minimum monthly income required "
    "is ₹60,000. [E001]"
)


result = validate_citation_support(
    answer,
    evidence
)


print("\n==============================")
print("CITATION SUPPORT TEST")
print("==============================")

print("Valid:", result["valid"])
print("Details:", result["citations"])