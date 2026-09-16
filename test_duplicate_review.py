from review_queue import add_to_review_queue


request_id = "DUPLICATE-TEST-001"


review1 = add_to_review_queue(
    request_id=request_id,
    query="What is the processing fee?",
    product="home_loan",
    reason="INSUFFICIENT_EVIDENCE",
    answer="Manual review required.",
    evidence=[]
)

print("\nFirst request:")
print(review1["review_id"])


review2 = add_to_review_queue(
    request_id=request_id,
    query="What is the processing fee?",
    product="home_loan",
    reason="INSUFFICIENT_EVIDENCE",
    answer="Manual review required.",
    evidence=[]
)

print("\nSecond request:")
print(review2["review_id"])