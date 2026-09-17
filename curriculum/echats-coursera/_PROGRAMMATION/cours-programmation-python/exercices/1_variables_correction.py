# ============================
# Chapitre 1 : Variables
# ============================

# =========== Exercice 1 ===========
# Créer une variable age contenant son âge puis l'afficher.
# Modifier la valeur de age pour simuler un an de plus puis l'afficher.
# Créer une variable nom contenant son prénom puis afficher : "Bonjour, je m’appelle <nom> !"
def exercice1():
    age = 24
    age = age + 1  # On peut aussi écrire age += 1
    print(age)
    nom = "Louis"
    print(f"Bonjour, je m'appelle {nom}")


# =========== Exercice 2 ===========
# Créer deux variables a et b avec des nombres au choix.
# Calculer et afficher :
#  - leur somme
#  - leur différence
#  - leur produit
#  - leur quotient
def exercice2():
    a = 34
    b = 72
    somme = a + b
    difference = a - b
    produit = a * b
    quotient = a / b
    print(f"Somme: {somme}")
    print(f"Différence: {difference}")
    print(f"Produit: {produit}")
    print(f"Quotient: {quotient}")


# =========== Exercice 3 ===========
# Créer deux variables x et y avec des nombres.
# Échanger leurs valeurs puis afficher les nouvelles valeurs.
def exercice3():
    x = 5
    y = 10
    print(f"Avant échange: x={x}, y={y}")
    temp = x
    x = y
    y = temp
    print(f"Après échange: x={x}, y={y}")


# =========== Exercice 4 ===========
# Créer une variable prenom et une variable nom.
# Les concaténer dans une variable fullname avec un espace puis afficher : "Bonjour <fullname> !"
def exercice4():
    prenom = "Alice"
    nom = "Dupont"
    fullname = prenom + " " + nom
    print(f"Bonjour {fullname} !")


# =========== Exercice 5 ===========
# Créer une variable prix_unitaire et une variable quantite.
# Calculer le prix total puis l'afficher.
# Modifier la valeur de prix_unitaire puis recalculer et réafficher le prix total.
def exercice5():
    prix_unitaire = 12
    quantite = 5
    total = prix_unitaire * quantite
    print(f"Prix total: {total}")
    prix_unitaire = 15
    total = prix_unitaire * quantite
    print(f"Nouveau prix total: {total}")


# =========== Exercice 6 ===========
# Créer une variable contenant une température en Celsius.
# Convertir cette température en Fahrenheit avec la formule : F = C * 9/5 + 32 puis l'afficher.
def exercice6():
    celsius = 20
    fahrenheit = celsius * 9 / 5 + 32
    print(f"{celsius}°C = {fahrenheit}°F")


# =========== Exercice 7 ===========
# Créer une variable pi et une variable rayon.
# Calculer l’aire d’un cercle (pi * rayon^2) puis l'afficher.
def exercice7():
    pi = 3.14159
    rayon = 5
    aire = pi * (rayon ** 2)  # rayon^2 s'écrit rayon**2 en Python
    print(f"Aire du cercle de rayon {rayon} = {aire}")


# Exécution des exercices
# exercice1()
# exercice2()
# exercice3()
# exercice4()
# exercice5()
# exercice6()
# exercice7()
