import os
from pathlib import Path

from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


# Environment
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


# Flask
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5001"))


# Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN", "")
HUGGINGFACE_REPO_ID = os.getenv(
    "HUGGINGFACE_REPO_ID",
    ""
)


# Data paths
DATA_PATH = BASE_DIR / "data" / "raw"
VECTORSTORE_PATH = BASE_DIR / "vectorstore" / "faiss_index"
LOG_DIR = BASE_DIR / "logs"


# RAG settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))

TOP_K = int(os.getenv("TOP_K", "4"))


# Embedding model
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)