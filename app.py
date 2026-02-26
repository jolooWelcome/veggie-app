import streamlit as st
from openai import OpenAI

# --- 1. DESIGN & HARMONISIERUNG (CSS) ---
st.set_page_config(page_title="Sophis Veggie APP", page_icon="🥦", layout="centered")

st.markdown("""
    <style>
    /* Hintergrund */
    .stApp { background-color: #f4f4f4; }
    
    /* TITEL: RIESIG & WEINROT */
    .main-title { 
        font-size: 4.5rem !important; 
        color: #722F37 !important; 
        text-align: center !important;
        margin-bottom: 30px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ÜBERSCHRIFTEN (Labels) */
    .stApp label p, .stApp h2, .stApp h3 { 
        color: #31333F !important; 
        font-family: 'Inter', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }

    /* SPEZIELLE ÜBERSCHRIFT FÜR ERLAUBTE NAHRUNGSMITTEL (SCHWARZ) */
    .food-header {
        color: black !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        margin-top: 20px;
    }

    /* SCHWARZE EINGABEFELDER (Inputs) */
    .stTextArea textarea, .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
        background-color: #31333F !important;
        color: white !important;
        border: 2px solid #722F37 !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }

    /* FIX: AUSGEWÄHLTE MAHLZEIT IM FELD ZWINGEND WEISS */
    div[data-baseweb="select"] span, 
    div[data-baseweb="select"] div[aria-selected="true"],
    div[data-baseweb="select"] div {
        color: white !important;
    }

    /* RADIO-BUTTONS */
    div[role="radiogroup"] {
        background-color: #31333F;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #722F37;
    }
    div[role="radiogroup"] label p { color: white !important; }

    /* GELBER ZAUBER-BUTTON */
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
    }
    
    /* KOMPAKTE LEBENSMITTEL-LISTE (SCHWARZE SCHRIFT) */
    .small-food-card {
        background: white;
        padding: 5px 10px;
        border-radius: 6px;
        border-left: 3px solid #722F37;
        margin-bottom: 3px;
        font-size: 0.85rem;
        color: black !important; /* Zwingend Schwarz für Sophia */
        font-weight: 500;
    }

    /* FIX FÜR DAS EINGABEFELD IN DER LISTE (SCHWARZ) */
    .food-list-input input {
        color: black !important;
        background-color: white !important;
        border: 1px solid #722F37 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISIERUNG DER ERLAUBTEN LISTE ---
if 'allowed_foods' not in st.session_state:
    st.session_state.allowed_foods = [
        "Weissbrot, Toastbrot (Frisch)", "Reis, Mais, Hirse", "Nudeln (ohne Ei)", 
        "Hafer/Haferflocken", "Wasser", "Tee", "Apfelsaft", "Salz, Olivenöl", 
        "Frische Kräuter", "Frischkäse", "Hüttenkäse", "Butter/Sahne", 
        "Karotte", "Zuccini", "Brokkoli", "Kartoffeln/Süsskartoffeln", 
        "Gurken", "Kopfsalat", "Eisbergsalat", "Blumenkohl", "Sellerie", 
        "Erbsen", "Äpfel/ Birnen (geschält)", "Melone, Trauben (weiss)", "Mango/Heidelbeere"
    ]

# --- 3. OBERFLÄCHE (UI) ---
st.markdown('<h1 class="main-title">Sophis Veggie APP</h1>', unsafe_allow_html=True)

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
        Du bist Sophis persönlicher KI-Buddy (16 Jahre alt, locker & witzig).
        STRENGE REGELN:
        1. Rezepte NUR aus 'Wünsche' oder 'Kühlschrank'.
        2. Check gegen VIP-Liste: {', '.join(st.session_state.allowed_foods)}. 
           Falls was fehlt -> witzige Warnung!
        3. Fleisch/Fisch? -> Absolutes Veto im Teenie-Slang!
        4. Erstelle 3 Menü-Optionen ({plan_art}) für {mahlzeit_typ} inkl. Zubereitung & Einkaufsliste.
        """
        with st.spinner('🚀 Sophia, die KI poliert die Rezepte...'):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success("✅ Check erledigt! Hier sind deine Optionen:")
            st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Oje, Fehler: {e}")

st.markdown("---")

# --- 5. ERLAUBTE LISTE ANZEIGEN (SCHWARZE SCHRIFT) ---
st.markdown('<p class="food-header">🛒 Meine erlaubten Nahrungsmittel</p>', unsafe_allow_html=True)

# Das Eingabefeld für neue Nahrungsmittel in Weiß/Schwarz
st.markdown('<div class="food-list-input">', unsafe_allow_html=True)
new_food = st.text_input("Nahrungsmittel ergänzen:", placeholder="Zutat tippen...", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("➕ Hinzufügen"):
    if new_food and new_food not in st.session_state.allowed_foods:
        st.session_state.allowed_foods.append(new_food)
        st.rerun()

# Kompakte Anzeige der Liste in SCHWARZ
for food in st.session_state.allowed_foods:
    cols = st.columns([10, 1])
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("❌", key=food):
        st.session_state.allowed_foods.remove(food)
        st.rerun()
