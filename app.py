import streamlit as st
import os
from openai import OpenAI

# Сначала пробуем взять ключ из настроек Streamlit (для интернета),
# если их нет — берем из переменной окружения (для твоего ПК)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.environ.get("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"

st.set_page_config(page_title="Sused AI", page_icon="🤖")

st.markdown("""<style>.stApp {background-color: #131314; color: #e3e3e3;}</style>""", unsafe_allow_html=True)

st.title("🤖 Sused AI")

if not api_key:
    st.error("Ключ не найден! Зайди в настройки (Secrets) и добавь GROQ_API_KEY")
    st.stop()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Введите сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                max_tokens=2048
            )
            ai_response = response.choices[0].message.content
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            message_placeholder.markdown(f"❌ Ошибка: {e}")