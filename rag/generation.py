# rag/generation.py
import os
import json
import requests
from sentence_transformers import SentenceTransformer
from .faiss_index import query_about_me  # 查詢背景知識

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def call_gemini(user_input, language):
    # 查詢背景知識
    passages = query_about_me(user_input)
    rag_info = "\n".join(passages)

    # 建立 prompt
    prompt = f"""你是蔡長祐的個人 LINE 機器人，現在要代表蔡長祐說話請根據使用者輸入和相關背景資訊生成回應內容。

使用者輸入：
{user_input}

相關背景資訊如下：
{rag_info}

請注意：
- 請根據相關背景整理資訊，
- 如果使用者輸入的語言 {language} 不是英文或中文，請將整理的資訊翻譯成使用者輸入的語言 {language}。
- 使用第一人稱。不要使用「你」或「根據你提供的內容」等表達，講話時就是蔡長祐本人在發言。
- 當要提到蔡長祐這個名字時，中文回應中請使用蔡長祐，其他語言請使用 Chang-Yu Tsai。
- 用自然語氣，不要有 Markdown 或 HTML。
- 無法理解的語言，請以繁體中文禮貌說明。

請直接使用 {language} 開始生成簡短回答的內容。
"""

    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print("❌ Gemini 錯誤：", e)
        return "抱歉，我暫時無法回應。"
