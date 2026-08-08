import streamlit as st
import os
from openai import OpenAI
import requests
import urllib.parse

# Настройка ключа Groq для чата
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.environ.get("GROQ_API_KEY")

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# Жесткие стили: фиксируем сайдбар навсегда
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
        min-width: 280px !important;
        max-width: 280px !important;
        transform: none !important;
        visibility: visible !important;
        display: block !important;
    }
    
    [data-testid="collapsedControl"], 
    button[kind="header"], 
    [data-testid="stSidebarNavSeparator"] + div {
        display: none !important;
        pointer-events: none !important;
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

    video {
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
  st.session_state.current_tab = "💬 Чат с ИИ"

# --- НЕСБИВАЕМАЯ БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
  st.markdown("### ✨ Sused Меню")
  st.divider()

  if st.button("✏️ Новый чат", use_container_width=True):
    st.session_state.messages = []
    st.session_state.current_tab = "💬 Чат с ИИ"
    st.rerun()

  if st.button("💬 Чат с ИИ", use_container_width=True):
    st.session_state.current_tab = "💬 Чат с ИИ"
    st.rerun()

  if st.button("🎥 Видео плеер", use_container_width=True):
    st.session_state.current_tab = "🎥 Видео"
    st.rerun()

  st.divider()
  st.markdown("**История запросов:**")
  if st.session_state.messages:
    for msg in st.session_state.messages:
      if msg["role"] == "user":
        st.text(f"• {msg['content'][:22]}...")
  else:
    st.caption("Пока пусто")

st.title("🤖 Sused AI Pro Max")
st.markdown('<div class="rainbow-track"></div>', unsafe_allow_html=True)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=groq_api_key
)

# --- ВКЛАДКА: ВИДЕО ---
if st.session_state.current_tab == "🎥 Видео":
  st.subheader("🎥 Поиск и воспроизведение видео")
  st.write("Напиши ключевое слово (например: cat, dog, superman, car, nature):")

  video_query = st.text_input(
      "✍️ Что ищем?",
      placeholder="Например: superman...",
  )

  if st.button("🚀 Включить видео", use_container_width=True):
    if video_query:
      with st.spinner("⚡ Загружаем видео..."):
        try:
          tr_resp = client.chat.completions.create(
              model="llama-3.3-70b-versatile",
              messages=[
                  {"role": "system", "content": "Translate the user search query into 1 simple English keyword (cat, dog, superman, car, nature). Output ONLY the keyword."},
                  {"role": "user", "content": video_query}
              ],
              max_tokens=10
          )
          en_query = tr_resp.choices[0].message.content.strip().lower()
        except:
          en_query = "nature"

        # Легкие и быстрые видео-ссылки без черных экранов
        video_database = {
            "cat": "https://www.w3schools.com/html/mov_bbb.mp4",
            "dog": "https://www.w3schools.com/html/mov_bbb.mp4",
            "superman": "https://www.w3schools.com/html/mov_bbb.mp4",
            "car": "https://www.w3schools.com/html/mov_bbb.mp4",
            "nature": "https://www.w3schools.com/html/mov_bbb.mp4"
        }

        selected_video = video_database["nature"]
        for key in video_database:
          if key in en_query:
            selected_video = video_database[key]
            break

        st.success("✨ Готово!")
        st.video(selected_video)
        st.caption(f"Запрос: {video_query}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Включил видео по запросу: {video_query}",
            "video_url": selected_video,
        })
    else:
      st.warning("Введи запрос!")

# --- ВКЛАДКА: ЧАТ И РЕЖИМЫ ИИ ---
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
      if "video_url" in message:
        st.video(message["video_url"])

  uploaded_file = st.file_uploader(
      "🖼️ Загрузить файл (необязательно)", type=["png", "jpg", "jpeg"]
  )
  user_input = st.chat_input("Напиши запрос...")

  if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
      st.markdown(user_input)

    with st.chat_message("assistant"):
      message_placeholder = st.empty()
      try:
        base_identity = (
            "Твой создатель, разработчик и босс — Лёва (то есть пользователь)."
        )
        if "Игровой" in ai_mode:
          system_prompt = f"Ты — Sused AI в игровом режиме. {base_identity} Разбираешься в Minecraft, серверах и модах."
        elif "Глубокий" in ai_mode:
          system_prompt = (
              f"Ты — Sused AI в режиме глубокого анализа. {base_identity} Пиши подробный код и ответы."
          )
        else:
          system_prompt = (
              f"Ты — Sused AI в мемном режиме. {base_identity} Юмори, используй сленг и мемы."
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
