import logging
from typing import Optional

import chromadb
from sentence_transformers import SentenceTransformer

from app.config import settings

logger = logging.getLogger(__name__)

_embedding_model: Optional[SentenceTransformer] = None
_chroma_client: Optional[chromadb.PersistentClient] = None
_collection: Optional[chromadb.Collection] = None


def _get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        logger.info(f"加载嵌入模型: {settings.embedding_model}")
        _embedding_model = SentenceTransformer(settings.embedding_model)
    return _embedding_model


def _get_collection() -> chromadb.Collection:
    global _chroma_client, _collection
    if _collection is None:
        db_path = settings.chroma_db_abs_path
        logger.info(f"连接 ChromaDB: {db_path}")
        _chroma_client = chromadb.PersistentClient(path=db_path)
        ef = _get_embedding_model()
        _collection = _chroma_client.get_or_create_collection(
            name=settings.collection_name,
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(f"集合已加载: {settings.collection_name}, 文档数: {_collection.count()}")
    return _collection


def search(
    query: str,
    top_k: int = 5,
    school: Optional[str] = None,
) -> list[dict]:
    collection = _get_collection()

    where_filter = None
    if school:
        where_filter = {"school": {"$eq": school}}

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter,
    )

    items = []
    documents = results.get("documents", [[]])
    metadatas = results.get("metadatas", [[]])
    distances = results.get("distances", [[]])

    if not documents or not documents[0]:
        return items

    for i in range(len(documents[0])):
        doc = documents[0][i]
        meta = metadatas[0][i] if metadatas and metadatas[0] else {}
        dist = distances[0][i] if distances and distances[0] else 0.0
        similarity = 1.0 - dist

        items.append({
            "text": doc,
            "source": meta.get("source", "未知"),
            "school": meta.get("school", "未知"),
            "chapter": meta.get("chapter", ""),
            "similarity": round(similarity, 4),
        })

    return items


def get_collection_info() -> dict:
    collection = _get_collection()
    return {
        "name": settings.collection_name,
        "count": collection.count(),
        "embedding_model": settings.embedding_model,
    }
