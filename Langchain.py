import os
import sqlite3
import numpy as np
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI

# Set up API keys
os.environ["GOOGLE_API_KEY"] = "AIzaSyAKPYOPkye7Y80ma2GaMmbvqx-QPk43sBI"

# Load PDF documents
pdf1_loader = PyPDFLoader("EN-Ethical Hacking.pdf")
pdf2_loader = PyPDFLoader("gray-hat-hacking.pdf")

docs_pdf1 = pdf1_loader.load()
docs_pdf2 = pdf2_loader.load()
documents = docs_pdf1 + docs_pdf2

# Extract text from the documents
texts = [doc.page_content for doc in documents]

# Generate embeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = embedding_model.embed_documents(texts)

# Store embeddings in a FAISS index
faiss_index = FAISS.from_texts(texts, embedding_model)
faiss_index.save_local("faiss_index")

# Query the FAISS index
query = "Explain ethical hacking principles."
query_embedding = embedding_model.embed_query(query)
results = faiss_index.similarity_search_by_vector(query_embedding, k=3)

for result in results:
    print(result.page_content)

# Save embeddings and text in SQLite
conn = sqlite3.connect("embeddings.db")
c = conn.cursor()

# Create a table to store embeddings
c.execute('''CREATE TABLE IF NOT EXISTS embeddings (id INTEGER PRIMARY KEY, text TEXT, embedding BLOB)''')

# Insert text and embeddings into the database
for i, (text, embedding) in enumerate(zip(texts, embeddings)):
    embedding_array = np.array(embedding)  # Convert list to numpy array
    c.execute("INSERT INTO embeddings (id, text, embedding) VALUES (?, ?, ?)",
              (i, text, embedding_array.tobytes()))

# Commit changes and close the database
conn.commit()
conn.close()
