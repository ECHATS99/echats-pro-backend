# ============================
# Chapitre 4 : Les boucles
# ============================

# =========== Exercice 1 ===========
# Affiche les nombres de 1 à 10 avec une boucle for.
def exercice1():
    for i in range(1, 11):        # range(1,11) génère 1 à 10 inclus
        print(i)


# =========== Exercice 2 ===========
# Affiche uniquement les nombres pairs de 1 à 20.
def exercice2():
    for i in range(1, 21):
        if i % 2 == 0:            # % 2 pour vérifier si pair
            print(i)


# =========== Exercice 3 ===========
# Demande un mot à l’utilisateur.
# Affiche chaque lettre du mot sur une ligne différente.
def exercice3():
    mot = input("Écrire un mot : ")
    for lettre in mot:            # boucle sur chaque caractère
        print(lettre)


# =========== Exercice 4 ===========
# Utilise une boucle while pour demander à l’utilisateur
# de deviner le nombre secret (par ex. 7).
# Continue tant qu’il n’a pas trouvé.
def exercice4():
    secret = 7
    devine = None
    while devine != secret:       # continue tant que ce n'est pas trouvé
        devine = int(input("Devine le nombre secret : "))
    print("Bravo ! Tu as trouvé le nombre secret.")


# =========== Exercice 5 ===========
# Demande un nombre n à l’utilisateur.
# Calcule la somme des entiers de 1 à n (1+2+3+...+n).
def exercice5():
    n = int(input("Écrire un nombre : "))
    somme = 0
    for i in range(1, n+1):      # additionner de 1 à n inclus
        somme += i
    print(f"La somme des entiers de 1 à {n} est {somme}")


# Exécution des exercices
# exercice1()
# exercice2()
# exercice3()
# exercice4()
# exercice5()
