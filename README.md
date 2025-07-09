# 個人化 LINE 聊天機器人：做一個代表你發言的機器人！

[👉 點擊連結前往機器人](https://line.me/R/ti/p/@315qdpit)

我們要做的就是把你的 LINE 機器人接上一個大型語言模型，再透過 RAG 技術讓它說出更準確、貼近你風格的話。

這份專案內容主要提供程式碼的相關設置。要完整部署一個屬於你的機器人，你還需要：

1. 建立 LINE 機器人，並進行 webhook 設定。
2. 將這些程式碼部署到公開可造訪的伺服器或雲平臺（例如 GCP、Render、Fly.io 等）。
3. 準備語言模型：下載模型或使用 API 方式呼叫（如 Gemini API、Ollama）。

```
personalised_chat_bot/
├── app.py                     # 主應用，接收 LINE 訊息並回應
├── requirements.txt           # 所需套件
├── testing_rag_local.py       # 本地測試用的 RAG 查詢腳本
├── rag/
│   ├── about_me.txt.template  # 個人簡介語料（RAG 檢索用）
│   ├── chunking.py            # 將文章分段
│   ├── build_index.py         # 將每一個 chunk 生成embeddings
│   ├── faiss_index.py         # 向量檢索邏輯（使用 FAISS）
│   └── generation.py          # 生成回應邏輯（串接 LLM）
├── models/
│   └── lid.176.bin            # fastText 語言偵測模型（請手動下載）
└── README.md                  # 專案說明
```

---

## 🧠 大型語言模型選用

本專案預設使用 Google 的 `Gemini 2.0 flash` 模型，透過 API 呼叫生成回應。

你也可以選擇使用：

- [Ollama](https://ollama.com/)：本地部署免費模型（如 `mistral`, `llama3` 等）
- OpenAI GPT 系列（需付費）
- Hugging Face 提供的 API（多數有免費試用額度）

---

## 📊 作業流程

**使用者輸入文字**  
→ `app.py` 接收並處理輸入  
→ 呼叫 `faiss_index.py` 進行相似語料檢索（RAG）  
→ 擷取 `about_me.txt` 中最相似段落  
→ 組合 prompt 給大型語言模型（Gemini API）  
→ 模型生成回應並傳回給使用者！

---

## 🧩 主程式 `app.py`

這是 Flask 建構的主伺服器，負責接收 LINE webhook 訊息，調用下游模組（檢索 + 生成）後，回應訊息給使用者。

💡 請確保你已將 API 金鑰妥善設置於 `.env` 檔案，避免將敏感資訊硬編碼在程式中。

```python
# Gemini API endpoint 範例
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
```

---

## 🔎 檢索模組 `rag/faiss_index.py`

這個模組負責從 `about_me.txt` 中檢索與使用者輸入最相似的段落，做為 RAG 的語境補強。

💡 在首次使用前請先執行建索腳本（見 `build_index.py`），會將文字轉為向量並存為 FAISS index：

```bash
python rag/build_index.py
```

你也可以調整預設檔案名稱：

```python
BASE_DIR = os.path.dirname(__file__)
ABOUT_ME_PATH = os.path.join(BASE_DIR, "about_me.txt")  # ← 請確保此檔案已存在
```

`about_me.txt` 是你的個人資料描述，越具體，生成的回應就越貼近你的風格與背景。

---

## 🧠 FAISS 是什麼？

[FAISS (Facebook AI Similarity Search)](https://faiss.ai) 是 Facebook 開源的向量檢索系統，可用於高效查詢語意相近的段落，廣泛應用於 RAG 系統。

---

## 📂 金鑰倉庫 `.env`

請將你的金鑰寫在 `.env` 檔案中，程式會自動讀取：

```
LINE_CHANNEL_ACCESS_TOKEN=你的 LINE Token
LINE_CHANNEL_SECRET=你的 LINE Secret
GEMINI_API_KEY=你的 Gemini API 金鑰
```

⚠️ **請勿將 `.env` 檔上傳至 GitHub，建議加入 `.gitignore`！**

---

## 📁 fastText 語言偵測模型（選用）

若使用 `lang_detect()` 函式進行多語支援，需下載 fastText 模型至 `models/` 資料夾。

請手動下載：
[https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin)

或使用 wget：

```bash
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin -P models/
```

---

如需進一步協助（部屬到 GCP、整合更多模型），歡迎提 issue 或 PR ✨
