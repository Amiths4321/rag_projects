from decision_layer import make_retrieval_decision


high_confidence = {
    "score": 5.2,
    "margin": 1.5,
    "level": "HIGH"
}

low_confidence = {
    "score": 0.5,
    "margin": 0.05,
    "level": "LOW"
}


print("HIGH CONFIDENCE:")
print(
    make_retrieval_decision(
        high_confidence,
        []
    )
)


print("\nLOW CONFIDENCE:")
print(
    make_retrieval_decision(
        low_confidence,
        []
    )
)


print("\nPOLICY CONFLICT:")

conflicts = [
    {
        "field": "minimum_income",
        "values": [50000, 60000]
    }
]

print(
    make_retrieval_decision(
        high_confidence,
        conflicts
    )
)