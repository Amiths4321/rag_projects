from hybrid_retriever import hybrid_retrieve
from reranker import rerank
from confidence import calculate_confidence
from conflict_detector import detect_policy_conflict
from retrieval_quality import check_retrieval_quality
from decision_layer import make_retrieval_decision

import json
from datetime import datetime


def calculate_recall_at_k(
    results,
    expected_document,
    expected_section,
    k=3
):
    top_results = results[:k]

    for result in top_results:

        document = result.get("document", {})

        if (
            document.get("document") == expected_document
            and
            document.get("section") == expected_section
        ):
            return 1.0

    return 0.0


def calculate_precision_at_k(
    results,
    expected_document,
    expected_section,
    k=3
):
    top_results = results[:k]

    relevant_count = 0

    for result in top_results:

        document = result.get("document", {})

        if (
            document.get("document") == expected_document
            and
            document.get("section") == expected_section
        ):
            relevant_count += 1

    return relevant_count / k


def calculate_mrr(
    results,
    expected_document,
    expected_section,
    k=3
):
    top_results = results[:k]

    for rank, result in enumerate(top_results, start=1):

        document = result.get("document", {})

        if (
            document.get("document") == expected_document
            and
            document.get("section") == expected_section
        ):
            return 1.0 / rank

    return 0.0


def calculate_f1(precision, recall):

    if precision + recall == 0:
        return 0.0

    return 2 * (
        precision * recall
    ) / (
        precision + recall
    )

def find_source_rank(
    results,
    expected_document,
    expected_section,
    k=5
):
    top_results = results[:k]

    for rank, result in enumerate(top_results, start=1):

        document = result.get("document", {})

        if (
            document.get("document") == expected_document
            and
            document.get("section") == expected_section
        ):
            return rank

    return None


def calculate_reranker_improvement(
    hybrid_rank,
    reranked_rank
):
    if hybrid_rank is None:
        return "NOT_RETRIEVED"

    if reranked_rank is None:
        return "LOST"

    if reranked_rank < hybrid_rank:
        return "IMPROVED"

    if reranked_rank == hybrid_rank:
        return "UNCHANGED"

    return "DEGRADED"

def calculate_reranker_improvement_rate(stats):
    total_comparable = (
        stats["IMPROVED"]
        + stats["UNCHANGED"]
        + stats["DEGRADED"]
    )

    if total_comparable == 0:
        return 0.0

    return stats["IMPROVED"] / total_comparable

TEST_CASES = [

    {
        "question": "What is the minimum income required for a home loan?",
        "product": "home_loan",
        "expected_document": "banking_policy_v2.txt",
        "expected_section": "Eligibility"
    },

    {
        "question": "What is the minimum age for a home loan?",
        "product": "home_loan",
        "expected_document": "banking_policy_v2.txt",
        "expected_section": "Eligibility"
    },

    {
        "question": "What documents are required for a home loan?",
        "product": "home_loan",
        "expected_document": "banking_policy_v2.txt",
        "expected_section": "Documents"
    },

    {
        "question": "What is the minimum income required for a personal loan?",
        "product": "personal_loan",
        "expected_document": "personal_loan_policy.txt",
        "expected_section": "Eligibility"
    },

    {
        "question": "What is the maximum personal loan tenure?",
        "product": "personal_loan",
        "expected_document": "personal_loan_policy.txt",
        "expected_section": "Loan Tenure"
    }

]


print("\n==============================")
print("RAG PIPELINE TEST")
print("==============================")


total_recall = 0.0
total_precision = 0.0
total_mrr = 0.0
total_f1 = 0.0

evaluation_results = []

reranker_stats = {
        "IMPROVED": 0,
        "UNCHANGED": 0,
        "DEGRADED": 0,
        "NOT_RETRIEVED": 0,
        "LOST": 0
    }

passed_tests = 0
review_tests = 0
failed_tests = 0

