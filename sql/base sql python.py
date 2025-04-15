import csv
import sqlite3

# Ouverture des CSV et initialisation des listes
donnees1 = []
donnees2 = []
donnees3 = []
donnees4 = []

try:
    # Lecture des fichiers CSV
    with open('vehicules-2023.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header1 = next(reader)
        for row in reader:
            donnees1.append(row)
    print(f"Lecture de vehicules-2023.csv terminée : {len(donnees1)} lignes")

    with open('usagers-2023.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header2 = next(reader)
        for row in reader:
            donnees2.append(row)
    print(f"Lecture de usagers-2023.csv terminée : {len(donnees2)} lignes")

    with open('lieux-2023.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header3 = next(reader)
        for row in reader:
            donnees3.append(row)
    print(f"Lecture de lieux-2023.csv terminée : {len(donnees3)} lignes")

    with open('caract-2023.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header4 = next(reader)
        for row in reader:
            donnees4.append(row)
    print(f"Lecture de caract-2023.csv terminée : {len(donnees4)} lignes")

    # Connexion à la base SQLite
    conn = sqlite3.connect('accidents.db')
    cursor = conn.cursor()

    # Fonction générique pour créer une table et insérer les données
    def creer_et_inserer(nom_table, header, donnees):
        colonnes = ', '.join([f'"{col}" TEXT' for col in header])
        cursor.execute(f"DROP TABLE IF EXISTS {nom_table}")
        cursor.execute(f"CREATE TABLE {nom_table} ({colonnes})")
        placeholders = ', '.join(['?'] * len(header))
        cursor.executemany(f"INSERT INTO {nom_table} VALUES ({placeholders})", donnees)
        print(f" Table {nom_table} créée et {len(donnees)} lignes insérées")

    # Création et insertion pour chaque table
    creer_et_inserer("vehicule", header1, donnees1)
    creer_et_inserer("usager", header2, donnees2)
    creer_et_inserer("lieu", header3, donnees3)
    creer_et_inserer("caract", header4, donnees4)

    # Vérification (exemple pour vehicule)
    cursor.execute("SELECT COUNT(*) FROM vehicule")
    print("Nombre de lignes dans vehicule :", cursor.fetchone()[0])

    conn.commit()
    conn.close()

except Exception as e:
    print(" Erreur :", e)

except FileNotFoundError as e:
    print(f"Erreur : Fichier non trouvé - {e}")
    exit(1)
        
# Vérification du contenu (échantillons)
if donnees1:
    print("Exemple véhicule :", donnees1[0])
if donnees2:
    print("Exemple usager :", donnees2[0])
if donnees3:
    print("Exemple lieu :", donnees3[0])
if donnees4:
    print("Exemple caractéristique :", donnees4[0])

try:
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('accidents.db')
    cursor = conn.cursor()

    # Activation des clés étrangères
    cursor.execute("PRAGMA foreign_keys = ON")

    # Création de la table vehicule d'abord (puisqu'elle est référencée par usager)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicule (
        Num_Acc INTEGER,
        id_vehicule INTEGER,
        num_veh TEXT,
        senc INTEGER,
        catv INTEGER,
        obs INTEGER,
        obsm INTEGER,
        choc INTEGER,
        manv INTEGER
        motor INTEGER,
        PRIMARY KEY(Num_Acc, id_vehicule)
    )
    """)

    # Création de la table usager ensuite
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usager (
        Num_Acc INTEGER,
        id_usager INTEGER,
        id_vehicule INTEGER,
        num_veh TEXT,
        place INTEGER,
        catu INTEGER,
        grav INTEGER,
        sexe INTEGER,
        an_nais INTEGER,
        trajet INTEGER,
        secu1 INTEGER,
        secu2 INTEGER,
        secu3 INTEGER,
        locp INTEGER,
        actp INTEGER,
        etap INTEGER,
        PRIMARY KEY(Num_Acc, id_usager),
        FOREIGN KEY(Num_Acc, id_vehicule) REFERENCES vehicule(Num_Acc, id_vehicule)
    )
    """)

    # Table lieu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lieu (
        Num_Acc INTEGER,
        catr INTEGER,
        voie TEXT,
        v1 INTEGER,
        v2 TEXT,
        circ INTEGER,
        nbv INTEGER,
        vosp INTEGER,
        prof INTEGER,
        pr INTEGER,
        pr1 INTEGER,
        plan INTEGER,
        lartpc INTEGER,
        larrout INTEGER,
        surf INTEGER,
        infra INTEGER,
        situ INTEGER,
        vma INTEGER,
        PRIMARY KEY(Num_Acc)
    )
    """)

    # Table caract
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS caract (
        Num_Acc INTEGER,
        jour INTEGER,
        mois INTEGER,
        an INTEGER,
        hrmn TIME,
        lum INTEGER,
        dep INTEGER,
        com INTEGER,
        agg INTEGER,
        int INTEGER,
        atm INTEGER,
        col INTEGER,
        adr TEXT,
        lat REAL,
        long REAL,
        PRIMARY KEY(Num_Acc)
    )
    """)

    # Insertion dans la table 'vehicule'
    insertion_reussie = 0
    erreurs_insertion = 0
    for donnee in donnees1:
        try:
            if len(donnee) >= 9:  # Vérifier qu'il y a suffisamment de colonnes
                # Conversion des valeurs en types appropriés
                values = [
                    int(donnee[0]) if donnee[0] and donnee[0].strip() else None,  # Num_Acc
                    int(donnee[1]) if donnee[1] and donnee[1].strip() else None,  # id_vehicule
                    donnee[2],  # num_veh
                    int(donnee[3]) if donnee[3] and donnee[3].strip() else None,  # sens_circulation
                    int(donnee[4]) if donnee[4] and donnee[4].strip() else None,  # catégorie_vehicule
                    int(donnee[5]) if donnee[5] and donnee[5].strip() else None,  # obstacle_fixe
                    int(donnee[6]) if donnee[6] and donnee[6].strip() else None,  # obstacle_mobile
                    int(donnee[7]) if donnee[7] and donnee[7].strip() else None,  # point_de_choc
                    int(donnee[8]) if donnee[8] and donnee[8].strip() else None   # motorisation
                ]
                cursor.execute("""
                    INSERT INTO vehicule (Num_Acc, id_vehicule, num_veh, senc, catv, obs, obsm, choc, manv, motor)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, values)
                insertion_reussie += 1
        except Exception as e:
            erreurs_insertion += 1
            if erreurs_insertion <= 5:  # Limiter le nombre d'erreurs affichées
                print(f"Erreur d'insertion véhicule : {e}, données : {donnee}")
    print(f"Insertion des véhicules : {insertion_reussie} réussies, {erreurs_insertion} erreurs")

    # Insertion dans la table 'usager'
    insertion_reussie = 0
    erreurs_insertion = 0
    for donnee in donnees2:
        try:
            if len(donnee) >= 16:
                # Conversion des valeurs en types appropriés
                values = [
                    int(donnee[0]) if donnee[0] and donnee[0].strip() else None,  # Num_Acc
                    int(donnee[1]) if donnee[1] and donnee[1].strip() else None,  # id_usager
                    int(donnee[2]) if donnee[2] and donnee[2].strip() else None,  # id_vehicule
                    donnee[3],  # num_veh
                    int(donnee[4]) if donnee[4] and donnee[4].strip() else None,  # place
                    int(donnee[5]) if donnee[5] and donnee[5].strip() else None,  # catégorie_usager
                    int(donnee[6]) if donnee[6] and donnee[6].strip() else None,  # gravité_blessure
                    int(donnee[7]) if donnee[7] and donnee[7].strip() else None,  # sexe
                    int(donnee[8]) if donnee[8] and donnee[8].strip() else None,  # année_naissance
                    int(donnee[9]) if donnee[9] and donnee[9].strip() else None,  # trajet
                    int(donnee[10]) if donnee[10] and donnee[10].strip() else None,  # secu_1
                    int(donnee[11]) if donnee[11] and donnee[11].strip() else None,  # secu_2
                    int(donnee[12]) if donnee[12] and donnee[12].strip() else None,  # secu_3
                    int(donnee[13]) if donnee[13] and donnee[13].strip() else None,  # localisation_piéton
                    int(donnee[14]) if donnee[14] and donnee[14].strip() else None,  # action_piéton
                    int(donnee[15]) if len(donnee) > 15 and donnee[15] and donnee[15].strip() else None  # etat_piéton
                ]
                cursor.execute("""
                    INSERT INTO usager (Num_Acc, id_usager, id_vehicule, num_veh, place, catu, grav, sexe, an_nais, trajet, secu1, secu2, secu3, locp, actp, etap)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, values)
                insertion_reussie += 1
        except Exception as e:
            erreurs_insertion += 1
            if erreurs_insertion <= 5:  # Limiter le nombre d'erreurs affichées
                print(f"Erreur d'insertion usager : {e}, données : {donnee}")
    print(f"Insertion des usagers : {insertion_reussie} réussies, {erreurs_insertion} erreurs")

    # Insertion dans la table 'lieu'
    insertion_reussie = 0
    erreurs_insertion = 0
    for donnee in donnees3:
        try:
            if len(donnee) >= 18:
                # Conversion des valeurs en types appropriés
                values = [
                    int(donnee[0]) if donnee[0] and donnee[0].strip() else None,  # Num_Acc
                    int(donnee[1]) if donnee[1] and donnee[1].strip() else None,  # catr
                    donnee[2],  # voie
                    int(donnee[3]) if donnee[3] and donnee[3].strip() else None,  # v1
                    donnee[4],  # v2
                    int(donnee[5]) if donnee[5] and donnee[5].strip() else None,  # circ
                    int(donnee[6]) if donnee[6] and donnee[6].strip() else None,  # nbv
                    int(donnee[7]) if donnee[7] and donnee[7].strip() else None,  # vosp
                    int(donnee[8]) if donnee[8] and donnee[8].strip() else None,  # prof
                    int(donnee[9]) if donnee[9] and donnee[9].strip() else None,  # pr
                    int(donnee[10]) if donnee[10] and donnee[10].strip() else None,  # pr1
                    int(donnee[11]) if donnee[11] and donnee[11].strip() else None,  # plan
                    int(donnee[12]) if donnee[12] and donnee[12].strip() else None,  # lartpc
                    int(donnee[13]) if donnee[13] and donnee[13].strip() else None,  # larrout
                    int(donnee[14]) if donnee[14] and donnee[14].strip() else None,  # surf
                    int(donnee[15]) if donnee[15] and donnee[15].strip() else None,  # infra
                    int(donnee[16]) if donnee[16] and donnee[16].strip() else None,  # situ
                    int(donnee[17]) if donnee[17] and donnee[17].strip() else None   # vma
                ]
                cursor.execute("""
                    INSERT INTO lieu (Num_Acc, catr, voie, v1, v2, circ, nbv, vosp, prof, pr, pr1, plan, lartpc, larrout, surf, infra, situ, vma)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, values)
                insertion_reussie += 1
        except Exception as e:
            erreurs_insertion += 1
            if erreurs_insertion <= 5:  # Limiter le nombre d'erreurs affichées
                print(f"Erreur d'insertion lieu : {e}, données : {donnee}")
    print(f"Insertion des lieux : {insertion_reussie} réussies, {erreurs_insertion} erreurs")

    # Insertion dans la table 'caract'
    insertion_reussie = 0
    erreurs_insertion = 0
    for donnee in donnees4:
        try:
            if len(donnee) >= 15:
                # Conversion des valeurs en types appropriés
                values = [
                    int(donnee[0]) if donnee[0] and donnee[0].strip() else None,  # Num_Acc
                    int(donnee[1]) if donnee[1] and donnee[1].strip() else None,  # jour
                    int(donnee[2]) if donnee[2] and donnee[2].strip() else None,  # mois
                    int(donnee[3]) if donnee[3] and donnee[3].strip() else None,  # an
                    donnee[4],  # heure (TEXT)
                    int(donnee[5]) if donnee[5] and donnee[5].strip() else None,  # luminosité
                    int(donnee[6]) if donnee[6] and donnee[6].strip() else None,  # departement
                    int(donnee[7]) if donnee[7] and donnee[7].strip() else None,  # commune
                    int(donnee[8]) if donnee[8] and donnee[8].strip() else None,  # agglomération
                    int(donnee[9]) if donnee[9] and donnee[9].strip() else None,  # intersection
                    int(donnee[10]) if donnee[10] and donnee[10].strip() else None,  # cond_atmosphériques
                    int(donnee[11]) if donnee[11] and donnee[11].strip() else None,  # type_de_collision
                    donnee[12],  # adresse
                    float(donnee[13].replace(',', '.')) if donnee[13] and donnee[13].strip() else None,  # latitude
                    float(donnee[14].replace(',', '.')) if donnee[14] and donnee[14].strip() else None   # longitude
                ]
                cursor.execute("""
                    INSERT INTO caract (Num_Acc, jour, mois, an, hrmn, lum, dep, com, agg, int, atm, col, adr, lat, long)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, values)
                insertion_reussie += 1
        except Exception as e:
            erreurs_insertion += 1
            if erreurs_insertion <= 5:  # Limiter le nombre d'erreurs affichées
                print(f"Erreur d'insertion caractéristique : {e}, données : {donnee}")
    print(f"Insertion des caractéristiques : {insertion_reussie} réussies, {erreurs_insertion} erreurs")

    # Enregistrement des modifications
    conn.commit()

    # Vérification du nombre d'enregistrements dans chaque table
    cursor.execute("SELECT COUNT(*) FROM vehicule")
    count_vehicules = cursor.fetchone()[0]
    print(f"Nombre d'enregistrements dans la table vehicule: {count_vehicules}")

    cursor.execute("SELECT COUNT(*) FROM usager")
    count_usagers = cursor.fetchone()[0]
    print(f"Nombre d'enregistrements dans la table usager: {count_usagers}")

    cursor.execute("SELECT COUNT(*) FROM lieu")
    count_lieux = cursor.fetchone()[0]
    print(f"Nombre d'enregistrements dans la table lieu: {count_lieux}")

    cursor.execute("SELECT COUNT(*) FROM caract")
    count_caract = cursor.fetchone()[0]
    print(f"Nombre d'enregistrements dans la table caract: {count_caract}")

    # Exemples de données dans chaque table
    print("\nVérification des données insérées:")
    
    cursor.execute("SELECT * FROM vehicule LIMIT 3")
    print("\nExemples de véhicules:")
    for row in cursor.fetchall():
        print(row)
        
    cursor.execute("SELECT * FROM usager LIMIT 3")
    print("\nExemples d'usagers:")
    for row in cursor.fetchall():
        print(row)
            
    cursor.execute("SELECT * FROM lieu LIMIT 3")  
    print("\nExemples de lieux:")
    for row in cursor.fetchall():
        print(row)
        
    cursor.execute("SELECT * FROM caract LIMIT 3")
    print("\nExemples de caractéristiques:")
    for row in cursor.fetchall():
        print(row)

except Exception as e:
    print(f"Erreur lors des opérations sur la base de données: {e}")
    if 'conn' in locals():
        conn.rollback()
finally:
    # Fermeture de la connexion
    if 'conn' in locals():
        conn.close()
        print("\nBase de données créée et connexion fermée.")
