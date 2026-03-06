from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.features.ai.agent import get_ai_agent
from src.features.ai.tools import get_flight_market_data, get_demand_stats
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["AI Agent"])


class ChatRequest(BaseModel):
    message: str


class PriceSuggestionRequest(BaseModel):
    destination_name: str


def run_agent(user_input: str) -> str:
    llm = get_ai_agent()

    market_data = get_flight_market_data.invoke({"destination_name": user_input})
    demand_data = get_demand_stats.invoke({})

    prompt = (
        f"Eres un asistente de vuelos. Responde en espanol.\n\n"
        f"Datos del mercado: {market_data}\n"
        f"Estadisticas de demanda: {demand_data}\n\n"
        f"Pregunta del usuario: {user_input}\n\n"
        f"Responde de forma clara y concisa basandote en los datos disponibles."
    )

    response = llm.invoke(prompt)
    return response.content


@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """Chatbot general que responde sobre vuelos, impuestos y mascotas."""
    try:
        response = run_agent(request.message)
        return {"response": response}
    except Exception:
        logger.exception("AI chat error")
        raise HTTPException(status_code=500, detail="Error procesando solicitud de IA")


@router.post("/suggest-price")
async def suggest_price(request: PriceSuggestionRequest):
    """Agente especializado en sugerir ajustes de precios basados en demanda."""
    llm = get_ai_agent()

    market_data = get_flight_market_data.invoke({"destination_name": request.destination_name})
    demand_data = get_demand_stats.invoke({})

    prompt = (
        f"Eres un analista de precios de vuelos. Responde en espanol.\n\n"
        f"Datos del destino {request.destination_name}: {market_data}\n"
        f"Estadisticas de demanda: {demand_data}\n\n"
        f"Sugiere si debemos aumentar o disminuir el precio base o los impuestos "
        f"basandote en la popularidad actual. Da recomendaciones concretas con numeros."
    )

    try:
        response = llm.invoke(prompt)
        return {"suggestion": response.content}
    except Exception:
        logger.exception("AI suggest-price error")
        raise HTTPException(status_code=500, detail="Error procesando sugerencia de precio")