import streamlit as st
import pandas as pd
import numpy as np
    
def compute_net_result(plan, nb_total, nb_reinsertion, nb_SE, nb_SE_reinsertion, ventes_SE, ventes_FS, effic_reinsertion):
    """
    Calcule le résultat net annuel à partir des paramètres.
    plan: 1 (grosse capacité) ou 2 (petite capacité)
    nb_total: nombre total d'ouvriers
    nb_reinsertion: nombre d'ouvriers en réinsertion (>= 50% du total)
    nb_SE: nombre d'ouvriers affectés aux sardines entières
    nb_SE_reinsertion: parmi nb_SE, ceux en réinsertion.
    ventes_SE: ventes journalières attendues pour sardines entières (boîtes)
    ventes_FS: ventes journalières attendues pour filets (boîtes)
    effic_reinsertion: pourcentage d’efficacité (entre 60 et 80)
    """
    # Paramètres fixes de rendement
    rendement_exp = {"entieres": 100, "filets": 50}
    rendement_reinsertion = {
        "entieres": rendement_exp["entieres"] * effic_reinsertion / 100,
        "filets": rendement_exp["filets"] * effic_reinsertion / 100
    }
    
    
    # Répartition du personnel
    nb_classiques = nb_total - nb_reinsertion
    nb_SE_classique = nb_SE - nb_SE_reinsertion
    nb_FS = nb_total - nb_SE
    nb_FS_reinsertion = nb_reinsertion - nb_SE_reinsertion
    nb_FS_classique = nb_FS - nb_FS_reinsertion

    # Capacité de la machine et effectifs fixes en production
    if plan == 1:
        capacite_machine = 3000 * 0.8  # boîtes/h
        nb_conducteurs = 1
        nb_contremetres = 1
    else:
        capacite_machine = 1500 * 2 * 0.8  # boîtes/h
        nb_conducteurs = 2
        nb_contremetres = 2

    # Production horaire (basée sur les ouvriers affectés aux deux lignes)
    prod_SE_h = nb_SE_classique * rendement_exp["entieres"] + nb_SE_reinsertion * rendement_reinsertion["entieres"]
    prod_FS_h = nb_FS_classique * rendement_exp["filets"] + nb_FS_reinsertion * rendement_reinsertion["filets"]

    # Evite goulot d'étranglement sur la machine
    if prod_SE_h + prod_FS_h > capacite_machine:
        return None  # solution non viable

    # Prod hebdomadaire (35 heures par semaine, 5j ouvrés)
    prod_SE_week = prod_SE_h * 35
    prod_FS_week = prod_FS_h * 35

    # Prod annuelle (46 semaines)
    prod_SE_year = prod_SE_week * 46
    prod_FS_year = prod_FS_week * 46

    # Limitation des ventes effectives
    annual_sales_SE = min(prod_SE_year, ventes_SE * 5 * 52)
    annual_sales_FS = min(prod_FS_year, ventes_FS * 5 * 52)

    prix_SE = 0.9
    prix_FS = 1.5
    cout_matiere_SE = 0.5
    cout_matiere_FS = 0.4
    
    revenu_total = annual_sales_SE * prix_SE + annual_sales_FS * prix_FS
    cout_matiere_total = prod_SE_year * cout_matiere_SE + prod_FS_year * cout_matiere_FS
    cout_expedition = (prod_SE_year + prod_FS_year) * 0.045
    cout_commission = 0.1 * revenu_total
    cout_variables = cout_matiere_total + cout_expedition + cout_commission

    subvention = nb_reinsertion * 7500

    salaire_Yves = 2500
    salaire_secretaire = 1500
    salaire_magasinier = 1200
    salaire_ouvrier = 1000
    salaire_superviseur = 1500  # pour contremaître et conducteur
    salaire_administration = 1500

    charges_patronales = 1.5

    salaire_total_mensuel = (
        nb_total * salaire_ouvrier +
        salaire_magasinier +
        nb_contremetres * salaire_superviseur +
        nb_conducteurs * salaire_superviseur +
        salaire_administration +
        salaire_Yves
    ) * charges_patronales

    cout_fixes = salaire_total_mensuel * 12 + 30000 + 36000 + 6000 + 2500 * 12 + 1000 * 12

    # Résultat net annuel
    resultat_net = revenu_total - cout_variables - cout_fixes + subvention

    return resultat_net

