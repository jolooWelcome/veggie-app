import streamlit as st
from openai import OpenAI

# --- 1. DESIGN & KONFIGURATION (MOBILE FIRST) ---
st.set_page_config(page_title="Sophis Veggie APP", page_icon="🥑", layout="centered")

# Weinrot, Grau & Gelber Akzent + Miniatur-Design für die Liste
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
    
    /* DER GELBE BUTTON (Hauptaktion) */
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
    
    /* KOMPAKTE LEBENSMITTEL-LISTE (Anpassung) */
    .small-food-card {
        background: white;
        padding: 5px 10px;
        border-radius: 6px;
        border-left: 3px solid #722F37;
        margin-bottom: 3px;
        font-size: 0.8rem; /* Kleinere Schrift */
        color: #4b5563;
    }

    /* Kleinere Buttons für die Liste */
    div[data-testid="column"] button {
        padding: 2px 5px !important;
        font-size: 0.7rem !important;
        height: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISIERUNG DER VOLLSTÄNDIGEN LISTE ---
if 'allowed_foods' not in st.session_state:
    st.session_state.allowed_foods = [
        "Weissbrot, Toastbrot (Frisch)", "Reis, Mais, Hirse", "Nudeln (ohne Ei)", 
        "Hafer/Haferflocken", "Wasser", "Tee", "Apfelsaft", "Salz, Olivenöl", 
        "Frische Kräuter", "Frischkäse", "Hüttenkäse", "Butter/Sahne", 
        "Karotte", "Zuccini", "Brokkoli", "Kartoffeln/Süsskartoffeln", 
        "Gurken", "Kopfsalat", "Eisbergsalat", "Blumenkohl", "Sellerie", 
        "Erbsen", "Äpfel/ Birnen (geschält)", "Melone, Trauben (weiss)", "Mango/Heidelbeere"
    ]

# --- 3. HAUPTOBERFLÄCHE ---
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

# --- 4. KI-AKTION (Der gelbe Button) ---
if st.button("✨ KI Menü zaubern"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
        Du bist Sophis persönlicher KI-Koch. Erstelle ein vegetarisches Menü ({plan_art}) für {mahlzeit_typ}.
        WÜNSCHE: {wünsche}, UNVERTRÄGLICHKEITEN: {unvertraeglichkeiten}, BUDGET: {budget} CHF, KALORIEN: {kalorien} kcal.
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

# --- 5. KOMPAKTE LISTE: MEINE ERLAUBTEN NAHRUNGSMITTEL ---
st.markdown("#### 🛒 Erlaubte Nahrungsmittel (kompakt)")

# Eingabe für neue Lebensmittel (ebenfalls kompakt)
new_food = st.text_input("Liste ergänzen:", placeholder="Zutat...", label_visibility="collapsed")
if st.button("➕ Zutat hinzufügen"):
    if new_food and new_food not in st.session_state.allowed_foods:
        st.session_state.allowed_foods.append(new_food)
        st.rerun()

# Anzeige der Liste in kleinerer Schrift
for food in st.session_state.allowed_foods:
    cols = st.columns([10, 1]) # Viel Platz für Text, wenig für den Button
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("❌", key=food): # Kleineres X statt Papierkorb für Platzersparnis
        st.session_state.allowed_foods.remove(food)
        st.rerun()
