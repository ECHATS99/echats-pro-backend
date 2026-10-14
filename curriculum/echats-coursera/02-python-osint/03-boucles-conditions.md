---
title: "Boucles et Conditions"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 40
order: 3
category: "python"
tags: ["python", "if", "for", "while", "boucles", "conditions", "comprehensions", "logs"]
prerequisites: ["01-introduction-python", "02-types-donnees"]
learning_objectives:
  - "Écrire des conditions avec if, elif, else et opérateurs logiques"
  - "Répéter des actions avec for, while, break et continue"
  - "Utiliser range, enumerate et les compréhensions de listes"
  - "Analyser un fichier de journal ligne par ligne pour détecter des anomalies"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Boucles et Conditions

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Écrire des conditions avec `if`, `elif`, `else` et opérateurs logiques
- Répéter des actions avec `for`, `while`, `break` et `continue`
- Utiliser `range`, `enumerate` et les compréhensions de listes
- Analyser un fichier de journal ligne par ligne pour détecter des anomalies

## 📚 Prérequis

- Leçon 01 : *Introduction à Python*
- Leçon 02 : *Types de données* (listes, dictionnaires, chaînes)

## 🧭 Introduction

Un programme utile fait deux choses : **prendre des décisions** et **répéter des actions**. « Si cette adresse IP a plus de cinq échecs de connexion, signale-la. » « Pour chaque ligne du journal, extrais l'adresse. » Ces deux idées s'expriment avec des **conditions** (`if`) et des **boucles** (`for`, `while`).

Dans un journal de serveur de 100 000 lignes, aucun humain ne cherche à l'œil les tentatives suspectes. Un script de dix lignes le fait en une seconde. C'est le cœur de l'automatisation en cybersécurité : transformer une masse de données en quelques observations utiles.

Cette leçon te donne ces outils. Avec elle, tu seras capable d'écrire ton premier véritable outil d'analyse.

## 📖 Concepts clés

### 1. Les comparaisons et les booléens

| Opérateur | Sens |
|---|---|
| `==` | égal à |
| `!=` | différent de |
| `<`, `>` | inférieur, supérieur |
| `<=`, `>=` | inférieur ou égal, supérieur ou égal |
| `in` | appartient à |
| `not in` | n'appartient pas à |
| `is` | est le même objet (utilisé surtout avec `None`) |

⚠️ **Ne confonds pas `=` (affectation) et `==` (comparaison).**

```python
port = 22
print(port == 22)             # True
print(port in [22, 80, 443])  # True
print("admin" in "administrateur")  # True
```

**Opérateurs logiques** : `and` (et), `or` (ou), `not` (non).

```python
port = 443
protocole = "tcp"
print(port == 443 and protocole == "tcp")   # True
print(port == 80 or port == 8080)           # False
print(not (port < 1024))                    # False
```

### 2. La condition if / elif / else

```python
echecs = 7

if echecs >= 10:
    print("CRITIQUE : blocage immédiat")
elif echecs >= 5:
    print("ALERTE : surveillance renforcée")
else:
    print("Normal")
```

**Points essentiels :**
- la ligne se termine par `:` ;
- le bloc qui suit est **indenté de 4 espaces** ;
- `elif` est évalué seulement si les conditions précédentes sont fausses ;
- `else` est facultatif et couvre tous les autres cas ;
- seul **le premier bloc vrai** s'exécute.

Condition sur une valeur « vraie ou fausse » :

```python
utilisateur = input("Nom : ").strip()
if not utilisateur:
    print("Le nom est vide")
```

**Expression conditionnelle** (forme courte) :

```python
statut = "ouvert" if port == 80 else "à vérifier"
```

### 3. Les conditions imbriquées

```python
age = 20
a_un_badge = True

if age >= 18:
    if a_un_badge:
        print("Accès autorisé")
    else:
        print("Badge requis")
else:
    print("Accès refusé")
```

