import streamlit as st
from openai import OpenAI

# --- 1. DESIGN & KONFIGURATION (MOBILE FIRST) ---
st.set_page_config(page_title="Sophis Veggie APP", page_icon="🥑", layout="centered")

# Weinrot & Grau Styling
st.markdown("""
    <style>
    /* Hintergrund & Basis-Schrift */
    .stApp { background-color: #f4f4f4; }
    .stApp p, .stApp div, .stApp span, .stApp li, .stApp label { 
        color: #31333F !important; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Header-Styling */
    h1, h2, h3 { color: #722F37 !important; text-align: center; }
    
    /* Input-Felder Styling */
    .stTextArea textarea, .stTextInput input, .stNumberInput input {
        border: 1px solid #722F37 !important;
        border-radius: 8px !important;
    }
    
    /* Der Weinrote Button */
    .stButton>button { 
        background-color: #722F37 !important; 
        color: white !important; 
        border-radius: 12px; 
        border: none; 
        height: 3.5em; 
        width: 100%; 
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Card-Look für die Lebensmittelliste */
    .food-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #722F37;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIK FÜR DIE LEBENSMITTELLISTE ---
# Wir speichern die Liste dauerhaft für diese Sitzung
if 'allowed_foods' not in st.session_state:
    st.session_state.allowed_foods = ["Avocado", "Quinoa", "Kichererbsen", "Feta", "Spinat"]

# --- 3. OBERFLÄCHE (UI) ---
st.title("🥑 Sophis Veggie APP")
st.markdown("---")

# Eingabe-Bereich
with st.container():
    wünsche = st.text_area("Was möchtest du essen?", placeholder="z.B. Etwas Leichtes mit Nudeln...")
    unvertraeglichkeiten = st.text_input("Unverträglichkeiten:", placeholder="z.B. Laktose, Nüsse...")
    
    col1, col2 = st.columns(2)
    with col1:
        mahlzeit_typ = st.selectbox("Mahlzeit:", ["Morgenessen", "Mittagessen", "Nachtessen"])
        plan_art = st.radio("Planung für:", ["Einmalige Mahlzeit", "Wochenplan (7 Tage)"])
    
    with col2:
        kalorien = st.number_input("Kalorienziel:", value=600)
        budget = st.number_input("Budget (CHF):", value=20)

# --- 4. KI-AKTION ---
if st.button("✨ KI-Menü zaubern"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        prompt = f"""
        Du bist Sophis persönlicher KI-Koch. Erstelle ein vegetarisches Menü ({plan_art}) für {mahlzeit_typ}.
        WÜNSCHE: {wünsche}
        UNVERTRÄGLICHKEITEN: {unvertraeglichkeiten}
        BUDGET: {budget} CHF
        KALORIEN: {kalorien} kcal pro Mahlzeit.
        NUTZE BEVORZUGT DIESE LEBENSMITTEL: {', '.join(st.session_state.allowed_foods)}
        
        Struktur: 1. Name des Gerichts, 2. Zutaten, 3. Anleitung, 4. Nährwert-Check.
        Wording: Motivierend, frisch und klar.
        """
        
        with st.spinner('Sophia, die KI stellt dein Menü zusammen...'):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success("Dein Gourmet-Plan ist da!")
            st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Huch! Da gab es ein Problem: {e}")

st.markdown("---")

# --- 5. INTERAKTIVE LISTE: WAS DARF SOPHIA ESSEN? ---
st.subheader("🛒 Meine erlaubten Lebensmittel")
st.info("Diese Liste nutzt die KI bevorzugt für deine Rezepte.")

# Neues Lebensmittel hinzufügen
new_food = st.text_input("Neues Lebensmittel ergänzen:", placeholder="z.B. Tofu")
if st.button("➕ Hinzufügen"):
    if new_food and new_food not in st.session_state.allowed_foods:
        st.session_state.allowed_foods.append(new_food)
        st.rerun()

# Liste anzeigen und löschen ermöglichen
for food in st.session_state.allowed_foods:
    cols = st.columns([4, 1])
    cols[0].markdown(f"<div class='food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("🗑️", key=food):
        st.session_state.allowed_foods.remove(food)
        st.rerun()
