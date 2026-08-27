import logging

from fastapi import APIRouter

from app.api.agent import _agents_ready, call_agent, _extract_json
from app.config import settings
from app.core.response import success
from app.models.schemas import CoursewareRequest, WritingFrameRequest, WritingFeedbackRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/workbench", tags=["教学工作台"])

WRITING_THEMES = {
    "学习": ["少年灯下苦读", "遇到难题困惑", "老师指点迷津", "豁然开朗喜悦", "学有所成分享", "勤学终有所成"],
    "友谊": ["两人初次相遇", "一起学习嬉戏", "发生争执矛盾", "和好如初情深", "友谊天长地久", "送别依依不舍"],
    "坚持": ["立下远大志向", "遭遇挫折失败", "内心挣扎动摇", "咬牙坚持前行", "终获成功喜悦", "回顾来路无悔"],
    "诚信": ["面临利益诱惑", "内心天人交战", "选择坚守诚信", "获得他人敬重", "美名传扬四方", "诚信为本立身"],
}


@router.post("/courseware")
async def generate_courseware(req: CoursewareRequest):
    if _agents_ready():
        result = await call_agent(settings.wengai_agent_id, req.text)
        return success(data={"courseware": result})
    return success(data={"courseware": _mock_courseware(req.text, req.source, req.grade), "mock": True})


def _mock_courseware(text: str, source: str, grade: str) -> dict:
    return {
        "translation": "孔子说：学了知识并按时复习，不也是很愉快吗？有志同道合的朋友从远方来，不也是很快乐吗？别人不了解我，我却不怨恨，不也是有才德的人吗？",
        "panels": [
            {"visual": "孔子端坐案前，手持竹简阅读", "text": "学而时习之，不亦说乎"},
            {"visual": "弟子从远方而来，二人拱手相迎", "text": "有朋自远方来，不亦乐乎"},
            {"visual": "孔子独立窗前，神色从容", "text": "人不知而不愠，不亦君子乎"},
        ],
        "teaching_plan": [
            {"phase": "导入环节", "duration": "5分钟", "action": "播放水墨动画，引起学生兴趣，提问"这句话是什么意思？""},
            {"phase": "讲解环节", "duration": "15分钟", "action": "逐句解读原文，对照白话翻译，讲解重点字词"},
            {"phase": "互动环节", "duration": "15分钟", "action": "使用漫画分镜让学生排序、填空，加深理解"},
            {"phase": "拓展环节", "duration": "10分钟", "action": "讨论"学习的快乐"，联系学生自身经历"},
        ],
    }


@router.post("/writing/frame")
async def generate_writing_frame(req: WritingFrameRequest):
    themes = WRITING_THEMES.get(req.theme, WRITING_THEMES["学习"])
    panels = themes[: req.panel_count]
    return success(data={"panels": [{"visual": p, "text": ""} for p in panels]})


@router.post("/writing/feedback")
async def get_writing_feedback(req: WritingFeedbackRequest):
    filled = [p for p in req.panels if p.get("text", "").strip()]
    total = len(req.panels)
    fill_rate = len(filled) / total if total > 0 else 0

    strengths = ["故事结构完整，有起承转合", "画面描述具体，可视化程度高"]
    if fill_rate == 1.0:
        strengths.append("所有分镜均已完成填写")
    suggestions = ["第2格可以增加更多环境描写来烘托氛围", "人物动作描述可以更丰富，增强画面感"]
    if fill_rate < 1.0:
        suggestions.append(f"还有{total - len(filled)}格未填写，请补全内容")
    suggestions.append("结尾可以加一句点睛之笔，深化主题")

    return success(data={"strengths": strengths, "suggestions": suggestions, "fill_rate": fill_rate})
