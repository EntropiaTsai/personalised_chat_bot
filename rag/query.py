# RAG.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class ChunkSearcher:
    def __init__(self, model_name, index_path):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(index_path)

        # 讀回 chunks 原文
        with open(index_path + ".txt", "r", encoding="utf-8") as f:
            self.chunks = [line.strip() for line in f if line.strip()]

    def query(self, question, top_k=5):  # 你可以修改想要看到前幾筆相似資料
        query_vec = self.model.encode([question], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, top_k)
        results = [(self.chunks[i], float(distances[0][idx])) for idx, i in enumerate(indices[0])]
        return results

# 範例查詢
if __name__ == "__main__":
    searcher = ChunkSearcher(
        model_name="all-MiniLM-L6-v2",
        index_path="./faiss_index/consecutive.index"
    )

    query_text = input('輸入你想檢索的內容：')
    results = searcher.query(query_text)
    print('輸入文本：\n-----------------------\n',query_text)
    for text, score in results:
        print(f"Score: {score:.4f}")
        print(f"Text: {text}\n")
