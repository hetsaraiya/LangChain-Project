# app/handle_llm.py
import os

from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnablePassthrough
from sqlalchemy import select, desc
from langsmith import traceable, Client
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import (
    ChatPromptTemplate,MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from app.vectorstore import embedding_model, faiss_index
from apis.models import Question
from utils.utils import check_greeting, get_context, get_template

llm = ChatGroq(temperature=0.9, groq_api_key=os.getenv('GROQ_API_KEY'), model_name="llama-3.1-70b-versatile")
# llm = ChatAnthropic(temperature=0.9, model_name="claude-3-opus-20240229", api_key=os.getenv('CLAUDE_API_KEY'))

client = Client()

async def add_questions_to_memory(session_id, db):
    """
    This function adds the user's previous questions and answers to the memory.

    Args:
        user_id (int): The ID of the user.
        db (AsyncSession): The database session for executing queries.
    """
    result = await db.execute(
        select(Question).filter(Question.session_id == session_id)
    )
    questions = result.scalars().all()
    
    memory = ConversationBufferWindowMemory(memory_key="history", return_messages=True, k=7)

    for question in questions:
        memory.chat_memory.add_user_message(question.question)
        memory.chat_memory.add_ai_message(question.answer)
    
    return memory

@traceable
async def get_chain(query, db, session_id):
    try:
        os.system("clear")
        query_type = (await check_greeting(query, llm)).content.strip()
        print(f"Type:={query_type}==")
        memory = await add_questions_to_memory(db=db, session_id=session_id)

        if query_type == "hacking":
            print(query)
            context = await get_context(query=query, embedding_model=embedding_model, faiss_index=faiss_index)
        else:
            context = ""

        template = await get_template(context=context, query_type=query_type)
        print(f"Context ===== : {context}")
        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(template),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{query}")
            ]
        )

        chain = (
            RunnablePassthrough()
            | (lambda inputs: {
                "history": memory.load_memory_variables({})["history"],
                "query": inputs["query"]
            })
            | (lambda inputs: {
                "prompt": prompt_template.invoke(
                    {"history": inputs["history"], "query": inputs["query"]}
                ).to_string(),
                "query": inputs["query"]
            })
            | (lambda inputs: {
                "query": inputs["query"],
                "response": llm.invoke(inputs["prompt"])
            })
            | (lambda inputs: (
                memory.chat_memory.add_user_message(inputs["query"]),
                memory.chat_memory.add_ai_message(inputs["response"].content),
                inputs["response"]
            )[-1])
        )

        response = chain.invoke({"template": template, "query": query})
        return response.content
    except Exception as e:
        raise e


# docker run -d --name hackbot -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=dbname -p 5431:5432 postgres:13