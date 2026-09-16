import json

from review_queue import add_to_review_queue


review = add_to_review_queue(
    request_id="TEST-001",
    query="What is the processing fee?",
    product="home_loan",
    reason="INSUFFICIENT_EVIDENCE",
    answer=(
        "The available policy information "
        "is insufficient."
    ),
    evidence=[]
)


print("\n==============================")
print("MANUAL REVIEW QUEUE")
print("==============================")

print(
    json.dumps(
        review,
        indent=4,
        ensure_ascii=False
    )
)

print("\nReview item added successfully.")