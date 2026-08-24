import logging

import httpx
from fastapi import APIRouter

from app.config import settings
from app.core.exceptions import AppException
from app.core.response import success
from app.models.schemas import GenerateRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agent", tags=["Agent 调用"])

SPARK_API = settings.spark_api_base
WENGAI_AGENT_ID = settings.wengai_agent_id
MOYING_AGENT_ID = settings.moying_agent_id
API_KEY = settings.spark_api_key


async def call_agent(agent_id: str, user_input: str) -> dict:
    if not agent_id or not API_KEY:
        raise AppException(code=503, message="Agent 尚未配置，请等待 AI 模型组完成 Agent 创建后填充 .env")

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            SPARK_API,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"agent_id": agent_id, "input": user_input},
        )
        if resp.status_code != 200:
            raise AppException(code=502, message=f"Agent 调用失败: HTTP {resp.status_code}")
        return resp.json()


@router.post("/generate")
async def generate(req: GenerateRequest):
    result = {}

    if req.mode in ("full", "text"):
        wengai = await call_agent(WENGAI_AGENT_ID, req.text)
        result["text_output"] = wengai
        if req.mode == "text":
            return success(data=result)

    storyboard = ""
    if "text_output" in result:
        storyboard = result["text_output"].get("storyboard", "")

    if req.mode in ("full", "visual"):
        input_text = storyboard if req.mode == "full" else req.text
        moying = await call_agent(MOYING_AGENT_ID, input_text)
        result["visual_output"] = moying

    return success(data=result)
