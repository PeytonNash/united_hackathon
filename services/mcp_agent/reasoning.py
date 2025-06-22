from langchain_google_vertexai import ChatVertexAI

llm = ChatVertexAI(
    model="gemini-1.5-flash",
    project="gcp-project",
    temperature=0.4,
    max_output_tokens=1024,
)
