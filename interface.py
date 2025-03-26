from tkinter import *

class App:
    def __init__(self, fen):
        ''' Cette méthode dit constructeur permet de créer une instance de App '''
        self.fen = fen
        self.fen.geometry('400x400')
        self.fen.configure(bg="#d9d9d9")
        self.fen.title("CSV_Python_SQL")
        self.accueil()

    def accueil(self):
        '''page d'accueil'''
        #insertion de l'image chapeau
        try:
            self.photo1 = PhotoImage(file="inserer le chemin de l'image")  # Replace with actual image path
            self.picture = Label(self.fen, image=self.photo1)
            self.picture.photo = self.photo1
            self.picture.place(x=10, y=10)
        except Exception as e:
            print(f"Error loading image: {e}")
        
        # Message d'accueil
        self.label_welcome = Label(self.fen, text="Bienvenue dans le gestionnaire d'arbre généalogique", bg="#d9d9d9")
        self.label_welcome.place(x=10, y=50)

        # bouton de création d'un arbre
        self.bouton_creer = Button(self.fen, bg="#FFFFFF", text='Créer', command=self.creer)
        self.bouton_creer.place(x=10, y=350)

        # bouton d'ajout
        self.bouton_ajout = Button(self.fen, bg="#FFFFFF", text='Ajouter', command=self.ajouter)
        self.bouton_ajout.place(x=70, y=350)

        # bouton d'affichage infixe
        self.bouton_aff_infixe = Button(self.fen, bg="#FFFFFF", text="Afficher les membres", command=self.afficher)
        self.bouton_aff_infixe.place(x=140, y=350)

        # bouton de suppression
        self.bouton_sup = Button(self.fen, bg="#FFFFFF", text='Informations', command=self.informer)
        self.bouton_sup.place(x=320, y=350)

    def quitter(self):
        self.fen.destroy()

    def ajouter(self):
        '''Cette méthode permet d'accéder à la fenêtre d'ajout d'un membre de la famille'''
        # On supprime les composants précédemment créés
        self.bouton_creer.destroy()
        self.bouton_ajout.destroy()
        self.bouton_aff_infixe.destroy()
        self.bouton_sup.destroy()

        # On crée les composants nécessaires à l'ajout d'un membre
        self.label1 = Label(self.fen, bg="#d9d9d9", text='Nom')
        self.label1.place(x=10, y=200)
        self.nom = StringVar(self.fen)
        self.txtEditNom = Entry(self.fen, textvariable=self.nom)
        self.txtEditNom.place(x=130, y=200)

        self.label2 = Label(self.fen, bg="#d9d9d9", text='Date de naissance')
        self.label2.place(x=10, y=280)
        self.date_naissance = StringVar(self.fen)
        self.txtEditDate = Entry(self.fen, textvariable=self.date_naissance)
        self.txtEditDate.place(x=130, y=280)

        # bouton de validation
        self.bouton_val = Button(self.fen, bg="grey", text='Valider', command=self.accueil)
        self.bouton_val.place(x=300, y=350)

    def creer(self):
        # Functionality to create the tree
        pass

    def afficher(self):
        # Functionality to display tree members
        pass

    def informer(self):
        # Functionality to provide information
        pass


if __name__ == "__main__":
    fen = Tk()
    app = App(fen)
    fen.mainloop()