@st.cache_data(show_spinner=False)
def run_optimization(nb_ouvriers):
    results = []
    combinations_count = 0  # Compteur des combinaisons analysées
    for plan in [1, 2]:
        for nb_total in range(10, nb_ouvriers+1):  # de 10 à nb_ouvriers
            for nb_reinsertion in range(int(np.ceil(nb_total * 0.5)), nb_total + 1):
                for nb_SE in range(0, nb_total + 1):
                    min_SE_reinsertion = max(0, nb_SE - (nb_total - nb_reinsertion))
                    max_SE_reinsertion = min(nb_SE, nb_reinsertion)
                    for nb_SE_reinsertion in range(min_SE_reinsertion, max_SE_reinsertion + 1):
                        for ventes_SE in range(7000, 10001, 500):
                            for ventes_FS in range(2000, 5001, 500):
                                for effic in range(60, 81, 5):
                                    res = compute_net_result(
                                        plan, nb_total, nb_reinsertion, nb_SE, nb_SE_reinsertion,
                                        ventes_SE, ventes_FS, effic
                                    )
                                    if res is not None:
                                        results.append({
                                            "Plan": "Plan 1" if plan == 1 else "Plan 2",
                                            "Nb total d'ouvriers": nb_total,
                                            "Nb en reinsertion": nb_reinsertion,
                                            "Nb d'ouvriers sur les sardines entières": nb_SE,
                                            "Nb d'ouvriers en reinsertion sur les sardines entières": nb_SE_reinsertion,
                                            "Ventes de sardines entières projetées": ventes_SE,
                                            "Ventes de filets projetées": ventes_FS,
                                            "Efficacité reinsertion (%)": effic,
                                            "Résultat net annuel (€)": res
                                        })
                                    combinations_count += 1  # Incrémenter le compteur pour chaque combinaison analysée
    df_results = pd.DataFrame(results)
    df_best = df_results.sort_values(by="Résultat net annuel (€)", ascending=False).reset_index(drop=True)
    return df_best, combinations_count  # Retourner aussi le nombre de combinaisons analysées

def main():
    st.set_page_config(page_title="(KAMO) Kouign A'Metaheuristic Optimization", layout="wide")
    
    col1, col2 = st.columns([0.9, 4])

    with col1:
        st.image("Kouign-removebg-preview.png")

    with col2:
        st.title("GALETTES v1 : notre algorithme d'optimisation du résultat net")
    
    st.markdown("#### (Generative Algorithm for Linear Estimation Toward Total Efficiency & Success)",)
    st.write("")  
    st.write("")               
    st.write(
        """
        Détection et analyses des paramètres afin de maximiser le résultat net 
        de la société de M. Le Guellec. Les paramètres optimisés sont :
        - Choix du plan d'investissement (plan 1 vs plan 2)
        - Nombre d'ouvriers en réinsertion (minimum 50% du total)
        - Répartition des ouvriers aux sardines entières et filets
        - Ventes journalières prévues (sardines entières et filets)
        - Efficacité des ouvriers en réinsertion (entre 60% et 80%)
        """
    )
    
    st.title("Nombre d'ouvriers")
    nb_ouvriers = st.slider("Nombre d'ouvriers maximal souhaité", 1,40,22)


    if st.button("Lancer l'optimisation"):
        with st.spinner("Optimisation en cours, merci de patienter..."):
            df_best, combinations_count = run_optimization(nb_ouvriers)  # Récupère aussi le nombre de combinaisons
        st.success(f"Optimisation terminée ! {combinations_count} combinaisons analysées.")  # Affiche le nombre de combinaisons
        st.markdown("### Top 10 des combinaisons optimales")
        st.dataframe(df_best.head(10))
        st.markdown("### Top 100")
        st.dataframe(df_best.head(100)) 


    st.markdown("""
    <div style="color: lightgray; padding-top: 20px;">
        Powered by Python 3.13.2 64-bit © 2025 MASSAS GRATIOT HAMY. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()
