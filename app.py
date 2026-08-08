import streamlit as st
import os
from openai import OpenAI
import requests

# Ключи
STABILITY_API_KEY = "sk-DFEaOMcYxvyso7NorFtGc6zaht2GGhOjlWlRZ7sDeewKJH9C"
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.environ.get("GROQ_API_KEY")

# URL для генерации картинок по тексту (Stable Image Core)
STABILITY_GENERATE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
# URL для инпаинтинга (правки фото)
STABILITY_INPAINT_URL = "https://api.stability.ai/v2beta/stable-image/edit/inpaint"

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖")
st.markdown("<style>.stApp {background-color: #131314; color: #e3e3e3;}</style>", unsafe_allow_html=True)

st.title("🤖 Sused AI Pro Max")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

uploaded_file = st.file_uploader("Загрузить фото для редактирования (необязательно)", type=['png', 'jpg', 'jpeg'])

user_input = st.chat_input("Напиши /generate [текст] для картинки или /inpainting [текст] для фото")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 1. Генерация картинки с нуля по команде /generate
    if user_input.startswith("/generate "):
        prompt_text = user_input.replace("/generate ", "", 1)
        with st.chat_message("assistant"):
            st.info(f"🎨 Генерирую картинку: '{prompt_text}'...")
            
            headers = {
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "image/*"
            }
            # Используем multipart/form-data для Stability AI v2beta
            files = {
                "prompt": (None, prompt_text),
                "output_format": (None, "jpeg")
            }

            try:
                response = requests.post(
                    STABILITY_GENERATE_URL,
                    headers=headers,
                    files=files
                )
                if response.status_code == 200:
                    st.success("Готово!")
                    st.image(response.content, caption=f"Результат: {prompt_text}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Сгенерировал по запросу: {prompt_text}",
                        "image": response.content
                    })
                else:
                    st.error(f"Ошибка API: {response.text}")
            except Exception as e:
                st.error(f"Ошибка: {e}")

    # 2. Редактирование фото по команде /inpainting
    elif user_input.startswith("/inpainting "):
        if uploaded_file:
            prompt_text = user_input.replace("/inpainting ", "", 1)
            with st.chat_message("assistant"):
                st.info(f"🎨 Изменяю фото: '{prompt_text}'...")
                
                payload = {
                    "prompt": prompt_text,
                    "output_format": "jpeg",
                    "strength": 0.8
                }
                files = {'image': ('input.jpg', uploaded_file.getvalue(), 'image/jpeg')}
                headers = {
                    "Authorization": f"Bearer {STABILITY_API_KEY}",
                    "Accept": "image/*"
                }

                try:
                    response = requests.post(STABILITY_INPAINT_URL, headers=headers, files=files, data=payload)
                    if response.status_code == 200:
                        st.success("Готово!")
                        st.image(response.content, caption=f"Результат: {prompt_text}")
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f"Результат по фото: {prompt_text}",
                            "image": response.content
                        })
                    else:
                        st.error(f"Ошибка API: {response.text}")
                except Exception as e:
                    st.error(f"Ошибка: {e}")
        else:
            with st.chat_message("assistant"):
                st.warning("Сначала загрузи картинку сверху для использования /inpainting!")

    # 3. Обычное текстовое общение через Groq
    else:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                messages_for_llm = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                messages_for_llm.insert(0, {
                    "role": "system", 
                    "content": "Ты — Sused AI, крутой ассистент. Твой создатель — Лёва."
                })
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_llm,
                    max_tokens=2048
                )
                ai_response = response.choices[0].message.content
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                message_placeholder.markdown(f"❌ Ошибка: {e}")
