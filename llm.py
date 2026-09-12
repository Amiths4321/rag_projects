import ollama

from prompt import build_rag_prompt


MODEL_NAME = "llama3.2"


def generate_answer(query, context):

    prompt = build_rag_prompt(query, context)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]