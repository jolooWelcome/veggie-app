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
    .stButton>button:hover { background-color: #a00028; border: none; }
    label { font-weight: bold !important; font-size: 1.1rem !important; color: #333 !important; }
    /* Eingabefelder Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #fdfdfd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SETUP OPENAI ---
# Dein neuer Key ist hier integriert
OPENAI_API_KEY = "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"

# --- 3. OBERFLÄCHE ---
st.title("🥗 Veggie-Genius")
st.write("Dein Schweizer Assistent für gesunde, vegetarische Wochenplanung.")
st.divider()

st.subheader("Deine Vorlieben")
wünsche = st.text_area("Was möchtest du essen?", 
                       placeholder="z.B. Pizza, Pasta, Tofu...", height=100)

allergien = st.text_input("Allergien / Unverträglichkeiten", 
                          placeholder="z.B. keine")

col1, col2 = st.columns(2)
with col1:
    kcal = st.number_input("Kalorien pro Mahlzeit", min_value=200, value=600, step=50)
with col2:
    budget = st.number_input("Budget (CHF)", min_value=10, value=50, step=5)

mahlzeiten = st.multiselect("Welche Mahlzeiten?", 
                            ["Frühstück", "Mittagessen", "Nachtessen"], 
                            default=["Mittagessen"])

st.divider()

# --- 4. LOGIK (CHATGPT ANFRAGE) ---
if st.button("Wochenplan erstellen ✨"):
    if not wünsche:
        st.warning("Bitte gib kurz deine Vorlieben ein!")
    else:
        with st.spinner('ChatGPT erstellt deinen Plan...'):
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            # Wir nutzen GPT-4o-mini: Extrem schnell, günstig und zuverlässig
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Du bist ein hilfreicher Koch-Assistent für Jugendliche in der Schweiz. Erstelle vegetarische Pläne mit Schweizer Zutaten."},
                    {"role": "user", "content": f"Erstelle einen vegetarischen Wochenplan. Wünsche: {wünsche}. Allergien: {allergien}. Kalorien: {kcal} pro Mahlzeit. Budget: {budget} CHF. Antworte mit: 1. Plan (Tabelle Mo-So), 2. Rezepte (einfach), 3. Einkaufsliste (sortiert)."}
                ],
                "temperature": 0.7
            }
            
            try:
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
                result = response.json()
                
                if response.status_code == 200:
                    answer = result['choices'][0]['message']['content']
                    st.success("Erfolg! Dein Plan ist fertig.")
                    st.markdown(answer)
                else:
                    error_msg = result.get('error', {}).get('message', 'Unbekannter Fehler')
                    st.error(f"OpenAI Fehler: {error_msg}")
                    if "insufficient_quota" in error_msg:
                        st.info("Hinweis: Du musst bei OpenAI ein kleines Guthaben (z.B. 5 CHF) aufladen, um den Key zu nutzen.")
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")
