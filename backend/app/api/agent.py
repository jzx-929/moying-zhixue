import json
import logging
import re

import httpx
from fastapi import APIRouter

from app.config import settings
from app.core.exceptions import AppException
from app.core.response import success
from app.models.schemas import GenerateRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agent", tags=["Agent 调用"])

SPARK_API_URL = "https://xingchen-api.xf-yun.com/workflow/v1/chat/completions"


def _agents_ready() -> bool:
    return bool(
        settings.spark_api_key
        and settings.spark_api_secret
        and settings.wengai_agent_id
        and settings.moying_agent_id
    )


async def call_agent(flow_id: str, user_input: str) -> dict:
    headers = {
        "Authorization": f"Bearer {settings.spark_api_key}:{settings.spark_api_secret}",
        "Content-Type": "application/json",
    }
    payload = {
        "flow_id": flow_id,
        "uid": "moying-zhixue",
        "stream": False,
        "parameters": {"AGENT_USER_INPUT": user_input},
        "ext": {"bot_id": "workflow", "caller": "workflow"},
    }
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(SPARK_API_URL, headers=headers, json=payload)
    if resp.status_code != 200:
        raise AppException(code=502, message=f"Agent 调用失败: HTTP {resp.status_code} {resp.text[:200]}")
    data = resp.json()
    content = data["choices"][0]["delta"]["content"]
    return _extract_json(content)


def _extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if m:
            text = m.group(1).strip()
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        text = m.group(0)
    return json.loads(text)


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
    agents_ready = _agents_ready()

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
