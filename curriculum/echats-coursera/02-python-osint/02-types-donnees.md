---
title: "Types de Données Python"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 40
order: 2
category: "python"
tags: ["python", "listes", "dictionnaires", "tuples", "ensembles", "chaines", "types"]
prerequisites: ["01-introduction-python"]
learning_objectives:
  - "Manipuler les chaînes de caractères avec leurs méthodes"
  - "Utiliser listes, tuples, ensembles et dictionnaires"
  - "Choisir la structure de données adaptée à un besoin"
  - "Convertir et vérifier des types, y compris sur des données de sécurité"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Types de Données Python

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Manipuler les chaînes de caractères avec leurs méthodes
- Utiliser listes, tuples, ensembles et dictionnaires
- Choisir la structure de données adaptée à un besoin
- Convertir et vérifier des types, y compris sur des données de sécurité

## 📚 Prérequis

- Leçon 01 : *Introduction à Python* (variables, `print`, `input`, f-strings)

## 🧭 Introduction

Un programme manipule des **données** : des adresses IP, des noms d'utilisateurs, des ports, des lignes de journal, des résultats d'API. Pour bien les traiter, il faut les ranger dans les bonnes « boîtes ». Python propose plusieurs **types de données** et **structures** : texte, nombres, listes, dictionnaires, ensembles…

Choisir la bonne structure, c'est la moitié du travail. Pour stocker les ports ouverts d'une machine, une **liste** ou un **ensemble** ; pour associer à chaque adresse IP un nombre d'échecs de connexion, un **dictionnaire** ; pour représenter un couple (adresse, port) qui ne doit pas changer, un **tuple**.

Cette leçon est la plus « dense » du module, mais aussi l'une des plus utiles : la quasi-totalité des scripts de sécurité (analyse de journaux, scrapers OSINT, outils réseau) reposent sur ces structures. Prends le temps de **taper chaque exemple**.

## 📖 Concepts clés

### 1. Rappel des types simples

| Type | Exemple | Usage |
|---|---|---|
| `int` | `22`, `-5` | Entiers (ports, compteurs) |
| `float` | `3.14` | Nombres décimaux |
| `str` | `"admin"` | Texte |
| `bool` | `True`, `False` | Vrai / faux |
| `NoneType` | `None` | « Aucune valeur » |

Les **booléens** apparaissent comme résultats de comparaisons :

```python
print(22 == 22)      # True
print(80 > 443)      # False
print("a" in "banane")   # True
```

Valeurs considérées comme **fausses** (*falsy*) : `False`, `None`, `0`, `0.0`, `""` (texte vide), `[]`, `{}`, `()`, `set()`. Tout le reste est considéré comme vrai.

### 2. Les chaînes de caractères (str)

Une chaîne est une **suite de caractères**, entourée de guillemets simples ou doubles.

```python
message = "Connexion refusée"
multi = """Ceci est
un texte sur
plusieurs lignes"""
```

**Indexation et découpage (*slicing*)** : chaque caractère a une position, **la première est 0**.

```python
mot = "cyber"
print(mot[0])        # c
print(mot[-1])       # r  (le dernier)
print(mot[1:4])      # yb  (de l'indice 1 inclus à 4 exclu)
print(mot[:3])       # cyb
print(mot[2:])       # ber
print(mot[::-1])     # rebyc  (inversé)
print(len(mot))      # 5
```

**Les chaînes sont immuables** : on ne peut pas modifier un caractère en place (`mot[0] = "k"` provoque une erreur). On crée une nouvelle chaîne.

**Méthodes essentielles :**

```python
texte = "  Echec de connexion pour ADMIN  "
print(texte.strip())               # supprime les espaces autour
print(texte.lower())               # minuscules
print(texte.upper())               # majuscules
print(texte.replace("ADMIN", "root"))
print(texte.split())               # ['Echec', 'de', 'connexion', 'pour', 'ADMIN']
print("192.168.1.25".split("."))   # ['192', '168', '1', '25']
print("-".join(["a", "b", "c"]))   # a-b-c
print(texte.startswith("  Echec")) # True
print("connexion" in texte)        # True
print(texte.count("o"))            # nombre d'occurrences
print(texte.find("ADMIN"))         # position, ou -1 si absent
```

