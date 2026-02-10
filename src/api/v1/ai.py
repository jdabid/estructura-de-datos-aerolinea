from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.features.ai.agent import get_ai_agent

router = APIRouter(prefix="/ai", tags=["AI Agent"])

class ChatRequest(BaseModel):
    message: str

class PriceSuggestionRequest(BaseModel):
    destination_name: str

@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """Chatbot general que responde sobre vuelos, impuestos y mascotas."""
    agent = get_ai_agent()
    try:
        response = agent.run(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest-price")
async def suggest_price(request: PriceSuggestionRequest):
    """Agente especializado en sugerir ajustes de precios basados en demanda."""
    agent = get_ai_agent()
    prompt = (
        f"Analiza la demanda para {request.destination_name} y sugiere si debemos "
        "aumentar o disminuir el precio base o los impuestos basándote en la popularidad actual."
    )
    try:
        response = agent.run(prompt)
        return {"suggestion": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))