Préfère un code **à plat** quand c'est possible : `if age >= 18 and a_un_badge:`. Moins d'imbrication = moins de bugs et plus de clarté.

### 4. La boucle for

La boucle `for` parcourt les éléments d'une séquence (liste, chaîne, dictionnaire, fichier…).

```python
for port in [22, 80, 443]:
    print("Test du port", port)

for lettre in "SOC":
    print(lettre)
```

**`range()`** génère une suite de nombres :

```python
for i in range(5):            # 0, 1, 2, 3, 4
    print(i)
for i in range(1, 6):         # 1 à 5
    print(i)
for port in range(20, 30, 2): # 20, 22, 24, 26, 28 (pas de 2)
    print(port)
```

**`enumerate()`** donne l'indice **et** la valeur :

```python
machines = ["web-01", "db-01", "mail-01"]
for numero, nom in enumerate(machines, start=1):
    print(f"{numero}. {nom}")
```

**`zip()`** parcourt plusieurs listes en parallèle :

```python
noms = ["web-01", "db-01"]
ips = ["10.0.0.10", "10.0.0.20"]
for nom, ip in zip(noms, ips):
    print(nom, ip)
```

**Parcourir un dictionnaire :**

```python
echecs = {"10.0.0.5": 12, "10.0.0.9": 2}
for ip, nombre in echecs.items():
    if nombre > 5:
        print(f"{ip} : {nombre} échecs, à surveiller")
```

### 5. La boucle while

`while` répète **tant qu'une condition est vraie**.

```python
tentatives = 0
while tentatives < 3:
    print("Tentative", tentatives + 1)
    tentatives += 1
```

⚠️ **Boucle infinie** : si la condition ne devient jamais fausse, le programme tourne sans fin (arrêt avec `Ctrl+C`). Assure-toi que quelque chose modifie la condition.

Exemple d'utilisation : demander une saisie valide jusqu'à ce qu'elle le soit.

```python
while True:
    saisie = input("Port (1-65535) : ").strip()
    if saisie.isdigit() and 1 <= int(saisie) <= 65535:
        port = int(saisie)
        break
    print("Entrée invalide, recommence.")
print("Port retenu :", port)
```

### 6. break, continue et else de boucle

- `break` : **sort** de la boucle immédiatement ;
- `continue` : **saute** au tour suivant ;
- `else` (sur une boucle) : s'exécute si la boucle s'est terminée **sans `break`**.

```python
for port in [21, 22, 80]:
    if port == 21:
        continue          # on ignore FTP
    if port == 80:
        print("Web trouvé")
        break
    print("Port inspecté :", port)

mot_de_passe_trouve = False
for essai in ["1234", "azerty", "motdepasse"]:
    if essai == "motdepasse":
        print("Faible : mot de passe courant détecté")
        break
else:
    print("Aucune correspondance")
```

### 7. Les compréhensions

Une **compréhension de liste** construit une liste en une ligne :

```python
ports = [22, 80, 443, 3306, 8080]
privilegies = [p for p in ports if p < 1024]        # [22, 80, 443]
etiquettes = [f"port-{p}" for p in ports]
```

Il en existe pour les ensembles (`{... for ...}`) et les dictionnaires (`{k: v for ...}`) :

```python
longueurs = {mot: len(mot) for mot in ["admin", "root", "test"]}
```

Reste lisible : si la compréhension devient longue ou complexe, écris une boucle normale.

### 8. Lire un fichier ligne par ligne

Pour analyser un journal, on **ouvre** le fichier et on boucle dessus :

```python
with open("auth.log", "r", encoding="utf-8") as fichier:
    for ligne in fichier:
        ligne = ligne.strip()
        if "Failed password" in ligne:
            print(ligne)
```

- `with open(...) as fichier` ferme **automatiquement** le fichier à la fin du bloc, même en cas d'erreur ;
- on parcourt le fichier **ligne par ligne**, ce qui consomme peu de mémoire même pour un fichier énorme ;
- `"r"` = lecture ; `"w"` = écriture (écrase) ; `"a"` = ajout à la fin.

