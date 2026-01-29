import streamlit as st
import google.generativeai as genai

# --- 1. DESIGN & LOOK ---
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

# --- 2. SETUP (STABILE VERSION) ---
# Dein Key bleibt gleich
genai.configure(api_key="AIzaSyDp-jxQJZhK54rT2fvPduTAIZzKpHYb2Rc")

# WICHTIG: Wir nutzen 'gemini-pro', das ist die stabilste Einstellung für Cloud-Apps
model = genai.GenerativeModel('gemini-pro')

# --- 3. OBERFLÄCHE ---
st.title("Veggie-Genius")
st.write("Dein KI-Assistent für vegetarische Wochenpläne, Rezepte und Einkaufslisten.")
st.divider()

wünsche = st.text_area("Was möchtest du diese Woche gerne essen?", 
                       placeholder="z.B. Pasta-Gerichte, Tacos, viel frisches Gemüse...", height=100)

allergien = st.text_input("Hast du Allergien oder Unverträglichkeiten?", 
                          placeholder="z.B. Nüsse, Laktose... (oder leer lassen)")

st.divider()
col1, col2 = st.columns(2)
with col1:
    kcal = st.number_input("Kalorienziel pro Mahlzeit:", min_value=200, value=600, step=50)
with col2:
    budget = st.number_input("Max. Budget für die Woche (CHF):", min_value=10, value=60, step=5)

mahlzeiten = st.multiselect("Welche Mahlzeiten sollen geplant werden?", 
                            ["Frühstück", "Mittagessen", "Nachtessen"], 
                            default=["Mittagessen", "Nachtessen"])

# --- 4. GENERIERUNG ---
if st.button("Jetzt detaillierten Wochenplan erstellen ✨"):
    if not wünsche:
        st.warning("Bitte gib kurz deine Essenswünsche ein!")
    else:
        with st.spinner('KI erstellt deinen Plan...'):
            prompt = f"""
            Erstelle einen detaillierten vegetarischen Wochenplan für Jugendliche.
            - Wünsche: {wünsche}
            - Allergien: {allergien}
            - Kalorien pro Mahlzeit: ca. {kcal} kcal
            - Gesamtbudget für den Einkauf: {budget} CHF (Schweizer Preise)
            - Mahlzeiten: {mahlzeiten}
            
            Struktur der Antwort:
            1. WOCHENPLAN: Übersicht Montag bis Sonntag.
            2. REZEPTE: Einfache Kochanleitungen.
            3. EINKAUFSLISTE: Sortiert nach Kategorien.
            """
            try:
                response = model.generate_content(prompt)
                st.success("Erfolg! Dein Plan ist bereit.")
                st.markdown(response.text)
            except Exception as e:
                # Zeigt uns den exakten Fehler an, falls Google blockiert
                st.error(f"Google API Fehler: {e}")
