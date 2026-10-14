---
title: "Le Routage"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 30
order: 7
category: "reseau"
tags: ["reseau", "routage", "routeur", "table-de-routage", "ospf", "bgp", "passerelle"]
prerequisites: ["04-adressage-ip"]
learning_objectives:
  - "Expliquer comment un routeur choisit le chemin d'un paquet"
  - "Lire une table de routage"
  - "Distinguer routage statique et dynamique"
  - "Identifier les risques de sécurité liés au routage"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Le Routage

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Expliquer comment un routeur choisit le chemin d'un paquet
- Lire une table de routage
- Distinguer routage statique et dynamique
- Identifier les risques de sécurité liés au routage

## 📚 Prérequis

- Leçon 04 : *Adressage IP et Sous-réseaux* (réseau, masque, CIDR)

## 🧭 Introduction

Imagine que tu dois envoyer un colis de Brazzaville à Kinshasa, Dakar ou Paris. Tu ne connais pas la route complète. Tu le donnes à la poste de ton quartier, qui le transmet à un centre de tri, lequel le passe à un autre, et ainsi de suite. À chaque étape, un opérateur ne connaît que **le prochain relais**, pas tout le trajet.

C'est exactement le **routage**. Un routeur reçoit un paquet, lit l'adresse de destination, consulte sa **table de routage** et envoie le paquet vers le **prochain saut** (*next hop*). Ce processus se répète de routeur en routeur jusqu'à destination.

Le routage est le cœur de la couche 3 (réseau). Pour un professionnel de la sécurité, il compte pour trois raisons : savoir **où passe le trafic**, savoir **comment un attaquant peut le dévier**, et savoir **où placer les contrôles** (pare-feu, segmentation). Des incidents réels sont survenus lorsque des routes Internet ont été annoncées par erreur ou par malveillance, détournant le trafic de pays entiers.

## 📖 Concepts clés

### 1. Que fait un routeur ?

Un routeur possède **plusieurs interfaces**, chacune connectée à un réseau différent. Pour chaque paquet reçu, il :
1. lit l'adresse IP de destination ;
2. cherche dans sa table de routage la **route la plus précise** qui correspond ;
3. décrémente le TTL ;
4. envoie le paquet vers le prochain saut par l'interface appropriée.

Il ne regarde pas le contenu de l'application (HTTP, DNS…) : il ne lit que l'en-tête IP.

### 2. Les hôtes aussi routent (un peu)