for number, test in enumerate(TEST_CASES, start=1):

    query = test["question"]
    product = test["product"]

    print(f"\n\nTEST {number}")
    print("------------------------------")

    print("Question:", query)
    print("Product:", product)


    # 1. Hybrid retrieval

    candidates = hybrid_retrieve(
        query,
        product
    )

    hybrid_rank = find_source_rank(
        candidates,
        test["expected_document"],
        test["expected_section"],
        k=5
    )

    print("\nCandidates:", len(candidates))

    print(
    "Hybrid Source Rank:",
        hybrid_rank
    )


    if not candidates:
        failed_tests += 1
        print("RESULT: FAILED - No candidates")
        continue


    # 2. Reranking

    results = rerank(
        query,
        candidates,
        top_k=3
    )

    reranked_rank = find_source_rank(
        results,
        test["expected_document"],
        test["expected_section"],
        k=3
    )

    print(
    "Reranked Source Rank:",
        reranked_rank
    )

    reranker_result = calculate_reranker_improvement(
        hybrid_rank,
        reranked_rank
    )

    reranker_stats[reranker_result] += 1

    print(
        "Reranker Result:",
        reranker_result
    )

    print("Reranked:", len(results))

    
    # 3. Retrieval quality

    quality = check_retrieval_quality(
        results,
        expected_document=test["expected_document"],
        expected_section=test["expected_section"],
        k=3
    )

    print(
        "Retrieval Quality:",
        quality["valid"],
        quality["reason"]
    )


    # 4. Confidence

    confidence = calculate_confidence(
        results
    )

    print(
        "Confidence:",
        confidence
    )


    # 5. Conflict detection

    conflicts = detect_policy_conflict(
        results
    )

    print(
        "Conflicts:",
        len(conflicts)
    )


    # 6. Final decision

    decision = make_retrieval_decision(
        confidence,
        conflicts
    )

    print(
        "Decision:",
        decision
    )


    # 7. Source verification

    source_found = False

    for result in results:

        document = result.get("document", {})

        if (
            document.get("document")
            == test["expected_document"]
            and
            document.get("section")
            == test["expected_section"]
        ):

            source_found = True
            break


    # 8. Recall@3

    recall_at_3 = calculate_recall_at_k(
        results,
        test["expected_document"],
        test["expected_section"],
        k=3
    )

    print(
        "Recall@3:",
        recall_at_3
    )


    # 9. Precision@3

    precision_at_3 = calculate_precision_at_k(
        results,
        test["expected_document"],
        test["expected_section"],
        k=3
    )

    print(
        "Precision@3:",
        round(precision_at_3, 4)
    )


    # 10. MRR

    mrr = calculate_mrr(
        results,
        test["expected_document"],
        test["expected_section"],
        k=3
    )

    print(
        "MRR:",
        round(mrr, 4)
    )


    # 11. F1@3

    f1 = calculate_f1(
        precision_at_3,
        recall_at_3
    )

    print(
        "F1@3:",
        round(f1, 4)
    )

    if hybrid_rank is not None and reranked_rank is not None:

        if reranked_rank < hybrid_rank:
            print("Reranker: IMPROVED")

        elif reranked_rank == hybrid_rank:
            print("Reranker: UNCHANGED")

        else:
            print("Reranker: DEGRADED")

    else:

        print("Reranker: SOURCE NOT FOUND")

    # 12. Save test evaluation

    evaluation_results.append({

        "test_number": number,

        "question": query,

        "product": product,

        "expected_document":
            test["expected_document"],

        "expected_section":
            test["expected_section"],

        "hybrid_rank":
            hybrid_rank,

        "reranked_rank":
            reranked_rank,

        "reranker_result":
            reranker_result,

        "recall_at_3":
            recall_at_3,

        "precision_at_3":
            precision_at_3,

        "mrr":
            mrr,

        "f1_at_3":
            f1,

        "source_found":
            source_found,

        "retrieval_quality":
            quality,

        "confidence":
            confidence,

        "conflicts":
            conflicts,

        "decision":
            decision
    })


    # 13. Add metrics to totals

    total_recall += recall_at_3
    total_precision += precision_at_3
    total_mrr += mrr
    total_f1 += f1


    # 14. Final test result

    if (
        quality["valid"]
        and
        decision["decision"] == "PROCEED"
        and
        source_found
    ):
        passed_tests += 1
        print("RESULT: PASSED")

    else:
        review_tests += 1
        print("RESULT: REVIEW")


    print(
        "Expected Source:",
        test["expected_document"],
        "|",
        test["expected_section"]
    )

    print(
        "Correct Source Found:",
        source_found
    )


# ==================================
# OVERALL METRICS
# ==================================

average_recall = (
    total_recall / len(TEST_CASES)
)

average_precision = (
    total_precision / len(TEST_CASES)
)

average_mrr = (
    total_mrr / len(TEST_CASES)
)

average_f1 = (
    total_f1 / len(TEST_CASES)
)

print("\n==============================")
print("RERANKER PERFORMANCE")
print("==============================")

for status, count in reranker_stats.items():

    print(
        status + ":",
        count
    )
reranker_improvement_rate = (
    calculate_reranker_improvement_rate(
        reranker_stats
    )
)

print(
    "\nReranker Improvement Rate:",
    round(reranker_improvement_rate * 100, 2),
    "%"
)
# ==================================
# EVALUATION REPORT
# ==================================

evaluation_report = {

    "timestamp":
        datetime.now().isoformat(),

    "dataset_size":
        len(TEST_CASES),

    "test_summary": {
        "passed": passed_tests,
        "review": review_tests,
        "failed": failed_tests
    },

    "metrics": {

        "recall_at_3":
            round(average_recall, 4),

        "precision_at_3":
            round(average_precision, 4),

        "mrr":
            round(average_mrr, 4),

        "f1_at_3":
            round(average_f1, 4)
    },

    "tests":
        evaluation_results
},

    


# ==================================
# SAVE JSON REPORT
# ==================================

filename = (
    "evaluation_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
    + ".json"
)


with open(
    filename,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        evaluation_report,
        file,
        indent=4,
        ensure_ascii=False
    )


print(
    "\nEvaluation report saved:",
    filename
)


# ==================================
# PRINT OVERALL METRICS
# ==================================

print("\n==============================")
print("TEST SUMMARY")
print("==============================")

print("Passed:", passed_tests)
print("Review:", review_tests)
print("Failed:", failed_tests)
print("Total:", len(TEST_CASES))

print("\n==============================")
print("OVERALL RETRIEVAL METRICS")
print("==============================")


print(
    "Recall@3:",
    round(average_recall, 4)
)

print(
    "Precision@3:",
    round(average_precision, 4)
)

print(
    "MRR:",
    round(average_mrr, 4)
)

print(
    "F1@3:",
    round(average_f1, 4)
)