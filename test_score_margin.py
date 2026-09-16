from score_analysis import calculate_score_margin


results = [
    {
        "reranker_score": 6.20
    },
    {
        "reranker_score": 2.10
    },
    {
        "reranker_score": 0.50
    }
]


margin = calculate_score_margin(results)

print("\n==============================")
print("SCORE MARGIN TEST")
print("==============================")

print("Best score:", 6.20)
print("Second score:", 2.10)
print("Margin:", round(margin, 4))