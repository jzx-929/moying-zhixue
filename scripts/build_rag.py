#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
墨影智学 — RAG 文本库构建脚本
功能：繁简转换 → 文本清洗 → 分块 → 入库 Chroma → 检索验证

依赖安装：
    pip install chromadb opencc-python-reimplemented sentence-transformers

运行：
    python scripts/build_rag.py

说明：
    - 向量模型使用 BAAI/bge-small-zh-v1.5（中文语义检索），首跑自动下载约 95MB；
    - 繁简转换为强制步骤（语料含繁简混用），未安装 opencc 将直接报错；
    - 集合使用 cosine 距离，相似度 = 1 - 距离。
"""

import re
import hashlib
from pathlib import Path

# ============================================================
# 配置
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = PROJECT_ROOT / "data" / "texts"
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db"
COLLECTION_NAME = "guoxue_texts"

# 向量模型（中文语义检索）；可改用 "shibing624/text2vec-base-chinese" 等中文模型
EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"

# 学派映射
SCHOOL_MAP = {
    "论语": "儒家",
    "孟子": "儒家",
    "道德经": "道家",
    "庄子": "道家",
    "史记": "史家",
}

# 分块规则
SHORT_BOOKS = {"论语", "孟子", "道德经"}  # 短文本，不再切
LONG_BOOKS = {"庄子", "史记"}            # 长文本，按段落切

MAX_CHUNK_LEN = 400
OVERLAP_LEN = 50

# ============================================================
# 繁简转换
# ============================================================
def make_converter():
    """创建繁体→简体转换器（强制：语料含繁简混用，必须统一为简体）"""
    try:
        from opencc import OpenCC
    except ImportError:
        print("[FAIL] 未安装 opencc，繁简转换为强制步骤（语料含繁体），不可跳过")
        print("       请运行: pip install opencc-python-reimplemented")
        raise
    cc = OpenCC("t2s")  # t2s = Traditional to Simplified
    print("[OK] OpenCC 繁简转换器已加载")
    return cc.convert

# ============================================================
# 向量模型
# ============================================================
def get_embedding_function():
    """获取中文向量模型（语义检索用），首跑自动下载（约 95MB）"""
    try:
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
    except ImportError:
        print("[FAIL] 未安装 chromadb，请运行: pip install chromadb")
        raise
    try:
        ef = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
        print(f"[OK] 中文向量模型已加载: {EMBEDDING_MODEL}")
        return ef
    except Exception as e:
        print(f"[FAIL] 加载向量模型 {EMBEDDING_MODEL} 失败: {e}")
        print("       需安装 sentence-transformers: pip install sentence-transformers")
        raise

# ============================================================
# 文本清洗
# ============================================================
def clean_text(text):
    """清洗：半角标点转全角 → 去空行 → 去首尾空格 → 去全角空格缩进"""
    # 部分章节混用了半角逗号/分号等，统一为全角，保证分句正则正确生效
    punct_map = str.maketrans({",": "，", ";": "；", ":": "：", "!": "！", "?": "？"})
    text = text.translate(punct_map)
    lines = []
    for line in text.splitlines():
        line = line.strip()
        line = line.lstrip("\u3000")  # 去全角空格缩进
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)

# ============================================================
# 分块
# ============================================================
def chunk_short_text(text, book_name):
    """
    短文本分块（论语/孟子/道德经）：
    - 道德经：整篇作为一块（每章只有几十字）
    - 论语/孟子：按说话人条目切分
    """
    chunks = []

    if book_name == "道德经":
        chunks.append(text)
    else:
        # 按说话人开头切分：子曰、有子曰、曾子曰、子贡曰 等
        pattern = r'(?=(?:子|有子|曾子|子贡|子夏|子游|子张|子路|颜渊|冉有|季康子|孟武伯|鲁哀公|陈亢|巫马期|林放|王孙贾|仪封人|微生亩|孔子|孟子|梁惠王|齐宣王|滕文公|公孙丑|万章|告子)[曰问：:])'
        pieces = re.split(pattern, text)

        # 切分效果不好就按换行切
        if len(pieces) <= 1:
            pieces = [p.strip() for p in text.split("\n") if p.strip()]

        for piece in pieces:
            piece = piece.strip()
            if len(piece) >= 5:  # 太短的碎片跳过
                chunks.append(piece)

    return chunks

def chunk_long_text(text, max_len=MAX_CHUNK_LEN, overlap=OVERLAP_LEN):
    """
    长文本分块（庄子/史记）：
    按段落切，每块 max_len 字左右，相邻块重叠 overlap 字
    """
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current = ""

    for para in paragraphs:
        # 单段超过 max_len，按句子进一步切
        if len(para) > max_len:
            if current:
                chunks.append(current)
                current = ""
            # 按句号/问号/感叹号/分号切句子
            sentences = re.split(r'(?<=[。！？；])', para)
            sent_chunk = ""
            for sent in sentences:
                if len(sent_chunk) + len(sent) > max_len and sent_chunk:
                    chunks.append(sent_chunk)
                    sent_chunk = sent_chunk[-overlap:] + sent if overlap else sent
                else:
                    sent_chunk += sent
            if sent_chunk:
                chunks.append(sent_chunk)
        else:
            # 正常段落，积累到 max_len
            if len(current) + len(para) > max_len and current:
                chunks.append(current)
                current = current[-overlap:] + "\n" + para if overlap else para
            else:
                current = current + "\n" + para if current else para

    if current:
        chunks.append(current)

    return chunks

# ============================================================
# 处理所有文件
# ============================================================
def process_all_texts(convert_func):
    """遍历所有文本文件，清洗+繁简转换+分块，返回所有块"""
    all_chunks = []

    if not TEXT_DIR.exists():
        print(f"[FAIL] 文本目录不存在: {TEXT_DIR}")
        return all_chunks

    book_dirs = sorted([d for d in TEXT_DIR.iterdir() if d.is_dir()])
    print(f"\n找到 {len(book_dirs)} 个典籍目录: {[d.name for d in book_dirs]}")

    total_files = 0
    total_chunks = 0

    for book_dir in book_dirs:
        book_name = book_dir.name
        school = SCHOOL_MAP.get(book_name, "其他")
        txt_files = sorted(book_dir.glob("*.txt"))

        print(f"\n--- 处理《{book_name}》({school}) - {len(txt_files)} 个文件 ---")

        book_chunks = 0
        for txt_file in txt_files:
            chapter = txt_file.stem  # 文件名作为篇名
            raw = txt_file.read_text(encoding="utf-8")

            # 清洗 → 繁简转换 → 分块
            cleaned = clean_text(raw)
            simplified = convert_func(cleaned)

            if book_name in SHORT_BOOKS:
                pieces = chunk_short_text(simplified, book_name)
            else:
                pieces = chunk_long_text(simplified)

            # 打包成 chunk 记录
            for i, piece in enumerate(pieces):
                chunk_id = hashlib.md5(
                    f"{book_name}_{chapter}_{i}".encode("utf-8")
                ).hexdigest()[:12]

                all_chunks.append({
                    "id": chunk_id,
                    "text": piece,
                    "metadata": {
                        "source": book_name,
                        "chapter": chapter,
                        "school": school,
                        "chunk_index": i,
                        "total_chunks": len(pieces),
                    }
                })

            total_files += 1
            book_chunks += len(pieces)
            total_chunks += len(pieces)

        print(f"    《{book_name}》完成: {len(txt_files)} 文件 -> {book_chunks} 块")

    print(f"\n{'='*50}")
    print(f"总计: {total_files} 个文件, {total_chunks} 个文本块")
    print(f"{'='*50}")

    return all_chunks

# ============================================================
# 存入 Chroma 向量数据库
# ============================================================
def ingest_to_chroma(all_chunks):
    """将所有文本块存入 Chroma（使用中文向量模型 + cosine 距离）"""

    try:
        import chromadb
    except ImportError:
        print("[FAIL] 未安装 chromadb，请运行: pip install chromadb")
        return False

    ef = get_embedding_function()

    # 本地持久化
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # 已存在则删除重建（避免重复 / 切换向量模型后必须重建）
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"已清空旧的集合: {COLLECTION_NAME}")
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine", "description": "诸子百家国学文本库"},
    )
    print(f"[OK] Chroma 集合已创建: {COLLECTION_NAME} (cosine, {EMBEDDING_MODEL})")

    # 批量入库
    BATCH_SIZE = 100
    total = len(all_chunks)

    for i in range(0, total, BATCH_SIZE):
        batch = all_chunks[i:i + BATCH_SIZE]
        collection.add(
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )
        done = min(i + BATCH_SIZE, total)
        print(f"  入库进度: {done}/{total} ({done*100//total}%)")

    print(f"\n[OK] 入库完成! 共 {total} 条记录")
    return collection

# ============================================================
# 检索验证
# ============================================================
def verify_retrieval(collection):
    """测试几个查询，验证检索效果"""
    print(f"\n{'='*50}")
    print("检索验证测试")
    print(f"{'='*50}")

    test_queries = [
        "孔子论学习",
        "老子论道",
        "庄子逍遥",
        "项羽破釜沉舟",
    ]

    for query in test_queries:
        print(f"\n[查询] {query}")
        print("-" * 40)

        results = collection.query(
            query_texts=[query],
            n_results=3,
        )

        for j, (doc, meta, dist) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )):
            source = meta.get("source", "?")
            chapter = meta.get("chapter", "?")
            preview = doc[:80].replace("\n", " ")
            score = 1 - dist  # cosine 距离 → 相似度
            print(f"  [{j+1}] 《{source}·{chapter}》 相似度:{score:.2f}")
            print(f"      {preview}...")

    print(f"\n{'='*50}")
    print("验证完成! 检索结果与查询相关说明入库成功。")
    print(f"{'='*50}")

# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 60)
    print("  墨影智学 - RAG 文本库构建脚本")
    print("  流程: 繁简转换 -> 清洗 -> 分块 -> 入库 Chroma -> 验证")
    print("=" * 60)

    # 检查文本目录
    print(f"\n文本目录: {TEXT_DIR}")
    if not TEXT_DIR.exists():
        print(f"[FAIL] 目录不存在! 请确认文本文件已放在: {TEXT_DIR}")
        return

    # 1. 繁简转换器
    print("\n[1/5] 初始化繁简转换器...")
    convert_func = make_converter()

    # 2. 处理文本
    print("\n[2/5] 处理文本文件...")
    all_chunks = process_all_texts(convert_func)

    if not all_chunks:
        print("[FAIL] 没有找到任何文本块，请检查文本目录和文件格式")
        return

    # 3. 入库
    print(f"\n[3/5] 存入 Chroma (路径: {CHROMA_DIR})...")
    collection = ingest_to_chroma(all_chunks)

    if not collection:
        return

    # 4. 验证
    print("\n[4/5] 检索验证...")
    verify_retrieval(collection)

    # 5. 完成
    print("\n[5/5] 全部完成!")
    print(f"  - 向量数据库: {CHROMA_DIR}")
    print(f"  - 集合名: {COLLECTION_NAME}")
    print(f"  - 向量模型: {EMBEDDING_MODEL}")
    print(f"  - 总记录: {len(all_chunks)}")
    print(f"\n后续使用（重新打开时需重新指定向量模型）:")
    print(f"  import chromadb")
    print(f"  from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction")
    print(f"  ef = SentenceTransformerEmbeddingFunction(model_name='{EMBEDDING_MODEL}')")
    print(f"  client = chromadb.PersistentClient(path='{CHROMA_DIR}')")
    print(f"  collection = client.get_collection('{COLLECTION_NAME}', embedding_function=ef)")
    print(f"  results = collection.query(query_texts=['你的问题'], n_results=3)")

if __name__ == "__main__":
    main()
