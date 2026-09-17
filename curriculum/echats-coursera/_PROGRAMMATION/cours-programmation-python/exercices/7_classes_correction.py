# ============================
# Chapitre 7 : Classes
# ============================

# =========== Exercice 1 ===========
# Créer une classe Chien avec un attribut nom.
# Créer un objet de cette classe et afficher son nom.
def exercice1():
    class Chien:
        def __init__(self, nom):
            self.nom = nom
    mon_chien = Chien("Rex")
    print("Nom du chien :", mon_chien.nom)


# =========== Exercice 2 ===========
# Ajouter une méthode aboyer() à la classe Chien qui affiche "Woof !".
def exercice2():
    class Chien:
        def __init__(self, nom):
            self.nom = nom
        def aboyer(self):
            print("Woof !")
    mon_chien = Chien("Buddy")
    mon_chien.aboyer()


# =========== Exercice 3 ===========
# Créer une classe CompteBancaire avec un solde initial.
# Ajouter des méthodes deposer(montant) et retirer(montant).
def exercice3():
    class CompteBancaire:
        def __init__(self, solde_initial=0):
            self.solde = solde_initial
        def deposer(self, montant):
            self.solde += montant
        def retirer(self, montant):
            if montant <= self.solde:
                self.solde -= montant
            else:
                print("Solde insuffisant")
    compte = CompteBancaire(100)
    compte.deposer(50)
    compte.retirer(30)
    print("Solde final :", compte.solde)


# =========== Exercice 4 ===========
# Montrer la différence entre deux variables simples et deux objets.
def exercice4():
    # Variables simples
    a = 10
    b = a
    a = 20
    print("Variables simples : a =", a, ", b =", b)  # b reste 10

    # Objets
    class MaClasse:
        def __init__(self, valeur):
            self.valeur = valeur
    obj1 = MaClasse(10)
    obj2 = obj1
    obj1.valeur = 20
    print("Objets : obj1.valeur =", obj1.valeur, ", obj2.valeur =", obj2.valeur)  # obj2 aussi change


# =========== Exercice 5 ===========
# Créer une classe Rectangle avec largeur et hauteur.
# Ajouter une méthode aire() qui retourne la surface.
def exercice5():
    class Rectangle:
        def __init__(self, largeur, hauteur):
            self.largeur = largeur
            self.hauteur = hauteur
        def aire(self):
            return self.largeur * self.hauteur
    rect = Rectangle(4, 5)
    print("Aire du rectangle :", rect.aire())


# ============================
# Exécution des exercices
# ============================

exercice1()
exercice2()
exercice3()
exercice4()
exercice5()
