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


# ===== 教学工作台 =====
class CoursewareRequest(BaseModel):
    text: str = Field(..., description="古文原文")
    source: str = Field(default="", description="篇目名称")
    grade: str = Field(default="高中", description="适用年级")


class WritingFrameRequest(BaseModel):
    theme: str = Field(default="学习", description="写作主题")
    panel_count: int = Field(default=4, ge=3, le=6, description="分镜格数")


class WritingFeedbackRequest(BaseModel):
    panels: list[dict] = Field(..., description="分镜内容列表")


# ===== 文影创作坊 =====
class AdaptRequest(BaseModel):
    title: str = Field(default="", description="小说标题")
    text: str = Field(..., description="小说原文")
    style: str = Field(default="ink", description="目标风格: realistic/ink/anime/silent")


class DubRequest(BaseModel):
    text: str = Field(..., description="旁白文案")
    style: str = Field(default="caizhizhong", description="配音风格")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="语速")


# ===== 数字人文实验室 =====
class LabStatsResponse(BaseModel):
    text_chunks: int
    images: int
    classics: int
    dimensions: int
    school_distribution: list[dict]
    top_words: list[dict]
    composition_stats: dict
