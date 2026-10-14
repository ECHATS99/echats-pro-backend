---
title: "Web Scraping avec BeautifulSoup"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 7
category: "python"
tags: ["python", "scraping", "beautifulsoup", "html", "osint", "robots-txt", "ethique"]
prerequisites: ["06-requetes-http-python", "05-fichiers-io"]
learning_objectives:
  - "Comprendre la structure d'une page HTML et les sélecteurs CSS"
  - "Extraire titres, liens, tableaux et métadonnées avec BeautifulSoup"
  - "Respecter robots.txt, les conditions d'utilisation et la loi"
  - "Construire un petit collecteur d'informations publiques et exporter les résultats"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Web Scraping avec BeautifulSoup

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Comprendre la structure d'une page HTML et les sélecteurs CSS
- Extraire titres, liens, tableaux et métadonnées avec BeautifulSoup
- Respecter `robots.txt`, les conditions d'utilisation et la loi
- Construire un petit collecteur d'informations publiques et exporter les résultats

## 📚 Prérequis

- Leçon 06 : *Requêtes HTTP en Python*
- Leçon 05 : *Fichiers et entrées/sorties* (CSV, JSON)
- Notions de HTTP (leçon 06 du module Réseau & Linux)

## 🧭 Introduction

Une page web est faite pour être lue par un humain, mais derrière l'affichage se cache du **HTML**, un texte structuré qu'un programme peut analyser. Le **web scraping** (extraction de données web) consiste à télécharger une page puis à en extraire automatiquement les informations utiles : le titre d'un article, une liste de prix, les liens d'une page, les membres d'une équipe, les coordonnées publiques d'une organisation.

En cybersécurité, le scraping est une brique de l'**OSINT** (*Open Source Intelligence*, renseignement d'origine sources ouvertes). Un analyste l'utilise pour surveiller des publications de vulnérabilités, collecter des indicateurs de menaces publiés sur des blogs, cartographier la présence en ligne d'une organisation (dans un audit autorisé), ou vérifier ce que ses propres sites exposent publiquement.

Mais le scraping touche immédiatement à des questions de **droit et d'éthique** : droits d'auteur, conditions d'utilisation, protection des données personnelles, charge imposée aux serveurs. Ce n'est pas parce qu'une information est techniquement accessible qu'on a le droit de la collecter massivement ou de la réutiliser. Cette leçon t'apprend la technique **et** le cadre dans lequel l'utiliser.

## 📖 Concepts clés

### 1. HTML en deux minutes

Une page HTML est un **arbre** d'éléments imbriqués, délimités par des **balises** :

```html
<html>
  <head>
    <title>Alertes de sécurité</title>
    <meta name="description" content="Bulletins publics">
  </head>
  <body>
    <h1 id="titre">Bulletins récents</h1>
    <ul class="liste">
      <li class="alerte critique"><a href="/b/101">Faille dans le serveur X</a></li>
      <li class="alerte"><a href="/b/102">Mise à jour du logiciel Y</a></li>
    </ul>
    <table>
      <tr><th>CVE</th><th>Score</th></tr>
      <tr><td>CVE-2026-0001</td><td>9.8</td></tr>
    </table>
  </body>
</html>
```

Vocabulaire :
- **balise** : `<h1>…</h1>` (ouvrante et fermante) ;
- **attribut** : `href="/b/101"`, `class="alerte"`, `id="titre"` ;
- **classe** (`class`) : étiquette réutilisable ; **identifiant** (`id`) : unique dans la page ;
- **parent / enfant / frère** : relations dans l'arbre.

Dans ton navigateur, **clic droit → Inspecter** (F12) montre cet arbre. C'est l'outil indispensable pour trouver *où* se trouve l'information à extraire.

### 2. Installer BeautifulSoup

```bash
pip install requests beautifulsoup4 lxml
```

- `beautifulsoup4` : l'analyseur (on l'importe sous le nom `bs4`) ;
- `lxml` : analyseur rapide ; à défaut, `html.parser` est intégré à Python.

### 3. Premier scraping

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://example.com", timeout=10,
                 headers={"User-Agent": "ECHATS-Formation/1.0 (contact@exemple.cg)"})
