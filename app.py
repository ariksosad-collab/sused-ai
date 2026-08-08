import streamlit as st
import os
from openai import OpenAI
import requests
import re
import urllib.parse

# Настройка ключа Groq для чата
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.environ.get("GROQ_API_KEY")

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# Стили интерфейса
st.markdown(
    """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppToolbar {display: none !important;}
    
    [data-testid="stSidebar"] {
        background-color: #091216 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        min-width: 260px !important;
        max-width: 260px !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    .cat-cover {
        position: fixed;
        bottom: 5px;
        right: 10px;
        z-index: 999999;
        background: #0d1b1e;
        padding: 4px 10px;
        border-radius: 12px;
        border: 1px solid rgba(0, 255, 200, 0.3);
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.8);
    }
    .cat-cover img {
        width: 32px !important;
        height: 32px !important;
        border-radius: 50%;
    }
    .cat-cover span {
        font-size: 11px;
        color: #00ffc4;
        font-family: monospace;
    }

    .stApp {
        background-color: #0d1b1e;
        color: #e3e3e3;
        background-image: 
            radial-gradient(circle at 15% 20%, rgba(0, 168, 150, 0.2) 0%, transparent 35%),
            radial-gradient(circle at 85% 80%, rgba(29, 53, 87, 0.25) 0%, transparent 40%),
            linear-gradient(180deg, #0b131a 0%, #050b10 100%);
        background-attachment: fixed;
    }

    img, video {
        max-width: 480px !important;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }

    .rainbow-track {
        width: 100%;
        height: 35px;
        background: linear-gradient(90deg, #ff0055, #ff7f00, #ffff00, #00ff66, #00ffff, #0066ff, #9900ff, #ff0055);
        background-size: 400% 400%;
        animation: rainbow-flow 4s ease infinite;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }

    @keyframes rainbow-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Инициализация состояний
if "messages" not in st.session_state:
  st.session_state.messages = []
if "current_tab" not in st.session_state:
  st.session_state.current_tab = "💬 Чат"

# Боковое меню
with st.sidebar:
  st.markdown("### ✨ Gemini Меню")
  st.divider()

  if st.button("✏️ Новый чат", use_container_width=True):
    st.session_state.messages = []
    st.session_state.current_tab = "💬 Чат"
    st.rerun()

  if st.button("🎥 Видео / Визуал", use_container_width=True):
    st.session_state.current_tab = "🎥 Видео"
    st.rerun()

  if st.button("💬 Чат с ИИ", use_container_width=True):
    st.session_state.current_tab = "💬 Чат"
    st.rerun()

  st.divider()
  st.markdown("**Недавние чаты:**")
  if st.session_state.messages:
    for msg in st.session_state.messages:
      if msg["role"] == "user":
        st.text(f"• {msg['content'][:25]}...")
  else:
    st.caption("История пока пуста")

st.title("🤖 Sused AI Pro Max")
st.markdown('<div class="rainbow-track"></div>', unsafe_allow_html=True)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=groq_api_key
)

# Вкладка генерации визуала (бесплатно)
if st.session_state.current_tab == "🎥 Видео":
  st.subheader("🎥 Бесплатная генерация визуала / кадров")
  st.write("Опиши подробно сцену, и ИИ сгенерирует изображение бесплатно.")

  video_prompt = st.text_area(
      "✍️ Описание кадра:",
      placeholder="Например: Cinematic view of a futuristic city...",
  )

  if st.button("🚀 Создать бесплатно", use_container_width=True):
    if video_prompt:
      with st.spinner("✨ Генерация..."):
        try:
          encoded_prompt = urllib.parse.quote(
              video_prompt + ", cinematic lighting, 4k"
          )
          free_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"

          st.success("✨ Готово!")
          st.image(free_image_url, caption=f"Запрос: {video_prompt}")

          st.session_state.messages.append({
              "role": "assistant",
              "content": f"Сгенерировал визуал: {video_prompt}",
              "image_url": free_image_url,
          })
        except Exception as e:
          st.error(f"Ошибка: {e}")
    else:
      st.warning("Введи описание!")

# Вкладка чата
else:
  ai_mode = st.radio(
      "🎯 Выбери режим работы ИИ:",
      ["🎮 Игровой режим", "🧠 Глубокий (думающий)", "🔥 Мемный режим"],
      horizontal=True,
  )

  st.divider()

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])
      if "image" in message:
        st.image(message["image"])
      elif "image_url" in message:
        st.image(message["image_url"])

  uploaded_file = st.file_uploader(
      "🖼️ Загрузить картинку (необязательно)", type=["png", "jpg", "jpeg"]
  )
  user_input = st.chat_input("Напиши запрос...")

  if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
      st.markdown(user_input)

    with st.chat_message("assistant"):
      try:
        intent_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Reply ONLY with 'GENERATE' if user wants to draw/create"
                        " an image, or 'CHAT'."
                    ),
                },
                {"role": "user", "content": user_input},
            ],
            max_tokens=10,
        )
        intent = intent_response.choices[0].message.content.strip().upper()
      except:
        intent = "CHAT"

      if "GENERATE" in intent or any(
          kw in user_input.lower()
          for kw in [
              "нарисуй",
              "сгенерируй",
              "создай",
              "картинку",
              "арт",
              "превью",
              "обложк",
          ]
      ):
        st.info(f"🎨 Рисую бесплатно: '{user_input}'...")
        encoded_prompt = urllib.parse.quote(
            user_input + ", vibrant YouTube thumbnail style, 4k"
        )
        free_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

        st.success("Готово!")
        st.image(free_image_url, caption=f"Превью: {user_input}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Создал превью по запросу: {user_input}",
            "image_url": free_image_url,
        })
      else:
        message_placeholder = st.empty()
        try:
          base_identity = (
              "Твой создатель, разработчик и босс — Лёва (пользователь)."
          )
          if "Игровой" in ai_mode:
            system_prompt = f"Ты — Sused AI в игровом режиме. {base_identity}"
          elif "Глубокий" in ai_mode:
            system_prompt = (
                f"Ты — Sused AI в режиме глубокого анализа. {base_identity}"
            )
          else:
            system_prompt = (
                f"Ты — Sused AI в мемном режиме. {base_identity} Юмори и"
                " используй сленг."
            )

          messages_for_llm = [
              {"role": m["role"], "content": m["content"]}
              for m in st.session_state.messages
          ]
          messages_for_llm.insert(
              0, {"role": "system", "content": system_prompt}
          )

          response = client.chat.completions.create(
              model="llama-3.3-70b-versatile",
              messages=messages_for_llm,
              max_tokens=2048,
          )
          ai_response = response.choices[0].message.content
          message_placeholder.markdown(ai_response)
          st.session_state.messages.append(
              {"role": "assistant", "content": ai_response}
          )
        except Exception as e:
          message_placeholder.markdown(f"❌ Ошибка: {e}")
