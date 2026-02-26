import streamlit as st
from openai import OpenAI

# --- 1. DESIGN-EINSTELLUNGEN ---
st.set_page_config(page_title="VeggieVibe", page_icon="🥦")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stApp p, .stApp div, .stApp span, .stApp li { color: #31333F !important; }
    h1, h2, h3 { color: #722F37 !important; }
    .stButton>button { background-color: #722F37 !important; color: white !important; border-radius: 10px; border: none; height: 3em; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DER AUTOMATISCHE SCHLÜSSEL ---
# Die App holt sich den Key jetzt selbstständig aus dem Tresor
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("⚠️ Schlüssel im Tresor nicht gefunden! Bitte Schritt 2 ausführen.")

# --- 3. OBERFLÄCHE ---
st.title("🥦 VeggieVibe")
st.subheader("Dein KI-Wochenplaner (Pro-Version)")

wünsche = st.text_area("Was möchtest du essen?", placeholder="z.B. Pasta, Pizza...")
col1, col2 = st.columns(2)
with col1:
    kalorien = st.number_input("Kalorienziel pro Tag:", value=2000)
with col2:
    budget = st.number_input("Budget (CHF):", value=50)

reste = st.text_area("Reste im Kühlschrank?", placeholder="z.B. 2 Eier, halbe Gurke")

# --- 4. START ---
if st.button("🚀 Plan jetzt erstellen"):
    if not wünsche and not reste:
        st.warning("⚠️ Bitte gib deine Wünsche ein!")
    else:
        with st.spinner('KI erstellt deinen Plan...'):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein Veggie-Koch-Profi für Jugendliche. Antworte immer auf Deutsch."},
                        {"role": "user", "content": f"Plan für: {wünsche}. Reste: {reste}. Budget: {budget} CHF, Kalorien: {kalorien}."}
                    ]
                )
                st.success("Dein Plan ist bereit!")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Fehler: {e}")