r.raise_for_status()

soupe = BeautifulSoup(r.text, "html.parser")
print(soupe.title.string)             # Example Domain
print(soupe.h1.get_text(strip=True))  # texte du premier <h1>

for lien in soupe.find_all("a"):
    print(lien.get("href"), lien.get_text(strip=True))
```

### 4. Naviguer et chercher

**Recherche par balise, classe, identifiant :**

```python
soupe.find("h1")                               # premier <h1>
soupe.find_all("li")                           # tous les <li>
soupe.find("h1", id="titre")                   # par identifiant
soupe.find_all("li", class_="alerte")          # par classe (class_ avec underscore)
soupe.find_all("a", href=True)                 # <a> possédant un attribut href
soupe.find_all(["h1", "h2", "h3"])             # plusieurs balises
```

**Sélecteurs CSS** (très pratiques, avec `select` et `select_one`) :

```python
soupe.select("ul.liste li a")          # <a> dans <li> dans <ul class="liste">
soupe.select_one("#titre")             # par identifiant
soupe.select("li.alerte.critique")     # deux classes
soupe.select("table tr td:nth-of-type(1)")
soupe.select('a[href^="/b/"]')         # href commençant par /b/
```

**Lire le contenu :**

```python
element = soupe.select_one("li.alerte a")
print(element.get_text(strip=True))    # texte sans espaces superflus
print(element["href"])                 # attribut (KeyError s'il est absent)
print(element.get("href"))             # None s'il est absent
print(element.attrs)                   # dictionnaire des attributs
```

**Naviguer dans l'arbre :**

```python
element.parent
element.find_next_sibling("li")
element.children      # enfants directs
element.find_parent("ul")
```

### 5. Extraire un tableau

```python
lignes = []
for tr in soupe.select("table tr"):
    cellules = [c.get_text(strip=True) for c in tr.find_all(["th", "td"])]
    if cellules:
        lignes.append(cellules)
print(lignes)      # [['CVE', 'Score'], ['CVE-2026-0001', '9.8']]
```

Le même résultat se fait avec `pandas.read_html`, mais comprendre la mécanique reste précieux.

### 6. Liens relatifs et absolus

Les liens d'une page sont souvent **relatifs** (`/b/101`). Pour obtenir l'URL complète :

```python
from urllib.parse import urljoin, urlparse

base = "https://exemple.org/bulletins/"
absolu = urljoin(base, "/b/101")        # https://exemple.org/b/101
print(urlparse(absolu).netloc)          # exemple.org
```

Pour ne rester que sur le même domaine, compare `urlparse(url).netloc`.

### 7. Métadonnées utiles

```python
description = soupe.find("meta", attrs={"name": "description"})
if description:
    print(description.get("content"))

for meta in soupe.find_all("meta", property=True):      # balises Open Graph
    print(meta["property"], meta.get("content"))

for script in soupe.find_all("script", src=True):       # scripts externes
    print("Script :", script["src"])
```

En audit de **ses propres** sites, ces informations révèlent les bibliothèques chargées, les services tiers (analytique, traqueurs) et d'éventuels commentaires HTML oubliés (`<!-- mot de passe de test -->`) :

```python
from bs4 import Comment
for c in soupe.find_all(string=lambda t: isinstance(t, Comment)):
    print("Commentaire :", c.strip())
```

### 8. Pages dynamiques (JavaScript)

Certaines pages chargent leur contenu **après coup** avec du JavaScript. Dans ce cas, `requests` ne voit que la « coquille » vide. Options, du plus simple au plus lourd :
1. **Chercher l'API** utilisée par la page (onglet Réseau des outils de développement) : souvent, les données arrivent déjà en JSON, plus simple à exploiter (leçon 08).
2. Utiliser un navigateur automatisé (**Selenium**, **Playwright**) pour exécuter le JavaScript.

Si un site fournit une **API officielle**, c'est toujours préférable au scraping : plus stable, légale et explicite sur les limites.

### 9. Le cadre éthique et légal : indispensable

**robots.txt** : fichier à la racine d'un site (`https://exemple.org/robots.txt`) qui indique aux robots ce qu'ils peuvent ou non visiter.

