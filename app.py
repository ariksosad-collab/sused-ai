import streamlit as st
import os
from openai import OpenAI
import base64
import requests

# API Keys
STABILITY_API_KEY = "sk-DFEaOMcYxvyso7NorFtGc6zaht2GGhOjlWlRZ7sDeewKJH9C"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

STABILITY_INPAINT_URL = "https://api.stability.ai/v2beta/stable-image/edit/inpainting"

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖")

st.markdown("<style>.stApp {background-color: #131314; color: #e3e3e3;}</style>", unsafe_allow_html=True)

st.title("🤖 Sused AI Pro Max")

def perform_inpainting(original_image_bytes, prompt_text):
    with st.chat_message("assistant"):
        st.info(f"🎨 Рисую: '{prompt_text}'...")
        
        payload = {
            "prompt": prompt_text,
            "mode": "replace",
            "output_format": "jpeg",
            "strength": 0.8
        }
        
        files = {'image': ('input.jpg', original_image_bytes, 'image/jpeg')}
        
        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "image/*"
        }

        try:
            with st.spinner("Работает нейрохудожник..."):
                response = requests.post(STABILITY_INPAINT_URL, headers=headers, files=files, data=payload)
            
            if response.status_code == 200:
                st.success("Готово!")
                st.image(response.content, caption=f"Результат: {prompt_text}")
            else:
                st.error(f"Ошибка API: {response.text}")
        except Exception as e:
             st.error(f"Ошибка: {e}")

uploaded_file = st.file_uploader("Загрузи фото", type=['png', 'jpg', 'jpeg'])
user_input = st.chat_input("Напиши /inpainting и что нарисовать")

if user_input and user_input.startswith("/inpainting "):
    if uploaded_file:
        perform_inpainting(uploaded_file.getvalue(), user_input.replace("/inpainting ", "", 1))
    else:
        st.warning("Сначала загрузи картинку!")
