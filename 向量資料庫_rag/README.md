# 向量資料庫 RAG Chatbot

基於 RAG (Retrieval-Augmented Generation) 架構的智慧問答系統

## 📝 功能特色

- 🔍 基於 ChromaDB 的向量資料庫儲存與檢索
- 🤖 使用 Google Gemini 進行自然語言理解與生成
- 💡 整合 LlamaIndex 實現高效知識檢索
- 🌐 透過 Streamlit 提供互動式網頁介面



### 安裝步驟

1. 複製專案
```bash
git clone https://github.com/yourusername/vector-db-rag.git
cd vector-db-rag
```

2. 安裝相依套件
```bash
pip install -r requirements.txt
```

3. 設定環境變數
建立 .env 檔案並填入以下設定：
```plaintext
gemini_key="YOUR_GEMINI_API_KEY"
file_path="YOURDATA_FILE_PATH"
persist_dir="YOUR_PERSIST_DIR"
model_name="models/text-embedding-004"
collection_name="my_collection"
```

### 使用方式

1. 建立向量資料庫
```bash
python src/build_data.py
```

2. 啟動聊天機器人
```bash
streamlit run src/chatbot.py
```

## 🛠️ 系統架構

### 主要組件

- **向量資料庫**: ChromaDB
- **AI 模型**: Google Gemini
- **檢索框架**: LlamaIndex
- **前端介面**: Streamlit

### 資料流程

1. 文件預處理與向量化
2. 儲存至 ChromaDB
3. 使用者查詢處理
4. 知識檢索與回答生成

## 📁 專案結構

```
vector-db-project/
├── .env                    # 環境設定
├── requirements.txt        # 相依套件
├── src/
│   ├── build_data.py      # 資料建置
│   ├── chatbot.py         # 主程式
│   └── data_processing.py # 資料處理
└── chroma_db/             # 向量資料庫
```

## ⚙️ 設定說明

### 環境變數
- `gemini_key`: Google Gemini API 金鑰
- `file_path`: 震動分析文件路徑
- `persist_dir`: 向量資料庫儲存位置
- `model_name`: 使用的模型名稱
- `collection_name`: 資料集合名稱

## 🙏 致謝

- Google Gemini
- ChromaDB
- LlamaIndex
- Streamlit

---

⭐️ 如果這個專案對您有幫助，請給我們一個星星！
