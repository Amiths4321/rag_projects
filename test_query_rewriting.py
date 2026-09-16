from query_rewriter import rewrite_query
from hybrid_retriever import hybrid_retrieve
from reranker import rerank


TEST_CASES = [

    {
        "history": [
            {
                "question": "What is the minimum income for a home loan?",
                "answer": "The minimum monthly income is ₹60,000."
            }
        ],
        "question": "What documents are required for it?",
        "product": "home_loan",
        "expected_document": "banking_policy_v2.txt",
        "expected_section": "Documents"
    },

    {
        "history": [
            {
                "question": "What is the minimum age for a personal loan?",
                "answer": "Applicants must be at least 21 years old."
            }
        ],
        "question": "What is its maximum tenure?",
        "product": "personal_loan",
        "expected_document": "personal_loan_policy.txt",
        "expected_section": "Loan Tenure"
    }
]


def source_found(
    results,
    expected_document,
    expected_section
):
    for result in results:

        document = result.get("document", {})

        if (
            document.get("document")
            == expected_document
            and
            document.get("section")
            == expected_section
        ):
            return True

    return False


print("\n==============================")
print("QUERY REWRITING EVALUATION")
print("==============================")


for number, test in enumerate(TEST_CASES, start=1):

    original_query = test["question"]
    product = test["product"]
    history = test["history"]

    print(f"\nTEST {number}")
    print("------------------------------")

    print(
        "Original:",
        original_query
    )


    # 1. Rewrite query

    rewritten_query = rewrite_query(
        original_query,
        product,
        history
    )

    print(
        "Rewritten:",
        rewritten_query
    )


    # 2. Retrieve using original query

    original_candidates = hybrid_retrieve(
        original_query,
        product
    )

    original_results = rerank(
        original_query,
        original_candidates,
        top_k=3
    ) if original_candidates else []


    # 3. Retrieve using rewritten query

    rewritten_candidates = hybrid_retrieve(
        rewritten_query,
        product
    )

    rewritten_results = rerank(
        rewritten_query,
        rewritten_candidates,
        top_k=3
    ) if rewritten_candidates else []


    # 4. Check original retrieval

    original_found = source_found(
        original_results,
        test["expected_document"],
        test["expected_section"]
    )


    # 5. Check rewritten retrieval

    rewritten_found = source_found(
        rewritten_results,
        test["expected_document"],
        test["expected_section"]
    )


    print(
        "\nOriginal source found:",
        original_found
    )

    print(
        "Rewritten source found:",
        rewritten_found
    )


    # 6. Compare

    if rewritten_found and not original_found:

        print("RESULT: REWRITING IMPROVED RETRIEVAL")

    elif rewritten_found and original_found:

        print("RESULT: BOTH RETRIEVED SOURCE")

    elif not rewritten_found and original_found:

        print("RESULT: REWRITING DEGRADED RETRIEVAL")

    else:

        print("RESULT: SOURCE NOT FOUND")