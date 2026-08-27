import json
import logging
from typing import Literal

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from app.core.response import success

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/export", tags=["导出"])


class ExportRequest(BaseModel):
    title: str = Field("墨影智学作品", description="作品标题")
    source: str = Field("", description="古文出处")
    translation: str = Field("", description="白话翻译")
    storyboard: list[dict] = Field(default=[], description="分镜列表")
    visual_frames: list[dict] = Field(default=[], description="构图列表")
    format: Literal["json", "text"] = Field("json", description="导出格式")


@router.post("/")
async def export_work(req: ExportRequest):
    if req.format == "json":
        content = json.dumps({
            "title": req.title,
            "source": req.source,
            "translation": req.translation,
            "storyboard": req.storyboard,
            "visual_frames": req.visual_frames,
        }, ensure_ascii=False, indent=2)
        return PlainTextResponse(content, media_type="application/json",
                                 headers={"Content-Disposition": f"attachment; filename=moying_export.json"})

    lines = [f"【{req.title}】", ""]
    if req.source:
        lines.append(f"出处：{req.source}")
    if req.translation:
        lines.append(f"白话翻译：{req.translation}")
    lines.append("")

    if req.storyboard:
        lines.append("── 分镜文案 ──")
        for shot in req.storyboard:
            idx = shot.get("shot", 0)
            visual = shot.get("visual", "")
            text = shot.get("text", "")
            duration = shot.get("duration", "")
            lines.append(f"第{idx}格 [{duration}]")
            lines.append(f"  画面：{visual}")
            lines.append(f"  台词：「{text}」")
            lines.append("")

    if req.visual_frames:
        lines.append("── 水墨构图 ──")
        for frame in req.visual_frames:
            idx = frame.get("shot", 0)
            comp = frame.get("composition", "")
            ink = frame.get("ink_density", "")
            ws = frame.get("whitespace", "")
            lines.append(f"第{idx}帧")
            lines.append(f"  构图：{comp}")
            lines.append(f"  墨色：{ink}")
            lines.append(f"  留白：{ws}")
            lines.append("")

    content = "\n".join(lines)
    return PlainTextResponse(content, media_type="text/plain; charset=utf-8",
                             headers={"Content-Disposition": f"attachment; filename=moying_export.txt"})
