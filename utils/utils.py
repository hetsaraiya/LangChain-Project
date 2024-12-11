from dotenv import load_dotenv

from utils.constants import TEMPLATE

load_dotenv()

async def get_template(context, query_type):
    template = TEMPLATE
    if not template:
        raise ValueError("TEMPLATE environment variable is not set.")
    
    formatted_template = template.format(
        query_type=query_type,
        context=context.replace("{", " ").replace("}", " ")
    )
    
    return formatted_template

async def get_context(query, embedding_model, faiss_index):
    query_embedding = embedding_model.embed_query(query)
    results = faiss_index.similarity_search_by_vector(query_embedding, k=10)
    context = "\n\n".join([result.page_content for result in results])
    return context

async def get_querytype_template(query):
    return f"""
    {query}
    Analyze the query above and respond with one of the following words:
    - "greeting" (if it is a greeting)
    - "hacking" (if it is about hacking)
    - "general" (if it is about anything else)

    Respond with only one word and no explanations.
    """

async def check_greeting(query, llm):
    temp = await get_querytype_template(query)
    return llm.invoke(temp)

async def generate_title(query, llm):
    template = f"""
    {query}

    Analyze the query above and respond with a 2-3 word long chat session title for the query.

    never add "
    """
    title = llm.invoke(template)
    return title.content