On approfondira les fichiers dans la leçon 05.

### 9. Exemple complet : détecter une force brute

```python
from collections import Counter

compteur = Counter()

with open("auth.log", "r", encoding="utf-8", errors="ignore") as f:
    for ligne in f:
        if "Failed password" not in ligne:
            continue
        mots = ligne.split()
        if "from" in mots:
            ip = mots[mots.index("from") + 1]
            compteur[ip] += 1

SEUIL = 5
for ip, nombre in compteur.most_common():
    if nombre >= SEUIL:
        print(f"[ALERTE] {ip} : {nombre} échecs")
```

Ce petit programme :
1. lit un journal d'authentification ;
2. ignore les lignes sans « Failed password » (`continue`) ;
3. extrait l'IP après le mot « from » ;
4. compte les échecs par IP ;
5. affiche celles qui dépassent un seuil.

Il illustre le schéma d'analyse le plus courant : **filtrer → extraire → compter → alerter**.

### 10. Bonnes pratiques

- **Nomme tes seuils** (`SEUIL = 5`) au lieu de laisser des « nombres magiques » dans le code.
- **Évite les boucles imbriquées profondes** : elles ralentissent et compliquent la lecture.
- **Ne modifie pas une liste pendant que tu la parcours** : crée-en une nouvelle.
- **Prévois les cas limites** : fichier vide, ligne mal formée, valeur absente.
- **Ne fais jamais confiance aux données du fichier** : une ligne de journal peut contenir n'importe quoi (y compris du contenu forgé par un attaquant). Valide avant d'utiliser.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : analyse uniquement **tes propres journaux** ou des **fichiers d'exercice fournis**. Les journaux d'un système tiers peuvent contenir des données personnelles et ne s'analysent qu'avec autorisation.

### Exercice 1 — Classer un niveau d'alerte

Demande un nombre d'échecs et affiche :
- `0 à 2` : « Normal »
- `3 à 9` : « À surveiller »
- `10 et plus` : « Critique »
- une valeur négative ou non numérique : « Entrée invalide ».

```python
saisie = input("Nombre d'échecs : ").strip()
if not saisie.lstrip("-").isdigit() or int(saisie) < 0:
    print("Entrée invalide")
else:
    n = int(saisie)
    if n <= 2:
        print("Normal")
    elif n <= 9:
        print("À surveiller")
    else:
        print("Critique")
```

### Exercice 2 — Table de multiplication et FizzBuzz sécurisé

1. Affiche la table de 7 de 1 à 10.
2. Pour les nombres de 1 à 30 : affiche « PAIR » ou « IMPAIR ».
3. Affiche seulement les nombres divisibles par 3 **ou** 5.

```python
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")
print([n for n in range(1, 31) if n % 3 == 0 or n % 5 == 0])
```

### Exercice 3 — Deviner un nombre (while)

Le programme choisit un nombre entre 1 et 20 avec `random.randint`. L'utilisateur propose des nombres ; le programme répond « plus grand » ou « plus petit » jusqu'à trouver, en comptant les essais.

```python
import random
secret = random.randint(1, 20)
essais = 0
while True:
    saisie = input("Ton choix : ").strip()
    if not saisie.isdigit():
        print("Entre un nombre.")
        continue
    essais += 1
    choix = int(saisie)
    if choix < secret:
        print("Plus grand")
    elif choix > secret:
        print("Plus petit")
    else:
        print(f"Trouvé en {essais} essais !")
        break
```

### Exercice 4 — Contrôleur de robustesse de mot de passe

Écris un programme qui lit un mot de passe et attribue un score :
- +1 s'il a au moins 12 caractères ;
- +1 s'il contient une minuscule, +1 une majuscule, +1 un chiffre, +1 un symbole ;
- affiche « Faible », « Moyen » ou « Fort » selon le score.

