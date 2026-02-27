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
        font-size: 3rem !important; 
        color: #722F37 !important; 
        text-align: center !important;
        font-weight: 800 !important;
        margin-bottom: 5px !important;
    }
    
    .sub-title {
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }

    /* EINGABE-CONTAINER */
    div[data-testid="stVerticalBlock"] > div:has(div.stTextArea) {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* DER ZAUBER-BUTTON */
    .stButton>button { 
        background: linear-gradient(135deg, #FFD700 0%, #FFB800 100%) !important; 
        color: #31333F !important; 
        border-radius: 50px !important; 
        border: none !important;
        height: 3.5em !important; 
        width: 100% !important; 
        font-weight: 800 !important;
        box-shadow: 0 8px 15px rgba(255, 215, 0, 0.3) !important;
    }

    /* VIP-LISTEN KARTEN & DELETE BUTTON */
    .small-food-card {
        background: #fff;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #ddd;
        font-size: 0.95rem;
        color: #333 !important;
        height: 45px; /* Gleiche Höhe wie der Button */
        display: flex;
        align-items: center;
    }

    /* GRAUER LÖSCH-BUTTON */
    .del-btn-style button {
        background-color: #E0E0E0 !important;
        color: black !important;
        border: 1px solid #ddd !important;
        border-radius: 8px !important;
        height: 45px !important;
        width: 100% !important;
        font-weight: bold !important;
        transition: background 0.2s !important;
    }
    
    .del-btn-style button:hover {
        background-color: #D0D0D0 !important;
        border-color: #bbb !important;
    }

    /* KI-ANTWORT BOX */
    .ai-response-box {
        background-color: white;
        color: #31333F;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #FFD700;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-top: 20px;
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
st.markdown('<p class="sub-title">Dein smarter Begleiter für gesundes Essen ✨</p>', unsafe_allow_html=True)

with st.container():
    wünsche = st.text_area("✨ Was möchtest du heute essen?", placeholder="z.B. Nudeln...")
    kuehlschrank = st.text_area("🧊 Das habe ich noch im Kühlschrank:", placeholder="z.B. Zuccini...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        mahlzeit_typ = st.selectbox("🍽️ Mahlzeit:", ["Morgenessen", "Mittagessen", "Nachtessen"])
        plan_art = st.radio("📅 Modus:", ["Einmalige Mahlzeit", "Wochenplan (7 Tage)"])
    with col_b:
        kalorien = st.number_input("🔥 Kalorien:", value=600, step=50)
        budget = st.number_input("💰 Budget (CHF):", value=20, step=5)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. KI-LOGIK ---
if st.button("✨ MENÜ ZAUBERN"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
        Identität: Du bist ein strenger, aber lockerer Ernährungsberater.
        Aufgabe: 3 Menüs erstellen. NUR Zutaten aus dieser Liste verwenden: {', '.join(st.session_state.allowed_foods)}.
        Sollte der User Wünsche ({wünsche}) oder Kühlschrank-Inhalt ({kuehlschrank}) haben, die nicht auf der Liste sind, weise höflich darauf hin.
        Mahlzeit: {mahlzeit_typ}. Budget: {budget} CHF. Kalorien: {kalorien}.
        """
        with st.spinner('🧙‍♀️ Sophia kombiniert die Zutaten...'):
            response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            st.session_state.last_response = response.choices[0].message.content
            st.rerun()
    except Exception as e:
        st.error(f"Fehler: {e}")

if st.session_state.last_response:
    st.markdown(f'<div class="ai-response-box">{st.session_state.last_response}</div>', unsafe_allow_html=True)
    if st.button("👨‍🍳 Neue Ideen"):
        st.session_state.last_response = None
        st.rerun()

# --- 5. VIP LISTE VERWALTUNG ---
st.markdown("---")
st.markdown('### 🛒 Diese Zutaten darf ich verwenden')

# NEUE ZUTAT HINZUFÜGEN
new_food = st.text_input("➕ Neue Zutat zur Liste hinzufügen:", placeholder="z.B. Quinoa, Tofu...")
if st.button("Hinzufügen"):
    if new_food and new_food not in st.session_state.allowed_foods:
        st.session_state.allowed_foods.append(new_food)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ANZEIGE DER LISTE MIT GRAUEN BUTTONS
for food in st.session_state.allowed_foods:
    cols = st.columns([8, 2]) # Verhältnis angepasst für breitere Buttons
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    
    # Der Lösch-Button in einem speziellen Design-Container
    with cols[1]:
        st.markdown('<div class="del-btn-style">', unsafe_allow_html=True)
        if st.button("X", key=f"del_{food}"):
            st.session_state.allowed_foods.remove(food)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)




