import logging
from pathlib import Path
from typing import Optional

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from app.config import settings

logger = logging.getLogger(__name__)

_ef: Optional[SentenceTransformerEmbeddingFunction] = None
_chroma_client = None
_collection = None


def _get_embedding_function() -> SentenceTransformerEmbeddingFunction:
    global _ef
    if _ef is None:
        logger.info(f"加载嵌入模型: {settings.embedding_model}")
        _ef = SentenceTransformerEmbeddingFunction(model_name=settings.embedding_model)
    return _ef


def _build_in_memory() -> chromadb.Collection:
    """沙箱降级：从 embedding_metadata 表重建内存集合（重新嵌入文档）"""
    import sqlite3

    logger.info("沙箱降级模式：从 embedding_metadata 重建内存集合")
    db_path = settings.chroma_db_abs_path
    sqlite_path = str(Path(db_path) / "chroma.sqlite3")

    client = chromadb.EphemeralClient()
    ef = _get_embedding_function()
    collection = client.create_collection(
        name=settings.collection_name,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM collections WHERE name = ?",
        (settings.collection_name,),
    )
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise RuntimeError(f"集合 '{settings.collection_name}' 不存在")
    collection_id = row["id"]

    cursor.execute(
        "SELECT id FROM segments WHERE collection = ? AND scope = 'METADATA'",
        (collection_id,),
    )
    seg_row = cursor.fetchone()
    if not seg_row:
        conn.close()
        raise RuntimeError("找不到 METADATA segment")
    segment_id = seg_row["id"]

    cursor.execute(
        "SELECT e.id, e.embedding_id FROM embeddings e "
        "WHERE e.segment_id = ? ORDER BY e.id",
        (segment_id,),
    )
    embedding_rows = cursor.fetchall()

    batch_ids = []
    batch_docs = []
    batch_metas = []
    BATCH_SIZE = 100

    for er in embedding_rows:
        eid_int = er["id"]
        eid_str = er["embedding_id"]

        cursor.execute(
            "SELECT key, string_value, int_value, float_value, bool_value "
            "FROM embedding_metadata WHERE id = ?",
            (eid_int,),
        )
        meta_rows = cursor.fetchall()

        document = None
        meta = {}
        for mr in meta_rows:
            key = mr["key"]
            if key == "chroma:document":
                document = mr["string_value"]
            else:
                if mr["string_value"] is not None:
                    meta[key] = mr["string_value"]
                elif mr["int_value"] is not None:
                    meta[key] = mr["int_value"]
                elif mr["float_value"] is not None:
                    meta[key] = mr["float_value"]
                elif mr["bool_value"] is not None:
                    meta[key] = bool(mr["bool_value"])

        if document is None:
            document = ""

        batch_ids.append(eid_str)
        batch_docs.append(document)
        batch_metas.append(meta)

        if len(batch_ids) >= BATCH_SIZE:
            collection.add(
                ids=batch_ids,
                documents=batch_docs,
                metadatas=batch_metas,
            )
            logger.info(f"已加载 {collection.count()} 条记录...")
            batch_ids = []
            batch_docs = []
            batch_metas = []

    if batch_ids:
        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            metadatas=batch_metas,
        )

    conn.close()
    logger.info(f"内存集合重建完成: {collection.count()} 条记录")
    return collection


def _get_collection() -> chromadb.Collection:
    global _chroma_client, _collection
    if _collection is None:
        db_path = settings.chroma_db_abs_path
        logger.info(f"连接 ChromaDB: {db_path}")
        ef = _get_embedding_function()

        try:
            _chroma_client = chromadb.PersistentClient(path=db_path)
            existing = [c.name for c in _chroma_client.list_collections()]
            if settings.collection_name in existing:
                _collection = _chroma_client.get_collection(
                    settings.collection_name,
                    embedding_function=ef,
                )
                _collection.count()
                logger.info(f"持久化集合已加载: {settings.collection_name}")
            else:
                raise RuntimeError(
                    f"集合 '{settings.collection_name}' 不存在，请先运行 scripts/build_rag.py"
                )
        except Exception as e:
            logger.warning(f"持久化加载失败: {e}，降级为内存模式")
            _collection = _build_in_memory()
            _chroma_client = None

        logger.info(f"集合就绪: {settings.collection_name}, 文档数: {_collection.count()}")
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
