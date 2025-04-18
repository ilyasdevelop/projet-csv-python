Outil d'Analyse de Base de Données d'Accidents

Ce projet fournit une interface graphique pour analyser les données d'accidents stockées dans une base de données SQLite.
Installation

    Installez les dépendances nécessaires :

pip install -r requirements.txt

Placez vos fichiers de données CSV dans le répertoire csv :

    vehicules-2023.csv

    usagers-2023.csv

    lieux-2023.csv

    caract-2023.csv

Initialisez la base de données :

    python "sql/base sql python.py"

Utilisation

    Lancez l'interface graphique :

    python "interface graphique/interface_graphique_ctk.py"

    Sélectionnez le fichier de base de données (accidents.db) lorsqu'il vous est demandé.

    Entrez des requêtes SQL dans la zone de texte et cliquez sur "Exécuter" pour les lancer.

    Utilisez le bouton de basculement mode clair/sombre pour changer de thème.

Exemples de Requêtes

Le fichier sql/requetes.sql contient des exemples de requêtes qui peuvent être utilisées pour analyser les données d'accidents.
Dépannage

    Si vous rencontrez des problèmes avec les fichiers CSV, assurez-vous qu'ils sont correctement formatés avec un point-virgule (;) comme séparateur.

    Vérifiez que toutes les dépendances requises sont installées.

    Contrôlez que le fichier de base de données existe et est accessible.
