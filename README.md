# 個人化LINE聊天機器人：做一個代表你發言的機器人！
我們要做的就是把你的 LINE 機器人接上一個大型語言模型，再來透過 RAG 的技術，去讓機器人說出來的話更準確！
這份專案內容主要是提供程式碼的相關設置，要完整設置整個機器人，你還需要：

1. 建立 LINE 機器人，並且進行相關設置。
2. 將這些程式碼部署到公開可造訪的伺服器或雲平臺。
3. 下載模型或者使用 API 呼叫模型。
```
personalised_chat_bot/
├── app.py                     # 主應用，接收 LINE 訊息並回應
├── requirements.txt          # 所需套件
├── testing_rag_local.py      # 本地測試用的 RAG 查詢腳本
├── rag/
│   ├── about_me.txt          # 個人簡介語料
│   └── faiss_index.py        # RAG 查詢邏輯（embedding + 向量查詢）
└── README.md                 # 專案說明（你可以放這段結構）
```

## 大型語言模型選用

這個機器人選用 Google 的免費開源模型 `Gemini 2.0 flash`，機器人會透過申請的 API呼叫模型。

你也可以透過 [Ollama](https://ollama.com/)下載其他免費的開源模型，或者使用其他付費模型。



<!-- *雖然模型效果很差，但在成本考量之下，我們可以先用簡單的模型熟悉流程，後面也可以再換成其他模型～* -->

## 作業流程
**使用者輸入文字** ➔ 文字送到 `app.py` ➔ `app.py` 將文字送給 `faiss_index.py` ➔ `faiss_index.py` 將輸入文字在 `about.me.txt`  中檢索出相關的內容 ➔ 檢索內容送回 `app.py` 的大型語言模型 ➔ 大型語言模型根據檢索內容生成文字 ➔ **輸出文字送給使用者**

## 主程式：`app.py`
呼叫大型語言模型的主程式，使用者輸入進來的文字會在這裡接收，處理後送出給使用者。

💡 大型語言模型的選用，取決於個人，因此需要先行在裝置上安裝（本機、GCP、AWS、fly.io等等）。

💡 記得要修改程式裡API 金鑰的地方，建議透過 `.env` 去設置，避免你公開這個檔案時，你的金鑰會被別人盜用：

```python
# Gemini API endpoint
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

```

## RAG （Retrieval-Augmented Generation）：`rag`
在 `rag` 資料夾下，有兩個檔案負責 RAG 的工作，`faiss_index.py` 會透過檢索 `about_me.txt` 的內容，將這些內容送給 `app.py` ，進而調整要給大型語言模型的內容，大型語言模型會透過這些內容去生成送給使用者的文字。

💡 [FAISS (Facebook AI Similarity Search)]('faiss.ai') 是 facebook 提供的向量庫工具，可以將你提供的檢索文件，運算出相似性的相關數值，作為 RAG 的依據。

💡 `about_me.txt` 是 RAG 參考的檢索文件，其中放的是個人自傳，機器人會根據你的個人資訊，提供使用者相關訊息，你也可以根據你的機器人目的去調整檢索文件。

## 金鑰倉庫 `env.env`

設置時請把檔名從 `env.env` 改成 `.env`，`app.py` 才會從裡面獲取你的各項金鑰。

💡 這個檔案千千萬萬不要公開，這都是屬於個人的機密資料，一旦外流，別人就可以使用這些金鑰去架設他的機器人，但你卻要負擔這些成本。

```
LINE_CHANNEL_ACCESS_TOKEN=<LINE ACCESS TOKEN>
LINE_CHANNEL_SECRET=<LINE SECRET>
GEMINI_API_KEY=<GEMINI金鑰>
```



