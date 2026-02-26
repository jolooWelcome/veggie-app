import streamlit as st
from openai import OpenAI

# --- 1. DESIGN-FIX (SCHRIFTFARBE ERZWINGEN) ---
st.set_page_config(page_title="VeggieVibe", page_icon="🥦")

st.markdown("""
    <style>
    /* Hintergrund hellgrau */
    .stApp { background-color: #f8f9fa; }
    /* Alle Texte in der App dunkelgrau/schwarz machen */
    .stApp p, .stApp div, .stApp span, .stApp li {
        color: #31333F !important;
    }
    h1, h2, h3 { color: #722F37 !important; }
    .stButton>button { background-color: #722F37 !important; color: white !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SEITENLEISTE ---
with st.sidebar:
    st.title("Sicherheit")
    user_api_key = st.text_input("OpenAI API Key hier einfügen:", type="password")
    st.info("Dein Key wird nur für diese Sitzung genutzt.")

# --- 3. OBERFLÄCHE ---
st.title("🥦 VeggieVibe")
st.subheader("Dein smarter KI-Wochenplaner")

wünsche = st.text_area("Was möchtest du essen?", placeholder="z.B. Pasta, Pizza...")
col1, col2 = st.columns(2)
with col1:
    kalorien = st.number_input("Kalorienziel:", value=2000)
with col2:
    budget = st.number_input("Budget (CHF):", value=50)

# --- 4. START ---
if st.button("🚀 Plan jetzt erstellen"):
    if not user_api_key:
        st.error("⚠️ Bitte gib zuerst deinen API-Key in der linken Seitenleiste ein!")
    elif not wünsche:
        st.warning("⚠️ Was möchtest du essen?")
    else:
        with st.spinner('KI kocht gerade...'):
            try:
                client = OpenAI(api_key=user_api_key)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein Veggie-Koch-Profi für Jugendliche. Antworte immer auf Deutsch."},
                        {"role": "user", "content": f"Erstelle einen vegetarischen Plan für: {wünsche}. Budget: {budget} CHF, Kalorien: {kalorien}."}
                    ]
                )
                
                # Hier wird das Ergebnis angezeigt
                st.success("Fertig!")
                st.markdown("---")
                # Wir nutzen Markdown, um sicherzugehen, dass es formatiert ist
                st.markdown(f"### Dein Plan:\n{response.choices[0].message.content}")
                
            except Exception as e:
                st.error(f"Fehler: {e}")
