---
title: "Fichiers et Entrées/Sorties"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 40
order: 5
category: "python"
tags: ["python", "fichiers", "pathlib", "csv", "json", "regex", "logs"]
prerequisites: ["03-boucles-conditions", "04-fonctions-modules"]
learning_objectives:
  - "Lire et écrire des fichiers texte et binaires en toute sécurité"
  - "Manipuler chemins et dossiers avec pathlib"
  - "Lire et produire des fichiers CSV et JSON"
  - "Extraire des informations d'un journal avec les expressions régulières"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Fichiers et Entrées/Sorties

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Lire et écrire des fichiers texte et binaires en toute sécurité
- Manipuler chemins et dossiers avec `pathlib`
- Lire et produire des fichiers CSV et JSON
- Extraire des informations d'un journal avec les expressions régulières

## 📚 Prérequis

- Leçon 03 : *Boucles et conditions*
- Leçon 04 : *Fonctions, modules et gestion des erreurs*

## 🧭 Introduction

Presque tout ce qu'un analyste en cybersécurité manipule est stocké dans des **fichiers** : journaux de serveurs, exports CSV d'un outil de scan, rapports JSON d'une API, listes d'adresses IP suspectes, captures, configurations. Savoir les lire, les transformer et en écrire de nouveaux est une compétence de base.

Python excelle dans ce domaine. En quelques lignes, tu peux parcourir un journal de plusieurs gigaoctets, extraire toutes les adresses IP, les dédoublonner, les comparer à une liste de réputation et produire un rapport. C'est ce que tu feras dans cette leçon.

Les fichiers sont aussi un terrain sensible pour la sécurité : chemins construits à partir d'entrées utilisateur (attaques par *path traversal*), fichiers temporaires prévisibles, permissions trop larges, données personnelles écrites en clair. Tu apprendras donc les bons réflexes en même temps que la technique.

## 📖 Concepts clés

### 1. Ouvrir, lire, écrire

La fonction `open()` renvoie un objet fichier. On l'utilise presque toujours avec `with`, qui ferme le fichier automatiquement :

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
print(contenu)
```

**Modes d'ouverture :**

| Mode | Effet |
|---|---|
| `"r"` | Lecture (défaut) ; erreur si le fichier n'existe pas |
| `"w"` | Écriture ; **écrase** le contenu existant ; crée le fichier |
| `"a"` | Ajout à la fin (*append*) ; crée le fichier si besoin |
| `"x"` | Création exclusive ; erreur si le fichier existe déjà |
| `"b"` | Mode binaire (à ajouter : `"rb"`, `"wb"`) |
| `"+"` | Lecture et écriture (`"r+"`) |

**Toujours préciser `encoding="utf-8"`** en mode texte : sans cela, le comportement dépend du système et provoque des erreurs avec les accents.

### 2. Méthodes de lecture

```python
with open("auth.log", "r", encoding="utf-8", errors="ignore") as f:
    tout = f.read()            # tout le fichier dans une seule chaîne
    # f.readline()             # une ligne
    # f.readlines()            # liste de toutes les lignes
```

Pour de gros fichiers, **parcours ligne par ligne** : l'ensemble n'est jamais chargé en mémoire.

```python
with open("auth.log", encoding="utf-8", errors="ignore") as f:
    for numero, ligne in enumerate(f, start=1):
        if "Failed" in ligne:
            print(numero, ligne.strip())
```

`errors="ignore"` (ou `"replace"`) évite qu'un caractère invalide dans un journal (ils en contiennent souvent) ne fasse planter le programme.

### 3. Écrire dans un fichier

```python
alertes = ["203.0.113.45", "198.51.100.7"]

with open("alertes.txt", "w", encoding="utf-8") as f:
    f.write("Adresses signalées\n")
    for ip in alertes:
        f.write(ip + "\n")

with open("alertes.txt", "a", encoding="utf-8") as f:
    f.write("Fin du rapport\n")

# Équivalent pratique avec print
with open("alertes.txt", "a", encoding="utf-8") as f:
    print("Ligne ajoutée", file=f)
```

`write()` n'ajoute **pas** de retour à la ligne automatiquement. `print(..., file=f)` en ajoute un.

### 4. Les chemins avec pathlib

`pathlib` est le module moderne pour manipuler des chemins, de façon **portable** (Windows, Linux, macOS).

```python
from pathlib import Path

dossier = Path("rapports")
dossier.mkdir(exist_ok=True)                  # crée le dossier s'il n'existe pas

