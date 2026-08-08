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

if "bg_theme" not in st.session_state:
    st.session_state.bg_theme = "Темная"
if "fx_effect" not in st.session_state:
    st.session_state.fx_effect = "Без эффекта"

bg_colors = {
    "Темная": "#131314",
    "Светлая": "#f0f2f6",
    "Неоновая": "#0a0a1a",
    "Киберпанк": "#1a001a"
}
text_colors = {
    "Темная": "#e3e3e3",
    "Светлая": "#111111",
    "Неоновая": "#00ffff",
    "Киберпанк": "#ff00ff"
}

current_bg = bg_colors.get(st.session_state.bg_theme, "#131314")
current_txt = text_colors.get(st.session_state.bg_theme, "#e3e3e3")

# Обычная строка без f, чтобы Python не ругался на скобки JS
st.markdown("""
<style>
    .stApp {
        background-color: """ + current_bg + """;
        color: """ + current_txt + """;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    #rainbow-banner {
        width: 100%;
        height: 120px;
        background: linear-gradient(90deg, #1f1f23, #2d2d38, #1f1f23);
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
        border: 1px solid #333;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    #rainbow-banner h2 {
        background: linear-gradient(90deg, #ff0055, #ff7f00, #ffff00, #00ff66, #00ffff, #9900ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        margin: 0;
    }
</style>

<script>
document.addEventListener('mousemove', function(e) {
    let x = e.clientX;
    let y = e.clientY;
    
    if (y < 250) {
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
        dot.style.boxShadow = '0 0 10px ' + dot.style.backgroundColor;
        
        document.body.appendChild(dot);
        
        setTimeout(() => {
            dot.style.transition = 'all 0.5s ease';
            dot.style.transform = 'scale(0.2)';
            dot.style.opacity = '0';
        }, 30);
        
        setTimeout(() => {
            dot.remove();
        }, 530);
    }
});
</script>
""", unsafe_allow_html=True)

# --- ПРАВАЯ ПАНЕЛЬ СОХРАНЕННЫХ ЧАТОВ ---
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

# --- ПУЛЬТ НАСТРОЕК В ПРАВОМ УГЛУ ---
col_title, col_settings = st.columns([2, 2])

with col_title:
    st.title("🤖 Sused AI Pro Max")

with col_settings:
    st.markdown("<div style='text-align: right;'>⚙️ <b>Настройки темы и эффектов</b></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.bg_theme = st.selectbox("Фон", ["Темная", "Светлая", "Неоновая", "Киберпанк"], label_visibility="collapsed")
    with c2:
        st.session_state.fx_effect = st.selectbox("Эффект", ["Без эффекта", "🌧️ Дождь", "⚡ Молнии/Гроза", "✨ Звезды"], label_visibility="collapsed")

# --- ВЕРХНИЙ ДЛИННЫЙ БАННЕР С РАДУЖНЫМ КУРСОРОМ ---
st.markdown("""
<div id="rainbow-banner">
    <h2>✨ Наведи курсор сюда для радужного шлейфа! ✨</h2>
</div>
""", unsafe_allow_html=True)

# --- ВИЗУАЛЬНЫЕ ЭФФЕКТЫ ---
if st.session_state.fx_effect == "🌧️ Дождь":
    st.markdown("""
    <style>
    @keyframes rain {
        0% {background-position: 0px 0px;}
        100% {background-position: -50px 500px;}
    }
    .stApp {
        background-image: linear-gradient(0deg, rgba(255,255,255,0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: rain 0.8s linear infinite;
    }
    </style>
    """, unsafe_allow_html=True)
elif st.session_state.fx_effect == "⚡ Молнии/Гроза":
    st.markdown("""
    <style>
    @keyframes flash {
        0%, 90%, 95%, 100% {opacity: 1;}
        92%, 97% {opacity: 0.3; filter: brightness(1.8); background-color: #334466;}
    }
    .stApp {
        animation: flash 4s infinite;
    }
    </style>
    """, unsafe_allow_html=True)
elif st.session_state.fx_effect == "✨ Звезды":
    st.markdown("""
    <style>
    .stApp {
        background-image: radial-gradient(white 1px, transparent 0);
        background-size: 40px 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГИКА ЧАТА И ГЕНЕРАЦИИ ---
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

user_input = st.chat_input("Напиши /generate [описание] для картинки или просто общайся")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if user_input.startswith("/generate "):
        raw_prompt = user_input.replace("/generate ", "", 1)
        with st.chat_message("assistant"):
            st.info(f"🌐 Перевожу и генерирую: '{raw_prompt}'...")
            
            try:
                translation_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Translate the following user prompt into a detailed English image generation prompt. Output ONLY the translated prompt text, nothing else."},
                        {"role": "user", "content": raw_prompt}
                    ],
                    max_tokens=200
                )
                english_prompt = translation_response.choices[0].message.content.strip()
            except:
                english_prompt = raw_prompt

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
                    st.image(response.content, caption=f"Запрос: {raw_prompt}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Сгенерировал по запросу: {raw_prompt}",
                        "image": response.content
                    })
                else:
                    st.error(f"Ошибка API: {response.text}")
            except Exception as e:
                st.error(f"Ошибка: {e}")

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
                    "Authorization": f"Bearer {STBILITY_API_KEY}" if 'STBILITY_API_KEY' in locals() else f"Bearer {STABILITY_API_KEY}",
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
