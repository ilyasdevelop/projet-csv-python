# interface.py
import tkinter as tk
from tkinter import ttk
import sqlite3

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Recherche d'accidents")
        self.setup_ui()

    def setup_ui(self):
        # Champ de saisie pour la gravité
        self.label = ttk.Label(self.root, text="Gravité (1-4):")
        self.label.pack(pady=5)
        self.gravite_entry = ttk.Entry(self.root)
        self.gravite_entry.pack(pady=5)

        # Bouton de recherche
        self.btn = ttk.Button(self.root, text="Rechercher", command=self.search)
        self.btn.pack(pady=10)

        # Tableau des résultats
        self.tree = ttk.Treeview(self.root, columns=("Num_acc", "choc", "collision"), show="headings")
        self.tree.heading("Num_acc", text="N° Accident")
        self.tree.heading("choc", text="Type de choc")
        self.tree.heading("collision", text="Collision")
        self.tree.pack()

    def search(self):
        gravite = self.gravite_entry.get()
        conn = sqlite3.connect('accidents.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Num_acc, choc, collision FROM Accident WHERE gravite = ?", (gravite,))
        rows = cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    