fichier = dossier / "analyse.txt"             # l'opérateur / assemble les chemins
fichier.write_text("Résultat\n", encoding="utf-8")
print(fichier.read_text(encoding="utf-8"))

print(fichier.name)          # analyse.txt
print(fichier.stem)          # analyse
print(fichier.suffix)        # .txt
print(fichier.parent)        # rapports
print(fichier.exists())      # True
print(fichier.is_file())     # True
print(fichier.stat().st_size)  # taille en octets
```

**Parcourir des dossiers :**

```python
for chemin in Path(".").glob("*.log"):           # fichiers .log du dossier courant
    print(chemin)

for chemin in Path("/var/log").rglob("*.log"):   # récursif
    print(chemin)

racine = Path.home()                             # dossier personnel
```

Autres outils : `os.listdir()`, `os.walk()`, `shutil.copy()`, `shutil.move()`, `shutil.rmtree()` (supprime un dossier entier, **à manier avec prudence**).

### 5. Sécurité des chemins : path traversal

Si un programme construit un chemin à partir d'une saisie ou d'un paramètre externe, un attaquant peut fournir `../../etc/passwd` pour sortir du dossier prévu. C'est une vulnérabilité classique (*path traversal* ou *directory traversal*).

```python
from pathlib import Path

BASE = Path("/srv/rapports").resolve()

def ouvrir_rapport(nom):
    cible = (BASE / nom).resolve()
    if BASE not in cible.parents and cible != BASE:
        raise PermissionError("Chemin hors du dossier autorisé")
    return cible.read_text(encoding="utf-8")
```

Principes :
- `resolve()` normalise le chemin (supprime `..`, suit les liens) ;
- on vérifie que le résultat reste **dans** le dossier autorisé ;
- on préfère une **liste blanche** de noms autorisés quand c'est possible ;
- on ne fait jamais confiance à un nom de fichier venant de l'extérieur.

### 6. Fichiers binaires

Pour lire des fichiers qui ne sont pas du texte (images, exécutables, archives), on ouvre en mode binaire. On obtient des objets `bytes`.

```python
with open("image.png", "rb") as f:
    entete = f.read(8)
print(entete)                         # b'\x89PNG\r\n\x1a\n'
print(entete == b"\x89PNG\r\n\x1a\n") # True si c'est un vrai PNG
```

Les premiers octets d'un fichier (sa **signature**, ou *magic number*) révèlent son vrai type, quelle que soit son extension. Un fichier nommé `facture.pdf` qui commence par `MZ` est en réalité un exécutable Windows : c'est un indice utilisé en forensic et en analyse de malwares.

| Signature (début) | Type |
|---|---|
| `%PDF` | PDF |
| `PK\x03\x04` | ZIP (et DOCX, XLSX, JAR) |
| `\x89PNG` | PNG |
| `\xff\xd8\xff` | JPEG |
| `MZ` | Exécutable Windows (EXE, DLL) |
| `\x7fELF` | Exécutable Linux |

### 7. Le format CSV

Le **CSV** (*Comma-Separated Values*) est un format de tableau en texte. Python fournit le module `csv`.

**Lecture :**

```python
import csv

with open("scan.csv", newline="", encoding="utf-8") as f:
    lecteur = csv.DictReader(f)         # utilise la 1re ligne comme noms de colonnes
    for ligne in lecteur:
        print(ligne["ip"], ligne["port"], ligne["service"])
```

**Écriture :**

```python
import csv

resultats = [
    {"ip": "192.168.1.10", "port": 22, "service": "ssh"},
    {"ip": "192.168.1.10", "port": 443, "service": "https"},
]
with open("resultats.csv", "w", newline="", encoding="utf-8") as f:
    ecrivain = csv.DictWriter(f, fieldnames=["ip", "port", "service"])
    ecrivain.writeheader()
    ecrivain.writerows(resultats)
```

⚠️ **Injection CSV** : si une cellule commence par `=`, `+`, `-` ou `@`, Excel ou LibreOffice peut l'interpréter comme une **formule** à l'ouverture. Quand tu exportes des données issues de sources non fiables (noms, commentaires), préfixe ces cellules par une apostrophe ou une espace, ou neutralise ces caractères.

### 8. Le format JSON

**JSON** est le format d'échange des API web et de nombreux outils. Il correspond aux dictionnaires, listes, chaînes, nombres, booléens et `null` (`None`) de Python.

```python
import json

donnees = {
    "machine": "web-01",
    "ports": [22, 443],
    "ouvert_internet": True
}

