from collections import defaultdict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from src.features.ai.agent import get_ai_agent
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["AI Agent"])

# Simple in-memory chat history (per-session, resets on restart)
chat_histories: dict[str, list] = defaultdict(list)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class PriceSuggestionRequest(BaseModel):
    destination_name: str


class DemandPredictionRequest(BaseModel):
    destination_name: str


def run_agent(user_input: str) -> str:
    agent = get_ai_agent()
    result = agent.invoke({"input": user_input})
    return result["output"]


@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """Chatbot general que responde sobre vuelos, impuestos y mascotas."""
    try:
        agent = get_ai_agent()
        history = chat_histories[request.session_id]

        result = agent.invoke({
            "input": request.message,
            "chat_history": history,
        })

        # Save to history (keep last 20 messages)
        history.append(HumanMessage(content=request.message))
        history.append(AIMessage(content=result["output"]))
        if len(history) > 20:
            chat_histories[request.session_id] = history[-20:]

        return {"response": result["output"]}
    except Exception:
        logger.exception("AI chat error")
        raise HTTPException(status_code=500, detail="Error procesando solicitud de IA")


@router.post("/suggest-price")
async def suggest_price(request: PriceSuggestionRequest):
    """Agente especializado en sugerir ajustes de precios basados en demanda."""
    try:
        agent = get_ai_agent()
        prompt = (
            f"Analiza el destino '{request.destination_name}'. "
            f"Consulta los datos del mercado y estadisticas de demanda. "
            f"Sugiere si debemos aumentar o disminuir el precio base o los impuestos "
            f"basandote en la popularidad actual. Da recomendaciones concretas con numeros."
        )
        result = agent.invoke({"input": prompt})
        return {"suggestion": result["output"]}
    except Exception:
        logger.exception("AI suggest-price error")
        raise HTTPException(status_code=500, detail="Error procesando sugerencia de precio")


@router.post("/predict-demand")
async def predict_demand_endpoint(request: DemandPredictionRequest):
    """Predice la demanda futura de un destino basandose en datos historicos."""
    try:
        agent = get_ai_agent()
        prompt = (
            f"Analiza la demanda del destino '{request.destination_name}'. "
            f"Consulta los datos del mercado y estadisticas de demanda. "
            f"Da una prediccion detallada sobre la demanda futura, "
            f"incluyendo recomendaciones de precios y capacidad."
        )
        result = agent.invoke({"input": prompt})
        return {"prediction": result["output"]}
    except Exception:
        logger.exception("AI predict-demand error")
        raise HTTPException(status_code=500, detail="Error procesando prediccion de demanda")


@router.post("/embed-destination")
async def embed_destination(destination_id: int, description: str):
    """Genera y almacena el embedding de un destino."""
    from src.shared.embeddings import store_destination_embedding
    try:
        store_destination_embedding(destination_id, description)
        return {"status": "ok", "message": f"Embedding almacenado para destino {destination_id}"}
    except Exception:
        logger.exception("Error storing embedding")
        raise HTTPException(status_code=500, detail="Error almacenando embedding")


@router.get("/search-destinations")
async def search_destinations(query: str, limit: int = 5):
    """Busca destinos similares usando busqueda semantica con pgvector."""
    from src.shared.embeddings import search_similar_destinations
    try:
        results = search_similar_destinations(query, limit)
        return {"results": results}
    except Exception:
        logger.exception("Error searching destinations")
        raise HTTPException(status_code=500, detail="Error buscando destinos similares")
