import sqlite3
import logging

def tester_base_donnees():
    """Teste la connexion à la base de données et vérifie les données."""
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('accidents.db')
        cursor = conn.cursor()
        
        # Vérifier les tables
        tables = ['lieu', 'caract', 'vehicule', 'usager']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            nombre = cursor.fetchone()[0]
            print(f"Nombre d'enregistrements dans {table}: {nombre}")
        
        # Vérifier le nombre total d'accidents
        cursor.execute("SELECT COUNT(DISTINCT Num_Acc) FROM caract")
        total_accidents = cursor.fetchone()[0]
        print(f"\nNombre total d'accidents: {total_accidents}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    tester_base_donnees() 