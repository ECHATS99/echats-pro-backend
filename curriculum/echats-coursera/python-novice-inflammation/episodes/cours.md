# Table des matières

### Cours

0. [Qu'est-ce qu'un programme, et quel est l'intérêt de Python ?](#0-quest-ce-quun-programme-et-quel-est-lintérêt-de-python)
1. [Variables](#1-variables)
   1. [Qu'est-ce qu'une variable ?](#a-quest-ce-quune-variable)
   2. [Comment les utiliser ?](#b-comment-les-utiliser)
   3. [Les types des variables](#c-les-types-des-variables)
   4. [Conversions entre types](#d-conversions-entre-types)
2. [Lecture et écriture](#2-lecture-et-écriture)
   1. [La communication avec un ordinateur](#a-la-communication-avec-un-ordinateur)
   2. [Comment utiliser la lecture et l'écriture](#b-comment-utiliser-la-lecture-et-lécriture)
3. [Les conditions](#3-les-conditions)
   1. [Qu'est-ce qu'une condition ?](#a-quest-ce-quune-condition)
   2. [Comment faire une condition ?](#b-comment-faire-une-condition)
      - [Introduction à l’algèbre booléenne](#a-introduction-à-lalgèbre-booléenne)
      - [Écrire une condition](#b-écrire-une-condition)
4. [Les boucles](#4-les-boucles)
   1. [Qu'est-ce qu'une boucle ?](#a-quest-ce-quune-boucle)
   2. [Comment faire une boucle ?](#b-comment-faire-une-boucle)
5. [Structures de données](#5-structures-de-données)
   1. [Tableaux](#a-tableaux)
      - [Tri par sélection](#a-tri-par-sélection)
      - [Flag](#b-flag)
      - [Tri à bulles](#c-tri-à-bulles)
      - [Recherche dichotomique](#d-recherche-dichotomique)
      - [Tableaux multidimensionnels](#e-tableaux-multidimensionnels)
   2. [Listes](#b-listes)
   3. [Dictionnaires](#c-dictionnaires)
   4. [Tuples](#d-tuples)
6. [Fonctions](#6-fonctions)
7. [Classes](#7-classes)
8. [Fichiers](#8-fichiers)
   - [Modes d'ouverture](#81-modes-douverture-des-fichiers)
   - [Écriture](#82-écriture-dans-un-fichier)
   - [Lecture](#83-lecture-dun-fichier)
   - [Lecture et écriture combinées](#84-lecture-et-écriture-combinées)
   - [Fichiers binaires](#85-manipulation-de-fichiers-binaires)
   - [Bonnes pratiques](#86-bonnes-pratiques)
9. [Les virtual environments](#9-virtual-environments)
10. [Bibliothèques](#10-bibliothèques)

### Appendice

1. [Annexe A : Utilisation du terminal (CMD / PowerShell)](#annexe-a--utilisation-du-terminal-cmd--powershell)
2. [Annexe B : Raccourcis utiles dans VSCode](#annexe-b--raccourcis-utiles-dans-vscode)
3. [Annexe C : Le binaire](#annexe-c--le-binaire)
4. [Annexe D : le pseudo-code](#annexe-d--le-pseudo-code)



# Cours de programmation en Python

## 0. Qu'est-ce qu'un programme, et quel est l'intérêt de Python ?

Un ordinateur est une machine qui peut exécuter des instructions. Ces instructions sont des ordres précis que l’ordinateur suit pour effectuer un calcul, afficher quelque chose ou interagir avec l’utilisateur. On les regroupe dans ce que l'on appelle des **programmes**.

Un **programme** est une suite d’instructions que l’ordinateur exécute pour accomplir une tâche. Par exemple, calculer une moyenne, afficher un message, ou demander à l’utilisateur de saisir des informations.

**Python** est un langage de programmation très utilisé pour sa simplicité et sa lisibilité. Il permet :

* D’écrire du code clair et court.
* De manipuler facilement des nombres, des textes, et des données.
* De créer rapidement des programmes pour apprendre, tester ou automatiser des tâches.

## 1. Variables

### A. Qu'est-ce qu'une variable ?

Une variable est une **boîte nommée dans laquelle on peut stocker des informations**. Elle peut contenir un nombre, un texte, un vrai/faux, ou même un objet plus complexe.

Exemple :

```python
age = 15            # assigne le nombre 15 dans la variable "age"
nom = "Jean"        # assigne le texte "Jean" dans la variable "nom"
est_vrai = True     # assigne le booléen True dans la variable "est_vrai"
```

Ici, `age`, `nom` et `est_vrai` sont des variables. 

**Remarques importantes :**

* Le nom d’une variable doit commencer par une lettre ou un underscore `_`.
* On ne peut pas mettre d’espaces dans un nom de variable.
* Les variables sont sensibles à la casse : `age` ≠ `Age`.

### B. Comment les utiliser ?

Une fois qu’on a assigné une variable, on peut :

* Lire sa valeur : `print(age)`
* Modifier sa valeur : `age = age + 1`
* Combiner plusieurs variables :

```python
prenom = "Alice"                
nom = "Dupont"
fullname = prenom + " " + nom
print(f"Bonjour {fullname} !") # Affiche : "Bonjour Alice Dupont !"
```

On peut aussi faire des calculs avec des nombres :

```python
a = 5
b = 3
print(a)       # affiche 5
print(b)       # affiche 3
somme = a + b
produit = a * b
print("Somme :", somme)         # affiche 8
print("Produit :", produit)     # affiche 15
```

### C. Les types des variables

Chaque variable a un **type**, c’est-à-dire le genre de données qu’elle contient. Le type détermine **ce que l’on peut faire avec cette variable** et comment Python la traite. Si on fait une erreur de type, Python peut produire une erreur.

Il existe quatre principaux types :
- `int` : nombres entiers (ex. 15)
- `float` : nombres décimaux (ex. 19.99)
- `str` : textes ou chaînes de caractères (ex. "Alice")
- `bool` : valeurs vrai/faux (True / False)

#### a. Les nombres entiers (`int`)

* Ce sont des nombres sans virgule.
* Exemple :

```python
age = 15          # int : 15 est un entier
print(age)        # affiche 15
```

On peut faire toutes sortes de calculs avec des entiers :

```python
a = 10
b = 3
print(a + b)      # addition → 13
print(a - b)      # soustraction → 7
print(a * b)      # multiplication → 30
print(a // b)     # division entière → 3
print(a % b)      # reste de la division → 1
```

#### b. Les nombres décimaux (`float`)

* Ce sont des nombres avec une virgule (ou un point en Python).
* Exemple :

```python
prix = 19.99      # float : nombre décimal
print(prix)       # affiche 19.99
```

On peut aussi faire des calculs :

```python
total = prix * 3
print(total)      # affiche 59.97
```

#### c. Les textes (`str`)

* Ce sont des suites de caractères, comme des mots ou des phrases.
* Les chaînes de caractères s’écrivent entre **guillemets simples `'`** ou **guillemets doubles `"`**.
* Exemple :

```python
prenom = "Alice"
nom = 'Dupont'
print(prenom)     # affiche Alice
print(nom)        # affiche Dupont
```

On peut **concaténer** (coller) des chaînes :

```python
fullname = prenom + " " + nom
print(fullname)   # affiche Alice Dupont
```

On peut aussi répéter des chaînes avec `*` :

```python
echo = "Hi! " * 3
print(echo)       # affiche Hi! Hi! Hi! 
```

#### d. Les booléens (`bool`)

* Ce sont des valeurs **vraies ou fausses** : `True` ou `False`.
* On les utilise pour les conditions et les tests :

```python
est_mineur = True
peut_voter = False
print(est_mineur) # True
print(peut_voter) # False
```

Ils peuvent aussi résulter d’opérations de comparaison :

```python
age = 15
print(age >= 18)  # False
print(age < 18)   # True
```

### D. Conversions entre types

Parfois, on a besoin de **changer le type d’une variable** pour faire certains calculs ou manipulations. On appelle cela une **conversion**.

#### a. Convertir en entier (`int`)

* Transforme un nombre décimal ou un texte en entier (si possible).

```python
x = "15"        # x est une chaîne de caractères
y = int(x)      # conversion en entier
print(y + 5)    # 20
```

#### b. Convertir en décimal (`float`)

* Transforme un entier ou un texte en nombre à virgule :

```python
x = "19.99"
y = float(x)    # conversion en float
print(y + 0.01) # 20.0
```

* Attention : `"15.5"` ne peut pas être converti directement en `int`. Il faut d'abord le convertir en float.
```python
x = "15.5"
y = int(float(x))  # d'abord en float puis en int
print(y)           # affiche 15
```

#### c. Convertir en texte (`str`)

* Transforme un nombre ou un booléen en texte pour l’afficher facilement :

```python
age = 15
print("Tu as " + str(age) + " ans")  # concaténation possible
```

#### d. Convertir en booléen (`bool`)

* Transforme une valeur en vrai (`True`) ou faux (`False`).

```python
x = 0
y = bool(x)     # False car 0 est considéré comme faux
z = bool(5)     # True car tout nombre non nul est vrai
```

#### Résumé :

| Type    | Exemple          | Utilisation principale |
| ------- | ---------------- | ---------------------- |
| `int`   | `15`             | Nombres entiers        |
| `float` | `19.99`          | Nombres décimaux       |
| `str`   | `"Alice"`        | Textes, mots, phrases  |
| `bool`  | `True` / `False` | Vrai/faux, conditions  |


## 2. Lecture et écriture

### A. La communication avec un ordinateur

Pour interagir avec un programme, l’ordinateur a besoin d’**entrées** (ce que l’utilisateur fournit) et peut donner des **sorties** (ce qu’il affiche). On parle de **lecture** et d'**écriture**. La lecture est le fait que l'ordinateur lise une valeur que l'on lui communique tandis que l'écriture est le fait qu'il affiche une valeur qu'il possède. On utilise ces expressions du point de vue l'ordinateur :

- **Lecture** : "Je suis un ordinateur, je lis (je retiens) ce que l'utilisateur m'écrit"
- **Ecriture** : "Je suis un ordinateur, j'écris (j'affiche) ce que je retiens en mémoire

### B. Comment utiliser la lecture et l'écriture

En Python, `input()` permet de **lire des données** depuis l’utilisateur, et `print()` permet de **les afficher**.

```python
nom = input("Quel est ton nom ? ")
print("Bonjour", nom)
```

* On peut demander plusieurs informations et les stocker pour les réutiliser :

```python
sport = input("Quel est ton sport préféré ? ")
couleur = input("Quelle est ta couleur préférée ? ")
serie = input("Quelle est ta série préférée ? ")
print(f"Résumé : sport={sport}, couleur={couleur}, série={serie}")
```

* Les valeurs lues avec `input()` sont toujours du texte (**str**).
* Lire un nombre avec `input()` renvoie toujours un texte. Il résulte que les conversions vues dans le chapitre précédent sont indispensables pour faire des calculs avec les valeurs entrées par les utilisateurs. Il faut convertir les nombres entrés **int** ou **float**. 

```python
age = input("Ton âge : ")   # age est un str
age = int(age)               # maintenant age est un int
print(age + 1)               # on peut calculer
```

```python
a = int(input("Nombre A : "))          # entier
b = float(input("Nombre B : "))        # nombre décimal
somme = a + b
print(f"La somme est {somme}")
```

## 3. Les conditions


### A. Qu’est-ce qu’une condition ?

Une **condition** permet au programme de **prendre des décisions** selon certaines règles.

Exemple simple :

```python
age = 17
if age >= 18:
    print("Majeur")
else:
    print("Mineur")
```

Ici, Python teste si `age >= 18`.

* Si c’est vrai (`True`) : exécute le bloc `print("Majeur")`.
* Sinon (`False`) : exécute le bloc `else`.

### B. Comment faire une condition ?

#### a. Introduction à l’algèbre booléenne

* Une condition renvoie **True** (vrai) ou **False** (faux).
* Opérateurs courants :

  * `==` : égal à
  * `!=` : différent de
  * `>`  : supérieur à
  * `<`  : inférieur à
  * `>=` : supérieur ou égal
  * `<=` : inférieur ou égal

#### b. Écrire une condition

```python
mot = input("Écris un mot : ")
if mot == "python":     # Si la valeur de mot est égale à "python" alors...
    print("Bravo !")    # on écrit "Bravo !"
else:                   # sinon...
    print("Raté !")     # on écrit  "Raté !"
```

Autre exemple avec deux nombres :

```python
a = 5
b = 8
if a > b:                               # Si a est plus grand que b alors...
    print(f"Le plus grand est {a}")     # on écrit "Le plus grand est {a}
else:                                   # sinon...
    print(f"Le plus grand est {b}")     # on écrit "Le plus grand est {b}
```

* On peut combiner les conditions pour plusieurs cas avec `elif` :

```python
note = float(input("Note : "))
if note >= 16:
    print("Très bien")
elif note >= 14:
    print("Bien")
elif note >= 12:
    print("Assez bien")
elif note >= 10:
    print("Réussi")
else:
    print("Echec")
```



### C. Combiner plusieurs conditions

Parfois, il faut vérifier **plusieurs critères à la fois**. Pour ça, on utilise les opérateurs logiques :

* `and` → **et** : toutes les conditions doivent être vraies
* `or` → **ou** : au moins une condition doit être vraie
* `not` → **non** : inverse le résultat d’une condition

#### a. Exemple avec `and` (et)

```python
age = 20
carte = True

if age >= 18 and carte:
    print("Vous pouvez entrer")
else:
    print("Accès refusé")
```

Explications :

* `age >= 18 and carte` → les deux conditions doivent être vraies pour entrer dans le `if`.
* Si une seule est fausse, le bloc `else` est exécuté.

#### b. Exemple avec `or` (ou)

```python
jour = "samedi"
vacances = False

if jour == "samedi" or vacances:
    print("Repos !")
else:
    print("Travail...")
```

Explications :

* Avec `or`, si **l’une des conditions** est vraie, le bloc `if` est exécuté.
* Ici, le message "Repos !" s’affiche si c’est samedi **ou** si c’est les vacances.

#### c. Exemple avec `not` (non)

```python
connecte = False

if not connecte:
    print("Veuillez vous connecter")
else:
    print("Bienvenue !")
```

Explications :

* `not connecte` inverse la valeur de `connecte`.
* Comme `connecte` est `False`, `not connecte` devient `True` → exécute le bloc `if`.

#### d. Combiner plusieurs opérateurs

```python
age = 25
carte = True
jour = "lundi"

if (age >= 18 and carte) and (jour != "dimanche"):
    print("Entrée autorisée")
else:
    print("Accès refusé")
```

* On peut combiner `and`, `or` et `not` en même temps.
* Les parenthèses permettent de **clarifier l’ordre** des opérations.

## 4. Les boucles

### A. Qu’est-ce qu’une boucle ?

Une **boucle** permet de répéter une action plusieurs fois sans écrire plusieurs fois la même instruction.

Exemple :

```python
for i in range(1, 6):
    print(i)
```

Cela affiche 1, 2, 3, 4, 5.

### B. Comment faire une boucle ?

* **Boucles définies (`for`)** : on sait à l’avance combien de fois répéter.

```python
# afficher les nombres pairs de 1 à 10
for i in range(1, 11):
    if i % 2 == 0:
        print(i)
```

* **Boucles indéfinies (`while`)** : on répète jusqu’à ce qu’une condition soit remplie.

```python
secret = 7
devine = None
while devine != secret:
    devine = int(input("Devine le nombre secret : "))
print("Bravo !")
```

**Remarque** : Parfois, un mauvais programme peut entraîner une boucle infinie. Si la boucle infinie peut être désirable dans certains cas, il faut bien veiller à ce que les boucles soient écrites correctement.

* On peut également parcourir une chaîne de caractères :

```python
mot = input("Écris un mot : ")
for lettre in mot:
    print(lettre)
```

* Calculer une somme avec une boucle :

```python
n = int(input("Nombre : "))
somme = 0
for i in range(1, n+1):
    somme += i
print(f"La somme de 1 à {n} est {somme}")
```

## 5. Structures de données

En programmation, il est rare de travailler avec **une seule variable** à la fois. Souvent, on doit stocker et manipuler **plusieurs valeurs**. Pour cela, Python propose des structures de données.

### A. Tableaux

Un **tableau** (ou `list` en Python) est une collection de valeurs **ordonnées**, accessibles par un **indice**.

Exemple :

```python
nombres = [5, 2, 9, 1, 7]  # tableau contenant 5 nombres
print(nombres[0])           # premier élément → 5
print(nombres[3])           # quatrième élément → 1
```

#### a. Tri par sélection

Le **tri par sélection** consiste à parcourir le tableau pour trouver le plus petit élément, le mettre en première position, puis répéter pour les éléments suivants.

```python
nombres = [5, 2, 9, 1, 7]

for i in range(len(nombres)):
    min_index = i
    for j in range(i+1, len(nombres)):
        if nombres[j] < nombres[min_index]:
            min_index = j
    nombres[i], nombres[min_index] = nombres[min_index], nombres[i]

print(nombres)  # affiche [1, 2, 5, 7, 9]
```

#### b. Flag

Un **flag** est une variable qui indique si quelque chose a été trouvé ou pas.

```python
nombres = [3, 0, 5, 8]
trouve = False
for n in nombres:
    if n == 0:
        trouve = True
        break
if trouve:
    print("Zéro trouvé !")
```

#### c. Tri à bulles

Le **tri à bulles** compare chaque élément avec le suivant et échange si nécessaire, en répétant le processus plusieurs fois.

```python
nombres = [5, 2, 9, 1, 7]
for i in range(len(nombres)):
    for j in range(len(nombres)-1-i):
        if nombres[j] > nombres[j+1]:
            nombres[j], nombres[j+1] = nombres[j+1], nombres[j]
print(nombres)
```

#### d. Recherche dichotomique

La **recherche dichotomique** fonctionne sur un **tableau trié**. On compare l’élément du milieu et on réduit la recherche à la moitié pertinente.

```python
tableau = [1, 3, 5, 7, 9, 11]
x = int(input("Nombre à chercher : "))
debut = 0
fin = len(tableau) - 1
trouve = False

while debut <= fin:
    milieu = (debut + fin) // 2
    if tableau[milieu] == x:
        trouve = True
        break
    elif tableau[milieu] < x:
        debut = milieu + 1
    else:
        fin = milieu - 1

print("Trouvé !" if trouve else "Non trouvé")
```

#### e. Tableaux multidimensionnels

On peut avoir des **tableaux à plusieurs dimensions**, comme un tableau 2D (liste de listes).

```python
matrice = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for ligne in matrice:
    print(sum(ligne))  # somme de chaque ligne
```

### B. Listes

Une **liste** est similaire à un tableau, mais plus flexible : on peut ajouter ou supprimer des éléments facilement.

```python
fruits = []
fruits.append("pomme")
fruits.append("banane")
fruits.append("cerise")
fruits.remove("banane")
print(fruits)  # ['pomme', 'cerise']
```

### C. Dictionnaires

Un **dictionnaire** stocke des **paires clé → valeur**. On peut accéder à une valeur via sa clé.

```python
personne = {"nom": "Alice", "age": 20}
print(personne["nom"])  # Alice
print(personne["age"])  # 20

personne["ville"] = "Paris"  # ajouter une clé
print(personne)
```

### D. Tuples

Un **tuple** est une collection de valeurs **immuable** (on ne peut pas modifier les éléments après création).

```python
coord = (3, 4)
print(coord[0])  # 3
```

## 6. Fonctions

Une **fonction** est un bloc de code que l’on peut réutiliser pour effectuer une tâche précise.

```python
def bonjour():
    print("Bonjour !")

bonjour()  # Appel de la fonction
```

### Fonctions avec paramètres

```python
def saluer(nom):
    print(f"Bonjour {nom} !")

saluer("Alice")
```

### Fonctions qui retournent une valeur

```python
def somme(a, b):
    return a + b

resultat = somme(3, 4)
print(resultat)  # 7
```

### Fonctions utiles pour apprendre

* Factorielle avec boucle :

```python
def factorielle(n):
    resultat = 1
    for i in range(1, n+1):
        resultat *= i
    return resultat
```

* Tester si un nombre est pair :

```python
def est_pair(n):
    return n % 2 == 0
```

## 7. Classes

Une **classe** est un modèle pour créer des **objets**. Un objet est une instance de la classe.

```python
class Chien:
    def __init__(self, nom):
        self.nom = nom

chien1 = Chien("Rex")
print(chien1.nom)  # Rex
```

### Méthodes

Une **méthode** est une fonction dans une classe.

```python
class Chien:
    def __init__(self, nom):
        self.nom = nom
    def aboyer(self):
        print("Woof !")

chien1 = Chien("Rex")
chien1.aboyer()
```

### Références vs variables simples

* Variables simples : copier une valeur crée une **nouvelle variable indépendante**.
* Objets : copier une variable crée une **référence vers le même objet**.

```python
a = 10
b = a
a = 20
print(a, b)  # 20 10

class MaClasse:
    pass
obj1 = MaClasse()
obj2 = obj1
obj1.attr = 5
print(obj2.attr)  # 5 (même objet)
```

### Exemple avec rectangle

```python
class Rectangle:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
    def aire(self):
        return self.largeur * self.hauteur

rect = Rectangle(4, 5)
print(rect.aire())  # 20
```

## 8. Fichiers

Un fichier est un **conteneur de données stocké sur le disque**. En Python, on peut **lire** son contenu, **écrire** dedans ou **ajouter** du texte sans supprimer ce qui existe déjà. Les fichiers peuvent être **texte** ou **binaire**. 

Pour manipuler un fichier, on utilise la fonction `open()`, qui renvoie un objet fichier. Toujours fermer le fichier après usage, ou mieux, utiliser `with` pour gérer automatiquement la fermeture.

### 8.1 Modes d'ouverture des fichiers

| Mode | Description |
|------|-------------|
| `"r"` | Lecture seule. Le fichier doit exister, sinon une erreur est levée. |
| `"w"` | Écriture seule. Crée le fichier s'il n'existe pas, sinon écrase le contenu existant. |
| `"a"` | Ajout à la fin du fichier. Crée le fichier s'il n'existe pas. |
| `"x"` | Création exclusive. Échoue si le fichier existe déjà. |
| `"rb"` | Lecture binaire. Utilisé pour les fichiers non texte (images, sons…). |
| `"wb"` | Écriture binaire. Écrase le fichier ou le crée. |
| `"ab"` | Ajout binaire. |
| `"r+"` | Lecture et écriture. Le fichier doit exister. |
| `"w+"` | Lecture et écriture. Écrase le fichier ou le crée. |
| `"a+"` | Lecture et ajout à la fin du fichier. Crée le fichier s’il n’existe pas. |

---

### 8.2 Écriture dans un fichier

```python
# Mode "w" : écriture (écrase le contenu existant)
with open("monfichier.txt", "w", encoding="utf-8") as f:
    f.write("Bonjour fichier !\n")
    f.write("Une deuxième ligne.\n")
````

```python
# Mode "a" : ajout à la fin
with open("monfichier.txt", "a", encoding="utf-8") as f:
    f.write("Une ligne ajoutée à la fin.\n")
```

> **Astuce :** Toujours préciser `encoding="utf-8"` pour éviter les problèmes avec les accents ou caractères spéciaux.

---

### 8.3 Lecture d'un fichier

```python
# Lecture complète
with open("monfichier.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
print(contenu)
```

```python
# Lecture ligne par ligne
with open("monfichier.txt", "r", encoding="utf-8") as f:
    for ligne in f:
        print(ligne.strip())  # strip() supprime le saut de ligne à la fin
```

```python
# Lecture dans une liste
with open("monfichier.txt", "r", encoding="utf-8") as f:
    lignes = f.readlines()
print(lignes)
```

---

### 8.4 Lecture et écriture combinées

```python
# Mode "r+" : lecture et écriture
with open("monfichier.txt", "r+", encoding="utf-8") as f:
    print(f.read())  # lire le contenu
    f.write("Une nouvelle ligne à la fin.\n")  # ajouter du contenu
```

---

### 8.5 Manipulation de fichiers binaires

```python
# Écriture binaire
with open("image.png", "wb") as f:
    f.write(b"\x89PNG...")  # contenu binaire

# Lecture binaire
with open("image.png", "rb") as f:
    data = f.read()
print(data[:10])  # affiche les 10 premiers octets
```

**Résumé :**

* Texte → `"r"`, `"w"`, `"a"`, `"r+"`, `"w+"`, `"a+"`
* Binaire → `"rb"`, `"wb"`, `"ab"`, `"rb+"`, `"wb+"`, `"ab+"`

### 8.6 Bonnes pratiques

1. Toujours utiliser `with` pour ouvrir les fichiers. Cela ferme automatiquement le fichier, même en cas d’erreur.
2. Toujours préciser l’encodage (`utf-8`) pour les fichiers texte.
3. Préférer l’ajout (`"a"` ou `"a+"`) si on ne veut pas écraser le contenu existant.
4. Utiliser les modes binaires pour les fichiers non texte (images, sons, PDF…).
5. Éviter les chemins relatifs compliqués pour ne pas se perdre dans l’arborescence.

## 9. Virtual Environments

Un **virtual environment** est un espace isolé pour Python. Il permet d’installer des bibliothèques sans modifier le Python global.

```bash
# créer un environnement
python -m venv monenv

# activer
# Windows
monenv\Scripts\activate
# Linux / Mac
source monenv/bin/activate

# installer une bibliothèque
pip install requests

# désactiver
deactivate
```

## 10. Bibliothèques

Une **bibliothèque** est un ensemble de fonctions ou classes prêtes à l’emploi.

```python
# math
import math
print(math.sqrt(25))  # 5.0

# random
import random
print(random.randint(1, 10))

# datetime
from datetime import datetime
print(datetime.now())

# requests (installer via pip)
import requests
r = requests.get("https://example.com")
print(r.text[:100])

# os
import os
print(os.listdir("."))
```

# Appendice

## Annexe A : Utilisation du terminal (CMD / PowerShell)

### 1. Qu’est-ce qu’un terminal ?

Un **terminal** (ou console) est une fenêtre où tu peux **taper des commandes pour communiquer directement avec l’ordinateur**.
C’est comme parler à l’ordinateur en langage texte au lieu de cliquer avec la souris.

En Python, on l’utilise pour :

* Lancer un programme : `python mon_programme.py`
* Installer ou gérer des bibliothèques : `pip install nom_librairie`
* Naviguer dans les dossiers de ton ordinateur : `cd`
* Créer ou supprimer des dossiers : `mkdir`, `rmdir`

### 2. Commandes indispensables

| Commande                                 | Description                        | Exemple                   |
| ---------------------------------------- | ---------------------------------- | ------------------------- |
| `cd`                                     | Changer de dossier                 | `cd Documents\Python`     |
| `cd ..`                                  | Remonter d’un dossier              | `cd ..`                   |
| `dir` (Windows) / `ls` (Linux/Mac)       | Lister les fichiers du dossier     | `dir`                     |
| `mkdir`                                  | Créer un dossier                   | `mkdir mon_dossier`       |
| `rmdir`                                  | Supprimer un dossier vide          | `rmdir mon_dossier`       |
| `python mon_programme.py`                | Lancer un programme Python         | `python test.py`          |
| `python -m venv monenv`                  | Créer un environnement virtuel     | `python -m venv env`      |
| `monenv\Scripts\activate` (Windows)      | Activer l’environnement virtuel    | `env\Scripts\activate`    |
| `source monenv/bin/activate` (Linux/Mac) | Activer l’environnement virtuel    | `source env/bin/activate` |
| `pip install nom_librairie`              | Installer une bibliothèque         | `pip install requests`    |
| `pip list`                               | Voir les bibliothèques installées  | `pip list`                |
| `deactivate`                             | Désactiver l’environnement virtuel | `deactivate`              |

### 3. Raccourcis utiles dans le terminal

* **Flèche haut / bas** : rappeler les commandes précédentes
* **Tab** : auto-complétion des noms de fichiers ou dossiers
* **Ctrl+C** : arrêter un programme en cours (par exemple si une boucle tourne trop longtemps)

## Annexe B : Raccourcis utiles dans VSCode

VSCode est l’éditeur de code que tu utilises pour écrire tes programmes Python. Ces raccourcis rendent l’écriture plus rapide et pratique :

| Raccourci                 | Action                                                                        |
| ------------------------- | ----------------------------------------------------------------------------- |
| `Ctrl + X`                | Couper (supprime le texte sélectionné et le met dans le presse-papiers)       |
| `Ctrl + C`                | Copier le texte sélectionné                                                   |
| `Ctrl + V`                | Coller le texte depuis le presse-papiers                                      |
| `Ctrl + Z`                | Annuler la dernière action                                                    |
| `Ctrl + Y`                | Rétablir l’action annulée (inverse de Ctrl+Z)                                 |
| `Ctrl + /`                | Commenter / décommenter une ligne ou une sélection                            |
| `Ctrl + Backspace`        | Supprimer le mot à gauche du curseur                                          |
| `Ctrl + Shift + P`        | Ouvrir la palette de commandes (très utile pour chercher une commande VSCode) |
| `Alt + Flèche haut / bas` | Déplacer une ligne de code vers le haut ou le bas                             |
| `Ctrl + S`                | Sauvegarder le fichier actuel                                                 |

### Conseils pour ne pas se perdre :

1. Toujours **ouvrir VSCode dans le dossier de ton projet** : `cd mon_dossier` dans le terminal puis `code .` (ouvre le dossier dans VSCode).
2. Toujours **activer l’environnement virtuel** avant d’installer des bibliothèques.
3. Si un programme ne marche pas, vérifier que tu es **dans le bon dossier** et que tu as bien **sauvegardé ton fichier** (`Ctrl+S`).

## Annexe C : Le binaire

Le **binaire** est le langage que l’ordinateur comprend vraiment : il n’utilise que **deux symboles** : `0` et `1`.

* Chaque chiffre binaire est appelé un **bit**.
* Un groupe de 8 bits forme un **octet**, qui peut représenter un nombre, une lettre ou une couleur.

**Exemples :**

* Le nombre 5 en binaire → `101`
* Le nombre 10 en binaire → `1010`
* La lettre 'A' en binaire (ASCII) → `01000001`

### Pourquoi le binaire ?

* Les ordinateurs utilisent des **circuits électroniques** qui sont **ON ou OFF**.
* ON → 1, OFF → 0.
* Tout ce que l’ordinateur fait (calcul, stockage, affichage) est **converti en binaire**.

### Utilité en Python

Même si Python nous cache la complexité du binaire, **il est parfois utile de connaître et manipuler les nombres binaires**.

* Conversion d’un entier en binaire : `bin()`

```python
x = 13
print(bin(x))  # affiche '0b1101' → 13 en binaire
```

* Conversion d’un binaire en entier : `int()` avec base 2

```python
binaire = "1101"
nombre = int(binaire, 2)
print(nombre)  # affiche 13
```

* Manipulation bit à bit (utile pour certaines opérations sur des drapeaux, masques ou cryptographie) :

```python
a = 5       # 0101 en binaire
b = 3       # 0011 en binaire

print(a & b)  # AND bit à bit → 0101 & 0011 = 0001 → 1
print(a | b)  # OR bit à bit  → 0101 | 0011 = 0111 → 7
print(a ^ b)  # XOR bit à bit → 0101 ^ 0011 = 0110 → 6
print(a << 1) # décalage à gauche → 0101 << 1 = 1010 → 10
print(a >> 1) # décalage à droite → 0101 >> 1 = 0010 → 2
```

* Applications concrètes :

  * Cryptographie simple et jeux
  * Optimisation des calculs
  * Communication avec du matériel ou des fichiers binaires

### Petit exercice pour comprendre

Convertir 13 en binaire :

1. 13 ÷ 2 = 6 reste 1 → bit le plus à droite
2. 6 ÷ 2 = 3 reste 0
3. 3 ÷ 2 = 1 reste 1
4. 1 ÷ 2 = 0 reste 1 → bit le plus à gauche

**Résultat : 13 en binaire = 1101**

## Annexe D : le pseudo-code

Le **pseudo-code** est une manière d’écrire un programme **sans se soucier de la syntaxe exacte d’un langage** comme Python. On utilise des mots simples pour expliquer ce que le programme doit faire.

### A. Intérêt du pseudo-code

* Permet de **planifier un programme** avant de coder.
* Aide à **comprendre la logique** et les étapes à suivre.
* Facilite le passage vers n’importe quel langage de programmation.
* Permet de **réfléchir à l’algorithme** sans se bloquer sur les détails techniques.

**Exemple :**
On veut écrire un programme qui demande un nombre à l’utilisateur et dit s’il est pair ou impair.

En pseudo-code, on peut écrire :

```
DEBUT
    DEMANDER un nombre à l'utilisateur
    SI le nombre est divisible par 2
        AFFICHER "Le nombre est pair"
    SINON
        AFFICHER "Le nombre est impair"
FIN
```

Puis, en Python, ça devient :

```python
n = int(input("Nombre : "))
if n % 2 == 0:
    print("Le nombre est pair")
else:
    print("Le nombre est impair")
```

### B. Comment écrire en pseudo-code

Quelques conseils pour rédiger un pseudo-code :

1. Utiliser des **mots simples et clairs** : `DEBUT`, `FIN`, `SI`, `SINON`, `TANT QUE`, `POUR`.
2. Écrire **une instruction par ligne**.
3. Indenter les blocs pour montrer les actions **à l’intérieur d’une condition ou d’une boucle**.
4. Ne pas se soucier de la syntaxe exacte d’un langage.

**Exemple avec une boucle :**

```
DEBUT
    INITIALISER somme à 0
    POUR i de 1 à 5
        AJOUTER i à somme
    FIN POUR
    AFFICHER somme
FIN
```

Ce pseudo-code correspond en Python à :

```python
somme = 0
for i in range(1, 6):
    somme += i
print(somme)
```