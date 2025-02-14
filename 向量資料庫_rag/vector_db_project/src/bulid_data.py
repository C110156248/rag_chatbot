import os
import streamlit as st
from dotenv import load_dotenv
from data_processing import process_document, split_text
from llama_index.core import VectorStoreIndex, StorageContext, Document, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
import chromadb  

# 載入環境變數
load_dotenv()
GEMINI_API = os.getenv("gemini_key")
file_path = os.getenv("file_path")
persist_dir = os.getenv("persist_dir")
model_name = os.getenv("model_name")
collection_name = os.getenv("collection_name")

# 設定嵌入模型
embed_model = GeminiEmbedding(
    api_key=GEMINI_API,
    model_name=model_name
)
Settings.embed_model = embed_model

# 設定 LLM 模型
llm = Gemini(api_key=GEMINI_API)
Settings.llm = llm

def main():
    # 1. 載入文本並切分
    text_content = process_document(file_path)
    text_chunks = split_text(text_content)

    # 2. 準備 LlamaIndex 的 Document 物件
    documents = [Document(text=chunk) for chunk in text_chunks]

    # 3. 設定 Chroma 客戶端和集合
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    chroma_collection = chroma_client.get_or_create_collection(collection_name)
    # 4. 建立 LlamaIndex 的 ChromaVectorStore
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # 5. 建立 StorageContext
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 6. 建立索引
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,  # 明確指定嵌入模型
    )


    #7. 測試查詢
    query_engine = index.as_query_engine()
    response = query_engine.query("請回答震動分析的知識?")
    print("Query results:", response)

if __name__ == "__main__":
    main()