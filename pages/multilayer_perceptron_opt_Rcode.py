import numpy as np
import pandas as pd
import streamlit as st

# Définir le mot de passe (à remplacer par votre propre mot de passe)
PASSWORD = "mdp"

# Demander à l'utilisateur de saisir un mot de passe
user_password = st.text_input("Entrez le token d'administration pour accéder à cette page :", type="password")

# Vérifier si le mot de passe saisi est correct
if user_password == PASSWORD:
    st.success("vérifié")
    
    # Contenu de la page protégée
    st.title("Page protégée")
    
    
    # Paramètres fixes (à adapter si nécessaire)
    heures_semaine = 35
    semaines_an = 46
    rendement_exp = {"entieres": 100, "filets": 50}
    # Efficacité des ouvriers en réinsertion (en %)
    efficacite_reinsertion = 70
    rendement_reinsertion = {
        "entieres": rendement_exp["entieres"] * efficacite_reinsertion / 100,
        "filets": rendement_exp["filets"] * efficacite_reinsertion / 100,
    }
    # Tarifications et coûts matières
    prix_vente = {"entieres": 0.9, "filets": 1.5}
    cout_matiere = {"entieres": 0.5, "filets": 0.4}
    # Prévisions de ventes journalières
    ventes_entieres = 8500
    ventes_filets = 3500

    # Autres paramètres de coûts
    cout_expédition = 0.045
    cout_commission = 0.1
    # Frais fixes (hors salaires et amortissements) en €/an
    loyer_usine = 30000
    autres_charges = 36000 + 6000 + 2500 * 12 + 1000 * 12

    # Salaires mensuels hors charges patronales
    salaire = {
        "Yves": 2500,
        "secretaire": 1500,
        "magasinier": 1200,
        "ouvrier": 1000,
        "contremaitre": 1500,
        "conducteur": 1500,
    }
    charges_patronales = 1.5  # Charges = 50% du salaire

    # Subvention réinsertion par ouvrier réinsertion (€/an)
    subvention_reinsertion = 7500

    # Définition de deux plans d'investissement
    # Pour plan 1 (machine grosse capacité)
    plan1 = {
        "capacite_machine": 3000 * 0.8,  # boîtes/h
        "nb_conducteurs": 1,
        "nb_contremetres": 1,
        "investissement": 180000 + 30000  # simplifié
    }
    # Pour plan 2 (machines petite capacité, double équipe)
    plan2 = {
        "capacite_machine": 1500 * 2 * 0.8,  # boîtes/h
        "nb_conducteurs": 2,
        "nb_contremetres": 2,
        "investissement": 50000 + 40000 + 30000  # simplifié
    }

    # Fonction de calcul du résultat net pour une configuration donnée
    def calcul_resultat_net(plan, nb_ouvriers, nb_ouvriers_reinsertion, nb_ouvriers_SE, nb_ouvriers_SE_reinsertion):
        """
        nb_ouvriers : total ouvriers
        nb_ouvriers_reinsertion : nombre d'ouvriers en réinsertion (>=50% du total)
        nb_ouvriers_SE : ouvriers affectés aux sardines entières
        nb_ouvriers_SE_reinsertion : parmi les ouvriers affectés aux sardines entières, ceux en réinsertion
        Les autres ouvriers (nb_ouvriers - nb_ouvriers_SE) travailleront sur les filets.
        """
        # Répartition des ouvriers en production classique et en réinsertion
        nb_ouvriers_SE_classique = nb_ouvriers_SE - nb_ouvriers_SE_reinsertion
        nb_ouvriers_FS = nb_ouvriers - nb_ouvriers_SE
        nb_ouvriers_FS_reinsertion = nb_ouvriers_reinsertion - nb_ouvriers_SE_reinsertion
        nb_ouvriers_FS_classique = nb_ouvriers_FS - nb_ouvriers_FS_reinsertion
        
        # Calcul de la production par heure (selon affectation)
        prod_entieres_heure = nb_ouvriers_SE_classique * rendement_exp["entieres"] \
            + nb_ouvriers_SE_reinsertion * rendement_reinsertion["entieres"]
        prod_filets_heure = nb_ouvriers_FS_classique * rendement_exp["filets"] \
            + nb_ouvriers_FS_reinsertion * rendement_reinsertion["filets"]
        
        # Vérification de la contrainte de débit machine (en boîtes/h)
        debit_entree = prod_entieres_heure + prod_filets_heure
        if debit_entree > plan["capacite_machine"]:
            return None  # Non admissible : goulot d'étranglement
        
        # Production hebdomadaire et annuelle (en boîtes)
        prod_entieres_hebdo = prod_entieres_heure * heures_semaine
        prod_filets_hebdo = prod_filets_heure * heures_semaine
        
        prod_entieres_an = prod_entieres_hebdo * semaines_an
        prod_filets_an = prod_filets_hebdo * semaines_an
        
        # On ne peut vendre que le minimum entre production et demande (en considérant 5 jours ouvrables par semaine et 52 semaines)
        vente_entieres_an = min(prod_entieres_an, ventes_entieres * 52 * 5)
        vente_filets_an = min(prod_filets_an, ventes_filets * 52 * 5)
        
        # Chiffre d'affaires annuel
        ca_total = vente_entieres_an * prix_vente["entieres"] + vente_filets_an * prix_vente["filets"]
        
        # Coûts matières annuels
        cout_matieres = prod_entieres_an * cout_matiere["entieres"] + prod_filets_an * cout_matiere["filets"]
        
        # Autres coûts variables
        couts_variables = (prod_entieres_an + prod_filets_an) * cout_expédition + cout_commission * ca_total
        
        # Marge brute
        marge_brute = ca_total - cout_matieres
        
        # Coûts fixes (salaires, loyer, autres charges)
        # Salaires : Yves, secrétaire, magasinier, ouvriers, contremaîtres et conducteurs
        salaire_total_mensuel = (salaire["Yves"] + salaire["secretaire"] + salaire["magasinier"] +
                                nb_ouvriers * salaire["ouvrier"] +
                                plan["nb_contremetres"] * salaire["contremaitre"] +
                                plan["nb_conducteurs"] * salaire["conducteur"]) * charges_patronales
        cout_salaires_annuel = salaire_total_mensuel * 12
        cout_fixes = cout_salaires_annuel + loyer_usine + autres_charges
        # On néglige ici l'amortissement pour le calcul simplifié du résultat net
        # Ajout des subventions en réinsertion
        subventions = nb_ouvriers_reinsertion * subvention_reinsertion
        
        resultat_net = ca_total - (couts_variables + cout_fixes) + subventions
        
        return resultat_net

    # Recherche par grille sur une plage de paramètres
    resultats = []
    # On parcourt le plan 1 et le plan 2
    for plan_name, plan in zip(["Plan 1", "Plan 2"], [plan1, plan2]):
        # Nombre total d'ouvriers de 10 à 40
        for nb_ouvriers in range(10, 41):
            # Contrainte : au moins 50 % en réinsertion
            nb_min_reinsertion = int(np.ceil(nb_ouvriers * 0.5))
            for nb_ouvriers_reinsertion in range(nb_min_reinsertion, nb_ouvriers+1):
                # Affectation des ouvriers aux sardines entières : de 0 à nb_ouvriers
                for nb_ouvriers_SE in range(0, nb_ouvriers+1):
                    # nb_ouvriers_SE_reinsertion doit être entre max(0, nb_ouvriers_SE - (nb_ouvriers - nb_ouvriers_reinsertion)) et min(nb_ouvriers_SE, nb_ouvriers_reinsertion)
                    min_SE_reinsertion = max(0, nb_ouvriers_SE - (nb_ouvriers - nb_ouvriers_reinsertion))
                    max_SE_reinsertion = min(nb_ouvriers_SE, nb_ouvriers_reinsertion)
                    for nb_ouvriers_SE_reinsertion in range(min_SE_reinsertion, max_SE_reinsertion+1):
                        net = calcul_resultat_net(plan, nb_ouvriers, nb_ouvriers_reinsertion, nb_ouvriers_SE, nb_ouvriers_SE_reinsertion)
                        if net is not None:
                            resultats.append({
                                "Plan": plan_name,
                                "Total ouvriers": nb_ouvriers,
                                "Ouvriers réinsertion": nb_ouvriers_reinsertion,
                                "Ouvriers SE": nb_ouvriers_SE,
                                "Ouvriers SE réinsertion": nb_ouvriers_SE_reinsertion,
                                "Résultat net": net
                            })

    # Conversion des résultats en DataFrame
    df_resultats = pd.DataFrame(resultats)
    # Sélection de la/les configuration(s) offrant le meilleur résultat net
    best_result = df_resultats.loc[df_resultats["Résultat net"].idxmax()]


    # Affichage du meilleur résultat avec un cadre coloré
    st.markdown("## 🏆 Meilleure configuration détectée par notre logiciel Kouign a'Machine Learning :")
    st.success(f"**Plan :** {best_result['Plan']}")
    st.dataframe(best_result.to_frame().T)  # Affichage formaté en tableau
    st.write("### Détails :")

    # Affichage du top 10 avec mise en forme
    st.markdown("## 📊 Top 10 des configurations (par résultat net décroissant) :")
    st.dataframe(df_resultats.sort_values("Résultat net", ascending=False).head(10))

        
        
    # Vous pouvez ajouter d'autres éléments ou fonctionnalités ici
else:
    if user_password != "":
        st.error("Mot de passe incorrect. Veuillez réessayer.")
