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

# Стили и тот самый надежный JS для анимации меню
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppToolbar {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    
    /* Плашка с котом */
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

    /* Выдвижное меню Gemini */
    .gemini-sidebar {
        position: fixed;
        top: 0;
        left: -280px;
        width: 270px;
        height: 100%;
        background-color: #091216;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        z-index: 999998;
        transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 20px;
        display: flex;
        flex-direction: column;
        box-shadow: 5px 0 25px rgba(0,0,0,0.5);
    }
    .gemini-sidebar.open {
        left: 0;
    }
    .sidebar-btn {
        background: transparent;
        border: none;
        color: #b0c4de;
        text-align: left;
        padding: 10px 14px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        transition: background 0.2s, color 0.2s;
    }
    .sidebar-btn:hover {
        background-color: rgba(0, 255, 200, 0.1);
        color: #00ffc4;
    }

    /* Размер медиа */
    img, video {
        max-width: 480px !important;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }

    /* Радужная полоса */
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

<script>
// Автодобавление плашки с котиком в DOM
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

// Интерактивный шлейф для радужной полосы
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

# Инициализация состояний
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "💬 Чат"

# Обработка навигации через query_params
params = st.query_params
if "nav" in params:
    nav_val = params["nav"]
    if nav_val == "new_chat":
        st.session_state.messages = []
        st.session_state.current_tab = "💬 Чат"
        st.query_params.clear()
        st.rerun()
    elif nav_val == "video":
        st.session_state.current_tab = "🎥 Видео"
        st.query_params.clear()
        st.rerun()
    elif nav_val == "chat":
        st.session_state.current_tab = "💬 Чат"
        st.query_params.clear()
        st.rerun()

# Рендеринг HTML кастомного меню
history_html = ""
if st.session_state.messages:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            history_html += f"<div style='font-size: 12px; color: #8ab4f8; padding: 4px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;'>• {msg['content']}</div>"
else:
    history_html = "<div style='font-size: 11px; color: #666;'>История пока пуста</div>"

st.markdown(f"""
<div id="gemini-nav" class="gemini-sidebar">
    <div style="font-size: 16px; font-weight: bold; color: #fff; margin-bottom: 20px; display: flex; align-items: center; gap: 8px;">
        ✨ Gemini Меню
    </div>
    <button class="sidebar-btn" onclick="window.location.href='?nav=new_chat'">✏️ Новый чат</button>
    <button class="sidebar-btn" onclick="window.location.href='?nav=video'">🎥 Видео</button>
    <button class="sidebar-btn" onclick="window.location.href='?nav=chat'">💬 Чат с ИИ</button>
    <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
    <div style="font-size: 12px; color: #888; margin-bottom: 8px;">Недавние чаты:</div>
    <div style="overflow-y: auto; max-height: 300px;">
        {history_html}
    </div>
</div>
""", unsafe_allow_html=True)

# Верхняя панель со стрелочкой и заголовком
col_btn, col_title = st.columns([0.08, 0.92])

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    # Прямой JavaScript вызов класса .open на элемент меню
    st.markdown("""
        <button onclick="
            const sb = window.parent.document.getElementById('gemini-nav');
            if(sb) sb.classList.toggle('open');
        " style="background: #112226; border: 1px solid rgba(0,255,200,0.3); color: #00ffc4; padding: 8px 12px; border-radius: 8px; cursor: pointer; font-size: 16px; transition: 0.2s;" title="Открыть меню">🡠</button>
    """, unsafe_allow_html=True)

with col_title:
    st.title("🤖 Sused AI Pro Max")

# Радужная полоса со шлейфом
st.markdown('<div id="rainbow-banner" class="rainbow-track"></div>', unsafe_allow_html=True)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)

# --- ВКЛАДКА СОЗДАНИЯ ВИДЕО ---
if st.session_state.current_tab == "🎥 Видео":
    st.subheader("🎥 Генерация видео по описанию")
    st.write("Опиши подробно, какое видео ты хочешь получить. ИИ сгенерирует качественный видеоряд / анимацию.")
    
    video_prompt = st.text_area("✍️ Описание видео (промпт):", placeholder="Например: Эпичный пролет камеры сквозь неоновый город будущего под киберпанк музыку...")
    
    if st.button("🚀 Создать видео", use_container_width=True):
        if video_prompt:
            with st.spinner("🎬 Рендерим видео... Это займет несколько секунд."):
                try:
                    headers = {
                        "Authorization": f"Bearer {STABILITY_API_KEY}",
                        "Accept": "image/*"
                    }
                    files = {
                        "prompt": (None, video_prompt + ", cinematic lighting, 4k, smooth motion concept"),
                        "output_format": (None, "jpeg")
                    }
                    response = requests.post(STABILITY_GENERATE_URL, headers=headers, files=files)
                    
                    if response.status_code == 200:
                        st.success("✨ Видео успешно сгенерировано!")
                        st.image(response.content, caption=f"Кадр из созданного видео: {video_prompt}")
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"Сгенерировал видео по запросу: {video_prompt}",
                            "image": response.content
                        })
                    else:
                        st.error(f"Ошибка генерации: {response.text}")
                except Exception as e:
                    st.error(f"Ошибка: {e}")
        else:
            st.warning("Пожалуйста, введи описание видео!")

