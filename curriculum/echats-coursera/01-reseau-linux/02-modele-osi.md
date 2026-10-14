---
title: "Le Modèle OSI"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 30
order: 2
category: "reseau"
tags: ["reseau", "osi", "couches", "encapsulation", "fondamentaux"]
prerequisites: ["01-introduction-reseaux"]
learning_objectives:
  - "Nommer et ordonner les 7 couches du modèle OSI"
  - "Expliquer le principe d'encapsulation"
  - "Associer protocoles, équipements et attaques à chaque couche"
  - "Utiliser le modèle OSI pour diagnostiquer un problème réseau"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Le Modèle OSI

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Nommer et ordonner les 7 couches du modèle OSI
- Expliquer le principe d'encapsulation
- Associer protocoles, équipements et attaques à chaque couche
- Utiliser le modèle OSI pour diagnostiquer un problème réseau

## 📚 Prérequis

- Leçon 01 : *Introduction aux Réseaux Informatiques* (hôtes, switch, routeur, adresses IP et MAC).

## 🧭 Introduction

Dans la leçon précédente, tu as vu qu'un message traverse ton téléphone, une box, un opérateur, puis des serveurs. Mais qui s'occupe de quoi ? Qui transforme ton texte en signaux électriques ou radio ? Qui s'assure que le message arrive entier et dans l'ordre ? Qui décide du chemin ?

Pour répondre sans se perdre, les ingénieurs ont découpé la communication réseau en **couches**. Chaque couche a une mission précise et ne se préoccupe pas du travail des autres. Le **modèle OSI** (*Open Systems Interconnection*), publié par l'ISO à la fin des années 1970 et normalisé dans les années 1980, en propose sept.

Pourquoi est-ce essentiel en cybersécurité ? Parce que toute attaque et toute défense se situent à une couche donnée. Un câble coupé (couche 1), un usurpateur d'adresse MAC (couche 2), un scan de ports (couche 4), une injection SQL (couche 7) : ce sont des problèmes différents qui appellent des protections différentes. Savoir « à quelle couche on est » est le premier réflexe d'un analyste.

Le modèle OSI est un **modèle théorique de référence**. Dans la pratique, Internet fonctionne avec le modèle TCP/IP (leçon suivante), plus simple. Mais le vocabulaire OSI (« couche 2 », « attaque de couche 7 ») est universel, et tu l'entendras tous les jours.

## 📖 Concepts clés

### 1. L'analogie de la lettre postale

Imagine que tu envoies un courrier important depuis Brazzaville vers un correspondant à Douala :

1. Tu rédiges la lettre (le contenu).
2. Tu la mets dans une enveloppe avec l'adresse du destinataire.
3. La poste la trie, la place dans un sac pour la bonne région.
4. Le sac est chargé dans un camion ou un avion (le transport physique).
5. À l'arrivée, le processus se déroule à l'envers : sac ouvert, enveloppe ouverte, lettre lue.

Chaque étape ajoute une enveloppe supplémentaire à l'aller et la retire au retour. C'est exactement le principe de l'**encapsulation** et de la **décapsulation**.

### 2. Les sept couches

On les numérote **de bas en haut**, de la plus physique à la plus proche de l'utilisateur.

| N° | Couche | Rôle | Unité de données | Exemples |
|---|---|---|---|---|
| 7 | Application | Interface avec les applications de l'utilisateur | Données | HTTP, DNS, SMTP, FTP |
| 6 | Présentation | Format, chiffrement, compression | Données | TLS (en partie), JPEG, UTF-8 |
| 5 | Session | Ouverture, maintien, fermeture des dialogues | Données | Sessions, cookies de session (en partie) |
| 4 | Transport | Transport fiable ou non, ports | Segment / datagramme | TCP, UDP |
| 3 | Réseau | Adressage logique, routage | Paquet | IP, ICMP |
| 2 | Liaison de données | Communication locale, adresses MAC | Trame | Ethernet, Wi-Fi (802.11), ARP |
| 1 | Physique | Transmission des bits sur le support | Bits | Câble RJ45, fibre, ondes radio |