**Formatage** avec les f-strings :

```python
ip = "203.0.113.45"
echecs = 7
print(f"{ip} : {echecs} échecs")
print(f"{echecs:03d}")           # 007 (3 chiffres avec zéros)
print(f"{3.14159:.2f}")          # 3.14
```

**Caractères spéciaux** : `\n` (retour à la ligne), `\t` (tabulation), `\\` (antislash), `\"` (guillemet).

### 3. Les listes (list)

Une **liste** est une collection **ordonnée et modifiable** d'éléments, entre crochets.

```python
ports = [22, 80, 443]
mixte = ["admin", 25, True]
vide = []
```

```python
print(ports[0])         # 22
print(ports[-1])        # 443
print(ports[0:2])       # [22, 80]
print(len(ports))       # 3
print(80 in ports)      # True
```

**Modifier une liste :**

```python
ports.append(8080)        # ajoute à la fin
ports.insert(0, 21)       # insère à l'indice 0
ports.remove(80)          # retire la valeur 80
dernier = ports.pop()     # retire et renvoie le dernier
ports[0] = 2222           # remplace un élément
ports.sort()              # trie en place
ports.reverse()           # inverse
```

Autres opérations : `sorted(ports)` (renvoie une liste triée sans modifier l'originale), `min()`, `max()`, `sum()`, `ports + [3306]` (concaténation), `ports.count(22)`, `ports.index(22)`.

**Attention** : une copie simple avec `=` ne duplique pas la liste.

```python
a = [1, 2, 3]
b = a            # b et a désignent LA MÊME liste
b.append(4)
print(a)         # [1, 2, 3, 4] : a a aussi changé !
c = a.copy()     # copie indépendante
```

### 4. Les tuples (tuple)

Un **tuple** est comme une liste **non modifiable**, entre parenthèses.

```python
connexion = ("192.168.1.10", 443)
ip, port = connexion          # « déballage »
print(ip, port)
# connexion[0] = "x"  → erreur : un tuple est immuable
```

On l'utilise pour des données qui forment un tout et ne doivent pas changer : coordonnées, couple (adresse, port), couple (nom, version).

### 5. Les ensembles (set)

Un **ensemble** est une collection **sans doublons et sans ordre**, entre accolades.

```python
ports_ouverts = {22, 80, 443, 80, 22}
print(ports_ouverts)        # {80, 22, 443} : doublons supprimés
ports_ouverts.add(8080)
ports_ouverts.discard(22)
print(443 in ports_ouverts) # True (recherche très rapide)
```

Les ensembles sont parfaits pour les **comparaisons** :

```python
attendus = {22, 443}
observes = {22, 80, 443, 3306}

print(observes - attendus)      # {80, 3306} : ports en trop
print(attendus - observes)      # set() : rien ne manque
print(attendus & observes)      # intersection
print(attendus | observes)      # union
```

Cas typique : comparer l'**inventaire attendu** et **les résultats d'un scan** pour détecter les écarts. Pour dédoublonner une liste : `list(set(ma_liste))`.

### 6. Les dictionnaires (dict)

Un **dictionnaire** associe des **clés** à des **valeurs**, entre accolades, comme un annuaire.

```python
utilisateur = {
    "nom": "alice",
    "uid": 1001,
    "admin": False,
    "groupes": ["dev", "ssh"]
}

print(utilisateur["nom"])               # alice
print(utilisateur.get("email"))         # None (pas d'erreur si absent)
print(utilisateur.get("email", "n/a"))  # valeur par défaut
utilisateur["email"] = "alice@exemple.cg"   # ajoute ou modifie
del utilisateur["admin"]                # supprime
print("uid" in utilisateur)             # True : test sur les clés
```

Parcourir un dictionnaire :

```python
print(utilisateur.keys())      # les clés
print(utilisateur.values())    # les valeurs
for cle, valeur in utilisateur.items():
    print(cle, "→", valeur)
```

**Cas d'usage classique : compter des occurrences.**

```python
echecs = {}
for ip in ["10.0.0.5", "10.0.0.5", "192.168.1.9", "10.0.0.5"]:
    echecs[ip] = echecs.get(ip, 0) + 1
print(echecs)    # {'10.0.0.5': 3, '192.168.1.9': 1}
```

La bibliothèque standard fournit `collections.Counter`, qui fait ce travail en une ligne :

```python
from collections import Counter
print(Counter(["10.0.0.5", "10.0.0.5", "192.168.1.9", "10.0.0.5"]).most_common(1))
```

**Dictionnaires imbriqués** et JSON : les réponses d'API web (leçon 08) arrivent presque toujours sous la forme de dictionnaires et de listes imbriqués, que Python manipule naturellement.

```python
serveur = {
    "nom": "web-01",
    "ip": "203.0.113.10",
    "services": [
        {"port": 22, "nom": "ssh"},
        {"port": 443, "nom": "https"}
    ]
}
print(serveur["services"][1]["nom"])    # https
```

### 7. Choisir la bonne structure

| Besoin | Structure |
|---|---|
| Suite ordonnée, modifiable (lignes d'un fichier) | `list` |
| Données fixes qui forment un tout | `tuple` |
| Éléments uniques, tests d'appartenance rapides, différences | `set` |
| Association clé → valeur | `dict` |
| Texte | `str` |

### 8. Conversions de types

```python
int("22")            # 22
str(443)             # "443"
float("3.5")         # 3.5
list("abc")          # ['a', 'b', 'c']
tuple([1, 2])        # (1, 2)
set([1, 1, 2])       # {1, 2}
list({1, 2})         # [1, 2]
dict([("a", 1), ("b", 2)])   # {'a': 1, 'b': 2}
```

Vérifier un type :

```python
isinstance(22, int)              # True
isinstance("22", int)            # False
"22".isdigit()                   # True : le texte ne contient que des chiffres
```

### 9. Compréhensions de listes (aperçu)

Une façon compacte de construire une liste :

```python
ports = [22, 80, 443, 3306, 8080]
ports_web = [p for p in ports if p in (80, 443, 8080)]
print(ports_web)             # [80, 443, 8080]

carres = [n ** 2 for n in range(1, 6)]
print(carres)                # [1, 4, 9, 16, 25]
```

Tu les approfondiras dans la leçon 03.

### 10. Sécurité et types de données

- **Valider les entrées** : une valeur de type texte reçue d'un utilisateur ou d'une API n'est **pas digne de confiance**. Vérifie son type, sa longueur et son format avant de l'utiliser (par exemple : un numéro de port doit être un entier entre 1 et 65535).
- **Ne pas confondre `"22"` et `22`** : `"22" == 22` est `False`. Des comparaisons de types incohérentes sont une source classique de bugs, parfois de failles.
- **Secrets** : ne stocke pas de mots de passe dans des listes ou des dictionnaires que tu affiches ou journalises par erreur.
- **Données personnelles** : les noms, e-mails, adresses IP sont des données personnelles dans de nombreux cadres légaux ; manipule-les avec précaution (OSINT, journaux).

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : tous les exemples travaillent sur des données fictives ou locales. Pour des données réelles de tiers, respecte la loi sur la protection des données personnelles.

### Exercice 1 — Manipuler une chaîne

Soit `ligne = "Oct 03 10:15:22 srv sshd[842]: Failed password for admin from 203.0.113.45 port 51822 ssh2"`.

1. Extrais l'adresse IP (indice : `split()` puis `index("from") + 1`).
2. Extrais le nom d'utilisateur (après « for »).
3. Affiche-les avec une f-string.

Solution :

```python
ligne = "Oct 03 10:15:22 srv sshd[842]: Failed password for admin from 203.0.113.45 port 51822 ssh2"
mots = ligne.split()
utilisateur = mots[mots.index("for") + 1]
ip = mots[mots.index("from") + 1]
port = int(mots[mots.index("port") + 1])
print(f"Utilisateur : {utilisateur} | IP : {ip} | port source : {port}")
```

### Exercice 2 — Listes

1. Crée une liste `ports = [80, 22, 443, 22, 3306, 80, 8080]`.
2. Supprime les doublons et trie le résultat.
3. Affiche le nombre de ports, le plus petit et le plus grand.

```python
ports = [80, 22, 443, 22, 3306, 80, 8080]
uniques = sorted(set(ports))
print(uniques, len(uniques), min(uniques), max(uniques))
```

### Exercice 3 — Comparer deux ensembles

Un administrateur attend uniquement les ports `{22, 443}` ouverts. Un scan a trouvé `{22, 80, 443, 3389}`.

Affiche les ports **inattendus** et les ports **manquants**.

```python
attendus = {22, 443}
observes = {22, 80, 443, 3389}
print("Inattendus :", sorted(observes - attendus))
print("Manquants :", sorted(attendus - observes))
```

### Exercice 4 — Dictionnaire de comptage

À partir de la liste de tentatives :

```python
tentatives = ["admin", "root", "admin", "test", "admin", "root", "guest"]
```

Construis un dictionnaire `{nom: nombre}` puis affiche les noms triés par nombre décroissant.

```python
compte = {}
for nom in tentatives:
    compte[nom] = compte.get(nom, 0) + 1
for nom, n in sorted(compte.items(), key=lambda x: x[1], reverse=True):
    print(f"{nom:10s} {n}")
```

Question guidée : que suggère un grand nombre d'essais sur « admin » et « root » ? (Une attaque par force brute ou par dictionnaire visant des comptes courants.)

### Exercice 5 — Structure imbriquée

Représente deux serveurs, chacun avec un nom, une IP et une liste de services (port + nom). Affiche, pour chacun, la liste de ses ports.

```python
parc = [
    {"nom": "web-01", "ip": "192.168.10.10",
     "services": [{"port": 22, "nom": "ssh"}, {"port": 443, "nom": "https"}]},
    {"nom": "db-01", "ip": "192.168.10.20",
     "services": [{"port": 22, "nom": "ssh"}, {"port": 3306, "nom": "mysql"}]},
]
for machine in parc:
    ports = [s["port"] for s in machine["services"]]
    print(machine["nom"], machine["ip"], ports)
```

### Exercice 6 — Valider une entrée

Écris un programme qui demande un numéro de port, et affiche « valide » si c'est un entier entre 1 et 65535, sinon « invalide ».

```python
saisie = input("Port : ").strip()
if saisie.isdigit() and 1 <= int(saisie) <= 65535:
    print("valide")
else:
    print("invalide")
```

Teste avec `22`, `0`, `70000`, `abc`, `-5`, ` 443 `. Pourquoi tester d'abord `isdigit()` ? (Pour éviter qu'`int()` plante sur du texte non numérique.)

### Exercice 7 — Défi : analyseur de lignes de journal

Avec une liste de trois lignes de journal fictives (comme dans l'exercice 1), construis une liste de dictionnaires `{"utilisateur":..., "ip":...}`, puis un dictionnaire comptant les échecs par IP.

## 🔍 Approfondissement

### Pour aller plus loin

- La documentation officielle : tutoriel Python, section « Structures de données » (docs.python.org/fr/3/tutorial/datastructures.html).
- Le module `collections` : `Counter`, `defaultdict`, `namedtuple`.
- Le livre en ligne « Automatisez les tâches ennuyeuses avec Python » (Al Sweigart, en anglais) pour des exercices pratiques.

### Pièges courants

- ❌ **Erreur fréquente 1** : croire que `b = a` copie une liste.
- ✅ **Bonne pratique** : utiliser `a.copy()` ou `list(a)` pour obtenir une vraie copie.
- ❌ **Erreur fréquente 2** : confondre `[]` (liste vide), `{}` (dictionnaire vide) et `set()` (ensemble vide).
- ✅ **Bonne pratique** : un ensemble vide s'écrit `set()`, pas `{}`.
- ❌ **Erreur fréquente 3** : accéder à une clé absente avec `d["clé"]` et provoquer une `KeyError`.
- ✅ **Bonne pratique** : `d.get("clé", valeur_par_defaut)` ou tester `"clé" in d`.
- ❌ **Erreur fréquente 4** : supposer qu'un ensemble garde l'ordre.
- ✅ **Bonne pratique** : utiliser `sorted()` si l'ordre compte.
- ❌ **Erreur fréquente 5** : oublier que l'indexation commence à 0.
- ✅ **Bonne pratique** : le premier élément est `[0]`, le dernier `[-1]`.

## 🧪 Quiz de validation

**Question 1 : Que renvoie `"cyber"[1:4]` ?**
- A) `cyb`
- B) `yber`
- C) `ybe` ✅
- D) `cybe`

