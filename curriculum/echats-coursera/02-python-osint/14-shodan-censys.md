---
title: "Shodan et Censys : Cartographier ce qui est Exposé sur Internet"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 45
order: 14
category: "osint"
tags: ["shodan", "censys", "osint", "iot", "bannieres", "surface-exposition", "api"]
prerequisites: ["13-maltego", "08-api-rest-python"]
learning_objectives:
  - "Comprendre comment Shodan et Censys indexent les services exposés sur Internet"
  - "Interroger ces moteurs par navigateur et par API pour auditer sa propre exposition"
  - "Reconnaître les risques révélés par des services mal protégés"
  - "Distinguer un usage d'audit légitime d'un usage de reconnaissance offensive non autorisée"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Shodan et Censys : Cartographier ce qui est Exposé sur Internet

> 🔔 **IMPORTANT** — Comptez environ 45 minutes. Un compte gratuit sur Shodan (ou Censys) vous sera utile pour les exercices.

## 🎯 Ce que vous allez apprendre 🌐

Chaque service exposé sur Internet — un serveur web, une caméra connectée, un système de contrôle industriel mal configuré — répond, techniquement, à quiconque l'interroge. **Shodan** et **Censys** sont des moteurs de recherche qui scannent Internet en continu et indexent ces réponses, un peu comme Google indexe des pages web. Le résultat : une base consultable de tout ce qui est visible publiquement sur Internet, souvent bien plus que ce que leurs propriétaires imaginent exposer.

Vous allez :
- comprendre comment ces moteurs construisent leur index, en continu et à l'échelle d'Internet entier,
- apprendre leur syntaxe de recherche pour cibler précisément un type de service ou une organisation,
- auditer ce que votre propre réseau expose publiquement,
- mesurer les risques révélés par des services mal protégés, découverts sans jamais y accéder directement.

> ⚠️ **AVERTISSEMENT** — Consulter les résultats de Shodan ou Censys sur un service appartenant à un tiers est une activité de collecte **passive** : le moteur a déjà fait le scan, vous ne faites qu'interroger son index. Mais se **connecter** à un service ainsi découvert (une caméra, une interface d'administration, une base de données) sans autorisation reste une tentative d'intrusion, exactement comme pour tout accès non autorisé étudié dans ce cours. Consultez ces moteurs sur votre propre infrastructure, ou limitez-vous à observer les résultats sans jamais vous y connecter.

## 📚 Prérequis

- Leçon 13 : *Maltego*
- Leçon 08 : *API REST en Python*

## Comment ces moteurs construisent leur index

### Le scan continu d'Internet

Shodan et Censys parcourent en permanence l'intégralité de l'espace d'adressage IPv4 (voir module Réseau & Linux, leçon 04), en envoyant des sondes vers différents ports, puis en enregistrant la **bannière** renvoyée par chaque service qui répond — ce texte d'identification qu'un serveur envoie généralement au début d'une connexion, révélant son logiciel, sa version, parfois sa configuration.

```
220 ProFTPD 1.3.5 Server ready.
SSH-2.0-OpenSSH_7.4
HTTP/1.1 200 OK
Server: nginx/1.18.0
```

Ce mécanisme rejoint directement le fuzzing et le scan de ports déjà étudiés (module Réseau & Linux, leçon 16 ; module Sécurité Web, leçon 15) — à une différence près et fondamentale : **le scan a déjà été fait**, par le moteur lui-même, à l'échelle de tout Internet, en continu. Consulter Shodan ne déclenche donc aucune nouvelle requête vers la cible ; vous consultez un index déjà constitué, ce qui en fait une méthode purement **passive** au sens de la leçon 13 du module Sécurité Web.

### La syntaxe de recherche

```
org:"Nom d'organisation"          # services appartenant à une organisation identifiée
country:"CG"                       # résultats limités à un pays (code ISO)
port:21                            # un port précis
product:"OpenSSH"                  # un logiciel précis
hostname:"exemple.cg"              # un domaine précis
```

Ces filtres se combinent pour construire des recherches précises :

```
org:"Nom d'organisation" port:3389
```

révèle, par exemple, tous les services de bureau à distance Windows (RDP, port 3389 — module Réseau & Linux, leçon 03) exposés par une organisation donnée, un port rarement justifié d'être accessible publiquement sans restriction.

## Défi : auditer votre propre exposition

### Rechercher votre organisation ou votre adresse IP

