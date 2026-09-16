from pipeline_steps import retrieve_and_rerank


query = "What is the minimum income required for a home loan?"

product = "home_loan"


result = retrieve_and_rerank(
    query,
    product
)


print("\n==============================")
print("PIPELINE STEPS TEST")
print("==============================")

print(
    "Candidates:",
    len(result["candidates"])
)

print(
    "Reranked:",
    len(result["results"])
)

print(
    "Confidence:",
    result["confidence"]
)

print(
    "Conflicts:",
    len(result["conflicts"])
)

print(
    "Quality:",
    result["quality"]
)

print(
    "Decision:",
    result["decision"]
)