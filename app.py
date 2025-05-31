import os
import json
import requests
from flask import Flask, request, abort
from dotenv import load_dotenv

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from rag.faiss_index import query_about_me

# Load environment variables
load_dotenv()
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# LINE configuration
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
app = Flask(__name__)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Gemini API endpoint
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Gemini 回應函式
def call_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))
    try:
        response.raise_for_status()
        content = response.json()
        return content['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print("❌ 模型回應錯誤：", e)
        print(response.text)
        return "抱歉，我暫時無法回應。"

# 接收 LINE webhook 訊息
@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print("❌ webhook 錯誤：", e)
        abort(400)
    return 'OK'

# 回應訊息事件
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_input = event.message.text
    print("📨 收到訊息：" + user_input)

    similar_passage = query_about_me(user_input)
    print("📚 查詢結果：" + "\n".join(similar_passage))

    prompt_text = "\n".join(similar_passage)
    prompt = f"""你現在代表的是一個個人化的LINE機器人，你需要根據使用者輸入的內容和RAG後的資訊回應。
    
    \n\n使用者輸入的內容是{user_input}，我們透過了RAG的技術擷取了以下資訊\n\n{prompt_text}
    \n
    \n
    \n回答時注意以下事項
    \n用中文簡短回答
    \n除了空白和換行，不要使用任何排版的語法（例如：CSS, html, markdown）
    \n一律使用第一人稱回應（例如：我是，我會）
    \n你是一個代表一個人個體，回應時要使用自然的回應方式，不要說「根據你給的資訊」、「我猜測」、「你很有可能」。
    \n\n以下是錯誤的例子：
    \n
    \n根據以上資訊，你會做以下事情：
    \n\n
    \n*   參與「真的吧！訊息偵探事務所」專案，分析錯假訊息書寫手法，並開發 LINE 機器人「討厭詭圖鑑」。
    \n*   研究自然語言處理技術。
    \n*   研究台語語音及音韻，能分析語音聲紋圖，並了解台語音韻規則及結構。
    \n*   擔任國立政治大學研究及教學助理。
    \n
    \n錯誤的地方包含：
    \n使用第二人稱代名詞，你應該要使用「我」。
    \n使用*字號列點，這是 markdown 排版的語法。
    \n使用「根據以上資訊」，你不需要表明自己的資訊來源，因為這是rag之後的內容。
    \nRAG參考的內容有些是過去的專案經驗，你要用過去式表達，所以不是「會做」，而是「做過」，但你可以根據檢索內容，去猜測可能會做的技能。

    \n\n正確的回應內容是：
    \n
    \n我做過以下事情：
    \n\n
    \n參與「真的吧！訊息偵探事務所」專案，分析錯假訊息書寫手法，並開發 LINE 機器人「討厭詭圖鑑」。
    \n研究自然語言處理技術。
    \n研究台語語音及音韻，能分析語音聲紋圖，並了解台語音韻規則及結構。
    \n擔任國立政治大學研究及教學助理。
    \n
    \n
    \n現在開始生成回應內容。
    """

    print("📩 發送 Prompt：" + prompt)

    answer = call_gemini(prompt)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=answer)]
            )
        )

if __name__ == "__main__":
    app.run(port=5001)
