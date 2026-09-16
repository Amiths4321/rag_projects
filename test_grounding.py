from grounding_evaluator import evaluate_grounding


context = """
Applicants must have a minimum monthly income
of ₹60,000.

Applicants must be at least 21 years old.
"""


answer = """
The minimum monthly income required is ₹60,000 and the processing fee is ₹2,000..
"""


result = evaluate_grounding(
    answer,
    context
)


print("\n==============================")
print("GROUNDING TEST")
print("==============================")

print("Grounded:", result["grounded"])
print("Reason:", result["reason"])
print(
    "Unsupported values:",
    result["unsupported_values"]
)