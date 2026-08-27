import base64
import logging
import re
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel, Field

from app.api.agent import _agents_ready, call_agent, _mock_text_output
from app.config import settings
from app.core.response import success

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ocr", tags=["文漫互转"])


@router.post("/recognize")
async def recognize_text(
    file: UploadFile = File(...),
    do_generate: bool = Form(False),
):
    content = await file.read()
    if not content:
        return success(data={"text": "", "error": "空文件"})

    extracted = _extract_chinese_text(content)
    logger.info(f"OCR 识别完成，提取文本长度: {len(extracted)}")

    result = {"text": extracted, "char_count": len(extracted)}

    if do_generate and extracted:
        if _agents_ready():
            agent_result = await call_agent(settings.wengai_agent_id, extracted)
            result["agent_output"] = agent_result
        else:
            result["agent_output"] = _mock_text_output(extracted)
            result["mock"] = True

    return success(data=result)


@router.post("/generate-from-image")
async def generate_from_image(
    file: UploadFile = File(...),
):
    content = await file.read()
    extracted = _extract_chinese_text(content)

    if not extracted:
        return success(data={"error": "未识别到有效文字", "text": ""})

    if _agents_ready():
        text_output = await call_agent(settings.wengai_agent_id, extracted)
        visual_output = await call_agent(
            settings.moying_agent_id,
            __import__("json").dumps(text_output.get("storyboard", []), ensure_ascii=False),
        )
        return success(data={"text_output": text_output, "visual_output": visual_output})

    from app.api.agent import _mock_visual_output
    mock_text = _mock_text_output(extracted)
    mock_visual = _mock_visual_output(mock_text.get("storyboard", []))
    return success(data={
        "text_output": mock_text,
        "visual_output": mock_visual,
        "mock": True,
    })


def _extract_chinese_text(content: bytes) -> str:
    try:
        text = content.decode("utf-8", errors="ignore")
    except Exception:
        text = ""

    if not text.strip() or len(text) < 4:
        try:
            import pytesseract
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(img, lang="chi_sim+eng")
        except ImportError:
            text = "图片OCR功能需要安装 pytesseract 和 Pillow（pip install pytesseract Pillow）"
        except Exception as e:
            text = f"OCR识别失败: {e}"

    chinese_pattern = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+")
    matches = chinese_pattern.findall(text)
    return "".join(matches) if matches else text.strip()
