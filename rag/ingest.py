from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import hashlib


# ==============================
# Configuration
# ==============================

DB_PATH = "vector_store"
HASH_FILE = os.path.join(DB_PATH, "doc_hash.txt")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


# ==============================
# Utilities
# ==============================

def get_text_hash(text: str) -> str:
    """
    Generate MD5 hash for document text.
    Used to detect document changes.
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def save_hash(hash_value: str):
    """
    Save document hash to file.
    """
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        f.write(hash_value)


def load_saved_hash() -> str | None:
    """
    Load saved hash if exists.
    """
    if not os.path.exists(HASH_FILE):
        return None

    with open(HASH_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


# ==============================
# Main Function
# ==============================

def create_or_load_vector_store(text: str):
    """
    Create new vector store or load existing one.
    Automatically rebuilds if document content changes.
    """

    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    current_hash = get_text_hash(text)

    # ==========================
    # Case 1: Vector store exists
    # ==========================
    if os.path.exists(DB_PATH):

        saved_hash = load_saved_hash()

        # If hash matches → load existing DB
        if saved_hash == current_hash:
            print("🔄 Loading existing vector store...")
            return FAISS.load_local(
                DB_PATH,
                embeddings,
                allow_dangerous_deserialization=True
            )

        # If hash different → rebuild
        print("⚠️ Document changed. Rebuilding vector store...")

    else:
        print("🆕 Creating new vector store...")

    # ==========================
    # Rebuild vector store
    # ==========================

    # 1️⃣ Split document
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    docs = splitter.create_documents([text])

    db = FAISS.from_documents(docs, embeddings)

    os.makedirs(DB_PATH, exist_ok=True)

    db.save_local(DB_PATH)

    save_hash(current_hash)

    print("💾 Vector store built and saved successfully.")

    return db