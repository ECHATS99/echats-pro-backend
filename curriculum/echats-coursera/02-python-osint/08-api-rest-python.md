---
title: "API REST en Python"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 8
category: "python"
tags: ["python", "api", "rest", "json", "authentification", "pagination", "rate-limit", "osint"]
prerequisites: ["06-requetes-http-python", "05-fichiers-io", "04-fonctions-modules"]
learning_objectives:
  - "Expliquer ce qu'est une API REST et ses principes"
  - "Interroger une API publique avec authentification, pagination et gestion des limites"
  - "Exploiter et transformer des réponses JSON"
  - "Sécuriser l'usage des clés d'API et construire un client réutilisable"
author: "ECHATS PRO"
language: "fr"
published: true
---

# API REST en Python

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Expliquer ce qu'est une API REST et ses principes
- Interroger une API publique avec authentification, pagination et gestion des limites
- Exploiter et transformer des réponses JSON
- Sécuriser l'usage des clés d'API et construire un client réutilisable

## 📚 Prérequis

- Leçon 06 : *Requêtes HTTP en Python*
- Leçons 04 et 05 : fonctions, erreurs, JSON

## 🧭 Introduction

Dans la leçon précédente, tu as extrait des informations de pages HTML conçues pour des humains, avec toute la fragilité que cela suppose : si le site change sa mise en page, ton script casse. Il existe une méthode bien plus propre pour récupérer des données : l'**API** (*Application Programming Interface*).

Une API est une « porte d'entrée » officielle qu'un service met à disposition des programmes. Tu envoies une requête précise, tu reçois une réponse structurée, presque toujours en **JSON**. Pas de HTML à décortiquer, pas de mise en page : juste les données. Et surtout, c'est **explicitement autorisé**, avec des règles claires (limites, authentification, conditions).

En cybersécurité, les API sont partout. Les bases de vulnérabilités (CVE), les services de réputation d'adresses IP, les moteurs de recherche d'appareils connectés, les plateformes de renseignement sur les menaces, les outils de supervision et les services cloud exposent tous une API. Un analyste qui sait les interroger peut **enrichir** une alerte en quelques secondes : « cette adresse IP est-elle connue pour des attaques ? », « cette vulnérabilité est-elle exploitée activement ? ».

Dans cette leçon, tu apprendras à interroger une API REST de façon propre, sûre et réutilisable.

## 📖 Concepts clés

### 1. Qu'est-ce qu'une API REST ?

**REST** (*Representational State Transfer*) est un style d'architecture pour des API construites sur HTTP. Ses principes :

- les **ressources** sont identifiées par des **URL** (`/utilisateurs/42`, `/vulnerabilites/CVE-2026-0001`) ;
- on agit sur elles avec les **méthodes HTTP** : `GET` (lire), `POST` (créer), `PUT`/`PATCH` (modifier), `DELETE` (supprimer) ;
- les échanges sont **sans état** : chaque requête contient tout ce qu'il faut (y compris l'authentification) ;
- les données circulent le plus souvent en **JSON** ;
- les **codes HTTP** disent le résultat : `200` OK, `201` créé, `400` requête invalide, `401` non authentifié, `403` interdit, `404` introuvable, `429` trop de requêtes, `500` erreur serveur.

Exemple de correspondance :

| Action | Requête |
|---|---|
| Lister les articles | `GET /api/articles` |
| Lire l'article 7 | `GET /api/articles/7` |
| Créer un article | `POST /api/articles` + corps JSON |
| Modifier l'article 7 | `PUT /api/articles/7` + corps JSON |
| Supprimer l'article 7 | `DELETE /api/articles/7` |

### 2. Lire la documentation d'une API

Avant tout code, lis la documentation officielle. Elle indique :
- l'**URL de base** (`https://api.exemple.org/v2`) ;
- les **points d'accès** (*endpoints*) et leurs paramètres ;
- le mode d'**authentification** ;
- les **limites de débit** (quotas) ;
- le **format des réponses** et des erreurs ;
- les **conditions d'utilisation** (usage commercial, redistribution, délai de mise en cache).

