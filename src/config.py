import os
from dotenv import load_dotenv

load_dotenv()

# Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PDF_PATH = os.path.join(DATA_DIR, "referentiel_activites_competences _evaluation.pdf")

# Ollama
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "qwen3-embedding:0.6b")
OLLAMA_OPTIONS = {"think": False}
OLLAMA_OPTIONS = {"think": False}

# FAISS
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index")

# Params chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Params retriever 
RETRIEVER_K = 4

