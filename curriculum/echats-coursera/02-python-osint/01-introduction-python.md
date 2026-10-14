---
title: "Introduction à Python"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 35
order: 1
category: "python"
tags: ["python", "introduction", "installation", "variables", "print", "input", "venv"]
prerequisites: ["10-commandes-linux-essentielles"]
learning_objectives:
  - "Expliquer pourquoi Python est le langage de référence en cybersécurité"
  - "Installer Python et exécuter un script depuis le terminal"
  - "Utiliser variables, print, input et commentaires"
  - "Lire un message d'erreur Python et créer un environnement virtuel"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Introduction à Python

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Expliquer pourquoi Python est le langage de référence en cybersécurité
- Installer Python et exécuter un script depuis le terminal
- Utiliser variables, `print`, `input` et commentaires
- Lire un message d'erreur Python et créer un environnement virtuel

## 📚 Prérequis

- Savoir utiliser un terminal (leçon 10 du module Réseau & Linux). Aucune expérience de programmation n'est nécessaire.

## 🧭 Introduction

Dans le module précédent, tu as automatisé des tâches avec Bash. Bash est excellent pour enchaîner des commandes, mais dès qu'il faut manipuler des données complexes, interroger un service web, analyser un fichier volumineux ou écrire un outil réutilisable, on se tourne vers un langage de programmation plus complet. En cybersécurité, ce langage est très souvent **Python**.

Pourquoi Python ? Parce qu'il est **lisible** (il ressemble à de l'anglais structuré), **rapide à écrire**, et surtout parce qu'il dispose d'un **écosystème énorme** : bibliothèques pour le réseau (`socket`, `requests`, `scapy`), l'analyse de données, la cryptographie (`hashlib`, `cryptography`), le web scraping, l'automatisation, l'intelligence artificielle. La plupart des outils de sécurité modernes ont une API ou un script Python : des outils de forensic comme Volatility, des frameworks d'analyse, des scripts de CTF, des outils OSINT.

Pour un défenseur, Python sert à analyser des journaux, enrichir des alertes, automatiser des vérifications. Pour un testeur d'intrusion (en cadre légal), il sert à écrire de petits outils sur mesure quand les outils existants ne suffisent pas. Pour un analyste OSINT, il sert à collecter et croiser des informations publiques. Dans ce module, tu vas apprendre Python **en l'appliquant à des problèmes de sécurité et de recherche d'information**.

## 📖 Concepts clés

### 1. Qu'est-ce que Python ?

Python est un langage **interprété** : tu écris du texte, et un programme appelé l'**interpréteur** l'exécute ligne par ligne. Pas besoin de compilation préalable. Il est :
- **généraliste** : web, scripts, données, sécurité, IA ;
- **multiplateforme** : Windows, Linux, macOS ;
- **gratuit et open source**.

Il existe deux grandes versions : Python 2 (abandonné depuis 2020) et **Python 3** (le seul à utiliser aujourd'hui). Dans ce cours, `python3` désigne toujours Python 3.

### 2. Installer Python

**Linux (Debian, Ubuntu, Kali)** : souvent déjà installé.

```bash
python3 --version
sudo apt update && sudo apt install python3 python3-pip python3-venv
```

**Windows** : télécharge l'installateur sur python.org et **coche la case « Add Python to PATH »** avant d'installer. Vérifie ensuite dans l'invite de commandes :

```bash
python --version
```

**macOS** : `brew install python` (avec Homebrew) ou l'installateur officiel.

Selon les systèmes, la commande s'appelle `python3` ou `python`. Utilise celle qui affiche une version commençant par 3.

### 3. Deux façons d'exécuter du Python

**a) Le mode interactif (REPL)** : tu tapes une instruction, tu vois le résultat immédiatement. Idéal pour tester.

```bash
python3
>>> 2 + 3
5
>>> print("Bonjour")
Bonjour
>>> exit()
```

Les symboles `>>>` sont l'invite de Python. On quitte avec `exit()` ou `Ctrl+D`.

**b) Un script** : un fichier texte avec l'extension `.py`.

```bash
nano bonjour.py        # ou n'importe quel éditeur
python3 bonjour.py
```