Beaucoup d'API publient une description au format **OpenAPI / Swagger**, avec une page interactive pour tester les requêtes.

### 3. Premier appel : une API publique de test

`jsonplaceholder.typicode.com` est une fausse API conçue pour s'entraîner.

```python
import requests

r = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=10)
r.raise_for_status()
article = r.json()
print(article["title"])
print(article["userId"])
```

`r.json()` transforme directement le corps JSON en dictionnaire Python.

**Liste et filtrage par paramètres :**

```python
r = requests.get("https://jsonplaceholder.typicode.com/posts",
                 params={"userId": 1}, timeout=10)
articles = r.json()
print(len(articles), "articles pour l'utilisateur 1")
```

**Création (POST) :**

```python
r = requests.post("https://jsonplaceholder.typicode.com/posts",
                  json={"title": "Test", "body": "Contenu", "userId": 1}, timeout=10)
print(r.status_code)     # 201
print(r.json())          # l'objet créé (avec un id)
```

### 4. Authentification

Presque toutes les API réelles demandent de **s'identifier**. Les mécanismes courants :

| Méthode | Principe | Exemple |
|---|---|---|
| **Clé d'API** | Une chaîne secrète envoyée en en-tête ou en paramètre | `X-API-Key: abc123` |
| **Jeton Bearer** | Un jeton (souvent JWT ou OAuth) dans `Authorization` | `Authorization: Bearer <jeton>` |
| **Basic Auth** | Identifiant et mot de passe encodés en Base64 (à n'utiliser qu'en HTTPS) | `auth=("user", "mdp")` |
| **OAuth 2.0** | Délégation d'accès : l'utilisateur autorise une application sans lui donner son mot de passe | Flux d'autorisation avec jeton d'accès |

```python
import os, requests

cle = os.environ.get("MON_API_KEY")
if not cle:
    raise SystemExit("Définis la variable d'environnement MON_API_KEY")

entetes = {"X-API-Key": cle, "Accept": "application/json"}
r = requests.get("https://api.exemple.org/v1/ressource", headers=entetes, timeout=10)
```

**Règles d'or pour les secrets :**
- **jamais** de clé en dur dans le code ;
- **jamais** de clé dans un dépôt Git (utilise un fichier `.env` listé dans `.gitignore`) ;
- **ne journalise jamais** les en-têtes d'authentification ;
- donne à chaque clé le **minimum de droits** nécessaires (moindre privilège) ;
- **révoque et régénère** immédiatement une clé divulguée ;
- une clé gratuite et personnelle ne se partage pas.

Pour les fichiers `.env`, la bibliothèque `python-dotenv` charge les variables :

```python
from dotenv import load_dotenv
load_dotenv()          # lit le fichier .env du dossier courant
```

### 5. Gérer la pagination

Une API ne renvoie pas des millions de résultats d'un coup. Elle les **pagine**. Trois schémas courants :

**a) Par numéro de page :**

```python
def toutes_les_pages(url, params=None):
    page = 1
    while True:
        p = dict(params or {}, page=page, per_page=100)
        r = requests.get(url, params=p, timeout=10)
        r.raise_for_status()
        donnees = r.json()
        if not donnees:
            break
        yield from donnees
        page += 1
```

**b) Par décalage (`offset`/`limit`)** : `?offset=200&limit=100`.

**c) Par curseur** : la réponse contient un jeton `next_cursor` ou un lien `next` à réutiliser.

```python
def parcourir(url):
    while url:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        corps = r.json()
        yield from corps["resultats"]
        url = corps.get("next")          # None à la dernière page
```

`yield from` fait de ces fonctions des **générateurs** : elles produisent les résultats un par un, sans tout charger en mémoire. Ajoute toujours une **limite de sécurité** (nombre de pages maximum) pour éviter une boucle infinie.

