import streamlit as st
import pandas as pd
import numpy as np

def search_combination(df, search_params):

    mask = pd.Series(True, index=df.index)
    for key, value in search_params.items():
        mask = mask & (df[key] == value)
    matching_rows = df[mask]
    
    if matching_rows.empty:
        return None

    rank = matching_rows.index[0]  # le meilleur résultat correspond à l'indice 0
    total = len(df)
    score_percentage = ((df.index.get_loc(rank) + 1) / total) * 100
    return score_percentage

def interpret_score(score):

    if score < 10:
        return "Excellente combinaison Yves. Vous êtes dans le top 10% des résultats, ce qui est remarquable. Si cette stratégie vous intéresse, c'est un très bon choix d'un point de vue stratégique."
    elif score < 25:
        return "Très bonne combinaison Yves. Vous êtes dans le top 25% des meilleurs choix à faire."
    elif score < 50:
        return "Bonne combinaison Yves. Vous êtes dans le top 50% des meilleurs choix stratégiques. Il est cependant possible de trouver mieux"
    else:
        return "Peut mieux faire Yves, nous vous déconseillons cette stratégie. Il existe de bien meilleures alternatives parmi les possibilités."


def compute_net_result(plan, nb_total, nb_reinsertion, nb_SE, nb_SE_reinsertion, ventes_SE, ventes_FS, effic_reinsertion):
    # (Votre fonction inchangée)
    rendement_exp = {"entieres": 100, "filets": 50}
    rendement_reinsertion = {
        "entieres": rendement_exp["entieres"] * effic_reinsertion / 100,
        "filets": rendement_exp["filets"] * effic_reinsertion / 100
    }
    
    nb_classiques = nb_total - nb_reinsertion
    nb_SE_classique = nb_SE - nb_SE_reinsertion
    nb_FS = nb_total - nb_SE
    nb_FS_reinsertion = nb_reinsertion - nb_SE_reinsertion
    nb_FS_classique = nb_FS - nb_FS_reinsertion

    if plan == 1:
        capacite_machine = 3000 * 0.8
        nb_conducteurs = 1
        nb_contremetres = 1
    else:
        capacite_machine = 1500 * 2 * 0.8
        nb_conducteurs = 2
        nb_contremetres = 2

    prod_SE_h = nb_SE_classique * rendement_exp["entieres"] + nb_SE_reinsertion * rendement_reinsertion["entieres"]
    prod_FS_h = nb_FS_classique * rendement_exp["filets"] + nb_FS_reinsertion * rendement_reinsertion["filets"]

    if prod_SE_h + prod_FS_h > capacite_machine:
        return None

    prod_SE_week = prod_SE_h * 35
    prod_FS_week = prod_FS_h * 35

    prod_SE_year = prod_SE_week * 46
    prod_FS_year = prod_FS_week * 46

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
    salaire_superviseur = 1500
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

    resultat_net = revenu_total - cout_variables - cout_fixes + subvention
    return resultat_net

@st.cache_data(show_spinner=False)
def run_optimization(nb_ouvriers):
    results = []
    combinations_count = 0
    for plan in [1]:
        for nb_total in range(10, nb_ouvriers+1):
            for nb_reinsertion in range(int(np.ceil(nb_total * 0.5)), nb_total + 1):
                for nb_SE in range(0, nb_total + 1):
                    min_SE_reinsertion = max(0, nb_SE - (nb_total - nb_reinsertion))
                    max_SE_reinsertion = min(nb_SE, nb_reinsertion)
                    for nb_SE_reinsertion in range(min_SE_reinsertion, max_SE_reinsertion + 1):
                        for ventes_SE in range(2000, 10001, 500):
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
                                    combinations_count += 1
        df_results = pd.DataFrame(results)
        df_best = df_results.sort_values(by="Résultat net annuel (€)", ascending=False).reset_index(drop=True)

        df_best["Total ventes"] = df_best["Ventes de sardines entières projetées"] + df_best["Ventes de filets projetées"]

        indices_a_garder = df_best.groupby("Résultat net annuel (€)")["Total ventes"].idxmin()

        df_best = df_best.loc[indices_a_garder].reset_index(drop=True)

        df_best.drop(columns="Total ventes", inplace=True)
        
        df_best = df_best.sort_values(by="Résultat net annuel (€)", ascending=False).reset_index(drop=True)


    return df_best, combinations_count

