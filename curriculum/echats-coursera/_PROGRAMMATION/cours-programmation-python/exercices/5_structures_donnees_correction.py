# ============================
# Chapitre 5 : Structures de données
# ============================

# ======== A. Tableaux ========

# =========== Exercice 1 ===========
# Créer un tableau [5, 2, 9, 1, 7].
# Implémenter le tri par sélection à la main (sans utiliser sorted()).
def exercice1():
    tableau = [5, 2, 9, 1, 7]
    n = len(tableau)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if tableau[j] < tableau[min_index]:
                min_index = j
        tableau[i], tableau[min_index] = tableau[min_index], tableau[i]
    print("Tableau trié par sélection :", tableau)


# =========== Exercice 2 ===========
# Implémenter un "flag" :
# Parcourir un tableau et, si la valeur 0 est trouvée, afficher "Zéro trouvé !"
def exercice2():
    tableau = [3, 5, 0, 7, 2]
    for valeur in tableau:
        if valeur == 0:
            print("Zéro trouvé !")
            break


# =========== Exercice 3 ===========
# Implémenter le tri à bulles (bubble sort).
def exercice3():
    tableau = [5, 2, 9, 1, 7]
    n = len(tableau)
    for i in range(n):
        for j in range(0, n - i - 1):
            if tableau[j] > tableau[j + 1]:
                tableau[j], tableau[j + 1] = tableau[j + 1], tableau[j]
    print("Tableau trié par bulles :", tableau)


# =========== Exercice 4 ===========
# Implémenter une recherche dichotomique (binary search).
# Utiliser un tableau trié [1, 3, 5, 7, 9, 11].
# Demander à l’utilisateur un nombre et indiquer s’il est présent.
def exercice4():
    tableau = [1, 3, 5, 7, 9, 11]
    nombre = int(input("Entrez un nombre : "))
    gauche = 0
    droite = len(tableau) - 1
    trouve = False
    while gauche <= droite:
        milieu = (gauche + droite) // 2
        if tableau[milieu] == nombre:
            trouve = True
            break
        elif tableau[milieu] < nombre:
            gauche = milieu + 1
        else:
            droite = milieu - 1
    if trouve:
        print(f"{nombre} est présent dans le tableau.")
    else:
        print(f"{nombre} n'est pas présent dans le tableau.")


# =========== Exercice 5 ===========
# Créer un tableau 2D (3x3) rempli de nombres.
# Afficher la somme de chaque ligne.
def exercice5():
    tableau2D = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    for i, ligne in enumerate(tableau2D):
        somme = sum(ligne)
        print(f"Somme de la ligne {i} :", somme)


# ======== B. Listes ========

# =========== Exercice 6 ===========
# Créer une liste vide.
# Ajouter les nombres de 1 à 5 avec append().
def exercice6():
    liste = []
    for i in range(1, 6):
        liste.append(i)
    print("Liste après ajout :", liste)


# =========== Exercice 7 ===========
# Créer une liste ["pomme", "banane", "cerise"].
# Supprimer "banane".
def exercice7():
    liste = ["pomme", "banane", "cerise"]
    liste.remove("banane")
    print("Liste après suppression :", liste)


# ======== C. Dictionnaires ========

# =========== Exercice 8 ===========
# Créer un dictionnaire {"nom": "Alice", "age": 20}.
# Afficher le nom puis l’âge.
def exercice8():
    dico = {"nom": "Alice", "age": 20}
    print("Nom :", dico["nom"])
    print("Âge :", dico["age"])


# =========== Exercice 9 ===========
# Ajouter une clé "ville" avec une valeur au dictionnaire précédent.
def exercice9():
    dico = {"nom": "Alice", "age": 20}
    dico["ville"] = "Paris"
    print("Dictionnaire après ajout :", dico)


# ======== D. Tuples ========

# =========== Exercice 10 ===========
# Créer un tuple (3, 4).
# Afficher sa première valeur.
def exercice10():
    t = (3, 4)
    print("Première valeur du tuple :", t[0])


# ============================
# Exécution des exercices
# ============================

exercice1()
exercice2()
exercice3()
# Pour l'exercice 4, il faut entrer un nombre depuis le clavier
# exercice4()
exercice5()
exercice6()
exercice7()
exercice8()
exercice9()
exercice10()
