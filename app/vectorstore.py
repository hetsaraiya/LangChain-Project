# app/vectorstore.py
import os
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.embeddings import AIEmbeddings
from utils.constants import AI_API_KEY
# embedding_model = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_model = AIEmbeddings(api_key=AI_API_KEY)

def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:
    embeddings = np.array(embeddings)
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return embeddings / norms

if os.path.exists('faiss_index'):
    faiss_index = FAISS.load_local("faiss_index", embeddings=embedding_model, allow_dangerous_deserialization=True)

def create_vectorstore(*args):
    documents = []
    for arg in args:
        documents += PyPDFLoader(arg).load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(documents=documents)

    texts = [doc.page_content for doc in split_docs]

    embeddings = embedding_model.embed_documents(texts)

    embeddings_np = np.array(embeddings)

    normalized_embeddings = normalize_embeddings(embeddings_np)

    text_embeddings = list(zip(texts, normalized_embeddings))

    faiss_index = FAISS.from_embeddings(text_embeddings, embedding_model)

    faiss_index.save_local("faiss_index")
