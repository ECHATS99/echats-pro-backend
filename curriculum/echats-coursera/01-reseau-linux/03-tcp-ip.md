---
title: "Le Modèle TCP/IP"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 30
order: 3
category: "reseau"
tags: ["reseau", "tcp", "udp", "ip", "ports", "handshake"]
prerequisites: ["01-introduction-reseaux", "02-modele-osi"]
learning_objectives:
  - "Situer le modèle TCP/IP par rapport au modèle OSI"
  - "Expliquer la poignée de main en trois temps de TCP"
  - "Distinguer TCP et UDP et choisir le bon selon l'usage"
  - "Comprendre les ports et observer des connexions sur sa machine"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Le Modèle TCP/IP

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Situer le modèle TCP/IP par rapport au modèle OSI
- Expliquer la poignée de main en trois temps de TCP
- Distinguer TCP et UDP et choisir le bon selon l'usage
- Comprendre les ports et observer des connexions sur ta machine

## 📚 Prérequis

- Leçon 01 : *Introduction aux Réseaux Informatiques*
- Leçon 02 : *Le Modèle OSI*

## 🧭 Introduction

Le modèle OSI est un excellent outil d'apprentissage, mais ce n'est pas lui qui fait tourner Internet. Le véritable « moteur » s'appelle **TCP/IP**, du nom de ses deux protocoles les plus célèbres : *Transmission Control Protocol* et *Internet Protocol*. Il est né dans les années 1970 d'un projet de recherche américain (ARPANET) et s'est imposé parce qu'il était simple, robuste et ouvert.

Pourquoi le maîtriser quand on fait de la cybersécurité ? Parce que **chaque scan de ports, chaque attaque par déni de service, chaque règle de pare-feu** repose sur des notions TCP/IP : adresses, ports, états de connexion, drapeaux. Quand un outil comme Nmap te dit « port 443 ouvert », il parle de TCP/IP. Quand un analyste voit une avalanche de paquets SYN, il reconnaît une attaque.

Cette leçon est le pivot du module : elle relie le vocabulaire théorique de l'OSI à la réalité des paquets qui circulent sur ton réseau, y compris les paiements Mobile Money et les applications que tu utilises chaque jour.

## 📖 Concepts clés

### 1. Les quatre couches de TCP/IP

TCP/IP regroupe les sept couches d'OSI en quatre :

| Couche TCP/IP | Équivalent OSI | Rôle | Protocoles |
|---|---|---|---|
| Application | 5, 6, 7 | Services pour l'utilisateur | HTTP, HTTPS, DNS, SMTP, SSH, FTP |
| Transport | 4 | Communication entre applications | TCP, UDP |
| Internet | 3 | Adressage et routage | IP, ICMP |
| Accès réseau | 1, 2 | Transmission sur le support local | Ethernet, Wi-Fi |

Le principe reste le même : encapsulation à l'envoi, décapsulation à la réception.

### 2. IP : le facteur qui ne garantit rien

**IP** (*Internet Protocol*) a une mission : acheminer des paquets d'une adresse source à une adresse destination, de routeur en routeur. Mais IP est un protocole **sans garantie** (« au mieux ») :
- un paquet peut se perdre ;
- plusieurs paquets peuvent arriver dans le désordre ;
- un paquet peut être dupliqué.

IP ne vérifie rien : c'est le travail de la couche au-dessus. Un en-tête IPv4 contient notamment l'adresse source, l'adresse destination, le protocole transporté (TCP = 6, UDP = 17, ICMP = 1) et le **TTL** (*Time To Live*), un compteur décrémenté à chaque routeur traversé. Quand il atteint 0, le paquet est détruit : cela évite qu'un paquet tourne indéfiniment. C'est d'ailleurs le principe qui fait fonctionner `traceroute`.

### 3. Les ports : à quelle porte frapper ?

L'adresse IP identifie **la machine**. Mais une machine exécute plusieurs services en même temps : un serveur web, une messagerie, un accès à distance… Le **port** identifie **le service** visé. Analogie : l'adresse IP est l'adresse d'un immeuble, le port est le numéro de l'appartement.

