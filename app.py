import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide", page_icon="🐟")

st.markdown("""
    <style>
    body {
        background-color: #f0f8ff;  /* Couleur bleu clair (océan) */
        color: #2e8b57;  /* Couleur vert mer */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1 {
        color: #006994;  /* Bleu profond pour le titre */
    }
    h2 {
        color: #2e8b57;  /* Couleur vert pour les sous-titres */
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stMarkdown p {
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Welcome Yves ! 🐟")

st.write("Rendez-vous sur la page **Analyses de données**, pour étudier l'influence des choix stratégiques sur vos résultats financiers et autres KPIs")
st.write("Rendez-vous sur la page **GALETTES v1**, pour générer le scénario optimal vous garantissant des résultats maximaux sur vos résultats financiers et autres KPIs")

st.image("https://cdna.artstation.com/p/assets/images/images/040/550/526/original/tt_art-sardine-swim2-2.gif?1629201172", 
         use_container_width=True)

st.markdown("""
    <style>
    .main {
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/ec/Ocean_view%2C_Tamborine_Mountain.jpg');
        background-size: cover;
        background-position: center;
    }
    </style>
""", unsafe_allow_html=True)