Pour écrire du code confortablement, utilise un éditeur comme **VS Code** (avec l'extension Python), **PyCharm Community**, ou **Thonny** (très simple pour débuter).

### 4. Ton premier programme

```python
# bonjour.py
print("Bonjour, monde !")
print("Bienvenue sur ECHATS PRO")
```

- `print()` affiche du texte à l'écran ;
- le texte est entre **guillemets** (simples `'...'` ou doubles `"..."`) ;
- `#` introduit un **commentaire**, ignoré par Python ; il sert à expliquer ton code.

### 5. Les variables

Une **variable** est un nom qui désigne une valeur gardée en mémoire. Analogie : une étiquette collée sur une boîte.

```python
nom = "Alice"
age = 25
taille = 1.68
est_etudiant = True

print(nom)
print("Age :", age)
```

Règles de nommage :
- lettres, chiffres et `_` uniquement ; **ne commence pas par un chiffre** ;
- sensible à la casse : `Nom` ≠ `nom` ;
- pas de mots réservés (`if`, `for`, `class`, `True`…) ;
- convention : **snake_case** (`adresse_ip`, `nombre_echecs`).

Choisis des noms **parlants** : `tentatives_echouees` vaut mieux que `t`. Un code lisible est un code plus facile à auditer.

On peut changer la valeur d'une variable à tout moment :

```python
compteur = 0
compteur = compteur + 1       # compteur vaut maintenant 1
compteur += 1                 # raccourci : maintenant 2
```

Python est à **typage dynamique** : tu n'as pas à déclarer le type (entier, texte…), il est déduit de la valeur. Tu peux le consulter avec `type()` :

```python
print(type(25))          # <class 'int'>
print(type("texte"))     # <class 'str'>
print(type(3.14))        # <class 'float'>
print(type(True))        # <class 'bool'>
```

### 6. Opérations de base

```python
a = 10
b = 3
print(a + b)     # 13  addition
print(a - b)     # 7   soustraction
print(a * b)     # 30  multiplication
print(a / b)     # 3.333...  division (résultat décimal)
print(a // b)    # 3   division entière
print(a % b)     # 1   reste (modulo)
print(a ** b)    # 1000  puissance
```

Pour le texte, `+` concatène (colle) et `*` répète :

```python
prenom = "Alice"
print("Bonjour " + prenom)
print("-" * 20)
```

### 7. Interagir : afficher et lire

`print()` accepte plusieurs valeurs et des options :

```python
print("Adresse IP :", "192.168.1.25")
print("A", "B", "C", sep="-")        # A-B-C
print("Sans retour à la ligne", end="")
```

Les **f-strings** (chaînes formatées) insèrent des variables dans du texte, et c'est la méthode recommandée :

```python
nom = "Alice"
port = 22
print(f"{nom} se connecte au port {port}")
```

`input()` lit ce que l'utilisateur tape. **Elle renvoie toujours du texte**, même si l'utilisateur saisit un nombre :

```python
nom = input("Ton prénom : ")
age_texte = input("Ton âge : ")
age = int(age_texte)              # conversion en entier
print(f"Dans 5 ans, tu auras {age + 5} ans")
```

Fonctions de conversion : `int()`, `float()`, `str()`, `bool()`.

### 8. Comprendre les erreurs

Tu vas rencontrer des erreurs : c'est normal, c'est même la façon d'apprendre. Python affiche une **trace d'appel** (*traceback*) :

```
Traceback (most recent call last):
  File "test.py", line 3, in <module>
    print(nom)
NameError: name 'nom' is not defined
```

Comment lire :
1. **Va à la dernière ligne** : le type d'erreur et le message (`NameError: name 'nom' is not defined`).
2. Regarde le **numéro de ligne** juste au-dessus (`line 3`).
3. Relis la ligne concernée.

Erreurs fréquentes :

| Erreur | Cause habituelle |
|---|---|
| `SyntaxError` | Faute d'écriture (parenthèse oubliée, `:` manquant, guillemet non fermé) |
| `NameError` | Variable utilisée avant d'être définie, ou faute de frappe dans le nom |
| `TypeError` | Opération sur des types incompatibles (`"5" + 3`) |
| `ValueError` | Valeur impossible à convertir (`int("abc")`) |
| `IndentationError` | Mauvais alignement des lignes |
| `ModuleNotFoundError` | Bibliothèque non installée |

Astuce : copier le **message d'erreur** dans un moteur de recherche donne presque toujours la réponse.

### 9. L'indentation : le signe distinctif de Python

Là où d'autres langages utilisent des accolades `{ }`, Python utilise l'**indentation** (les espaces au début de la ligne) pour délimiter des blocs de code. Tu la rencontreras dans la leçon 03 (conditions, boucles). Règle : **4 espaces par niveau**, jamais de mélange avec des tabulations.

### 10. Les modules et pip

Python vient avec une **bibliothèque standard** riche (`os`, `sys`, `datetime`, `random`, `hashlib`, `socket`, `json`, `re`…). On l'utilise avec `import` :

```python
import datetime
print(datetime.datetime.now())

import random
print(random.randint(1, 100))
```

Pour des bibliothèques tierces, on utilise **pip**, le gestionnaire de paquets :

```bash
pip install requests          # ou pip3 / python3 -m pip install requests
pip list
```

### 11. Les environnements virtuels

Quand on travaille sur plusieurs projets, chacun peut avoir besoin de versions différentes des mêmes bibliothèques. L'**environnement virtuel** (*venv*) isole les dépendances de chaque projet :

```bash
python3 -m venv mon_env             # crée l'environnement
source mon_env/bin/activate         # active (Linux/macOS)
# Windows : mon_env\Scripts\activate
pip install requests
deactivate                          # quitte l'environnement
```

Une fois activé, l'invite affiche `(mon_env)`. Bonnes pratiques de sécurité : **un environnement par projet**, ne jamais installer de paquets en root avec `sudo pip`, et ne n'installer que des paquets dont tu connais l'origine (des paquets malveillants aux noms trompeurs existent sur les dépôts publics : c'est le *typosquatting* de paquets).

