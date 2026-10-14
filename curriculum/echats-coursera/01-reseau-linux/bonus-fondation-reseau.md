---
title: "LEÇON 1  Le Réseau : Fondation de tout"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 20
order: 90
category: "reseau"
tags: ["reseau", "bonus"]
prerequisites: []
learning_objectives: []
author: "ECHATS PRO"
language: "fr"
published: true
---

## Enrichissement pédagogique — guide opératoire

### Positionnement
Cette leçon ouvre le parcours vers la cyberdéfense opérationnelle de niveau institutionnel. Elle ne constitue pas une accréditation officielle; elle installe les fondations nécessaires à l’administration système, au développement sécurisé, à l’investigation et à la détection.

### Objectifs observables
À la fin de la séance, l’apprenant sait expliquer les couches OSI et leur relation avec TCP/IP, distinguer TCP et UDP, interpréter une adresse IPv4 et une notation CIDR, relier IP, port et service, expliquer DNS et ARP, puis rédiger une note séparant observation, hypothèse et preuve.

### Prérequis
Aucun prérequis technique formel. Toute manipulation reste limitée au propre appareil, à un laboratoire local ou à un système explicitement autorisé.

### Checkpoints
Après OSI, explique pourquoi HTTPS mobilise plusieurs couches. Après TCP/UDP, choisis le protocole adapté à trois scénarios. Après l’adressage, calcule `/24` et `/30` et explique le cas `/32`. Après DNS/ARP, distingue résolution de nom, association locale et routage.

### Pratique guidée
Sur un environnement autorisé, observe `ip addr`, `ip route`, `ip neigh`, `ss -tuln` et `getent hosts example.com`. Pour chaque observation, consigne la commande, le résultat utile, l’interprétation, la limite et le test de confirmation.

### Challenge légal et éthique
À partir d’une sortie réseau fournie par l’enseignant, rédige une note d’une page avec périmètre, actifs, protocoles, preuves, hypothèses, limites et trois recommandations défensives priorisées. Aucun scan de tiers n’est demandé.

### Précisions et erreurs fréquentes
ARP est généralement rattaché à la liaison de données tout en faisant le lien avec l’adressage réseau. DNS utilise souvent UDP mais peut utiliser TCP selon le contexte. Un port ouvert est un indice de surface exposée, pas une vulnérabilité confirmée. Une route `/32` ne doit pas être décrite comme un sous-réseau classique sans préciser le contexte.

### Synthèse opérationnelle
L’analyste relie couche, protocole, adresse, port, service, observation et preuve. Il distingue toujours ce qui est connu de ce qui est supposé et de ce qui reste à vérifier.


**Le réseau. Parce que tout passe par le réseau.**

Un hacker qui ne comprend pas ce qui se passe sur le fil est aveugle. Avant Kali, avant les outils, avant tout — tu dois voir le réseau comme tu vois ta propre main.

---

Laisse-moi d'abord sauvegarder ton profil de formation :

Sauvegardé. Maintenant —

---

# 📡 LEÇON 1 — Le Réseau : Fondation de tout
### *Modèle OSI · TCP/IP · Protocoles · Adressage*

---

## PARTIE 1 — Pourquoi le réseau en premier

Imagine un cambrioleur qui veut entrer dans une banque. S'il ne comprend pas le plan du bâtiment, les entrées, les sorties, les caméras, les gardiens et comment ils communiquent entre eux — il est perdu avant même de commencer.

Le réseau c'est le plan du bâtiment de l'informatique.

Chaque attaque, chaque investigation, chaque outil de cybersécurité — Wireshark, Nmap, Metasploit, Burp Suite — tout repose sur la compréhension du réseau. Si tu ne comprends pas ce qui se passe sur le fil, tu utilises des outils sans comprendre ce qu'ils font. Tu seras toujours dépendant d'un tutoriel.

---

## PARTIE 2 — Le Modèle OSI

OSI signifie **Open Systems Interconnection**. C'est un modèle théorique créé en 1984 pour standardiser comment les ordinateurs communiquent. Il découpe la communication en **7 couches**, chacune avec un rôle précis.

Retiens cette phrase pour mémoriser les couches dans l'ordre :

