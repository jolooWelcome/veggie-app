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

    /* GELBER HAUPT-BUTTON */
    .stButton>button { 
        background-color: #FFD700 !important; 
        color: #31333F !important; 
        border-radius: 12px; 
        border: 2px solid #722F37; 
        height: 3.5em; 
        width: 100%; 
        font-weight: bold;
        font-size: 1.1rem;
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
        height: 35px;
        display: flex;
        align-items: center;
    }

/* SPEZIAL-STYLING FÜR DIE LÖSCH-BUTTONS */
    /* Wir suchen alle Buttons, deren interner Name mit 'del_' beginnt */
    div.stButton > button[key^="del_"] {
        background-color: #31333F !important; /* Dunkel wie deine Budget-Felder */
        color: white !important;              /* Das Kreuz wird weiß */
        border: 1px solid #722F37 !important; /* Ein dezenter Rand in deiner App-Farbe */
        border-radius: 6px !important;
        height: 35px !important;              /* Schön kompakt */
        width: 45px !important;               /* Nicht zu breit */
        padding: 0px !important;
        line-height: 1 !important;
        font-weight: bold !important;
    }

    /* Damit der Button beim Drücken nicht wieder gelb wird */
    div.stButton > button[key^="del_"]:active, 
    div.stButton > button[key^="del_"]:focus,
    div.stButton > button[key^="del_"]:hover {
        background-color: #454754 !important; /* Etwas heller beim Drüberfahren */
        color: white !important;
        border-color: #722F37 !important;
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
        
        # Arbeits-Anzeige während der Generierung
        with st.status("Das Menü wird erstellt...", expanded=True) as status:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.last_response = response.choices[0].message.content
            status.update(label="Menü fertig gezaubert!", state="complete", expanded=False)
            st.rerun()
            
    except Exception as e:
        st.error(f"Fehler: {e}")

if st.session_state.last_response:
    st.markdown("---")
    st.markdown(f'<div style="color: black;">{st.session_state.last_response}</div>', unsafe_allow_html=True)
    if st.button("👨‍🍳 Neues Menü würfeln"):
        st.session_state.last_response = None
        st.rerun()

# --- 5. VIP LISTE VERWALTUNG ---
st.markdown("---")
st.markdown('<p class="black-text">🛒 Diese Zutaten darf ich verwenden</p>', unsafe_allow_html=True)

neue_zutat = st.text_input("Zutat zur VIP-Liste hinzufügen:")
if st.button("Hinzufügen"):
    if neue_zutat and neue_zutat not in st.session_state.allowed_foods:
        st.session_state.allowed_foods.append(neue_zutat)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

for food in st.session_state.allowed_foods:
    # Aufteilung 10 zu 1, damit der Lösch-Button schmal bleibt
    cols = st.columns([10, 1])
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    with cols[1]:
        if st.button("X", key=f"del_{food}"):
            st.session_state.allowed_foods.remove(food)
            st.rerun()