# Écrire
with open("machine.json", "w", encoding="utf-8") as f:
    json.dump(donnees, f, ensure_ascii=False, indent=2)

# Lire
with open("machine.json", encoding="utf-8") as f:
    charge = json.load(f)
print(charge["ports"])

# Depuis / vers une chaîne
texte = json.dumps(donnees)
objet = json.loads(texte)
```

Gérer les erreurs : un JSON mal formé lève `json.JSONDecodeError`.

```python
try:
    objet = json.loads('{"a": 1,}')      # virgule en trop
except json.JSONDecodeError as e:
    print("JSON invalide :", e)
```

**Sécurité** : n'utilise **jamais** `pickle` pour charger des fichiers venant d'une source non fiable, car la désérialisation d'un fichier pickle piégé peut exécuter du code. Préfère JSON pour les échanges de données.

### 9. Les expressions régulières (module re)

Une **expression régulière** (*regex*) décrit un motif de texte. Elle permet d'extraire des adresses IP, des e-mails, des dates, des identifiants… depuis un texte brut.

```python
import re

ligne = "Failed password for admin from 203.0.113.45 port 51822 ssh2"

motif_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
print(re.findall(motif_ip, ligne))             # ['203.0.113.45']

m = re.search(r"for (\w+) from ([\d.]+) port (\d+)", ligne)
if m:
    utilisateur, ip, port = m.groups()
    print(utilisateur, ip, port)               # admin 203.0.113.45 51822
```

**Éléments de syntaxe :**

| Motif | Signification |
|---|---|
| `.` | N'importe quel caractère |
| `\d`, `\w`, `\s` | Chiffre, caractère de mot, espace |
| `+`, `*`, `?` | Un ou plus, zéro ou plus, optionnel |
| `{n}`, `{n,m}` | Exactement n, entre n et m fois |
| `[abc]`, `[^abc]` | Un caractère parmi, un caractère sauf |
| `^`, `$` | Début, fin de ligne |
| `( )` | Groupe capturé |
| `\b` | Limite de mot |
| `\|` | Ou |

Utilise toujours des **chaînes brutes** `r"..."` pour les regex (le `\` n'est alors pas interprété par Python).

Fonctions principales : `re.search` (première occurrence), `re.findall` (toutes), `re.match` (au début), `re.sub` (remplacer), `re.compile` (précompiler un motif utilisé souvent).

⚠️ **Attention** : le motif IP ci-dessus accepte `999.999.999.999`. Pour valider une adresse, combine la regex avec `ipaddress.ip_address()` (leçon 04). Et prends garde aux regex mal conçues : certains motifs provoquent une **explosion combinatoire** (*ReDoS*) sur des entrées forgées, qui bloque le programme.

### 10. Un outil complet : extraire et résumer les IP d'un journal

```python
import csv
import json
import re
import ipaddress
from collections import Counter
from pathlib import Path

MOTIF = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

def extraire_ips(chemin):
    compteur = Counter()
    with open(chemin, encoding="utf-8", errors="ignore") as f:
        for ligne in f:
            for candidat in MOTIF.findall(ligne):
                try:
                    compteur[str(ipaddress.ip_address(candidat))] += 1
                except ValueError:
                    continue
    return compteur

def exporter(compteur, dossier):
    dossier = Path(dossier)
    dossier.mkdir(exist_ok=True)
    with open(dossier / "ips.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ip", "occurrences", "privee"])
        for ip, n in compteur.most_common():
            w.writerow([ip, n, ipaddress.ip_address(ip).is_private])
    (dossier / "ips.json").write_text(
        json.dumps(compteur.most_common(), indent=2), encoding="utf-8")

if __name__ == "__main__":
    c = extraire_ips("auth.log")
    exporter(c, "sortie")
    print(f"{len(c)} adresses distinctes exportées")
```

### 11. Bonnes pratiques de sécurité sur les fichiers

- **Permissions** : un fichier contenant des secrets ou des données personnelles se crée avec des droits restreints.

```python
import os
fd = os.open("secret.txt", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, "w") as f:
    f.write("donnée sensible\n")
```

- **Fichiers temporaires** : utilise `tempfile` (noms imprévisibles, droits restrictifs), pas `/tmp/resultat.txt`.

```python
import tempfile
with tempfile.NamedTemporaryFile("w", delete=True, encoding="utf-8") as tmp:
    tmp.write("données éphémères")
