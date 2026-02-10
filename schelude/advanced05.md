### Fase 5: Inteligencia Artificial - Implementación Técnica

En esta semana, integraremos un **Agente de IA basado en LangChain** que utiliza la técnica **RAG (Retrieval-Augmented Generation)**. El agente no solo responderá preguntas frecuentes, sino que tendrá acceso a herramientas ("Tools") para consultar en tiempo real la base de datos de vuelos y las estadísticas de demanda en Redis, permitiendo generar sugerencias de precios dinámicos.

---

### 1. Herramientas del Agente (Tools)
**Archivo:** `src/features/ai/tools.py`
Definimos las funciones que el LLM puede ejecutar para obtener datos reales del sistema.

```python

```

---

### 2. Configuración del Agente IA
**Archivo:** `src/features/ai/agent.py`
Configuramos el cerebro de la IA utilizando OpenAI (requiere `OPENAI_API_KEY`).

```python

```

---

### 3. API Endpoints para la IA
**Archivo:** `src/api/v1/ai.py`
Creamos los puntos de entrada para el chatbot y la lógica de precios dinámicos.

```python
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
```

---

### 4. Actualización de la Aplicación Principal
**Archivo:** `src/main.py` (Actualizado)
Registramos el router de IA.

```python

```

---

### 5. Requerimientos de Software (Dependencias)
**Archivo:** `requirements.txt` (Nuevas adiciones)
Debemos asegurar que estas librerías estén instaladas en nuestro contenedor.

```text

```

---

### Resumen de Logros en la Semana 5:
1.  **Integración RAG:** El agente de IA ahora puede "leer" la base de datos de PostgreSQL y Redis para dar respuestas precisas.
2.  **Precios Dinámicos:** Implementada la capacidad de analizar la demanda (vía herramientas de IA) para sugerir cambios estratégicos en los precios.
3.  **Chatbot Funcional:** Endpoint `/chat` listo para integrarse con un frontend o WhatsApp, resolviendo dudas sobre impuestos y mascotas automáticamente.
4.  **Uso de Herramientas (Tooling):** El LLM no alucina precios, ya que está obligado a usar las funciones `get_flight_market_data` para responder.

**Próximo paso (Semana 6):** Finalización del proyecto con Pruebas de Integración (QA), optimización de los manifiestos de Kubernetes y despliegue final en producción.