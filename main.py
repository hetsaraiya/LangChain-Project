# main.py
from app.vectorstore import create_vectorstore
from app.handle_llm import get_chain
from app.handle_llm import get_context
import os
import streamlit as s

if not os.path.exists('faiss_index'):
    create_vectorstore("EN-Ethical Hacking.pdf", "gray-hat-hacking.pdf")

s.title("Ethical Hacking Chatbot")

prompt = s.chat_input("You")

if prompt:
    response = get_chain(query=prompt)
    s.write("context : ", get_context(query=prompt))
    s.write("Mixtral : ", response["text"])