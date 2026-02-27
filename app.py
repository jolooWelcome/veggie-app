import streamlit as st
from openai import OpenAI

# --- 1. DESIGN & KONSTRUKTION (CSS) ---
st.set_page_config(page_title="Sophis Veggie APP", page_icon="🥦", layout="centered")

st.markdown("""
    <style>
    /* Hintergrund & Schriftart */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { 
        background-color: #F8F9FA; 
        font-family: 'Inter', sans-serif;
    }
    
    /* TITEL DESIGN */
    .main-title { 
        font-size: 3.5rem !important; 
        color: #722F37 !important; 
        text-align: center !important;
        margin-bottom: 10px !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-title {
        text-align: center;
        color: #555;
        margin-bottom: 40px;
        font-size: 1.1rem;
    }

    /* EINGABE-CONTAINER (Cards) */
    div[data-testid="stVerticalBlock"] > div:has(div.stTextArea) {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* LABELS & ÜBERSCHRIFTEN */
    .stApp label p { 
        color: #722F37 !important; 
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    /* STYLING DER INPUT-FELDER */
    .stTextArea textarea, .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #31333F !important;
        border: 1px solid #ddd !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #722F37 !important;
        box-shadow: 0 0 0 2px rgba(114, 47, 55, 0.2) !important;
    }

    /* DER ZAUBER-BUTTON */
    .stButton>button { 
        background: linear-gradient(135deg, #FFD700 0%, #FFB800 100%) !important; 
        color: #31333F !important; 
        border-radius: 50px !important; 
        border: none !important;
        height: 4em !important; 
        width: 100% !important; 
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        letter-spacing: 1px;
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3) !important;
        transition: transform 0.2s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
    }

    /* KI-ANTWORT BOX */
    .ai-response-box {
        background-color: white;
        color: #31333F;
        padding: 30px;
        border-radius: 20px;
        border-left: 8px solid #FFD700;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        line-height: 1.6;
        margin-top: 20px;
    }

    /* VIP-LISTEN KARTEN */
    .small-food-card {
        background: #fff;
        padding: 8px 15px;
        border-radius: 50px;
        border: 1px solid #eee;
        margin-bottom: 5px;
        font-size: 0.9rem;
        color: #333 !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISIERUNG ---
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
st.markdown('<p class="sub-title">Gesunde Rezepte basierend auf deinen Vorräten ✨</p>', unsafe_allow_html=True)

# Eingabe-Bereich in einer Box
with st.container():
    wünsche = st.text_area("✨ Was möchtest du heute essen?", placeholder="z.B. Etwas Leichtes mit Nudeln...")
    kuehlschrank = st.text_area("🧊 Das habe ich noch im Kühlschrank:", placeholder="z.B. 2 Karotten, Frischkäse...")
    
    col1, col2 = st.columns(2)
    with col1:
        mahlzeit_typ = st.selectbox("🍽️ Mahlzeit:", ["Morgenessen", "Mittagessen", "Nachtessen"])
        plan_art = st.radio("📅 Modus:", ["Einmalige Mahlzeit", "Wochenplan (7 Tage)"])
    
    with col2:
        kalorien = st.number_input("🔥 Kalorien-Limit:", value=600, step=50)
        budget = st.number_input("💰 Budget (CHF):", value=20, step=5)

st.markdown("<br>", unsafe_allow_html=True) # Abstandhalter

# --- 4. KI-LOGIK ---
if st.button("✨ MENÜ ZAUBERN"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        prompt = f"""
        Identität: Du bist ein strenger, aber lockerer Ernährungsberater. Dein Tonfall ist motivierend.
        Hauptaufgabe: Erstelle für Sophia genau 3 Menüvorschläge inklusive Einkaufsliste, Kostenangaben und Kalorienangaben.
        
        STRENGE REGELN: 
        - NUR Zutaten aus der VIP-Liste oder den Usereingaben verwenden.
        - Alles muss vegetarisch sein.
        - Zubereitung unter 30 Minuten.
        
        DATEN:
        - Wunsch: {wünsche}
        - Kühlschrank: {kuehlschrank}
        - VIP-Liste: {', '.join(st.session_state.allowed_foods)}
        - Mahlzeit: {mahlzeit_typ}
        """

        with st.spinner('🧙‍♀️ Sophia schwingt den Kochlöffel...'):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.last_response = response.choices[0].message.content
            st.rerun()
    except Exception as e:
        st.error(f"Fehler: {e}")

# Resultate anzeigen
if st.session_state.last_response:
    st.markdown("### 🍲 Deine Menü-Vorschläge")
    st.markdown(f'<div class="ai-response-box">{st.session_state.last_response}</div>', unsafe_allow_html=True)
    
    if st.button("👨‍🍳 Neue Ideen würfeln"):
        st.session_state.last_response = None
        st.rerun()

# VIP Liste Bereich
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('### 🛒 Meine VIP-Zutaten')
st.info("Diese Zutaten darf die KI immer verwenden.")

for food in st.session_state.allowed_foods:
    cols = st.columns([10, 1])
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("❌", key=f"del_{food}"):
        st.session_state.allowed_foods.remove(food)
        st.rerun()