### 6. Limites de débit (rate limiting)

Les API limitent le nombre de requêtes (par minute, par jour). Des en-têtes courants indiquent l'état du quota :

| En-tête | Sens |
|---|---|
| `X-RateLimit-Limit` | Quota total |
| `X-RateLimit-Remaining` | Requêtes restantes |
| `X-RateLimit-Reset` | Moment de remise à zéro |
| `Retry-After` | Secondes à attendre après un `429` |

```python
import time

def appel_respectueux(session, url, **kw):
    r = session.get(url, timeout=10, **kw)
    if r.status_code == 429:
        attente = int(r.headers.get("Retry-After", "5"))
        print(f"Quota atteint, pause de {attente}s")
        time.sleep(attente)
        return appel_respectueux(session, url, **kw)
    restantes = r.headers.get("X-RateLimit-Remaining")
    if restantes is not None and int(restantes) < 3:
        time.sleep(2)
    r.raise_for_status()
    return r
```

Respecter les quotas protège aussi **ton** compte : un dépassement répété peut entraîner la suspension de ta clé.

### 7. Traiter les réponses JSON

Les réponses sont des dictionnaires et des listes imbriqués. Accède aux données avec prudence : un champ peut être absent ou `null`.

```python
reponse = {
    "ip": "203.0.113.45",
    "reputation": {"score": 87, "categories": ["scanner", "bruteforce"]},
    "pays": None
}

score = reponse.get("reputation", {}).get("score", 0)
pays = reponse.get("pays") or "inconnu"
categories = ", ".join(reponse.get("reputation", {}).get("categories", []))
print(f"Score {score}, pays {pays}, catégories : {categories}")
```

**Aplatir et exporter** vers CSV :

```python
import csv
lignes = [{"ip": "203.0.113.45", "score": 87}, {"ip": "198.51.100.7", "score": 12}]
with open("reputation.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["ip", "score"])
    w.writeheader()
    w.writerows(lignes)
```

**Gestion d'erreurs de format** : une réponse n'est pas toujours du JSON valide (page d'erreur HTML d'un proxy, par exemple).

```python
try:
    donnees = r.json()
except ValueError:
    print("Réponse non JSON :", r.text[:200])
    donnees = None
```

### 8. Concevoir un client d'API réutilisable

Regrouper la configuration et la logique dans une **classe** évite de répéter les mêmes réglages :

```python
import os
import time
import requests

class ClientAPI:
    def __init__(self, base_url, cle=None, delai=1.0):
        self.base_url = base_url.rstrip("/")
        self.delai = delai
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ECHATS-Formation/1.0",
            "Accept": "application/json",
        })
        if cle:
            self.session.headers["Authorization"] = f"Bearer {cle}"
        self._dernier = 0.0

    def _attendre(self):
        ecart = time.time() - self._dernier
        if ecart < self.delai:
            time.sleep(self.delai - ecart)
        self._dernier = time.time()

    def get(self, chemin, **params):
        self._attendre()
        r = self.session.get(f"{self.base_url}/{chemin.lstrip('/')}",
                             params=params, timeout=10)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", "5")))
            return self.get(chemin, **params)
        r.raise_for_status()
        return r.json()

# Utilisation
client = ClientAPI("https://jsonplaceholder.typicode.com", delai=0.5)
print(client.get("posts/1")["title"])
```

Cette classe centralise l'authentification, le délai minimum entre requêtes, la gestion de `429` et le `timeout`.

### 9. Mise en cache : économiser les quotas

Une même information demandée dix fois consomme dix requêtes. On peut garder les réponses en mémoire :

```python
from functools import lru_cache

@lru_cache(maxsize=1024)
def reputation(ip):
    return client.get(f"ip/{ip}")
```

Pour un cache persistant, enregistre les réponses dans un fichier JSON avec une date, et ne réinterroge qu'au-delà d'un certain âge. Respecte les règles de mise en cache de l'éditeur de l'API.

