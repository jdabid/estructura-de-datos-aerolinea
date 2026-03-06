# Skill: Add New AI Tool (RAG Pattern)

Add a new LangChain tool for the AI agent to retrieve data from PostgreSQL or Redis.

## Instructions

1. Ask the user: what data should the tool retrieve, from which source (PostgreSQL, Redis, or both)

2. Add the tool in `src/features/ai/tools.py` following the RAG pattern:

### For PostgreSQL data retrieval:
```python
@tool
def {tool_name}({params}: str) -> str:
    """Description of what data this tool retrieves."""
    db = SessionLocal()
    try:
        # Query the database
        result = db.query(Model).filter(...).all()
        return json.dumps({
            "field": value,
            # ... structured data for the LLM
        })
    finally:
        db.close()
```

### For Redis data retrieval:
```python
@tool
def {tool_name}() -> str:
    """Description of what stats this tool retrieves."""
    # Use redis_client to get stats
    value = redis_client.get("stats:key_name")
    return json.dumps({
        "stat_name": value or 0,
    })
```

3. Key conventions:
   - Import `@tool` from `langchain.tools`
   - Import `SessionLocal` from `src.shared.database` for DB access
   - Import `redis_client` from `src.shared.redis_client` for Redis
   - Always return JSON string with `json.dumps()`
   - Always close DB session in `finally` block
   - Docstring is required - the LLM uses it to understand when to call the tool

4. Wire the tool into the AI endpoint in `src/api/v1/ai.py`:
   - Import the new tool
   - Call it in `run_agent()` or the relevant endpoint
   - Include its output in the prompt sent to the LLM

5. Prompt engineering pattern:
```python
prompt = (
    f"Eres un asistente de vuelos. Responde en espanol.\n\n"
    f"Datos: {tool_result}\n\n"
    f"Pregunta: {user_input}\n\n"
    f"Responde basandote en los datos disponibles."
)
```

6. The LLM is Groq (Llama 3.3 70B) configured as singleton in `src/features/ai/agent.py` via `get_ai_agent()`.
