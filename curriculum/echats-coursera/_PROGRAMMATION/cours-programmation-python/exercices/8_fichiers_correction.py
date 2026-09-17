# ============================
# Chapitre 8 : Fichiers
# ============================

# =========== Exercice 1 ===========
# Écrire "Bonjour fichier !" dans un fichier texte.
def exercice1():
    with open("fichier.txt", "w") as f:
        f.write("Bonjour fichier !\n")

# =========== Exercice 2 ===========
# Lire le contenu du fichier texte et l'afficher.
def exercice2():
    with open("fichier.txt", "r") as f:
        contenu = f.read()
    print("Contenu du fichier :", contenu)

# =========== Exercice 3 ===========
# Demander à l’utilisateur une phrase.
# Écrire la phrase dans un fichier "sortie.txt".
def exercice3():
    phrase = input("Entrez une phrase : ")
    with open("sortie.txt", "w") as f:
        f.write(phrase + "\n")

# =========== Exercice 4 ===========
# Lire le fichier "sortie.txt" et compter le nombre de mots.
def exercice4():
    with open("sortie.txt", "r") as f:
        texte = f.read()
    mots = texte.split()
    print("Nombre de mots :", len(mots))

# =========== Exercice 5 ===========
# Écrire dans un fichier plusieurs lignes de nombres.
# Puis relire le fichier et calculer la somme des nombres.
def exercice5():
    nombres = [3, 7, 1, 5, 10]
    with open("nombres.txt", "w") as f:
        for n in nombres:
            f.write(str(n) + "\n")
    somme = 0
    with open("nombres.txt", "r") as f:
        for ligne in f:
            somme += int(ligne.strip())
    print("Somme des nombres :", somme)


# ============================
# Exécution des exercices
# ============================

exercice1()
exercice2()
exercice3()
exercice4()
exercice5()
