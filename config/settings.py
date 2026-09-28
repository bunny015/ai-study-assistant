import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
LOG_DIR = BASE_DIR / "logs"
INDEX_DIR = BASE_DIR / "data" / "index"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free").strip()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2").strip()
TOP_K = int(os.getenv("TOP_K", "4"))
MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", "12"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "700"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))


def validate_config(require_api_key=True):
    errors = []
    if require_api_key and not OPENROUTER_API_KEY:
        errors.append("OPENROUTER_API_KEY is not set")
    if not OPENROUTER_MODEL:
        errors.append("OPENROUTER_MODEL is empty")
    if TOP_K < 1:
        errors.append("TOP_K must be at least 1")
    if MAX_HISTORY_TURNS < 1:
        errors.append("MAX_HISTORY_TURNS must be at least 1")
    return errors