**Mnémotechnique** (de la couche 7 à la 1) : « **A**ucun **P**irate **S**ait **T**oujours **R**éussir **L**es **P**iratages » : **A**pplication, **P**résentation, **S**ession, **T**ransport, **R**éseau, **L**iaison, **P**hysique. Choisis la phrase qui te parle, l'important est de la retenir.

### 3. Les couches en détail

**Couche 1 : Physique**
Elle transporte des **bits** (0 et 1) sous forme de signaux : tension électrique dans un câble cuivre, impulsions lumineuses dans une fibre, ondes radio pour le Wi-Fi ou la 4G.
- Équipements : câbles, hubs, répéteurs, cartes réseau (partie matérielle).
- Problèmes typiques : câble débranché, connecteur abîmé, interférences.
- Risques sécurité : coupure, écoute physique d'un câble, brouillage radio.

**Couche 2 : Liaison de données**
Elle organise l'échange entre deux machines **directement connectées** (même réseau local). Elle regroupe les bits en **trames** et utilise les **adresses MAC**.
- Équipements : switchs, points d'accès Wi-Fi.
- Protocoles : Ethernet, Wi-Fi, ARP (qui associe une IP à une MAC).
- Risques sécurité : usurpation d'adresse MAC (*MAC spoofing*), empoisonnement ARP (*ARP poisoning*), saturation de la table d'un switch.

**Couche 3 : Réseau**
Elle gère l'**adressage logique** (adresses IP) et le **routage** : choisir le chemin d'un paquet à travers plusieurs réseaux.
- Équipements : routeurs, pare-feu de niveau 3.
- Protocoles : IPv4, IPv6, ICMP (utilisé par `ping`).
- Risques sécurité : usurpation d'adresse IP (*IP spoofing*), inondation ICMP, redirection de routes.

**Couche 4 : Transport**
Elle assure la communication **de bout en bout** entre deux applications, identifiées par des **ports**. TCP est fiable (accusés de réception, réordonnancement), UDP est rapide mais sans garantie.
- Protocoles : TCP, UDP.
- Risques sécurité : scans de ports, attaques par saturation (SYN flood).

**Couche 5 : Session**
Elle ouvre, maintient et ferme des **dialogues** entre applications. Dans la pratique, ses fonctions sont souvent absorbées par les couches supérieures.
- Risques sécurité : vol ou détournement de session (*session hijacking*).

**Couche 6 : Présentation**
Elle s'occupe de la **représentation** des données : encodage, compression, chiffrement. Elle garantit que l'émetteur et le récepteur « parlent le même format ».
- Exemples : encodage UTF-8, compression, chiffrement TLS (selon les interprétations).
- Risques sécurité : algorithmes de chiffrement faibles, mauvais encodage exploité pour contourner des filtres.

**Couche 7 : Application**
La plus proche de l'utilisateur. Elle fournit les protocoles utilisés par les logiciels : navigation web, messagerie, transfert de fichiers.
- Protocoles : HTTP/HTTPS, DNS, SMTP, FTP, SSH.
- Risques sécurité : injection SQL, XSS, phishing, exploitation de services vulnérables. C'est la couche où se trouvent la majorité des failles que tu étudieras dans le module Sécurité Web.

### 4. L'encapsulation

Quand ton navigateur envoie une requête, les données descendent les couches. À chaque niveau, un **en-tête** (*header*) est ajouté, comme une enveloppe qui contient la précédente :

```
Couche 7 : [ Données HTTP ]
Couche 4 : [ En-tête TCP | Données HTTP ]                         → segment
Couche 3 : [ En-tête IP | En-tête TCP | Données HTTP ]           → paquet
Couche 2 : [ En-tête Eth | En-tête IP | TCP | Données | Fin ]    → trame
Couche 1 : 0101101001011...                                       → bits
```

À la réception, la **décapsulation** retire les en-têtes dans l'ordre inverse. Chaque couche ne lit que **son** en-tête. Un routeur, par exemple, lit l'en-tête IP (couche 3) mais ignore le contenu HTTP.

