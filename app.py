import streamlit as st
from openai import OpenAI

# --- 1. DESIGN & HARMONISIERUNG (CSS) ---
st.set_page_config(page_title="Sophis Veggie APP", page_icon="🥦", layout="centered")

st.markdown("""
    <style>
    /* Hintergrund */
    .stApp { background-color: #f4f4f4; }
    
    /* UNIFORME ÜBERSCHRIFTEN (Labels) */
    .stApp label p, .stApp h2, .stApp h3, p { 
        color: #31333F !important; 
        font-family: 'Inter', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        margin-bottom: 5px !important;
    }
    
    /* TITEL: DOPPELT SO GROSS & OHNE SYMBOL */
    h1 { 
        font-size: 4.5rem !important; /* Doppelt so groß wie vorher */
        color: #722F37 !important; 
        text-align: center !important;
        margin-bottom: 30px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
    }

    /* UNIFORME SCHWARZE FELDER (Inputs) */
    .stTextArea textarea, .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
        background-color: #31333F !important;
        color: white !important;
        border: 2px solid #722F37 !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        padding: 10px !important;
    }

    /* FIX: AUSGEWÄHLTE MAHLZEIT IN WEISS */
    div[data-baseweb="select"] span, 
    div[data-baseweb="select"] div[aria-selected="true"],
    div[data-baseweb="select"] div {
        color: white !important;
        font-size: 1rem !important;
    }

    /* Radio-Buttons (Plan-Modus) */
    div[role="radiogroup"] {
        background-color: #31333F;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #722F37;
        color: white !important;
    }
    div[role="radiogroup"] label p { color: white !important; font-size: 0.95rem !important; }

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
        margin-top: 20px;
    }
    
    /* Kompakte Karten unten */
    .small-food-card {
        background: white;
        padding: 5px 10px;
        border-radius: 6px;
        border-left: 3px solid #722F37;
        margin-bottom: 3px;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DEINE ERLAUBTE LISTE ---
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
# Titel jetzt ohne Emoji und über CSS vergrößert
st.markdown("<h1>Sophis Veggie APP</h1>", unsafe_allow_html=True)

with st.container():
    wünsche = st.text_area("Was möchtest du essen?", placeholder="z.B. Nudeln...")
    kuehlschrank = st.text_area("Habe ich noch im Kühlschrank:", placeholder="z.B. Zuccini...")
    
    col

