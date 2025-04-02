# CSV to Database Converter

## Description du projet
Ce projet a été développé dans le cadre scolaire et permet de transformer des fichiers CSV en base de données relationnelle. L'application dispose d'une interface graphique facilitant la manipulation et la conversion des données.

## Fonctionnalités
- Import de fichiers CSV de différents formats
- Prévisualisation des données avant conversion
- Paramétrage des types de données pour chaque colonne
- Création automatique de schémas de base de données
- Conversion et stockage dans plusieurs formats de base de données (SQLite, MySQL, PostgreSQL)
- Interface graphique intuitive pour une utilisation sans connaissances techniques avancées
- Historique des conversions effectuées

## Prérequis
- Python 3.8 ou version ultérieure
- Bibliothèques requises :
-    tkinter, customtkinter, os, CTKLisbox, sqlite3, pandas
## Installation
1. Clonez ce dépôt sur votre machine locale :
```bash
git clone https://github.com/votre-nom/csv-to-database.git
cd csv-to-database
```

2. Créez et activez un environnement virtuel (recommandé) :
```bash
python -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation
1. Lancez l'application :
```bash
python main.py
```

2. Dans l'interface graphique :
   - Cliquez sur "Importer un fichier CSV"
   - Configurez les paramètres de conversion
   - Prévisualisez les données
   - Sélectionnez le type de base de données cible
   - Lancez la conversion

## Structure du projet
```
csv-to-database/
├── main.py             # Point d'entrée de l'application
├── requirements.txt    # Dépendances du projet
├── src/
│   ├── gui/            # Modules de l'interface graphique
│   ├── parsers/        # Analyseurs pour différents formats CSV
│   ├── converters/     # Convertisseurs vers différentes bases de données
│   └── utils/          # Fonctions utilitaires
├── tests/              # Tests unitaires et d'intégration
└── doc/                # Documentation
```

## Contribution
Ce projet a été développé dans le cadre d'un cours de [nom du cours]. Les contributions sont les bienvenues sous forme de pull requests, en particulier pour :
- Ajouter le support de nouveaux formats de bases de données
- Améliorer l'interface utilisateur
- Optimiser les performances de conversion

## Licence
Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
