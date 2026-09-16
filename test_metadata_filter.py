from metadata_filter import build_metadata_filter


metadata_filter = build_metadata_filter(
    product="home_loan",
    policy_version="v2.0",
    effective_date="2026-06-01",
    document_type="loan_policy"
)


print("\n==============================")
print("METADATA FILTER TEST")
print("==============================")

print("Product:        home_loan")
print("Policy Version: v2.0")
print("Effective Date: 2026-06-01")
print("Document Type:  loan_policy")

print("\nFilter created successfully:")
print(metadata_filter)