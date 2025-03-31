import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Dashboard", layout="wide", page_icon="🐟")

# Personnalisation du style
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

# Titre de la page
st.title("Welcome Yves ! 🐟")

# Textes avec descriptions
st.write("Rendez-vous sur la page **Analytique**, pour étudier l'influence des choix stratégiques sur vos résultats financiers et autres KPIs")
st.write("Rendez-vous sur la page **Kouign'optimisation**, pour générer le scénario optimal vous garantissant des résultats maximaux sur vos résultats financiers et autres KPIs")
st.write("Rendez-vous sur la page **Marketing**, pour estimer l'influence de vos investissements marketing sur vos ventes")

# Ajouter une image animée sur le thème de la mer (exemple d'une sardine nageant)
st.image("https://cdna.artstation.com/p/assets/images/images/040/550/526/original/tt_art-sardine-swim2-2.gif?1629201172", 
         use_container_width=True)

# Ajouter un fond d'écran de la mer pour une ambiance plus immersive
st.markdown("""
    <style>
    .main {
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/ec/Ocean_view%2C_Tamborine_Mountain.jpg');
        background-size: cover;
        background-position: center;
    }
    </style>
""", unsafe_allow_html=True)