### 12. Python et cybersécurité : un avant-goût

Un exemple concret, qui calcule l'empreinte (hash) d'un mot :

```python
import hashlib

mot = "ECHATS"
empreinte = hashlib.sha256(mot.encode()).hexdigest()
print(f"SHA-256 de {mot} : {empreinte}")
```

Tu n'as pas besoin de tout comprendre maintenant : tu verras les hachages dans le module Cryptographie. L'important est de constater qu'en quelques lignes, Python réalise une opération de sécurité réelle.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : les programmes de cette leçon n'interagissent qu'avec ta propre machine. Quand tu écriras des outils qui contactent d'autres systèmes (leçons suivantes), tu ne les testeras que sur des cibles autorisées.

### Exercice 1 — Premier script

1. Crée `presentation.py` :

```python
nom = "Ton prénom"
ville = "Ta ville"
objectif = "devenir analyste en cybersécurité"
print(f"Je m'appelle {nom}, j'habite à {ville} et mon objectif est de {objectif}.")
```

2. Remplace les valeurs par les tiennes et exécute : `python3 presentation.py`.

### Exercice 2 — Calculatrice simple

Écris un programme qui demande deux nombres et affiche leur somme, leur différence, leur produit et leur quotient.

Solution possible :

```python
a = float(input("Premier nombre : "))
b = float(input("Deuxième nombre : "))
print(f"Somme : {a + b}")
print(f"Différence : {a - b}")
print(f"Produit : {a * b}")
print(f"Quotient : {a / b}")
```

Teste avec `b = 0`. Que se passe-t-il ? (`ZeroDivisionError` : on apprendra à gérer ce cas.)

### Exercice 3 — Conversion de durées

Demande un nombre de secondes et affiche-le en heures, minutes et secondes. Indice : `//` et `%`.

```python
total = int(input("Nombre de secondes : "))
heures = total // 3600
minutes = (total % 3600) // 60
secondes = total % 60
print(f"{total} s = {heures} h {minutes} min {secondes} s")
```

### Exercice 4 — Lire des erreurs

Voici trois programmes buggés. Trouve l'erreur de chaque, sans les exécuter d'abord, puis vérifie :

```python
# A
print("Bonjour)

# B
age = input("Âge : ")
print(age + 5)

# C
nombre = int("douze")
```

**Corrigé :** A : guillemet non fermé (`SyntaxError`) ; B : `age` est du texte, on ne peut pas ajouter 5 (`TypeError`), il faut `int(age)` ; C : « douze » n'est pas convertible (`ValueError`).

### Exercice 5 — Mini-outil : informations sur ta machine

```python
import platform
import getpass
import socket
import datetime

print("=== Informations locales ===")
print("Utilisateur :", getpass.getuser())
print("Nom de la machine :", socket.gethostname())
print("Système :", platform.system(), platform.release())
print("Version de Python :", platform.python_version())
print("Date et heure :", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
```

