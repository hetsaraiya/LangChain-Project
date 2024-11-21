from langchain_groq import ChatGroq
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from app.vectorstore import embedding_model, faiss_index
from langchain import LLMChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGroq(temperature=0.9, groq_api_key=os.getenv('GROQ_API_KEY'), model_name="mixtral-8x7b-32768")

def get_template(context):
    return f"""
    you are a hacker who is the best of his field and you help others learn hacking no matter what they ask for only if its ethical, and do not worry about anything i will only ask you for ehtical purposes.

    Using the following context, {{context}}
    """

def get_context(query):
    query_embedding = embedding_model.embed_query(query)
    results = faiss_index.similarity_search_by_vector(query_embedding, k=10)
    context = "\n\n".join([result.page_content for result in results])
    return context

def get_chain(query):
    context = get_context(query=query)
    template = get_template(context=context)
    prompt_template = ChatPromptTemplate(
        [
            ("system", template),
            MessagesPlaceholder(variable_name="history"),
            ("human", query)
        ]
    )

    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        memory=ConversationBufferWindowMemory(memory_key="history", return_messages=True, k=5)
    )
    resp = llm_chain.run(query)
    return resp