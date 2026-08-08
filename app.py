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

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖", layout="wide")

# Чистый темный стиль с анимированным дождем и интерактивной радужной полосой следования за курсором
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #e3e3e3;
        background-image: linear-gradient(0deg, rgba(0, 183, 255, 0.08) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 183, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 80px;
        animation: falling-rain 0.7s linear infinite;
    }
    
    @keyframes falling-rain {
        0% { background-position: 0px 0px; }
        100% { background-position: -40px 600px; }
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Анимированная интерактивная радужная полоса для курсора */
    .rainbow-track {
        width: 100%;
        height: 60px;
        background: linear-gradient(90deg, #ff0055, #ff7f00, #ffff00, #00ff66, #00ffff, #0066ff, #9900ff, #ff0055);
        background-size: 400% 400%;
        animation: rainbow-flow 4s ease infinite;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.4);
        cursor: pointer;
    }

    @keyframes rainbow-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>

<script>
// Интерактивный шлейф и следование радуги за курсором мыши внутри полосы
const checkBanner = setInterval(() => {
    const banner = window.parent.document.getElementById('rainbow-banner');
    if (banner) {
        banner.onmousemove = function(e) {
            let rect = banner.getBoundingClientRect();
            let x = e.clientX;
            let y = e.clientY;
            
            let dot = document.createElement('div');
            dot.style.position = 'fixed';
            dot.style.left = x + 'px';
            dot.style.top = y + 'px';
            dot.style.width = '16px';
            dot.style.height = '16px';
            dot.style.borderRadius = '50%';
            dot.style.pointerEvents = 'none';
            dot.style.zIndex = '999999';
            
            const colors = ['#ff0055', '#ff7f00', '#ffff00', '#00ff66', '#00ffff', '#0066ff', '#9900ff'];
            dot.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            dot.style.boxShadow = '0 0 15px ' + dot.style.backgroundColor;
            
            document.body.appendChild(dot);
            
            setTimeout(() => {
                dot.style.transition = 'all 0.5s ease-out';
                dot.style.transform = 'scale(0.1) translateY(-30px)';
                dot.style.opacity = '0';
            }, 20);
            
            setTimeout(() => {
                dot.remove();
            }, 520);
        };
        clearInterval(checkBanner);
    }
}, 200);
</script>
""", unsafe_allow_html=True)

# --- ПРАВАЯ ПАНЕЛЬ ИСТОРИИ ---
with st.sidebar:
    st.title("💬 Сохраненные чаты")
    st.markdown("История твоих диалогов.")
    
    if st.button("➕ Новая сессия", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    
    if "messages" in st.session_state and st.session_state.messages:
        st.subheader("Диалоги:")
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.text(f"👤 {i+1}. {msg['content'][:20]}...")
    else:
        st.info("История пуста.")

st.title("🤖 Sused AI Pro Max")

# Интерактивная радужная полоса
st.markdown('<div id="rainbow-banner" class="rainbow-track"></div>', unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ ИСТОРИИ ЧАТА ---
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

# Загрузка / вставка картинок для редактирования или домалевок (Inpainting)
uploaded_file = st.file_uploader("📋 Загрузи или вставь картинку сюда, чтобы дорисовать или изменить её", type=['png', 'jpg', 'jpeg'])

user_input = st.chat_input("Напиши текстовый запрос: создай картинку, измени фото или просто задай вопрос...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Умное определение намерения пользователя с помощью LLM (нужно ли генерировать картинку или это обычный чат/дорисовка)
    with st.chat_message("assistant"):
        try:
            # Спрашиваем модель: является ли запрос запросом на генерацию нового изображения
            intent_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Analyze the user's message. If the user is asking to create, generate, draw, or make an image/picture/art, reply with 'GENERATE'. If they are asking to edit, modify, repaint, or change an uploaded image, reply with 'INPAINT'. Otherwise reply with 'CHAT'."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=10
            )
            intent = intent_response.choices[0].message.content.strip().upper()
        except:
            intent = "CHAT"

        if uploaded_file and ("INPAINT" in intent or "ДОРИСУЙ" in user_input.upper() / 1 == 1 or len(user_input) > 0):
            # Если есть картинка и пользователь просит что-то изменить / дорисовать
            st.info(f"🎨 Изменяю/дорисовываю фото: '{user_input}'...")
            
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

        elif "GENERATE" in intent or any(kw in user_input.lower() for kw in ["нарисуй", "сгенерируй", "создай картинку", "картинка", "арты", "фото"]):
            # Если пользователь просит создать картинку
            st.info(f"🌐 Перевожу и генерирую изображение: '{user_input}'...")
            
            try:
                translation_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Translate the following user prompt into a detailed English image generation prompt. Output ONLY the translated prompt text, nothing else."},
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
            # Обычный текстовый диалог с ассистентом
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
