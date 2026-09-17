# ============================
# Chapitre 6 : Fonctions
# ============================

# =========== Exercice 1 ===========
# Écrire une fonction qui affiche "Bonjour !" quand elle est appelée.
def exercice1():
    print("Bonjour !")

# =========== Exercice 2 ===========
# Écrire une fonction qui prend un prénom en paramètre et affiche "Bonjour <prénom> !".
def exercice2(prenom="Alice"):
    print(f"Bonjour {prenom} !")

# =========== Exercice 3 ===========
# Écrire une fonction qui prend deux nombres en paramètre et retourne leur somme.
def exercice3(a=0, b=0):
    return a + b

# =========== Exercice 4 ===========
# Écrire une fonction factorielle(n) qui calcule n! avec une boucle.
def exercice4(n=5):
    resultat = 1
    for i in range(1, n + 1):
        resultat *= i
    return resultat

# =========== Exercice 5 ===========
# Écrire une fonction est_pair(n) qui retourne True si n est pair, False sinon.
def exercice5(n=0):
    return n % 2 == 0


# ============================
# Exécution des exercices
# ============================

exercice1()
exercice2("Jean")
print("Somme de 3 et 5 :", exercice3(3, 5))
print("Factorielle de 5 :", exercice4(5))
print("8 est pair ?", exercice5(8))
print("7 est pair ?", exercice5(7))
