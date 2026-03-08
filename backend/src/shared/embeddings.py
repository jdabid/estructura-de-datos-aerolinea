"""Utilidades para generar y buscar embeddings con pgvector."""
from sqlalchemy import text
from src.shared.database import SessionLocal
import hashlib


def generate_embedding(text_input: str) -> list[float]:
    """Genera un embedding deterministico basado en hash para uso sin modelo externo.

    En produccion se reemplazaria por un modelo real (sentence-transformers, OpenAI, etc).
    Genera un vector de 384 dimensiones normalizado.
    """
    hash_bytes = hashlib.sha384(text_input.lower().encode()).digest()
    raw = [b / 255.0 for b in hash_bytes]
    norm = sum(x * x for x in raw) ** 0.5
    return [x / norm for x in raw] if norm > 0 else raw


def store_destination_embedding(destination_id: int, description: str) -> None:
    """Almacena el embedding de la descripcion de un destino."""
    embedding = generate_embedding(description)
    db = SessionLocal()
    try:
        db.execute(
            text("""
                UPDATE destinations
                SET description = :desc, embedding = :emb::vector
                WHERE id = :id
            """),
            {"desc": description, "emb": str(embedding), "id": destination_id}
        )
        db.commit()
    finally:
        db.close()


def search_similar_destinations(query: str, limit: int = 5) -> list[dict]:
    """Busca destinos similares usando distancia coseno."""
    query_embedding = generate_embedding(query)
    db = SessionLocal()
    try:
        results = db.execute(
            text("""
                SELECT id, name, description,
                       1 - (embedding <=> :query::vector) as similarity
                FROM destinations
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> :query::vector
                LIMIT :limit
            """),
            {"query": str(query_embedding), "limit": limit}
        ).fetchall()
        return [
            {"id": r.id, "name": r.name, "description": r.description, "similarity": round(r.similarity, 4)}
            for r in results
        ]
    finally:
        db.close()
