import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)

QDRANT_PATH = os.getenv(
    "QDRANT_PATH",
    "qdrant_storage"
)

REVIEW_QUEUE_FILE = os.getenv(
    "REVIEW_QUEUE_FILE",
    "manual_review_queue.json"
)

DASHBOARD_FILE = os.getenv(
    "DASHBOARD_FILE",
    "dashboard_data.json"
)