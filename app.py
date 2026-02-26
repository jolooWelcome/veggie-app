import streamlit as st
from openai import OpenAI

# --- 1. DESIGN & KONFIGURATION ---
st.set_page_config(page_title="Sophis Veggie APP", page_icon="🥑", layout="centered")

# CSS für Weinrot, Grau, Gelben Button und "Black Fields" mit weißer Schrift
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    
    /* Allgemeine Schriftfarbe */
    .stApp p, .stApp div, .stApp span, .stApp li, .stApp label { 
        color: #31333F !important; 
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 { color: #722F37 !important; text-align: center; }
    
    /* "BLACK FIELDS": Dunkle Eingabefelder mit weißer Schrift */
    .stTextArea textarea, .stTextInput input, .stNumberInput input {
        background-color: #31333F !important;
        color: white !important;
        border: 2px solid #722F37 !important;
        border-radius: 8px !important;
    }

    /* Gelber Zauber-Button */
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
    
    /* Kompakte Lebensmittel-Karten */
    .small-food-card {
        background: white;
        padding: 5px 10px;
        border-radius: 6px;
        border-left: 3px solid #722F37;
        margin-bottom: 3px;
        font-size: 0.8rem;
        color: #4b5563;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISIERUNG DER NAHRUNGSMITTEL ---
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
    wünsche = st.text_area("Was möchtest du essen?", placeholder="z.B. Nudeln mit Gemüse...")
    kuehlschrank = st.text_area("Habe ich noch im Kühlschrank:", placeholder="z.B. Brokkoli, Frischkäse...")
    unvertraeglichkeiten = st.text_input("Unverträglichkeiten:", placeholder="Zusätzliche Infos...")
    
    col1, col2 = st.columns(2)
    with col1:
        mahlzeit_typ = st.selectbox("Mahlzeit auswählen:", ["Morgenessen", "Mittagessen", "Nachtessen"])
        plan_art = st.radio("Zeitraum:", ["Einmalige Mahlzeit", "Wochenplan (7 Tage)"])
    
    with col2:
        kalorien = st.number_input("Kalorienziel:", value=600)
        budget = st.number_input("Budget (CHF):", value=20)

# --- 4. KI-LOGIK (STRENGER FILTER) ---
if st.button("✨ KI Menü zaubern"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # Die Anweisung wurde verschärft: NUR die genannten Zutaten verwenden
        prompt = f"""
        Du bist Sophis persönlicher KI-Koch. Erstelle ein vegetarisches Menü ({plan_art}) für {mahlzeit_typ}.
        
        WICHTIGSTE REGEL: Verwende für die Rezepte AUSSCHLIESSLICH Zutaten aus diesen zwei Listen:
        1. WÜNSCHE: {wünsche}
        2. KÜHLSCHRANK: {kuehlschrank}
        (Salz, Wasser und Olivenöl sind als Basis immer erlaubt).
        
        Berücksichtige zudem:
        - UNVERTRÄGLICHKEITEN: {unvertraeglichkeiten}
        - BUDGET: {budget} CHF
        - KALORIEN: {kalorien} kcal.
        
        STRUKTUR DER ANTWORT:
        1. 🍽️ MENÜ-VORSCHLAG (Name, Zutaten, Anleitung)
        2. 🛒 EINKAERFSLISTE (Was muss noch gekauft werden, um die Wünsche zu erfüllen?)
        """
        
        with st.spinner('Sophia, die KI filtert deine Zutaten...'):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success("Dein Gourmet-Plan & Einkaufsliste sind bereit!")
            st.markdown("---")
            st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Fehler: {e}")

st.markdown("---")

# --- 5. KOMPAKTE LISTE: MEINE ERLAUBTEN NAHRUNGSMITTEL ---
st.markdown("#### 🛒 Meine erlaubten Nahrungsmittel (Referenz)")

new_food = st.text_input("Liste ergänzen:", placeholder="Zutat...", label_visibility="collapsed")
if st.button("➕ Hinzufügen"):
    if new_food and new_food not in st.session_state.allowed_foods:
        st.session_state.allowed_foods.append(new_food)
        st.rerun()

# Kompakte Anzeige der Liste
for food in st.session_state.allowed_foods:
    cols = st.columns([10, 1])
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("❌", key=food):
        st.session_state.allowed_foods.remove(food)
        st.rerun()
