from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.features.ai.tools import get_flight_market_data, get_demand_stats, search_destinations_by_description, predict_demand
import os
import functools


SYSTEM_PROMPT = """Eres un asistente inteligente especializado en vuelos y reservas.
Responde siempre en espanol.

Tienes acceso a herramientas para consultar:
- Datos del mercado de vuelos (precios, impuestos, promociones)
- Estadisticas de demanda y popularidad de destinos
- Busqueda semantica de destinos similares
- Prediccion de demanda futura por destino

Usa las herramientas cuando necesites datos actuales para responder.
Si no encuentras informacion, indicalo claramente.
Da respuestas concisas y utiles."""


@functools.lru_cache(maxsize=1)
def get_ai_agent():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is not set")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=api_key,
    )

    tools = [get_flight_market_data, get_demand_stats, search_destinations_by_description, predict_demand]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        max_iterations=5,
        handle_parsing_errors=True,
    )
