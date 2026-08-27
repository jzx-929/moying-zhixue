import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, rag, agent, workbench, studio, lab
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.services import rag_service

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="墨影智学后端 API",
    description="文本-漫画-动画跨媒介教学智能体 · 后端服务",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(health.router, tags=["健康检查"])
app.include_router(rag.router)
app.include_router(agent.router)
app.include_router(workbench.router)
app.include_router(studio.router)
app.include_router(lab.router)


@app.on_event("startup")
async def startup():
    logger.info("墨影智学后端服务启动中...")
    asyncio.create_task(_preload_rag())


async def _preload_rag():
    try:
        logger.info("后台预加载 RAG 集合...")
        await asyncio.to_thread(rag_service._get_collection)
        logger.info("RAG 集合预加载完成")
    except Exception as e:
        logger.warning(f"RAG 预加载失败（首次检索时将重试）: {e}")


@app.on_event("shutdown")
async def shutdown():
    logger.info("墨影智学后端服务已关闭")
