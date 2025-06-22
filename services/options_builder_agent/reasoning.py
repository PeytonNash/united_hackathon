from langchain_google_vertexai import ChatVertexAI
from .config import VERTEX_MODEL, GCP_PROJECT_ID

llm = ChatVertexAI(
    model=VERTEX_MODEL,
    project=GCP_PROJECT_ID,
    temperature=0.4,
    max_output_tokens=1024,
)