```

- **Ne jamais écrire de mots de passe ou de jetons en clair** dans des journaux ou des exports.
- **Limiter la taille** lue pour les fichiers d'origine inconnue (`f.read(10_000_000)`).
- **Vérifier le type réel** d'un fichier reçu (signature), pas seulement son extension.
- **Données personnelles** : minimiser, anonymiser quand c'est possible, supprimer ce qui n'est plus utile.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : n'analyse que **tes fichiers** ou des fichiers d'exercice. Les journaux d'un système tiers contiennent souvent des données personnelles (adresses IP, identifiants) protégées par la loi.

### Exercice 1 — Lire et écrire

1. Crée `joueurs.txt` avec trois noms (un par ligne), en Python.
2. Relis-le et affiche chaque nom en majuscules, avec son numéro de ligne.
3. Ajoute un quatrième nom en mode `"a"`.

```python
with open("joueurs.txt", "w", encoding="utf-8") as f:
    f.write("alice\nbob\ncharlie\n")
with open("joueurs.txt", "a", encoding="utf-8") as f:
    f.write("diane\n")
with open("joueurs.txt", encoding="utf-8") as f:
    for n, nom in enumerate(f, 1):
        print(n, nom.strip().upper())
```

### Exercice 2 — Compter les mots

Écris `compter_mots(chemin)` qui renvoie un `Counter` des mots d'un fichier (en minuscules, sans ponctuation). Affiche les 5 plus fréquents. Teste-la sur un texte de ton choix.

### Exercice 3 — Pathlib

1. Crée un dossier `labo/` contenant trois fichiers `a.log`, `b.log` et `c.txt`.
2. Liste uniquement les `.log` avec `glob`.
3. Pour chacun, affiche son nom, sa taille et si elle dépasse 0 octet.

### Exercice 4 — Détecter le vrai type d'un fichier

Écris `type_reel(chemin)` qui lit les premiers octets et renvoie « PDF », « ZIP », « PNG », « JPEG », « EXE », « ELF » ou « inconnu ». Teste-la en **renommant** un fichier PNG en `.txt` : ta fonction doit toujours répondre « PNG ».

```python
SIGNATURES = {
    b"%PDF": "PDF",
    b"PK\x03\x04": "ZIP",
    b"\x89PNG": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"MZ": "EXE",
    b"\x7fELF": "ELF",
}

def type_reel(chemin):
    with open(chemin, "rb") as f:
        debut = f.read(8)
    for signature, nom in SIGNATURES.items():
        if debut.startswith(signature):
            return nom
    return "inconnu"
```

Question guidée : pourquoi est-ce utile en enquête ? (Un fichier peut être déguisé en changeant son extension.)

### Exercice 5 — CSV vers JSON

1. Crée `machines.csv` :

```
nom,ip,os
web-01,192.168.1.10,Ubuntu
db-01,192.168.1.20,Debian
poste-07,192.168.1.57,Windows
```

2. Lis-le avec `csv.DictReader` et écris `machines.json` (liste de dictionnaires).
3. Relis le JSON et affiche les machines Linux.

### Exercice 6 — Extraire les IP d'un journal

Utilise l'outil de la section 10 sur le fichier `auth.log` de la leçon 03. Vérifie que `ips.csv` et `ips.json` sont créés. Ouvre le CSV dans un tableur. Combien d'adresses distinctes ? Lesquelles sont privées ?

### Exercice 7 — Regex : extraire plusieurs champs

À partir de lignes d'accès web de ce type :

```
203.0.113.45 - - [03/Oct/2026:10:15:22 +0100] "GET /admin HTTP/1.1" 403 512
```

Écris une regex avec groupes pour récupérer : IP, date, méthode, chemin, code de réponse. Puis affiche les requêtes dont le code est `403` ou `404`.

```python
import re
motif = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<date>[^\]]+)\] "(?P<methode>\w+) (?P<chemin>\S+) [^"]*" (?P<code>\d{3})'
)
ligne = '203.0.113.45 - - [03/Oct/2026:10:15:22 +0100] "GET /admin HTTP/1.1" 403 512'
m = motif.match(ligne)
if m:
    print(m.groupdict())
