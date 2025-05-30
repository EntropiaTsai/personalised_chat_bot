from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
from linebot.v3.messaging.models import ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from dotenv import load_dotenv
import os
import requests
from rag.faiss_index import query_about_me

# 載入 .env 檔案中的密鑰
load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

print("✅ Access Token:", LINE_CHANNEL_ACCESS_TOKEN)
print("✅ Channel Secret:", LINE_CHANNEL_SECRET)

# 初始化 Flask 和 LINE Messaging API
app = Flask(__name__)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
line_bot_api = MessagingApi(ApiClient(configuration))

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 簽章驗證失敗")
        abort(400)

    return "OK"

def call_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
	    "model": "tinyllama",  ## 修改成你要的模型
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print("❌ 模型回應錯誤：", e)
        return "系統忙碌中，請稍後再試。"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_text = event.message.text

    # 🔍 取出相關 context
    context_passage = "\n".join(query_about_me(user_text))
    prompt = f"根據以下資訊回答問題：「{user_text}」\n\n{context_passage}\n請用中文簡短回答："

    print(f"📨 收到訊息：{user_text}")
    print(f"📚 查詢結果：{context_passage}")
    print(f"📩 發送 Prompt：{prompt}")

    # 🔁 呼叫本機模型
    reply_text = call_ollama(prompt)

    # 回傳結果
    line_bot_api.reply_message(
        ReplyMessageRequest(
            replyToken=event.reply_token,
            messages=[TextMessage(text=reply_text)]
        )
    )

# ✅ 額外加一個 default handler 用來偵測未處理的事件（可選）
@handler.default()
def debug_event(event):
    print("🛠 未處理的事件：", event)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
