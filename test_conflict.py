from conflict_detector import detect_policy_conflict


results = [
    {
        "document": {
            "document": "banking_policy.txt",
            "product": "home_loan",
            "section": "Eligibility",
            "policy_version": "v1.0",
            "effective_date": "2026-01-01",
            "text": (
                "Applicants must have a "
                "minimum monthly income of ₹50,000."
            )
        }
    },

    {
        "document": {
            "document": "banking_policy_v2.txt",
            "product": "home_loan",
            "section": "Eligibility",
            "policy_version": "v2.0",
            "effective_date": "2026-06-01",
            "text": (
                "Applicants must have a "
                "minimum monthly income of ₹60,000."
            )
        }
    }
]


conflicts = detect_policy_conflict(
    results
)


print("\n==============================")
print("POLICY CONFLICT TEST")
print("==============================")


if conflicts:

    print("\nCONFLICT DETECTED")

    for conflict in conflicts:

        print(
            "\nProduct:",
            conflict["product"]
        )

        print(
            "Section:",
            conflict["section"]
        )

        for policy in conflict["policies"]:

            print(
                "\nPolicy Version:",
                policy["policy_version"]
            )

            print(
                "Effective Date:",
                policy["effective_date"]
            )

            print(
                "Text:",
                policy["text"]
            )

else:

    print("\nNo conflict detected.")