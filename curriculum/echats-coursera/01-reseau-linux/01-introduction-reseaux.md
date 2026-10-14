---
title: "Introduction aux Réseaux Informatiques"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 25
order: 1
category: "reseau"
tags: ["reseau", "lan", "wan", "fondamentaux", "ip"]
prerequisites: []
learning_objectives:
  - "Comprendre le rôle d'un réseau informatique"
  - "Identifier les composants d'un réseau"
  - "Distinguer LAN, WAN, MAN"
  - "Observer la configuration réseau de sa propre machine"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Introduction aux Réseaux Informatiques

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Comprendre le rôle d'un réseau informatique
- Identifier les composants d'un réseau
- Distinguer LAN, WAN, MAN
- Lire la configuration réseau de ta propre machine

## 📚 Prérequis

Aucun prérequis. Cette leçon est accessible aux débutants complets.

## 🧭 Introduction

Quand tu envoies un message WhatsApp à un ami à Pointe-Noire alors que tu es à Brazzaville, ton message traverse en quelques centaines de millisecondes ton téléphone, l'antenne de ton opérateur, des câbles, des serveurs, puis le chemin inverse jusqu'à l'appareil de ton ami. Tout cela repose sur une chose : **un réseau informatique**.

Un réseau, c'est simplement un ensemble d'appareils (ordinateurs, téléphones, serveurs, imprimantes…) capables d'échanger des données grâce à des règles communes. Sans réseau, pas d'Internet, pas de Mobile Money, pas de banque en ligne, pas de réseaux sociaux.

**Pourquoi est-ce crucial en cybersécurité ?** Parce que presque toutes les attaques passent par un réseau. Un pirate qui vole des identifiants, un ransomware qui se propage dans une entreprise, un site web compromis : à chaque fois, des données circulent d'un point A à un point B. Si tu ne comprends pas comment elles circulent, tu ne peux ni les attaquer en test d'intrusion légal, ni les défendre.

Dans le parcours ECHATS PRO, cette leçon est la porte d'entrée du module **Réseau & Linux**. Les suivantes (modèle OSI, TCP/IP, DNS, firewall…) s'appuient toutes sur le vocabulaire posé ici.

## 📖 Concepts clés

### 1. Définition d'un réseau

Imagine un quartier. Chaque maison est un appareil. Les rues sont les liaisons (câbles ou ondes radio). Les carrefours sont les équipements qui orientent la circulation. Les adresses des maisons permettent au facteur de livrer le courrier au bon endroit. Dans un réseau informatique :

- les **maisons** sont les *hôtes* (PC, smartphones, serveurs) ;
- les **rues** sont les *supports de transmission* (câble Ethernet, fibre optique, Wi-Fi, 4G/5G) ;
- les **carrefours** sont les *équipements d'interconnexion* (switch, routeur) ;
- les **adresses** sont les *adresses IP* et *adresses MAC* ;
- le **code de la route** est l'ensemble des *protocoles* (TCP/IP, HTTP, DNS…).

Un **protocole** est un ensemble de règles qui permettent à deux machines de se comprendre, comme deux personnes qui parlent la même langue et respectent un tour de parole.

Les données ne circulent pas d'un bloc. Elles sont découpées en petits morceaux appelés **paquets** (ou trames selon le niveau). Chaque paquet porte une étiquette : qui envoie, qui reçoit, dans quel ordre le remonter. C'est comme envoyer un grand colis en plusieurs enveloppes numérotées.

### 2. Rôles d'un réseau

Un réseau permet principalement de :

1. **Partager des ressources** : une imprimante, un dossier, une connexion Internet.
2. **Communiquer** : e-mails, appels vidéo, messageries.
3. **Centraliser** : une base de données clients accessible depuis plusieurs agences.
4. **Offrir des services** : sites web, applications, paiement mobile.

Chaque point d'accès est aussi une **surface d'attaque** potentielle : plus un réseau est connecté, plus il est utile, et plus il doit être protégé.

### 3. Types de réseaux

**PAN (Personal Area Network)**
Réseau de quelques mètres autour d'une personne : ton téléphone connecté à ton casque Bluetooth ou à ta montre.

