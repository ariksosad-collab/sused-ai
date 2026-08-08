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

STABILITY_GENERATE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
STABILITY_INPAINT_URL = "https://api.stability.ai/v2beta/stable-image/edit/inpaint"

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖", layout="wide")

# Дизайн: скрываем верхнюю панель Streamlit (Share, GitHub и т.д.) и делаем радужный курсор
st.markdown("""
<style>
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    /* Полное скрытие стандартной шапки и меню Streamlit справа сверху */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stToolbar {display: none;}
    
    /* Стилизация сайдбара */
    [data-testid="stSidebar"] {
        background-color: #1a1a1c;
        border-left: 1px solid #333;
    }
</style>

<script>
// Яркий радужный след за курсором
document.addEventListener('mousemove', function(e) {
    let cursorTrail = document.createElement('div');
    cursorTrail.style.position = 'fixed';
    cursorTrail.style.left = e.pageX + 'px';
    cursorTrail.style.top = e.pageY + 'px';
    cursorTrail.style.width = '14px';
    cursorTrail.style.height = '14px';
    cursorTrail.style.borderRadius = '50%';
    cursorTrail.style.pointerEvents = 'none';
    cursorTrail.style.zIndex = '999999';
    
    const colors = ['#ff0055', '#ff7f00', '#ffff00', '#00ff66', '#00ffff', '#0066ff', '#9900ff'];
    cursorTrail.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    cursorTrail.style.boxShadow = '0 0 12px ' + cursorTrail.style.backgroundColor;
    
    document.body.appendChild(cursorTrail);
    
    setTimeout(() => {
        cursorTrail.style.transition = 'all 0.6s ease';
        cursorTrail.style.transform = 'scale(0.2)';
        cursorTrail.style.opacity = '0';
    }, 40);
    
    setTimeout(() => {
        cursorTrail.remove();
    }, 640);
});
</script>
""", unsafe_allow_html=True)

# --- ПРАВАЯ ВЫДВИГАЮЩАЯСЯ ПАНЕЛЬ (СОХРАНЕННЫЕ ЧАТЫ) ---
with st.sidebar:
    st.title("💬 Сохраненные чаты")
    st.markdown("История твоих запросов и сессий.")
    
    if st.button("➕ Новая сессия / Очистить чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    
    if "messages" in st.session_state and st.session_state.messages:
        st.subheader("Диалоги:")
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.text(f"👤 {i+1}. {msg['content'][:22]}...")
    else:
        st.info("Пока пусто.")

# --- ОСНОВНОЙ ЭКРАН ---
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

user_input = st.chat_input("Напиши /generate [описание] для картинки или просто общайся")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 1. Генерация картинки (/generate)
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

    # 2. Редактирование фото (/inpainting)
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

    # 3. Обычный чат
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
