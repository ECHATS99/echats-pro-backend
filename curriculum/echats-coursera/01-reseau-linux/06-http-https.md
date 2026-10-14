---
title: "HTTP et HTTPS : le langage du web"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 35
order: 6
category: "reseau"
tags: ["reseau", "http", "https", "tls", "cookies", "curl", "headers"]
prerequisites: ["03-tcp-ip", "05-dns"]
learning_objectives:
  - "Décrire le cycle requête/réponse HTTP"
  - "Lire une requête, une réponse, les méthodes et les codes d'état"
  - "Expliquer le rôle des cookies et des en-têtes de sécurité"
  - "Comprendre ce que HTTPS protège et ce qu'il ne protège pas"
author: "ECHATS PRO"
language: "fr"
published: true
---

# HTTP et HTTPS : le langage du web

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Décrire le cycle requête/réponse HTTP
- Lire une requête, une réponse, les méthodes et les codes d'état
- Expliquer le rôle des cookies et des en-têtes de sécurité
- Comprendre ce que HTTPS protège et ce qu'il ne protège pas

## 📚 Prérequis

- Leçon 03 : *TCP/IP*
- Leçon 05 : *DNS*

## 🧭 Introduction

Chaque fois que tu ouvres un site, consultes ton compte Mobile Money en ligne ou utilises une application qui se connecte à un serveur, tu parles **HTTP**. C'est le protocole de la couche application qui définit comment un client (navigateur, application mobile) demande une ressource à un serveur, et comment ce serveur répond.

Il a été conçu au début des années 1990 pour échanger des pages de texte. Il transporte aujourd'hui des vidéos, des paiements, des API entre applications. Il a été conçu **sans sécurité** : à l'origine, tout circulait en clair. D'où **HTTPS**, qui ajoute le chiffrement via TLS.

Pour un futur professionnel de la cybersécurité, HTTP est incontournable : la majorité des vulnérabilités que tu étudieras (injections SQL, XSS, CSRF, IDOR…) passent par des requêtes HTTP. Savoir en lire une brute, avec ses en-têtes et ses paramètres, est la base de l'analyse d'applications web.

## 📖 Concepts clés

### 1. Le modèle requête / réponse

HTTP est un protocole **client-serveur** simple : le client envoie une **requête**, le serveur renvoie une **réponse**. Chaque échange est indépendant : HTTP est **sans état** (*stateless*), le serveur ne se souvient pas de la requête précédente. C'est pour cette raison qu'existent les **cookies** (voir plus bas).

Par défaut, HTTP utilise **TCP, port 80** ; HTTPS utilise **TCP, port 443**.

### 2. Anatomie d'une URL

```
https://www.exemple.cg:443/boutique/produit?id=42&couleur=bleu#avis
\___/   \____________/\__/\______________/\______________/\___/
schéma      hôte      port     chemin        paramètres   ancre
```

- **Schéma** : protocole (`http`, `https`).
- **Hôte** : nom de domaine ou adresse IP.
- **Chemin** : la ressource demandée.
- **Paramètres (query string)** : données envoyées après le `?`, séparées par `&`. Ce sont des points d'entrée classiques pour les attaques.
- **Ancre** : partie traitée uniquement par le navigateur, jamais envoyée au serveur.

### 3. Une requête HTTP

```http
GET /boutique/produit?id=42 HTTP/1.1
Host: www.exemple.cg
User-Agent: Mozilla/5.0 (Linux; Android 13)
Accept: text/html
Accept-Language: fr-FR
Cookie: session=abc123xyz
```

Trois parties :
1. **Ligne de requête** : méthode, chemin, version.
2. **En-têtes** (*headers*) : métadonnées (hôte, navigateur, langues, cookies…).
3. **Corps** (*body*), facultatif : les données envoyées (par exemple un formulaire).

### 4. Les méthodes HTTP

| Méthode | Usage | Corps ? |
|---|---|---|
| GET | Lire une ressource | Non |
| POST | Envoyer des données (formulaire, création) | Oui |
| PUT | Remplacer une ressource | Oui |
| PATCH | Modifier partiellement | Oui |
| DELETE | Supprimer | Non |
| HEAD | Comme GET, sans le corps (en-têtes seuls) | Non |
| OPTIONS | Demander les méthodes autorisées | Non |

**Sécurité** : une donnée sensible (mot de passe, jeton) ne doit **jamais** passer dans l'URL d'un GET, car les URL sont conservées dans l'historique, les journaux de serveur et les en-têtes `Referer`. On utilise POST avec HTTPS.

### 5. Une réponse HTTP

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 1523
Set-Cookie: session=abc123xyz; HttpOnly; Secure
Server: nginx

