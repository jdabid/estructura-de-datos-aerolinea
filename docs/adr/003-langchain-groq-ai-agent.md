# ADR-003: Agente de IA con LangChain y Groq

**Fecha:** 2025-02-01
**Estado:** Aceptado

## Contexto

Se requiere un agente conversacional que permita a los usuarios consultar vuelos,
crear reservas y obtener estadísticas mediante lenguaje natural. El agente debe poder
invocar las mismas operaciones que la API REST, integrándose con la base de datos
y servicios existentes.

## Decisión

Se implementa un **agente ReAct** usando:
- **LangChain** como framework de orquestación del agente
- **Groq** (Llama 3.3 70B) como LLM por su baja latencia y costo competitivo
- **PostgreSQL + pgvector** para búsqueda semántica (RAG)
- **Tools** decorados con `@tool` de LangChain para exponer operaciones del sistema

El agente reside en `src/features/ai/` con:
- `agent.py` - Configuración del agente y cadena de ejecución
- `tools.py` - Herramientas disponibles para el agente

## Consecuencias

**Positivas:**
- Interfaz conversacional natural para usuarios no técnicos
- Reutilización de la lógica de negocio existente (commands/queries)
- Groq ofrece inferencia rápida (~200ms) con modelos open-source
- pgvector permite RAG sin servicios externos adicionales

**Negativas:**
- Dependencia de servicio externo (Groq API) para funcionalidad de IA
- Latencia adicional en cada interacción (llamada a LLM + tools)
- Requiere `GROQ_API_KEY` configurada, sin ella los endpoints de IA no funcionan
- El comportamiento del agente no es 100% determinístico
