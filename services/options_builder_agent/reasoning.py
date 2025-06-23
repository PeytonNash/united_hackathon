from langchain_google_vertexai import ChatVertexAI
from .config import VERTEX_MODEL, GCP_PROJECT_ID
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import RunnableSequence

# Define the prompt
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are an options builder agent. You suggest flights, hotels, and lounges to customers."
    ),
    HumanMessagePromptTemplate.from_template("{user_query}"),
])

# Define the LLM
llm = ChatVertexAI(
    model=VERTEX_MODEL,
    project=GCP_PROJECT_ID,
    temperature=0.4,
    max_output_tokens=1024,
)

# Create a RunnableSequence
chain = RunnableSequence([prompt, llm])