<!DOCTYPE html>
<html> ... </html>
```

Elle contient une **ligne de statut**, des **en-têtes**, puis le **corps** (la page, l'image, du JSON…).

### 6. Les codes d'état

| Famille | Sens | Exemples |
|---|---|---|
| 1xx | Information | 101 Switching Protocols |
| 2xx | Succès | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved Permanently, 302 Found |
| 4xx | Erreur côté client | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| 5xx | Erreur côté serveur | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

Distinction utile : **401** = tu n'es pas authentifié ; **403** = tu es identifié mais tu n'as pas le droit. Les codes 5xx qui apparaissent après l'envoi d'une entrée étrange peuvent révéler un défaut de traitement côté serveur : c'est un indice classique en test d'intrusion.

### 7. Les cookies et les sessions

Comme HTTP n'a pas de mémoire, le serveur donne au client un **cookie** (via l'en-tête `Set-Cookie`) que le navigateur renvoie à chaque requête suivante. Après connexion, le serveur associe un **identifiant de session** à ton compte. Ce cookie fait office de « badge » : qui le possède est reconnu comme toi. Voler un cookie de session, c'est donc voler ta connexion (*session hijacking*).

Attributs importants :

| Attribut | Rôle |
|---|---|
| `Secure` | Le cookie n'est envoyé qu'en HTTPS |
| `HttpOnly` | Le cookie est inaccessible au JavaScript (protège contre le vol par XSS) |
| `SameSite` | Limite l'envoi du cookie dans les requêtes issues d'autres sites (protège contre le CSRF) |
| `Expires` / `Max-Age` | Durée de vie |

### 8. En-têtes de sécurité

Un serveur bien configuré envoie des en-têtes qui durcissent le comportement du navigateur :

| En-tête | Effet |
|---|---|
| `Strict-Transport-Security` (HSTS) | Force l'usage de HTTPS pour ce site |
| `Content-Security-Policy` | Limite les sources de scripts et de ressources (réduit l'impact du XSS) |
| `X-Content-Type-Options: nosniff` | Empêche le navigateur de deviner le type d'un fichier |
| `X-Frame-Options` / `frame-ancestors` | Empêche l'intégration du site dans un cadre (clickjacking) |
| `Referrer-Policy` | Contrôle les informations envoyées dans `Referer` |

L'absence de ces en-têtes n'est pas une faille en soi, mais un signe de configuration perfectible, que tu signaleras dans un rapport d'audit.

### 9. HTTPS et TLS

**HTTPS = HTTP + TLS** (*Transport Layer Security*, successeur de SSL). TLS apporte trois garanties :

1. **Confidentialité** : les données sont chiffrées, un intermédiaire (Wi-Fi public, opérateur) ne peut pas les lire.
2. **Intégrité** : toute modification en route est détectée.
3. **Authentification** : un **certificat** prouve que tu parles bien au vrai serveur du domaine, grâce à une autorité de certification (AC) de confiance.

Principe simplifié de la poignée de main TLS :
1. Le client annonce les versions et suites de chiffrement qu'il supporte.
2. Le serveur présente son **certificat**.
3. Le client vérifie le certificat (signature, domaine, date de validité).
4. Client et serveur établissent une **clé de session** partagée.
5. Tout le reste de l'échange est chiffré avec cette clé.

Nous détaillerons TLS et les certificats dans le module Cryptographie.

**Ce que HTTPS ne fait PAS :**
- il ne rend pas un site **honnête** : un site de phishing peut avoir un cadenas ;
- il ne protège pas contre les failles de l'application (injection SQL, XSS fonctionnent aussi en HTTPS) ;
- il ne cache pas **à quel domaine** tu te connectes (le nom du serveur reste en général visible via DNS et SNI) ;
- il ne protège pas un poste déjà infecté.

### 10. Versions de HTTP

- **HTTP/1.1** : texte, une requête à la fois par connexion (ou en pipeline limité).
- **HTTP/2** : binaire, plusieurs requêtes en parallèle sur une connexion.
- **HTTP/3** : fonctionne au-dessus de QUIC (UDP), plus rapide à établir.

Les principes (méthodes, codes, en-têtes) restent les mêmes.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : envoie des requêtes uniquement vers des sites publics en lecture simple, ou vers **tes propres serveurs**. Ne teste jamais de paramètres piégés ou de forçage de mots de passe sur un site tiers sans autorisation écrite.

### Exercice 1 — Voir une requête avec curl

```bash
curl -v http://example.com
```

Dans la sortie, les lignes commençant par `>` sont ta requête, celles commençant par `<` sont la réponse. Repère :
1. la méthode et le chemin ;
2. le code d'état ;
3. les en-têtes de réponse (`Content-Type`, `Server`…).

### Exercice 2 — Récupérer seulement les en-têtes

```bash
curl -I https://example.com
```

(`-I` envoie une requête HEAD.) Cherche la présence d'en-têtes de sécurité comme `Strict-Transport-Security`. Teste avec quelques sites publics et compare.

### Exercice 3 — Observer une redirection

```bash
curl -I http://github.com
curl -IL http://github.com
```

La première commande montre un code 301 et l'en-tête `Location`. Avec `-L`, curl suit la redirection vers HTTPS. Tu vois comment un site force le passage au chiffrement.

### Exercice 4 — Les outils du navigateur

1. Ouvre un site, appuie sur **F12**, onglet **Réseau** (*Network*).
2. Recharge la page.
3. Clique sur la première requête : observe les en-têtes de requête et de réponse, le code d'état, la taille.
4. Onglet **Application / Stockage** : regarde les cookies du site et leurs attributs (`Secure`, `HttpOnly`, `SameSite`).

### Exercice 5 — Inspecter un certificat

Clique sur le cadenas dans la barre d'adresse, puis « Certificat » : repère l'émetteur, le nom du domaine couvert, les dates de validité. Que se passerait-il si la date était dépassée ? (Le navigateur afficherait un avertissement.)

### Exercice 6 — Comparer HTTP et HTTPS dans Wireshark

Sur **ta propre machine**, capture un `curl http://example.com` : tu peux lire la requête en clair. Capture ensuite `curl https://example.com` : le contenu n'est plus lisible, seule la poignée de main TLS apparaît. C'est la démonstration directe de l'apport du chiffrement.

