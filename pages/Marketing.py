import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Paramètres basés sur des entreprises similaires comme La Belle Iloise (à moindre échelle)
a_entieres, b_entieres, c_entieres = 12000, 0.75, 60000  # Sardines entières
a_filets, b_filets, c_filets = 6000, 0.75, 30000  # Filets

def ventes_estimees(investissement):
    """
    Estime le nombre de boîtes vendues en fonction de l'investissement marketing.
    Modèle en S : Ventes = (a * Investissement^b) / (c + Investissement^b)
    """
    ventes_entieres = (a_entieres * investissement**b_entieres) / (c_entieres + investissement**b_entieres)
    ventes_filets = (a_filets * investissement**b_filets) / (c_filets + investissement**b_filets)
    
    return int(ventes_entieres), int(ventes_filets)

# Interface Streamlit
st.title("Estimation des ventes en fct° de l'investissement marketing")

investissement = st.number_input("Entrez le montant de l'investissement marketing en euros :", min_value=0.0, step=500.0)

if investissement > 0:
    ventes_entieres, ventes_filets = ventes_estimees(investissement)
    
    st.write(f"Avec un investissement de {investissement:.2f} euros :")
    st.write(f" - Ventes estimées de sardines entières : {ventes_entieres} boîtes/jour")
    st.write(f" - Ventes estimées de filets de sardines : {ventes_filets} boîtes/jour")
    
    # Graphique interactif
    fig, ax = plt.subplots()
    categories = ["Sardines Entières", "Filets de Sardines"]
    ventes = [ventes_entieres, ventes_filets]
    ax.bar(categories, ventes, color=["blue", "green"])
    ax.set_ylabel("Nombre de boîtes vendues/jour")
    ax.set_title("Impact de l'investissement sur les ventes")
    st.pyplot(fig)

# Graphique statique montrant la relation entre investissement et ventes
investissements = np.linspace(0, 100000, 100)
ventes_entieres_curve = [(a_entieres * i**b_entieres) / (c_entieres + i**b_entieres) for i in investissements]
ventes_filets_curve = [(a_filets * i**b_filets) / (c_filets + i**b_filets) for i in investissements]

fig_static, ax_static = plt.subplots()
ax_static.plot(investissements, ventes_entieres_curve, label="Sardines entières", color="blue")
ax_static.plot(investissements, ventes_filets_curve, label="Filets de sardines", color="green")
ax_static.set_xlabel("Investissement marketing (euros)")
ax_static.set_ylabel("Nombre de boîtes vendues/jour")
ax_static.set_title("Relation investissement marketing - ventes, marché de la sardine en conserve haut de gamme")
ax_static.legend()
st.markdown("""
    <div style="color: gray; padding-top: 5px; padding-bottom: 5px">
        Projections obtenues à partir de l'analyse des investissements marketing de trois autres conserveries bretonnes haut de gamme de taille différentes : La Belle-Iloise, Conserverie Courtin et Conserverie Kerné.
    </div>
    """, unsafe_allow_html=True)
st.pyplot(fig_static)