Même ton PC ou ton téléphone consulte une mini-table de routage pour décider :
- si la destination est **dans le même réseau** (il l'envoie directement) ;
- sinon, il envoie le paquet à la **passerelle par défaut** (ta box).

Pour savoir si une destination est locale, il applique son masque (voir leçon 04). Exemple : ta machine est en `192.168.1.25/24`. Pour joindre `192.168.1.40`, c'est direct. Pour joindre `8.8.8.8`, c'est via la passerelle `192.168.1.1`.

### 3. La table de routage

Chaque ligne d'une table contient en gros :

| Champ | Signification |
|---|---|
| Destination | Le réseau visé (ex. `10.0.2.0/24`) |
| Masque / préfixe | La taille de ce réseau |
| Passerelle (next hop) | Le prochain routeur à qui envoyer |
| Interface | La sortie à utiliser |
| Métrique | Le « coût » de la route (plus petit = préféré) |

Exemple simplifié :

```
Destination      Passerelle      Interface   Métrique
192.168.1.0/24   (directe)       eth0        0
10.0.2.0/24      192.168.1.254   eth0        10
0.0.0.0/0        192.168.1.1     eth0        100
```

La route `0.0.0.0/0` est la **route par défaut** : elle capte tout ce qui n'a pas de route plus précise. C'est elle qui envoie ton trafic vers Internet.

### 4. La règle du préfixe le plus long

Quand plusieurs routes correspondent à une destination, le routeur choisit **la plus spécifique**, c'est-à-dire celle au masque le plus long (*longest prefix match*).

Exemple : destination `10.0.2.55`, avec deux routes :
- `10.0.0.0/8` via A
- `10.0.2.0/24` via B

Les deux correspondent, mais `/24` est plus précis que `/8` : le paquet part vers **B**.

Conséquence de sécurité : annoncer une route **plus précise** que celle du voisin suffit à détourner le trafic. C'est le principe de nombreux détournements de routes.

### 5. Routage statique et dynamique

**Routage statique** : un administrateur écrit les routes à la main.
- ✅ Simple, prévisible, léger, pas de protocole à attaquer.
- ❌ Fastidieux à grande échelle, ne réagit pas seul aux pannes.
- Usage : petits réseaux, route par défaut vers l'opérateur.

**Routage dynamique** : les routeurs **échangent leurs routes** grâce à des protocoles et s'adaptent aux changements.
- ✅ S'adapte aux pannes, évolue avec le réseau.
- ❌ Plus complexe ; chaque protocole est une surface d'attaque s'il n'est pas authentifié.

### 6. Les protocoles de routage

On les classe en deux familles :

**Protocoles intérieurs (IGP)**, au sein d'une même organisation :

| Protocole | Particularité |
|---|---|
| RIP | Très simple, métrique = nombre de sauts (max 15), obsolète pour les grands réseaux |
| OSPF | Basé sur l'état des liens, rapide, très utilisé en entreprise |
| EIGRP | Protocole Cisco, hybride |

**Protocole extérieur (EGP)**, entre organisations :

| Protocole | Particularité |
|---|---|
| BGP | Le protocole d'**Internet**. Relie les « systèmes autonomes » (AS), c'est-à-dire les réseaux des opérateurs, fournisseurs de contenu, grandes entreprises |

Un **système autonome** (AS) est un ensemble de réseaux sous une même autorité d'administration, identifié par un numéro (ASN). BGP fonctionne sur la **confiance** entre opérateurs.

### 7. Sécurité du routage

| Risque | Description | Parade |
|---|---|---|
| **Détournement BGP** (*BGP hijacking*) | Un AS annonce des préfixes qui ne lui appartiennent pas : le trafic est dévié (écoute, panne, usurpation) | Filtrage des préfixes, RPKI (validation d'origine) |
| **Injection de fausses routes** | Un attaquant dans le réseau annonce des routes OSPF/RIP mensongères | Authentification des voisins de routage |
| **Routage source** | Option IP qui laisse l'émetteur imposer le chemin (peut servir à contourner des filtres) | Désactiver le routage source |
| **Route par défaut mal configurée** | Fuite de trafic interne vers un autre réseau | Revue de configuration, segmentation |
| **Usurpation d'adresse IP** | Faux paquets avec adresse source falsifiée | Filtrage anti-usurpation (ex. uRPF, BCP38) |
| **Passerelle compromise** | Si l'attaquant contrôle le routeur, il voit tout le trafic non chiffré | Mises à jour, mots de passe forts, administration sécurisée |

**Défense en profondeur** : le routeur est aussi un point de contrôle. On y place des **listes de contrôle d'accès** (ACL) pour filtrer le trafic entre réseaux, et on sépare les réseaux sensibles des réseaux invités.

### 8. Le TTL et traceroute

Chaque routeur décrémente le TTL de 1. Quand il tombe à 0, le routeur détruit le paquet et renvoie un message ICMP « Time Exceeded ». `traceroute` exploite cela : il envoie des paquets avec un TTL de 1, puis 2, puis 3… et note quel routeur répond à chaque fois, révélant ainsi le chemin.

### 9. Routage en pratique en Afrique francophone

Une part importante du trafic africain transite encore par des liaisons passant par l'Europe avant de revenir sur le continent. Le développement des points d'échange Internet (IXP) locaux permet de garder le trafic local à l'intérieur de la région, ce qui améliore la latence, réduit les coûts et diminue l'exposition à des interceptions lointaines.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : tu n'observes ici que **ta machine** et des chemins publics. Ne modifie jamais la configuration d'un routeur qui n'est pas le tien.

### Exercice 1 — Lire la table de routage de ta machine

```bash
# Windows
route print

# Linux
ip route show

# macOS
netstat -nr
```

Repère :
1. la **route par défaut** (`0.0.0.0/0` ou `default`) ;
2. l'adresse de la **passerelle** ;
3. la route de ton **réseau local** (par exemple `192.168.1.0/24`).

Question guidée : si tu veux joindre `192.168.1.40` puis `8.8.8.8`, par où ta machine envoie-t-elle chaque paquet ? (Direct pour le premier, via la passerelle pour le second.)

### Exercice 2 — Tracer le chemin

```bash
# Windows
tracert -d example.com

# Linux/macOS
traceroute -n example.com
```

(`-d` / `-n` évitent la résolution de noms, ce qui accélère l'affichage.)

Pour chaque ligne :
1. note l'adresse du routeur ;
2. observe les temps de réponse ;
3. repère à quel moment les temps augmentent : changement de pays ou liaison longue distance.

Compare avec un site hébergé localement et un site hébergé à l'étranger.

### Exercice 3 — Préfixe le plus long (papier-crayon)

Soit la table :

```
10.0.0.0/8      → via R1
10.20.0.0/16    → via R2
10.20.30.0/24   → via R3
0.0.0.0/0       → via R4
```

Pour chaque destination, indique le routeur choisi :

| Destination | Réponse |
|---|---|
| 10.20.30.5 | R3 (/24, le plus précis) |
| 10.20.99.1 | R2 (/16) |
| 10.99.1.1 | R1 (/8) |
| 8.8.8.8 | R4 (route par défaut) |

### Exercice 4 — Explorer un système autonome

Cherche l'adresse publique de ta box (voir leçon 04) et utilise un service public de consultation d'ASN (par exemple bgp.he.net) pour savoir à quel **AS** appartient cette adresse. Tu découvres quel opérateur la gère. Il s'agit d'informations publiques.

### Exercice 5 — Ajouter une route sur une machine de laboratoire

**Uniquement dans une machine virtuelle de test**, pour comprendre le mécanisme :

```bash
# Linux : ajouter une route vers un réseau fictif via la passerelle
sudo ip route add 10.99.0.0/24 via 192.168.1.1
ip route show
# La retirer ensuite
sudo ip route del 10.99.0.0/24
```

Remplace `192.168.1.1` par ta passerelle réelle. Tu viens de manipuler directement la table de routage.

## 🔍 Approfondissement

### Pour aller plus loin

- Cisco Networking Academy : modules gratuits de routage (CCNA).
- Le site de l'Internet Society sur la sécurité du routage (MANRS : *Mutually Agreed Norms for Routing Security*).
- RFC 4271 (BGP) pour les curieux.

### Pièges courants

- ❌ **Erreur fréquente 1** : croire qu'un routeur connaît le chemin complet. Il ne connaît que le **prochain saut**.
- ✅ **Bonne pratique** : raisonner en « saut par saut ».
- ❌ **Erreur fréquente 2** : confondre passerelle par défaut et DNS. La passerelle route les paquets ; le DNS traduit les noms.
- ✅ **Bonne pratique** : en dépannage, vérifier séparément passerelle (ping) et DNS (nslookup).
- ❌ **Erreur fréquente 3** : laisser les protocoles de routage dynamique sans authentification.
- ✅ **Bonne pratique** : authentifier les voisins de routage et limiter les interfaces qui participent.
- ❌ **Erreur fréquente 4** : considérer un routeur comme un simple boîtier de connexion.
- ✅ **Bonne pratique** : le mettre à jour, changer ses identifiants par défaut, désactiver l'administration à distance non nécessaire.

## 🧪 Quiz de validation

**Question 1 : À quoi sert la passerelle par défaut ?**
- A) À traduire les noms de domaine
- B) À recevoir les paquets destinés à l'extérieur du réseau local ✅
- C) À chiffrer le trafic
- D) À distribuer les adresses IP

