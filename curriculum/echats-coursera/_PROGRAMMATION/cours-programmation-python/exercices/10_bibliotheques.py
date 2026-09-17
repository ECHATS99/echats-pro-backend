# ============================
# Chapitre 10 : Bibliothèques
# ============================

# =========== Exercice 1 ===========
# Importer la bibliothèque math et afficher la racine carrée de 25.
def exercice1():
    import math
    print("Racine carrée de 25 :", math.sqrt(25))


# =========== Exercice 2 ===========
# Importer la bibliothèque random.
# Afficher un nombre aléatoire entre 1 et 10.
def exercice2():
    import random
    print("Nombre aléatoire entre 1 et 10 :", random.randint(1, 10))


# =========== Exercice 3 ===========
# Utiliser datetime pour afficher la date et l’heure actuelles.
def exercice3():
    from datetime import datetime
    maintenant = datetime.now()
    print("Date et heure actuelles :", maintenant)


# =========== Exercice 4 ===========
# Utiliser requests (à installer) pour récupérer le code source de "https://example.com".
def exercice4():
    import requests
    url = "https://example.com"
    response = requests.get(url)
    print("Code source :", response.text[:200], "...")  # affiche les 200 premiers caractères


# =========== Exercice 5 ===========
# Utiliser os pour lister les fichiers dans le dossier courant.
def exercice5():
    import os
    fichiers = os.listdir(".")
    print("Fichiers dans le dossier courant :", fichiers)


# ============================
# Exécution des exercices
# ============================

exercice1()
exercice2()
exercice3()
exercice4()
exercice5()
