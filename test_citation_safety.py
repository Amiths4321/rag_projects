from citation_validator import validate_citations
from citation_support_validator import validate_citation_support


EVIDENCE = [
    {
        "evidence_id": "E001",
        "document": "banking_policy_v2.txt",
        "section": "Eligibility",
        "text": (
            "Applicants must have a minimum "
            "monthly income of ₹60,000."
        )
    },
    {
        "evidence_id": "E002",
        "document": "banking_policy_v2.txt",
        "section": "Documents",
        "text": (
            "Applicants must provide valid "
            "identity proof and address proof."
        )
    }
]


TEST_CASES = [

    {
        "name": "VALID CITATION",
        "answer": (
            "The minimum monthly income is "
            "₹60,000. [E001]"
        ),
        "expected": True
    },

    {
        "name": "FAKE EVIDENCE ID",
        "answer": (
            "The minimum monthly income is "
            "₹60,000. [E999]"
        ),
        "expected": False
    },

    {
        "name": "WRONG EVIDENCE",
        "answer": (
            "The minimum monthly income is "
            "₹60,000. [E002]"
        ),
        "expected": False
    }
]


print("\n======================================")
print("CITATION SAFETY TEST")
print("======================================")


passed = 0


for number, test in enumerate(
    TEST_CASES,
    start=1
):

    citation_result = validate_citations(
        test["answer"],
        EVIDENCE
    )

    support_result = (
        validate_citation_support(
            test["answer"],
            EVIDENCE
        )
    )

    safe = (
        citation_result["valid"]
        and support_result["valid"]
    )

    test_passed = (
        safe == test["expected"]
    )

    if test_passed:
        passed += 1

    print(f"\nTEST {number}")
    print("--------------------------------------")

    print("Type:", test["name"])
    print("Answer:", test["answer"])

    print(
        "Citation valid:",
        citation_result["valid"]
    )

    print(
        "Citation supported:",
        support_result["valid"]
    )

    print(
        "Expected safe:",
        test["expected"]
    )

    print(
        "Result:",
        "PASS" if test_passed else "FAIL"
    )


print("\n======================================")
print("SUMMARY")
print("======================================")

print("Passed:", passed)
print("Total:", len(TEST_CASES))

print(
    "Pass Rate:",
    round(
        passed / len(TEST_CASES) * 100,
        2
    ),
    "%"
)
