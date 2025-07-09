
import os
import json
import requests
from flask import Flask, request, abort
from dotenv import load_dotenv

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from detection import lang_detect

from rag.faiss_index import query_about_me
from rag.generation import call_gemini  # 👈 加這一行

# 載入環境變數（本機）
load_dotenv()
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

print("🔧 LINE_SECRET:", LINE_CHANNEL_SECRET)
print("🔧 LINE_TOKEN:", LINE_CHANNEL_ACCESS_TOKEN)



# Flask 與 LINE 初始化
app = Flask(__name__)
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=["POST"]) # 設定一個接口讓line developer 把資訊 post 給我
def webhook():
    print("🪵 webhook 被呼叫了")
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    print("📩 收到訊息：", body)
    print("📩 簽名：", signature)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("❌ Webhook 處理錯誤：", e)
        abort(400)
    
    return "OK"

# 文字訊息
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print("✅ 成功觸發 handler.add 的回應處理！")
    user_input = event.message.text
    language = lang_detect(user_input)

    print("🗣 使用者輸入：", user_input)
    print("🗣 語言：", language)

    answer = call_gemini(user_input, language)  # 👈 改成調用模組
    print("🤖 回應內容：", answer)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=answer)]
            )
        )

if __name__ == "__main__":
    print("🚀 Flask 準備啟動")
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