> **"Please Do Not Throw Sausage Pizza Away"**

| # | Couche | Nom FR | Rôle | Exemples |
|---|--------|--------|------|---------|
| 7 | Application | Application | Interface avec l'utilisateur | HTTP, FTP, DNS, SMTP |
| 6 | Presentation | Présentation | Encodage, chiffrement, compression | SSL/TLS, JPEG, ASCII |
| 5 | Session | Session | Ouvre/maintient/ferme les sessions | NetBIOS, RPC |
| 4 | Transport | Transport | Fiabilité, ports, segmentation | TCP, UDP |
| 3 | Network | Réseau | Adressage et routage | IP, ICMP, ARP |
| 2 | Data Link | Liaison | Accès au support physique | Ethernet, WiFi, MAC |
| 1 | Physical | Physique | Bits sur le câble | Câble RJ45, fibre, radio |

**Comment retenir ça concrètement ?**

Quand tu envoies un message WhatsApp :
- Couche 7 : WhatsApp prépare ton message
- Couche 6 : il est chiffré (TLS)
- Couche 5 : une session est maintenue avec le serveur WhatsApp
- Couche 4 : le message est découpé en segments TCP
- Couche 3 : chaque segment reçoit une adresse IP source et destination
- Couche 2 : chaque paquet reçoit une adresse MAC source et destination
- Couche 1 : des bits 0 et 1 voyagent sur le WiFi ou le câble

**Pourquoi c'est crucial en cybersécurité ?**

Chaque attaque cible une couche précise :
- Attaque physique → couche 1 (couper un câble, brouillage WiFi)
- ARP Spoofing → couche 2
- IP Spoofing, DDoS → couche 3
- TCP SYN Flood → couche 4
- DNS Poisoning → couche 7

Quand tu lis un rapport d'attaque et qu'ils disent "layer 7 attack" — tu sais immédiatement que ça vise l'application, pas l'infrastructure.

---

## PARTIE 3 — Le Modèle TCP/IP

En pratique, on utilise TCP/IP — une version simplifiée à **4 couches** :

| TCP/IP | Correspond à OSI |
|--------|-----------------|
| Application | Couches 5, 6, 7 |
| Transport | Couche 4 |
| Internet | Couche 3 |
| Accès réseau | Couches 1, 2 |

C'est ce modèle qui gouverne vraiment Internet.

---

## PARTIE 4 — TCP vs UDP

Ces deux protocoles sont les chevaux de bataille de la couche Transport. Comprendre leur différence c'est fondamental.

### TCP — Transmission Control Protocol

**Caractéristiques :**
- Orienté connexion — il établit une connexion avant d'envoyer
- Fiable — il garantit que tous les paquets arrivent et dans l'ordre
- Plus lent — à cause des vérifications

**Le Three-Way Handshake TCP** — retiens-le par cœur :

```
Client                    Serveur
  |                          |
  |-------- SYN ----------->|   "Je veux me connecter"
  |                          |
  |<------ SYN-ACK ----------|   "D'accord, je suis prêt"
  |                          |
  |-------- ACK ----------->|   "Compris, on commence"
  |                          |
  |====== DONNÉES ==========|
```

**SYN** = Synchronize  
**ACK** = Acknowledge

Ce handshake est la base de :
- L'attaque **SYN Flood** (envoyer des milliers de SYN sans jamais envoyer le ACK final — le serveur s'épuise)
- L'outil **Nmap** qui scanne les ports avec des SYN
- La compréhension des connexions dans Wireshark

**Utilise TCP pour :** HTTP, HTTPS, FTP, SSH, SMTP — tout ce qui doit être fiable.

---

### UDP — User Datagram Protocol

**Caractéristiques :**
- Sans connexion — il envoie sans vérifier
- Non fiable — les paquets peuvent se perdre
- Très rapide — pas de vérification

**Utilise UDP pour :** DNS, streaming vidéo, jeux en ligne, VoIP — tout ce qui préfère la vitesse à la fiabilité.

**En cybersécurité :** beaucoup d'outils OSINT et de scan utilisent UDP. Les attaques DNS Amplification utilisent UDP.

---