Un port est un nombre de 0 à 65 535.

| Plage | Nom | Usage |
|---|---|---|
| 0 – 1023 | Ports bien connus | Services standards |
| 1024 – 49151 | Ports enregistrés | Applications |
| 49152 – 65535 | Ports dynamiques | Connexions temporaires côté client |

Ports à connaître absolument :

| Port | Protocole | Service |
|---|---|---|
| 20/21 | TCP | FTP |
| 22 | TCP | SSH |
| 23 | TCP | Telnet (non chiffré, à éviter) |
| 25 | TCP | SMTP |
| 53 | UDP/TCP | DNS |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 143 | TCP | IMAP |
| 443 | TCP | HTTPS |
| 3306 | TCP | MySQL |
| 3389 | TCP | Bureau à distance Windows (RDP) |

Une connexion est identifiée par un quadruplet : **IP source, port source, IP destination, port destination**. Quand ton navigateur contacte un site, il utilise un port source dynamique (par exemple 52814) vers le port 443 du serveur.

### 4. TCP : le transporteur fiable

**TCP** (*Transmission Control Protocol*) fournit un service **fiable et orienté connexion** :
- il établit une connexion avant d'envoyer les données ;
- il numérote les segments pour les remettre dans l'ordre ;
- il exige des **accusés de réception** (ACK) et renvoie ce qui s'est perdu ;
- il régule le débit pour ne pas saturer le récepteur ou le réseau.

On l'utilise quand **chaque octet compte** : pages web, e-mails, transferts de fichiers, accès SSH.

**Les drapeaux (flags) TCP** sont de petits indicateurs dans l'en-tête :

| Drapeau | Signification |
|---|---|
| SYN | Demande d'ouverture de connexion |
| ACK | Accusé de réception |
| FIN | Fermeture propre |
| RST | Rupture brutale de la connexion |
| PSH | Transmettre immédiatement les données |

### 5. La poignée de main en trois temps (three-way handshake)

Avant d'échanger des données, un client et un serveur « se présentent » :

```
Client                          Serveur
  |  ---- SYN (seq = x) ---->     |   1. « Je voudrais me connecter »
  |  <-- SYN-ACK (seq = y,        |   2. « OK, je suis prêt, et toi ? »
  |        ack = x+1) ---------   |
  |  ---- ACK (ack = y+1) ---->   |   3. « Parfait, on commence »
  |                               |
  |  <====== données ======>      |
```

Analogie téléphonique : « Allô ? » (SYN) → « Allô, je t'entends, tu m'entends ? » (SYN-ACK) → « Oui, je t'entends » (ACK).

Les nombres `seq` sont des **numéros de séquence** qui permettent de remettre les segments dans l'ordre et de détecter les pertes.

**Fermeture** : chaque côté envoie un FIN et reçoit un ACK ; un RST coupe la connexion immédiatement.

**Lien avec la sécurité** :
- Un **scan de ports** envoie des SYN et regarde les réponses : SYN-ACK = port ouvert, RST = port fermé, pas de réponse = port filtré par un pare-feu.
- Une attaque **SYN flood** envoie un grand nombre de SYN sans jamais finir la poignée de main, pour saturer le serveur. C'est un exemple de déni de service. La défense classique est l'usage de « SYN cookies » et de limitations de débit.

### 6. UDP : le transporteur rapide

**UDP** (*User Datagram Protocol*) est **sans connexion** et **sans garantie** : il envoie des datagrammes et ne vérifie rien. En contrepartie, il est **léger et rapide**.

On l'utilise quand la **vitesse prime sur la perfection** : appels vocaux et vidéo, jeux en ligne, streaming en direct, requêtes DNS.

Analogie : TCP est un courrier recommandé avec accusé de réception ; UDP est une carte postale glissée dans une boîte aux lettres.

