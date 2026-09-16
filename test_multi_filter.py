from metadata_filter import build_metadata_filter


filters = [
    {
        "name": "Home Loan Current Policy",
        "params": {
            "product": "home_loan",
            "effective_date": "2026-06-01"
        }
    },
    {
        "name": "Home Loan V2",
        "params": {
            "product": "home_loan",
            "policy_version": "v2.0"
        }
    },
    {
        "name": "Personal Loan",
        "params": {
            "product": "personal_loan",
            "document_type": "loan_policy"
        }
    },
    {
        "name": "Exact Policy",
        "params": {
            "product": "home_loan",
            "policy_version": "v2.0",
            "effective_date": "2026-06-01",
            "document_type": "loan_policy"
        }
    }
]


print("\n==============================")
print("MULTI-CONDITION FILTER TEST")
print("==============================")


for test in filters:

    metadata_filter = build_metadata_filter(
        **test["params"]
    )

    print("\nTest:", test["name"])
    print("------------------------------")
    print("Conditions:")

    for key, value in test["params"].items():
        print(f"  {key} = {value}")

    print("\nFilter:")
    print(metadata_filter)