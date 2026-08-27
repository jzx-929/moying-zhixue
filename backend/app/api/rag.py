from fastapi import APIRouter, Query

from app.core.exceptions import AppException
from app.core.response import success
from app.models.schemas import RagSearchRequest
from app.services import rag_service

router = APIRouter(prefix="/api/rag", tags=["RAG 检索"])


@router.get("/search")
async def search(
    q: str = Query(..., description="搜索关键词或古文片段"),
    top_k: int = Query(default=5, ge=1, le=20),
    school: str = Query(default=None, description="学派过滤"),
):
    items = rag_service.search(query=q, top_k=top_k, school=school)
    return success(data={"total": len(items), "items": items})


@router.post("/search")
async def search_post(req: RagSearchRequest):
    items = rag_service.search(
        query=req.query, top_k=req.top_k, school=req.school
    )
    return success(data={"total": len(items), "items": items})


@router.get("/info")
async def collection_info():
    info = rag_service.get_collection_info()
    return success(data=info)
