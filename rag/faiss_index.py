# rag/faiss_index.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# 設定檔案路徑
BASE_DIR = os.path.dirname(__file__)
ABOUT_ME_PATH = os.path.join(BASE_DIR, "about_me_bak.txt")  ## 將檔名修改為 about_me.txt ，並在about_me.txt 編輯你的自我介紹

# 載入 embedding 模型
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 載入 about_me.txt
with open(ABOUT_ME_PATH, "r", encoding="utf-8") as f:
    documents = [line.strip() for line in f if line.strip()]

# 將句子轉為向量
document_embeddings = embedder.encode(documents, convert_to_numpy=True)

# 建立 FAISS index
index = faiss.IndexFlatL2(document_embeddings.shape[1])
index.add(document_embeddings)

# 查詢函式
def query_about_me(question, top_k=3):
    question_vec = embedder.encode([question], convert_to_numpy=True)
    distances, indices = index.search(question_vec, top_k)
    return [documents[i] for i in indices[0]]

