---
title: "Le Pare-feu (Firewall)"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 35
order: 9
category: "reseau"
tags: ["reseau", "firewall", "pare-feu", "iptables", "ufw", "filtrage", "dmz"]
prerequisites: ["03-tcp-ip", "04-adressage-ip"]
learning_objectives:
  - "Expliquer le rôle et les types de pare-feu"
  - "Écrire et lire des règles de filtrage simples"
  - "Comprendre le filtrage avec état et les zones de sécurité"
  - "Configurer un pare-feu local avec ufw ou iptables"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Le Pare-feu (Firewall)

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Expliquer le rôle et les types de pare-feu
- Écrire et lire des règles de filtrage simples
- Comprendre le filtrage avec état et les zones de sécurité
- Configurer un pare-feu local avec `ufw` ou `iptables`

## 📚 Prérequis

- Leçon 03 : *TCP/IP* (ports, TCP, UDP)
- Leçon 04 : *Adressage IP et Sous-réseaux*

## 🧭 Introduction

Un immeuble sécurisé a un gardien à l'entrée : il vérifie qui entre, qui sort, et refuse ceux qui n'ont rien à y faire. Un **pare-feu** (*firewall*) joue ce rôle pour un réseau ou un ordinateur. Il examine le trafic qui passe et décide, selon des **règles**, de l'autoriser ou de le bloquer.

Le pare-feu est l'un des piliers les plus anciens de la sécurité informatique, et il reste indispensable. Il réduit la **surface d'attaque** : un service que personne ne peut joindre depuis l'extérieur est beaucoup plus difficile à attaquer. Beaucoup d'incidents proviennent de services exposés par erreur à Internet (bases de données, bureau à distance) qu'un simple filtrage aurait protégés.

Dans cette leçon, tu apprendras comment un pare-feu raisonne, comment écrire des règles propres, et comment appliquer le **principe du moindre privilège** : n'autoriser que ce qui est nécessaire, interdire tout le reste.

## 📖 Concepts clés

### 1. Que fait un pare-feu ?

Il inspecte chaque paquet ou connexion et applique une **action** selon des critères :

| Critère | Exemple |
|---|---|
| Adresse IP source | `203.0.113.5` |
| Adresse IP destination | `192.168.10.20` |
| Protocole | TCP, UDP, ICMP |
| Port source / destination | 22, 80, 443 |
| Interface | `eth0` (externe), `eth1` (interne) |
| Direction | entrant (*inbound*), sortant (*outbound*) |
| État de la connexion | nouvelle, établie |

