from app.vectorstore import create_vectorstore
from app.handle_llm import get_chain
import os

prompt = "Hello how are you doing today?"


if not os.path.exists('faiss_index'):
    create_vectorstore("EN-Ethical Hacking.pdf", "gray-hat-hacking.pdf")

llm_chain = get_chain(query=prompt)
print(llm_chain)