import streamlit as st
import os
from openai import OpenAI
import requests

STABILITY_API_KEY = "sk-DFEaOMcYxvyso7NorFtGc6zaht2GGhOjlWlRZ7sDeewKJH9C"
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.environ.get("GROQ_API_KEY")

STABILITY_GENERATE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
STABILITY_INPAINT_URL = "https://api.stability.ai/v2beta/stable-image/edit/inpaint"

# Возвращаем wide макет, чтобы боковая панель (стрелочка) работала правильно
st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖", layout="wide")

# Минимализм: скрываем верхнюю панель Streamlit, ставим анимированный фон с дождем и красивую радугу
st.markdown("""
<style>
    /* Скрываем стандартную шапку, GitHub и Share */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppToolbar {display: none !important;}
    
    /* Анимированный фон с эффектом стекающих капель дождя по стеклу */
    .stApp {
        background-color: #0b131a;
        color: #e3e3e3;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(0, 150, 160, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(0, 100, 130, 0.1) 0%, transparent 50%),
            linear-gradient(180deg, rgba(11, 19, 26, 0.8) 0%, rgba(5, 10, 15, 0.95) 100%);
        background-attachment: fixed;
        position: relative;
    }

    /* Эффект капель через анимированные наложения */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient(rgba(255, 255, 255, 0.15) 1px, transparent 0);
        background-size: 35px 35px;
        animation: rain-drops 1.2s linear infinite;
        pointer-events: none;
        opacity: 0.6;
    }

    @keyframes rain-drops {
        0% { background-position: 0px 0px; }
        100% { background-position: -15px 70px; }
    }

    /* Компактный размер для сгенерированных изображений */
    img {
        max-width: 450px !important;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }

    /* Анимированная радужная полоса */
    .rainbow-track {
        width: 100%;
        height: 45px;
        background: linear-gradient(90deg, #ff0055, #ff7f00, #ffff00, #00ff66, #00ffff, #0066ff, #9900ff, #ff0055);
        background-size: 400% 400%;
        animation: rainbow-flow 4s ease infinite;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }

    @keyframes rainbow-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>

<script>
// Интерактивный шлейф за курсором в радужной полосе
const checkBanner = setInterval(() => {
    const banner = window.parent.document.getElementById('rainbow-banner');
    if (banner) {
        banner.onmousemove = function(e) {
            let x = e.clientX;
            let y = e.clientY;
            
            let dot = document.createElement('div');
            dot.style.position = 'fixed';
            dot.style.left = x + 'px';
            dot.style.top = y + 'px';
            dot.style.width = '12px';
            dot.style.height = '12px';
            dot.style.borderRadius = '50%';
            dot.style.pointerEvents = 'none';
            dot.style.zIndex = '999999';
            
            const colors = ['#ff0055', '#ff7f00', '#ffff00', '#00ff66', '#00ffff', '#0066ff', '#9900ff'];
            dot.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            dot.style.boxShadow = '0 0 12px ' + dot.style.backgroundColor;
            
            document.body.appendChild(dot);
            
            setTimeout(() => {
                dot.style.transition = 'all 0.4s ease-out';
                dot.style.transform = 'scale(0.1) translateY(-20px)';
                dot.style.opacity = '0';
            }, 20);
            
            setTimeout(() => {
                dot.remove();
            }, 420);
        };
        clearInterval(checkBanner);
    }
}, 200);
</script>
""", unsafe_allow_html=True)

# --- БОКОВАЯ ПАНЕЛЬ (ИСТОРИЯ И СТРЕЛОЧКА) ---
with st.sidebar:
    st.title("💬 Сохраненные чаты")
    if st.button("➕ Новая сессия", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    if "messages" in st.session_state and st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.text(f"👤 {i+1}. {msg['content'][:18]}...")
    else:
        st.info("История пуста.")

st.title("🤖 Sused AI Pro Max")

# Радужная полоса
st.markdown('<div id="rainbow-banner" class="rainbow-track"></div>', unsafe_allow_html=True)

# Инициализация клиента и истории
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

# Загрузчик файлов для дорисовки / редактирования картинок
uploaded_file = st.file_uploader("🖼️ Загрузить картинку для изменения или дорисовки (необязательно)", type=['png', 'jpg', 'jpeg'])

user_input = st.chat_input("Напиши запрос (например: нарисуй кота, измени фон и т.д.) или задай вопрос...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # Умное определение намерения пользователя
        try:
            intent_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Analyze user intent. Reply ONLY with 'GENERATE' if they want to create/draw a new image, 'INPAINT' if they want to edit/modify/repaint an existing uploaded image, or 'CHAT' for normal text conversation."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=10
            )
            intent = intent_response.choices[0].message.content.strip().upper()
        except:
            intent = "CHAT"

        if uploaded_file and ("INPAINT" in intent or any(kw in user_input.lower() for kw in ["дорисуй", "измени", "поменяй", "переделай", "фото"])):
            st.info(f"🎨 Изменяю картинку: '{user_input}'...")
            
            payload = {
                "prompt": user_input,
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
                    st.image(response.content, caption=f"Результат: {user_input}")
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"Результат по фото: {user_input}",
                        "image": response.content
                    })
                else:
                    st.error(f"Ошибка API: {response.text}")
            except Exception as e:
                st.error(f"Ошибка: {e}")

        elif "GENERATE" in intent or any(kw in user_input.lower() for kw in ["нарисуй", "сгенерируй", "создай", "картинку", "арт", "фотообои"]):
            st.info(f"🌐 Генерирую изображение: '{user_input}'...")
            
            try:
                translation_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Translate the user prompt into a detailed English image generation prompt. Output ONLY the translated prompt text."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=200
                )
                english_prompt = translation_response.choices[0].message.content.strip()
            except:
                english_prompt = user_input

            headers = {
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "image/*"
            }
            files = {
                "prompt": (None, english_prompt),
                "output_format": (None, "jpeg")
            }

            try:
                response = requests.post(STABILITY_GENERATE_URL, headers=headers, files=files)
                if response.status_code == 200:
                    st.success("Готово!")
                    st.image(response.content, caption=f"Запрос: {user_input}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Сгенерировал по запросу: {user_input}",
                        "image": response.content
                    })
                else:
                    st.error(f"Ошибка API: {response.text}")
            except Exception as e:
                st.error(f"Ошибка: {e}")
        else:
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
