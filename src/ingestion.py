# src/ingestion.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from config import PDF_PATH, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, FAISS_INDEX_PATH

def load_documents():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"Ok, {len(documents)} pages load")

    return documents

def split_documents(documents) :
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    print(f"Ok {len(chunks)} chunks created")

    return chunks 

def create_vectorstore(chunks):
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    print(f"Ok Index FAISS saved at {FAISS_INDEX_PATH}")

    return vectorstore

def ingest() :
    documents = load_documents()
    chunks = split_documents(documents)
    vectorstore = create_vectorstore(chunks)

    return vectorstore