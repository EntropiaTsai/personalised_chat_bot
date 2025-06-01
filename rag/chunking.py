import os
import json
from sentence_transformers import SentenceTransformer, util

# 設定路徑：請將原始資料存為 original_data.txt（每段一行）
INPUT_PATH = "rag/about_me.txt"

# 載入資料
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# 載入 embedding 模型
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(lines, convert_to_tensor=True)

# 相似度閾值（可自行調整）
COSINE_THRESHOLD = 0.75

# --- 1. Statistical chunking ---
stat_chunks = []
current_chunk = [lines[0]]
for i in range(1, len(lines)):
    sim = util.cos_sim(embeddings[i - 1], embeddings[i]).item()
    if sim > COSINE_THRESHOLD:
        current_chunk.append(lines[i])
    else:
        stat_chunks.append(" ".join(current_chunk))
        current_chunk = [lines[i]]
if current_chunk:
    stat_chunks.append(" ".join(current_chunk))
print('Statistical chunking finished.')

# --- 2. Consecutive chunking（每 3 句為一段）---
consec_chunks = []
for i in range(0, len(lines), 3):
    consec_chunks.append(" ".join(lines[i:i+3]))
print('Consecutive chunking finished.')

# --- 3. Cumulative chunking ---
cum_chunks = []
current_chunk = [lines[0]]
current_embed = [embeddings[0]]
for i in range(1, len(lines)):
    chunk_avg = sum(current_embed) / len(current_embed)
    sim = util.cos_sim(chunk_avg, embeddings[i]).item()
    if sim > COSINE_THRESHOLD:
        current_chunk.append(lines[i])
        current_embed.append(embeddings[i])
    else:
        cum_chunks.append(" ".join(current_chunk))
        current_chunk = [lines[i]]
        current_embed = [embeddings[i]]
if current_chunk:
    cum_chunks.append(" ".join(current_chunk))
print('Cumulative chunking finished.')



# 儲存結果
os.makedirs("vector_base", exist_ok=True)
with open("vector_base/chunked_statistical.json", "w", encoding="utf-8") as f:
    json.dump(stat_chunks, f, ensure_ascii=False, indent=2)

with open("vector_base/chunked_consecutive.json", "w", encoding="utf-8") as f:
    json.dump(consec_chunks, f, ensure_ascii=False, indent=2)

with open("vector_base/chunked_cumulative.json", "w", encoding="utf-8") as f:
    json.dump(cum_chunks, f, ensure_ascii=False, indent=2)

print("✅ Chunking 完成！已輸出至 vector_base/ 資料夾")
