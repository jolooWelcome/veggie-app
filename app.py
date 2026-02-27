import streamlit as st
from openai import OpenAI

# --- 1. DESIGN & KONSTRUKTION (CSS) ---
st.set_page_config(page_title="Sophis Veggie APP", page_icon="🥦", layout="centered")

st.markdown("""
    <style>
    /* Hintergrund */
    .stApp { background-color: #f4f4f4; }
    
    /* TITEL */
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

    /* SCHWARZE EINGABEFELDER mit WEISSER SCHRIFT */
    .stTextArea textarea, .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
        background-color: #31333F !important;
        color: white !important;
        border: 2px solid #722F37 !important;
        border-radius: 8px !important;
    }

    .black-text {
        color: black !important;
        font-weight: bold !important;
    }

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
    
    /* VIP-Karten Design */
    .small-food-card {
        background: white;
        padding: 5px 10px;
        border-radius: 6px;
        border-left: 3px solid #722F37;
        margin-bottom: 3px;
        font-size: 0.85rem;
        color: black !important;
        height: 38px; /* Höhe für Angleichung an Button */
        display: flex;
        align-items: center;
    }

    /* GRAUER LÖSCH-BUTTON (Anpassung laut Auftrag) */
    .stButton>button[key^="del_"] {
        background-color: #cccccc !important;
        color: black !important;
        border: 1px solid #999999 !important;
        border-radius: 6px !important;
        height: 38px !important; /* Gleiche Höhe wie das Feld */
        width: 100% !important;
        padding: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISIERUNG SESSION STATE ---
if 'last_response' not in st.session_state:
    st.session_state.last_response = None
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
st.markdown('<h1 class="main-title">Sophis Veggie APP</h1>', unsafe_allow_html=True)

with st.container():
    wünsche = st.text_area("Was möchtest du essen?", placeholder="z.B. Nudeln...")
    kuehlschrank = st.text_area("Habe ich noch im Kühlschrank:", placeholder="z.B. Zuccini...")
    
    col1, col2 = st.columns(2)
    with col1:
        mahlzeit_typ = st.selectbox("Mahlzeiten anpassen:", ["Morgenessen", "Mittagessen", "Nachtessen"])
        plan_art = st.radio("Plan-Modus:", ["Einmalige Mahlzeit", "Wochenplan (7 Tage)"])
    
    with col2:
        kalorien = st.number_input("Kalorienziel pro Mahlzeit:", value=600)
        budget = st.number_input("Budget (CHF):", value=20)

# --- 4. KI-LOGIK ---
if st.button("✨ Menü zaubern"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
        Identität: Du bist ein strenger, aber lockerer Ernährungsberater.
        Aufgabe: 3 Menüs aus dieser Liste erstellen: {', '.join(st.session_state.allowed_foods)}.
        Sollte der User Wünsche ({wünsche}) oder Kühlschrank ({kuehlschrank}) haben, die nicht auf der Liste sind, weise höflich darauf hin.
        """
        with st.spinner('Sophia, die KI stellt die Optionen zusammen...'):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.last_response = response.choices[0].message.content
            st.rerun()
    except Exception as e:
        st.error(f"Fehler: {e}")

if st.session_state.last_response:
    st.markdown("---")
    st.markdown(f'<div style="color: black;">{st.session_state.last_response}</div>', unsafe_allow_html=True)
    if st.button("👨‍🍳 Neues Menü würfeln"):
        st.session_state.last_response = None
        st.rerun()

# --- 5. VIP LISTE VERWALTUNG (Deine Anpassungen) ---
st.markdown("---")
st.markdown('<p class="black-text">🛒 Diese Zutaten darf ich verwenden</p>', unsafe_allow_html=True)

# Feld zum Ergänzen neuer Zutaten
neue_zutat = st.text_input("Zutat zur VIP-Liste hinzufügen:")
if st.button("Hinzufügen"):
    if neue_zutat and neue_zutat not in st.session_state.allowed_foods:
        st.session_state.allowed_foods.append(neue_zutat)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

for food in st.session_state.allowed_foods:
    cols = st.columns([10, 2])
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("X", key=f"del_{food}"):
        st.session_state.allowed_foods.remove(food)
        st.rerun()

