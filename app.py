import streamlit as st
from openai import OpenAI

# --- 1. DESIGN & KONFIGURATION (MOBILE FIRST) ---
st.set_page_config(page_title="Sophis Veggie APP", page_icon="🥑", layout="centered")

# Weinrot & Grau Styling mit gelbem Button-Akzent
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    .stApp p, .stApp div, .stApp span, .stApp li, .stApp label { 
        color: #31333F !important; 
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 { color: #722F37 !important; text-align: center; }
    
    .stTextArea textarea, .stTextInput input, .stNumberInput input {
        border: 1px solid #722F37 !important;
        border-radius: 8px !important;
    }
    
    /* DER GELBE BUTTON (Anpassung) */
    .stButton>button { 
        background-color: #FFD700 !important; /* Gelb/Gold */
        color: #31333F !important; /* Dunkle Schrift für bessere Lesbarkeit */
        border-radius: 12px; 
        border: 2px solid #722F37; /* Weinroter Rand für den Kontrast */
        height: 3.5em; 
        width: 100%; 
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .food-card {
        background: white;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #722F37;
        margin-bottom: 5px;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIK FÜR DIE LEBENSMITTELLISTE (Sophias Liste) ---
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
st.title("🥑 Sophis Veggie APP")

with st.container():
    wünsche = st.text_area("Was möchtest du essen?", placeholder="z.B. Etwas Leichtes...")
    unvertraeglichkeiten = st.text_input("Unverträglichkeiten:", placeholder="Zusätzliche Infos...")
    
    col1, col2 = st.columns(2)
    with col1:
        mahlzeit_typ = st.selectbox("Mahlzeit auswählen:", ["Morgenessen", "Mittagessen", "Nachtessen"])
        plan_art = st.radio("Zeitraum:", ["Einmalige Mahlzeit", "Wochenplan (7 Tage)"])
    
    with col2:
        kalorien = st.number_input("Kalorienziel:", value=600)
        budget = st.number_input("Budget (CHF):", value=20)

# --- 4. KI-AKTION ---
if st.button("✨ KI Menü zaubern"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        prompt = f"""
        Du bist Sophis persönlicher KI-Koch. Erstelle ein vegetarisches Menü ({plan_art}) für {mahlzeit_typ}.
        WÜNSCHE: {wünsche}
        UNVERTRÄGLICHKEITEN: {unvertraeglichkeiten}
        BUDGET: {budget} CHF
        KALORIEN: {kalorien} kcal pro Mahlzeit.
        NUTZE AUSSCHLIESSLICH ODER BEVORZUGT DIESE LEBENSMITTEL: {', '.join(st.session_state.allowed_foods)}
        
        Wording: Motivierend, frisch und klar.
        """
        
        with st.spinner('Sophia, dein gelber Glücksbutton arbeitet...'):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success("Dein Gourmet-Plan ist fertig!")
            st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Fehler: {e}")

st.markdown("---")

# --- 5. INTERAKTIVE LISTE: WAS DARF SOPHIA ESSEN? ---
st.subheader("🛒 Erlaubte Lebensmittel")

# Neues Lebensmittel hinzufügen
new_food = st.text_input("Liste ergänzen:", placeholder="Zutat tippen...")
if st.button("➕ Zutat hinzufügen"):
    if new_food and new_food not in st.session_state.allowed_foods:
        st.session_state.allowed_foods.append(new_food)
        st.rerun()

# Liste anzeigen
for food in st.session_state.allowed_foods:
    cols = st.columns([5, 1])
    cols[0].markdown(f"<div class='food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("🗑️", key=food):
        st.session_state.allowed_foods.remove(food)
        st.rerun()
