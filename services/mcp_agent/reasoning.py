from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a disruption coordinator agent. You handle delays, apply business rules, and escalate when needed."
    ),
    HumanMessagePromptTemplate.from_template("{user_query}"),
])

llm = ChatVertexAI(
    model="gemini-1.5-flash",
    project="gcp-project",
    temperature=0.4,
    max_output_tokens=1024,
)

chain = LLMChain(llm=llm, prompt=prompt)
