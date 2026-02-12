from langchain_groq import ChatGroq
import os
import functools


@functools.lru_cache(maxsize=1)
def get_ai_agent():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is not set")

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=api_key,
    )