def main():
    st.set_page_config(page_title="GALETTE v1", layout="wide")
    
    col1, col2 = st.columns([0.9, 4])
    with col1:
        st.image("Kouign-removebg-preview.png")
    with col2:
        st.title("GALETTE v1 : notre algorithme d'optimisation du résultat net")
    
    st.markdown("#### (Generative Algorithm for Linear Estimation Toward Total Efficiency)")
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
    nb_ouvriers = st.slider("Nombre d'ouvriers maximal souhaité", 1, 40, 22)

    if st.button("Lancer l'optimisation"):
        with st.spinner("Optimisation en cours, merci de patienter..."):
            df_best, combinations_count = run_optimization(nb_ouvriers)
        st.success(f"Optimisation terminée ! {combinations_count} combinaisons analysées.")
        st.markdown("### Top 10 des combinaisons optimales")
        st.dataframe(df_best.head(10))
        
        # Sauvegarde dans st.session_state pour réutilisation
        st.session_state.df_best = df_best

    st.markdown("---")
    st.markdown("### Une idée de stratégie ? Evaluez son score de pertinence ici. ")
    if "df_best" in st.session_state:
        df_best = st.session_state.df_best
        # Pour chaque paramètre, on récupère les valeurs uniques existantes
        plans = sorted(df_best["Plan"].unique())
        nb_total_options = sorted(df_best["Nb total d'ouvriers"].unique())
        nb_reinsertion_options = sorted(df_best["Nb en reinsertion"].unique())
        nb_SE_options = sorted(df_best["Nb d'ouvriers sur les sardines entières"].unique())
        nb_SE_reinsertion_options = sorted(df_best["Nb d'ouvriers en reinsertion sur les sardines entières"].unique())
        ventes_SE_options = sorted(df_best["Ventes de sardines entières projetées"].unique())
        ventes_FS_options = sorted(df_best["Ventes de filets projetées"].unique())
        effic_options = sorted(df_best["Efficacité reinsertion (%)"].unique())
        
        with st.expander("Définir les paramètres de recherche"):
            search_plan = st.selectbox("Plan", plans)
            search_nb_total = st.selectbox("Nombre total d'ouvriers", nb_total_options)
            # On filtre nb_reinsertion pour que ce soit cohérent (>= 50% du total)
            reinsertion_min = int(np.ceil(search_nb_total * 0.5))
            reinsertion_valid = [val for val in nb_reinsertion_options if val >= reinsertion_min and val <= search_nb_total]
            search_nb_reinsertion = st.selectbox("Nombre d'ouvriers en réinsertion", reinsertion_valid)
            # Pour les sardines entières, on propose les valeurs disponibles
            search_nb_SE = st.selectbox("Nombre d'ouvriers sur les sardines entières", nb_SE_options)
            # On restreint nb_SE_reinsertion aux valeurs cohérentes
            valid_SE_reinsertion = [val for val in nb_SE_reinsertion_options if val <= search_nb_reinsertion and val <= search_nb_SE]
            search_nb_SE_reinsertion = st.selectbox("Nombre d'ouvriers en réinsertion sur les sardines entières", valid_SE_reinsertion)
            search_ventes_SE = st.selectbox("Ventes de sardines entières projetées", ventes_SE_options)
            search_ventes_FS = st.selectbox("Ventes de filets projetées", ventes_FS_options)
            search_effic = st.selectbox("Efficacité reinsertion (%)", effic_options)
            
            if st.button("Rechercher combinaison"):
                search_params = {
                    "Plan": search_plan,
                    "Nb total d'ouvriers": search_nb_total,
                    "Nb en reinsertion": search_nb_reinsertion,
                    "Nb d'ouvriers sur les sardines entières": search_nb_SE,
                    "Nb d'ouvriers en reinsertion sur les sardines entières": search_nb_SE_reinsertion,
                    "Ventes de sardines entières projetées": search_ventes_SE,
                    "Ventes de filets projetées": search_ventes_FS,
                    "Efficacité reinsertion (%)": search_effic,
                }
                score = search_combination(df_best, search_params)
                if score is None:
                    st.write("Aucune combinaison ne correspond exactement aux paramètres fournis.")
                else:
                    interpretation = interpret_score(score)
                    st.write(f"La combinaison se situe dans le top {score:.2f}% des résultats.")
                    st.write(interpretation)
    else:
        st.info("Lancez l'optimisation pour générer le DataFrame afin de calculer le score de votre choix de stratégie (avec le nombre d'ouvriers souhaité)")

    
    st.markdown("""
    <div style="color: lightgray; padding-top: 20px;">
        Powered by Python 3.13.2 64-bit © 2025 MASSAS GRATIOT HAMY. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
