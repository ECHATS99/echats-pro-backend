---
title: "Requêtes HTTP en Python"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 6
category: "python"
tags: ["python", "requests", "http", "headers", "cookies", "session", "timeout", "tls"]
prerequisites: ["06-http-https", "04-fonctions-modules", "05-fichiers-io"]
learning_objectives:
  - "Envoyer des requêtes GET et POST avec la bibliothèque requests"
  - "Lire codes d'état, en-têtes, cookies et corps des réponses"
  - "Gérer sessions, délais d'attente, erreurs et tentatives"
  - "Écrire un petit vérificateur d'en-têtes de sécurité sur ses propres sites"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Requêtes HTTP en Python

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Envoyer des requêtes GET et POST avec la bibliothèque `requests`
- Lire codes d'état, en-têtes, cookies et corps des réponses
- Gérer sessions, délais d'attente, erreurs et tentatives
- Écrire un petit vérificateur d'en-têtes de sécurité sur tes propres sites

## 📚 Prérequis

- Leçon 06 du module Réseau & Linux : *HTTP et HTTPS* (méthodes, codes d'état, en-têtes, cookies)
- Leçons 04 et 05 de ce module (fonctions, erreurs, fichiers, JSON)

## 🧭 Introduction

Dans la leçon HTTP du premier module, tu as utilisé `curl` et les outils du navigateur pour observer des requêtes. Maintenant, tu vas les **programmer**. Avec Python, tu peux interroger des centaines de pages ou d'API, enregistrer les résultats, tester l'état d'un service, vérifier la configuration de tes propres sites.

La bibliothèque **`requests`** est la référence : simple, lisible, très répandue. Elle est utilisée aussi bien par des développeurs web que par des analystes OSINT (collecte d'informations publiques), des équipes de supervision (vérification de disponibilité) et des testeurs d'intrusion (automatisation de tests autorisés).

C'est donc un outil à double tranchant : le même script qui vérifie la santé de ton site peut, mal utilisé, surcharger celui d'un tiers ou collecter des données sans droit. Tout au long de cette leçon, tu apprendras à écrire des clients **polis, robustes et légaux** : délais d'attente, limitation de débit, respect des conditions d'utilisation, identification claire.

## 📖 Concepts clés

### 1. Installer et premier appel

```bash
python3 -m venv env && source env/bin/activate
pip install requests
```

```python
import requests

reponse = requests.get("https://example.com", timeout=10)
print(reponse.status_code)      # 200
print(reponse.headers["Content-Type"])
print(reponse.text[:200])       # début du corps (texte)
```

**Toujours mettre un `timeout`** : sans cela, `requests` peut attendre indéfiniment une réponse qui ne vient pas, et ton programme reste bloqué.

### 2. L'objet Response

| Attribut / méthode | Contenu |
|---|---|
| `r.status_code` | Code HTTP (200, 404…) |
| `r.ok` | `True` si le code est < 400 |
| `r.headers` | En-têtes de réponse (dictionnaire insensible à la casse) |
| `r.text` | Corps décodé en texte |
| `r.content` | Corps en octets (images, fichiers) |
| `r.json()` | Corps interprété comme JSON |
| `r.cookies` | Cookies reçus |
| `r.url` | URL finale (après redirections) |
| `r.history` | Liste des redirections suivies |
| `r.elapsed` | Durée de la requête |
| `r.encoding` | Encodage détecté |
| `r.raise_for_status()` | Lève une exception si le code est 4xx ou 5xx |

```python
r = requests.get("http://github.com", timeout=10)
print(r.url)                  # https://github.com/ (redirigé)
print([h.status_code for h in r.history])   # [301]
```

### 3. Paramètres d'URL et en-têtes

**Paramètres de requête (query string)** : laisse `requests` les encoder.

```python
params = {"q": "cybersécurité", "page": 2}
r = requests.get("https://httpbin.org/get", params=params, timeout=10)
print(r.url)        # https://httpbin.org/get?q=cybers%C3%A9curit%C3%A9&page=2
print(r.json()["args"])
```

(httpbin.org est un service public conçu pour tester les clients HTTP.)

**En-têtes personnalisés :**

```python
entetes = {
    "User-Agent": "ECHATS-Formation/1.0 (contact: ton-email@exemple.cg)",
    "Accept": "application/json",
}
r = requests.get("https://httpbin.org/headers", headers=entetes, timeout=10)
print(r.json())
```

**Bonne pratique d'éthique** : identifie-toi avec un `User-Agent` clair qui permet de te contacter. Se faire passer pour un navigateur ordinaire pour contourner une règle d'un site peut violer ses conditions d'utilisation.

### 4. Envoyer des données : POST, PUT, DELETE

```python
# Formulaire classique (application/x-www-form-urlencoded)
r = requests.post("https://httpbin.org/post",
                  data={"utilisateur": "demo", "message": "bonjour"}, timeout=10)
print(r.json()["form"])

# Corps JSON (Content-Type: application/json ajouté automatiquement)
r = requests.post("https://httpbin.org/post",
                  json={"nom": "web-01", "ports": [22, 443]}, timeout=10)
print(r.json()["json"])

# Autres méthodes
requests.put("https://httpbin.org/put", json={"a": 1}, timeout=10)
requests.delete("https://httpbin.org/delete", timeout=10)
requests.head("https://example.com", timeout=10)        # en-têtes seulement
```

**Envoyer un fichier :**

```python
with open("rapport.txt", "rb") as f:
    r = requests.post("https://httpbin.org/post", files={"fichier": f}, timeout=30)
```

### 5. Cookies et sessions

Un **objet `Session`** conserve les cookies entre les requêtes et réutilise la connexion (plus rapide). C'est la bonne façon de simuler une navigation avec authentification.

```python
s = requests.Session()
s.headers.update({"User-Agent": "ECHATS-Formation/1.0"})

s.get("https://httpbin.org/cookies/set/session_id/abc123", timeout=10)
r = s.get("https://httpbin.org/cookies", timeout=10)
print(r.json())          # {'cookies': {'session_id': 'abc123'}}
```

Ne mets **jamais** de vrais identifiants dans ton code source. Utilise des variables d'environnement :

```python
import os
token = os.environ.get("API_TOKEN")
if not token:
    raise SystemExit("Variable API_TOKEN absente")
s.headers["Authorization"] = f"Bearer {token}"
```

### 6. Gérer les erreurs

Les requêtes réseau échouent souvent : DNS introuvable, serveur éteint, délai dépassé, certificat invalide. Les exceptions de `requests` héritent de `requests.exceptions.RequestException`.

```python
import requests

def telecharger(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r
    except requests.exceptions.Timeout:
        print("Délai dépassé :", url)
    except requests.exceptions.SSLError:
        print("Erreur de certificat TLS :", url)
    except requests.exceptions.ConnectionError:
        print("Connexion impossible :", url)
    except requests.exceptions.HTTPError as e:
        print("Erreur HTTP :", e.response.status_code, url)
    except requests.exceptions.RequestException as e:
        print("Erreur inattendue :", e)
    return None
```

### 7. TLS : ne jamais désactiver la vérification

Par défaut, `requests` **vérifie le certificat** du serveur HTTPS. Tu verras sur Internet des conseils comme `verify=False` pour « faire disparaître l'erreur ». **C'est dangereux** : cela supprime la protection contre l'interception (homme du milieu).

```python
# À ÉVITER, sauf sur un laboratoire isolé avec un certificat auto-signé que tu maîtrises :
# requests.get(url, verify=False)

# Préférable : fournir le certificat de l'autorité de confiance
requests.get("https://mon-serveur-interne.local", verify="/chemin/ca-interne.pem", timeout=10)
```

Si une erreur de certificat apparaît, **comprends pourquoi** (certificat expiré, nom incorrect, autorité inconnue) avant de la contourner.

### 8. Redirections, flux et gros fichiers

```python
# Contrôler les redirections
r = requests.get("http://github.com", allow_redirects=False, timeout=10)
print(r.status_code, r.headers.get("Location"))

# Télécharger un gros fichier par blocs (sans tout charger en mémoire)
with requests.get("https://example.com/gros.zip", stream=True, timeout=30) as r:
    r.raise_for_status()
    with open("gros.zip", "wb") as f:
        for bloc in r.iter_content(chunk_size=8192):
            f.write(bloc)
```

Limite la taille téléchargée pour des sources inconnues (vérifie `Content-Length`, ou arrête après un maximum d'octets).

### 9. Nouvelles tentatives et limitation de débit

Un serveur peut répondre `429 Too Many Requests` (trop de requêtes) ou `503`. Un client bien élevé :
- **ralentit** entre les requêtes (`time.sleep`) ;
- **réessaie avec un délai croissant** (*backoff exponentiel*) ;
- respecte l'en-tête `Retry-After` quand il existe.

```python
import time
import requests

def get_poli(url, tentatives=3, pause=1.0):
    for essai in range(1, tentatives + 1):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 429:
                attente = int(r.headers.get("Retry-After", pause * 2 ** essai))
                time.sleep(attente)
                continue
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException:
            if essai == tentatives:
                raise
            time.sleep(pause * 2 ** essai)
    return None
```

`requests` peut aussi s'appuyer sur `urllib3.util.retry.Retry` via un adaptateur de session pour automatiser cela.

### 10. Exemple utile : vérifier les en-têtes de sécurité de TON site

```python
import requests

ENTETES_ATTENDUS = {
    "Strict-Transport-Security": "Force HTTPS (HSTS)",
    "Content-Security-Policy": "Limite les sources de contenu (réduit le XSS)",
    "X-Content-Type-Options": "Empêche le sniffing de type MIME",
    "X-Frame-Options": "Protège contre le clickjacking",
    "Referrer-Policy": "Contrôle les informations de référent",
}

def verifier(url):
    r = requests.get(url, timeout=10)
    print(f"{url} → {r.status_code}")
    for nom, role in ENTETES_ATTENDUS.items():
        etat = "présent" if nom in r.headers else "ABSENT"
        print(f"  {nom:28s} {etat:8s} ({role})")
    if "Server" in r.headers:
        print(f"  Server : {r.headers['Server']} (divulgue une information sur le serveur)")
    for cookie in r.cookies:
        if not cookie.secure:
            print(f"  Cookie '{cookie.name}' sans attribut Secure")

verifier("https://example.com")
```

Ce script est un **contrôle de configuration** inoffensif : il lit des en-têtes publics, comme le ferait un navigateur. À appliquer à **tes propres sites** ou à ceux pour lesquels tu es mandaté.

### 11. Éthique et légalité du client HTTP automatisé

| Principe | Application |
|---|---|
| **Autorisation** | Tes propres services, ou accord écrit. Pas de tests « pour voir » sur des sites tiers |
| **Conditions d'utilisation** | Lis-les : certains sites interdisent l'automatisation |
| **robots.txt** | Fichier à la racine d'un site qui indique ce que les robots peuvent visiter (voir leçon suivante) |
| **Charge raisonnable** | Une requête à la fois, pauses, pas de parallélisme agressif |
| **Données personnelles** | Collecte minimale ; respect des lois de protection des données |
| **Pas de contournement** | Ne contourne pas un mécanisme d'authentification, un CAPTCHA ou une limite pour obtenir ce qui n'est pas public |
| **Transparence** | User-Agent identifiable avec contact |

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : utilise des cibles prévues pour les tests : `httpbin.org`, `example.com`, `jsonplaceholder.typicode.com`, **ta VM** ou **tes propres sites**. N'envoie jamais de rafales de requêtes à un site tiers, et ne teste jamais de mots de passe ou d'entrées piégées sans autorisation écrite.

### Exercice 1 — Premier contact

```python
import requests
r = requests.get("https://example.com", timeout=10)
print("Code :", r.status_code)
print("Type :", r.headers.get("Content-Type"))
print("Taille :", len(r.content), "octets")
print("Durée :", r.elapsed.total_seconds(), "s")
```

Questions guidées : le code est-il 200 ? À quel format correspond le contenu ? Quelle est la durée de la requête ?

### Exercice 2 — Paramètres et JSON

À l'aide de `https://httpbin.org/get`, envoie les paramètres `ville=Brazzaville` et `lang=fr`. Affiche l'URL finale et le dictionnaire `args` renvoyé. Vérifie que les caractères spéciaux sont correctement encodés.

### Exercice 3 — POST d'un formulaire et d'un JSON

Envoie avec `requests.post` : (1) un formulaire `data={"nom": "Alice"}`, puis (2) un `json={"nom": "Alice", "roles": ["analyste"]}` vers `https://httpbin.org/post`. Compare les clés `form` et `json` de la réponse. Quelle différence de `Content-Type` ? (Observe `r.request.headers`.)

### Exercice 4 — Redirections

1. `requests.get("http://github.com", allow_redirects=False)` : note le code et l'en-tête `Location`.
2. Refais l'appel en suivant les redirections et affiche `r.history`.
3. Explique ce que tu constates sur le passage de HTTP à HTTPS.

### Exercice 5 — Sessions et cookies

Utilise une `Session` pour définir un cookie via `https://httpbin.org/cookies/set/niveau/debutant`, puis lis-le avec `https://httpbin.org/cookies`. Que se passe-t-il si tu fais le second appel avec `requests.get` (sans session) ? (Le cookie est absent.)

### Exercice 6 — Fonction de téléchargement robuste

Écris `telecharger(url, destination)` qui :
1. utilise `stream=True` et un `timeout` ;
2. refuse les fichiers de plus de 5 Mo (contrôle de `Content-Length` et du cumul d'octets) ;
3. écrit dans `destination` ;
4. renvoie l'empreinte SHA-256 du fichier (module `hashlib`) ;
5. gère proprement toutes les erreurs.

### Exercice 7 — Vérificateur d'en-têtes de sécurité

Reprends le script de la section 10. Applique-le :
1. à `https://example.com` ;
2. au site que tu héberges en laboratoire (par exemple ta VM avec nginx) ;
3. génère un petit rapport CSV : `url, entete, present`.

Compare avant et après avoir ajouté des en-têtes dans la configuration de ton serveur.

### Exercice 8 — Surveillance simple de disponibilité

Écris un programme qui interroge une liste de **tes** URL toutes les 60 secondes (3 tours suffisent pour le test), journalise l'heure, le code et la durée dans un fichier, et affiche une alerte si le code est ≥ 500 ou si la durée dépasse 2 secondes. Utilise `time.sleep` entre les tours.

### Exercice 9 — Défi : client poli

Écris une fonction `get_poli()` avec backoff exponentiel qui respecte `Retry-After`, plus un limiteur qui impose au moins 1 seconde entre deux requêtes vers un même domaine. Teste-la avec `https://httpbin.org/status/429` et `https://httpbin.org/status/200`.

## 🔍 Approfondissement

### Pour aller plus loin

- La documentation de `requests` (requests.readthedocs.io) : « Quickstart » et « Advanced Usage ».
- `httpx` : bibliothèque moderne compatible avec l'asynchrone ; `aiohttp` pour la concurrence.
- OWASP *Web Security Testing Guide* pour comprendre ce que les testeurs vérifient (à pratiquer seulement avec autorisation).

### Pièges courants

- ❌ **Erreur fréquente 1** : oublier `timeout`, le programme se fige.
- ✅ **Bonne pratique** : un `timeout` sur chaque appel.
- ❌ **Erreur fréquente 2** : désactiver `verify` pour supprimer une erreur de certificat.
- ✅ **Bonne pratique** : comprendre l'erreur et corriger la cause, ou fournir le bon certificat de confiance.
- ❌ **Erreur fréquente 3** : ne pas vérifier le code de retour et traiter une page d'erreur comme un succès.
- ✅ **Bonne pratique** : `raise_for_status()` ou test explicite de `r.ok`.
- ❌ **Erreur fréquente 4** : mots de passe et jetons écrits dans le code ou dans les journaux.
- ✅ **Bonne pratique** : variables d'environnement, fichiers de secrets protégés, masquage dans les logs.
- ❌ **Erreur fréquente 5** : boucle de requêtes sans pause sur le site d'un tiers.
- ✅ **Bonne pratique** : pauses, backoff, respect des limites et des conditions d'utilisation.

## 🧪 Quiz de validation

**Question 1 : Pourquoi toujours préciser `timeout` dans `requests.get` ?**
- A) Pour chiffrer la requête
- B) Pour éviter que le programme attende indéfiniment une réponse ✅
- C) Pour augmenter la vitesse du serveur
- D) C'est obligatoire pour HTTPS