**LAN (Local Area Network)**
Réseau local couvrant un espace limité : une maison, un bureau, un cybercafé, une salle de classe.
- Caractéristiques : débit élevé, faible latence, géré par une seule organisation.
- Avantages : rapide, peu coûteux, simple à administrer.
- Exemples : le Wi-Fi de ta box, le réseau d'une agence bancaire, le réseau d'un laboratoire universitaire.

**MAN (Metropolitan Area Network)**
Réseau couvrant une ville ou une agglomération.
- Caractéristiques : relie plusieurs sites d'une même zone urbaine, souvent en fibre optique.
- Avantages : interconnecte des LAN à l'échelle d'une ville.
- Exemples : le réseau reliant les agences d'une banque dans une même capitale, un réseau municipal.

**WAN (Wide Area Network)**
Réseau couvrant de grandes distances : pays, continents.
- Caractéristiques : débit et latence variables, souvent opéré par des fournisseurs tiers.
- Avantages : relie des sites très éloignés.
- Exemples : **Internet** est le plus grand WAN au monde ; le réseau d'un opérateur de téléphonie reliant plusieurs pays d'Afrique centrale ; les liaisons sous-marines qui amènent la connectivité sur le continent.

| Type | Portée | Exemple | Qui le gère ? |
|---|---|---|---|
| PAN | ~10 m | Téléphone ↔ casque Bluetooth | Toi |
| LAN | Bâtiment | Wi-Fi d'un bureau | Une organisation |
| MAN | Ville | Agences d'une banque | Organisation / opérateur |
| WAN | Pays / monde | Internet | Opérateurs multiples |

### 4. Composants d'un réseau

| Composant | Rôle | Exemple |
|---|---|---|
| Hôte / terminal | Émet ou reçoit des données | PC, smartphone, serveur |
| Carte réseau (NIC) | Connecte l'hôte au réseau, possède une adresse MAC | Carte Ethernet, puce Wi-Fi |
| Switch (commutateur) | Relie les machines d'un même réseau local et transmet les trames à la bonne destination | Switch 8 ports d'un bureau |
| Routeur | Relie des réseaux différents et choisit le chemin des paquets | Box Internet, routeur d'opérateur |
| Point d'accès Wi-Fi | Fournit une connexion sans fil à un LAN | Borne Wi-Fi |
| Firewall (pare-feu) | Filtre le trafic selon des règles de sécurité | Pare-feu Windows, appliance dédiée |
| Serveur | Fournit un service à d'autres machines | Serveur web, serveur DNS |
| Support de transmission | Transporte les signaux | Câble RJ45, fibre, ondes radio |

**Switch vs routeur : la confusion classique.** Le switch fait circuler les données *à l'intérieur* d'un réseau. Le routeur fait circuler les données *entre* des réseaux. Pour reprendre l'analogie du quartier : le switch est le système de rues à l'intérieur du quartier, le routeur est la sortie qui mène vers les autres quartiers.

### 5. Adresses : comment trouver la bonne machine

Deux types d'adresses coexistent :

- **Adresse MAC** : identifiant physique de la carte réseau, de la forme `A4:5E:60:C2:11:9B`. Elle sert à la communication au sein d'un même réseau local.
- **Adresse IP** : identifiant logique de la machine sur un réseau, de la forme `192.168.1.25` (IPv4). Elle sert à acheminer les paquets entre réseaux.

Ta machine possède aussi une **passerelle par défaut** (*default gateway*) : l'adresse du routeur vers lequel elle envoie tout ce qui est destiné à l'extérieur du réseau local. Nous détaillerons l'adressage dans la leçon *04 – Adressage IP*.

### 6. Architectures : client-serveur et pair-à-pair

- **Client-serveur** : des clients demandent des services à un serveur central. C'est le modèle du web : ton navigateur (client) demande une page à un serveur.
- **Pair-à-pair (P2P)** : chaque machine peut être à la fois cliente et serveuse. C'est le cas de certains partages de fichiers.

La majorité des attaques web que tu étudieras plus tard ciblent le modèle client-serveur.

### 7. Le chemin d'une requête, de bout en bout

Quand tu ouvres un site depuis ton téléphone en Wi-Fi :

1. Ton téléphone (hôte) obtient une adresse IP de la box (via DHCP, étudié plus tard).
2. Il demande à un serveur DNS la correspondance entre le nom du site et son adresse IP.
3. Il envoie sa requête à la passerelle (la box).
4. La box (routeur) la transmet vers le réseau de l'opérateur, puis vers Internet, saut après saut.
5. Le serveur du site reçoit la requête, prépare la réponse, et la renvoie par le chemin inverse.

