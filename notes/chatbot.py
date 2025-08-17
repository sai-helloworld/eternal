
import os
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model

# Get API key from environment
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment!")

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=512,
    api_key=api_key   # ✅ explicitly pass API key
)

def ask_groq(query: str) -> str:
    response = llm.invoke(query)
    return response.content