*Explication : sans délai d'attente, une connexion bloquée peut figer le programme.*

**Question 2 : Quelle méthode lève une exception si le code HTTP est 4xx ou 5xx ?**
- A) `r.json()`
- B) `r.raise_for_status()` ✅
- C) `r.close()`
- D) `r.verify()`

*Explication : `raise_for_status()` transforme les erreurs HTTP en exceptions faciles à gérer.*

**Question 3 : Quel est l'intérêt d'un objet `Session` ?**
- A) Il désactive TLS
- B) Il conserve les cookies et réutilise la connexion entre les requêtes ✅
- C) Il envoie les requêtes en parallèle automatiquement
- D) Il chiffre le code source

*Explication : la session maintient l'état (cookies, en-têtes communs) et améliore les performances.*

**Question 4 : Pourquoi est-il dangereux d'utiliser `verify=False` ?**
- A) Cela ralentit la requête
- B) Cela supprime la vérification du certificat et expose à l'interception ✅
- C) Cela supprime les cookies
- D) Cela change l'adresse IP

*Explication : sans vérification, un attaquant en position d'homme du milieu peut se faire passer pour le serveur.*

**Question 5 : Que doit faire un client poli face à une réponse 429 ?**
- A) Renvoyer immédiatement la requête en boucle
- B) Attendre (en respectant `Retry-After` si présent) puis réessayer avec un délai croissant ✅
- C) Changer d'adresse IP
- D) Ignorer l'erreur