## 🔍 Approfondissement

### Pour aller plus loin

- MDN Web Docs : section « HTTP » (en français), la référence pour les en-têtes et les méthodes.
- Le site securityheaders.com pour tester les en-têtes de **ton propre site**.
- Module « Web Fundamentals » de TryHackMe.

### Pièges courants

- ❌ **Erreur fréquente 1** : croire que le cadenas signifie « site sûr ». Il signifie seulement « connexion chiffrée vers ce domaine ».
- ✅ **Bonne pratique** : vérifier l'adresse exacte du domaine avant de saisir un mot de passe.
- ❌ **Erreur fréquente 2** : mettre des informations sensibles dans l'URL.
- ✅ **Bonne pratique** : POST pour les données sensibles, et jamais d'identifiants dans les paramètres d'URL.
- ❌ **Erreur fréquente 3** : oublier `Secure` et `HttpOnly` sur les cookies de session.
- ✅ **Bonne pratique** : activer systématiquement `Secure`, `HttpOnly` et `SameSite`.
- ❌ **Erreur fréquente 4** : confondre 401 et 403.
- ✅ **Bonne pratique** : 401 = non authentifié, 403 = authentifié mais non autorisé.

## 🧪 Quiz de validation

**Question 1 : Quel port utilise HTTPS par défaut ?**
- A) 80
- B) 22
- C) 443 ✅
- D) 8080

*Explication : HTTP utilise 80, HTTPS 443.*

**Question 2 : Que signifie qu'HTTP est « sans état » ?**
- A) Il ne fonctionne pas sur Internet
- B) Le serveur ne garde pas en mémoire les requêtes précédentes d'un client ✅
- C) Il ne peut pas envoyer de données
- D) Il est toujours chiffré

*Explication : chaque requête est indépendante ; les cookies servent à maintenir une session.*

**Question 3 : Que signifie le code 404 ?**
- A) Erreur interne du serveur
- B) Accès interdit
- C) Ressource introuvable ✅
- D) Redirection permanente

*Explication : 404 Not Found indique que la ressource demandée n'existe pas à cette adresse.*

**Question 4 : Quel attribut empêche le JavaScript de lire un cookie ?**
- A) Secure
- B) HttpOnly ✅
- C) SameSite
- D) Max-Age

*Explication : `HttpOnly` réduit les conséquences d'une faille XSS en protégeant les cookies de session.*

**Question 5 : Que garantit TLS ?**
- A) Que le site est honnête
- B) Confidentialité, intégrité et authentification du serveur ✅
- C) L'absence de failles dans l'application
- D) L'anonymat de l'utilisateur

*Explication : TLS protège la connexion, pas le comportement du site ni les failles de l'application.*

## 📝 Résumé

- HTTP est un protocole requête/réponse sans état, sur TCP (ports 80 et 443).
- Une requête contient méthode, chemin, en-têtes et éventuellement un corps ; la réponse contient un code d'état, des en-têtes et un corps.
- Les cookies maintiennent les sessions ; leurs attributs (`Secure`, `HttpOnly`, `SameSite`) sont cruciaux.
- Les en-têtes de sécurité (HSTS, CSP…) durcissent les navigateurs.
- HTTPS = HTTP + TLS : chiffrement, intégrité, authentification du serveur, mais ni garantie d'honnêteté ni protection contre les failles applicatives.

## 🎓 Ce que tu as appris

✅ Lire et interpréter requêtes, réponses et codes d'état
✅ Comprendre le rôle des cookies et des en-têtes de sécurité
✅ Expliquer ce que HTTPS apporte et ses limites
✅ Utiliser `curl` et les outils du navigateur pour observer le trafic

## ➡️ Leçon suivante

**07 : Le routage** : comment les paquets trouvent leur chemin entre réseaux, tables de routage, routes statiques et dynamiques. Fichier : `07-routage.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