Chaque saut traverse des équipements différents. Chacun est un point où le trafic peut être observé, filtré, ou, pour un attaquant, intercepté si le chiffrement est absent.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : dans cette leçon, tu n'observes que **ta propre machine** et **ton propre réseau**. N'analyse jamais un réseau qui ne t'appartient pas sans autorisation écrite. Dans la plupart des pays, y compris ceux de la zone francophone africaine, l'accès non autorisé à un système informatique est une infraction pénale.

### Exercice 1 — Identifier son propre réseau

**Sous Windows** (ouvre l'invite de commandes : touche Windows, tape `cmd`, Entrée) :

```bash
ipconfig /all
```

**Sous Linux ou macOS** (ouvre un terminal) :

```bash
ip addr show
# ou, sur les systèmes plus anciens / macOS
ifconfig
```

Repère les informations suivantes et note-les :

| Information | Où la trouver | Ta valeur |
|---|---|---|
| Adresse IPv4 | `IPv4 Address` / `inet` | |
| Masque de sous-réseau | `Subnet Mask` / `netmask` | |
| Passerelle par défaut | `Default Gateway` | |
| Adresse MAC | `Physical Address` / `ether` | |
| Serveur DNS | `DNS Servers` | |

**Résultat attendu** (exemple) : une adresse du type `192.168.1.25`, un masque `255.255.255.0`, une passerelle `192.168.1.1`.

Questions guidées :
1. Ton adresse IP commence-t-elle par `192.168`, `10.` ou `172.16` à `172.31` ? Ce sont des adresses **privées**, utilisées uniquement à l'intérieur d'un LAN.
2. L'adresse de ta passerelle ressemble-t-elle à la tienne ? Elles partagent généralement les trois premiers nombres. Pourquoi, selon toi ? (Réponse : elles sont dans le même réseau.)
3. Quel équipement possède l'adresse de la passerelle ? (Réponse : ton routeur ou ta box.)

### Exercice 2 — Tester la connectivité avec `ping`

La commande `ping` envoie de petits messages à une machine et mesure le temps de réponse.

```bash
# Tester ta propre carte réseau (boucle locale)
ping 127.0.0.1

# Tester ta passerelle (remplace par TA valeur)
ping 192.168.1.1

# Tester Internet par adresse IP
ping 8.8.8.8
```

Sous Linux/macOS, ajoute `-c 4` pour limiter à 4 envois : `ping -c 4 8.8.8.8`.

**Résultat attendu** : des lignes indiquant `time=12ms` (ou une valeur proche) et des statistiques finales avec `0% packet loss`.

Interprétation, étape par étape :
- Si `127.0.0.1` échoue : problème de pile réseau sur ta machine.
- Si la passerelle échoue : problème entre ta machine et ta box (Wi-Fi, câble).
- Si `8.8.8.8` échoue alors que la passerelle répond : problème côté opérateur ou Internet.

C'est la première méthode de diagnostic : **partir de la machine et remonter vers l'extérieur**, couche par couche.

### Exercice 3 — Voir le chemin avec `traceroute`

```bash
# Windows
tracert example.com

# Linux / macOS
traceroute example.com
```

Chaque ligne est un **saut** (un routeur traversé). Tu verras d'abord ta box, puis des équipements de ton opérateur, puis des routeurs intermédiaires. Certaines lignes affichent `* * *` : le routeur ne répond pas, ce qui est normal.

Questions guidées :
1. Combien de sauts compte le trajet ?
2. À partir de quel saut le temps de réponse augmente-t-il fortement ? Cela correspond souvent à un changement de pays ou à une liaison longue distance.

### Exercice 4 — Dessiner ton réseau

Sur une feuille, dessine : ton appareil, ta box, Internet, et les autres appareils connectés chez toi (téléphone, TV…). Étiquette chaque élément avec son type (hôte, routeur, point d'accès) et note son adresse IP si tu la connais. Ce schéma est ta première **cartographie réseau**, étape fondamentale de tout audit.

## 🔍 Approfondissement

### Pour aller plus loin

- La page Wikipédia « Réseau informatique » pour une vue d'ensemble.
- Le module d'initiation aux réseaux de TryHackMe (« Pre Security »).
- Le cours gratuit « Réseaux » de l'ANSSI (SecNumacadémie), en français.

### Pièges courants

- ❌ **Erreur fréquente 1** : confondre Internet et le Web. Internet est l'infrastructure (le réseau de réseaux), le Web est un service parmi d'autres qui l'utilise (avec le mail, la VoIP, etc.).
- ✅ **Bonne pratique** : toujours distinguer l'infrastructure (réseau) du service (application).
- ❌ **Erreur fréquente 2** : croire qu'une adresse IP identifie une personne. Elle identifie une interface sur un réseau, et peut être partagée (NAT) ou changer (DHCP).
- ✅ **Bonne pratique** : en investigation, rattacher une IP à une personne demande des journaux, des horodatages précis et un cadre légal.
- ❌ **Erreur fréquente 3** : penser qu'un réseau Wi-Fi « caché » ou avec un mot de passe simple est sûr.
- ✅ **Bonne pratique** : utiliser WPA2/WPA3 avec une phrase de passe longue et changer les identifiants par défaut de la box.

### Lien avec la cybersécurité

Chaque composant vu aujourd'hui a ses vulnérabilités typiques : mots de passe par défaut sur les routeurs, switchs mal configurés, firewalls trop permissifs, serveurs exposés sans mise à jour. Les prochaines leçons t'apprendront à les identifier et à les corriger.

## 🧪 Quiz de validation

**Question 1 — Quel équipement permet de relier deux réseaux différents ?**
- A) Le switch
- B) Le routeur ✅
- C) Le hub
- D) Le répéteur

