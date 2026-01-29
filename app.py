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

# --- 2. SETUP (VERSION 1 STABLE) ---
# Wir nutzen die stabilste Konfiguration für Streamlit Cloud
API_KEY = "AIzaSyDp-jxQJZhK54rT2fvPduTAIZzKpHYb2Rc"
genai.configure(api_key=API_KEY)

# Wir nutzen gemini-1.5-flash ohne Zusätze - das ist der aktuelle Cloud-Standard
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. OBERFLÄCHE (ALLES WIEDER DA) ---
st.title("🥗 Veggie-Genius")
st.write("Dein persönlicher Assistent für gesunde, vegetarische Wochenplanung.")
st.divider()

st.subheader("Deine Details")
wünsche = st.text_area("Was isst du gerne?", 
                       placeholder="z.B. Pasta, Tacos, viel frisches Gemüse...", height=100)

allergien = st.text_input("Allergien oder Unverträglichkeiten?", 
                          placeholder="z.B. Nüsse, Laktose oder 'Keine'")

col1, col2 = st.columns(2)
with col1:
    kcal = st.number_input("Kalorienziel pro Mahlzeit", min_value=200, value=600)
with col2:
    budget = st.number_input("Wochenbudget (CHF)", min_value=10, value=50)

mahlzeiten = st.multiselect("Welche Mahlzeiten?", 
                            ["Frühstück", "Mittagessen", "Nachtessen"], 
                            default=["Mittagessen", "Nachtessen"])

st.divider()

# --- 4. GENERIERUNG ---
if st.button("Jetzt meinen persönlichen Wochenplan erstellen ✨"):
    if not wünsche:
        st.warning("Bitte gib kurz deine Vorlieben ein!")
    else:
        with st.spinner('KI erstellt deinen Plan...'):
            prompt = f"""
            Erstelle einen vegetarischen Wochenplan für Jugendliche.
            Wünsche: {wünsche}. Allergien: {allergien}. 
            Max. {kcal} kcal pro Mahlzeit. Budget: {budget} CHF.
            Mahlzeiten: {mahlzeiten}.
            Antworte bitte mit: 1. Wochenplan, 2. Rezepte, 3. Einkaufsliste (nach Kategorien).
            """
            try:
                # Wir rufen die KI ohne Beta-Zusätze auf
                response = model.generate_content(prompt)
                if response.text:
                    st.success("Plan fertig!")
                    st.markdown(response.text)
                else:
                    st.error("Die KI hat keine Antwort geliefert. Bitte versuche es erneut.")
            except Exception as e:
                st.error(f"Hinweis: {e}")
                st.info("Falls dieser Fehler bleibt: Erstelle bitte im Google AI Studio einen NEUEN Key. Manchmal werden Keys bei der ersten Nutzung in neuen Umgebungen blockiert.")