Aide : `any(c.islower() for c in mdp)`, `c.isupper()`, `c.isdigit()`, `not c.isalnum()`.

```python
mdp = input("Mot de passe à évaluer : ")
score = 0
if len(mdp) >= 12: score += 1
if any(c.islower() for c in mdp): score += 1
if any(c.isupper() for c in mdp): score += 1
if any(c.isdigit() for c in mdp): score += 1
if any(not c.isalnum() for c in mdp): score += 1
niveau = "Faible" if score <= 2 else "Moyen" if score <= 4 else "Fort"
print(f"Score {score}/5 : {niveau}")
```

⚠️ Ne saisis jamais un mot de passe **réel** que tu utilises ailleurs dans un programme que tu ne maîtrises pas. Teste avec des exemples.

### Exercice 5 — Analyser un journal fictif

1. Crée `auth.log` avec ces lignes :

```
Oct 03 10:15:22 srv sshd[842]: Failed password for admin from 203.0.113.45 port 51822 ssh2
Oct 03 10:15:25 srv sshd[842]: Failed password for root from 203.0.113.45 port 51823 ssh2
Oct 03 10:15:29 srv sshd[842]: Failed password for admin from 203.0.113.45 port 51824 ssh2
Oct 03 10:16:01 srv sshd[845]: Accepted publickey for alice from 192.168.1.20 port 40322 ssh2
Oct 03 10:16:40 srv sshd[850]: Failed password for test from 198.51.100.7 port 40100 ssh2
Oct 03 10:17:02 srv sshd[853]: Failed password for admin from 203.0.113.45 port 51825 ssh2
```

2. Exécute le programme de la section 9 avec `SEUIL = 3`.
3. Résultat attendu : `[ALERTE] 203.0.113.45 : 4 échecs`.
4. Modifie le script pour afficher aussi les **comptes ciblés** par cette IP.

### Exercice 6 — Détecter un schéma suspect

Étends le programme pour construire un dictionnaire `{ip: ensemble_de_comptes}`. Une IP qui essaie **plus de 3 comptes différents** ressemble à un balayage de comptes (*password spraying*).

```python
from collections import defaultdict
comptes_par_ip = defaultdict(set)
with open("auth.log", encoding="utf-8") as f:
    for ligne in f:
        if "Failed password" in ligne:
            m = ligne.split()
            utilisateur = m[m.index("for") + 1]
            ip = m[m.index("from") + 1]
            comptes_par_ip[ip].add(utilisateur)
for ip, comptes in comptes_par_ip.items():
    if len(comptes) >= 2:
        print(f"{ip} a tenté {len(comptes)} comptes : {sorted(comptes)}")
```

### Exercice 7 — Défi : mini-scanner de ports local

Utilise le module `socket` pour tester quels ports de **ta propre machine** (`127.0.0.1`) sont ouverts parmi une liste :

```python
import socket

PORTS = [21, 22, 25, 53, 80, 443, 3306, 8000, 8080]
for port in PORTS:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        if s.connect_ex(("127.0.0.1", port)) == 0:
            print(f"Port {port} ouvert")
        else:
            print(f"Port {port} fermé")
```

Compare avec `ss -tln`. **Ne remplace pas `127.0.0.1` par l'adresse d'une machine qui ne t'appartient pas** : un scan sans autorisation est interdit (voir leçon 16, Nmap).

## 🔍 Approfondissement

### Pour aller plus loin

- Documentation officielle : « Structures de contrôle » (docs.python.org/fr/3/tutorial/controlflow.html).
- Le module `itertools` pour des boucles avancées, et `pathlib` pour les fichiers.
- Exercices sur *Exercism* (Python) et *Advent of Code* pour t'entraîner à la logique.

### Pièges courants