### 10. Cas d'usage en cybersécurité

| Besoin | Type d'API | Exemple d'usage |
|---|---|---|
| Vulnérabilités connues | Bases CVE (NVD du NIST, CVE.org, CISA KEV) | Vérifier si une version logicielle est concernée |
| Réputation d'adresse IP / domaine | Services de renseignement sur les menaces | Enrichir une alerte de journal |
| Fuite de données | Services de notification de compromission | Vérifier si une adresse e-mail apparaît dans une fuite connue, de façon privée |
| Surface d'attaque | Moteurs de recherche d'appareils connectés | Inventorier ce que **ton organisation** expose |
| Vérification de fichier | Services d'analyse d'empreintes | Rechercher le hash d'un fichier suspect |
| Supervision interne | API de SIEM, de pare-feu, de cloud | Automatiser des rapports et des réponses |

Quelques principes de prudence :
- **Ne transmets pas de données sensibles** (contenu de fichiers confidentiels, informations clients) à un service tiers sans vérifier ses conditions : tu peux **divulguer** ce que tu cherchais à protéger.
- Préfère envoyer une **empreinte (hash)** plutôt que le fichier lui-même.
- Vérifie que ton usage est conforme à la licence (certaines API gratuites interdisent un usage commercial).

### 11. Sécurité côté API : ce que tu dois savoir

Quand tu consommes des API, tu apprends aussi comment on les **attaque**, pour mieux les défendre. Le référentiel **OWASP API Security Top 10** recense les risques majeurs, parmi lesquels :

- **autorisation défaillante au niveau de l'objet** (BOLA/IDOR) : changer un identifiant (`/commandes/101` → `/commandes/102`) donne accès aux données d'un autre utilisateur ;
- **authentification faible** : clés prévisibles, jetons sans expiration ;
- **exposition excessive de données** : l'API renvoie plus de champs que nécessaire ;
- **absence de limitation de débit** : permet le déni de service et le forçage ;
- **mauvaise configuration** : messages d'erreur trop bavards, CORS permissif ;
- **consommation non sécurisée d'API tierces** : faire confiance sans vérifier aux données reçues d'un partenaire.

Ces thèmes seront approfondis dans le module Sécurité Web. Retiens dès maintenant : **toute donnée reçue d'une API est une entrée non fiable** et doit être validée avant usage.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : utilise des API publiques de test (`jsonplaceholder.typicode.com`, `httpbin.org`) ou des API pour lesquelles **tu disposes d'une clé personnelle** et dont tu respectes les conditions. N'essaie jamais d'accéder à des ressources qui ne sont pas les tiennes en modifiant des identifiants, et ne lance aucun test de sécurité sur l'API d'un tiers sans autorisation écrite.

### Exercice 1 — Premiers appels

1. `GET https://jsonplaceholder.typicode.com/users` : affiche le nom et l'e-mail de chaque utilisateur (données fictives).
2. `GET /users/3` : affiche la ville de l'utilisateur 3 (`address.city`).
3. Que se passe-t-il pour `/users/9999` ? Note le code retourné et gère l'erreur proprement.

```python
import requests
BASE = "https://jsonplaceholder.typicode.com"

for u in requests.get(f"{BASE}/users", timeout=10).json():
    print(f"{u['name']:25s} {u['email']}")

r = requests.get(f"{BASE}/users/9999", timeout=10)
print(r.status_code)     # 404
```

### Exercice 2 — Filtrer et agréger

À partir de `/posts` (100 articles) et `/users`, construis un dictionnaire `{nom_utilisateur: nombre_d_articles}` et affiche le classement. Indice : associe `userId` à `id`.

### Exercice 3 — Pagination

JSONPlaceholder accepte `_page` et `_limit`. Écris un générateur qui récupère `/comments` par pages de 50 (`?_page=1&_limit=50`) jusqu'à épuisement, avec un maximum de 5 pages. Affiche le nombre total de commentaires récupérés.

