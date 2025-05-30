from rag.faiss_index import query_about_me
import requests

def call_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3:latest",
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print("❌ 模型錯誤：", e)
        return "系統錯誤，請稍後再試。"

if __name__ == "__main__":
    question = input("請輸入問題")
    passages = query_about_me(question)
    context = "\n".join(passages)
    
    prompt = f"""根據下列資料回答問題：{question}
    
資料如下：
{context}

請用中文簡短回答："""

    print("📚 查詢結果：", context)
    print("📩 發送 Prompt：", prompt)
    print("🧠 模型回應：", call_ollama(prompt))