Actions possibles :
- **ACCEPT / ALLOW** : laisser passer ;
- **DROP** : jeter silencieusement (l'émetteur ne reçoit rien) ;
- **REJECT** : refuser en avertissant l'émetteur ;
- **LOG** : journaliser.

`DROP` rend les scans plus lents et moins informatifs pour l'attaquant, `REJECT` facilite le diagnostic en interne. Le choix dépend du contexte.

### 2. Les grandes familles de pare-feu

| Type | Niveau | Principe |
|---|---|---|
| **Filtrage de paquets (sans état)** | Couches 3-4 | Examine chaque paquet isolément (IP, port). Rapide, mais ne comprend pas la notion de connexion |
| **Filtrage avec état (*stateful*)** | Couches 3-4 | Suit les connexions : une réponse à une requête sortante est automatiquement autorisée |
| **Proxy / passerelle applicative** | Couche 7 | S'interpose entre client et serveur, comprend le protocole (HTTP, FTP…) |
| **Pare-feu nouvelle génération (NGFW)** | Couches 3-7 | Ajoute inspection applicative, détection d'intrusion, filtrage par utilisateur et par application |
| **WAF (Web Application Firewall)** | Couche 7 | Protège spécifiquement les applications web (filtre injections, XSS…) |

On distingue aussi :
- **pare-feu réseau** : équipement placé entre deux réseaux ;
- **pare-feu personnel (hôte)** : logiciel sur chaque machine (pare-feu Windows, `ufw`, `iptables`/`nftables`).

### 3. Filtrage avec état : pourquoi c'est important

Sans état, pour autoriser la navigation web, il faudrait ouvrir tous les ports hauts en entrée pour laisser revenir les réponses. Un pare-feu **stateful** garde en mémoire une **table de connexions** :

1. Ton PC envoie un SYN vers `203.0.113.10:443` → le pare-feu note la connexion (état **NEW**).
2. La réponse revient → le pare-feu la reconnaît (état **ESTABLISHED**) et l'autorise automatiquement.
3. Un paquet entrant **non sollicité** qui ne correspond à aucune connexion connue est bloqué.

Résultat : la règle « tout ce qui est initié depuis l'intérieur est autorisé, les connexions initiées depuis l'extérieur sont bloquées » protège les postes de travail sans gêner la navigation.

### 4. Politique par défaut : refuser par défaut

Deux philosophies :
- **Liste blanche** (*default deny*) : on bloque tout, puis on autorise explicitement ce qui est nécessaire. **C'est la bonne pratique.**
- **Liste noire** (*default allow*) : on autorise tout, puis on bloque ce qui est dangereux. Trop fragile, on oublie toujours quelque chose.

### 5. L'ordre des règles compte

Les règles sont évaluées **de haut en bas**, la **première qui correspond** s'applique.

```
1. ACCEPT  tcp  depuis 10.0.0.0/24 vers port 22      (SSH depuis l'admin)
2. DROP    tcp  depuis n'importe où vers port 22     (SSH interdit aux autres)
3. ACCEPT  tcp  vers port 443                          (HTTPS public)
4. DROP    tout le reste                               (politique par défaut)
```

Si on inverse les règles 1 et 2, personne ne pourrait plus se connecter en SSH, même l'administrateur. Une **règle trop large placée trop haut** masque les règles suivantes : c'est une erreur classique.

### 6. Zones de sécurité et DMZ

Un pare-feu d'entreprise sépare plusieurs **zones** de confiance différente :

```
Internet (non fiable)
     │
 [Pare-feu]──── DMZ (serveurs publics : web, mail)
     │
 Réseau interne (confiance élevée)
```

- **Zone externe (WAN)** : Internet, non fiable.
- **DMZ** (*zone démilitarisée*) : héberge les serveurs accessibles depuis Internet. Si un serveur y est compromis, l'attaquant ne se retrouve pas directement dans le réseau interne.
- **Zone interne (LAN)** : postes et serveurs internes.

Règles typiques :
- Internet → DMZ : autorisé seulement sur les ports publics (80, 443).
- Internet → LAN : **interdit**.
- DMZ → LAN : très restreint (par exemple seulement vers une base de données précise).
- LAN → Internet : autorisé, filtré et journalisé.

### 7. Ce que le pare-feu ne fait pas

- Il ne protège pas contre une **faille dans un service autorisé** (une injection SQL passe par le port 443, donc passe le pare-feu classique).
- Il ne détecte pas un **malware** déjà présent sur un poste interne qui communique via des ports autorisés.
- Il ne voit pas **le trafic chiffré** (sans inspection TLS).
- Il ne remplace pas les mises à jour, l'authentification forte ou la surveillance.

Le pare-feu est **une couche** dans une **défense en profondeur**.

### 8. Pare-feu sous Linux : ufw, iptables, nftables

Linux filtre le trafic dans le noyau avec **netfilter**, piloté par :
- **iptables** : outil historique, règles par chaînes (`INPUT`, `OUTPUT`, `FORWARD`) ;
- **nftables** : successeur moderne d'iptables ;
- **ufw** (*Uncomplicated Firewall*) : interface simplifiée, idéale pour débuter.

Chaînes principales d'iptables :

| Chaîne | Trafic concerné |
|---|---|
| INPUT | Entrant vers la machine elle-même |
| OUTPUT | Sortant de la machine |
| FORWARD | Traversant la machine (si elle sert de routeur) |

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : applique ces règles uniquement sur **ta propre machine ou une machine virtuelle de test**. Attention : une mauvaise règle peut te couper l'accès **SSH** à un serveur distant. Ne teste jamais sur un serveur de production sans accès console de secours.

### Exercice 1 — Pare-feu simple avec ufw (Linux/Debian/Ubuntu)

```bash
# Voir l'état
sudo ufw status verbose

# Politique par défaut : tout entrant refusé, tout sortant autorisé
sudo ufw default deny incoming
sudo ufw default allow outgoing

# IMPORTANT : autoriser SSH AVANT d'activer le pare-feu si tu es connecté à distance
sudo ufw allow 22/tcp

# Autoriser le web
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Activer
sudo ufw enable
sudo ufw status numbered
```

Questions guidées :
1. Quelle est la politique par défaut en entrée ? (refuser)
2. Que se passerait-il si tu avais activé ufw sans autoriser le port 22 sur un serveur distant ? (tu perdrais l'accès)

### Exercice 2 — Règles plus précises avec ufw

```bash
# Autoriser SSH uniquement depuis une adresse précise
sudo ufw allow from 192.168.1.50 to any port 22 proto tcp

# Bloquer une adresse
sudo ufw deny from 203.0.113.99

# Limiter les tentatives de connexion SSH (protection contre le forçage)
sudo ufw limit 22/tcp

# Supprimer une règle par son numéro
sudo ufw delete 3
```

### Exercice 3 — Écrire des règles iptables

```bash
# Voir les règles actuelles
sudo iptables -L -n -v --line-numbers

# Autoriser le trafic local (boucle locale)
sudo iptables -A INPUT -i lo -j ACCEPT

# Autoriser les réponses aux connexions déjà établies
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Autoriser SSH et HTTPS en entrée
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Politique par défaut : tout le reste est refusé en entrée
sudo iptables -P INPUT DROP
```

Explication ligne par ligne :
- `-A INPUT` : ajoute une règle à la chaîne INPUT ;
- `-p tcp --dport 22` : protocole TCP, port de destination 22 ;
- `-j ACCEPT` : action à appliquer ;
- `-P INPUT DROP` : politique par défaut de la chaîne.

Pour **ne pas perdre** ces règles au redémarrage, il faut les sauvegarder (par exemple avec `iptables-persistent` sous Debian/Ubuntu).

### Exercice 4 — Pare-feu Windows

1. Ouvre « Pare-feu Windows Defender avec fonctions avancées de sécurité ».
2. Regarde les **règles de trafic entrant** : lesquelles sont activées ?
3. Crée une règle bloquant le trafic entrant sur le port TCP 3389 (bureau à distance) si tu ne l'utilises pas.

En ligne de commande (PowerShell en administrateur) :

```powershell
Get-NetFirewallProfile | Select Name, Enabled
New-NetFirewallRule -DisplayName "Bloquer RDP" -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Block
```

### Exercice 5 — Vérifier l'effet de tes règles

Depuis **une deuxième machine à toi** (ou une VM), teste :

```bash
nc -zv <ip-de-ta-machine> 22
nc -zv <ip-de-ta-machine> 8080
```

- Un port autorisé répond « succeeded ».
- Un port bloqué par `DROP` expire (timeout) ; par `REJECT`, il répond « refused ».

Tu observes concrètement la différence entre DROP et REJECT.

### Exercice 6 — Concevoir une politique (papier-crayon)

Une PME congolaise a :
- un serveur web public ;
- un serveur de fichiers interne ;
- des postes de bureau.

Écris les règles (zones : Internet, DMZ, LAN) en indiquant l'action et la justification pour : Internet → serveur web, Internet → serveur de fichiers, LAN → Internet, LAN → serveur web (administration), DMZ → LAN.

**Corrigé possible :** Internet → web : autoriser 80/443 ; Internet → fichiers : interdire ; LAN → Internet : autoriser, journaliser ; LAN → web : autoriser l'admin depuis un poste précis ; DMZ → LAN : interdire par défaut.

## 🔍 Approfondissement

### Pour aller plus loin

- Documentation officielle de `ufw` et de `nftables`.
- Guides de l'ANSSI sur la configuration de pare-feu.
- Module « Firewalls » de TryHackMe (« Network Security »).

### Pièges courants

- ❌ **Erreur fréquente 1** : activer un pare-feu à distance sans autoriser SSH et se couper l'accès.
- ✅ **Bonne pratique** : toujours avoir un accès de secours (console) et autoriser SSH d'abord.
- ❌ **Erreur fréquente 2** : empiler des règles « ACCEPT any » « temporaires » qui restent des années.
- ✅ **Bonne pratique** : documenter chaque règle, ajouter une date et un responsable, et auditer régulièrement.
- ❌ **Erreur fréquente 3** : ne filtrer que le trafic entrant. Le trafic **sortant** non contrôlé permet à un malware de joindre son serveur de commande.
- ✅ **Bonne pratique** : filtrer aussi la sortie dans les environnements sensibles.
- ❌ **Erreur fréquente 4** : croire qu'un pare-feu suffit.
- ✅ **Bonne pratique** : l'associer à des mises à jour, à la segmentation, à la journalisation et à la surveillance.

## 🧪 Quiz de validation

**Question 1 : Quelle approche est recommandée pour un pare-feu ?**
- A) Tout autoriser puis bloquer ce qui est dangereux
- B) Tout bloquer par défaut puis autoriser le nécessaire ✅
- C) Ne rien filtrer en sortie
- D) Désactiver le pare-feu sur le réseau interne

