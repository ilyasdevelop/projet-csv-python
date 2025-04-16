# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 19:26:22 2025

@author: arthu
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class SQLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SQL Query Tool")
        self.geometry("750x550")

        self.conn = None # Connexion à la base de données, initialisée à None

        
        self.db_label_var = tk.StringVar()# Variable pour afficher le nom de la base de données ouverte
        self.db_label_var.set("Aucune base sélectionnée")# Si l'utilisateur n'a pas sélectionner de base de donnée

        # Bouton pour ouvrir une base de données SQLite
        self.open_button = tk.Button(self, text="Ouvrir une base de données", command=self.open_database)
        self.open_button.pack(pady=10)

        # Label pour afficher le nom du fichier de la base de données ouverte
        self.db_label = tk.Label(self, textvariable=self.db_label_var, fg="blue")
        self.db_label.pack()

        # Champ de saisie pour la requête SQL
        self.query_input = tk.Entry(self, width=80)
        self.query_input.insert(0, "Écris ta requête SQL ici")  # Texte par défaut dans le champ
        self.query_input.pack(pady=10)

        # Bouton pour exécuter la requête SQL
        self.run_button = tk.Button(self, text="Exécuter", command=self.execute_query)
        self.run_button.pack(pady=5)

        # Cadre pour afficher les résultats de la requête
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=10, fill="both", expand=True)

        # Treeview pour afficher les résultats de la requête
        self.tree = ttk.Treeview(self.result_frame)
        self.tree.pack(fill="both", expand=True)

        # Ajout d'un événement pour effacer le texte de la requête quand l'utilisateur clique dans le champ
        self.query_input.bind("<FocusIn>", self.clear_placeholder)

    def open_database(self):
        # Ouvre un dialogue pour sélectionner une base de données SQLite
        filepath = filedialog.askopenfilename(
            title="Choisir une base SQLite",
            filetypes=[("Base de données SQLite", "*.db *.sqlite3"), ("Tous les fichiers", "*.*")]
        )
        if filepath:
            try:
                # Si une connexion existante, on la ferme avant d'en ouvrir une nouvelle
                if self.conn:
                    self.conn.close()

                # On ouvre la connexion à la base de données SQLite
                self.conn = sqlite3.connect(filepath)
                self.db_label_var.set(f"Base sélectionnée : {filepath}")
                messagebox.showinfo("Succès", "Connexion à la base réussie !")

            except Exception as e:
                # Si une erreur se produit (par exemple fichier non valide), on affiche un message d'erreur
                messagebox.showerror("Erreur", f"Impossible d'ouvrir la base : {e}")

    def update_treeview(self, columns, rows):
        # Met à jour la Treeview avec les nouvelles colonnes et lignes
        self.tree.delete(*self.tree.get_children())  # Supprime les anciennes lignes
        self.tree["columns"] = columns  # Définit les colonnes
        self.tree["show"] = "headings"  # Affiche uniquement les en-têtes des colonnes
        for col in columns:
            # Ajoute les en-têtes de colonnes
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Définit une largeur par défaut pour chaque colonne

        # Ajoute chaque ligne dans la Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def execute_query(self):
        # Vérifie si une base de données est ouverte
        if not self.conn:
            messagebox.showwarning("Base manquante", "Veuillez d'abord sélectionner une base de données.")
            return

        # Récupère la requête SQL saisie
        query = self.query_input.get()

        # Vérifie que la requête commence par SELECT
        if not query.strip().lower().startswith("select"):
            messagebox.showwarning("Requête non autorisée", "Seules les requêtes SELECT sont autorisées.")
            return

        try:
            # Exécute la requête SQL et récupère les résultats
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            # Récupère les noms des colonnes à partir de la description du curseur
            columns = [desc[0] for desc in cursor.description]

            # Met à jour la Treeview avec les résultats
            self.update_treeview(columns, rows)

        except Exception as e:
            # Si une erreur se produit lors de l'exécution de la requête, affiche un message d'erreur
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def clear_placeholder(self, event):
        # Efface le texte par défaut "Écris ta requête SQL ici" lorsque l'utilisateur clique dans le champ
        if self.query_input.get() == "Écris ta requête SQL ici":
            self.query_input.delete(0, "end")

if __name__ == "__main__":
    app = SQLApp()
    app.mainloop()