**Conséquence en sécurité** : un pare-feu, un IDS ou un analyseur comme Wireshark peut inspecter différentes couches. Plus l'inspection monte haut, plus elle est fine, mais plus elle coûte en ressources.

### 5. Où se placent les équipements ?

| Équipement | Couche principale |
|---|---|
| Hub, répéteur, câble | 1 |
| Switch, point d'accès Wi-Fi | 2 |
| Routeur | 3 |
| Pare-feu classique (filtrage IP/ports) | 3-4 |
| Pare-feu applicatif (WAF), proxy | 7 |

Certains équipements modernes (« switchs de niveau 3 », pare-feu nouvelle génération) couvrent plusieurs couches.

### 6. OSI et dépannage : la méthode des couches

Un technicien efficace ne devine pas : il **teste couche par couche**.

1. **Couche 1** : le câble est-il branché ? Le Wi-Fi est-il activé ? Les voyants sont-ils allumés ?
2. **Couche 2** : la machine est-elle connectée au bon réseau ? A-t-elle une adresse MAC visible ?
3. **Couche 3** : a-t-elle une adresse IP valide ? Peut-elle joindre la passerelle (`ping`) ?
4. **Couche 4** : le port du service est-il ouvert ?
5. **Couche 7** : le service répond-il correctement (page web, serveur de messagerie) ?

Cette approche s'applique aussi aux audits : on cartographie, puis on analyse couche par couche.

### 7. Exemple complet : ouvrir une page web

Tu tapes `https://exemple.org` dans ton navigateur :

- **Couche 7** : le navigateur prépare une requête HTTP ; au préalable, DNS traduit le nom en adresse IP.
- **Couche 6** : la requête est chiffrée par TLS.
- **Couche 5** : la session sécurisée est établie.
- **Couche 4** : TCP ouvre une connexion vers le port 443 du serveur.
- **Couche 3** : IP ajoute les adresses source et destination.
- **Couche 2** : Wi-Fi ou Ethernet ajoute les adresses MAC pour le prochain saut (la box).
- **Couche 1** : les trames deviennent des ondes radio ou des signaux électriques.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : capture uniquement le trafic de **ta propre machine** sur **ton propre réseau**. Intercepter le trafic d'autrui sans autorisation est illégal.

### Exercice 1 — Retrouver les couches dans ta configuration

```bash
# Windows
ipconfig /all

# Linux
ip addr show
ip route show
```

Classe chaque information trouvée dans sa couche :

| Information | Couche |
|---|---|
| Adresse MAC | ? |
| Adresse IP | ? |
| Passerelle par défaut | ? |
| Type de connexion (Ethernet / Wi-Fi) | ? |

*Réponses : MAC → 2 ; IP → 3 ; passerelle → 3 ; type de connexion → 1 et 2.*

### Exercice 2 — Diagnostic par couches

Joue le rôle du technicien. Exécute dans l'ordre :

```bash
ping 127.0.0.1          # ta pile réseau locale fonctionne-t-elle ?
ping <ta-passerelle>    # joins-tu ton routeur ?
ping 8.8.8.8            # joins-tu Internet par adresse IP ?
ping example.com        # la résolution de noms (DNS) fonctionne-t-elle ?
```

Interprétation :
- Échec au 3e ping mais succès au 2e : problème au-delà de ta box (opérateur).
- Succès au 3e mais échec au 4e : problème **DNS** (couche 7).

### Exercice 3 — Observer l'encapsulation avec Wireshark

1. Installe Wireshark (gratuit, wireshark.org).
2. Lance une capture sur ton interface Wi-Fi ou Ethernet.
3. Dans la barre de filtre, tape `icmp`.
4. Dans un terminal, exécute `ping 8.8.8.8`.
5. Arrête la capture et clique sur un paquet.

Dans le panneau central, tu verras des blocs empilés :
- **Frame** (couche 1 : informations sur la capture)
- **Ethernet II** (couche 2 : adresses MAC)
- **Internet Protocol Version 4** (couche 3 : adresses IP)
- **Internet Control Message Protocol** (le contenu ICMP)