*Explication : quand la destination n'est pas dans le réseau local, la machine envoie le paquet à la passerelle.*

**Question 2 : Entre `10.0.0.0/8` et `10.20.0.0/16`, quelle route est choisie pour `10.20.5.5` ?**
- A) 10.0.0.0/8
- B) 10.20.0.0/16 ✅
- C) Aucune
- D) Les deux en même temps

*Explication : la règle du préfixe le plus long retient la route la plus précise.*

**Question 3 : Quel protocole est utilisé entre les opérateurs sur Internet ?**
- A) RIP
- B) OSPF
- C) BGP ✅
- D) DHCP

*Explication : BGP relie les systèmes autonomes qui composent Internet.*

**Question 4 : Qu'est-ce que le routage statique ?**
- A) Des routes saisies manuellement par l'administrateur ✅
- B) Des routes apprises automatiquement
- C) Un routage chiffré
- D) Un routage sans passerelle

*Explication : les routes statiques ne changent pas seules, contrairement au routage dynamique.*

**Question 5 : Quel est un risque lié à BGP ?**
- A) Le détournement de préfixes IP ✅
- B) L'attribution d'adresses MAC
- C) L'expiration d'un bail DHCP
- D) La compression de données

*Explication : un AS peut annoncer à tort des préfixes qui ne lui appartiennent pas, ce qui dévie le trafic.*

## 📝 Résumé

- Un routeur lit l'adresse de destination et envoie le paquet vers le prochain saut selon sa table de routage.
- La route la plus précise (préfixe le plus long) l'emporte ; la route par défaut (`0.0.0.0/0`) capte le reste.
- Le routage peut être statique (manuel) ou dynamique (RIP, OSPF en interne, BGP entre opérateurs).
- `route print`, `ip route` et `traceroute` permettent d'observer ta table et ton chemin.
- Les risques majeurs sont le détournement de routes, les fausses annonces, l'usurpation d'adresse et les routeurs mal sécurisés.

## 🎓 Ce que tu as appris

✅ Décrire la décision de routage d'un paquet
✅ Lire une table de routage et appliquer le préfixe le plus long
✅ Comparer routage statique et dynamique
✅ Identifier les menaces sur le routage et leurs parades

## ➡️ Leçon suivante

**08 : Switching et VLAN** : comment fonctionne un commutateur, la table MAC, la segmentation par VLAN et les attaques de couche 2. Fichier : `08-switching-vlan.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
