# app/vectorstore.py
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# "EN-Ethical Hacking.pdf"
# "gray-hat-hacking.pdf"


embedding_model = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")
faiss_index = FAISS.load_local("faiss_index", embeddings=embedding_model, allow_dangerous_deserialization=True)

def create_vectorstore(*args):
    documents = ""
    for arg in args:
        documents = documents + PyPDFLoader(arg).load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    text = text_splitter.split_documents(documents=documents)

    texts = [doc.page_content for doc in text]

    faiss_index = FAISS.from_texts(texts, embedding_model)
    faiss_index.save_local("faiss_index")