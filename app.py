import streamlit as st
import os
from openai import OpenAI
import base64
import requests

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.environ.get("GROQ_API_KEY")

# Актуальная модель для работы с картинками (Vision)
VISION_MODEL_NAME = "qwen/qwen3.6-27b"
TEXT_MODEL_NAME = "llama-3.3-70b-versatile"
IMAGE_GEN_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
STABILITY_API_KEY = st.secrets.get("STABILITY_API_KEY")

st.set_page_config(page_title="Sused AI Pro", page_icon="🤖")

st.markdown("""<style>.stApp {background-color: #131314; color: #e3e3e3;}</style>""", unsafe_allow_html=True)

st.title("🤖 Sused AI Pro")

if not api_key:
    st.error("Ключ не найден! Добавь GROQ_API_KEY в настройки (Secrets).")
    st.stop()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# Функция генерации изображений
def generate_image(prompt_text):
    with st.chat_message("assistant"):
        st.info(f"🎨 Генерирую: '{prompt_text}'...")
        if not STABILITY_API_KEY:
             st.error("API ключ для генерации (Stability) не найден в Secrets!")
             st.session_state.messages.append({"role": "assistant", "content": "Ошибка: нет ключа генерации."})
             return

        payload = {"prompt": prompt_text, "output_format": "jpeg"}
        files = {'none': ''}
        headers = {"Authorization": f"Bearer {STABILITY_API_KEY}", "Accept": "image/*"}

        try:
            response = requests.post(IMAGE_GEN_API_URL, headers=headers, files=files, data=payload)
            if response.status_code == 200:
                image_base64 = base64.b64encode(response.content).decode('utf-8')
                st.image(f"data:image/jpeg;base64,{image_base64}", caption=f"Запрос: {prompt_text}")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Вот результат по запросу: '{prompt_text}'\n\ndata:image/jpeg;base64,{image_base64}"
                })
            else:
                st.error("❌ Ошибка генерации изображения.")
        except Exception as e:
            st.error(f"❌ Ошибка: {e}")

# Функция обработки фото
def process_image_message(user_prompt, uploaded_file):
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    with st.chat_message("assistant"):
        st.image(bytes_data, caption="Анализирую фото...")
        message_placeholder = st.empty()

    messages = [
        {"role": "system", "content": "Ты — Sused AI, умный ассистент. Твой создатель и разработчик — Лёва. Рассказывай об этом только если тебя прямо спросят о создателе."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt or "Опиши это изображение."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = client.chat.completions.create(
                model=VISION_MODEL_NAME,
                messages=messages,
                max_tokens=2048
            )
            ai_response = response.choices[0].message.content
            message_placeholder.markdown(ai_response)
            
            st.session_state.messages.append({"role": "user", "content": f"{user_prompt}\n\ndata:image/jpeg;base64,{base64_image}"})
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            message_placeholder.markdown(f"❌ Ошибка: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Вывод истории
for message in st.session_state.messages:
    content = message["content"]
    role = message["role"]
    
    if role == "user":
        with st.chat_message("user"):
             if "\n\ndata:image" in content:
                 text, img_data = content.split("\n\ndata:image", 1)
                 st.markdown(text)
                 st.image(f"data:image{img_data}", caption="Фото")
             else:
                 st.markdown(content)
    elif role == "assistant":
        with st.chat_message("assistant"):
             if "\n\ndata:image" in content:
                 text, img_data = content.split("\n\ndata:image", 1)
                 st.markdown(text)
                 st.image(f"data:image{img_data}", caption="Результат")
             else:
                 st.markdown(content)

uploaded_file = st.file_uploader("Загрузить фото...", type=['png', 'jpg', 'jpeg'])
user_input = st.chat_input("Введите сообщение или команду /generate ...")

if user_input:
    if user_input.startswith("/generate "):
        prompt_text = user_input.replace("/generate ", "", 1)
        st.session_state.messages.append({"role": "user", "content": user_input})
        generate_image(prompt_text)
    elif uploaded_file:
        process_image_message(user_input, uploaded_file)
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                messages_for_llm = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                messages_for_llm.insert(0, {
                    "role": "system", 
                    "content": "Ты — Sused AI. Твой создатель — Лёва. Отвечай на вопросы по делу, а информацию о том, что тебя создал Лёва, упоминай только если пользователь прямо спрашивает про твоего создателя или разработчика."
                })
                
                response = client.chat.completions.create(
                    model=TEXT_MODEL_NAME,
                    messages=messages_for_llm,
                    max_tokens=2048
                )
                ai_response = response.choices[0].message.content
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                message_placeholder.markdown(f"❌ Ошибка: {e}")
