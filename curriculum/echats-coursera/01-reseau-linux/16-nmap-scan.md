---
title: "Scan Réseau avec Nmap"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 16
category: "reseau"
tags: ["nmap", "scan", "ports", "decouverte", "nse", "reconnaissance", "audit"]
prerequisites: ["03-tcp-ip", "04-adressage-ip", "09-firewall", "15-wireshark-analyse"]
learning_objectives:
  - "Expliquer à quoi sert un scan réseau et dans quel cadre légal l'utiliser"
  - "Découvrir les hôtes actifs et scanner des ports avec Nmap"
  - "Identifier les services, versions et systèmes d'exploitation"
  - "Interpréter les résultats et les transformer en recommandations de sécurité"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Scan Réseau avec Nmap

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Expliquer à quoi sert un scan réseau et dans quel cadre légal l'utiliser
- Découvrir les hôtes actifs et scanner des ports avec Nmap
- Identifier les services, versions et systèmes d'exploitation
- Interpréter les résultats et les transformer en recommandations de sécurité

## 📚 Prérequis

- Leçon 03 : *TCP/IP* (ports, handshake)
- Leçon 04 : *Adressage IP* (CIDR)
- Leçon 09 : *Pare-feu*
- Leçon 15 : *Wireshark* (observer un scan côté défenseur)

## 🧭 Introduction

Avant de protéger un réseau, il faut savoir **ce qu'il contient** : quelles machines sont actives, quels services écoutent sur quels ports, quelles versions de logiciels tournent. On ne peut pas défendre ce qu'on ne connaît pas. C'est le rôle de la **découverte réseau** et du **scan de ports**, et l'outil de référence s'appelle **Nmap** (*Network Mapper*).

Créé en 1997 et toujours maintenu, gratuit et open source, Nmap est utilisé par les administrateurs pour faire l'inventaire de leur parc et vérifier que les règles de pare-feu font bien ce qu'on croit, et par les équipes de test d'intrusion pour cartographier la surface d'attaque d'un client. Les attaquants l'utilisent aussi, d'où l'intérêt pour un défenseur de savoir à quoi un scan ressemble dans les journaux.

**Règle d'or de cette leçon : on ne scanne que ce qu'on possède ou ce pour quoi on a une autorisation écrite.** Un scan non autorisé peut constituer une tentative d'intrusion aux yeux de la loi, perturber des services fragiles et te valoir un blocage ou des poursuites. La seule cible publique qui l'autorise explicitement est **scanme.nmap.org**, mise à disposition par le projet Nmap pour les tests (avec modération).

## 📖 Concepts clés

### 1. Les états d'un port

Nmap classe chaque port dans un état :

| État | Signification |
|---|---|
| **open** | Un service écoute et accepte des connexions |
| **closed** | Le port est accessible mais aucun service n'écoute (la machine répond par RST) |
| **filtered** | Un pare-feu ou un filtre bloque, Nmap ne peut pas savoir (pas de réponse) |
| **unfiltered** | Accessible, mais Nmap ne sait pas s'il est ouvert ou fermé (scan ACK) |
| **open\|filtered** | Nmap ne peut pas trancher (courant en UDP) |
| **closed\|filtered** | Idem, entre fermé et filtré |

### 2. Les grandes phases d'un scan

1. **Résolution de noms** (DNS), sauf si désactivée avec `-n`.
2. **Découverte d'hôtes** : quelles machines répondent ?
3. **Scan de ports** : quels ports sont ouverts sur chaque hôte actif ?
4. **Détection de services et de versions** (optionnel).
5. **Détection du système d'exploitation** (optionnel).
6. **Scripts NSE** (optionnel).
7. **Rapport**.

### 3. Spécifier les cibles

```bash
nmap 192.168.1.10                # une machine
nmap scanme.nmap.org             # un nom (cible de test autorisée)
nmap 192.168.1.1-50              # une plage
nmap 192.168.1.0/24              # un sous-réseau (notation CIDR, voir leçon 04)
nmap -iL cibles.txt              # liste dans un fichier
nmap 192.168.1.0/24 --exclude 192.168.1.1   # exclure une machine
```