```
User-agent: *
Disallow: /admin/
Disallow: /prive/
Crawl-delay: 10
```

Python sait le lire :

```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("https://exemple.org/robots.txt")
rp.read()
if rp.can_fetch("ECHATS-Formation", "https://exemple.org/bulletins/"):
    print("Autorisé")
```

Ce fichier est une **convention de politesse**, pas une barrière technique, mais le respecter est une règle de base de l'éthique, et l'ignorer peut être retenu contre toi.

**Règles à suivre :**

| Règle | Détail |
|---|---|
| **Conditions d'utilisation** | Lis-les. Beaucoup interdisent le scraping automatisé ou la réutilisation des données |
| **Droit d'auteur** | Un contenu reste protégé : le collecter pour analyse n'autorise pas à le republier |
| **Données personnelles** | Noms, e-mails, photos, numéros de téléphone sont des données personnelles : les lois (RGPD en Europe, lois nationales ailleurs) encadrent leur collecte et leur usage, **même si elles sont publiques** |
| **Charge** | Une requête à la fois, une pause d'au moins 1 à 2 secondes, jamais de rafales |
| **Identification** | User-Agent explicite avec un moyen de contact |
| **Accès protégés** | Ne contourne jamais une authentification, un CAPTCHA, un blocage ou un paywall |
| **Finalité** | Collecte uniquement ce qui est nécessaire à un objectif légitime et documenté |
| **Stockage** | Sécurise les données collectées, supprime-les quand elles ne servent plus |

Un principe simple : **si tu n'oserais pas expliquer ton scraping à l'éditeur du site ou à la personne concernée, ne le fais pas.**

### 10. Un collecteur poli et complet

```python
import csv
import time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

UA = "ECHATS-Formation/1.0 (contact: ton-email@exemple.cg)"
PAUSE = 2.0   # secondes entre deux requêtes

def robots_autorise(url):
    parsed = urlparse(url)
    rp = RobotFileParser()
    rp.set_url(f"{parsed.scheme}://{parsed.netloc}/robots.txt")
    try:
        rp.read()
    except Exception:
        return False           # dans le doute, on s'abstient
    return rp.can_fetch(UA, url)

def collecter_liens(url):
    if not robots_autorise(url):
        print("Interdit par robots.txt :", url)
        return []
    r = requests.get(url, headers={"User-Agent": UA}, timeout=10)
    r.raise_for_status()
    soupe = BeautifulSoup(r.text, "html.parser")
    resultats = []
    for a in soupe.find_all("a", href=True):
        resultats.append({
            "texte": a.get_text(strip=True),
            "url": urljoin(url, a["href"]),
        })
    return resultats

def exporter(liens, fichier):
    with open(fichier, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["texte", "url"])
        w.writeheader()
        w.writerows(liens)

if __name__ == "__main__":
    liens = collecter_liens("https://example.com")
    exporter(liens, "liens.csv")
    time.sleep(PAUSE)
    print(f"{len(liens)} liens exportés")
```

Remarque : ce programme **vérifie `robots.txt`**, **s'identifie**, **temporise** et **gère les erreurs** (à étendre avec `try/except`, voir leçon 06). C'est le modèle à reproduire.

### 11. Scraping et sécurité défensive

Le scraping n'est pas qu'offensif ou OSINT. Côté défense :
- **Surveiller ce qui fuit** : vérifier que les pages publiques de ton organisation n'exposent pas d'e-mails internes, de commentaires de développement, de chemins de fichiers.
- **Détecter les scrapers abusifs** : un nombre anormal de requêtes depuis une même adresse, un User-Agent générique, des accès à des pages qu'aucun humain ne visite sont des signaux ; on y répond avec limitation de débit (*rate limiting*), CAPTCHA, ou en rendant les données disponibles par API contrôlée.
- **Veille** : suivre des flux publics de bulletins de sécurité et d'indicateurs de compromission (en privilégiant les flux RSS et API officiels).

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : pour t'entraîner, utilise des sites **conçus pour le scraping** — `books.toscrape.com` et `quotes.toscrape.com` — ou **tes propres pages** hébergées en local (par exemple `python3 -m http.server`). Ne collecte pas de données personnelles de tiers, ne cible pas de réseau social ni de site qui l'interdit, et reste limité à quelques pages.

