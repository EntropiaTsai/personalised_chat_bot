# rag/faiss_index.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# 設定 index 與文本路徑
BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, "../faiss_index/statistical.index")
CHUNKS_PATH = INDEX_PATH + ".txt"

# 載入模型（僅用來對 query encode）
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 載入 index
index = faiss.read_index(INDEX_PATH)

# 載入對應的 chunk 原文
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    documents = [line.strip() for line in f if line.strip()]

# 查詢函式
def query_about_me(question, top_k=3):
    query_vec = embedder.encode([question], convert_to_numpy=True)
    distances, indices = index.search(query_vec, top_k)
    return [documents[i] for i in indices[0]]
