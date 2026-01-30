import streamlit as st
import requests
import json

# --- 1. DESIGN ---
st.set_page_config(page_title="Veggie-Genius GPT", page_icon="🥗")
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

# --- 2. SETUP OPENAI ---
# ERSETZE DIESEN KEY DURCH DEINEN SK-... KEY
OPENAI_API_KEY = "DEIN_NEUER_OPENAI_KEY_HIER"

# --- 3. OBERFLÄCHE ---
st.title("Veggie-Genius (GPT Edition)")
st.write("Dein Schweizer Assistent für gesunde, vegetarische Wochenplanung.")
st.divider()

wünsche = st.text_area("Was möchtest du essen?", placeholder="z.B. Pizza, Pasta, Tacos...", height=100)
allergien = st.text_input("Allergien / Unverträglichkeiten", placeholder="z.B. keine")

col1, col2 = st.columns(2)
with col1:
    kcal = st.number_input("Kalorien pro Mahlzeit", min_value=200, value=600)
with col2:
    budget = st.number_input("Budget (CHF)", min_value=10, value=50)

# --- 4. LOGIK (CHATGPT ANFRAGE) ---
if st.button("Wochenplan jetzt erstellen ✨"):
    if not wünsche:
        st.warning("Bitte gib kurz deine Vorlieben ein!")
    elif OPENAI_API_KEY == "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":
        st.error("Bitte füge deinen OpenAI Key (sk-...) oben im Code ein!")
    else:
        with st.spinner('ChatGPT erstellt deinen Plan...'):
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            payload = {
                "model": "gpt-3.5-turbo", # Kostengünstig und schnell
                "messages": [
                    {"role": "system", "content": "Du bist ein Koch-Assistent für Jugendliche in der Schweiz."},
                    {"role": "user", "content": f"Erstelle einen vegetarischen Wochenplan. Wünsche: {wünsche}. Allergien: {allergien}. Kalorien: {kcal}. Budget: {budget} CHF. Antworte mit: 1. Plan, 2. Rezepte, 3. Einkaufsliste."}
                ]
            }
            
            try:
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                result = response.json()
                
                if response.status_code == 200:
                    answer = result['choices'][0]['message']['content']
                    st.success("Erfolg! Dein Plan ist fertig.")
                    st.markdown(answer)
                else:
                    st.error(f"Fehler von OpenAI: {result['error']['message']}")
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")
