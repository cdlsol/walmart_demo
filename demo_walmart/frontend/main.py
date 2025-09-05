import streamlit as st
import requests
import base64

with open("static/swan_profile.png", "rb") as f:
    swan_avatar = f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

with open("static/vs_favicon.png", "rb") as f:
    data = base64.b64encode(f.read()).decode("utf-8")

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{data}" width="200">
        <h2 style="margin-top: 0;">💬 Swanalytics Chatbot</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant", avatar=swan_avatar).write(msg["content"])
    else:
        st.chat_message("user", avatar="👤").write(msg["content"])

if prompt := st.chat_input():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="👤").write(prompt)

    # Show "Thinking..." placeholder
    placeholder = st.chat_message("assistant", avatar=swan_avatar)
    with placeholder:
        thinking_text = st.empty()
        thinking_text.write("Thinking...")

    walmart_api = "http://localhost:8080/question"
    payload = {"question": prompt}

    # Call LLM API
    try:
        response = requests.post(walmart_api, json=payload)
        response.raise_for_status()
        msg = response.json()["answer"]
    except Exception as e:
        msg = f"Sorry, something went wrong: {e}"

    # Replace "Thinking..." with final answer
    thinking_text.write(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
