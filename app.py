import streamlit as st
import requests
import json

# --- 1. DESIGN & LOOK (Weinrot) ---
st.set_page_config(page_title="Veggie-Genius", page_icon="🥗")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { color: #800020 !important; }
    .stButton>button { 
        background-color: #800020; color: white !important; 
        border-radius: 20px; border: none; height: 3.5em; width: 100%; font-weight: bold;
    }
    .stButton>button:hover { background-color: #a00028; }
    label { font-weight: bold !important; font-size: 1.1rem !important; color: #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SETUP (NEUER KEY & DIREKTE WEB-SCHNITTSTELLE) ---
API_KEY = "AIzaSyCaeXliVeWdH4KVGex2oSnNUhK3JQSTMsw"
# Wir nutzen die REST-Schnittstelle, um die "404 Library" Fehler zu umgehen
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# --- 3. OBERFLÄCHE (URSPIEGLICHE INHALTE) ---
st.title("Veggie-Genius")
st.write("Dein Schweizer Assistent für gesunde, vegetarische Wochenplanung.")
st.divider()

st.subheader("Deine Vorlieben")
wünsche = st.text_area("Was möchtest du essen?", 
                       placeholder="z.B. Pizza, Pasta, Tacos...", height=100)

allergien = st.text_input("Allergien / Unverträglichkeiten", placeholder="z.B. keine")

st.divider()
col1, col2 = st.columns(2)
with col1:
    kcal = st.number_input("Kalorien pro Mahlzeit", min_value=200, value=600)
with col2:
    budget = st.number_input("Budget (CHF)", min_value=10, value=50)

mahlzeiten = st.multiselect("Welche Mahlzeiten?", 
                            ["Frühstück", "Mittagessen", "Nachtessen"], 
                            default=["Mittagessen", "Nachtessen"])

st.divider()

# --- 4. LOGIK ---
if st.button("Wochenplan jetzt erstellen ✨"):
    if not wünsche:
        st.warning("Bitte gib kurz deine Vorlieben ein!")
    else:
        with st.spinner('KI erstellt deinen Plan via Direktleitung...'):
            payload = {
                "contents": [{
                    "parts": [{"text": f"Erstelle einen vegetarischen Wochenplan für Jugendliche in der Schweiz. Wünsche: {wünsche}. Allergien: {allergien}. Kalorien: {kcal}. Budget: {budget} CHF. Mahlzeiten: {mahlzeiten}. Antworte mit: 1. Plan, 2. Rezepte, 3. Einkaufsliste."}]
                }]
            }
            headers = {'Content-Type': 'application/json'}
            
            try:
                # Wir schicken die Anfrage direkt übers Web (umgeht lokale 404 Fehler)
                response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("Erfolg! Dein Plan ist fertig.")
                    st.markdown(answer)
                else:
                    st.error(f"Google meldet Fehler {response.status_code}. Details: {response.text}")
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")
