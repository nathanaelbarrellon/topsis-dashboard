import streamlit as st

# --- Configuration de la page ---
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# --- Titre principal ---
st.title("✈️ Dashboard")
st.write("Bienvenue sur le tableau de bord du projet !")

st.markdown("---")

# --- Section Inputs ---
st.header("Inputs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Vehicle Classes")
    vehicle = st.selectbox("Choisir le véhicule :", ["Class 1", "Class 2", "Class 3", "Class 4"])

with col2:
    st.subheader("Clean-sheet")
    clean_sheet = st.checkbox("Oui, design from scratch")

with col3:
    st.subheader("Electrification")
    electrif = st.selectbox("Niveau :", ["None", "Hybrid", "Full Electric"])

with col4:
    st.subheader("Orientation technique")
    tech_orient = st.radio("Choix :", ["Conservative", "Aggressive", "Innovative"])

st.markdown("---")

# --- Section Mission specifications ---
st.subheader("Mission Specifications")
col5, col6, col7 = st.columns(3)

with col5:
    range_km = st.slider("Range (km)", 100, 2000, 500)
with col6:
    speed = st.slider("Cruise speed (km/h)", 200, 900, 600)
with col7:
    payload = st.number_input("Payload (kg)", 0, 20000, 2000)

st.markdown("---")

# --- Timeframe ---
st.subheader("Timeframe")
timeframe = st.select_slider("Horizon temporel (années)", options=[1, 2, 3, 4, 5], value=3)

st.markdown("---")

# --- Résultats / Critères ---
st.header("Outputs / Criteria")

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.subheader("A/C Performance")
    st.metric("Cruise Efficiency", "82%", delta="+2%")
    st.button("Afficher les plots", key="ac_perf")

with col_b:
    st.subheader("Operation / Fleet")
    st.metric("Utilization Rate", "74%", delta="-3%")
    st.button("Afficher les plots", key="fleet")

with col_c:
    st.subheader("Environment 🌱")
    st.metric("CO₂ Reduction", "-32%", delta="-5%")
    st.button("Afficher les plots", key="env")

with col_d:
    st.subheader("Cost 💰")
    st.metric("Total Cost", "$2.1M", delta="-8%")
    st.button("Afficher les détails", key="cost")

st.markdown("---")

# --- Footer ---
st.caption("Prototype Streamlit - Nathanaël Barrellon ✈️")
