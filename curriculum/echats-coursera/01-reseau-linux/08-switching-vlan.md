---
title: "Switching et VLAN"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 30
order: 8
category: "reseau"
tags: ["reseau", "switch", "vlan", "mac", "arp", "couche-2", "segmentation"]
prerequisites: ["02-modele-osi", "04-adressage-ip"]
learning_objectives:
  - "Expliquer le fonctionnement d'un switch et de sa table MAC"
  - "Décrire le rôle du protocole ARP"
  - "Comprendre les VLAN et la segmentation réseau"
  - "Identifier les attaques de couche 2 et leurs protections"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Switching et VLAN

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Expliquer le fonctionnement d'un switch et de sa table MAC
- Décrire le rôle du protocole ARP
- Comprendre les VLAN et la segmentation réseau
- Identifier les attaques de couche 2 et leurs protections

## 📚 Prérequis

- Leçon 02 : *Le Modèle OSI* (couche 2, trames, adresses MAC)
- Leçon 04 : *Adressage IP et Sous-réseaux*

## 🧭 Introduction

Dans la leçon précédente, tu as vu comment les routeurs relient des réseaux entre eux. Mais **à l'intérieur** d'un réseau local (le bureau d'une banque, la salle d'un cybercafé, le campus d'une université), qui se charge de livrer chaque trame à la bonne machine ? C'est le rôle du **switch** (commutateur), un équipement de **couche 2**.

Le switch est partout : dans les entreprises, les data centers, les écoles. C'est aussi un point sensible. Beaucoup d'attaques internes (écoute du trafic, usurpation d'identité réseau, mouvement latéral d'un attaquant) reposent sur des faiblesses de la couche 2. Et l'une des meilleures défenses d'un réseau d'entreprise, la **segmentation par VLAN**, se met en œuvre justement sur les switchs.

Cette leçon t'explique comment ils fonctionnent, pourquoi on les segmente, et comment les attaquants et les défenseurs s'affrontent à ce niveau.

## 📖 Concepts clés

### 1. Hub, switch : l'évolution

Un **hub** (concentrateur) est un équipement de couche 1 : il répète tout signal reçu sur **tous** ses ports. Résultat : toutes les machines voient tout le trafic, et les collisions sont fréquentes. Il est obsolète et dangereux (n'importe qui peut écouter).

Un **switch** est plus malin : il apprend **quelle machine est sur quel port** et envoie chaque trame **uniquement** vers le port concerné. Analogie : le hub est un haut-parleur qui crie le message à toute la salle ; le switch est un standardiste qui connecte directement les deux interlocuteurs.

### 2. La table MAC (CAM)

Un switch construit une **table d'adresses MAC** en observant les trames :

1. Une trame arrive sur le port 3 avec l'adresse MAC source `AA:AA:AA:AA:AA:AA`.
2. Le switch note : « `AA:AA…` est sur le port 3 ».
3. Pour une trame à destination de `BB:BB…` :
   - s'il connaît le port de `BB:BB…` → il envoie **uniquement** vers ce port (**commutation**) ;
   - s'il ne le connaît pas → il envoie sur **tous les ports sauf celui d'origine** (**inondation**, *flooding*), puis apprend la réponse.

| Port | Adresse MAC apprise |
|---|---|
| 1 | AA:AA:AA:AA:AA:AA |
| 2 | BB:BB:BB:BB:BB:BB |
| 3 | CC:CC:CC:CC:CC:CC |

Les entrées expirent après quelques minutes d'inactivité (*aging*).

### 3. Domaines de collision et de diffusion

- **Domaine de collision** : zone où deux émetteurs peuvent se gêner. Chaque port d'un switch forme son propre domaine de collision.
- **Domaine de diffusion** (*broadcast domain*) : zone atteinte par un message envoyé à tous (broadcast). Un switch **ne sépare pas** les diffusions : tous ses ports (sans VLAN) sont dans le même domaine. C'est un **routeur** (ou un VLAN) qui les sépare.

Plus un domaine de diffusion est grand, plus il y a de bruit, de ralentissement et de surface d'attaque.

### 4. ARP : retrouver la MAC à partir de l'IP

Pour envoyer une trame, ta machine doit connaître l'adresse **MAC** de la destination dans le réseau local. Or elle ne connaît que son **adresse IP**. Le protocole **ARP** (*Address Resolution Protocol*) fait le lien :

1. Ta machine (`192.168.1.25`) veut joindre `192.168.1.1`.
2. Elle diffuse : « **Qui a l'adresse 192.168.1.1 ?** » (ARP Request, envoyée à tous).
3. Le routeur répond : « **C'est moi, ma MAC est `11:22:33:44:55:66`.** » (ARP Reply, envoyée directement).
4. Ta machine mémorise l'association dans son **cache ARP**.

ARP **n'a aucune authentification** : n'importe quelle machine peut répondre, même à tort. C'est la faiblesse exploitée par l'attaque la plus célèbre de couche 2 (voir plus bas).

### 5. Les VLAN : segmenter virtuellement

Un **VLAN** (*Virtual LAN*) découpe **logiquement** un switch en plusieurs réseaux séparés. Les machines d'un même VLAN communiquent directement ; pour communiquer avec un autre VLAN, il faut passer par un routeur (ou un switch de niveau 3).

Exemple dans une banque :

| VLAN | Usage | Sous-réseau |
|---|---|---|
| 10 | Direction | 192.168.10.0/24 |
| 20 | Comptabilité | 192.168.20.0/24 |
| 30 | Caisses / agences | 192.168.30.0/24 |
| 40 | Wi-Fi invités | 192.168.40.0/24 |
| 99 | Administration des équipements | 192.168.99.0/24 |

**Avantages :**
- **Sécurité** : un poste compromis dans le VLAN « invités » ne voit pas le trafic de la comptabilité.
- **Performance** : domaines de diffusion plus petits.
- **Souplesse** : on regroupe les utilisateurs par fonction, pas par emplacement physique.
- **Conformité** : isoler les systèmes de paiement ou de données sensibles est souvent exigé par les normes.

### 6. Ports d'accès et ports « trunk »

- **Port d'accès** (*access*) : appartient à **un seul VLAN**. On y branche un PC, une imprimante, un téléphone.
- **Port trunk** : transporte **plusieurs VLAN** sur un même lien (entre deux switchs, ou entre un switch et un routeur). Les trames sont alors **étiquetées** (*tagged*) avec le numéro de VLAN, selon la norme **802.1Q**.

```
PC (VLAN 10) ─┐                          ┌─ PC (VLAN 10)
PC (VLAN 20) ─┤ Switch A ══ trunk ══ Switch B ├─ PC (VLAN 20)
PC (VLAN 30) ─┘   (VLAN 10, 20, 30)      └─ PC (VLAN 30)
```

Le **VLAN natif** est le VLAN dont les trames circulent **sans étiquette** sur un trunk : une mauvaise configuration à ce niveau est exploitable (voir plus bas).

### 7. Attaques de couche 2

| Attaque | Principe | Protection |
|---|---|---|
| **ARP spoofing / poisoning** | Un attaquant envoie de fausses réponses ARP pour se faire passer pour la passerelle. Le trafic des victimes passe par lui (attaque de l'homme du milieu) | *Dynamic ARP Inspection* (DAI), tables ARP statiques sur équipements critiques, chiffrement (HTTPS, VPN) |
| **MAC flooding** | Saturer la table MAC du switch avec de fausses adresses : le switch se met à inonder tous les ports et se comporte comme un hub | *Port security* (limiter le nombre de MAC par port) |
| **MAC spoofing** | Usurper l'adresse MAC d'une machine autorisée | Port security, authentification 802.1X |
| **VLAN hopping** | Passer d'un VLAN à un autre en abusant du trunk (négociation automatique, double étiquetage) | Désactiver la négociation de trunk, ne pas utiliser le VLAN 1/natif pour les utilisateurs, ports inutilisés en arrêt |
| **Faux serveur DHCP** | Une machine distribue de mauvaises passerelles/DNS | *DHCP snooping* |
| **Attaque sur STP** | Se faire élire « racine » de l'arbre de recouvrement pour détourner le trafic | *BPDU guard*, *root guard* |

**Bonnes pratiques de durcissement d'un switch :**
- désactiver les ports inutilisés et les placer dans un VLAN « poubelle » ;
- activer **port security** et **DHCP snooping** ;
- utiliser **802.1X** pour authentifier les équipements qui se connectent ;
- changer les mots de passe par défaut ; administrer via **SSH**, jamais Telnet ;
- mettre l'administration dans un VLAN dédié ;
- sauvegarder et versionner les configurations.

### 8. Le chiffrement comme filet de sécurité

Même si une attaque de couche 2 réussit, **le chiffrement de bout en bout** (HTTPS, SSH, VPN) limite fortement les dégâts : l'attaquant voit passer des données qu'il ne peut pas lire. C'est pourquoi la sécurité se pense **en couches**, sans dépendre d'une seule protection.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : dans cette leçon, tu observes **ta propre machine** et **ton propre réseau domestique**. Les attaques de couche 2 (ARP spoofing, MAC flooding…) ne se testent **que dans un laboratoire isolé que tu possèdes** (machines virtuelles), jamais sur un réseau d'école, d'entreprise ou public. Elles perturbent le réseau et sont illégales sans autorisation.

### Exercice 1 — Consulter ton cache ARP

```bash
# Windows, Linux, macOS
arp -a
```

Tu obtiens des paires adresse IP ↔ adresse MAC. Repère :
1. la ligne de ta **passerelle** (par exemple `192.168.1.1`) ;
2. les autres appareils de ton réseau (téléphone, TV…).

Note la MAC de ta passerelle : dans l'exercice 3, tu vérifieras qu'elle ne change pas.

### Exercice 2 — Observer ARP dans Wireshark

1. Lance Wireshark sur ton interface, filtre : `arp`.
2. Supprime l'entrée de ta passerelle dans le cache :
   ```bash
   # Linux (adapte l'IP)
   sudo ip neigh flush all
   # Windows (en administrateur)
   arp -d *
   ```
3. Envoie un ping vers ta passerelle : `ping 192.168.1.1`.
4. Dans Wireshark, repère le couple :
   - `Who has 192.168.1.1? Tell 192.168.1.25` (requête, diffusée) ;
   - `192.168.1.1 is at 11:22:...` (réponse).

Tu viens de voir la résolution ARP en direct.

### Exercice 3 — Détecter une anomalie ARP

Un signe d'empoisonnement ARP : **deux adresses IP différentes qui partagent la même adresse MAC** dans le cache, ou la **MAC de la passerelle qui change**. Compare :

```bash
arp -a
```

Dans un réseau sain, chaque IP a sa MAC propre et celle de la passerelle reste stable. Note tes observations : c'est la base d'une détection simple.

### Exercice 4 — Concevoir une segmentation (papier-crayon)

Une école de formation en informatique a :
- une salle de cours (30 postes) ;
- le bureau de l'administration (5 postes, données élèves) ;
- le Wi-Fi des étudiants ;
- un serveur de notes.

Propose : combien de VLAN, quels noms, quels sous-réseaux, et quelles communications autoriser.

**Corrigé possible :**

| VLAN | Usage | Sous-réseau | Règle |
|---|---|---|---|
| 10 | Salle de cours | 192.168.10.0/24 | Accès Internet, accès limité au serveur de notes (lecture) |
| 20 | Administration | 192.168.20.0/27 | Accès au serveur de notes, accès Internet |
| 30 | Wi-Fi étudiants | 192.168.30.0/24 | Internet seulement, aucun accès aux autres VLAN |
| 40 | Serveurs | 192.168.40.0/28 | Accepte uniquement les flux nécessaires, journalisés |

Principe appliqué : **moindre privilège** et **cloisonnement**.

### Exercice 5 — Simulation de VLAN en laboratoire (facultatif)

Avec **Cisco Packet Tracer** (gratuit) ou **GNS3** :
1. Place un switch et quatre PC.
2. Crée deux VLAN (10 et 20) et affecte deux PC à chacun.
3. Teste : `ping` entre PC du **même** VLAN réussit ; entre VLAN **différents** échoue.
4. Ajoute un routeur (ou un switch L3) pour autoriser la communication inter-VLAN, puis restreins-la avec une liste de contrôle d'accès.

Exemple de configuration simplifiée de port d'accès sur un switch Cisco :

```
Switch(config)# vlan 10
Switch(config-vlan)# name COMPTA
Switch(config)# interface fastEthernet 0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
```

## 🔍 Approfondissement

### Pour aller plus loin

- Cisco Packet Tracer et les cours gratuits « Networking Essentials » de Cisco Networking Academy.
- Norme IEEE 802.1Q (VLAN) et 802.1X (authentification de port).
- Guides de durcissement de switchs publiés par l'ANSSI et par les constructeurs.

### Pièges courants

- ❌ **Erreur fréquente 1** : croire qu'un switch protège contre l'écoute du réseau local. Il la rend plus difficile, pas impossible (ARP spoofing, MAC flooding).
- ✅ **Bonne pratique** : activer les protections de couche 2 **et** chiffrer les communications.
- ❌ **Erreur fréquente 2** : penser qu'un VLAN est un pare-feu. Un VLAN sépare, mais c'est le routeur/pare-feu qui **filtre** le trafic entre VLAN.
- ✅ **Bonne pratique** : associer chaque VLAN à des règles de filtrage explicites.
- ❌ **Erreur fréquente 3** : laisser les ports inutilisés actifs et les utilisateurs dans le VLAN par défaut (VLAN 1).
- ✅ **Bonne pratique** : désactiver les ports libres et changer le VLAN natif.
- ❌ **Erreur fréquente 4** : mélanger administration des équipements et trafic utilisateur.
- ✅ **Bonne pratique** : un VLAN de gestion dédié, accessible seulement depuis des postes d'administration.

## 🧪 Quiz de validation

**Question 1 : Que fait un switch quand il ne connaît pas le port d'une adresse MAC de destination ?**
- A) Il détruit la trame
- B) Il envoie la trame sur tous les ports sauf celui d'origine ✅
- C) Il demande l'adresse IP au routeur
- D) Il redémarre

