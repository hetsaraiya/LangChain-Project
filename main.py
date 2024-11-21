from app.vectorstore import create_vectorstore
from app.handle_llm import get_chain
import os
import streamlit as s

prompt = "Hello how are you doing today?"

if not os.path.exists('faiss_index'):
    create_vectorstore("EN-Ethical Hacking.pdf", "gray-hat-hacking.pdf")

s.title("Ethical Hacking Chatbot")

prompt = s.chat_input("You")

if prompt:
    llm_chain = get_chain(query=prompt)
    s.write("Bot", llm_chain)