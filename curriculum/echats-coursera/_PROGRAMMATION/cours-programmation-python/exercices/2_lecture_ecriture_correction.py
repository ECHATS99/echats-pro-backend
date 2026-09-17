# ============================
# Chapitre 2 : Lecture et écriture
# ============================

# =========== Exercice 1 ===========
# Demander à l’utilisateur son prénom puis afficher : "Bonjour <prénom> !"
# Indice : utiliser input() pour lire et print() pour afficher
def exercice1():
    prenom = input("Écrivez votre prénom : ")  # input() pour lire
    print(f"Bonjour {prenom} !")              # print() pour afficher


# =========== Exercice 2 ===========
# Demander à l’utilisateur deux nombres (a et b)
# Afficher leur somme, différence et produit
# Indice : utiliser int() pour convertir et print() pour afficher
def exercice2():
    a = int(input("Entrer nombre A : "))      # int() pour convertir
    b = int(input("Entrer nombre B : "))
    print(f"Somme : {a + b}")                 # print() pour afficher
    print(f"Différence : {a - b}")
    print(f"Produit : {a * b}")


# =========== Exercice 3 ===========
# Demander à l’utilisateur une phrase
# Afficher la phrase complète et le nombre de caractères
# Indice : len() permet de compter le nombre de caractères dans une chaîne
def exercice3():
    phrase = input("Écrire une phrase : ")    # input() pour lire
    print(f"Phrase complète : {phrase}")
    print(f"Nombre de caractères : {len(phrase)}")  # len() pour compter


# =========== Exercice 4 ===========
# Demander à l’utilisateur son âge
# Calculer son année de naissance (2025 - âge) puis afficher
# Indice : utiliser int() pour convertir l'âge et print() pour afficher
def exercice4():
    age = int(input("Quel est ton âge ? "))   # int() pour convertir
    annee_naissance = 2025 - age
    print(f"Tu es né(e) en {annee_naissance}")  # print() pour afficher


# =========== Exercice 5 ===========
# Créer un mini-questionnaire avec 3 questions posées à l’utilisateur
# Afficher un résumé des réponses
# Indice : stocker les réponses dans des variables et afficher avec print()
def exercice5():
    sport = input("Quel est ton sport préféré ? ")    # input() pour lire
    couleur = input("Quelle est ta couleur préférée ? ")
    serie = input("Quelle est ta série préférée ? ")
    print(f"Résumé : sport={sport}, couleur={couleur}, série={serie}")  # print() pour afficher


# Exécution des exercices
# exercice1()
# exercice2()
# exercice3()
# exercice4()
# exercice5()