Savoir lire le **CIDR** (leçon 04) est ici indispensable : `192.168.1.0/24` représente 256 adresses. Une erreur de masque peut te faire scanner bien plus que prévu, donc **hors périmètre autorisé**.

### 4. Découverte d'hôtes (« ping scan »)

```bash
nmap -sn 192.168.1.0/24
```

- `-sn` : découverte uniquement, **sans scan de ports**.
- Sur un réseau local, Nmap utilise **ARP** (très fiable). À distance, il combine ICMP echo, TCP SYN vers le 443, TCP ACK vers le 80, etc.
- Si les machines bloquent les « pings », `-Pn` saute la découverte et considère tous les hôtes comme actifs (plus lent mais utile contre les pare-feu).

### 5. Les principaux types de scan de ports

| Option | Nom | Principe | Remarques |
|---|---|---|---|
| `-sS` | **SYN scan** (« demi-ouverture ») | Envoie un SYN : SYN-ACK = ouvert, RST = fermé. N'achève jamais la poignée de main | Rapide, discret, **nécessite les privilèges root** ; scan par défaut avec root |
| `-sT` | **TCP connect** | Établit une vraie connexion complète avec le système | Sans privilèges ; plus bruyant, mieux journalisé |
| `-sU` | **UDP scan** | Envoie des datagrammes UDP et attend une réponse ou un ICMP « port unreachable » | **Lent** (pas d'accusé de réception) ; nécessaire pour DNS, SNMP, DHCP… |
| `-sA` | **ACK scan** | Cartographie les règles d'un pare-feu (filtré / non filtré) | Ne détermine pas ouvert / fermé |
| `-sV` | Détection de version | Interroge les services pour identifier logiciel et version | Souvent combiné aux autres |
| `-O` | Détection d'OS | Analyse les réponses TCP/IP (empreinte) | Nécessite root |
| `-A` | Scan « agressif » | Combine `-sV`, `-O`, scripts par défaut et traceroute | **Bruyant** ; à réserver aux environnements autorisés |

Par défaut, Nmap scanne les **1000 ports les plus courants**.

### 6. Choisir les ports

```bash
nmap -p 22 192.168.1.10               # un port
nmap -p 22,80,443 192.168.1.10        # plusieurs
nmap -p 1-1024 192.168.1.10           # une plage
nmap -p- 192.168.1.10                 # tous les ports (1-65535)
nmap --top-ports 100 192.168.1.10     # les 100 plus courants
nmap -F 192.168.1.10                  # rapide (100 ports)
nmap -sU -p 53,67,161 192.168.1.10    # ports UDP précis
```

### 7. Détection des services et des versions

```bash
sudo nmap -sV 192.168.1.10
```

Exemple de sortie :

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10
80/tcp   open  http    nginx 1.18.0
3306/tcp open  mysql   MySQL 8.0.36
```

Pourquoi c'est précieux : une version précise permet de la comparer à des bases de **vulnérabilités connues** (CVE, bases d'avis de sécurité) pour savoir si elle doit être mise à jour. **Savoir qu'une version est obsolète n'est pas en exploiter la faille** : dans un audit, on signale et on recommande la correction.

Plus l'intensité de détection est élevée (`--version-intensity 0-9`), plus Nmap envoie de sondes (et plus c'est visible).

### 8. Les scripts NSE (Nmap Scripting Engine)

Nmap embarque des centaines de scripts Lua, classés par catégories : `default`, `safe`, `discovery`, `vuln`, `auth`, `brute`, `intrusive`, etc.

```bash
nmap -sC 192.168.1.10                          # scripts par défaut (catégorie « default »)
nmap --script=banner 192.168.1.10              # récupère les bannières
nmap --script=http-title -p 80,443 192.168.1.10
nmap --script=ssl-cert -p 443 192.168.1.10     # informations du certificat
nmap --script=vuln 192.168.1.10                # contrôle des vulnérabilités connues
nmap --script-help=http-title                  # aide sur un script
```

**Précaution** : certaines catégories (`brute`, `intrusive`, `dos`, `exploit`) peuvent planter un service, générer du bruit ou enfreindre le périmètre autorisé. Utilise-les **seulement si ton autorisation les couvre explicitement**. Commence par `default`, `safe` et `discovery`.

### 9. Performance et discrétion

Nmap propose des profils de vitesse :

| Option | Usage |
|---|---|
| `-T0` à `-T5` | De « paranoïaque » (très lent) à « insensé » (très rapide) |
| `-T3` | Défaut |
| `-T4` | Recommandé sur un réseau local fiable |
| `--min-rate`, `--max-retries` | Réglages fins |

La vitesse maximale peut saturer un réseau fragile, déclencher des alertes ou provoquer des faux résultats. Un **test autorisé** s'accompagne généralement de règles d'engagement précisant les horaires, les plages et les débits permis.

Sur un réseau avec **IDS/IPS** (systèmes de détection), un scan est repéré. Les techniques d'évasion existent (fragmentation, leurres…), mais elles relèvent de tests d'intrusion avancés avec autorisation explicite ; dans cette leçon, on se concentre sur l'usage défensif et l'audit transparent.

### 10. Enregistrer et exploiter les résultats

```bash
nmap -sV 192.168.1.10 -oN resultat.txt       # format normal (lisible)
nmap -sV 192.168.1.10 -oX resultat.xml       # XML (pour outils et rapports)
nmap -sV 192.168.1.10 -oG resultat.gnmap     # « greppable »
nmap -sV 192.168.1.10 -oA resultat           # les trois formats à la fois
```

Autres options utiles : `-v` / `-vv` (plus de détails), `--reason` (pourquoi un port est dans cet état), `--open` (n'afficher que les ports ouverts), `-n` (pas de DNS), `--packet-trace` (voir les paquets envoyés).

### 11. Du résultat à la recommandation

Un scan n'a de valeur que s'il débouche sur une **action**. Exemple de lecture :

| Constat | Risque | Recommandation |
|---|---|---|
| 23/tcp (Telnet) ouvert | Identifiants en clair | Désactiver, utiliser SSH |
| 3389/tcp (RDP) exposé à Internet | Cible d'attaques par force brute et de vulnérabilités | Restreindre par pare-feu/VPN, activer l'authentification forte |
| 3306/tcp (MySQL) ouvert sur Internet | Base de données exposée | Écouter seulement sur `127.0.0.1` ou le LAN, filtrer |
| 80/tcp seul, sans redirection HTTPS | Trafic non chiffré | Mettre en place HTTPS et HSTS |
| Version d'OpenSSH ancienne | Failles connues | Mettre à jour |
| Port inconnu 31337 ouvert | Service non documenté, possible porte dérobée | Identifier le processus, vérifier, fermer |

On compare aussi le résultat à l'**attendu** : « je sais que cette machine ne devrait exposer que 22 et 443 ». Tout écart est une alerte.

### 12. Nmap, légalité et éthique

- **Autorisation écrite** : périmètre (adresses, plages), dates, horaires, types de scans autorisés, contact d'urgence.
- **Proportionnalité** : pas de scan agressif en production sans accord.
- **Confidentialité** : les résultats révèlent la structure d'un réseau ; conserve-les de façon sécurisée.
- **Transparence** : en audit interne, préviens l'équipe pour éviter de déclencher un incident par erreur.
- **Respect des tiers** : ne scanne pas d'adresses publiques « pour voir ». Beaucoup de fournisseurs d'accès considèrent les scans comme un abus et peuvent suspendre un compte.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : ne scanne que **ta machine (127.0.0.1)**, **tes VM**, **ton réseau domestique** (avec l'accord des membres du foyer) ou **scanme.nmap.org** (avec modération : quelques scans, pas de scripts intrusifs). Tout autre scan nécessite une autorisation écrite.

### Exercice 1 — Installer et vérifier

```bash
sudo apt install nmap          # Linux
nmap --version
```

(Windows/macOS : installateur sur nmap.org.)

### Exercice 2 — Scanner ta propre machine

```bash
nmap 127.0.0.1
nmap -p- 127.0.0.1
sudo nmap -sV 127.0.0.1
```

Compare avec :

```bash
ss -tuln
```

Question guidée : les ports que Nmap trouve ouverts correspondent-ils exactement à ceux que `ss` montre en écoute ? Pourquoi ? (Nmap voit ce qui est joignable via l'interface scannée ; `ss` montre tous les services en écoute, y compris ceux liés à une autre interface.)

### Exercice 3 — Découvrir ton réseau domestique

1. Retrouve ton sous-réseau avec `ip -4 addr` (par exemple `192.168.1.25/24`).
2. Lance :

```bash
nmap -sn 192.168.1.0/24
```

3. Dresse l'inventaire : combien d'appareils ? Les reconnais-tu tous (téléphones, TV, box, imprimante) ? **Un appareil inconnu est un point à investiguer** : un voisin connecté sans autorisation ? un objet connecté oublié ?

### Exercice 4 — Scanner ta VM de laboratoire

Sur une VM avec SSH et un serveur web (leçons précédentes) :

```bash
sudo nmap -sS -sV -p- <ip-de-la-vm> -oA scan_vm
cat scan_vm.nmap
```

Pour chaque port ouvert :
1. quel service ? quelle version ?
2. est-il nécessaire ?
3. comment le restreindre (pare-feu, configuration) ?

### Exercice 5 — Observer l'effet du pare-feu

1. Scanne la VM : note les ports ouverts.
2. Sur la VM, active `ufw` et n'autorise que SSH :

```bash
sudo ufw default deny incoming
sudo ufw allow 22/tcp
sudo ufw enable
```

3. Rescanne : les ports bloqués apparaissent comme **filtered** (si DROP) ou **closed** (si REJECT).
4. Utilise `--reason` pour voir le motif :

```bash
sudo nmap -sS --reason -p 22,80,443 <ip-de-la-vm>
```

### Exercice 6 — Voir ton scan côté défenseur

1. Lance Wireshark ou `tcpdump` **sur la VM cible**.
2. Depuis ta machine : `sudo nmap -sS <ip-de-la-vm>`, puis `nmap -sT <ip-de-la-vm>`.
3. Compare les paquets : le SYN scan envoie un SYN, reçoit un SYN-ACK, puis envoie un RST (pas de connexion complète) ; le connect scan termine la poignée de main et peut laisser une trace dans les journaux de l'application.

### Exercice 7 — Scripts NSE sur ta VM

```bash
nmap -sC -p 22,80 <ip-de-la-vm>
nmap --script=http-title,http-headers -p 80 <ip-de-la-vm>
nmap --script=ssh2-enum-algos -p 22 <ip-de-la-vm>
```

Observe : titres de pages, en-têtes HTTP, algorithmes de chiffrement offerts par SSH. Repère les éventuels algorithmes obsolètes à désactiver.

### Exercice 8 — Cible de test officielle

```bash
nmap -F scanme.nmap.org
nmap -sV -p 22,80,9929,31337 scanme.nmap.org
```

Reste raisonnable : quelques scans, aucun script intrusif ni force brute.

### Exercice 9 — Mini-rapport

À partir de l'exercice 4, rédige un rapport de 10 lignes :
1. périmètre scanné et date ;
2. commandes utilisées ;
3. services exposés ;
4. écarts par rapport à l'attendu ;
5. trois recommandations priorisées.

Un bon rapport est **factuel**, **reproductible** et **orienté action**.

## 🔍 Approfondissement

### Pour aller plus loin

- *Nmap Network Scanning*, le livre officiel de Gordon « Fyodor » Lyon (gratuit en ligne sur nmap.org).
- Le module « Nmap » de TryHackMe et les salles « Network Services ».
- La documentation NSE : nmap.org/nsedoc.

### Pièges courants

- ❌ **Erreur fréquente 1** : scanner un réseau sans autorisation « juste pour voir ».
- ✅ **Bonne pratique** : autorisation écrite, périmètre défini, ou environnement personnel.
- ❌ **Erreur fréquente 2** : faire confiance à un seul résultat. Un hôte « down » peut simplement bloquer les pings.
- ✅ **Bonne pratique** : recouper avec `-Pn`, un autre type de scan, ou un inventaire officiel.
- ❌ **Erreur fréquente 3** : lancer `-A -T5 -p-` sur toute une plage en production.
- ✅ **Bonne pratique** : adapter profondeur et vitesse, tester d'abord sur un échantillon.
- ❌ **Erreur fréquente 4** : confondre « port filtered » et « port fermé ».
- ✅ **Bonne pratique** : filtered = un équipement bloque ou ne répond pas ; closed = la machine répond qu'aucun service n'écoute.
- ❌ **Erreur fréquente 5** : oublier l'UDP, où se cachent DNS, SNMP et d'autres services sensibles.
- ✅ **Bonne pratique** : scanner au moins les ports UDP importants (`-sU --top-ports 50`).

## 🧪 Quiz de validation

**Question 1 : Que signifie l'état « filtered » pour un port dans Nmap ?**
- A) Le port est ouvert
- B) Le port est fermé avec un RST
- C) Un pare-feu ou filtre empêche de déterminer s'il est ouvert ✅
- D) Le port est chiffré

*Explication : filtered indique l'absence de réponse exploitable, généralement à cause d'un pare-feu.*

**Question 2 : Quelle option réalise la découverte d'hôtes sans scan de ports ?**
- A) `-sS`
- B) `-sn` ✅
- C) `-sV`
- D) `-p-`

*Explication : `-sn` vérifie quelles machines sont actives, sans tester leurs ports.*

**Question 3 : Quelle option identifie les logiciels et leurs versions sur les ports ouverts ?**
- A) `-sU`
- B) `-O`
- C) `-sV` ✅
- D) `-Pn`

*Explication : `-sV` interroge les services pour déterminer le logiciel et sa version.*

**Question 4 : Dans quel cas est-il légal de scanner un réseau avec Nmap ?**
- A) Quand on est curieux
- B) Quand on possède le réseau ou qu'on a une autorisation écrite ✅
- C) Quand le scan est rapide
- D) Quand on utilise le mode `-T0`

*Explication : l'autorisation et le périmètre définis sont la condition de légalité, quelle que soit la technique.*

**Question 5 : Quel avantage a le SYN scan (`-sS`) par rapport au TCP connect (`-sT`) ?**
- A) Il ne nécessite aucun privilège
- B) Il n'établit pas de connexion complète, il est plus rapide et laisse moins de traces applicatives ✅
- C) Il chiffre les paquets
- D) Il scanne l'UDP

*Explication : le SYN scan envoie un SYN puis un RST sans finir la poignée de main ; il demande en revanche les droits root.*

## 📝 Résumé

- Nmap cartographie un réseau : hôtes actifs, ports ouverts, services, versions, OS.
- Les états de port (open, closed, filtered…) renseignent sur les services et les filtrages en place.
- `-sn` découvre les hôtes, `-sS`/`-sT`/`-sU` scannent les ports, `-sV` identifie les versions, `-sC` et `--script` lancent des scripts NSE.
- Les résultats s'enregistrent en `-oN`, `-oX`, `-oG` ou `-oA` et se traduisent en recommandations concrètes.
- Un scan se voit dans les journaux et les captures : le comprendre aide les défenseurs.
- Le cadre légal prime : propriété ou autorisation écrite, périmètre défini, débit et intensité adaptés.

## 🎓 Ce que tu as appris

✅ Découvrir hôtes et services sur un réseau autorisé
✅ Choisir le bon type de scan selon l'objectif
✅ Lire les états de ports et en tirer des recommandations
✅ Rédiger un mini-rapport factuel et exploitable

## 🏁 Fin du module 01

Tu as terminé le module **Réseau & Linux** : modèles OSI et TCP/IP, adressage, DNS, HTTP/HTTPS, routage, commutation et VLAN, pare-feu, ligne de commande Linux, permissions, systemd, Bash, SSH, Wireshark et Nmap. Tu disposes maintenant du socle pour aborder les modules suivants.

## ➡️ Module suivant

**Module 02 : Python & OSINT**, en commençant par *01 : Introduction à Python* (fichier `02-python-osint/01-introduction-python.md`).

---

© 2026 ECHATS PRO — Tous droits réservés
