---
title: "Fonctions, Modules et Gestion des Erreurs"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 40
order: 4
category: "python"
tags: ["python", "fonctions", "modules", "try-except", "argparse", "ipaddress", "hashlib"]
prerequisites: ["01-introduction-python", "02-types-donnees", "03-boucles-conditions"]
learning_objectives:
  - "Définir et appeler des fonctions avec paramètres et valeurs de retour"
  - "Gérer les erreurs avec try / except / finally"
  - "Importer et créer des modules, utiliser la bibliothèque standard"
  - "Construire un petit outil en ligne de commande avec argparse"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Fonctions, Modules et Gestion des Erreurs

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Définir et appeler des fonctions avec paramètres et valeurs de retour
- Gérer les erreurs avec `try` / `except` / `finally`
- Importer et créer des modules, utiliser la bibliothèque standard
- Construire un petit outil en ligne de commande avec `argparse`

## 📚 Prérequis

- Leçons 01, 02 et 03 du module Python & OSINT

## 🧭 Introduction

Quand un script grandit, il devient vite illisible : des dizaines de lignes qui font tout, des morceaux de code copiés-collés à plusieurs endroits, des erreurs qui font planter le programme au premier cas imprévu. Trois outils permettent de garder le contrôle : les **fonctions**, les **modules** et la **gestion des erreurs**.

Une **fonction** est un bloc de code nommé, réutilisable : « vérifie qu'une adresse IP est valide », « calcule l'empreinte d'un fichier », « extrais le domaine d'une URL ». Un **module** est un fichier Python qui regroupe des fonctions, qu'on importe là où on en a besoin. La **gestion des erreurs** permet à un programme de réagir proprement à l'inattendu : fichier absent, réseau coupé, saisie incorrecte.

C'est aussi une question de **sécurité** : un outil qui plante sur une entrée mal formée, ou qui affiche une trace d'erreur révélant des chemins et des détails internes, peut devenir une faille. La plupart des vulnérabilités applicatives viennent d'entrées non validées et d'erreurs mal gérées. Savoir structurer son code, c'est aussi savoir le défendre.

## 📖 Concepts clés

### 1. Définir une fonction

```python
def saluer(nom):
    print(f"Bonjour {nom} !")

saluer("Alice")
saluer("Bob")
```

- `def` introduit la fonction ; son nom suit les règles des variables (snake_case) ;
- entre parenthèses : les **paramètres** ;
- le bloc indenté est le **corps** ;
- on **appelle** la fonction en écrivant son nom suivi de parenthèses.

### 2. Retourner une valeur

`return` renvoie un résultat à l'appelant :

```python
def est_port_valide(port):
    return isinstance(port, int) and 1 <= port <= 65535

print(est_port_valide(443))    # True
print(est_port_valide(70000))  # False
```

Une fonction sans `return` renvoie `None`. On peut retourner **plusieurs valeurs** (sous forme de tuple) :

```python
def analyser_adresse(adresse):
    ip, port = adresse.split(":")
    return ip, int(port)

ip, port = analyser_adresse("192.168.1.10:8080")
```

`print` **affiche** ; `return` **renvoie**. Une fonction qui calcule devrait renvoyer son résultat, pas l'afficher, pour pouvoir être réutilisée.

### 3. Paramètres : positionnels, nommés, par défaut

```python
def tester_port(hote, port=80, delai=1.0):
    return f"Test de {hote}:{port} (délai {delai}s)"

print(tester_port("127.0.0.1"))                    # utilise les valeurs par défaut
print(tester_port("127.0.0.1", 443))               # positionnel
print(tester_port("127.0.0.1", delai=0.5, port=22)) # nommés : ordre libre
```

**Nombre variable d'arguments :**

```python
def additionner(*nombres):
    return sum(nombres)

print(additionner(1, 2, 3, 4))      # 10

def afficher_options(**options):
    for cle, valeur in options.items():
        print(cle, "=", valeur)

afficher_options(verbose=True, port=22)
```

⚠️ **Piège classique** : ne mets jamais une liste ou un dictionnaire modifiable comme valeur par défaut (`def f(x, liste=[])`). Cette liste est partagée entre tous les appels. Utilise `None` :

```python
def ajouter(element, liste=None):
    if liste is None:
        liste = []
    liste.append(element)
    return liste
```

