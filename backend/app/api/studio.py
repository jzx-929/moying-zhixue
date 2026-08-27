import logging

from fastapi import APIRouter

from app.api.agent import _agents_ready, call_agent, _mock_text_output
from app.config import settings
from app.core.response import success
from app.models.schemas import AdaptRequest, DubRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/studio", tags=["文影创作坊"])

STYLE_MAP = {
    "realistic": "写实风格",
    "ink": "水墨风格",
    "anime": "动漫风格",
    "silent": "默片风格",
}


@router.post("/adapt")
async def adapt_novel(req: AdaptRequest):
    if _agents_ready():
        result = await call_agent(settings.wengai_agent_id, req.text)
        return success(data={"script": result})

    mock_script = {
        "title": req.title or "改编剧本",
        "genre": STYLE_MAP.get(req.style, "水墨动画"),
        "duration": "3-5分钟",
        "characters": ["主角", "配角甲", "配角乙"],
        "scenes": [
            {"location": "室外 · 黄昏", "action": "主角独自走在乡间小路上，神色忧郁", "dialogue": "这条路，还要走多久呢？"},
            {"location": "室内 · 书房", "action": "主角在灯下苦读，时而皱眉时而微笑", "dialogue": "原来如此，我明白了！"},
            {"location": "室外 · 清晨", "action": "主角迎着朝阳大步前行，背影坚定", "dialogue": "出发吧，新的一天！"},
        ],
    }
    return success(data={"script": mock_script, "mock": True})


@router.post("/dub")
async def generate_dub(req: DubRequest):
    style_names = {
        "caizhizhong": "蔡志忠旁白风格（简洁睿智）",
        "gentle": "温柔男声",
        "clear": "清澈女声",
        "story": "故事讲述者",
    }
    result = {
        "style": style_names.get(req.style, "蔡志忠旁白风格"),
        "speed": f"{req.speed}x",
        "text": req.text,
        "duration_estimate": f"约 {int(len(req.text) / 4 / req.speed)} 秒",
    }
    return success(data=result)