## PARTIE 5 — Adressage IP

### IPv4

Une adresse IPv4 c'est **4 octets** séparés par des points :

```
192.168.1.100
```

Chaque nombre va de 0 à 255 (= 8 bits = 1 octet).

**Les plages privées** — à mémoriser absolument :

| Plage | Usage |
|-------|-------|
| 10.0.0.0 — 10.255.255.255 | Réseaux privés (entreprises) |
| 172.16.0.0 — 172.31.255.255 | Réseaux privés (moyen) |
| 192.168.0.0 — 192.168.255.255 | Réseaux domestiques |
| 127.0.0.1 | Loopback — ta propre machine |

Quand tu vois une IP en **192.168.x.x** — c'est une IP locale, pas sur Internet.  
Quand tu vois **10.x.x.x** — idem, réseau interne.  
Une IP publique c'est tout le reste.

**En OSINT :** quand tu trouves une IP en 192.168.x.x dans des métadonnées, ça te dit que le fichier a été créé sur un réseau local — information utile.

---

### Le Masque de Sous-Réseau et CIDR

Le masque définit quelle partie de l'IP est le réseau et quelle partie est la machine.

```
IP      : 192.168.1.100
Masque  : 255.255.255.0
CIDR    : 192.168.1.100/24
```

**/24** signifie que les 24 premiers bits sont le réseau — il reste 8 bits pour les machines, soit **254 machines possibles** (256 - 2 pour broadcast et réseau).

Tableau des CIDR les plus courants :

| CIDR | Masque | Machines dispo |
|------|--------|----------------|
| /24 | 255.255.255.0 | 254 |
| /16 | 255.255.0.0 | 65 534 |
| /8 | 255.0.0.0 | 16 millions |
| /30 | 255.255.255.252 | 2 (liaisons point à point) |
| /32 | 255.255.255.255 | 1 seule machine |

**En pentesting :** quand tu fais un scan réseau, le CIDR te dit combien de machines tu dois scanner. `192.168.1.0/24` = 254 cibles potentielles.

---

### IPv6

Le successeur d'IPv4. Format sur 128 bits en hexadécimal :

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

IPv6 arrive massivement. En OSINT, de plus en plus de cibles ont des IPv6. Commence à les reconnaître.

---

## PARTIE 6 — Les Ports

Un port c'est une porte numérotée sur une machine. L'IP amène le paquet à la bonne machine, le port l'amène au bon programme.

**Les ports fondamentaux à mémoriser :**

| Port | Protocole | Usage |
|------|-----------|-------|
| 21 | FTP | Transfert de fichiers |
| 22 | SSH | Connexion distante sécurisée |
| 23 | Telnet | Connexion distante non sécurisée |
| 25 | SMTP | Envoi d'emails |
| 53 | DNS | Résolution de noms |
| 80 | HTTP | Web non chiffré |
| 110 | POP3 | Réception emails |
| 143 | IMAP | Réception emails |
| 443 | HTTPS | Web chiffré |
| 445 | SMB | Partage fichiers Windows |
| 3306 | MySQL | Base de données |
| 3389 | RDP | Bureau à distance Windows |
| 8080 | HTTP alt | Web alternatif |

**En cybersécurité :**
- Port 22 ouvert = SSH accessible = potentiel brute force
- Port 3389 ouvert = RDP = cible favorite des ransomwares
- Port 445 ouvert = SMB = EternalBlue (WannaCry)
- Port 23 ouvert = Telnet = communication en clair = catastrophe

---

## PARTIE 7 — DNS

Le DNS c'est l'annuaire d'Internet. Il traduit les noms en IP.

```
echats-808c4.web.app  →  DNS  →  142.250.x.x
```

**Les types d'enregistrements DNS :**

| Type | Signification |
|------|---------------|
| A | Nom → IPv4 |
| AAAA | Nom → IPv6 |
| MX | Serveur mail |
| CNAME | Alias vers un autre nom |
| NS | Serveur DNS autoritaire |
| TXT | Texte libre (vérification, SPF) |
| PTR | IPv4 → Nom (reverse DNS) |