### 4. La portée des variables

- Une variable créée **dans** une fonction est **locale** : elle n'existe que dans cette fonction.
- Une variable créée **en dehors** est **globale**, lisible partout.

```python
SEUIL = 5               # globale (constante par convention : majuscules)

def evaluer(echecs):
    niveau = "alerte" if echecs >= SEUIL else "normal"   # niveau est locale
    return niveau

print(evaluer(7))
# print(niveau)  → NameError
```

Bonne pratique : **évite de modifier des variables globales** depuis une fonction. Passe les données en paramètres et récupère-les en retour.

### 5. Documenter une fonction

Une **docstring** (chaîne en première ligne du corps) explique le rôle de la fonction. Les **annotations de types** précisent ce qui est attendu (facultatif mais très utile) :

```python
def extraire_ip(ligne: str) -> str | None:
    """Renvoie l'adresse IPv4 qui suit le mot 'from' dans une ligne de journal,
    ou None si elle est absente."""
    mots = ligne.split()
    if "from" in mots:
        return mots[mots.index("from") + 1]
    return None
```

`help(extraire_ip)` affiche la docstring. Un code documenté se relit et se vérifie bien plus facilement, atout majeur pour un audit.

### 6. Gérer les erreurs : try / except

Quand une erreur survient pendant l'exécution (une **exception**), le programme s'arrête, sauf si on la **capture**.

```python
try:
    nombre = int(input("Un nombre : "))
    resultat = 100 / nombre
    print(f"Résultat : {resultat}")
except ValueError:
    print("Ce n'est pas un nombre.")
except ZeroDivisionError:
    print("Division par zéro impossible.")
else:
    print("Tout s'est bien passé.")
finally:
    print("Fin du traitement.")
```

- `try` : le code susceptible d'échouer ;
- `except TypeErreur` : ce qu'on fait si **cette** erreur survient ;
- `else` : s'exécute si **aucune** erreur ;
- `finally` : s'exécute **toujours** (nettoyage : fermer un fichier, une connexion).

Exceptions fréquentes : `ValueError`, `TypeError`, `KeyError`, `IndexError`, `FileNotFoundError`, `PermissionError`, `ConnectionError`, `TimeoutError`.

**Lever une exception soi-même** quand une entrée est inacceptable :

```python
def definir_port(port):
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError(f"Port invalide : {port}")
    return port
```

**Bonnes pratiques :**
- **capture des exceptions précises** (`except FileNotFoundError`), jamais un `except:` nu ou `except Exception:` qui masque tout ;
- n'avale pas silencieusement une erreur (`except: pass`) : tu ne sauras plus ce qui s'est passé ;
- **journalise** l'erreur côté serveur, mais n'**affiche pas** à l'utilisateur final des détails internes (chemins, requêtes, traces) ;
- en sécurité, un échec doit être **sûr par défaut** (*fail secure*) : en cas de doute ou d'erreur, on refuse l'accès plutôt que de l'autoriser.

### 7. Les modules

Un **module** est un fichier `.py`. On l'importe avec `import`.

```python
import math
print(math.sqrt(16))                # 4.0

from math import sqrt, pi           # importe des noms précis
print(sqrt(25), pi)

import datetime as dt               # alias
print(dt.date.today())
```

**Modules utiles de la bibliothèque standard pour la cybersécurité :**

| Module | Usage |
|---|---|
| `os`, `pathlib` | Fichiers, dossiers, variables d'environnement |
| `sys` | Arguments, sortie du programme |
| `re` | Expressions régulières (recherche de motifs dans le texte) |
| `json`, `csv` | Lire et écrire des données structurées |
| `hashlib` | Empreintes (SHA-256…) |
| `ipaddress` | Manipuler et valider adresses et réseaux IP |
| `socket` | Communications réseau de bas niveau |
| `urllib` | Requêtes HTTP de base |
| `datetime` | Dates et heures |
| `subprocess` | Lancer des commandes système |
| `secrets` | Génération sécurisée de jetons et mots de passe |
| `logging` | Journalisation structurée |
| `argparse` | Arguments en ligne de commande |

**Exemples :**

