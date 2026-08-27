import logging

from fastapi import APIRouter

from app.core.response import success

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/lab", tags=["数字人文实验室"])

SCHOOL_DIST = [
    {"name": "儒家", "count": 1037, "percent": 60},
    {"name": "道家", "count": 519, "percent": 30},
    {"name": "史家", "count": 173, "percent": 10},
]

TOP_WORDS = [
    {"word": "君子", "count": 156, "percent": 100},
    {"word": "道", "count": 142, "percent": 91},
    {"word": "仁", "count": 128, "percent": 82},
    {"word": "学", "count": 98, "percent": 63},
    {"word": "义", "count": 87, "percent": 56},
    {"word": "天", "count": 76, "percent": 49},
    {"word": "人", "count": 72, "percent": 46},
    {"word": "德", "count": 65, "percent": 42},
    {"word": "知", "count": 58, "percent": 37},
    {"word": "礼", "count": 52, "percent": 33},
]

COMPOSITION_STATS = {
    "grid_cells": [5, 8, 12, 10, 25, 35, 3, 15, 45],
    "whitespace_ranges": [
        {"label": "30% 以下", "count": 12, "percent": 6},
        {"label": "30-40%", "count": 28, "percent": 14},
        {"label": "40-50%", "count": 65, "percent": 32.5},
        {"label": "50-60%", "count": 58, "percent": 29},
        {"label": "60% 以上", "count": 37, "percent": 18.5},
    ],
    "line_count_bars": [
        {"label": "≤3条", "height": 20},
        {"label": "4-5条", "height": 60},
        {"label": "6-7条", "height": 85},
        {"label": "8-9条", "height": 45},
        {"label": "≥10条", "height": 15},
    ],
    "ink_density": [
        {"label": "浓墨", "percent": 15},
        {"label": "中墨", "percent": 35},
        {"label": "淡墨", "percent": 50},
    ],
    "sentiment": [
        {"label": "积极正面", "percent": 45, "icon": "😊"},
        {"label": "中性叙述", "percent": 40, "icon": "😐"},
        {"label": "消极警示", "percent": 15, "icon": "😔"},
    ],
    "findings": [
        {"title": "构图规律", "color": "accent", "text": "蔡志忠漫画主体多位于右下或居中，左上大面积留白，形成"虚-实"对比，符合中国传统绘画"计白当黑"的美学原则。"},
        {"title": "极简特征", "color": "olive", "text": "单幅平均仅4.2条主线，最少仅2条，最高不超过8条。以最简练的线条传递最丰富的意蕴，是"以简驭繁"的典范。"},
        {"title": "墨色层次", "color": "gold", "text": "淡墨占比约50%，中墨35%，浓墨15%。整体色调淡雅，关键处用浓墨点睛，层次分明，节奏感强。"},
    ],
}

DATASETS = {
    "text_lib": {
        "name": "国学文本库",
        "icon": "📚",
        "chunks": 1729,
        "classics": 5,
        "total_chars": "约12万字",
        "embedding_model": "bge-small-zh-v1.5",
        "vector_dim": 512,
        "classic_list": ["论语", "孟子", "道德经", "庄子", "史记"],
    },
    "image_lib": {
        "name": "国风漫画图库",
        "icon": "🖼",
        "images": "500+",
        "annotations": "300+",
        "pairs": "500+",
        "style_tags": 8,
        "status": "收集中（Phase 2）",
    },
}


@router.get("/stats")
async def get_stats():
    return success(data={
        "text_chunks": 1729,
        "images": "500+",
        "classics": 5,
        "dimensions": 8,
    })


@router.get("/composition")
async def get_composition():
    return success(data=COMPOSITION_STATS)


@router.get("/text-analysis")
async def get_text_analysis():
    return success(data={
        "school_distribution": SCHOOL_DIST,
        "top_words": TOP_WORDS,
    })


@router.get("/datasets")
async def get_datasets():
    return success(data=DATASETS)