### Exercice 1 — Inspecter avant de coder

1. Ouvre `https://quotes.toscrape.com` dans ton navigateur.
2. Clic droit sur une citation → **Inspecter**.
3. Repère : la balise qui contient le texte, celle de l'auteur, celle des étiquettes (tags). Note leurs classes (par exemple `quote`, `text`, `author`).

### Exercice 2 — Extraire des citations

```python
import requests
from bs4 import BeautifulSoup

UA = {"User-Agent": "ECHATS-Formation/1.0"}
r = requests.get("https://quotes.toscrape.com", headers=UA, timeout=10)
soupe = BeautifulSoup(r.text, "html.parser")

for bloc in soupe.select("div.quote"):
    texte = bloc.select_one("span.text").get_text(strip=True)
    auteur = bloc.select_one("small.author").get_text(strip=True)
    tags = [t.get_text(strip=True) for t in bloc.select("a.tag")]
    print(f"{auteur} : {texte}  {tags}")
```

Questions guidées : combien de citations par page ? Comment accèderais-tu à la page suivante ? (Lien `li.next a`.)

### Exercice 3 — Plusieurs pages, poliment

Étends l'exercice 2 pour parcourir **3 pages au maximum**, avec une pause de 2 secondes entre chaque page, en suivant le lien « Next ». Enregistre les citations dans `citations.csv` (colonnes : auteur, texte, tags).

### Exercice 4 — Un tableau de livres

Sur `https://books.toscrape.com`, extrais pour la **première page** : le titre (attribut `title` du lien dans `h3`), le prix (`p.price_color`) et la disponibilité (`p.availability`). Construis une liste de dictionnaires et exporte-la en JSON. Affiche ensuite le livre le moins cher.

### Exercice 5 — robots.txt en pratique

1. Télécharge et affiche `https://quotes.toscrape.com/robots.txt` (s'il existe) et celui de `https://example.com`.
2. Écris `autorise(url)` à l'aide de `RobotFileParser`.
3. Teste-la sur plusieurs chemins et explique pourquoi un robot poli s'abstient quand `can_fetch` renvoie `False`.

### Exercice 6 — Audit de TA page

Crée un fichier `test.html` local avec : un titre, des commentaires HTML, deux scripts externes, une balise `meta`, et une adresse e-mail en clair. Lance `python3 -m http.server 8000` dans le dossier, puis écris un script qui :
1. affiche le titre ;
2. liste les scripts externes ;
3. liste les commentaires HTML ;
4. cherche les adresses e-mail avec une regex (leçon 05).

Question guidée : quelles informations ce type d'analyse révèle-t-il à un visiteur curieux ? Quelles sont les bonnes pratiques pour ne pas exposer d'adresses personnelles ou de commentaires internes ?

### Exercice 7 — Extraire un tableau HTML

Crée un fichier HTML avec un tableau de 5 lignes (hôte, adresse IP, statut). Extrais-le en liste de dictionnaires, puis calcule combien d'hôtes sont « hors ligne ».

### Exercice 8 — Défi : surveillance d'une page de bulletins (cas fictif)

Mets en place localement une page `bulletins.html` contenant trois bulletins de sécurité. Écris un script qui la télécharge toutes les 30 secondes (3 tours), compare avec la version précédente (liste des titres) et affiche **uniquement les nouveautés**. Modifie la page entre deux tours pour tester. Application réelle : surveiller la page de bulletins d'un éditeur de logiciels **dont les conditions autorisent l'automatisation**, ou, mieux, son flux RSS.

## 🔍 Approfondissement

### Pour aller plus loin

- Documentation de BeautifulSoup (crummy.com/software/BeautifulSoup/bs4/doc) et de `lxml`.
- **Scrapy** : framework complet de collecte à grande échelle (avec politesse intégrée).
- Playwright ou Selenium pour les pages dynamiques ; `feedparser` pour les flux RSS.
- La CNIL (France) et les autorités de protection des données de ton pays : guides sur la réutilisation de données publiques.

### Pièges courants

- ❌ **Erreur fréquente 1** : scraper sans lire `robots.txt` ni les conditions d'utilisation.
- ✅ **Bonne pratique** : lire, respecter, documenter.
- ❌ **Erreur fréquente 2** : écrire des sélecteurs trop fragiles (dépendant de la position exacte) qui cassent à la moindre mise en page.
- ✅ **Bonne pratique** : cibler des classes et attributs stables, prévoir les cas `None`.
- ❌ **Erreur fréquente 3** : appeler `.text` ou `.get_text()` sur `None` (`AttributeError`) quand un élément n'existe pas.
- ✅ **Bonne pratique** : tester `if element:` avant de lire son contenu.
- ❌ **Erreur fréquente 4** : collecter massivement des données personnelles « parce qu'elles sont publiques ».
- ✅ **Bonne pratique** : minimisation, finalité légitime, durée de conservation limitée.
- ❌ **Erreur fréquente 5** : ignorer les pages chargées en JavaScript et conclure que « le site est vide ».
- ✅ **Bonne pratique** : chercher l'API sous-jacente ou utiliser un navigateur automatisé.

## 🧪 Quiz de validation

**Question 1 : À quoi sert le fichier `robots.txt` ?**
- A) Il chiffre le site
- B) Il indique aux robots les parties du site qu'ils peuvent ou non visiter ✅
- C) Il liste les mots de passe
- D) Il accélère le serveur