```python
import ipaddress

ip = ipaddress.ip_address("192.168.1.25")
print(ip.is_private)                          # True
reseau = ipaddress.ip_network("192.168.1.0/24")
print(ip in reseau)                           # True
print(reseau.num_addresses)                   # 256
# ipaddress.ip_address("999.1.1.1") → ValueError
```

```python
import hashlib

def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(8192), b""):
            h.update(bloc)
    return h.hexdigest()
```

```python
import secrets, string
alphabet = string.ascii_letters + string.digits + "!@#$%&*"
mot_de_passe = "".join(secrets.choice(alphabet) for _ in range(16))
print(mot_de_passe)
```

> 🔐 Pour tout ce qui touche à la sécurité (mots de passe, jetons), utilise `secrets` et **non** `random`. Le module `random` est prévisible et ne convient pas à la cryptographie.

### 8. Créer son propre module

Un fichier `outils_reseau.py` :

```python
# outils_reseau.py
import ipaddress

def ip_valide(texte):
    """Renvoie True si 'texte' est une adresse IP valide."""
    try:
        ipaddress.ip_address(texte)
        return True
    except ValueError:
        return False

def est_privee(texte):
    return ipaddress.ip_address(texte).is_private
```

Un autre fichier dans le même dossier :

```python
# principal.py
from outils_reseau import ip_valide, est_privee

for adresse in ["192.168.1.1", "8.8.8.8", "999.0.0.1"]:
    if ip_valide(adresse):
        print(adresse, "privée" if est_privee(adresse) else "publique")
    else:
        print(adresse, "invalide")
```

### 9. Le bloc `if __name__ == "__main__"`

Pour qu'un fichier serve à la fois de **module importable** et de **script exécutable** :

```python
def principal():
    print("Programme lancé")

if __name__ == "__main__":
    principal()
```

Le code sous cette condition ne s'exécute que si le fichier est lancé directement, pas lorsqu'il est importé. C'est une convention très répandue.

### 10. Arguments en ligne de commande avec argparse

Un outil sérieux se pilote en ligne de commande. `argparse` gère les options et l'aide automatiquement :

```python
import argparse

def main():
    parseur = argparse.ArgumentParser(description="Compte les échecs de connexion par IP.")
    parseur.add_argument("journal", help="chemin du fichier de journal")
    parseur.add_argument("-s", "--seuil", type=int, default=5,
                         help="nombre d'échecs à partir duquel alerter (défaut : 5)")
    args = parseur.parse_args()
    print(f"Analyse de {args.journal} avec seuil {args.seuil}")

if __name__ == "__main__":
    main()
```

Utilisation :

```bash
python3 outil.py auth.log
python3 outil.py auth.log --seuil 3
python3 outil.py --help
```

### 11. Exemple complet : un petit outil structuré

```python
#!/usr/bin/env python3
"""Détecte les adresses IP avec trop d'échecs de connexion SSH."""
import argparse
import ipaddress
import sys
from collections import Counter

def extraire_ip(ligne):
    """Renvoie l'IP valide après 'from', ou None."""
    mots = ligne.split()
    if "Failed" not in mots or "from" not in mots:
        return None
    candidat = mots[mots.index("from") + 1]
    try:
        return str(ipaddress.ip_address(candidat))
    except ValueError:
        return None

def compter_echecs(chemin):
    compteur = Counter()
    with open(chemin, "r", encoding="utf-8", errors="ignore") as f:
        for ligne in f:
            ip = extraire_ip(ligne)
            if ip:
                compteur[ip] += 1
    return compteur

def main():
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("journal")
    parseur.add_argument("-s", "--seuil", type=int, default=5)
    args = parseur.parse_args()

    try:
        compteur = compter_echecs(args.journal)
    except FileNotFoundError:
        print(f"Erreur : fichier introuvable : {args.journal}", file=sys.stderr)
        return 1
    except PermissionError:
        print("Erreur : droits insuffisants pour lire le journal", file=sys.stderr)
        return 1

    for ip, n in compteur.most_common():
        if n >= args.seuil:
            print(f"[ALERTE] {ip} : {n} échecs")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

Remarque : cet outil sépare **extraction**, **comptage** et **interface**. Chaque fonction est testable séparément, et la validation de l'IP par `ipaddress` évite de traiter des données forgées.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : ces programmes ne traitent que des fichiers locaux d'exercice. Quand tu écriras des outils réseau, garde-les limités à ta machine, tes VM ou des cibles autorisées.

### Exercice 1 — Premières fonctions

Écris :
1. `carre(n)` qui renvoie n² ;
2. `est_pair(n)` qui renvoie `True` ou `False` ;
3. `moyenne(*nombres)` qui renvoie la moyenne de plusieurs nombres (ou `None` si aucun).

```python
def carre(n):
    return n * n

