import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.core.response import success
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/history", tags=["历史记录"])

HISTORY_DIR = Path("data/history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)


class HistorySaveRequest(BaseModel):
    title: str = Field(..., description="作品标题")
    input_text: str = Field("", description="输入文本")
    output_data: dict = Field(..., description="输出结果")
    module: str = Field("workshop", description="来源模块: workshop/workbench/studio")


@router.post("/")
async def save_history(req: HistorySaveRequest):
    record_id = str(uuid.uuid4())[:8]
    record = {
        "id": record_id,
        "title": req.title,
        "module": req.module,
        "input_text": req.input_text,
        "output_data": req.output_data,
        "created_at": datetime.now().isoformat(),
    }
    file_path = HISTORY_DIR / f"{record_id}.json"
    file_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"历史记录已保存: {record_id} ({req.title})")
    return success(data={"id": record_id})


@router.get("/")
async def list_history(
    module: Optional[str] = Query(None, description="按模块筛选"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
):
    files = sorted(HISTORY_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    items = []
    for f in files[:limit * 2]:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if module and data.get("module") != module:
                continue
            items.append({
                "id": data["id"],
                "title": data["title"],
                "module": data.get("module", "workshop"),
                "created_at": data["created_at"],
            })
        except Exception:
            continue
    return success(data={"items": items[:limit], "total": len(items)})


@router.get("/{record_id}")
async def get_history(record_id: str):
    file_path = HISTORY_DIR / f"{record_id}.json"
    if not file_path.exists():
        raise AppException(code=404, message="历史记录不存在")
    data = json.loads(file_path.read_text(encoding="utf-8"))
    return success(data=data)


@router.delete("/{record_id}")
async def delete_history(record_id: str):
    file_path = HISTORY_DIR / f"{record_id}.json"
    if file_path.exists():
        file_path.unlink()
    return success(data={"deleted": record_id})