*Explication : c'est l'inondation (flooding) ; il apprend ensuite l'emplacement grâce à la réponse.*

**Question 2 : À quoi sert le protocole ARP ?**
- A) Traduire les noms en adresses IP
- B) Trouver l'adresse MAC correspondant à une adresse IP dans le réseau local ✅
- C) Chiffrer les trames
- D) Distribuer les adresses IP

*Explication : le DNS traduit les noms, le DHCP distribue les adresses, ARP relie IP et MAC.*

**Question 3 : Quel est le principal intérêt des VLAN ?**
- A) Augmenter la vitesse de la fibre
- B) Segmenter logiquement un réseau pour isoler les groupes ✅
- C) Remplacer le routeur
- D) Chiffrer le Wi-Fi

*Explication : les VLAN créent des domaines de diffusion séparés et permettent d'isoler les usages.*

**Question 4 : Que provoque une attaque de type ARP spoofing ?**
- A) Un déni de service sur le DNS
- B) Le passage du trafic de la victime par la machine de l'attaquant ✅
- C) La suppression d'un VLAN
- D) La saturation d'un serveur web

*Explication : l'attaquant se fait passer pour la passerelle auprès de la victime (homme du milieu).*

**Question 5 : Quelle protection limite le nombre d'adresses MAC par port d'un switch ?**
- A) DNSSEC
- B) NAT
- C) Port security ✅
- D) HSTS

*Explication : la port security réduit les risques de MAC flooding et d'usurpation de MAC.*

## 📝 Résumé

- Un switch (couche 2) apprend les adresses MAC et envoie chaque trame au bon port ; sinon il inonde.
- ARP associe une adresse IP à une adresse MAC, sans authentification.
- Les VLAN segmentent un réseau en domaines séparés ; un routeur ou un pare-feu filtre entre eux.
- Ports d'accès = un VLAN ; ports trunk = plusieurs VLAN étiquetés (802.1Q).
- Les attaques de couche 2 incluent ARP spoofing, MAC flooding, VLAN hopping et faux DHCP ; port security, DAI, DHCP snooping et 802.1X les contrent.
- Le chiffrement de bout en bout reste le filet de sécurité final.

## 🎓 Ce que tu as appris

✅ Décrire la commutation et la table MAC
✅ Expliquer ARP et sa faiblesse
✅ Concevoir une segmentation en VLAN
✅ Citer les attaques de couche 2 et leurs protections

## ➡️ Leçon suivante

**09 : Le pare-feu (firewall)** : filtrage de paquets, règles, états, zones de sécurité, et comment concevoir une politique de filtrage. Fichier : `09-firewall.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