def est_pair(n):
    return n % 2 == 0

def moyenne(*nombres):
    return sum(nombres) / len(nombres) if nombres else None

print(carre(7), est_pair(10), moyenne(10, 12, 14), moyenne())
```

### Exercice 2 — Valider des adresses IP

Écris `classer_ip(texte)` qui renvoie `"invalide"`, `"privée"` ou `"publique"`. Teste avec `["192.168.1.1", "8.8.8.8", "10.0.0.5", "256.1.1.1", "abc", "127.0.0.1"]`.

```python
import ipaddress

def classer_ip(texte):
    try:
        ip = ipaddress.ip_address(texte)
    except ValueError:
        return "invalide"
    return "privée" if ip.is_private else "publique"

for t in ["192.168.1.1", "8.8.8.8", "10.0.0.5", "256.1.1.1", "abc", "127.0.0.1"]:
    print(f"{t:15s} → {classer_ip(t)}")
```

Question guidée : pourquoi `127.0.0.1` est-elle « privée » ici ? (Le module la classe parmi les adresses non routables publiquement ; on pourra aussi tester `ip.is_loopback`.)

### Exercice 3 — Gestion d'erreurs

Écris `lire_fichier(chemin)` qui renvoie le contenu du fichier, ou `None` en affichant un message adapté si le fichier est introuvable ou inaccessible. Teste-la avec un fichier existant, un fichier inexistant, et un fichier sans droit de lecture (`chmod 000`).

```python
def lire_fichier(chemin):
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Introuvable : {chemin}")
    except PermissionError:
        print(f"Accès refusé : {chemin}")
    return None
```

### Exercice 4 — Empreinte d'un fichier

Écris `sha256_fichier(chemin)` (voir section 7) et utilise-la pour comparer deux fichiers : s'ils ont la même empreinte, ils sont identiques. Modifie un caractère dans l'un d'eux et constate que l'empreinte change complètement.

Application : vérifier l'**intégrité** d'un fichier téléchargé en comparant son empreinte avec celle publiée par l'éditeur.

### Exercice 5 — Générateur de mots de passe

Écris `generer_mot_de_passe(longueur=16)` avec le module `secrets`. Refuse les longueurs inférieures à 12 en levant `ValueError`. Vérifie que le mot de passe généré contient au moins une minuscule, une majuscule, un chiffre et un symbole (régénère sinon).

```python
import secrets, string

def generer_mot_de_passe(longueur=16):
    if longueur < 12:
        raise ValueError("Longueur minimale : 12")
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    while True:
        mdp = "".join(secrets.choice(alphabet) for _ in range(longueur))
        if (any(c.islower() for c in mdp) and any(c.isupper() for c in mdp)
                and any(c.isdigit() for c in mdp) and any(c in "!@#$%&*" for c in mdp)):
            return mdp

