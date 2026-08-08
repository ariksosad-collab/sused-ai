import streamlit as st
import os
from openai import OpenAI
import requests
import re

STABILITY_API_KEY = "sk-DFEaOMcYxvyso7NorFtGc6zaht2GGhOjlWlRZ7sDeewKJH9C"
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.environ.get("GROQ_API_KEY")

STABILITY_GENERATE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
STABILITY_INPAINT_URL = "https://api.stability.ai/v2beta/stable-image/edit/inpaint"

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

# CSS + Идеальная стрелочка и плавная панель чатов + Кот поверх Manage app
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppToolbar {display: none !important;}
    
    /* Закрываем плашку Manage app в правом нижнем углу гифкой кота */
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

    /* Анимированный фон с дождем */
    .stApp {
        background-color: #0d1b1e;
        color: #e3e3e3;
        background-image: 
            radial-gradient(circle at 15% 20%, rgba(0, 168, 150, 0.2) 0%, transparent 35%),
            radial-gradient(circle at 85% 80%, rgba(29, 53, 87, 0.25) 0%, transparent 40%),
            linear-gradient(180deg, #0b131a 0%, #050b10 100%);
        background-attachment: fixed;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient(rgba(100, 220, 255, 0.25) 1.5px, transparent 0);
        background-size: 30px 45px;
        animation: drop-rain 0.8s linear infinite;
        pointer-events: none;
    }

    @keyframes drop-rain {
        0% { background-position: 0px 0px; }
        100% { background-position: -10px 60px; }
    }

    /* Стильная кнопка-стрелочка в шапке */
    .custom-sidebar-btn {
        background: rgba(0, 255, 200, 0.1);
        border: 1px solid rgba(0, 255, 200, 0.4);
        color: #00ffc4;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 0 10px rgba(0, 255, 200, 0.1);
        user-select: none;
    }
    .custom-sidebar-btn:hover {
        background: rgba(0, 255, 200, 0.25);
        box-shadow: 0 0 15px rgba(0, 255, 200, 0.4);
        transform: scale(1.05);
    }

    /* Шапка сайта */
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
    }

    /* Сайдбар плавная подсветка элементов */
    [data-testid="stSidebar"] .element-container div p {
        transition: all 0.2s ease;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 6px;
    }
    [data-testid="stSidebar"] .element-container div p:hover {
        background-color: rgba(0, 255, 200, 0.1);
        color: #00ffc4;
        padding-left: 14px;
    }
    [data-testid="stSidebar"] .element-container div p:hover::before {
        content: "➡️ ";
    }

    /* Размер картинок в чате */
    img {
        max-width: 450px !important;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }

    /* Радужная полоса */
    .rainbow-track {
        width: 100%;
        height: 40px;
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

<script>
// Внедряем гифку кота поверх Manage app
const addCatCover = setInterval(() => {
    try {
        const doc = window.parent.document;
        if (!doc.getElementById('custom-cat-cover')) {
            const cover = doc.createElement('div');
            cover.id = 'custom-cat-cover';
            cover.className = 'cat-cover';
            cover.innerHTML = '<img src="https://media.giphy.com/media/JQXaVaXLadghi/giphy.gif"><span>Sused Protected 🐾</span>';
            doc.body.appendChild(cover);
        }
    } catch(e) {}
}, 100);

// Шлейф за курсором в радужной полосе
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
            window.parent.document.body.appendChild(dot);
            setTimeout(() => {
                dot.style.transition = 'all 0.4s ease-out';
                dot.style.transform = 'scale(0.1) translateY(-20px)';
                dot.style.opacity = '0';
            }, 20);
            setTimeout(() => { dot.remove(); }, 420);
        };
        clearInterval(checkBanner);
    }
}, 200);
</script>
""", unsafe_allow_html=True)

# Инициализация состояния сайдбара
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = False

# --- БОКОВАЯ ПАНЕЛЬ ДЛЯ ЧАТОВ ---
if st.session_state.sidebar_state:
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

# Шапка со стрелочкой слева и названием
col_arrow, col_title = st.columns([0.08, 0.92])
with col_arrow:
    st.markdown("<br>", unsafe_allow_html=True)
    arrow_symbol = "◀" if st.session_state.sidebar_state else "▶"
    if st.button(arrow_symbol, help="Открыть/Закрыть сохраненные чаты"):
        st.session_state.sidebar_state = not st.session_state.sidebar_state
        st.rerun()
with col_title:
    st.title("🤖 Sused AI Pro Max")

# Радужная полоса
st.markdown('<div id="rainbow-banner" class="rainbow-track"></div>', unsafe_allow_html=True)

# ВЫБОР РЕЖИМОВ
ai_mode = st.radio(
    "🎯 Выбери режим работы ИИ:",
    ["🎮 Игровой режим", "🧠 Глубокий (думающий)", "🔥 Мемный режим"],
    horizontal=True
)

st.divider()

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

uploaded_file = st.file_uploader("🖼️ Загрузить картинку для изменения или дорисовки (необязательно)", type=['png', 'jpg', 'jpeg'])

user_input = st.chat_input("Напиши запрос, скинь ссылку на TikTok или попроси сделать превью...")

# Функция для TikTok
def get_tiktok_info(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://www.tiktok.com/oembed?url={url}", headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return f"[TikTok Видео] Автор: {data.get('author_name', 'Неизвестно')}, Заголовок/Описание: {data.get('title', 'Без описания')}"
    except:
        pass
    return f"Ссылка на TikTok видео: {url}"

if user_input:
    tiktok_match = re.search(r'(https?://(?:www\.)?(?:tiktok\.com/@[^/]+/video/\d+|vm\.tiktok\.com/\w+|vt\.tiktok\.com/\w+))', user_input)
    processed_input = user_input
    if tiktok_match:
        tt_url = tiktok_match.group(1)
        tt_data = get_tiktok_info(tt_url)
        processed_input = f"{user_input}\n\nКонтекст из TikTok: {tt_data}"

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            intent_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Analyze user intent. Reply ONLY with 'GENERATE' if they want to create/draw a new image or thumbnail/preview, 'INPAINT' if they want to edit/modify/repaint an existing uploaded image, or 'CHAT' for normal text conversation."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=10
            )
            intent = intent_response.choices[0].message.content.strip().upper()
        except:
            intent = "CHAT"

        if uploaded_file and ("INPAINT" in intent or any(kw in user_input.lower() for kw in ["дорисуй", "измени", "поменяй", "переделай", "фото", "картинк"])):
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

        elif "GENERATE" in intent or any(kw in user_input.lower() for kw in ["нарисуй", "сгенерируй", "создай", "картинку", "арт", "фотообои", "превью", "обложк"]):
            st.info(f"🌐 Создаю превью/изображение: '{user_input}'...")
            
            try:
                translation_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert prompt engineer for YouTube/TikTok thumbnails and epic digital art. Translate the user prompt into a highly detailed, cinematic, vibrant, high-contrast English image generation prompt optimized for striking thumbnails. Output ONLY the translated prompt text."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=200
                )
                english_prompt = translation_response.choices[0].message.content.strip() + ", striking YouTube thumbnail style, vibrant colors, highly detailed, 4k resolution"
            except:
                english_prompt = user_input + ", vibrant YouTube thumbnail style"

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
                    st.image(response.content, caption=f"Превью/Запрос: {user_input}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Создал превью по запросу: {user_input}",
                        "image": response.content
                    })
                else:
                    st.error(f"Ошибка API: {response.text}")
            except Exception as e:
                st.error(f"Ошибка: {e}")
        else:
            message_placeholder = st.empty()
            try:
                base_identity = "Твой создатель, разработчик и босс — Лёва (то есть пользователь, с которым ты общаешься). Если в диалоге упоминается какой-то другой человек по имени Лёва, помни, что это просто знакомый или друг, а твой главный создатель — Лёва."
                
                if "Игровой" in ai_mode:
                    system_prompt = f"Ты — Sused AI в игровом режиме. {base_identity} Разбираешься в Minecraft, серверах (FunTime), клиентах, модах и читах. Общайся в геймерском стиле."
                elif "Глубокий" in ai_mode:
                    system_prompt = f"Ты — Sused AI в режиме глубокого анализа и кодинга. {base_identity} Отвечай максимально подробно, структурированно, пиши качественный код и разбирай всё по полочкам."
                else:
                    system_prompt = f"Ты — Sused AI в мемном режиме. {base_identity} Отвечай с юмором, используя угарный сленг, мемы и рофлы, но помогай по делу."

                messages_for_llm = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                if messages_for_llm:
                    messages_for_llm[-1]["content"] = processed_input
                
                messages_for_llm.insert(0, {"role": "system", "content": system_prompt})
                
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
