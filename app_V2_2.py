import streamlit as st

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Formula 1 Telemetry",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Language state
# --------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "Français"

# --------------------------------------------------
# TOP BAR (layout-based, NOT CSS)
# --------------------------------------------------
top_left, top_spacer, top_right = st.columns([6, 1, 2])

with top_right:
    st.selectbox(
        "Language",
        ["Français", "English"],
        key="lang",
        label_visibility="collapsed"
    )

# --------------------------------------------------
# Force rerun on language change
# --------------------------------------------------
if st.session_state.get("_last_lang") != st.session_state.lang:
    st.session_state["_last_lang"] = st.session_state.lang
    st.rerun()

# --------------------------------------------------
# Page labels
# --------------------------------------------------
PAGE_LABELS = {
    "Français": {
        "home": "Accueil",
        "telemetry": "Télémétrie",
        "info": "Informations"
    },
    "English": {
        "home": "Home",
        "telemetry": "Telemetry",
        "info": "Informations"
    }
}

labels = PAGE_LABELS[st.session_state.lang]

# --------------------------------------------------
# Home page
# --------------------------------------------------
def home():
    translations = {
        "Français": {
            "title": "Bienvenue sur mon application de télémétrie",
            "subtitle": "Ceci est la page principale.",
            "telemetry": "Pour accéder à la télémétrie, cliquez sur « Telemetrie » dans la barre latérale.",
            "info": "Pour obtenir des informations, cliquez sur « Informations » dans la barre latérale."
        },
        "English": {
            "title": "Welcome to my telemetry application",
            "subtitle": "This is the main page.",
            "telemetry": "To access telemetry, click on « Telemetry » in the sidebar.",
            "info": "To get information, click on « Informations » in the sidebar."
        }
    }

    t = translations[st.session_state.lang]

    st.title(t["title"])
    st.write(t["subtitle"])
    st.info(f"{t['telemetry']}\n\n{t['info']}")

# --------------------------------------------------
# Navigation (translated)
# --------------------------------------------------
home_page = st.Page(home, title=labels["home"],  default=True)
telemetry_page = st.Page("pages/1_Telemetry.py", title=labels["telemetry"],)
info_page = st.Page("pages/2_info.py", title=labels["info"])

st.navigation([home_page, telemetry_page, info_page]).run()