*Explication : 429 signifie « trop de requêtes » ; il faut ralentir, pas insister.*

## 📝 Résumé

- `requests` simplifie GET, POST, PUT, DELETE, avec paramètres, en-têtes, JSON et fichiers.
- L'objet `Response` fournit code, en-têtes, corps, cookies, redirections et durée.
- Un client robuste utilise `timeout`, `raise_for_status()`, gestion d'exceptions, sessions et nouvelles tentatives avec backoff.
- La vérification TLS ne se désactive pas à la légère ; secrets en variables d'environnement.
- Un script de contrôle d'en-têtes de sécurité est un premier outil défensif utile sur tes propres sites.
- Cadre éthique : autorisation, conditions d'utilisation, charge raisonnable, minimisation des données.

## 🎓 Ce que tu as appris

✅ Envoyer et analyser des requêtes HTTP avec Python
✅ Gérer erreurs, délais, sessions et nouvelles tentatives
✅ Contrôler les en-têtes de sécurité d'un site dont tu es responsable
✅ Écrire des clients HTTP polis et respectueux de la loi

## ➡️ Leçon suivante

**07 : Web scraping avec BeautifulSoup** : extraire des informations de pages HTML publiques, dans le respect de `robots.txt` et du droit. Fichier : `07-scraping-beautifulsoup.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