| Critère | TCP | UDP |
|---|---|---|
| Connexion | Oui (handshake) | Non |
| Fiabilité | Garantie | Non garantie |
| Ordre des données | Respecté | Non garanti |
| Vitesse | Plus lent | Plus rapide |
| En-tête | 20 octets minimum | 8 octets |
| Usages | Web, mail, SSH, fichiers | DNS, VoIP, jeux, streaming |

**Sécurité** : comme UDP ne vérifie pas l'émetteur, il est plus facile à usurper et sert souvent aux attaques d'amplification (par exemple via des services DNS mal configurés).

### 7. ICMP : le messager de diagnostic

**ICMP** (*Internet Control Message Protocol*) n'est ni TCP ni UDP : c'est un protocole de contrôle de la couche Internet. Il transporte des messages d'erreur et de diagnostic. `ping` utilise les messages *Echo Request / Echo Reply* ; `traceroute` exploite les messages *Time Exceeded* produits quand le TTL tombe à zéro.

Beaucoup de pare-feu filtrent ICMP pour réduire la visibilité du réseau.

### 8. Les états d'une connexion TCP

Une connexion passe par plusieurs états, que tu liras dans des outils comme `netstat` ou `ss` :

| État | Signification |
|---|---|
| LISTEN | Le service attend des connexions |
| SYN_SENT | Connexion demandée, en attente de réponse |
| ESTABLISHED | Connexion active |
| TIME_WAIT | Connexion terminée, en attente de nettoyage |
| CLOSE_WAIT | L'autre côté a fermé, la fermeture locale est en attente |

Repérer des dizaines de connexions `SYN_SENT` ou `SYN_RECV` anormales peut révéler une attaque ou un balayage.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : ces exercices ne concernent que **ta propre machine**. Ne scanne jamais un réseau ou un serveur qui ne t'appartient pas sans autorisation écrite.

### Exercice 1 — Lister les connexions et ports ouverts

```bash
# Windows
netstat -ano

# Linux
ss -tulpn          # ports en écoute (TCP/UDP) + processus
ss -tn             # connexions TCP établies
```

Repère :
1. Les lignes en état **LISTEN** : quels services attendent des connexions sur ta machine ?
2. Les lignes **ESTABLISHED** : vers quelles adresses et quels ports ta machine communique-t-elle ?
3. Les ports distants : reconnais-tu des 443 (HTTPS) ?

Question guidée : pourquoi y a-t-il plusieurs connexions vers le port 443 alors que tu n'as qu'un navigateur ? (Réponse : chaque onglet, chaque ressource et chaque application peut ouvrir ses propres connexions.)

### Exercice 2 — Voir la poignée de main dans Wireshark

1. Lance Wireshark sur ton interface réseau.
2. Filtre d'affichage : `tcp.port == 443` (ou `tcp.flags.syn == 1` pour ne voir que les SYN).
3. Ouvre un site HTTPS dans ton navigateur.
4. Arrête la capture et cherche trois paquets consécutifs : `[SYN]`, `[SYN, ACK]`, `[ACK]`.

Clique sur chacun et déplie la section « Transmission Control Protocol » : repère les ports source et destination, les numéros de séquence et les drapeaux. Tu viens de voir la poignée de main en direct.

### Exercice 3 — Tester un port avec un outil simple

```bash
# Linux/macOS : tester si un port répond sur TA machine
nc -zv 127.0.0.1 22

# Windows (PowerShell)
Test-NetConnection -ComputerName 127.0.0.1 -Port 3389
```

Interprétation : « succeeded » signifie qu'un service écoute ; « refused » signifie qu'aucun service n'écoute. Teste un port que tu sais ouvert (par exemple celui vu dans l'exercice 1) puis un port fermé.

### Exercice 4 — Comparer TCP et UDP

Dans Wireshark, utilise tour à tour les filtres `udp.port == 53` puis `tcp`. Ouvre un site et compare : DNS passe en UDP (pas de handshake), la page web passe en TCP (handshake visible). Note la différence de taille d'en-tête dans le panneau de détails.

## 🔍 Approfondissement

### Pour aller plus loin