*Explication : c'est une convention que les robots respectueux suivent avant de parcourir un site.*

**Question 2 : Quelle méthode BeautifulSoup utilise un sélecteur CSS ?**
- A) `find_all()`
- B) `select()` ✅
- C) `get_text()`
- D) `parse()`

*Explication : `select` et `select_one` acceptent des sélecteurs CSS comme `ul.liste li a`.*

**Question 3 : Pourquoi `requests` ne voit-il parfois qu'une page presque vide ?**
- A) Le site est en panne
- B) Le contenu est chargé dynamiquement par JavaScript après le chargement initial ✅
- C) BeautifulSoup est défectueux
- D) Le certificat est expiré

*Explication : `requests` n'exécute pas le JavaScript ; il faut utiliser l'API de la page ou un navigateur automatisé.*

**Question 4 : Une information publique sur une personne peut-elle être collectée sans limite ?**
- A) Oui, puisqu'elle est publique
- B) Non, la collecte et la réutilisation de données personnelles restent encadrées par la loi ✅
- C) Oui, si on utilise un VPN
- D) Oui, si on la stocke chiffrée

*Explication : le caractère public d'une donnée ne supprime pas les obligations de finalité, de minimisation et de protection.*

**Question 5 : Quelle pratique rend un scraper « poli » ?**
- A) Envoyer des requêtes en parallèle le plus vite possible
- B) S'identifier par un User-Agent, temporiser entre les requêtes et respecter `robots.txt` ✅
- C) Cacher son identité pour éviter d'être bloqué
- D) Contourner les CAPTCHA

*Explication : identification, pauses et respect des règles du site limitent la charge et montrent une démarche de bonne foi.*

## 📝 Résumé

- Le HTML est un arbre de balises ; l'inspecteur du navigateur aide à repérer les éléments à extraire.
- BeautifulSoup extrait texte, attributs, liens et tableaux avec `find`, `find_all`, `select` et `get_text`.
- `urljoin` convertit les liens relatifs en URL complètes ; les pages dynamiques demandent l'API sous-jacente ou un navigateur automatisé.
- Le scraping doit respecter `robots.txt`, les conditions d'utilisation, le droit d'auteur et la protection des données personnelles.
- Un collecteur poli s'identifie, temporise, gère les erreurs et collecte le strict nécessaire.
- Côté défense, on audite ses propres pages et on détecte les scrapers abusifs.

## 🎓 Ce que tu as appris

✅ Lire la structure d'une page HTML et cibler les bons éléments
✅ Extraire liens, textes, tableaux et métadonnées
✅ Respecter le cadre légal et éthique de la collecte
✅ Exporter des résultats en CSV et JSON

## ➡️ Leçon suivante

**08 : API REST en Python** : interroger des API publiques, gérer authentification, pagination et limites de débit, et exploiter les réponses JSON. Fichier : `08-api-rest-python.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
