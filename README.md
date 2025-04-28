# Seconde Vague - Optimisation de la production de sardines

Seconde Vague est une application Streamlit réalisé dans le cadre du cours Suivi des Performances des Organisations de Sciences Po Aix. L'application, accessible en ligne à l'adresse (https://kouign.streamlit.app) permet de simuler et analyser les flux de production de sardines (entières et en filets) d'une entreprise fictive pour optimiser les revenus, les coûts et la rentabilité.

-----------------

## Fonctionnalités

- Visualisation des flux de production avec un diagramme dynamique.
- Suivi des objectifs de production et de vente.
- Calcul des KPIs financiers : revenus, coûts, marge brute, seuil de rentabilité.
- Alertes en cas de surcharge de production.

-----------------

## Installation

1. Cloner le dépôt:

   ```bash
   git clone https://github.com/pierreyveshamy/seconde_vague.git
   cd seconde_vague
   ```

2. Créer un environnement virtuel et installer les dépendances:

   ```bash
   python -m venv env
   source env/bin/activate  # Mac/Linux
   env\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. Lancer l'appli:

   ```bash
   streamlit run app.py
   ```

-----------------

## Structure du projet

```
seconde_vague/
├── pages/
│   └── analyses.py         # Pages secondaires Streamlit
├── app.py                   # Fichier principal Streamlit
├── requirements.txt         # Dépendances
└── README.md                # Documentation du projet
```

-----------------

## Déploiement sur Streamlit Cloud

1. Connecte ton compte GitHub à [Streamlit Cloud](https://share.streamlit.io/).
2. Sélectionne ce dépôt et déploie l'application.

-----------------

## Auteur

- Pierre-Yves Hamy 
- [GitHub](https://github.com/pierreyveshamy)
