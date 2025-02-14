import os
import streamlit as st
from dotenv import load_dotenv
from data_processing import process_document, split_text
from llama_index.core import VectorStoreIndex, StorageContext, Document, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
import chromadb  

# 設定頁面配置
st.set_page_config(page_title="震動分析聊天機器人", layout="wide")

# 載入環境變數
load_dotenv()
GEMINI_API = os.getenv("gemini_key")
file_path = os.getenv("file_path")
persist_dir = os.getenv("persist_dir")
model_name = os.getenv("model_name")
collection_name = os.getenv("collection_name")

# 初始化 session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_engine" not in st.session_state:
    # 設定嵌入模型
    embed_model = GeminiEmbedding(
        api_key=GEMINI_API,
        model_name=model_name
    )
    Settings.embed_model = embed_model

    # 設定 LLM 模型
    llm = Gemini(api_key=GEMINI_API)
    Settings.llm = llm

    # 載入和處理文件
    text_content = process_document(file_path)
    text_chunks = split_text(text_content)
    documents = [Document(text=chunk) for chunk in text_chunks]

    # 設定向量儲存
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    chroma_collection = chroma_client.get_or_create_collection("my_collection")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 建立索引和查詢引擎
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
    )
    st.session_state.query_engine = index.as_query_engine()

# 顯示標題
st.title("震動分析聊天機器人 🤖")
st.markdown("---")

# 顯示聊天訊息歷史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 聊天輸入
if prompt := st.chat_input("請輸入您的問題"):
    # 顯示使用者訊息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 顯示助理回應
    with st.chat_message("assistant"):
        response = st.session_state.query_engine.query(prompt)
        st.markdown(response.response)
    st.session_state.messages.append({"role": "assistant", "content": response.response})

# 顯示使用說明
with st.sidebar:
    st.markdown("### 使用說明")
    st.markdown("""
    1. 在輸入框中輸入您的問題
    2. 系統會從震動分析資料庫中尋找相關答案
    3. 您可以繼續提問，系統會保持對話紀錄
    """)

#streamlit run ./向量資料庫_rag/vector-db-project/src/chatbot.py