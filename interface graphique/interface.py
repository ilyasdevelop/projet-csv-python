import sys
import os
import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Vérifier si le chemin existe avant de l'ajouter
custom_path = r"C:\Users\Arthur.Loret\AppData\Roaming\Python\Python312\site-packages"
if os.path.exists(custom_path):
    sys.path.append(custom_path)

# Initialiser le mode sombre par défaut
ctk.set_appearance_mode("dark")  # "dark" ou "light"
ctk.set_default_color_theme("blue")

class SQLiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interrogation de Base de Données SQLite")
        self.root.geometry("1000x700")
        self.conn = None
        self.cursor = None
        self.db_path = None
        self.recent_queries = []
        self.query_history_index = -1
        
        self.create_widgets()
        
    def create_widgets(self):
        # Titre principal
        self.title_label = ctk.CTkLabel(self.root, text="Explorateur de Base de Données SQLite", 
                                        font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)
        
        # Frame pour les boutons supérieurs
        self.top_frame = ctk.CTkFrame(self.root)
        self.top_frame.pack(fill="x", padx=10, pady=5)
        
        # Bouton de sélection de la base de données
        self.db_button = ctk.CTkButton(self.top_frame, text="Sélectionner une base de données", 
                                        font=("Arial", 12), command=self.select_database)
        self.db_button.pack(side="left", padx=5)
        
        # Indicateur de connexion
        self.connection_label = ctk.CTkLabel(self.top_frame, text="Non connecté", 
                                            font=("Arial", 12), text_color="red")
        self.connection_label.pack(side="left", padx=10)
        
        # Commutateur de mode (Dark/Light)
        self.switch_var = ctk.StringVar(value="Off")
        self.mode_switch = ctk.CTkSwitch(self.top_frame, text="Mode clair", 
                                        variable=self.switch_var, onvalue="On", 
                                        offvalue="Off", command=self.toggle_mode)
        self.mode_switch.pack(side="right", padx=10)
        
        # Frame pour les tables à gauche
        self.left_frame = ctk.CTkFrame(self.root, width=200)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=5)
        
        # Label pour la liste des tables
        self.tables_label = ctk.CTkLabel(self.left_frame, text="Tables disponibles:", 
                                        font=("Arial", 12, "bold"))
        self.tables_label.pack(anchor="w", pady=5)
        
        # Liste des tables
        self.tables_listbox = ctk.CTkScrollableFrame(self.left_frame, width=180, height=300)
        self.tables_listbox.pack(fill="both", expand=True, pady=5)
        
        # Bouton pour afficher la structure de la table
        self.structure_button = ctk.CTkButton(self.left_frame, text="Afficher structure", 
                                            font=("Arial", 12), command=self.show_table_structure)
        self.structure_button.pack(pady=5, fill="x")
        
        # Bouton pour afficher les données de la table
        self.data_button = ctk.CTkButton(self.left_frame, text="Afficher données", 
                                        font=("Arial", 12), command=self.show_table_data)
        self.data_button.pack(pady=5, fill="x")
        
        # Frame principal pour la zone de requête et résultats
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)
        
        # Zone de saisie de requête
        self.query_frame = ctk.CTkFrame(self.main_frame)
        self.query_frame.pack(pady=5, fill="x")
        
        self.query_label = ctk.CTkLabel(self.query_frame, text="Requête SQL :", 
                                        font=("Arial", 12, "bold"))
        self.query_label.pack(anchor="w")
        
        self.query_entry = ctk.CTkTextbox(self.query_frame, height=120, 
                                        font=("Courier New", 12))
        self.query_entry.pack(fill="x")
        
        # Boutons pour naviguer dans l'historique des requêtes
        self.history_frame = ctk.CTkFrame(self.main_frame)
        self.history_frame.pack(fill="x", pady=5)
        
        self.prev_button = ctk.CTkButton(self.history_frame, text="⬅️ Précédente", 
                                        font=("Arial", 12), command=self.prev_query,
                                        width=100)
        self.prev_button.pack(side="left", padx=5)
        
        self.next_button = ctk.CTkButton(self.history_frame, text="Suivante ➡️", 
                                        font=("Arial", 12), command=self.next_query,
                                        width=100)
        self.next_button.pack(side="left", padx=5)
        
        # Bouton d'exécution
        self.execute_button = ctk.CTkButton(self.history_frame, text="Exécuter ▶️", 
                                            font=("Arial", 12, "bold"), 
                                            command=self.execute_query,
                                            fg_color="#007500")
        self.execute_button.pack(side="right", padx=5)
        
        self.save_button = ctk.CTkButton(self.history_frame, text="Exporter CSV", 
                                        font=("Arial", 12), command=self.export_to_csv)
        self.save_button.pack(side="right", padx=5)
        
        # Frame pour les résultats
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.pack(fill="both", expand=True, pady=5)
        
        self.results_label = ctk.CTkLabel(self.results_frame, text="Résultats :", 
                                        font=("Arial", 12, "bold"))
        self.results_label.pack(anchor="w")
        
        # Table d'affichage avec scrollbar
        self.tree_frame = ctk.CTkScrollableFrame(self.results_frame)
        self.tree_frame.pack(fill="both", expand=True)
        
        # Barre de statut
        self.status_frame = ctk.CTkFrame(self.root, height=30)
        self.status_frame.pack(fill="x", pady=5, padx=10)
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Prêt", 
                                        font=("Arial", 10))
        self.status_label.pack(side="left", padx=10)
        
        self.rows_label = ctk.CTkLabel(self.status_frame, text="0 lignes", 
                                        font=("Arial", 10))
        self.rows_label.pack(side="right", padx=10)
        
    def select_database(self):
        """Sélectionne une base de données SQLite."""
        self.db_path = filedialog.askopenfilename(
            title="Sélectionner une base de données SQLite", 
            filetypes=[("SQLite Database", "*.db"), ("Tous les fichiers", "*.*")]
        )
        
        if self.db_path:
            try:
                # Fermer la connexion existante si elle existe
                if self.conn:
                    self.conn.close()
                
                self.conn = sqlite3.connect(self.db_path)
                self.cursor = self.conn.cursor()
                self.connection_label.configure(text=f"Connecté: {os.path.basename(self.db_path)}", 
                                                text_color="green")
                self.status_label.configure(text=f"Base de données chargée: {self.db_path}")
                
                # Charger la liste des tables
                self.load_tables()
                
            except Exception as e:
                messagebox.showerror("Erreur de connexion", str(e))
                self.connection_label.configure(text="Erreur de connexion", text_color="red")
    
    def load_tables(self):
        """Charge la liste des tables de la base de données."""
        # Effacer les widgets existants
        for widget in self.tables_listbox.winfo_children():
            widget.destroy()
        
        # Récupérer la liste des tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        
        # Créer des boutons pour chaque table
        for i, (table,) in enumerate(tables):
            table_button = ctk.CTkButton(self.tables_listbox, text=table, 
                                        command=lambda t=table: self.select_table(t),
                                        anchor="w", height=30)
            table_button.pack(fill="x", pady=2)
    
    def select_table(self, table_name):
        """Sélectionne une table dans la liste."""
        self.selected_table = table_name
        query = f"SELECT * FROM {table_name} LIMIT 100;"
        self.query_entry.delete("1.0", "end")
        self.query_entry.insert("1.0", query)
        self.execute_query()
    
    def show_table_structure(self):
        """Affiche la structure de la table sélectionnée."""
        try:
            selected_table = self.get_selected_table()
            if selected_table:
                self.cursor.execute(f"PRAGMA table_info({selected_table});")
                columns = self.cursor.fetchall()
                
                # Créer un DataFrame pour afficher les résultats
                df = pd.DataFrame(columns, columns=[
                    'cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'
                ])
                
                # Effacer l'ancien affichage
                for widget in self.tree_frame.winfo_children():
                    widget.destroy()
                
                # Afficher les données dans la frame
                for i, row in df.iterrows():
                    row_frame = ctk.CTkFrame(self.tree_frame)
                    row_frame.pack(fill="x", pady=1)
                    
                    # Afficher le nom de la colonne avec un style plus visible
                    ctk.CTkLabel(row_frame, text=row['name'], width=120, 
                                font=("Arial", 12, "bold")).pack(side="left", padx=5)
                    
                    # Type de données
                    ctk.CTkLabel(row_frame, text=row['type'], width=100).pack(side="left", padx=5)
                    
                    # Clé primaire
                    pk_text = "PK" if row['pk'] == 1 else ""
                    ctk.CTkLabel(row_frame, text=pk_text, width=30).pack(side="left", padx=5)
                    
                    # Not Null
                    nn_text = "NOT NULL" if row['notnull'] == 1 else ""
                    ctk.CTkLabel(row_frame, text=nn_text, width=80).pack(side="left", padx=5)
                    
                    # Valeur par défaut
                    default_value = str(row['dflt_value']) if row['dflt_value'] is not None else ""
                    ctk.CTkLabel(row_frame, text=default_value, width=100).pack(side="left", padx=5)
                
                self.status_label.configure(text=f"Structure de la table {selected_table}")
                self.rows_label.configure(text=f"{len(df)} colonnes")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def show_table_data(self):
        """Affiche les données de la table sélectionnée."""
        selected_table = self.get_selected_table()
        if selected_table:
            query = f"SELECT * FROM {selected_table} LIMIT 100;"
            self.query_entry.delete("1.0", "end")
            self.query_entry.insert("1.0", query)
            self.execute_query()
    
    def get_selected_table(self):
        """Récupère le nom de la table sélectionnée."""
        if hasattr(self, 'selected_table'):
            return self.selected_table
        else:
            messagebox.showinfo("Information", "Veuillez sélectionner une table dans la liste.")
            return None
    
    def execute_query(self):
        """Exécute une requête SQL saisie par l'utilisateur et affiche les résultats."""
        query = self.query_entry.get("1.0", "end").strip()
        if not query:
            messagebox.showwarning("Requête vide", "Veuillez saisir une requête SQL.")
            return
        
        try:
            # Exécuter la requête
            start_time = pd.Timestamp.now()
            self.cursor.execute(query)
            
            # Vérifier si c'est une requête SELECT
            if query.strip().upper().startswith(("SELECT", "PRAGMA", "EXPLAIN")):
                # Récupérer les résultats
                rows = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                
                # Créer un DataFrame pour faciliter l'affichage
                df = pd.DataFrame(rows, columns=columns)
                
                # Effacer l'ancien affichage
                for widget in self.tree_frame.winfo_children():
                    widget.destroy()
                
                # Créer un header pour les colonnes
                header_frame = ctk.CTkFrame(self.tree_frame)
                header_frame.pack(fill="x", pady=2)
                
                for i, col in enumerate(columns):
                    ctk.CTkLabel(header_frame, text=col, width=120, 
                                font=("Arial", 12, "bold")).pack(side="left", padx=5)
                
                # Afficher les données
                for i, row in df.iterrows():
                    row_frame = ctk.CTkFrame(self.tree_frame)
                    row_frame.pack(fill="x", pady=1)
                    
                    for j, value in enumerate(row):
                        ctk.CTkLabel(row_frame, text=str(value), width=120).pack(side="left", padx=5)
                
                # Mettre à jour la barre de statut
                elapsed_time = (pd.Timestamp.now() - start_time).total_seconds()
                self.status_label.configure(text=f"Requête exécutée en {elapsed_time:.3f} secondes")
                self.rows_label.configure(text=f"{len(df)} lignes")
                
                # Stocker les résultats pour export
                self.last_results = df
            else:
                # Pour les requêtes modifiant la base de données
                self.conn.commit()
                
                # Afficher un message de confirmation
                affected_rows = self.cursor.rowcount
                messagebox.showinfo("Succès", f"Requête exécutée avec succès. {affected_rows} lignes affectées.")
                
                # Mettre à jour la barre de statut
                elapsed_time = (pd.Timestamp.now() - start_time).total_seconds()
                self.status_label.configure(text=f"Requête exécutée en {elapsed_time:.3f} secondes")
                self.rows_label.configure(text=f"{affected_rows} lignes affectées")
            
            # Ajouter la requête à l'historique
            self.add_to_history(query)
            
        except Exception as e:
            messagebox.showerror("Erreur SQL", str(e))
            self.status_label.configure(text=f"Erreur: {str(e)}")
    
    def add_to_history(self, query):
        """Ajoute une requête à l'historique."""
        # Supprimer les doublons consécutifs
        if not self.recent_queries or query != self.recent_queries[-1]:
            self.recent_queries.append(query)
            self.query_history_index = len(self.recent_queries) - 1
    
    def prev_query(self):
        """Navigue vers la requête précédente dans l'historique."""
        if self.recent_queries and self.query_history_index > 0:
            self.query_history_index -= 1
            self.query_entry.delete("1.0", "end")
            self.query_entry.insert("1.0", self.recent_queries[self.query_history_index])
    
    def next_query(self):
        """Navigue vers la requête suivante dans l'historique."""
        if self.recent_queries and self.query_history_index < len(self.recent_queries) - 1:
            self.query_history_index += 1
            self.query_entry.delete("1.0", "end")
            self.query_entry.insert("1.0", self.recent_queries[self.query_history_index])
    
    def export_to_csv(self):
        """Exporte les résultats actuels vers un fichier CSV."""
        if hasattr(self, 'last_results') and not self.last_results.empty:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Enregistrer les résultats sous"
            )
            
            if file_path:
                try:
                    self.last_results.to_csv(file_path, index=False)
                    messagebox.showinfo("Export réussi", f"Données exportées vers {file_path}")
                except Exception as e:
                    messagebox.showerror("Erreur d'export", str(e))
        else:
            messagebox.showinfo("Information", "Aucun résultat à exporter.")
    
    def toggle_mode(self):
        """Bascule entre les modes sombre et clair."""
        if self.switch_var.get() == "On":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
    
    def on_closing(self):
        """Ferme la connexion à la base de données et quitte l'application."""
        if self.conn:
            self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = SQLiteApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()