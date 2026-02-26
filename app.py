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

    /* ZWECKGEBUNDENE SCHRIFTFARBE DER KI-ANTWORT: IMMER SCHWARZ */
    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: black !important;
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
    
    /* Kompakte Karten */
    .small-food-card {
        background: white;
        padding: 5px 10px;
        border-radius: 6px;
        border-left: 3px solid #722F37;
        margin-bottom: 3px;
        font-size: 0.85rem;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISIERUNG SESSION STATE (Speicher für Interaktion) ---
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

# --- 4. KI-LOGIK MIT INTERAKTIONS-FLOW ---
if st.button("✨ KI Menü zaubern"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
        Du bist Sophis persönlicher KI-Buddy (16, locker & witzig). 
        STRENGE REGEL: Verwende AUSSCHLIESSLICH Zutaten aus 'Wünsche' oder 'Kühlschrank'.
        Checke gegen VIP-Liste: {', '.join(st.session_state.allowed_foods)}. 
        Wording: Locker, witzig, Emojis.
        
        AUFTRAG:
        Generiere 3 Menü-Vorschläge. 
        Für JEDEN Vorschlag erstelle: 
        1. Name des Gerichts
        2. Das detaillierte Rezept & Zubereitung
        3. Die Einkaufsliste mit Preisen in CHF.
        
        Daten: Wünsche: {wünsche}, Kühlschrank: {kuehlschrank}, Budget: {budget} CHF, Kcal: {kalorien}.
        """
        with st.spinner('🚀 Sophia, die KI stellt die Optionen zusammen...'):
            response = client.chat.completions.create(
                model="gpt-4o", # Wir nutzen das stärkere Modell für bessere Struktur
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.last_response = response.choices[0].message.content
            st.rerun() # Seite neu laden, um Buttons anzuzeigen
    except Exception as e:
        st.error(f"Oje, Fehler: {e}")

# Wenn ein Resultat da ist, zeigen wir es an
if st.session_state.last_response:
    st.markdown("---")
    st.success("✅ Deine Optionen sind bereit!")
    
    # Wir zeigen erst mal nur die Übersicht an (vereinfacht für die Demo)
    # Profi-Tipp: Hier könnte man den Text splitten. Für den User zeigen wir jetzt alles an, 
    # fügen aber die interaktive Bestätigung ein.
    
    st.markdown("### Hier sind deine Gourmet-Ideen:")
    st.write(st.session_state.last_response)
    
    st.markdown("---")
    st.markdown("### 🛠️ Was soll ich als Nächstes tun?")
    col_btn1, col_btn2 = st.columns(2)
    
    if col_btn1.button("📑 Einkaufsliste als Text zeigen"):
        st.info("Kopiere die Liste oben einfach in deine Notizen-App!")
        
    if col_btn2.button("👨‍🍳 Neues Menü würfeln"):
        st.session_state.last_response = None
        st.rerun()

st.markdown("---")
st.markdown("#### 🛒 Meine erlaubten Nahrungsmittel")
for food in st.session_state.allowed_foods:
    cols = st.columns([10, 1])
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("❌", key=f"del_{food}"):
        st.session_state.allowed_foods.remove(food)
        st.rerun()
