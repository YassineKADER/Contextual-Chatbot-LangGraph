import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import vector_store  # Import vector_store


# Function to load documents from data folder
def load_document(file_path: str) -> str:
    """Loads a text document from a file."""
    with open(file_path, "r") as f:
        text = f.read()
        return text


def load_documents_from_folder(folder_path: str) -> List[str]:
    """Loads all text documents from a folder."""
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            texts.append(load_document(file_path))
    return texts


def create_chunks(
    documents: List[str], chunk_size: int = 1000, chunk_overlap: int = 200
) -> List[str]:
    """Splits a list of text documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = []
    for doc in documents:
        chunks.extend(text_splitter.split_text(doc))
    return chunks


def embed_and_store(texts: List[str], metadata: List[dict] = None):
    """Embeds a list of text chunks and stores them with optional metadata to ChromaDB."""
    if metadata is None:
        vector_store.add_texts(texts)
    else:
        vector_store.add_texts(texts, metadata)


def retrieve_data(query: str, k=3) -> List[str]:
    results = vector_store.similarity_search(query, k=k)
    return [document.page_content for document in results]
