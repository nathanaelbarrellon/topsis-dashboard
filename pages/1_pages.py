
import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Coming Soon", page_icon="🚧", layout="centered")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .centered {
        text-align: center;
        padding-top: 80px;
    }
    .emoji {
        font-size: 80px;
        animation: bounce 1.2s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    </style>
""", unsafe_allow_html=True)

# --- CONTENU ---
st.markdown("<div class='centered'>", unsafe_allow_html=True)
st.markdown("<div class='emoji'>🚧</div>", unsafe_allow_html=True)
st.title("Page Under Construction")

progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)

st.success("Coming soon 🚀")
st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Streamlit Prototype - Nathanaël Barrellon/Arthur Daveau ✈️")
