# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:19:10 2025

@author: arthur.loret
"""

import sys
sys.path.append(r"C:\Users\Arthur.Loret\AppData\Roaming\Python\Python312\site-packages")
import customtkinter as ctk

from tkinter import filedialog, messagebox
import sqlite3
import pandas as pd

# Initialiser le mode sombre par défaut
ctk.set_appearance_mode("dark")  # "dark" ou "light"
ctk.set_default_color_theme("blue")

# Fonction pour sélectionner la base de données
def select_database():
    global conn, cursor, db_path
    db_path = filedialog.askopenfilename(title="Sélectionner une base de données SQLite", filetypes=[("SQLite Database", "*.db")])
    if db_path:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            messagebox.showinfo("Succès", f"Connexion réussie à {db_path}")
        except Exception as e:
            messagebox.showerror("Erreur de connexion", str(e))

def execute_query():
    """Exécute une requête SQL saisie par l'utilisateur et affiche les résultats."""
    query = query_entry.get("1.0", "end").strip()
    if not query:
        messagebox.showwarning("Requête vide", "Veuillez saisir une requête SQL.")
        return
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] 
        
        # Effacer l'ancien affichage
        for row in tree.winfo_children():  # Correcte la méthode utilisée pour obtenir les enfants
            tree.delete(row)
        
        # Mettre à jour les colonnes du Treeview
        tree["columns"] = columns
        tree["show"] = "headings"
        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=120, anchor="center")
        
        # Insérer les nouvelles données
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Erreur SQL", str(e))

# Fonction pour basculer entre les modes
def toggle_mode():
    if switch_var.get() == "On":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

# Interface CustomTkinter
root = ctk.CTk()
root.title("Interrogation de la Base de Données")
root.geometry("900x600")

# Titre
title_label = ctk.CTkLabel(root, text="Exécuter des requêtes SQL", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Bouton de sélection de la base de données
db_button = ctk.CTkButton(root, text="Sélectionner une base de données", font=("Arial", 12), command=select_database)
db_button.pack(pady=5)

# Zone de saisie de requête
query_frame = ctk.CTkFrame(root)
query_frame.pack(pady=5, fill="x", padx=10)
query_label = ctk.CTkLabel(query_frame, text="Saisissez votre requête SQL :", font=("Arial", 12))
query_label.pack(anchor="w")
query_entry = ctk.CTkTextbox(query_frame, height=100, font=("Arial", 12))
query_entry.pack(fill="x")

# Bouton d'exécution
execute_button = ctk.CTkButton(root, text="Exécuter", font=("Arial", 12), command=execute_query)
execute_button.pack(pady=10)

# Table d'affichage avec scrollbar
frame = ctk.CTkFrame(root)
frame.pack(fill="both", expand=True, padx=10, pady=5)

tree_frame = ctk.CTkFrame(frame)
tree_frame.pack(fill="both", expand=True)

tree_scroll = ctk.CTkScrollbar(tree_frame, orientation="vertical")
tree_scroll.pack(side="right", fill="y")

tree = ctk.CTkScrollableFrame(tree_frame)
tree.pack(fill="both", expand=True)

# **Correction :**
# Si vous voulez changer la couleur ou la configuration du Treeview (frame scrollable), utilisez les options suivantes :

tree.configure(fg_color="gray")  # Exemple de configuration correcte

# Commutateur de mode (Dark/Light)
switch_var = ctk.StringVar(value="Off")
mode_switch = ctk.CTkSwitch(root, text="Mode clair", variable=switch_var, onvalue="On", offvalue="Off", command=toggle_mode)
mode_switch.pack(pady=10)

# Lancer l'application
root.mainloop()

# Fermer la connexion à la base de données si elle existe
if 'conn' in globals():
    conn.close()