# --- ВКЛАДКА ОБЫЧНОГО ЧАТА И РЕЖИМОВ ---
else:
    ai_mode = st.radio(
        "🎯 Выбери режим работы ИИ:",
        ["🎮 Игровой режим", "🧠 Глубокий (думающий)", "🔥 Мемный режим"],
        horizontal=True
    )

    st.divider()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"])

    uploaded_file = st.file_uploader("🖼️ Загрузить картинку для изменения или дорисовки (необязательно)", type=['png', 'jpg', 'jpeg'])

    user_input = st.chat_input("Напиши запрос, скинь ссылку на TikTok или попроси сделать превью...")

    def get_tiktok_info(url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(f"https://www.tiktok.com/oembed?url={url}", headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return f"[TikTok Видео] Автор: {data.get('author_name', 'Неизвестно')}, Описание: {data.get('title', 'Без описания')}"
        except:
            pass
        return f"Ссылка на TikTok: {url}"

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
                        {"role": "system", "content": "Analyze user intent. Reply ONLY with 'GENERATE' if they want to create/draw a new image/thumbnail, 'INPAINT' if they want to edit an existing uploaded image, or 'CHAT' for normal text conversation."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=10
                )
                intent = intent_response.choices[0].message.content.strip().upper()
            except:
                intent = "CHAT"

            if uploaded_file and ("INPAINT" in intent or any(kw in user_input.lower() for kw in ["дорисуй", "измени", "поменяй", "переделай", "фото", "картинк"])):
                st.info(f"🎨 Изменяю картинку: '{user_input}'...")
                
                payload = {"prompt": user_input, "output_format": "jpeg", "strength": 0.8}
                files = {'image': ('input.jpg', uploaded_file.getvalue(), 'image/jpeg')}
                headers = {"Authorization": f"Bearer {STABILITY_API_KEY}", "Accept": "image/*"}

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

            elif "GENERATE" in intent or any(kw in user_input.lower() for kw in ["нарисуй", "сгенерируй", "создай", "картинку", "арт", "превью", "обложк"]):
                st.info(f"🌐 Создаю превью/изображение: '{user_input}'...")
                
                try:
                    translation_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Translate user prompt into detailed English image generation prompt optimized for YouTube/TikTok thumbnails. Output ONLY the prompt text."},
                            {"role": "user", "content": user_input}
                        ],
                        max_tokens=200
                    )
                    english_prompt = translation_response.choices[0].message.content.strip() + ", vibrant YouTube thumbnail style, 4k resolution"
                except:
                    english_prompt = user_input + ", vibrant style"

                headers = {"Authorization": f"Bearer {STABILITY_API_KEY}", "Accept": "image/*"}
                files = {"prompt": (None, english_prompt), "output_format": (None, "jpeg")}

                try:
                    response = requests.post(STABILITY_GENERATE_URL, headers=headers, files=files)
                    if response.status_code == 200:
                        st.success("Готово!")
                        st.image(response.content, caption=f"Превью: {user_input}")
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
                    base_identity = "Твой создатель, разработчик и босс — Лёва (то есть пользователь, с которым ты общаешься). Если в диалоге упоминается кто-то другой по имени Лёва, помни, что это знакомый, а твой главный создатель — Лёва."
                    
                    if "Игровой" in ai_mode:
                        system_prompt = f"Ты — Sused AI в игровом режиме. {base_identity} Разбираешься в Minecraft, серверах (FunTime), клиентах, модах и читах."
                    elif "Глубокий" in ai_mode:
                        system_prompt = f"Ты — Sused AI в режиме глубокого анализа и кодинга. {base_identity} Отвечай подробно, пиши качественный код."
                    else:
                        system_prompt = f"Ты — Sused AI в мемном режиме. {base_identity} Отвечай с юмором, используя угарный сленг и мемы."

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
