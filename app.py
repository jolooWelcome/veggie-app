import streamlit as st
import google.generativeai as genai

# --- 1. DESIGN (Weinrot & Sauber) ---
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

# --- 2. KI SETUP ---
# Dein funktionierender Key
API_KEY = "AIzaSyDp-jxQJZhK54rT2fvPduTAIZzKpHYb2Rc"
genai.configure(api_key=API_KEY)

# Wir nutzen gemini-1.5-flash ohne "beta" im Namen für maximale Stabilität
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. DIE URSPRÜNGLICHEN INHALTE ---
st.title("Veggie-Genius")
st.write("Dein Schweizer Assistent für gesunde, vegetarische Wochenplanung.")
st.divider()

st.subheader("Deine Vorlieben")
wünsche = st.text_area("Was möchtest du essen?", 
                       placeholder="z.B. Pizza, Pasta, Tacos, viel frisches Gemüse...", height=100)

allergien = st.text_input("Allergien / Unverträglichkeiten", 
                          placeholder="z.B. keine")

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
if st.button("Wochenplan erstellen ✨"):
    if not wünsche:
        st.warning("Bitte gib kurz ein, was du gerne essen möchtest!")
    else:
        with st.spinner('KI erstellt deinen Plan...'):
            prompt = f"""
            Erstelle einen vegetarischen Wochenplan für Jugendliche in der Schweiz.
            Wünsche: {wünsche}. Allergien: {allergien}. 
            Kalorien: ca. {kcal} kcal pro Mahlzeit. Budget: {budget} CHF.
            Mahlzeiten: {mahlzeiten}.
            
            ANTWORTE GEGLIEDERT IN:
            1. WOCHENPLAN (Tabelle Mo-So)
            2. REZEPTE (Kurz und einfach)
            3. EINKAUFSLISTE (Nach Kategorien sortiert)
            """
            try:
                # Hier nutzen wir den stabilen Aufruf
                response = model.generate_content(prompt)
                st.success("Plan fertig!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"KI-Fehler: {e}")
                st.info("Sollte der Fehler '404' bleiben, erstelle bitte kurz einen neuen Key im Google AI Studio.")
