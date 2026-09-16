from query_rewrite_validation import validate_rewrite


TESTS = [

    {
        "original":
            "What documents are required for it?",

        "rewritten":
            "What documents are required for a home loan?"
    },

    {
        "original":
            "What is the minimum income for it?",

        "rewritten":
            "What is the minimum income for a home loan?"
    },

    {
        "original":
            "What documents are required for it?",

        "rewritten":
            "What is the minimum income for a home loan?"
    }
]


for number, test in enumerate(TESTS, start=1):

    result = validate_rewrite(
        test["original"],
        test["rewritten"]
    )

    print("\nTEST", number)
    print("------------------------------")

    print(
        "Original:",
        test["original"]
    )

    print(
        "Rewritten:",
        test["rewritten"]
    )

    print(
        "Valid:",
        result["valid"]
    )

    print(
        "Reason:",
        result["reason"]
    )