from pathlib import Path


def load_documents():

    data_folder = Path("data")

    documents = []

    for file_path in data_folder.glob("*.txt"):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        chunks = [
            chunk.strip()
            for chunk in text.split("\n\n")
            if chunk.strip()
        ]

        for i, chunk in enumerate(
            chunks,
            start=1
        ):

            first_line = chunk.split("\n")[0].strip()

            if first_line.endswith(":"):
                section = first_line[:-1]
            else:
                section = "General"

            if "banking_policy" in file_path.name:
                product = "home_loan"

            elif "personal_loan" in file_path.name:
                product = "personal_loan"

            else:
                product = "unknown"

            documents.append({
                "document": file_path.name,
                "product": product,
                "section": section,
                "chunk_id": i,
                "text": chunk
            })

    return documents