*Explication : la politique « refuser par défaut » applique le moindre privilège et limite la surface d'attaque.*

**Question 2 : Qu'apporte un pare-feu avec état (stateful) ?**
- A) Il chiffre le trafic
- B) Il suit les connexions et autorise automatiquement les réponses légitimes ✅
- C) Il remplace l'antivirus
- D) Il attribue les adresses IP

*Explication : il mémorise les connexions initiées de l'intérieur et laisse revenir les réponses correspondantes.*

**Question 3 : Quelle est la différence entre DROP et REJECT ?**
- A) DROP jette silencieusement le paquet, REJECT prévient l'émetteur ✅
- B) DROP autorise, REJECT bloque
- C) Il n'y en a aucune
- D) REJECT chiffre le paquet

*Explication : avec DROP l'émetteur n'a aucune réponse (timeout), avec REJECT il reçoit un refus explicite.*

**Question 4 : Qu'est-ce qu'une DMZ ?**
- A) Une zone intermédiaire hébergeant les serveurs accessibles depuis Internet ✅
- B) Un type de câble
- C) Un protocole de routage
- D) Un antivirus réseau

*Explication : la DMZ isole les serveurs publics du réseau interne pour limiter les dégâts en cas de compromission.*

**Question 5 : Un pare-feu classique bloque-t-il une injection SQL envoyée sur le port 443 ?**
- A) Oui, toujours
- B) Non, le trafic vers un port autorisé passe ; il faut un WAF et du code sécurisé ✅
- C) Oui, s'il est stateful
- D) Seulement si le port est 80

*Explication : le pare-feu réseau filtre selon IP et ports, il ne comprend pas le contenu applicatif.*

## 📝 Résumé

- Un pare-feu filtre le trafic selon des règles (IP, ports, protocole, état, interface).
- Le filtrage avec état suit les connexions et simplifie la protection des postes.
- La bonne pratique est « refuser par défaut, autoriser le nécessaire », avec des règles ordonnées avec soin.
- Les zones (LAN, DMZ, Internet) permettent de cloisonner les serveurs selon leur exposition.
- `ufw`, `iptables`/`nftables` et le pare-feu Windows permettent de filtrer sur chaque machine.
- Un pare-feu ne remplace pas la sécurité applicative ni la surveillance : il est une couche parmi d'autres.

## 🎓 Ce que tu as appris

✅ Décrire les types de pare-feu et le filtrage avec état
✅ Écrire des règles ufw et iptables simples
✅ Concevoir une politique de filtrage avec zones
✅ Reconnaître les limites d'un pare-feu

## ➡️ Leçon suivante

**10 : Commandes Linux essentielles** : naviguer dans le système, manipuler fichiers et texte, enchaîner les commandes. Fichier : `10-commandes-linux-essentielles.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