### Exercice 4 — Client réutilisable

Reprends la classe `ClientAPI` de la section 8, ajoute :
1. une méthode `post(chemin, json)` ;
2. un compteur de requêtes envoyées ;
3. des journaux avec le module `logging` (méthode, URL, code, durée) **sans afficher** les en-têtes sensibles.

Teste-la sur JSONPlaceholder (GET et POST).

### Exercice 5 — Clés et variables d'environnement

1. Crée un fichier `.env` contenant `MON_API_KEY=cle_de_test_123`.
2. Ajoute `.env` à `.gitignore`.
3. Charge la variable avec `python-dotenv` et envoie-la en en-tête à `https://httpbin.org/headers`.
4. Vérifie dans la réponse que l'en-tête est bien transmis. Pourquoi ne faut-il **jamais** afficher cette valeur dans les journaux ?

### Exercice 6 — API de vulnérabilités (avec précaution)

Interroge l'API publique d'un catalogue de vulnérabilités **dont tu as lu les conditions** (par exemple la base nationale NVD du NIST, ou le catalogue CISA KEV publié en JSON). Pour t'entraîner :
1. télécharge le catalogue ;
2. compte le nombre d'entrées ;
3. filtre celles qui concernent un produit que tu utilises ;
4. exporte-les en CSV (CVE, produit, date d'ajout).

Remarque : vérifie la documentation actuelle de l'API (URL, paramètres, quotas), car ces services évoluent. Respecte les limites de débit.

### Exercice 7 — Rapport d'enrichissement

Écris un programme qui lit un fichier `ips.txt` (adresses **fictives** ou issues de tes propres journaux), interroge un service de réputation dont tu as une clé personnelle, **met en cache** les résultats dans un fichier JSON, et produit un CSV `ip, score, categories`. Gère les erreurs `401`, `404` et `429`.

Si tu n'as pas de clé : simule le service avec un petit serveur local (par exemple `http.server` ou Flask) qui renvoie des scores fictifs, pour t'entraîner à la logique sans dépendre d'un tiers.

### Exercice 8 — Défi : mini-API locale et son client

1. Crée une mini-API avec **Flask** (`pip install flask`) exposant `GET /machines` et `GET /machines/<id>` avec des données fictives, protégée par une clé d'API en en-tête (refus `401` sinon).
2. Écris un client Python qui l'interroge.
3. Teste : sans clé → 401 ; avec la mauvaise clé → 401 ; avec la bonne → 200 ; id inexistant → 404.

```python
from flask import Flask, jsonify, request, abort
app = Flask(__name__)
CLE = "cle-de-labo"
MACHINES = {1: {"nom": "web-01"}, 2: {"nom": "db-01"}}

@app.before_request
def verifier_cle():
    if request.headers.get("X-API-Key") != CLE:
        abort(401)

@app.get("/machines")
def lister():
    return jsonify(MACHINES)

@app.get("/machines/<int:mid>")
def lire(mid):
    if mid not in MACHINES:
        abort(404)
    return jsonify(MACHINES[mid])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
```

Lance-la seulement sur `127.0.0.1` (ta machine). C'est la préparation du module Sécurité Web, où tu apprendras à repérer et corriger les failles d'une API.

## 🔍 Approfondissement

### Pour aller plus loin

- Documentation de `requests` et de `httpx` ; spécification OpenAPI (swagger.io).
- **OWASP API Security Top 10** (owasp.org).
- Postman ou Bruno : outils graphiques pour explorer des API avant de coder.
- Le module « API » de TryHackMe et les défis API de plateformes de CTF.

### Pièges courants

- ❌ **Erreur fréquente 1** : écrire la clé d'API dans le code et publier le dépôt.
- ✅ **Bonne pratique** : variables d'environnement, `.env` hors dépôt, rotation des clés.
- ❌ **Erreur fréquente 2** : supposer qu'un champ JSON existe toujours (`KeyError`, `TypeError` sur `None`).
- ✅ **Bonne pratique** : `.get()`, valeurs par défaut, validation des données.
- ❌ **Erreur fréquente 3** : ignorer la pagination et croire avoir récupéré tous les résultats.
- ✅ **Bonne pratique** : lire la doc, parcourir toutes les pages avec une limite de sécurité.
- ❌ **Erreur fréquente 4** : marteler l'API et se faire bloquer.
- ✅ **Bonne pratique** : pauses, backoff, cache, respect de `Retry-After`.
- ❌ **Erreur fréquente 5** : envoyer des données confidentielles à un service tiers « pour vérifier ».
- ✅ **Bonne pratique** : envoyer des empreintes, lire les conditions du service, minimiser les données.

## 🧪 Quiz de validation

**Question 1 : Quelle méthode HTTP est utilisée pour lire une ressource dans une API REST ?**
- A) POST
- B) DELETE
- C) GET ✅
- D) PUT