Exécute-le. Quelles informations pourrait-on utiliser pour **identifier** ta machine ? (Nom d'hôte, utilisateur, version du système.) Les collectes d'informations de ce type sont le point de départ de tout inventaire de sécurité.

### Exercice 6 — Environnement virtuel

```bash
mkdir projet_python && cd projet_python
python3 -m venv env
source env/bin/activate
pip install requests
pip list
python3 -c "import requests; print(requests.__version__)"
deactivate
```

Vérifie que, une fois désactivé, `pip list` n'affiche plus `requests` dans l'environnement global (si tu ne l'y avais pas installé).

### Exercice 7 — Défi : générateur de message d'alerte

Demande le nom d'un utilisateur, une adresse IP et un nombre d'échecs de connexion, puis affiche :

```
[ALERTE] 7 échecs de connexion pour l'utilisateur 'admin' depuis 203.0.113.45
```

Ajoute la date et l'heure avec `datetime`. C'est la première brique d'un outil de supervision.

## 🔍 Approfondissement

### Pour aller plus loin

- La documentation officielle : docs.python.org/fr/3 (tutoriel en français).
- Les exercices progressifs de **France-IOI**, **OpenClassrooms** (« Apprenez à programmer en Python ») et **Codingame**.
- Le module « Python Basics » de TryHackMe.

### Pièges courants

- ❌ **Erreur fréquente 1** : oublier que `input()` renvoie du texte.
- ✅ **Bonne pratique** : convertir explicitement avec `int()` ou `float()`, et vérifier l'entrée.
- ❌ **Erreur fréquente 2** : mélanger tabulations et espaces dans l'indentation.
- ✅ **Bonne pratique** : configurer l'éditeur pour insérer 4 espaces.
- ❌ **Erreur fréquente 3** : nommer un fichier `random.py` ou `requests.py`, ce qui masque la vraie bibliothèque.
- ✅ **Bonne pratique** : donner à ses scripts des noms qui n'entrent pas en conflit avec des modules.
- ❌ **Erreur fréquente 4** : installer des paquets au hasard avec `sudo pip install`.
- ✅ **Bonne pratique** : environnement virtuel par projet, vérification du nom exact du paquet.

## 🧪 Quiz de validation

**Question 1 : Quelle fonction affiche du texte à l'écran en Python ?**
- A) `echo()`
- B) `print()` ✅
- C) `display()`
- D) `write()`

*Explication : `print()` est la fonction standard d'affichage.*

**Question 2 : Que renvoie toujours la fonction `input()` ?**
- A) Un entier
- B) Un booléen
- C) Une chaîne de caractères ✅
- D) Un décimal

*Explication : même si l'utilisateur tape un nombre, `input()` renvoie du texte ; il faut le convertir avec `int()` ou `float()`.*

**Question 3 : Quel nom de variable est valide ?**
- A) `2nom`
- B) `nom-utilisateur`
- C) `nom_utilisateur` ✅
- D) `class`

*Explication : un nom ne commence pas par un chiffre, ne contient pas de tiret et ne peut pas être un mot réservé.*

**Question 4 : À quoi sert un environnement virtuel (venv) ?**
- A) À accélérer Python
- B) À isoler les dépendances d'un projet ✅
- C) À chiffrer le code
- D) À installer Python

*Explication : chaque projet garde ses propres versions de bibliothèques sans perturber les autres ni le système.*

**Question 5 : Quelle est la bonne façon de lire une erreur Python (traceback) ?**
- A) Ignorer le message
- B) Lire la dernière ligne (type d'erreur) puis le numéro de ligne indiqué ✅
- C) Relancer le programme
- D) Réinstaller Python

*Explication : la dernière ligne donne le type et le message de l'erreur, les lignes précédentes indiquent où elle s'est produite.*

## 📝 Résumé

- Python est un langage lisible, interprété et très répandu en cybersécurité grâce à son écosystème de bibliothèques.
- On l'exécute en mode interactif (`python3`) ou via des scripts `.py`.
- Les variables stockent des valeurs ; les types de base sont `int`, `float`, `str`, `bool` ; `input()` renvoie du texte à convertir.
- Les f-strings facilitent l'affichage de variables dans du texte.
- Les messages d'erreur (traceback) indiquent le type, le message et la ligne du problème.
- `pip` installe des bibliothèques, et les environnements virtuels isolent les projets.

## 🎓 Ce que tu as appris

✅ Installer Python et exécuter des scripts
✅ Utiliser variables, opérations, `print`, `input` et f-strings
✅ Lire et corriger des erreurs courantes
✅ Créer un environnement virtuel et installer un paquet

## ➡️ Leçon suivante

**02 : Types de données** : listes, tuples, dictionnaires, ensembles et méthodes sur les chaînes de caractères. Fichier : `02-types-donnees.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
