import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import graphviz

def main():
    st.set_page_config(page_title="Tableau de bord stratégique - Yves Le Quellec", layout="wide")

    
    col1, col2, col3 = st.columns([1.1, 4,  1])

    with col1:
        st.image("Kouign-removebg-preview.png")
    
    with col2:
        st.title("Tableau de bord stratégique")
        st.markdown("### Kouign a'Management pour Yves Le Quellec")
    
    with col3:
        st.image("tt-art-sardine-swim2-2-2-unscreen.gif")
        
 
        
    st.sidebar.header("PARAMETRES STRATEGIQUES")
    
    
    # Sélection du plan d’investissement
    plan = st.sidebar.radio("Choix du plan d’investissement", ("Plan 1 : machine grosse capacité", "Plan 2 : machines petite capacité"))
        
    # Catégorie : Ajustement du personnel
    st.sidebar.subheader("AJUSTEMENT DES OUVRIERS")
    nb_ouvriers = st.sidebar.slider("Nombre ouvriers total", 1, 40, 22)
    nb_ouvriers_reinsertion = st.sidebar.slider("Nombre ouvriers en réinsertion", 0, nb_ouvriers, 11, key="ouvriers_reinsertion")
    efficacite_reinsertion = st.sidebar.slider("Efficacité des ouvriers en réinsertion (%)", 60, 100, 70, key="efficacite_reinsertion")

    nb_ouvriers_SE = st.sidebar.slider("Nombre d'ouvriers aux sardines entières", 0, nb_ouvriers, 11)


        # Assurer que min_nb_ouvriers_SE_reinsertion est toujours ≥ 0
    min_nb_ouvriers_SE_reinsertion = max(0, nb_ouvriers_SE - (nb_ouvriers - nb_ouvriers_reinsertion))

    # Assurer que la valeur maximale ne dépasse pas les contraintes
    max_nb_ouvriers_SE_reinsertion = min(nb_ouvriers_reinsertion, nb_ouvriers_SE)

    # Vérifier que les limites sont cohérentes
    if min_nb_ouvriers_SE_reinsertion > max_nb_ouvriers_SE_reinsertion:
        min_nb_ouvriers_SE_reinsertion = max_nb_ouvriers_SE_reinsertion

     # Vérification pour éviter l'erreur
    if min_nb_ouvriers_SE_reinsertion == max_nb_ouvriers_SE_reinsertion:
        nb_ouvriers_SE_reinsertion = min_nb_ouvriers_SE_reinsertion
    else:
        nb_ouvriers_SE_reinsertion = st.sidebar.slider(
            "Nombre d'ouvriers en réinsertion aux sardines entières",
            min_nb_ouvriers_SE_reinsertion, max_nb_ouvriers_SE_reinsertion
        )
        
    rendement_exp = {"entieres": 100, "filets": 50}  
    
    if plan == "Plan 1 : machine grosse capacité":
        capacite_machine = 3000 * 0.8
        nb_conducteurs = 1
        nb_contremetres = 1
    else:
        capacite_machine = 1500 * 2 * 0.8
        nb_conducteurs = 2
        nb_contremetres = 2

    eff_total = 3 + nb_ouvriers + nb_contremetres + nb_conducteurs
    
    st.sidebar.subheader("TARIFICATIONS PRODUITS")
    prix_entieres = st.sidebar.slider("Prix de vente - Sardines entières", 0.0, 2.0, 0.9, step=0.1)
    prix_filets = st.sidebar.slider("Prix de vente - Sardines filets", 0.0, 3.0, 1.5,step=0.1)
    
    prix_vente = {"entieres": prix_entieres, "filets": prix_filets}
    cout_matiere = {"entieres": 0.5, "filets": 0.4}  
    
    # Catégorie : Ventes
    st.sidebar.subheader("PREVISIONS DES VENTES")
    ventes_entieres = st.sidebar.slider("Ventes journalières - Sardines entières", 7000, 10000, 8500, key="ventes_entieres")
    ventes_filets = st.sidebar.slider("Ventes journalières - Filets de sardines", 2000, 5000, 3500, key="ventes_filets")
    

    # Catégorie : Rendement et efficacité
    rendement_reinsertion = {"entieres": rendement_exp["entieres"] * efficacite_reinsertion/100, "filets": rendement_exp["filets"] * efficacite_reinsertion/100} 
    
    nb_ouvriers_exp = nb_ouvriers - nb_ouvriers_reinsertion

    
    nb_ouvriers_FS = max(0, nb_ouvriers - nb_ouvriers_SE)
    nb_ouvriers_FS_reinsertion = max(0, nb_ouvriers_reinsertion - nb_ouvriers_SE_reinsertion)
    nb_ouvriers_FS = max(0,nb_ouvriers - nb_ouvriers_SE)
    nb_ouvriers_FS_reinsertion = max(0,nb_ouvriers_reinsertion - nb_ouvriers_SE_reinsertion)

    nb_ouvriers_FS_classique = nb_ouvriers_FS - nb_ouvriers_FS_reinsertion
    nb_ouvriers_SE_classique = nb_ouvriers_SE - nb_ouvriers_SE_reinsertion
   
    
    # Production estimée
    prod_entieres_heure = ((nb_ouvriers_SE_classique) * rendement_exp["entieres"] + nb_ouvriers_SE_reinsertion * rendement_reinsertion["entieres"])
    prod_filets_heure = ((nb_ouvriers_FS_classique) * rendement_exp["filets"] + nb_ouvriers_FS_reinsertion * rendement_reinsertion["filets"])
    
    prod_entieres_hebdo = prod_entieres_heure * 35 #On prend en compte 35h et non 32h (0.8 machine) car le goulot d'étranglement se situe sur la production des ouvriers.
    prod_filets_hebdo = prod_filets_heure * 35
  
    prod_entieres_annee = prod_entieres_hebdo * 46 
    prod_filets_annee = prod_filets_hebdo * 46

    st.markdown("## Répartition des ouvriers")
    df_prod = pd.DataFrame({
        "Affectation": ["Ouvriers classiques - sardines entières", "Ouvriers classiques - filets", "Ouvriers en réinsertion - sardines entières", "Ouvriers en réinsertion - filets"],
        "Effectif": [nb_ouvriers_SE_classique, nb_ouvriers_FS_classique, nb_ouvriers_SE_reinsertion, nb_ouvriers_FS_reinsertion]
    })
    st.table(df_prod)

    st.markdown("## KPIs production")
    
    # Vérification de la SURPRODUCTION et sous-production
    surprod_SE_hebdo = prod_entieres_hebdo - ventes_entieres * 5
    surprod_FS_hebdo = prod_filets_hebdo - ventes_filets * 5

    sousprod_SE_hebdo = -surprod_SE_hebdo if surprod_SE_hebdo < 0 else 0
    sousprod_FS_hebdo = -surprod_FS_hebdo if surprod_FS_hebdo < 0 else 0

    # Vérification d'équilibre prod-vente

    statut_SE = "Équilibre atteint" if surprod_SE_hebdo == 0 else ("SOUS-PRODUCTION, ne rép. pas à la demande estimée" if sousprod_SE_hebdo > 0 else "SURPRODUCTION, dépasse les obj. de ventes")
    statut_FS = "Équilibre atteint" if surprod_FS_hebdo == 0 else ("SOUS-PRODUCTION, ne rép. pas à la demande estimée" if sousprod_FS_hebdo > 0 else "SURPRODUCTION, dépasse les obj. de ventes")

    # Calcul du pourcentage d'ajustement
    
        # Calcul de l'ajustement
    if prod_entieres_hebdo == 0:
        ajustement_SE = 0 # Ou bien tu peux afficher un message ou gérer autrement
    else:
        ajustement_SE = ((ventes_entieres * 5 - prod_entieres_hebdo) / prod_entieres_hebdo) * 100

        # Calcul de l'ajustement
    if prod_filets_hebdo == 0:
        ajustement_FS = 0  # Ou bien tu peux afficher un message ou gérer autrement
    else:
        ajustement_FS = ((ventes_filets * 5 - prod_filets_hebdo) / prod_filets_hebdo) * 100

    def ajouter_fleche(val):
        if val > 0:
            return f"{val:+.1f}% ↑"  
        elif val < 0:
            return f"{val:+.1f}% ↓"  
        else:
            return f"{val:+.1f}% =" 

    # Application de la fonction aux ajustements
    ajustement_SE = ajouter_fleche(ajustement_SE)
    ajustement_FS = ajouter_fleche(ajustement_FS)

    # Création du DataFrame
    df_prod = pd.DataFrame({
        "Indicateur": ["Sardines entières", "Filets de sardines"],
        "Production hebdomadaire (5j ouvrés)": [f"{int(prod_entieres_hebdo):,} boîtes", f"{int(prod_filets_hebdo):,} boîtes"],
        "Statut": [statut_SE, statut_FS],
        "Ajustement nécessaire": [ajustement_SE, ajustement_FS]
    })

    # Fonction de mise en forme conditionnelle
    def color_surprod(val):
        if "SOUS-PRODUCTION, ne rép. pas à la demande estimée" in val:  # Sous-production → Rouge FF7F7F
            return "background-color: #FF7F7F; color: black; font-weight: bold"
        elif "SURPRODUCTION, dépasse les obj. de ventes" in val:  # Surproduction → Vert 90EE90
            return "background-color: #FFFF99; color: black; font-weight: bold"
        elif "Équilibre atteint" in val:  # Équilibre → Jaune FFFF99
            return "background-color: #90EE90; color: black; font-weight: bold"
        return ""
        
    # Affichage du tableau avec mise en forme
    st.dataframe(df_prod.style.applymap(color_surprod, subset=["Statut"]))
    
    def draw_process(sardine_rate, filet_rate, machine_rate, autoclave_rate):
        dot = graphviz.Digraph(graph_attr={'splines': 'ortho'})
        
        # Noeuds
        dot.node('A', 'Préparation des Sardines Entières', shape='box', fillcolor="yellow")
        dot.node('B', 'Préparation des Filets', shape='box', fillcolor="yellow")
        dot.node('S','Σ', shape='box', fillcolor="grey")
        
        if plan == "Plan 1 : machine grosse capacité":
            dot.node('C', 'Machine grosse capacité', shape='box')
            dot.node('D', 'Autoclave grosse capacité', shape='box')
        else:
            dot.node('C', '2 machines petite capacité', shape='box')
            dot.node('D', '2 autoclaves petite capacité', shape='box')
            
        dot.node('E', 'Stockage, prêt à être expédié', shape='box')

        # Calcul du débit à l'entrée de la machine et du débit de sortie
        entry_rate = sardine_rate + filet_rate  # Débit entrant
        exit_rate = machine_rate  # Débit sortant
        
        # Ajouter l'alerte si le débit à l'entrée est plus élevé que le débit de sortie
        if entry_rate > exit_rate:
            st.warning("Attention, risque d'accumulation de sardines en amont de la mise en boîtes!")
            # Optionnel : mettre en évidence les arêtes concernées
            dot.edge('S', 'C', label=f'{entry_rate} éq. boîtes/h', color="red", penwidth="2")  # Flèche en rouge

        else:
            dot.edge('S', 'C', label=f'{entry_rate} éq. boîtes/h')

        # Arêtes avec débits dynamiques
        dot.edge('A', 'S', label=f'{sardine_rate} éq. boîtes/h')
        dot.edge('B', 'S', label=f'{filet_rate} éq. boîtes/h')
        dot.edge('C', 'D', label=f'{machine_rate} boîtes non fermées/h au max')
        dot.edge('D', 'E', label=f'{autoclave_rate} boîtes finies/h au max')

        return dot

    # Titre et génération du diagramme
    st.title("Flux de production")
    flow_chart = draw_process(prod_entieres_heure, prod_filets_heure, capacite_machine, capacite_machine)
    st.graphviz_chart(flow_chart)
        


    revenu_total_annuel = min(prod_entieres_annee,ventes_entieres*52*5) * prix_vente["entieres"] + min(prod_filets_annee,ventes_filets*52*5) * prix_vente["filets"]
    cout_matieres_total_annuel = prod_entieres_annee * cout_matiere["entieres"] + prod_filets_annee * cout_matiere["filets"]
    couts_variables_totaux_annuel = cout_matieres_total_annuel + (prod_entieres_annee + prod_filets_annee) * 0.045 + 0.1 * revenu_total_annuel
    marge_brute = revenu_total_annuel - cout_matieres_total_annuel
    marge_sur_cout_variable = revenu_total_annuel - couts_variables_totaux_annuel
    
    part_marketing = st.sidebar.slider("Pourcentage du C.A. alloué (%)", 0.0, 15.0, 5.0,step=0.1)
    st.sidebar.markdown(f"Soit {revenu_total_annuel*part_marketing/100} € dédié au marketing")
    
    #Si la production dépasse les objectifs de ventes, il y aura des invendus non comptabilisés dans le C.A.
    
    subvention_reinsertion_annuelle = nb_ouvriers_reinsertion * 7500
    
    st.markdown(f"**Production de boîtes de filets hebdomadaire** : {int(prod_filets_hebdo)}")
    st.markdown(f"**Objectifs de ventes de boîtes de filets hebdomadaires** : {ventes_filets * 5}")

    st.markdown(f"**Production de boîtes de sardines entières hebdomadaire** : {int(prod_entieres_hebdo)}")
    st.markdown(f"**Objectifs de ventes de boîtes de sardines entières hebdomadaires** : {ventes_entieres * 5}")

    
    salaire_base = {"ouvrier": 1000, "magasinier": 1200, "contremaître": 1500, "administration": 1500, "conducteur": 1500, "Yves": 2500}
    charges_patronales = 1.5
    
    salaire_total_mensuel = (nb_ouvriers * salaire_base["ouvrier"] + salaire_base["magasinier"] + nb_contremetres * salaire_base["contremaître"] + nb_conducteurs * salaire_base["conducteur"] + salaire_base["administration"] + salaire_base["Yves"]) * charges_patronales    

    couts_fixes_annuels= salaire_total_mensuel*12 + 30000 + 36000 + 6000 + 2500*12 + 1000*12
    
    
    taux_marge_brute = (marge_brute / revenu_total_annuel) * 100
    resultat_net = revenu_total_annuel - couts_variables_totaux_annuel - couts_fixes_annuels + subvention_reinsertion_annuelle - revenu_total_annuel*part_marketing/100
    

    st.markdown("## KPIs financiers annuels")
    df_finance = pd.DataFrame({
        "Indicateur": [
            "Revenus totaux des ventes", 
            "Coûts matières totaux (sardines, huile, condiments et conserves)",
            "Autres coûts variables (expédition et frais commerciaux)",
            "Coûts variables totaux", 
            "Marge sur coûts variables",
            "Taux de marge brute",
            "Budget marketing",
            "Résultat net annuel"
        ],
        
        
        
        "Valeur": [
            f"{revenu_total_annuel:,.2f} €", 
            f"{cout_matieres_total_annuel:,.2f} €",
            f"{couts_variables_totaux_annuel:,.2f} €",
            f"{couts_variables_totaux_annuel:,.2f} €", 
            f"{marge_sur_cout_variable:,.2f} €",
            f"{taux_marge_brute:,.2f} %",
            f"{revenu_total_annuel*part_marketing/100:,.2f} €",
            f"{resultat_net:,.2f} €"
        ]
    })

    st.table(df_finance)
        
    st.markdown("## KPIs des RH")
    df_rh = pd.DataFrame({
        "Indicateur": ["Effectifs totaux", "Coût total des salaires mensuel", "Part d'ouvriers en réinsertion", "Productivité par employé en €/an"],
        "Valeur": [eff_total, f"{salaire_total_mensuel:,.2f} €", f"{int(nb_ouvriers_reinsertion*100/nb_ouvriers)}%", f"{(revenu_total_annuel / (eff_total)):.2f} € par employé"]
    })
    st.table(df_rh)

    # --- Graphique : Charges fixes et variables en fonction de la production ---

    # Définir une plage de production pour le graphique
    # Ici, on prend de 0 à 1.2 fois la production hebdomadaire maximum entre sardines entières et filets
    max_prod = max(prod_entieres_annee, prod_filets_annee) * 1.2
    production_range = np.linspace(0, max_prod, 100)

    # Calculer le coût variable unitaire pour chaque produit
    # Pour les charges variables, on inclut : coût matière + frais d'expédition (0.045€/boîte) + commission (10% du prix de vente)
    cv_entieres = cout_matiere["entieres"] + 0.045 + 0.1 * prix_entieres
    cv_filets   = cout_matiere["filets"] + 0.045 + 0.1 * prix_filets

    # Calculer le coût variable total pour chaque niveau de production (pour chaque produit)
    var_cost_entieres = cv_entieres * production_range
    var_cost_filets   = cv_filets * production_range

    # Charges fixes : elles ne dépendent pas de la production.
    # Ici, on affiche la même ligne horizontale correspondant aux charges fixes annuelles.
    fixed_cost_line = np.full_like(production_range, couts_fixes_annuels)

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(production_range, fixed_cost_line, 'k--', label="Charges fixes")
    ax.plot(production_range, var_cost_entieres, label="Charges variables - Sardines entières")
    ax.plot(production_range, var_cost_filets, label="Charges variables - Filets")
    ax.set_xlabel("Production (boîtes)")
    ax.set_ylabel("Coût (€)")
    ax.set_title("Charges fixes et variables en fonction de la production")
    ax.legend()
    ax.grid(True)

    # Affichage de l'histogramme des performances dans la première colonne
    st.markdown("## Performances")

    # Organiser les graphiques côte à côte en utilisant st.columns
    col1, col2 = st.columns(2)  # Créer 2 colonnes
    
    salaire_total_annuel = salaire_total_mensuel*12
    with col1:
        data = pd.DataFrame({
            "Catégorie": ["Revenu total annuel", "Total des coûts variables annuel", "Coût salaires annuel", "Charges fixes annuelles (dont amortissements)", "Subventions annuelles"],
            "Montant (€)": [revenu_total_annuel, couts_variables_totaux_annuel, salaire_total_annuel, couts_fixes_annuels, subvention_reinsertion_annuelle]
        })
        st.bar_chart(data.set_index("Catégorie"))
  
    # Affichage du graphique des coûts dans la deuxième colonne
    with col2:
        st.pyplot(fig)

  
    st.markdown("## S.I.G")
    
        # Catégorie : Ajustement du personnel
    capitaux_propres = st.number_input("Capitalisation propre", min_value=0, max_value=1000000, value=210000)
    actif_total = st.number_input("Actif total", min_value=0, max_value=10000000, value=210000) 
    amortissements = 180000/5

        # Calcul des S.I.G.

    ebitda = marge_brute - couts_fixes_annuels

    # Résultat d'exploitation (EBIT) (sans amortissement et dépréciation)
    ebit = ebitda - amortissements

    # Ratios financiers
    marge_nette = (resultat_net / revenu_total_annuel) * 100 if revenu_total_annuel > 0 else 0
    roa = (resultat_net / actif_total) * 100  # Supposer un actif total de 100 000€
    roe = (resultat_net / capitaux_propres) * 100  # Supposer des capitaux propres de 50 000€

    # Affichage des S.I.G. dans le tableau des KPIs financiers
    df_sigs = pd.DataFrame({
        "Indicateur": [
            "Marge brute",
            "Taux de marge brute",
            "EBITDA",
            "EBIT",
            "Résultat net",
            "Marge nette",
            "Rentabilité des actifs (ROA)",
            "Rentabilité des capitaux propres (ROE)"
        ],
        "Valeur": [
            f"{marge_brute:,.2f} €",
            f"{taux_marge_brute:.2f} %",
            f"{ebitda:,.2f} €",
            f"{ebit:,.2f} €",
            f"{resultat_net:,.2f} €",
            f"{marge_nette:.2f} %",
            f"{roa:.2f} %",
            f"{roe:.2f} %"
        ]
    })

    st.table(df_sigs)
    
    st.markdown("""
    <div style="color: lightgray; padding-top: 20px;">
        Powered by Python 3.13.2 64-bit © 2025 MASSAS GRATIOT HAMY. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()