**En OSINT :** les enregistrements DNS révèlent l'infrastructure. Un enregistrement MX te dit quel service email ils utilisent. Un CNAME peut révéler un hébergeur. Les sous-domaines peuvent révéler des serveurs cachés.

---

## PARTIE 8 — ARP

ARP = Address Resolution Protocol.

Quand ta machine veut envoyer un paquet à `192.168.1.1`, elle connaît l'IP mais pas l'adresse MAC physique. Elle crie sur le réseau :

> "Qui est 192.168.1.1 ? Donne-moi ton adresse MAC !"

Le routeur répond avec son MAC. Ta machine mémorise ça dans sa **table ARP** (cache ARP).

**En cybersécurité :** l'attaque **ARP Spoofing** consiste à répondre à cette question avant le vrai destinataire :

> "C'est moi 192.168.1.1 ! Mon MAC c'est AA:BB:CC:DD:EE:FF"

Résultat : tout le trafic passe par l'attaquant. C'est la base du **Man-in-the-Middle**.

---

## PARTIE 9 — Ce que voit un vrai analyste réseau

Quand un analyste ouvre Wireshark sur un réseau compromis, voici ce qu'il cherche :

1. **Connexions TCP vers des IPs inconnues** — possible C2 (Command & Control)
2. **Requêtes DNS inhabituelles** — possible DNS tunneling ou exfiltration
3. **ARP anormal** — même IP répondue par deux MAC différentes → ARP Spoofing
4. **SYN sans ACK en masse** → SYN Flood en cours
5. **Trafic sur des ports non standards** — malware qui communique sur port 443 mais c'est pas du HTTPS

Tu vois ? Sans comprendre TCP, ARP, DNS — tu ne peux rien lire dans Wireshark. Maintenant tu peux.

---

## ✅ EXERCICES — Leçon 1

Fais-les tous. Dans l'ordre. Pas de raccourcis.

---

**Exercice 1 — Sans outil, juste ta tête**

Réponds sans chercher, de mémoire :
1. Sur quelle couche OSI travaille IP ?
2. Sur quelle couche travaille Ethernet ?
3. Quel protocole de transport est fiable ?
4. Quel port utilise SSH ?
5. Que signifie /24 en CIDR ?
6. Quelle attaque exploite ARP ?
7. Combien d'étapes dans le TCP handshake ?

---

**Exercice 2 — Calcul réseau**

Pour chaque adresse, dis-moi : IP privée ou publique ? Combien de machines dans le réseau ?

```
a) 192.168.0.50/24
b) 10.0.0.1/8
c) 172.16.5.200/16
d) 8.8.8.8/32
e) 127.0.0.1/8
```

---

**Exercice 3 — Analyse de scénario**

Tu fais une mission OSINT sur une cible. Tu trouves ces infos :

```
IP de connexion : 192.168.1.45
Ports ouverts   : 22, 80, 443, 3389, 445
DNS MX record   : mail.google.com
```

Réponds :
1. Cette IP est-elle sur Internet ? Que ça t'apprend ?
2. Quel port représente le plus grand danger ici et pourquoi ?
3. Quel service email utilise la cible ?
4. Quel port pourrait être vulnérable à EternalBlue ?

---

**Exercice 4 — Reconstituer le handshake**

Remets ces étapes dans le bon ordre :
```
[ ] Le serveur envoie SYN-ACK
[ ] Le client envoie ACK
[ ] La connexion est établie
[ ] Le client envoie SYN
```

---

**Exercice 5 — Pratique Termux**

Dans Termux, tape ces commandes une par une et observe :

```bash
# Voir ta configuration réseau
ifconfig 2>/dev/null || ip addr

# Voir ta table ARP
arp -a 2>/dev/null || ip neigh

# Résoudre un DNS
nslookup google.com

# Voir les connexions actives
netstat -an 2>/dev/null || ss -an

# Ping avec TTL visible
ping -c 4 8.8.8.8
```

Pour chaque commande, note ce que tu vois et essaie de l'interpréter avec ce que tu as appris.

---

**Exercice 6 — Question de réflexion**

Tu reçois un email suspect. L'expéditeur dit être de "echats99@gmail.com" mais tu veux vérifier si c'est vrai. En utilisant uniquement ce que tu as appris sur le DNS et les protocoles email — par où tu commences ton investigation ? Décris ta démarche.

