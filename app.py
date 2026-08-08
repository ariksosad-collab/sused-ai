import streamlit as st
import os
from openai import OpenAI
import base64
import requests
import json

# Настройка ключа (для сервера Streamlit и для ПК)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.environ.get("GROQ_API_KEY")

# Используем модель, которая умеет видеть (Vision)
VISION_MODEL_NAME = "llama-3.2-90b-vision-preview"

# --- НАСТРОЙКА ДЛЯ ГЕНЕРАЦИИ КАРТИНОК (через отдельный сервис, например, Black Forest Labs на Groq) ---
# ВАЖНО: Для генерации нужен доступ к соответствующим эндпоинтам Groq (если поддерживается)
# или использование стороннего API. Для примера используем простую имитацию через API Stability.
# Если ты хочешь генерацию именно внутри Groq, это требует отдельной настройки.
# Для простоты сейчас мы используем команду-заглушку.
IMAGE_GEN_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
STABILITY_API_KEY = st.secrets.get("STABILITY_API_KEY") # Это нужно добавить в Secrets!

st.set_page_config(page_title="Sused AI Pro", page_icon="🤖")

st.markdown("""<style>.stApp {background-color: #131314; color: #e3e3e3;}</style>""", unsafe_allow_html=True)

st.title("🤖 Sused AI Pro (Vision & Gen)")

if not api_key:
    st.error("Ключ не найден! Добавь GROQ_API_KEY в настройки (Secrets).")
    st.stop()

# Инициализация клиента
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# --- Функция для генерации изображений ---
def generate_image(prompt_text):
    with st.chat_message("assistant"):
        st.info(f"🎨 Пытаюсь сгенерировать: '{prompt_text}'...")
        
        if not STABILITY_API_KEY:
             st.error("API ключ для генерации не найден в Secrets!")
             st.session_state.messages.append({"role": "assistant", "content": "Ошибка генерации: нет ключа."})
             return

        payload = {
            "prompt": prompt_text,
            "output_format": "jpeg"
        }
        files = {'none': ''}
        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "image/*"
        }

        try:
            response = requests.post(
                IMAGE_GEN_API_URL,
                headers=headers,
                files=files,
                data=payload,
            )
            
            if response.status_code == 200:
                image_base64 = base64.b64encode(response.content).decode('utf-8')
                st.image(f"data:image/jpeg;base64,{image_base64}", caption=f"Генерация по запросу: {prompt_text}")
                
                # Добавляем в историю
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Вот результат генерации по запросу: '{prompt_text}'\n\ndata:image/jpeg;base64,{image_base64}"
                })
            else:
                error_msg = response.json().get("errors", ["Unknown error"])[0]
                st.error(f"❌ Ошибка генерации: {error_msg}")
                st.session_state.messages.append({"role": "assistant", "content": f"Ошибка генерации: {error_msg}"})

        except Exception as e:
             st.error(f"❌ Исключение при генерации: {e}")
             st.session_state.messages.append({"role": "assistant", "content": f"Исключение при генерации: {e}"})


# --- Функция для обработки изображений в чате ---
def process_image_message(user_prompt, uploaded_file):
    # Конвертируем файл в base64
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    with st.chat_message("assistant"):
        st.image(bytes_data, caption="Анализирую ваше фото...")
        message_placeholder = st.empty()

    # Формируем сообщение для vision модели
    messages = [
        {"role": "system", "content": "Ты — Sused AI. Твой создатель и разработчик — Лёва."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Пользователь загрузил изображение и спрашивает: {user_prompt}"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
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
            
            # Добавляем в историю (сохраняем ссылку на изображение)
            st.session_state.messages.append({
                "role": "user", 
                "content": f"Пользователь загрузил фото и спросил: {user_prompt}\n\ndata:image/jpeg;base64,{base64_image}"
            })
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            message_placeholder.markdown(f"❌ Ошибка анализа фото: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"Ошибка анализа фото: {e}"})

# Инициализация сообщений (без системного промпта в истории для красоты)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение истории
for message in st.session_state.messages:
    content = message["content"]
    role = message["role"]
    
    if role == "user":
        with st.chat_message("user"):
             # Если в сообщении есть данные картинки
             if "\n\ndata:image" in content:
                 text, img_data = content.split("\n\ndata:image", 1)
                 st.markdown(text)
                 st.image(f"data:image{img_data}", caption="Загруженное фото")
             else:
                 st.markdown(content)
    
    elif role == "assistant":
        with st.chat_message("assistant"):
             # Если в ответе есть сгенерированная картинка
             if "\n\ndata:image" in content:
                 text, img_data = content.split("\n\ndata:image", 1)
                 st.markdown(text)
                 st.image(f"data:image{img_data}", caption="Результат генерации")
             else:
                 st.markdown(content)

# Основной ввод
uploaded_file = st.file_uploader("Загрузить фото...", type=['png', 'jpg', 'jpeg'])
user_input = st.chat_input("Введите сообщение или команду /generate...")

if user_input:
    # Проверка на команду генерации
    if user_input.startswith("/generate "):
        prompt_text = user_input.replace("/generate ", "", 1)
        st.session_state.messages.append({"role": "user", "content": f"Команда генерации: {user_input}"})
        generate_image(prompt_text)

    # Если есть фото для анализа
    elif uploaded_file:
        process_image_message(user_input, uploaded_file)

    # Обычный текстовый чат
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                # Для обычного текста используем оригинальную модель
                messages_for_llm = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                # Вставляем системный промпт в начало перед отправкой
                messages_for_llm.insert(0, {"role": "system", "content": "Ты — Sused AI. Твой создатель и разработчик — Лёва."})
                
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
