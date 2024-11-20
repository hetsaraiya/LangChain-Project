from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Reload the embedding model and FAISS index
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
faiss_index = FAISS.load_local("faiss_index", embedding_model)

# Define your query
query = "What are the ethical principles of hacking?"

# Embed the query and perform a similarity search
query_embedding = embedding_model.embed_query(query)
results = faiss_index.similarity_search_by_vector(query_embedding, k=3)

# Display the results
for result in results:
    print("Retrieved Document:")
    print(result.page_content)