---

## 📌 À retenir absolument de cette leçon

```
OSI = 7 couches (Physical → Application)
TCP/IP = 4 couches pratiques
TCP = fiable + handshake SYN/SYN-ACK/ACK
UDP = rapide + sans vérification
IP privées = 10.x, 172.16-31.x, 192.168.x
/24 = 254 machines, /16 = 65534 machines
DNS = traduit noms en IP
ARP = traduit IP en MAC → vulnérable au spoofing
Ports clés : 22/SSH, 80/HTTP, 443/HTTPS, 3389/RDP, 445/SMB
```

---


## 🧪 Quiz de validation

**Question 1 : Quelle couche OSI est principalement associée à l’adressage IP et au routage?**
- A) Couche 1
- B) Couche 2
- C) Couche 3 ✅
- D) Couche 7

*Explication : la bonne pratique professionnelle est « Couche 3 » — à préciser/enrichir par un relecteur.*

**Question 2 : Quelles sont les étapes du three-way handshake TCP?**
- A) SYN, SYN-ACK, ACK ✅
- B) ACK, FIN, RST
- C) DNS, ARP, ICMP
- D) GET, POST, 200

*Explication : la bonne pratique professionnelle est « SYN, SYN-ACK, ACK » — à préciser/enrichir par un relecteur.*

**Question 3 : Quel énoncé décrit UDP?**
- A) Il garantit chaque livraison
- B) Il évite l’établissement de connexion et privilégie la faible latence ✅
- C) Il chiffre toujours les données
- D) Il remplace toujours TCP

*Explication : la bonne pratique professionnelle est « Il évite l’établissement de connexion et privilégie la faible latence » — à préciser/enrichir par un relecteur.*

**Question 4 : Laquelle est une adresse IPv4 privée?**
- A) 8.8.8.8
- B) 172.20.4.10 ✅
- C) 1.1.1.1
- D) 203.0.113.10

*Explication : la bonne pratique professionnelle est « 172.20.4.10 » — à préciser/enrichir par un relecteur.*

**Question 5 : Que signifie principalement /24 dans 192.168.1.0/24?**
- A) 24 ports
- B) 24 bits de partie réseau ✅
- C) 24 machines exactement
- D) 24 octets

*Explication : la bonne pratique professionnelle est « 24 bits de partie réseau » — à préciser/enrichir par un relecteur.*

**Question 6 : Quel est le rôle principal du DNS?**
- A) Associer des noms à des informations réseau ✅
- B) Chiffrer les fichiers
- C) Remplacer un pare-feu
- D) Attribuer des mots de passe

*Explication : la bonne pratique professionnelle est « Associer des noms à des informations réseau » — à préciser/enrichir par un relecteur.*

**Question 7 : Quel risque est associé à une usurpation ARP?**
- A) Détournement du trafic local ✅
- B) Plus de bande passante
- C) Création d’un domaine public
- D) Conversion de TCP en UDP

*Explication : la bonne pratique professionnelle est « Détournement du trafic local » — à préciser/enrichir par un relecteur.*

**Question 8 : Un port ouvert prouve-t-il une vulnérabilité?**
- A) Oui, toujours
- B) Non, il indique surtout une surface exposée ✅
- C) Oui, si le port est connu
- D) Non, les ports ne concernent pas les services

*Explication : la bonne pratique professionnelle est « Non, il indique surtout une surface exposée » — à préciser/enrichir par un relecteur.*

**Question 9 : Quelle commande observe les sockets locaux en écoute?**
- A) ss -tuln ✅
- B) chmod 777
- C) passwd --delete
- D) ip neigh --flush

*Explication : la bonne pratique professionnelle est « ss -tuln » — à préciser/enrichir par un relecteur.*

**Question 10 : Une analyse professionnelle doit-elle distinguer observation et hypothèse?**
- A) Vrai ✅
- B) Faux

*Explication : la bonne pratique professionnelle est « Vrai » — à préciser/enrichir par un relecteur.*


---

© 2026 ECHATS PRO — Tous droits réservés