Chaque bloc correspond à une couche. Déplie-les et repère les adresses MAC et IP. C'est la meilleure façon de **voir** l'encapsulation.

### Exercice 4 — Capturer une requête web

Même méthode avec le filtre `dns`, puis ouvre un site dans ton navigateur. Observe la requête DNS et sa réponse. À quelle couche appartient DNS ? (Couche 7.)

## 🔍 Approfondissement

### Pour aller plus loin

- Documentation de Wireshark : section « User's Guide » sur les filtres d'affichage.
- Module « Introductory Networking » de TryHackMe.
- Cours de réseaux de l'ANSSI (SecNumacadémie).

### Pièges courants

- ❌ **Erreur fréquente 1** : croire que le modèle OSI est ce qu'Internet utilise réellement. C'est TCP/IP qui est implémenté ; OSI est un modèle de référence.
- ✅ **Bonne pratique** : utiliser OSI pour **raisonner et communiquer**, TCP/IP pour comprendre ce qui se passe réellement.
- ❌ **Erreur fréquente 2** : confondre couche 2 et couche 3 (MAC vs IP).
- ✅ **Bonne pratique** : retenir que la MAC sert **dans** un réseau local, l'IP **entre** les réseaux.
- ❌ **Erreur fréquente 3** : penser que HTTPS « sécurise tout ». TLS protège le contenu des échanges, pas la couche 3 ni les métadonnées (qui parle à qui, quand).
- ✅ **Bonne pratique** : raisonner par couche pour savoir ce qu'une protection couvre et ce qu'elle ne couvre pas.

## 🧪 Quiz de validation

**Question 1 : Combien de couches compte le modèle OSI ?**
- A) 4
- B) 5
- C) 7 ✅
- D) 9

*Explication : Physique, Liaison, Réseau, Transport, Session, Présentation, Application : sept couches.*

**Question 2 : À quelle couche travaille un routeur ?**
- A) Couche 2
- B) Couche 3 ✅
- C) Couche 5
- D) Couche 7

*Explication : le routeur utilise les adresses IP pour acheminer les paquets : c'est la couche Réseau.*

**Question 3 : Quelle unité de données correspond à la couche 2 ?**
- A) Le bit
- B) Le paquet
- C) La trame ✅
- D) Le segment

*Explication : couche 1 = bits, 2 = trames, 3 = paquets, 4 = segments (TCP) ou datagrammes (UDP).*

**Question 4 : Une injection SQL est une attaque de quelle couche ?**
- A) Couche 1
- B) Couche 4
- C) Couche 3
- D) Couche 7 ✅

*Explication : elle cible une application web, donc la couche Application.*

**Question 5 : Que signifie l'encapsulation ?**
- A) Compresser les données
- B) Ajouter un en-tête à chaque couche lors de l'émission ✅
- C) Chiffrer un fichier
- D) Supprimer les erreurs réseau

*Explication : chaque couche enveloppe les données de la couche supérieure avec son propre en-tête.*

## 📝 Résumé

- Le modèle OSI découpe la communication réseau en 7 couches : Physique, Liaison, Réseau, Transport, Session, Présentation, Application.
- L'encapsulation ajoute un en-tête à chaque couche à l'émission ; la décapsulation les retire à la réception.
- Les équipements et les protocoles se rangent par couche : switch en 2, routeur en 3, HTTP en 7.
- Le dépannage et l'audit se font couche par couche.
- Toute attaque et toute défense se situent à une ou plusieurs couches précises.

## 🎓 Ce que tu as appris

✅ Citer les 7 couches dans l'ordre
✅ Expliquer l'encapsulation
✅ Placer équipements, protocoles et attaques sur le bon niveau
✅ Observer des trames dans Wireshark

## ➡️ Leçon suivante

**03 : TCP/IP** : le modèle réellement utilisé par Internet, la poignée de main en trois temps (*three-way handshake*) et la différence entre TCP et UDP. Fichier : `03-tcp-ip.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
