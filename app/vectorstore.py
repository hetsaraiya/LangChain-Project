# app/vectorstore.py
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import os
from langchain_voyageai import VoyageAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
# "EN-Ethical Hacking.pdf"
# "gray-hat-hacking.pdf"


embedding_model = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_model_2 = VoyageAIEmbeddings(voyage_api_key=os.getenv("VOYAGE_API_KEY"), model="voyage-law-2")
if os.path.exists('faiss_index'):
    faiss_index = FAISS.load_local("faiss_index", embeddings=embedding_model_2, allow_dangerous_deserialization=True)

def create_vectorstore(*args):
    documents = []
    for arg in args:
        documents = documents + PyPDFLoader(arg).load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    text = text_splitter.split_documents(documents=documents)

    texts = [doc.page_content for doc in text]

    faiss_index = FAISS.from_texts(texts, embedding_model)
    faiss_index.save_local("faiss_index")

def create_vectorstore_2(*args):
    documents = []
    for arg in args:
        documents = documents + PyPDFLoader(arg).load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    text = text_splitter.split_documents(documents=documents)

    texts = [doc.page_content for doc in text]

    faiss_index = FAISS.from_texts(texts, embedding_model_2)
    faiss_index.save_local("faiss_index")