- ❌ **Erreur fréquente 1** : écrire `if x = 5:` au lieu de `if x == 5:`.
- ✅ **Bonne pratique** : `==` compare, `=` affecte.
- ❌ **Erreur fréquente 2** : oublier les `:` ou mal indenter le bloc (`IndentationError`).
- ✅ **Bonne pratique** : 4 espaces, un éditeur configuré pour Python.
- ❌ **Erreur fréquente 3** : boucle `while` infinie car la variable de contrôle n'est jamais modifiée.
- ✅ **Bonne pratique** : vérifier qu'une instruction fait progresser la condition ; prévoir un `break`.
- ❌ **Erreur fréquente 4** : supposer que chaque ligne du journal a le format attendu (`ValueError` sur `index`).
- ✅ **Bonne pratique** : tester `"from" in mots` avant `mots.index("from")`, ou utiliser `try/except` (leçon 04).
- ❌ **Erreur fréquente 5** : modifier une liste pendant qu'on la parcourt.
- ✅ **Bonne pratique** : construire une nouvelle liste avec une compréhension.

## 🧪 Quiz de validation

**Question 1 : Quelle est la différence entre `=` et `==` ?**
- A) Aucune
- B) `=` affecte une valeur, `==` compare deux valeurs ✅
- C) `=` compare, `==` affecte
- D) `==` supprime une variable

*Explication : `x = 5` crée ou modifie une variable ; `x == 5` teste l'égalité et renvoie `True` ou `False`.*

**Question 2 : Que génère `range(1, 6)` ?**
- A) 1, 2, 3, 4, 5, 6
- B) 0, 1, 2, 3, 4, 5
- C) 1, 2, 3, 4, 5 ✅
- D) 2, 3, 4, 5, 6

*Explication : `range(début, fin)` inclut le début et exclut la fin.*

**Question 3 : Que fait l'instruction `continue` dans une boucle ?**
- A) Elle quitte la boucle
- B) Elle passe directement à l'itération suivante ✅
- C) Elle relance le programme
- D) Elle arrête Python

*Explication : `continue` saute le reste du tour courant ; `break` quitte la boucle entièrement.*

**Question 4 : Pourquoi utiliser `with open(...) as f` ?**
- A) Pour chiffrer le fichier
- B) Pour que le fichier soit fermé automatiquement, même en cas d'erreur ✅
- C) Pour lire plus vite
- D) C'est obligatoire pour les fichiers de plus de 1 Mo

*Explication : le gestionnaire de contexte garantit la fermeture du fichier et évite les fuites de ressources.*

**Question 5 : Que vaut `[n for n in range(1, 8) if n % 2 == 0]` ?**
- A) `[1, 3, 5, 7]`
- B) `[2, 4, 6]` ✅
- C) `[0, 2, 4, 6]`
- D) `[2, 4, 6, 8]`

*Explication : on garde les nombres de 1 à 7 divisibles par 2.*

## 📝 Résumé

- `if` / `elif` / `else` prennent des décisions ; les blocs sont délimités par l'indentation (4 espaces) après un `:`.
- `for` parcourt une séquence (`range`, `enumerate`, `zip`, dictionnaires, fichiers) ; `while` répète tant qu'une condition est vraie.
- `break`, `continue` et `else` de boucle contrôlent le déroulement des itérations.
- Les compréhensions construisent des listes, ensembles et dictionnaires de façon concise.
- Lire un fichier ligne par ligne avec `with open` permet d'analyser des journaux volumineux.
- Schéma d'analyse type : filtrer, extraire, compter, alerter ; et toujours valider les données.

## 🎓 Ce que tu as appris

✅ Écrire des conditions claires et des boucles correctes
✅ Utiliser `range`, `enumerate`, `zip` et les compréhensions
✅ Parcourir un journal et compter des événements par IP
✅ Repérer une force brute et un balayage de comptes

## ➡️ Leçon suivante

**04 : Fonctions et modules** : organiser le code en fonctions réutilisables, gérer les erreurs avec `try/except`, créer ses propres modules. Fichier : `04-fonctions-modules.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
