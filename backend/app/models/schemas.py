from typing import Optional
from pydantic import BaseModel, Field


class RagSearchRequest(BaseModel):
    query: str = Field(..., description="搜索关键词或古文片段")
    top_k: int = Field(default=5, ge=1, le=20, description="返回结果数")
    school: Optional[str] = Field(default=None, description="按学派过滤：论语/庄子/孟子/道德经/史记")


class RagResultItem(BaseModel):
    text: str
    source: str
    school: str
    chapter: str
    similarity: float


class RagSearchResponse(BaseModel):
    total: int
    items: list[RagResultItem]


class GenerateRequest(BaseModel):
    text: str = Field(..., description="用户输入的古文")
    mode: str = Field(default="full", description="full=完整链路, text=仅文改, visual=仅画风")


class StoryboardShot(BaseModel):
    shot: int
    visual: str
    text: str
    duration: str


class TextAgentOutput(BaseModel):
    source: str
    translation: str
    script: dict
    storyboard: list[dict]


class VisualAgentOutput(BaseModel):
    frames: list[dict]


class GenerateResponse(BaseModel):
    text_output: Optional[dict] = None
    visual_output: Optional[dict] = None
