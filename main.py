# # main.py
# from app.vectorstore import create_vectorstore
# from app.handle_llm import get_chain_2, get_chain
# import os
# import streamlit as s

# if not os.path.exists('faiss_index'):
#     create_vectorstore("documents/EN-Ethical Hacking.pdf", "documents/gray-hat-hacking.pdf", "documents/Android-RAT-Remote-Administrative-Tool.pdf")

# s.title("Ethical Hacking Chatbot")

# prompt = s.chat_input("You")

# if prompt:
#     response = get_chain_2(query=prompt)
#     # s.write("context : ", get_context(query=prompt))
#     s.write("Llama : ", response)


from fastapi import FastAPI

from apis.routers import login
from apis.routers import user
from apis.routers import chat

app = FastAPI()

app.include_router(user.router)
app.include_router(login.router)
app.include_router(chat.router)