*Explication : le routeur travaille avec les adresses IP et achemine les paquets d'un réseau à un autre. Le switch, lui, relie les machines au sein d'un même réseau local.*

**Question 2 — Quel type de réseau décrit le mieux le Wi-Fi d'un cybercafé ?**
- A) WAN
- B) MAN
- C) LAN ✅
- D) PAN

*Explication : un LAN couvre un espace limité (un bâtiment) et est géré par une seule organisation.*

**Question 3 — Quelle adresse est une adresse IP privée ?**
- A) 8.8.8.8
- B) 192.168.1.25 ✅
- C) 41.77.10.5
- D) 142.250.74.46

*Explication : les plages 10.0.0.0/8, 172.16.0.0/12 et 192.168.0.0/16 sont réservées aux réseaux privés et ne sont pas routées sur Internet.*

**Question 4 — Que fait la commande `ping` ?**
- A) Elle chiffre les données
- B) Elle mesure si une machine répond et le temps de réponse ✅
- C) Elle bloque un port
- D) Elle change l'adresse IP

*Explication : `ping` envoie des messages de test (ICMP) et mesure la réponse. C'est un outil de diagnostic de base.*

**Question 5 — Que représente la passerelle par défaut ?**
- A) Le serveur DNS
- B) L'adresse MAC de la carte réseau
- C) Le routeur vers lequel sont envoyés les paquets destinés à l'extérieur du LAN ✅
- D) Le mot de passe du Wi-Fi

*Explication : quand la destination n'est pas dans ton réseau local, ta machine envoie le paquet à la passerelle, qui se charge de le faire suivre.*

## 📝 Résumé

- Un réseau est un ensemble d'appareils qui échangent des données selon des protocoles communs.
- On distingue PAN, LAN, MAN et WAN selon la portée ; Internet est un WAN gigantesque.
- Le switch relie les machines d'un même réseau, le routeur relie des réseaux entre eux.
- Une adresse MAC identifie une carte réseau localement ; une adresse IP identifie une machine sur un réseau.
- `ipconfig`/`ip addr`, `ping` et `traceroute` sont les outils de base pour observer et diagnostiquer.
- Tout réseau est une surface d'attaque : le comprendre est le préalable à sa défense.

## 🎓 Ce que tu as appris

✅ Définir un réseau et son utilité
✅ Distinguer PAN, LAN, MAN, WAN
✅ Nommer les composants et leurs rôles
✅ Lire ta configuration réseau et tester la connectivité

## ➡️ Leçon suivante

**02 – Le modèle OSI** : tu découvriras comment on découpe la communication réseau en 7 couches pour mieux la comprendre, la diagnostiquer et la sécuriser. Fichier : `02-modele-osi.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
