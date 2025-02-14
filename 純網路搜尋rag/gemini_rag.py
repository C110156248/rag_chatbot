import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from googleapiclient.discovery import build
import os
def generate_gemini_response(model_name, llm_input, api_key):# Gemini API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=model_name)
    try:
        response = model.generate_content(llm_input)
        return response.text
    except Exception as e:
        print(f"Error during Gemini response generation: {e}")
        return None
def search_google_custom(query, api_key, cse_id, num_results):# Custom Search API
    service = build("customsearch", "v1", developerKey=api_key)
    try:
      response = (
          service.cse()
          .list(q=query, cx=cse_id, num=num_results)
          .execute()
      )
      results = response.get("items", []) 
      formatted_results = []
      for item in results:
          formatted_results.append({
              "title": item.get("title", ""),
              "link": item.get("link", ""),
              "snippet": item.get("snippet", "")
          })
      return formatted_results
    except Exception as e:
        print(f"Error during Google Custom Search: {e}")
        return []
def rag_output(prompt, api_key, search_engine_id, cse_id, model_name): # RAG
    search_results=search_google_custom(prompt, search_engine_id, cse_id, 5)
    Retrieval_content = "這是網路上搜尋到的資料可供參考:\n"
    for i, result in enumerate(search_results):
      Retrieval_content += f"標題：{result['title']}\n"
      Retrieval_content += f"摘要：{result['snippet']}\n"
    response = generate_gemini_response(model_name, prompt, api_key)
    return response
def main_response(text):
    # 載入環境變數
    load_dotenv()
    gemini_key = os.getenv('gemini_key')
    search_engine_id = os.getenv('google_search_api')
    cse_id = os.getenv('google_CSE_ID')
    model_name = "gemini-1.5-flash"
    #rag
    user_query = text
    llm_input = f"根據要求，分析需要上網查詢的資訊(內部知識不足夠)。生成需要上網查詢資訊的的關鍵字(不需要相關說明，回傳資料可以直接複製、貼上使用): {user_query} "
    Google_Search_Keywords = generate_gemini_response(model_name, prompt, gemini_key)
    search_results = search_google_custom(Google_Search_Keywords, search_engine_id, cse_id, 5)
    Retrieval_content = "這是網路上搜尋到的資料可供參考:\n"
    for i, result in enumerate(search_results):
        Retrieval_content += f"標題：{result['title']}\n"
        Retrieval_content += f"摘要：{result['snippet']}\n"
        llm_input = f"Prompt:\n{user_query}\n{Retrieval_content[:4000]}"
    # generaiton
    gemini_output = rag_output(llm_input, gemini_key, search_engine_id, cse_id, model_name)
    return gemini_output

st.title("💬  Chatbot")
st.caption("🚀 A Streamlit chatbot powered by gemini and rag")
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("請輸入您的問題:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = main_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
    
    
#streamlit run gemini_rag.py