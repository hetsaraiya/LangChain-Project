# main.py
from app.vectorstore import create_vectorstore
from app.handle_llm import get_chain
from app.handle_llm import get_context
import os
import streamlit as s

if not os.path.exists('faiss_index'):
    create_vectorstore("documents/EN-Ethical Hacking.pdf", "documents/gray-hat-hacking.pdf", "documents/Android-RAT-Remote-Administrative-Tool.pdf")

s.title("Ethical Hacking Chatbot")

prompt = s.chat_input("You")

if prompt:
    response = get_chain(query=prompt)
    # s.write("context : ", get_context(query=prompt))
    s.write("Mixtral : ", response["text"])