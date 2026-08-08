# The user provided the key, I will incorporate it into the app code example.
# I will structure the response to provide the updated app.py code.

app_code = """
import streamlit as st
import os
from openai import OpenAI
import base64
import requests
import io

# API Keys
# Use the provided Stability API Key directly for this example.
# In a real production app, always use st.secrets.
STABILITY_API_KEY = "sk-DFEaOMcYxvyso7NorFtGc6zaht2GGhOjlWlRZ7sDeewKJH9C"

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.environ.get("GROQ_API_KEY")

# URL for Stability AI Inpainting API
STABILITY_INPAINT_URL = "https://api.stability.ai/v2beta/stable-image/edit/inpainting"

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖")

st.markdown("""<style>.stApp {background-color: #131314; color: #e3e3e3;}</style>""", unsafe_allow_html=True)

st.title("🤖 Sused AI Pro Max")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)

def perform_inpainting(original_image_bytes, prompt_text):
    with st.chat_message("assistant"):
        st.info(f"🎨 Рисую: '{prompt_text}'...")
        
        payload = {
            "prompt": prompt_text,
            "mode": "replace",
            "output_format": "jpeg",
            "strength": 0.8
        }
        
        files = {
            'image': ('input.jpg', original_image_bytes, 'image/jpeg')
        }
        
        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "image/*"
        }

        try:
            with st.spinner("Работает нейрохудожник..."):
                response = requests.post(
                    STABILITY_INPAINT_URL,
                    headers=headers,
                    files=files,
                    data=payload,
                )
            
            if response.status_code == 200:
                new_image_bytes = response.content
                st.success("Готово!")
                st.image(new_image_bytes, caption=f"Результат: {prompt_text}")
            else:
                error_data = response.json()
                st.error(f"❌ Ошибка Stability AI: {error_data}")

        except Exception as e:
             st.error(f"❌ Ошибка: {e}")

# --- Main App ---
if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("Загрузи фото", type=['png', 'jpg', 'jpeg'])
user_input = st.chat_input("Напиши /inpainting и что нарисовать")

if user_input and user_input.startswith("/inpainting "):
    if uploaded_file:
        prompt = user_input.replace("/inpainting ", "", 1)
        bytes_data = uploaded_file.getvalue()
        perform_inpainting(bytes_data, prompt)
    else:
        st.warning("Сначала загрузи картинку!")
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)
