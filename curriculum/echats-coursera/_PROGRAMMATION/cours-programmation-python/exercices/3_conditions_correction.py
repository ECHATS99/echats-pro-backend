# ============================
# Chapitre 3 : Les conditions
# ============================

# =========== Exercice 1 ===========
# Demande à l’utilisateur un nombre.
# Si le nombre est positif, affiche "Positif".
# Sinon, affiche "Négatif ou nul".
def exercice1():
    nombre = float(input("Écrire un nombre : "))  # input() + float() pour convertir
    if nombre > 0:                                # if pour condition
        print("Positif")
    else:
        print("Négatif ou nul")


# =========== Exercice 2 ===========
# Demande à l’utilisateur un âge.
# Si l’âge >= 18, affiche "Majeur".
# Sinon, affiche "Mineur".
def exercice2():
    age = int(input("Écrire votre âge : "))      # input() + int() pour convertir
    if age >= 18:                                 # if pour condition
        print("Majeur")
    else:
        print("Mineur")


# =========== Exercice 3 ===========
# Demande un mot à l’utilisateur.
# Si le mot est "python", affiche "Bravo !".
# Sinon, affiche "Raté !".
def exercice3():
    mot = input("Écrire un mot : ")
    if mot == "python":                           # == pour comparer
        print("Bravo !")
    else:
        print("Raté !")


# =========== Exercice 4 ===========
# Demande deux nombres à l’utilisateur.
# Affiche le plus grand des deux.
def exercice4():
    a = float(input("Écrire nombre A : "))
    b = float(input("Écrire nombre B : "))
    if a > b:                                     # if pour choisir le plus grand
        print(f"Le plus grand est {a}")
    else:
        print(f"Le plus grand est {b}")


# =========== Exercice 5 ===========
# Demande trois notes.
# Calcule la moyenne.
# Si moyenne >= 10 : "Réussi", sinon "Échoué".
def exercice5():
    note1 = float(input("Note 1 : "))
    note2 = float(input("Note 2 : "))
    note3 = float(input("Note 3 : "))
    moyenne = (note1 + note2 + note3) / 3        # Calcul de la moyenne
    if moyenne >= 10:
        print(f"Réussi (moyenne = {moyenne})")
    else:
        print(f"Échoué (moyenne = {moyenne})")


# Exécution des exercices
# exercice1()
# exercice2()
# exercice3()
# exercice4()
# exercice5()
