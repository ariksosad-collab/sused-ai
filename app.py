import streamlit as st
import os
from openai import OpenAI

# Настройка ключа Groq для чата
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.environ.get("GROQ_API_KEY")

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# --- УЛЬТРА-ДИЗАЙН И КИБЕРПАНК СТИЛИ ---
st.markdown(
    """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppToolbar {display: none !important;}
    
    /* Жесткая фиксация сайдбара */
    [data-testid="stSidebar"] {
        background-color: #050b0f !important;
        border-right: 1px solid rgba(0, 255, 204, 0.15);
        min-width: 280px !important;
        max-width: 280px !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Общий фон */
    .stApp {
        background-color: #070e14;
        color: #e2e8f0;
        background-image: 
            radial-gradient(circle at 10% 10%, rgba(0, 255, 170, 0.06) 0%, transparent 40%),
            radial-gradient(circle at 90% 90%, rgba(0, 102, 255, 0.06) 0%, transparent 40%),
            linear-gradient(180deg, #070e14 0%, #030609 100%);
        background-attachment: fixed;
    }

    /* Кастомизация полей ввода */
    .stTextInput input, .stTextArea textarea {
        background-color: #0d1620 !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 255, 204, 0.25) !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00ffcc !important;
        box-shadow: 0 0 12px rgba(0, 255, 204, 0.3);
    }

    /* Радужная линия */
    .rainbow-track {
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #00ffcc, #0066ff, #9900ff, #ff0055, #00ffcc);
        background-size: 400% 400%;
        animation: rainbow-flow 6s linear infinite;
        border-radius: 4px;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
    }

    @keyframes rainbow-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Кнопки */
    .stButton button {
        background: linear-gradient(135deg, #00b4d8 0%, #0077b6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 180, 216, 0.2);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0, 255, 204, 0.4);
        background: linear-gradient(135deg, #00ffcc 0%, #00b4d8 100%);
        color: #03070a;
    }

    /* Кастомные контейнеры чата */
    [data-testid="stChatMessage"] {
        background-color: #0d1620 !important;
        border: 1px solid rgba(0, 255, 204, 0.1) !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        padding: 15px;
        margin-bottom: 12px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Состояния
if "messages" not in st.session_state:
  st.session_state.messages = []
if "current_tab" not in st.session_state:
  st.session_state.current_tab = "💬 Чат с ИИ"

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
  st.markdown("### ✨ Sused Control Hub")
  st.divider()

  if st.button("✏️ Новый чат", use_container_width=True):
    st.session_state.messages = []
    st.session_state.current_tab = "💬 Чат с ИИ"
    st.rerun()

  if st.button("💬 Чат с ИИ", use_container_width=True):
    st.session_state.current_tab = "💬 Чат с ИИ"
    st.rerun()

  if st.button("🛠️ Студия кода и утилит", use_container_width=True):
    st.session_state.current_tab = "🛠️ Утилиты"
    st.rerun()

  st.divider()
  st.markdown("**История запросов:**")
  if st.session_state.messages:
    for msg in st.session_state.messages:
      if msg["role"] == "user":
        st.text(f"• {msg['content'][:22]}...")
  else:
    st.caption("История пуста")

st.title("🤖 Sused AI Pro Max")
st.markdown('<div class="rainbow-track"></div>', unsafe_allow_html=True)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=groq_api_key
)

# --- ВКЛАДКА: СТУДИЯ КОДА И УТИЛИТ ---
if st.session_state.current_tab == "🛠️ Утилиты":
  st.subheader("🛠️ Элитная студия разработки")
  st.write("Генератор кода с выбором уровня интеллекта и проработки:")

  tool_type = st.selectbox(
      "📌 Выбери инструмент:",
      ["📝 Генератор кода (Java / Python / Mods)", "🛒 Шаблоны ответов для FunPay"]
  )

  if tool_type == "📝 Генератор кода (Java / Python / Mods)":
    # Выбор режима кодинга
    code_mode = st.radio(
        "🧠 Режим генерации кода:",
        [
            "⚡ Умный режим (Хардкор: чистый рабочий код без заглушек, математика векторов, Fabric 1.21.4)",
            "🟢 Обычный режим (Базовый, простой код для учебы или быстрых задач)"
        ],
        horizontal=False
    )

    code_task = st.text_area("✍️ Подробно опиши задачу для кода:", placeholder="Например: напиши AimAssist под Fabric 1.21.4 с плавной интерполяцией...")
    lang = st.radio("Язык / Платформа:", ["Java (Minecraft Fabric)", "Python", "Другое"], horizontal=True)

    if st.button("🚀 Запустить генерацию кода", use_container_width=True):
      if code_task:
        with st.spinner("💻 ИИ пишет код..."):
          try:
            if "Умный режим" in code_mode:
              dev_system_prompt = (
                  "Ты — элитный старший разработчик софта и модификаций для Minecraft (Fabric 1.21.4, Yarn маппинги) и эксперт по Python/Java. "
                  "Твоя задача — писать абсолютно чистый, рабочий, законченный код от начала и до конца. "
                  "КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО использовать ленивые комментарии вроде '// тут допишите сами', '// ...', '// TODO' или оставлять пустые методы. "
                  "Всегда пиши полную логику: если это AimAssist, TriggerBot или модули клиента — пиши реальную математику векторов, расчеты Yaw/Pitch, плавную доводку и Raycast-проверки. "
                  "Выдавай код строго в блоках разметки Markdown."
              )
            else:
              dev_system_prompt = (
                  "Ты — помощник по программированию. Пиши понятный, простой и рабочий код без лишней сложности, с базовыми комментариями."
              )
            
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": dev_system_prompt},
                    {"role": "user", "content": f"Язык/Платформа: {lang}\nЗадача: {code_task}"}
                ],
                max_tokens=3072
            )
            generated_code = resp.choices[0].message.content
            st.markdown(generated_code)
          except Exception as e:
            st.error(f"Ошибка: {e}")
      else:
        st.warning("Введи задачу для кода!")

  else:
    fp_task = st.text_area("✍️ Ситуация для авто-ответа на FunPay:", placeholder="Например: покупатель оплатил донат-кейс на сервере, нужно выдать товар...")
    if st.button("🚀 Сгенерировать шаблон", use_container_width=True):
      if fp_task:
        with st.spinner("✍️ Создаю профессиональный шаблон..."):
          try:
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Ты — профессиональный продавец на маркетплейсе FunPay. Пиши вежливые, четкие, готовые к отправке шаблоны сообщений для покупателей."},
                    {"role": "user", "content": fp_task}
                ],
                max_tokens=600
            )
            st.info(resp.choices[0].message.content)
          except Exception as e:
            st.error(f"Ошибка: {e}")
      else:
        st.warning("Введи описание ситуации!")

# --- ВКЛАДКА: ЧАТ И РЕЖИМЫ ИИ ---
else:
  ai_mode = st.radio(
      "🎯 Выбери режим работы ИИ:",
      ["🎮 Игровой режим (Minecraft)", "🧠 Глубокий (думающий аналитик)", "🔥 Мемный режим"],
      horizontal=True,
  )

  st.divider()

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  user_input = st.chat_input("Напиши запрос для Sused AI...")

  if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
      st.markdown(user_input)

    with st.chat_message("assistant"):
      message_placeholder = st.empty()
      try:
        base_identity = (
            "Твой создатель, разработчик и босс — Лёва (то есть пользователь). Общайся с ним на «ты», уважительно и по-братски."
        )
        if "Игровой" in ai_mode:
          system_prompt = f"Ты — Sused AI в игровом режиме. {base_identity} Отлично разбираешься в Minecraft, серверах (включая FunTime), клиентах, модах под Fabric и джаве."
        elif "Глубокий" in ai_mode:
          system_prompt = (
              f"Ты — Sused AI в режиме глубокого анализа. {base_identity} Пиши глубокие технические ответы, детальный код и архитектурные решения без воды."
          )
        else:
          system_prompt = (
              f"Ты — Sused AI в мемном режиме. {base_identity} Юмори, используй актуальный сленг, мемы и общайся максимально непринужденно."
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
