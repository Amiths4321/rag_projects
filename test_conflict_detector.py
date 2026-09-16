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
                "Eligibility:\n"
                "Applicants must have a minimum monthly income "
                "of ₹50,000.\n"
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
                "Eligibility:\n"
                "Applicants must have a minimum monthly income "
                "of ₹60,000.\n"
            )
        }
    }
]


conflicts = detect_policy_conflict(results)

print("\n==============================")
print("POLICY CONFLICT TEST")
print("==============================")

for conflict in conflicts:
    print("\nProduct:", conflict["product"])
    print("Section:", conflict["section"])
    print("Field:", conflict["field"])
    print("Values:", conflict["values"])

print("\nConflicts detected:", len(conflicts))