print(generer_mot_de_passe())
```

### Exercice 6 — Créer ton module et ton outil

1. Crée un dossier `outils/`, avec `reseau.py` (fonctions `ip_valide`, `est_privee`) et `analyse.py` (programme de la section 11 adapté).
2. Importe `reseau` dans `analyse.py` pour valider les IP.
3. Exécute :

```bash
python3 analyse.py auth.log --seuil 3
python3 analyse.py inexistant.log
echo $?       # doit afficher 1
```

(Utilise le fichier `auth.log` de la leçon 03.)

### Exercice 7 — Défi : rapport d'analyse

Étends l'outil pour qu'il écrive un rapport dans un fichier si l'option `--sortie rapport.txt` est donnée. Le rapport contient : date, nombre total d'échecs, nombre d'IP distinctes, liste des IP au-dessus du seuil. Utilise `datetime`, `argparse` et des fonctions séparées.

## 🔍 Approfondissement

### Pour aller plus loin

- Documentation officielle : tutoriel « Modules », « Erreurs et exceptions », module `argparse`, `ipaddress`, `logging`.
- PEP 8 (guide de style Python) et l'outil **flake8** / **ruff** pour vérifier son code.
- Le module `unittest` ou **pytest** pour tester ses fonctions.

### Pièges courants

- ❌ **Erreur fréquente 1** : une fonction qui **affiche** son résultat au lieu de le **retourner**.
- ✅ **Bonne pratique** : `return` pour calculer, `print` seulement à l'interface.
- ❌ **Erreur fréquente 2** : `except:` ou `except Exception: pass`, qui cache les bugs et les attaques.
- ✅ **Bonne pratique** : capturer des exceptions précises et journaliser.
- ❌ **Erreur fréquente 3** : listes ou dictionnaires comme valeurs par défaut de paramètres.
- ✅ **Bonne pratique** : `None` puis création dans la fonction.
- ❌ **Erreur fréquente 4** : utiliser `random` pour générer des secrets.
- ✅ **Bonne pratique** : `secrets` pour tout ce qui touche à la sécurité.
- ❌ **Erreur fréquente 5** : nommer son fichier comme un module de la bibliothèque (`socket.py`, `random.py`).
- ✅ **Bonne pratique** : choisir des noms distincts pour éviter de masquer le vrai module.

## 🧪 Quiz de validation

**Question 1 : Quel mot-clé permet à une fonction de renvoyer un résultat ?**
- A) `print`
- B) `return` ✅
- C) `yield` uniquement
- D) `output`

*Explication : `return` renvoie une valeur à l'appelant ; `print` ne fait qu'afficher.*

**Question 2 : Que fait le bloc `finally` dans un `try` ?**
- A) Il s'exécute seulement s'il y a une erreur
- B) Il s'exécute toujours, qu'il y ait une erreur ou non ✅
- C) Il remplace `except`
- D) Il arrête le programme

*Explication : `finally` sert au nettoyage (fermer un fichier, une connexion) quelle que soit l'issue.*

**Question 3 : Pourquoi éviter `except: pass` ?**
- A) Parce que c'est plus lent
- B) Parce que cela masque les erreurs et empêche de comprendre ce qui se passe ✅
- C) Parce que Python l'interdit
- D) Parce que cela chiffre l'erreur

*Explication : une erreur ignorée en silence peut cacher un bug, une attaque ou une panne.*

**Question 4 : Quel module faut-il utiliser pour générer un mot de passe ou un jeton sécurisé ?**
- A) `random`
- B) `math`
- C) `secrets` ✅
- D) `time`

*Explication : `secrets` utilise un générateur adapté à la cryptographie, contrairement à `random`, prévisible.*

**Question 5 : À quoi sert `if __name__ == "__main__":` ?**
- A) À importer un module
- B) À exécuter du code seulement quand le fichier est lancé directement, pas lorsqu'il est importé ✅
- C) À définir une constante
- D) À arrêter une boucle

*Explication : cela permet à un fichier d'être à la fois un script et un module réutilisable.*

## 📝 Résumé

- Une fonction (`def`) regroupe du code réutilisable ; elle reçoit des paramètres (positionnels, nommés, par défaut) et renvoie un résultat avec `return`.
- Les variables locales n'existent que dans la fonction ; on évite de modifier des variables globales.
- `try` / `except` / `else` / `finally` gèrent les exceptions : on capture des erreurs précises, on journalise, on échoue de façon sûre.
- Les modules organisent le code ; la bibliothèque standard (`ipaddress`, `hashlib`, `secrets`, `re`, `json`, `argparse`…) couvre beaucoup de besoins de sécurité.
- `argparse` et `if __name__ == "__main__"` permettent de construire de vrais outils en ligne de commande.
- Validation des entrées et gestion propre des erreurs sont des pratiques de sécurité à part entière.

## 🎓 Ce que tu as appris

✅ Structurer son code en fonctions et modules
✅ Gérer les erreurs sans exposer d'informations sensibles
✅ Utiliser `ipaddress`, `hashlib` et `secrets` pour des tâches de sécurité
✅ Construire un outil en ligne de commande avec arguments

## ➡️ Leçon suivante

**05 : Fichiers et entrées/sorties** : lire et écrire des fichiers texte, CSV et JSON, gérer les chemins avec `pathlib` et traiter de gros journaux. Fichier : `05-fichiers-io.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