Si vous gérez un serveur personnel ou professionnel, recherchez-le directement par son adresse IP publique (que vous pouvez retrouver avec les techniques du module Réseau & Linux, leçon 04) :

```
ip:VOTRE_ADRESSE_IP_PUBLIQUE
```

`![Capture : page de résultats Shodan pour une recherche par adresse IP, affichant les ports ouverts détectés, les bannières de service associées, et la géolocalisation approximative du serveur.](img/02-14-shodan-resultat-ip.png)`

Si vous ne gérez aucun serveur public, observez à la place des résultats généraux pour un type de service, sans cibler d'organisation précise — par exemple `product:"MongoDB"`, qui révèle régulièrement des bases de données exposées sans authentification à travers le monde, un problème de configuration malheureusement très répandu.

> ❓ **DÉFI** — Si vous avez interrogé votre propre adresse IP, combien de ports ouverts Shodan a-t-il détectés, et correspondent-ils tous à des services que vous avez volontairement exposés ?
>
> <details>
> <summary>Voir un exemple de réflexion</summary>
>
> Si chaque port révélé correspond à un service que vous reconnaissez et avez délibérément exposé (un serveur web, par exemple), c'est un bon signe de maîtrise de votre surface d'exposition. Si un port vous surprend — un service que vous pensiez n'avoir jamais ouvert, ou qui devrait être restreint à votre réseau local — c'est exactement le type de découverte qu'un audit régulier avec ce genre d'outil permet de détecter avant qu'un tiers malveillant ne le fasse à votre place, un principe déjà rencontré dans le module Sécurité Web à propos du Google Dorking (leçon 10).
> </details>

### Observer, sans jamais s'y connecter

Pour les résultats généraux que vous avez observés (comme les bases de données exposées), limitez-vous strictement à lire les informations déjà fournies par Shodan dans ses résultats — jamais de tentative de connexion vers ces services, même par simple curiosité. C'est une règle non négociable : le fait qu'un service **réponde** à Internet ne vous donne aucune autorisation à l'utiliser.

> 📝 **NOTE — L'affaire des caméras non sécurisées**
>
> Shodan est régulièrement cité dans des reportages sur les objets connectés mal sécurisés : des caméras de surveillance, des équipements industriels, des appareils médicaux connectés, accessibles sans authentification depuis Internet, parfois avec leurs identifiants laissés par défaut. Ces découvertes ont contribué, au fil des années, à sensibiliser le grand public et les fabricants à l'importance de ne jamais exposer un service sans authentification réelle — une illustration concrète du principe de **moindre exposition**, complément direct du moindre privilège déjà étudié dans le module Réseau & Linux (leçon 11) : un service ne devrait être accessible que depuis là où il est réellement nécessaire, jamais ouvert au monde entier par défaut.

## Interroger par API avec Python

Comme la plupart des services présentés dans ce module, Shodan propose une API officielle, directement exploitable avec les compétences du module Python (leçon 08) :

```python
import shodan

API_KEY = "votre_cle_api"   # jamais en dur dans un script partagé — variable d'environnement, module Python leçon 08
api = shodan.Shodan(API_KEY)

resultats = api.search("product:nginx country:CG")
print(f"{resultats['total']} résultats trouvés")
for resultat in resultats["matches"][:5]:
    print(resultat["ip_str"], resultat["port"], resultat.get("org"))
```

Cette approche permet d'intégrer une veille Shodan régulière sur sa propre organisation dans un script d'audit automatisé, plutôt que de répéter manuellement la même recherche — un prolongement direct des bonnes pratiques de veille déjà évoquées dans le module Sécurité Web (leçon 10, à propos du Google Dorking).

## Shodan, Censys, et la défense

Au-delà de la recherche manuelle, ces outils s'intègrent dans une démarche de sécurité continue :
- **audit périodique** de sa propre surface d'exposition, pour détecter un service ouvert par erreur avant qu'un attaquant ne le trouve ;
- **veille sur un fournisseur** : savoir qu'un partenaire ou un prestataire expose un service mal protégé peut faire partie d'une évaluation de risque fournisseur ;
- **recherche de services vulnérables connus** à grande échelle, utilisée aussi bien par des chercheurs en sécurité pour mesurer l'ampleur d'une vulnérabilité nouvellement découverte, que, historiquement, par des acteurs malveillants — un rappel supplémentaire que ces outils, comme tant d'autres dans ce cours, servent la défense autant que l'attaque selon qui les utilise.

## 🔍 Pour aller plus loin