- RFC 793 (TCP) et RFC 791 (IP), lisibles en diagonale pour comprendre les en-têtes.
- Module « Network Fundamentals » sur TryHackMe.
- Le manuel de `ss` et de `nc` (`man ss`, `man nc`).

### Pièges courants

- ❌ **Erreur fréquente 1** : croire qu'un port « fermé » est sûr et qu'un port « filtré » ne l'est pas. Fermé veut dire : la machine répond qu'aucun service n'écoute. Filtré veut dire : un pare-feu ne répond pas. Les deux informations sont utiles à un attaquant comme à un défenseur.
- ✅ **Bonne pratique** : n'exposer que les ports strictement nécessaires.
- ❌ **Erreur fréquente 2** : penser qu'UDP est « moins sécurisé » par nature. Il est simplement sans état ; la sécurité dépend du protocole applicatif au-dessus.
- ✅ **Bonne pratique** : raisonner sur le service (DNS, VoIP…) et son chiffrement, pas seulement sur le transport.
- ❌ **Erreur fréquente 3** : laisser des services d'administration (RDP, SSH, bases de données) ouverts à tout Internet.
- ✅ **Bonne pratique** : restreindre l'accès par pare-feu, VPN ou liste d'adresses autorisées, et utiliser l'authentification forte.

## 🧪 Quiz de validation

**Question 1 : Combien de couches compte le modèle TCP/IP ?**
- A) 3
- B) 4 ✅
- C) 5
- D) 7

*Explication : Application, Transport, Internet, Accès réseau.*

**Question 2 : Quelle est la bonne séquence de la poignée de main TCP ?**
- A) ACK, SYN, SYN-ACK
- B) SYN, SYN-ACK, ACK ✅
- C) SYN, ACK, FIN
- D) SYN-ACK, SYN, ACK

*Explication : le client envoie SYN, le serveur répond SYN-ACK, le client conclut par ACK.*

**Question 3 : Quel port utilise HTTPS par défaut ?**
- A) 21
- B) 80
- C) 443 ✅
- D) 3389

*Explication : 80 est HTTP en clair, 443 est HTTP chiffré par TLS.*

**Question 4 : Pour un appel vidéo en direct, quel protocole de transport est le plus adapté ?**
- A) TCP, pour la fiabilité absolue
- B) UDP, pour la rapidité et la faible latence ✅
- C) ICMP
- D) FTP

*Explication : en direct, mieux vaut perdre une image que retarder toute la vidéo. UDP évite les retransmissions.*

**Question 5 : Un SYN flood consiste à…**
- A) Envoyer de nombreux SYN sans terminer la poignée de main, pour saturer un serveur ✅
- B) Chiffrer le trafic d'un serveur
- C) Lire les mots de passe sur le réseau
- D) Modifier les adresses MAC

*Explication : le serveur réserve des ressources pour chaque SYN reçu et finit par ne plus pouvoir accepter de vraies connexions.*

## 📝 Résumé

- TCP/IP est le modèle réellement utilisé par Internet : Application, Transport, Internet, Accès réseau.
- IP achemine les paquets sans garantie ; TCP ajoute fiabilité et ordre ; UDP privilégie la vitesse.
- Le port identifie le service, l'adresse IP identifie la machine.
- La poignée de main en trois temps (SYN, SYN-ACK, ACK) ouvre une connexion TCP.
- `ss`, `netstat`, `nc` et Wireshark permettent d'observer ports et connexions.
- Les scans de ports et le SYN flood exploitent directement ces mécanismes.

## 🎓 Ce que tu as appris

✅ Relier TCP/IP et OSI
✅ Expliquer le handshake TCP et le rôle des flags
✅ Choisir entre TCP et UDP selon l'usage
✅ Lister et interpréter les connexions de ta machine

## ➡️ Leçon suivante

**04 : Adressage IP** : classes, masques, notation CIDR, sous-réseaux et adresses privées. Tu apprendras à calculer un réseau à la main. Fichier : `04-adressage-ip.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
