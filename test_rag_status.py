from rag_status import get_rag_status


good_quality = {
    "valid": True,
    "reason": None
}

proceed_decision = {
    "decision": "PROCEED",
    "reason": None
}

print("SUCCESS:")
print(
    get_rag_status(
        good_quality,
        proceed_decision
    )
)


bad_quality = {
    "valid": False,
    "reason": "LOW_RELEVANCE"
}

print("\nBAD RETRIEVAL:")
print(
    get_rag_status(
        bad_quality,
        proceed_decision
    )
)


conflict_decision = {
    "decision": "MANUAL_REVIEW",
    "reason": "POLICY_CONFLICT"
}

print("\nPOLICY CONFLICT:")
print(
    get_rag_status(
        good_quality,
        conflict_decision
    )
)