- La documentation officielle de Shodan et de Censys, notamment leurs guides de syntaxe de recherche avancée.
- Shodan propose un **Shodan Monitor**, un tableau de bord dédié à la surveillance continue de sa propre surface d'exposition.
- Le module Sécurité Web & Pentest, leçon 13, sur la reconnaissance web, pour relier ces outils à une méthodologie de test complète.

## 🧪 Quiz de validation

**Question 1 : Pourquoi consulter Shodan sur l'infrastructure d'un tiers est-il considéré comme une activité passive ?**
- A) Parce que Shodan ne fonctionne que sur ses propres serveurs
- B) Parce que le scan a déjà été réalisé par Shodan lui-même ; consulter ses résultats ne déclenche aucune nouvelle requête vers la cible ✅
- C) Parce que Shodan chiffre toutes ses requêtes
- D) Ce n'est jamais le cas, Shodan est toujours une activité active

*Explication : vous interrogez un index déjà constitué, exactement comme une recherche sur un moteur de recherche classique ne scanne pas le site visé en temps réel.*

**Question 2 : Qu'est-ce qu'une bannière de service, au sens où Shodan l'utilise ?**
- A) Une publicité affichée sur le site de Shodan
- B) Le texte d'identification qu'un service renvoie en réponse à une connexion, révélant souvent son logiciel et sa version ✅
- C) Un certificat TLS
- D) Un type de pare-feu

*Explication : cette information, collectée par le scan continu de Shodan, permet d'identifier précisément la nature des services exposés.*

**Question 3 : Pourquoi ne faut-il jamais se connecter à un service découvert via Shodan sans autorisation ?**
- A) Parce que Shodan bloque techniquement toute connexion
- B) Parce que le fait qu'un service réponde publiquement ne constitue aucune autorisation à l'utiliser, et cela resterait une tentative d'intrusion ✅
- C) Parce que ces services sont toujours protégés par un mot de passe
- D) Parce que cela endommagerait automatiquement le service

*Explication : la visibilité publique d'un service n'a jamais été, en droit, une autorisation d'accès.*

**Question 4 : Quel principe de sécurité, déjà rencontré dans ce cours, est directement illustré par les découvertes de caméras ou d'objets connectés exposés sans authentification ?**
- A) Le principe du moindre privilège appliqué à l'exposition réseau : un service ne devrait être accessible que depuis là où il est réellement nécessaire ✅
- B) Le principe de la défense en profondeur uniquement
- C) Le principe de non-répudiation
- D) Le principe de disponibilité maximale

*Explication : c'est une application directe du moindre privilège (module Réseau & Linux, leçon 11), étendu ici à l'exposition réseau plutôt qu'aux permissions système.*

**Question 5 : Quel est l'intérêt d'utiliser l'API Shodan plutôt que l'interface web pour une veille régulière ?**
- A) L'API est toujours gratuite contrairement à l'interface web
- B) Elle permet d'automatiser et de répéter la surveillance de sa propre surface d'exposition dans un script, plutôt que de répéter une recherche manuelle ✅
- C) L'API donne accès à des résultats différents de l'interface web
- D) Elle ne nécessite aucune clé d'authentification

*Explication : l'automatisation via API s'inscrit dans la même logique de veille que celle déjà présentée pour le Google Dorking (module Python, leçon 10).*

## 📝 Résumé

- Shodan et Censys scannent en continu Internet et indexent les bannières des services qui répondent, constituant un moteur de recherche d'appareils et services exposés.
- Leur syntaxe de recherche (org, port, product, country...) permet de cibler précisément une organisation ou un type de service.
- Consulter ces moteurs est une activité passive ; s'y connecter sans autorisation reste une intrusion non autorisée, quelle que soit la facilité d'accès apparente.
- Un audit régulier de sa propre exposition, manuel ou automatisé par API, permet de détecter un service ouvert par erreur avant qu'un tiers malveillant ne le fasse.
- Ces outils illustrent une fois de plus le principe du moindre privilège, étendu ici à l'exposition réseau.

## 🎓 Ce que vous avez appris

✅ Comprendre comment Shodan et Censys indexent les services exposés sur Internet
✅ Utiliser leur syntaxe de recherche pour auditer une exposition précise
✅ Interroger ces moteurs par API avec Python
✅ Distinguer l'audit légitime de l'accès non autorisé à un service découvert

## ➡️ Leçon suivante

**15 : Analyse de métadonnées** : ce que les fichiers (photos, documents) révèlent sans qu'on le remarque. Fichier : `15-analyse-metadonnees.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
