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
    button[kind="primary"] {  /* NEU: nur Primary Buttons gelb */
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

    /* NEU: VIP-Chips (Option B) */
    .vip-chip-left {
        background: white;
        border: 1px solid rgba(114, 47, 55, 0.35);
        border-right: none;
        border-radius: 999px 0 0 999px;
        padding: 6px 12px;
        min-height: 35px;
        display: flex;
        align-items: center;
        color: #31333F !important;
        font-size: 0.9rem;
        overflow-wrap: anywhere;
    }

    /* NEU: "X" als Chip-Kappe rechts (passt optisch an die Pill an) */
    button[kind="tertiary"] {
        background: white !important;
        color: #6b7280 !important; /* neutral grau */
        border: 1px solid rgba(114, 47, 55, 0.35) !important;
        border-left: none !important;
        border-radius: 0 999px 999px 0 !important;
        height: 35px !important;
        width: 42px !important;
        padding: 0 !important;
        line-height: 1 !important;
        font-weight: 800 !important;
    }

    button[kind="tertiary"]:hover {
        background: rgba(220, 38, 38, 0.10) !important; /* leicht rot */
        color: #dc2626 !important;
        border-color: rgba(220, 38, 38, 0.35) !important;
    }

    button[kind="tertiary"]:focus,
    button[kind="tertiary"]:active {
        background: rgba(114, 47, 55, 0.08) !important;
        color: #722F37 !important;
        border-color: rgba(114, 47, 55, 0.45) !important;
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
if st.button("✨ Menü zaubern", type="primary"):  # NEU
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # ACHTUNG: Diese Zeile muss genau 8 Leerzeichen (oder 2 Tabs) vom Rand eingerückt sein
        prompt = f"""
        Identität: Du bist ein strenger, aber lockerer Ernährungsberater. Dein Tonfall ist motivierend. Nutze ss anstelle ß
        
        Hauptaufgabe: Erstelle für Sophia genau 3 Menüvorschläge basierend auf ihren Eingaben auf der APP inklusive Einkaufsliste, Kostenangaben und Kalorienangaben pro Menü
        
        Strenge Verbote: 
        - Benutze NIEMALS Zutaten, die nicht in der VIP-Liste stehen oder die nicht vegetarisch sind. Weise in diesem Fall Sophia darauf hin
        - Schlage keine Gerichte vor, die länger als 30 Minuten dauern.
        - Mach einen Hinweis bei Zutaten, die nicht auf der VIP-Liste sind, und bei nicht vegetarischen Zutaten wie Felisch und Fisch. Diese Zutaten dürfen dann auch nicht für die Menügestaltung verwendet werden
        
        Pflicht-Elemente pro Gericht:
        1. Ein kreativer Name.
        2. Eine Liste der Vitamine, die darin enthalten sind.
        3. Eine kurze Schätzung, wie viel "Dreckiges Geschirr" (Skala 1-5) anfällt.
        4. Das Rezept ausführlich beschreiben.
        5. Einkaufsliste mit Einzel- und Totalpreisen
        6. Gesamtkalorien pro Menü

        Du darfst Zutaten ergänzen es müssen aber zwingend die Zutaten auf der Liste sein.

        Wichtig: Mach einen witzigen Hinweis bei Zutaten die nicht auf der VIP-Liste sind oder die nicht vegetarisch sind
        
        DATEN AUS DER APP:
        Was möchtest du essen?: {wünsche}
        Habe ich noch im Kühlschrank: {kuehlschrank}
        Ergänzende Zutaten müssen zwingend aus der VIP-Liste kommen: {', '.join(st.session_state.allowed_foods)}
        Mahlzeit: {mahlzeit_typ}
        Plan-Modus: {plan_art}
        Budget-Ziel: {budget} CHF
        Kalorien-Ziel: {kalorien}
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
    if st.button("👨‍🍳 Neues Menü würfeln", type="primary"):  # NEU
        st.session_state.last_response = None
        st.rerun()

# --- 5. VIP LISTE VERWALTUNG ---
st.markdown("---")
st.markdown('<p class="black-text">🛒 Diese Zutaten darf ich verwenden</p>', unsafe_allow_html=True)

neue_zutat = st.text_input("Zutat zur VIP-Liste hinzufügen:")
if st.button("Hinzufügen", type="primary"):  # NEU
    if neue_zutat and neue_zutat not in st.session_state.allowed_foods:
        st.session_state.allowed_foods.append(neue_zutat)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

for food in st.session_state.allowed_foods:
    # NEU: Chip-Optik (linke Pill) + X als rechte Pill-Kappe
    cols = st.columns([10, 1], gap="small")  # NEU
    cols[0].markdown(f"<div class='vip-chip-left'>{food}</div>", unsafe_allow_html=True)  # NEU
    with cols[1]:
        if st.button("✕", key=f"del_{food}", type="tertiary"):  # NEU
            st.session_state.allowed_foods.remove(food)
            st.rerun()