*Explication : le découpage va de l'indice 1 (inclus) à 4 (exclu) : y, b, e.*

**Question 2 : Quelle structure élimine automatiquement les doublons ?**
- A) `list`
- B) `tuple`
- C) `set` ✅
- D) `str`

*Explication : un ensemble ne contient que des éléments uniques.*

**Question 3 : Comment accéder en toute sécurité à une clé qui peut ne pas exister dans un dictionnaire `d` ?**
- A) `d["clé"]`
- B) `d.get("clé")` ✅
- C) `d.find("clé")`
- D) `d(clé)`

*Explication : `get` renvoie `None` (ou une valeur par défaut) au lieu de lever une `KeyError`.*

**Question 4 : Quelle structure est immuable parmi les suivantes ?**
- A) `list`
- B) `dict`
- C) `tuple` ✅
- D) `set`

*Explication : un tuple ne peut plus être modifié après sa création, contrairement à une liste, un dictionnaire ou un ensemble.*

**Question 5 : Que vaut `{22, 80, 443} - {22, 443}` ?**
- A) `{22, 443}`
- B) `{80}` ✅
- C) `{22, 80, 443}`
- D) `set()`

*Explication : la différence renvoie les éléments présents dans le premier ensemble mais pas dans le second.*

**Question 6 : Pourquoi tester `saisie.isdigit()` avant `int(saisie)` ?**
- A) Pour accélérer le programme
- B) Pour éviter une `ValueError` si la saisie n'est pas un nombre ✅
- C) Pour chiffrer la saisie
- D) Ce n'est pas utile

*Explication : `int("abc")` provoque une erreur ; valider l'entrée est une bonne pratique de sécurité et de robustesse.*

## 📝 Résumé

- Les chaînes sont immuables, indexées à partir de 0, et riches en méthodes (`split`, `strip`, `replace`, `lower`…).
- Les listes sont ordonnées et modifiables ; les tuples sont immuables ; les ensembles sont sans doublons et idéaux pour comparer ; les dictionnaires associent clés et valeurs.
- Le comptage d'occurrences avec un dictionnaire ou `Counter` est un schéma très courant en analyse de journaux.
- Choisir la bonne structure simplifie et sécurise le code.
- Toute donnée venant de l'extérieur doit être validée (type, format, plage) avant usage.

## 🎓 Ce que tu as appris

✅ Manipuler et découper des chaînes
✅ Utiliser listes, tuples, ensembles et dictionnaires
✅ Comparer des ensembles pour détecter des écarts
✅ Valider des entrées avant de les convertir

## ➡️ Leçon suivante

**03 : Boucles et conditions** : prendre des décisions (`if`), répéter des actions (`for`, `while`) et traiter des fichiers de journaux ligne par ligne. Fichier : `03-boucles-conditions.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
