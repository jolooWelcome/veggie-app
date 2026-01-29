import streamlit as st
import google.generativeai as genai

# --- 1. DESIGN & LAYOUT (Weinrot) ---
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

# --- 2. KI SETUP (DEIN NEUER KEY) ---
API_KEY = "AIzaSyCaeXliVeWdH4KVGex2oSnNUhK3JQSTMsw"
genai.configure(api_key=API_KEY)

# Wir nutzen gemini-1.5-flash (der Standard für neue Keys)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. OBERFLÄCHE (ALLE FELDER) ---
st.title("Veggie-Genius")
st.write("Dein Schweizer Assistent für gesunde, vegetarische Wochenplanung.")
st.divider()

st.subheader("Deine Vorlieben")
wünsche = st.text_area("Was möchtest du gerne essen?", 
                       placeholder="z.B. Pasta, Tacos, viel frisches Gemüse...", height=100)

allergien = st.text_input("Hast du Allergien oder Unverträglichkeiten?", 
                          placeholder="z.B. Nüsse, Laktose oder 'Keine'")

st.divider()
col1, col2 = st.columns(2)
with col1:
    kcal = st.number_input("Kalorienziel pro Mahlzeit", min_value=200, value=600, step=50)
with col2:
    budget = st.number_input("Wochenbudget (in CHF)", min_value=10, value=50, step=5)

mahlzeiten = st.multiselect("Welche Mahlzeiten sollen geplant werden?", 
                            ["Frühstück", "Mittagessen", "Nachtessen"], 
                            default=["Mittagessen", "Nachtessen"])

st.divider()

# --- 4. LOGIK ---
if st.button("Jetzt meinen persönlichen Wochenplan erstellen ✨"):
    if not wünsche:
        st.warning("Bitte gib kurz deine Vorlieben ein!")
    else:
        with st.spinner('KI erstellt deinen Plan...'):
            prompt = f"""
            Erstelle einen detaillierten vegetarischen Wochenplan für Jugendliche in der Schweiz.
            Wünsche: {wünsche}. Allergien: {allergien}. 
            Kalorien: ca. {kcal} kcal pro Mahlzeit. Budget: {budget} CHF.
            Geplante Mahlzeiten: {mahlzeiten}.
            
            ANTWORTE GEGLIEDERT IN:
            1. WOCHENPLAN (Tabelle Montag bis Sonntag)
            2. REZEPTE (Einfach erklärt)
            3. EINKAUFSLISTE (Nach Kategorien: Gemüse, Kühlregal, Vorrat, Sonstiges)
            """
            try:
                response = model.generate_content(prompt)
                if response.text:
                    st.success("Plan erfolgreich erstellt!")
                    st.markdown(response.text)
                else:
                    st.error("Google hat keine Antwort geliefert. Versuche es erneut.")
            except Exception as e:
                st.error(f"Fehler: {e}")