*Explication : `GET` récupère une ressource sans la modifier ; POST crée, PUT/PATCH modifient, DELETE supprime.*

**Question 2 : Où faut-il stocker une clé d'API ?**
- A) En clair dans le code source
- B) Dans une variable d'environnement ou un fichier de secrets exclu du dépôt ✅
- C) Dans un commentaire HTML
- D) Dans le nom du fichier

*Explication : une clé dans le code peut fuiter avec le dépôt ; les variables d'environnement et fichiers `.env` ignorés par Git limitent ce risque.*

**Question 3 : Que signifie le code HTTP 429 ?**
- A) Ressource introuvable
- B) Erreur interne du serveur
- C) Trop de requêtes, le quota est dépassé ✅
- D) Authentification réussie

*Explication : il faut ralentir et respecter l'en-tête `Retry-After` quand il est présent.*

**Question 4 : Pourquoi la pagination est-elle nécessaire ?**
- A) Pour chiffrer les réponses
- B) Parce que l'API ne renvoie pas tous les résultats d'un coup, mais par morceaux ✅
- C) Pour changer le format JSON
- D) Pour supprimer les doublons

*Explication : sans parcourir les pages suivantes, on ne récupère qu'une partie des données.*

**Question 5 : Quel risque OWASP API correspond au fait de changer `/commandes/101` en `/commandes/102` pour voir la commande d'un autre utilisateur ?**
- A) Un déni de service
- B) Une autorisation défaillante au niveau de l'objet (BOLA / IDOR) ✅
- C) Une injection SQL
- D) Un défaut de chiffrement TLS

*Explication : l'API ne vérifie pas que l'utilisateur a le droit d'accéder à cet objet précis.*

## 📝 Résumé

- Une API REST expose des ressources par URL, manipulées avec les méthodes HTTP, et renvoie le plus souvent du JSON avec des codes d'état explicites.
- Lire la documentation (points d'accès, authentification, quotas, conditions) précède tout code.
- L'authentification par clé, jeton Bearer, Basic ou OAuth exige une gestion rigoureuse des secrets.
- La pagination, la limitation de débit, le cache et les nouvelles tentatives font un client robuste et poli.
- Les réponses JSON sont des entrées non fiables : accès prudent aux champs et validation.
- Les API sont au cœur de l'enrichissement d'alertes, de la veille sur les vulnérabilités et de l'automatisation, tout en étant elles-mêmes une cible (OWASP API Top 10).

## 🎓 Ce que tu as appris

✅ Interroger une API REST avec authentification et pagination
✅ Gérer quotas, erreurs et mise en cache
✅ Protéger tes clés et tes données
✅ Construire un client réutilisable et une mini-API de laboratoire

## ➡️ Leçon suivante

**09 : Introduction à l'OSINT** : définition, cycle du renseignement, sources ouvertes, cadre légal et éthique, premiers outils et méthodologie. Fichier : `09-osint-introduction.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
