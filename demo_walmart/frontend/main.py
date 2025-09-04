import streamlit as st
import requests


st.title("💬 Swanalytics Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    walmart_api = "http://localhost:8080/question"
    payload = {
        "question": prompt
    }

    # api will return:
    # return {
    #     "question": user_question,
    #     "context": context,
    #     "answer": answer
    # }
    try:
        response = requests.post(walmart_api, json=payload)
        response.raise_for_status()
        msg = response.json()["answer"]
    except Exception as e:
        msg = f"Sorry, something went wrong: {e}"

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)