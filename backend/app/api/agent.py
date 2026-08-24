import json
import logging

import httpx
from fastapi import APIRouter

from app.config import settings
from app.core.exceptions import AppException
from app.core.response import success
from app.models.schemas import GenerateRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agent", tags=["Agent 调用"])


async def call_agent(agent_id: str, user_input: str) -> dict:
    if not agent_id or not settings.spark_api_key:
        raise AppException(code=503, message="Agent 尚未配置，请等待 AI 模型组完成 Agent 创建后填充 .env")

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            settings.spark_api_base,
            headers={"Authorization": f"Bearer {settings.spark_api_key}"},
            json={"agent_id": agent_id, "input": user_input},
        )
        if resp.status_code != 200:
            raise AppException(code=502, message=f"Agent 调用失败: HTTP {resp.status_code}")
        return resp.json()


def _mock_text_output(text: str) -> dict:
    return {
        "source": "论语·学而",
        "translation": "孔子说：学了知识并按时复习，不也是令人愉悦的吗？有志同道合的朋友从远方来，不也是快乐的吗？别人不了解自己却不恼怒，不也是君子吗？",
        "script": {
            "title": "学而时习之",
            "theme": "学习与实践的快乐",
            "characters": ["孔子"],
        },
        "storyboard": [
            {"shot": 1, "visual": "孔子端坐案前，手持竹简，面带微笑，案上摊开数卷竹简", "text": "子曰：学而时习之，不亦说乎", "duration": "5s"},
            {"shot": 2, "visual": "一位弟子从远处的山道上走来，孔子起身相迎，二人拱手行礼", "text": "有朋自远方来，不亦乐乎", "duration": "4s"},
            {"shot": 3, "visual": "孔子独立窗前，望向远方，神态从容平和，不怒不忧", "text": "人不知而不愠，不亦君子乎", "duration": "4s"},
        ],
    }


def _mock_visual_output(storyboard: list) -> dict:
    frames = []
    for shot in storyboard:
        frames.append({
            "shot": shot.get("shot", 1),
            "composition": f"水墨构图：{shot.get('visual', '')[:30]}… 主体居中偏右，左侧大面积留白",
            "ink_density": "淡墨为主，关键线条浓墨",
            "whitespace": "约55%",
        })
    return {"frames": frames}


@router.post("/generate")
async def generate(req: GenerateRequest):
    result = {}
    agents_ready = bool(settings.wengai_agent_id and settings.moying_agent_id and settings.spark_api_key)

    if req.mode in ("full", "text"):
        if agents_ready:
            wengai = await call_agent(settings.wengai_agent_id, req.text)
            result["text_output"] = wengai
        else:
            logger.warning("Agent 未配置，返回 mock 数据用于联调")
            result["text_output"] = _mock_text_output(req.text)
            result["mock"] = True

        if req.mode == "text":
            return success(data=result)

    storyboard = []
    if "text_output" in result:
        sb = result["text_output"].get("storyboard", [])
        if isinstance(sb, list):
            storyboard = sb
        elif isinstance(sb, str):
            storyboard = json.loads(sb)

    if req.mode in ("full", "visual"):
        input_text = storyboard if req.mode == "full" else req.text
        if agents_ready:
            moying = await call_agent(settings.moying_agent_id, json.dumps(input_text, ensure_ascii=False))
            result["visual_output"] = moying
        else:
            result["visual_output"] = _mock_visual_output(storyboard)

    return success(data=result)