```

### Exercice 8 — Défi : chemin sûr

Écris une fonction `lire_dans_dossier(base, nom)` qui refuse tout nom provoquant une sortie du dossier `base` (teste avec `../secret.txt`, `/etc/passwd`, `sous/../../x`). Elle doit lever `PermissionError` dans ces cas et lire le fichier sinon.

## 🔍 Approfondissement

### Pour aller plus loin

- Documentation officielle : modules `pathlib`, `csv`, `json`, `re`, `tempfile`, `shutil`.
- **regex101.com** pour tester et comprendre des expressions régulières.
- Le HOWTO « Expressions régulières » de la documentation Python (en français).

### Pièges courants

- ❌ **Erreur fréquente 1** : ouvrir en mode `"w"` un fichier existant et perdre son contenu.
- ✅ **Bonne pratique** : utiliser `"a"` pour ajouter, ou `"x"` pour refuser d'écraser.
- ❌ **Erreur fréquente 2** : oublier `encoding="utf-8"` et obtenir des caractères illisibles ou des erreurs.
- ✅ **Bonne pratique** : toujours préciser l'encodage en mode texte.
- ❌ **Erreur fréquente 3** : lire un gros fichier d'un coup avec `read()` et saturer la mémoire.
- ✅ **Bonne pratique** : parcourir ligne par ligne ou par blocs.
- ❌ **Erreur fréquente 4** : construire un chemin avec une saisie utilisateur sans vérification.
- ✅ **Bonne pratique** : `resolve()` puis contrôle que le chemin reste dans le dossier autorisé.
- ❌ **Erreur fréquente 5** : charger des fichiers `pickle` de provenance inconnue.
- ✅ **Bonne pratique** : JSON pour les données externes.

## 🧪 Quiz de validation

**Question 1 : Quel mode d'ouverture ajoute du texte à la fin d'un fichier sans l'écraser ?**
- A) `"r"`
- B) `"w"`
- C) `"a"` ✅
- D) `"b"`

*Explication : `"a"` (append) conserve le contenu existant et écrit à la suite ; `"w"` l'efface.*

**Question 2 : Pourquoi lire un gros journal ligne par ligne ?**
- A) C'est plus joli
- B) Pour ne pas charger tout le fichier en mémoire ✅
- C) Pour chiffrer le contenu
- D) Parce que `read()` n'existe pas

*Explication : la boucle `for ligne in fichier` consomme très peu de mémoire, même pour des fichiers de plusieurs gigaoctets.*

**Question 3 : Que permet de détecter la signature (magic number) d'un fichier ?**
- A) Son auteur
- B) Son vrai type, même si l'extension a été modifiée ✅
- C) Son mot de passe
- D) Sa date de création

*Explication : les premiers octets identifient le format réel (ex. `%PDF`, `MZ`), indépendamment du nom.*

**Question 4 : Quelle vulnérabilité exploite un chemin comme `../../etc/passwd` ?**
- A) L'injection SQL
- B) Le path traversal (traversée de répertoires) ✅
- C) Le XSS
- D) Le SYN flood

*Explication : l'attaquant remonte l'arborescence pour sortir du dossier prévu et lire un fichier sensible.*

**Question 5 : Pourquoi éviter `pickle` pour des données de source non fiable ?**
- A) Il est trop lent
- B) La désérialisation d'un fichier piégé peut exécuter du code arbitraire ✅
- C) Il ne gère pas les listes
- D) Il ne fonctionne pas sous Linux

*Explication : `pickle` peut reconstruire des objets qui exécutent du code ; JSON ne transporte que des données.*

## 📝 Résumé

- `with open(..., encoding="utf-8")` lit et écrit des fichiers en les fermant automatiquement ; les modes `"r"`, `"w"`, `"a"`, `"x"` et `"b"` couvrent les besoins courants.
- `pathlib` manipule les chemins de façon portable ; `resolve()` et un contrôle de dossier protègent contre le path traversal.
- Les signatures (magic numbers) révèlent le vrai type d'un fichier.
- Les modules `csv` et `json` lisent et écrivent des données structurées ; attention à l'injection CSV et à `pickle`.
- Les expressions régulières extraient des champs d'un texte ; on valide ensuite avec `ipaddress`.
- Fichiers temporaires, permissions restrictives et minimisation des données sont des pratiques de sécurité à part entière.

## 🎓 Ce que tu as appris

✅ Lire et écrire des fichiers texte, binaires, CSV et JSON
✅ Manipuler chemins et dossiers avec `pathlib`
✅ Extraire des informations avec des regex
✅ Éviter le path traversal et les erreurs de sécurité courantes

## ➡️ Leçon suivante

**06 : Requêtes HTTP en Python** : envoyer des requêtes avec la bibliothèque `requests`, gérer en-têtes, cookies, délais et erreurs. Fichier : `06-requetes-http-python.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
