import streamlit as st
import os
from openai import OpenAI
import requests
import re
import urllib.parse

# Настройка ключа Groq для чата (текста)
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.environ.get("GROQ_API_KEY")

st.set_page_config(page_title="Sused AI Pro Max", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# Стили: фиксируем сайдбар, чтобы он всегда был открыт, и убираем лишнее
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppToolbar {display: none !important;}
    
    /* Принудительно показываем и фиксируем сайдбар на экране */
    [data-testid="stSidebar"] {
        background-color: #091216 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        min-width: 260px !important;
        max-width: 260px !important;
        transform: none !important;
        visibility: visible !important;
    }
    
    /* Убираем кнопку сворачивания */
    [data-testid="collapsedControl"] {
        display: none !important;
    }

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
const addCatCover = setInterval(() => {
