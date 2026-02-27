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

    /* ZWECKGEBUNDENE SCHRIFTFARBE: SCHWARZ */
    /* Dies gilt für KI-Antworten und spezifische Sektionen */
    .black-text {
        color: black !important;
        font-weight: bold !important;
    }

    /* FIX: LADETEXT (SPINNER) IN SCHWARZ */
    div[data-testid="stStatusWidget"] p {
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
if st.button("✨ KI Menü zaubern"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
        Identität: Du bist ein strenger, aber lockerer Ernährungsberater. Dein Tonfall ist motivierend.
Hauptaufgabe: Erstelle für Sophia genau 3 Menüvorschläge basierend auf ihren Eingaben auf der APP inklusive Einkaufsliste, Kosten Kalorien
Strenge Verbote: > - Benutze NIEMALS Zutaten, die nicht in der VIP-Liste stehen oder die nicht vegetarisch sind. Weise in diesem Fall Sophia darauf hin
•	Schlage keine Gerichte vor, die länger als 20 Minuten dauern.
•	[Hier ein weiteres Verbot einfügen, z.B. "Kein Alkohol"].
Pflicht-Elemente pro Gericht:
1.	Ein kreativer Name.
2.	Eine Liste der Vitamine, die darin enthalten sind.
3.	Eine kurze Schätzung, wie viel "Dreckiges Geschirr" (Skala 1-5) anfällt.
4.	Das Rezept in maximal 5 Schritten. Ein kreativer Name.
5.	Einkaufsliste
6.	Gesamtkalorien pro Menü

        
NUTZE DIESE DATEN:
Wünsche: {wünsche}
Kühlschrank: {kuehlschrank}
VIP-Liste: {', '.join(st.session_state.allowed_foods)}
Mahlzeit: {mahlzeit_typ}
        """
        # Hier ist der schwarze Ladetext
        with st.spinner('Sophia, die KI stellt die Optionen zusammen...'):
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
    st.markdown("---")
    # Ergebnis-Schrift in Schwarz über CSS-Klasse
    st.markdown(f'<div style="color: black;">{st.session_state.last_response}</div>', unsafe_allow_html=True)
    
    if st.button("👨‍🍳 Neues Menü würfeln"):
        st.session_state.last_response = None
        st.rerun()

st.markdown("---")
# Überschrift in Schwarz
st.markdown('<p class="black-text">🛒 Meine erlaubten Nahrungsmittel</p>', unsafe_allow_html=True)

for food in st.session_state.allowed_foods:
    cols = st.columns([10, 1])
    cols[0].markdown(f"<div class='small-food-card'>{food}</div>", unsafe_allow_html=True)
    if cols[1].button("❌", key=f"del_{food}"):
        st.session_state.allowed_foods.remove(food)
        st.rerun()

