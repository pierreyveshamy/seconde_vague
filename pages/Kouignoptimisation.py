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

    # Contrainte : éviter le goulot d'étranglement sur la machine
    if prod_SE_h + prod_FS_h > capacite_machine:
        return None  # solution non viable

    # Production hebdomadaire (35 heures par semaine, 5 jours ouvrés)
    prod_SE_week = prod_SE_h * 35
    prod_FS_week = prod_FS_h * 35

    # Production annuelle (46 semaines)
    prod_SE_year = prod_SE_week * 46
    prod_FS_year = prod_FS_week * 46

    # Limitation des ventes effectives
    annual_sales_SE = min(prod_SE_year, ventes_SE * 5 * 52)
    annual_sales_FS = min(prod_FS_year, ventes_FS * 5 * 52)

    # Tarifs et coûts matières
    prix_SE = 0.9
    prix_FS = 1.5
    cout_matiere_SE = 0.5
    cout_matiere_FS = 0.4

    # Calcul des revenus et des coûts
    revenu_total = annual_sales_SE * prix_SE + annual_sales_FS * prix_FS
    cout_matiere_total = prod_SE_year * cout_matiere_SE + prod_FS_year * cout_matiere_FS
    cout_expedition = (prod_SE_year + prod_FS_year) * 0.045
    cout_commission = 0.1 * revenu_total
    cout_variables = cout_matiere_total + cout_expedition + cout_commission

    # Subventions (7 500€ par an et par ouvrier en réinsertion)
    subvention = nb_reinsertion * 7500

    # Calcul des coûts fixes (salaires + loyers, électricité, etc.)
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
def run_optimization():
    results = []
    # Parcours des plages discrètes pour l'exploration
    for plan in [1, 2]:
        for nb_total in range(10, 41):  # de 10 à 40 ouvriers
            # contrainte: au moins 50% en réinsertion
            for nb_reinsertion in range(int(np.ceil(nb_total * 0.5)), nb_total + 1):
                for nb_SE in range(0, nb_total + 1):
                    # Pour nb_SE_reinsertion, bornes minimales et maximales
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
                                            "Nb_total": nb_total,
                                            "Nb_reinsertion": nb_reinsertion,
                                            "Nb_SE": nb_SE,
                                            "Nb_SE_reinsertion": nb_SE_reinsertion,
                                            "Ventes_SE": ventes_SE,
                                            "Ventes_FS": ventes_FS,
                                            "Efficacité_reinsertion (%)": effic,
                                            "Résultat_net (€)": res
                                        })
    df_results = pd.DataFrame(results)
    df_best = df_results.sort_values(by="Résultat_net (€)", ascending=False).reset_index(drop=True)
    return df_best

def main():
    st.set_page_config(page_title="(KAMO) Kouign A'Metaheuristic Optimization", layout="wide")
    st.title("Kouign'optimisation du résultat net")
    st.write(
        """
        Détection et analyses des paramètres afin de maximiser le résultat net 
        de la société de M. Le Guellec. Les paramètres optimisés sont :
        - Choix du plan d'investissement (Plan 1 ou Plan 2)
        - Nombre total d'ouvriers
        - Nombre d'ouvriers en réinsertion (minimum 50% du total)
        - Répartition des ouvriers aux sardines entières et filets
        - Ventes journalières prévues (sardines entières et filets)
        - Efficacité des ouvriers en réinsertion (entre 60% et 80%)
        """
    )

    if st.button("Lancer l'optimisation"):
        with st.spinner("Optimisation en cours, merci de patienter..."):
            df_best = run_optimization()
        st.success("Optimisation terminée !")
        st.markdown("### Top 10 des combinaisons optimales")
        st.dataframe(df_best.head(10))
        st.markdown("### Top 50")
        st.dataframe(df_best.head(300))  # Affiche seulement les 50 meilleures solutions


if __name__ == "__main__":
    main()
