from answer_evaluator import evaluate_answer


answer = """
The minimum monthly income required for a home loan
is ₹60,000.
"""


expected_phrases = [
    "₹60,000"
]


result = evaluate_answer(
    answer,
    expected_phrases
)


print("\n==============================")
print("ANSWER CORRECTNESS TEST")
print("==============================")

print("Answer:", answer)
print("Expected:", expected_phrases)
print("Matched:", result["matched"])
print("Missing:", result["missing"])
print("Correct:", result["correct"])