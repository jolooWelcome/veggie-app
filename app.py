import streamlit as st
from openai import OpenAI

# --- 1. DESIGN & HARMONISIERUNG (CSS) ---
st.set_page_config(page_title="Sophis Veggie APP", page_icon="🥑", layout="centered")

st.markdown("""
    <style>
    /* Hintergrund */
    .stApp { background-color: #f4f4f4; }
    
    /* UNIFORME ÜBERSCHRIFTEN (Labels) */
    .stApp label p, .stApp h1, .stApp h2, .stApp h3, p { 
        color: #31333F !important; 
        font-family: 'Inter', sans-serif !important;
        font-size: 1.05rem !important; /* Einheitliche Größe für alle Beschriftungen */
        font-weight: 600 !important;
        margin-bottom: 5px !important;
    }
    
    h1 { font-size: 2.2rem !important; color: #722F37 !important; margin-bottom: 20px !important; }

    /* UNIFORME SCHWARZE FELDER (Inputs) */
    /* Wir zwingen TextAreas, NumberInputs und Selectboxen auf das Design von 'Kalorienziel' */
    .stTextArea textarea, .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
        background-color: #31333F !important;
        color: white !important;
        border: 2px solid #722F37 !important;
        border-radius: 8px !important;
        font-size: 1rem !important; /* Exakt wie im Kalorienziel-Feld */
        font-family: 'Inter', sans-serif !important;
        padding: 10px !important;
    }

    /* FIX FÜR DEN TEXT IN DER AUSWAHLBOX (Mahlzeiten anpassen) */
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: white !important;
        font-size: 1rem !important;
    }

    /* Radio-Buttons (Plan-Modus) ebenfalls anpassen */
    div[role="radiogroup"] {
        background-color: #31333F;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #722F37;
        color: white !important;
    }
    div[role="radiogroup"] label p { color: white !important; font-size: 0.95rem !important; }

    /* DER GELBE ZAUBER-BUTTON */
    .stButton>button { 
        background-color: #FFD700 !important; 
        color: #31333F !important; 
        border-radius: 12px; 
        border: 2px solid #722F37; 
        height: 3.5em; 
        width: 100%; 
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    
    /* Kompakte Karten unten */
    .small-food-card {
        background: white;
        padding: 5px 10px;
        border-radius: 6px;
        border-left: 3px solid #722F37;
        margin-bottom: 3px;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DEINE ERLAUBTE LISTE ---
if 'allowed_foods' not in st.session_state:
    st.session_state.allowed_foods = [
        "Weissbrot, Toastbrot (Frisch)", "Reis, Mais, Hirse", "Nudeln (ohne Ei)", 
        "Hafer/Haferflocken", "Wasser", "Tee", "Apfelsaft", "Salz, Olivenöl", 
        "Frische Kräuter", "Frischkäse", "Hüttenkäse", "Butter/Sahne", 
        "Karotte", "Zuccini", "Brokkoli", "Kartoffeln/Süsskartoffeln", 
        "Gurken", "Kopfsalat", "Eisbergsalat", "Blumenkohl", "Sellerie", 
        "Erbsen", "Äpfel/ Birnen (geschält)", "Melone, Trauben (weiss)", "Mango/Heidelbeere"
    ]

# --- 3. OBERFLÄCHE ---
st.title("🥑 Sophis Veggie APP")

with st.container():
    wünsche = st.text_area("Was möchtest du essen?", placeholder="z.B. Nudeln...")
    kuehlschrank = st.text_area("Habe ich noch im Kühlschrank:", placeholder="z.B. Zuccini...")
    
    col1, col2 = st.columns(2)
    with col1:
        mahlzeit_typ = st.selectbox("Mahlzeiten anpassen:", ["Morgenessen", "Mittagessen", "Nachtessen"])
        plan_art = st.radio("Plan-Modus:", ["Einmalige Mahlzeit", "Wochenplan (7 Tage)"])
    
    with col2:
        kalorien = st.number_input("Kalorienziel:", value=600)
        budget = st.number_input("Budget (CHF):", value=20)

# --- 4. KI-LOGIK (DER WITZIGE VEGGIE-GUARD) ---
if st.button("✨ KI Menü zaubern"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        prompt = f"""
        Du bist Sophis persönlicher KI-Buddy (sie ist 16, sei locker & witzig 🤙). 
        
        STRENGE REGELN:
        1. Checke 'Wünsche' und 'Kühlschrank'. Wenn dort Dinge stehen, die NICHT auf dieser Liste sind: {', '.join(st.session_state.allowed_foods)}, weise sie direkt am Anfang witzig darauf hin!
        2. Wenn Fleisch/Fisch erwähnt wird -> Sofortiger Veto-Hinweis!
        3. Erstelle MINDESTENS 3 verschiedene Menü-Vorschläge ({plan_art}) für {mahlzeit_typ}.
        4. Gib für JEDES Menü die Zubereitung und eine Einkaufsliste an.
        
        DATEN:
        Wünsche: {wünsche} | Kühlschrank: {kuehlschrank} | Budget: {budget} CHF | Kalorien: {kalorien}
        """
        
        with st.spinner('🚀 Sophia, die KI poliert die Rezepte...'):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success("✅ Check erledigt! Hier sind deine Optionen:")
            st.markdown("---")
            st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Oje, Fehler: {e}")

st.markdown("---")
st.markdown("#### 🛒 Deine VIP-Lebensmittel")
for food in st.session_state.allowed_foods:
    cols = st.columns([10, 1])
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("❌", key=food):
        st.session_state.allowed_foods.remove(food)
        st.rerun()
