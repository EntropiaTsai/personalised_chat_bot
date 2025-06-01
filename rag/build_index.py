
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 設定資料與儲存路徑
CHUNKING_TYPES = ["statistical", "consecutive", "cumulative"]
VECTOR_BASE = "./vector_base"
INDEX_BASE = "./faiss_index"
MODEL_NAME = "all-MiniLM-L6-v2"

# 建立儲存資料夾
os.makedirs(INDEX_BASE, exist_ok=True)

# 載入 embedding 模型
model = SentenceTransformer(MODEL_NAME)

def build_single_index(chunk_file: str, index_file: str):
    # 讀取 chunks
    with open(chunk_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # 產生向量
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

    # 建立並儲存 FAISS Index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, index_file)

    # 儲存 chunks 的原文，供查詢時使用
    with open(index_file + ".txt", "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n")

    print(f"✅ 已建立並儲存 FAISS index：{index_file}")

if __name__ == "__main__":
    for chunk_type in CHUNKING_TYPES:
        json_path = os.path.join(VECTOR_BASE, f"chunked_{chunk_type}.json")
        index_path = os.path.join(INDEX_BASE, f"{chunk_type}.index")
        build_single_index(json_path, index_path)
    
    print("🎉 所有 chunking 類型的 FAISS index 建立完成！")
