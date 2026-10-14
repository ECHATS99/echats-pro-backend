---
title: "Adressage IP et Sous-réseaux"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 35
order: 4
category: "reseau"
tags: ["reseau", "ipv4", "ipv6", "cidr", "masque", "sous-reseau", "nat", "dhcp"]
prerequisites: ["01-introduction-reseaux", "02-modele-osi", "03-tcp-ip"]
learning_objectives:
  - "Lire et écrire une adresse IPv4 et un masque de sous-réseau"
  - "Utiliser la notation CIDR"
  - "Calculer l'adresse réseau, de diffusion et le nombre d'hôtes"
  - "Distinguer adresses publiques et privées, comprendre NAT et DHCP"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Adressage IP et Sous-réseaux

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Lire et écrire une adresse IPv4 et un masque de sous-réseau
- Utiliser la notation CIDR
- Calculer l'adresse réseau, l'adresse de diffusion et le nombre d'hôtes
- Distinguer adresses publiques et privées, et comprendre NAT et DHCP

## 📚 Prérequis

- Leçons 01 à 03 du module (réseau, OSI, TCP/IP).
- Savoir convertir un petit nombre en binaire est un plus, mais la leçon l'explique pas à pas.

## 🧭 Introduction

Pour qu'un colis arrive, il faut une adresse précise. Sur un réseau, c'est l'**adresse IP** qui joue ce rôle. Sans elle, un paquet ne sait ni d'où il vient, ni où il va.

En cybersécurité, l'adressage est omniprésent. Quand tu définis le périmètre d'un audit (« tester le réseau `192.168.10.0/24` »), quand tu écris une règle de pare-feu, quand tu analyses des journaux ou que tu lances Nmap, tu manipules des adresses et des masques. Une erreur de masque peut exposer un réseau entier ou, dans un test d'intrusion, te faire sortir de ton périmètre autorisé, ce qui est un problème légal grave.

Cette leçon est volontairement concrète : tu vas apprendre à **calculer** un réseau à la main. C'est la compétence qui sépare ceux qui utilisent des outils de ceux qui les comprennent.

## 📖 Concepts clés

### 1. L'adresse IPv4

Une adresse IPv4 est composée de **32 bits**, écrits en 4 groupes de 8 bits (**octets**), séparés par des points. Chaque octet est affiché en décimal, de 0 à 255.

```
Décimal :  192  .  168  .   1   .  25
Binaire :  11000000.10101000.00000001.00011001
```

Il existe environ 4,3 milliards d'adresses IPv4 (2³²). C'est devenu insuffisant, ce qui a conduit à IPv6 et à des astuces comme le NAT.

**Convertir un octet en binaire** : chaque bit vaut une puissance de 2.

| Bit | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| 192 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 168 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| 25 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 |

Par exemple : 25 = 16 + 8 + 1 → `00011001`.

### 2. Partie réseau et partie hôte

Une adresse IP se divise en deux :
- la **partie réseau** : identifie le réseau (comme le nom de la rue) ;
- la **partie hôte** : identifie la machine dans ce réseau (comme le numéro de la maison).

Le **masque de sous-réseau** indique où se fait la coupure. Les bits à `1` du masque désignent la partie réseau, les bits à `0` la partie hôte.

```
IP      : 192.168.1.25   = 11000000.10101000.00000001.00011001
Masque  : 255.255.255.0  = 11111111.11111111.11111111.00000000
                           |---- réseau ----------|-- hôte --|
```

Ici, le réseau est `192.168.1.0` et l'hôte est le n° 25.

### 3. La notation CIDR

Écrire `255.255.255.0` est long. La notation **CIDR** (*Classless Inter-Domain Routing*) compte simplement le nombre de bits à 1 du masque et l'ajoute après un slash : `192.168.1.25/24`.

| CIDR | Masque | Hôtes utilisables |
|---|---|---|
| /8 | 255.0.0.0 | 16 777 214 |
| /16 | 255.255.0.0 | 65 534 |
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /26 | 255.255.255.192 | 62 |
| /27 | 255.255.255.224 | 30 |
| /28 | 255.255.255.240 | 14 |
| /30 | 255.255.255.252 | 2 |

**Formule** : nombre d'hôtes utilisables = 2^(bits hôte) − 2. On retire 2 adresses réservées :
- la première (tous les bits hôte à 0) = **adresse du réseau** ;
- la dernière (tous les bits hôte à 1) = **adresse de diffusion** (*broadcast*).

Exemple : `/24` → 8 bits hôte → 2⁸ − 2 = 254 machines.

### 4. Calculer un réseau pas à pas

**Exemple : `192.168.10.77/26`**

1. Le masque /26 = 26 bits à 1 → `255.255.255.192`.
2. Les 24 premiers bits (3 octets) sont entièrement réseau. Le 4e octet est coupé : 2 bits réseau, 6 bits hôte.
3. 6 bits hôte → 2⁶ = **64 adresses** par sous-réseau (62 utilisables). Le « pas » est 64 : les sous-réseaux commencent à 0, 64, 128, 192.
4. L'adresse hôte `77` est entre 64 et 127, donc :
   - **Adresse réseau** : `192.168.10.64`
   - **Adresse de diffusion** : `192.168.10.127`
   - **Plage utilisable** : `192.168.10.65` à `192.168.10.126`
   - **Hôtes utilisables** : 62

Méthode rapide : trouver le pas (256 − valeur du masque dans l'octet coupé : 256 − 192 = 64), puis repérer dans quelle tranche tombe l'adresse.

### 5. Les anciennes classes

Avant le CIDR, on parlait de classes. Tu les rencontreras encore dans des cours et des examens :

| Classe | Premier octet | Masque par défaut |
|---|---|---|
| A | 1 – 126 | /8 |
| B | 128 – 191 | /16 |
| C | 192 – 223 | /24 |
| D | 224 – 239 | Multicast |
| E | 240 – 255 | Réservée |

Aujourd'hui, on travaille presque exclusivement en CIDR, sans tenir compte des classes.

### 6. Adresses publiques et privées

Les adresses **publiques** sont uniques sur Internet et attribuées par des organismes régionaux (en Afrique : AFRINIC). Les adresses **privées** ne sont pas routées sur Internet : elles servent à l'intérieur des réseaux locaux (RFC 1918).

| Plage privée | CIDR |
|---|---|
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 |

Adresses spéciales :
- `127.0.0.1` (boucle locale, *localhost*) : ta propre machine.
- `169.254.x.x` (APIPA) : adresse que s'attribue une machine quand elle n'a trouvé aucun serveur DHCP ; signe d'un problème de configuration.
- `0.0.0.0` : « toutes les interfaces » ou « adresse inconnue » selon le contexte.

### 7. NAT : partager une seule adresse publique

Ta box possède **une adresse publique** et tes appareils des adresses privées. Le **NAT** (*Network Address Translation*) traduit les adresses privées en adresse publique au passage. Quand ton téléphone (`192.168.1.25`) contacte un site, la box remplace l'adresse source par son adresse publique, retient la correspondance, et retraduit la réponse.

Conséquences :
- une même adresse IP publique peut représenter **des dizaines d'appareils**, voire des centaines d'abonnés chez certains opérateurs (CGNAT) : une IP ne désigne donc pas toujours une personne précise ;
- le NAT cache les machines internes mais **n'est pas un pare-feu** : il ne remplace aucune règle de filtrage.

### 8. DHCP : attribution automatique

Configurer chaque machine à la main serait fastidieux. Le **DHCP** (*Dynamic Host Configuration Protocol*) distribue automatiquement adresse IP, masque, passerelle et serveur DNS. La séquence est connue sous le nom **DORA** :

1. **D**iscover : le client crie « y a-t-il un serveur DHCP ? » (diffusion).
2. **O**ffer : le serveur propose une adresse.
3. **R**equest : le client demande à utiliser cette adresse.
4. **A**cknowledge : le serveur confirme.

Cette adresse est prêtée pour une durée limitée (le *bail*). **Risque** : un faux serveur DHCP (*rogue DHCP*) sur un réseau peut distribuer une fausse passerelle ou un faux DNS et rediriger le trafic.

### 9. Un mot sur IPv6

IPv6 utilise **128 bits**, notés en hexadécimal en 8 groupes : `2001:0db8:85a3:0000:0000:8a2e:0370:7334`. On peut abréger les zéros consécutifs : `2001:db8:85a3::8a2e:370:7334`. Il offre un espace d'adressage quasi illimité (environ 3,4 × 10³⁸ adresses) et supprime le besoin de NAT. La plupart des principes (réseau/hôte, préfixe, routage) restent les mêmes, avec une notation de préfixe du type `/64`. Nous y reviendrons dans un module avancé.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : ces exercices sont des calculs et des observations sur **ta propre machine**. Dans un audit réel, ne travaille que sur le périmètre écrit dans ton autorisation.

### Exercice 1 — Lire ton adressage

```bash
# Windows
ipconfig

# Linux
ip -4 addr show
```

Note ton adresse IPv4 et ton masque. Ensuite :
1. Convertis le masque en CIDR (compte les bits à 1). Exemple : 255.255.255.0 = /24.
2. Dis si ton adresse est privée ou publique.
3. Calcule l'adresse de ton réseau et le nombre d'hôtes possibles.

### Exercice 2 — Calculs à faire à la main

Calcule pour chaque cas l'adresse réseau, l'adresse de diffusion et le nombre d'hôtes utilisables :

| Adresse | Réseau | Diffusion | Hôtes |
|---|---|---|---|
| 192.168.1.130/25 | ? | ? | ? |
| 10.5.20.200/28 | ? | ? | ? |
| 172.16.45.9/20 | ? | ? | ? |

**Corrigé :**
- `192.168.1.130/25` → réseau `192.168.1.128`, diffusion `192.168.1.255`, 126 hôtes.
- `10.5.20.200/28` → pas de 16 ; 200 = 192 + 8 → réseau `10.5.20.192`, diffusion `10.5.20.207`, 14 hôtes.
- `172.16.45.9/20` → masque 255.255.240.0 ; pas de 16 dans le 3e octet ; 45 est dans la tranche 32–47 → réseau `172.16.32.0`, diffusion `172.16.47.255`, 4094 hôtes.

### Exercice 3 — Découper un réseau

Une agence reçoit le réseau `192.168.50.0/24` et veut 4 sous-réseaux égaux (Direction, Comptabilité, Technique, Invités).

1. 4 sous-réseaux = 2² → on emprunte 2 bits → nouveau masque **/26**.
2. Chaque sous-réseau contient 64 adresses (62 utilisables).
3. Résultat :

| Service | Réseau | Plage utilisable | Diffusion |
|---|---|---|---|
| Direction | 192.168.50.0/26 | .1 à .62 | .63 |
| Comptabilité | 192.168.50.64/26 | .65 à .126 | .127 |
| Technique | 192.168.50.128/26 | .129 à .190 | .191 |
| Invités | 192.168.50.192/26 | .193 à .254 | .255 |

Intérêt sécurité : séparer les services permet d'isoler un réseau compromis (par exemple « Invités ») du reste.

### Exercice 4 — Vérifier avec un outil

Sous Linux, l'outil `ipcalc` (à installer si besoin) valide tes calculs :

```bash
ipcalc 192.168.10.77/26
```

Compare sa sortie avec ton calcul manuel.

### Exercice 5 — Repérer ton adresse publique

Dans ton navigateur, cherche « quelle est mon adresse IP ». Compare avec celle de ta machine : l'adresse affichée est celle de ta box (ou de ton opérateur). Tu observes le NAT en action.

## 🔍 Approfondissement

### Pour aller plus loin

- Un calculateur de sous-réseaux en ligne (pour vérifier, pas pour remplacer l'entraînement).
- RFC 1918 (adresses privées) et RFC 4632 (CIDR).
- Les exercices d'adressage de Cisco Networking Academy (gratuits sur inscription).

### Pièges courants

- ❌ **Erreur fréquente 1** : oublier de retirer les 2 adresses réservées (réseau et diffusion) dans le compte d'hôtes.
- ✅ **Bonne pratique** : toujours utiliser 2^n − 2.
- ❌ **Erreur fréquente 2** : confondre le masque et l'adresse. Le masque seul ne désigne aucune machine.
- ✅ **Bonne pratique** : écrire systématiquement l'adresse avec son CIDR (`192.168.1.25/24`).
- ❌ **Erreur fréquente 3** : traiter une IP publique comme un identifiant sûr de personne.
- ✅ **Bonne pratique** : en investigation, croiser l'IP avec l'heure exacte, les journaux de l'opérateur et le cadre légal.
- ❌ **Erreur fréquente 4** : laisser un défaut de configuration où deux services partagent le même réseau sans cloisonnement.
- ✅ **Bonne pratique** : segmenter par fonction et appliquer des règles de filtrage entre segments.

## 🧪 Quiz de validation

**Question 1 : Combien de bits compose une adresse IPv4 ?**
- A) 16
- B) 32 ✅
- C) 64
- D) 128

*Explication : 4 octets de 8 bits = 32 bits.*

**Question 2 : À quel masque correspond /24 ?**
- A) 255.255.0.0
- B) 255.255.255.0 ✅
- C) 255.255.255.128
- D) 255.0.0.0

*Explication : 24 bits à 1 = trois octets pleins = 255.255.255.0.*

**Question 3 : Combien d'hôtes utilisables dans un réseau /26 ?**
- A) 30
- B) 64
- C) 62 ✅
- D) 126

*Explication : 6 bits hôte = 2⁶ = 64 adresses, moins 2 réservées = 62.*

**Question 4 : Laquelle de ces adresses est privée ?**
- A) 172.20.5.10 ✅
- B) 172.32.5.10
- C) 8.8.4.4
- D) 41.220.10.1

*Explication : la plage privée 172.16.0.0/12 va de 172.16.x.x à 172.31.x.x. 172.32 est donc publique.*

**Question 5 : Quel est le rôle du NAT ?**
- A) Chiffrer les données
- B) Traduire des adresses privées en adresse publique ✅
- C) Attribuer les adresses automatiquement
- D) Résoudre les noms de domaine

*Explication : le NAT permet à plusieurs machines privées de partager une adresse publique. L'attribution automatique, c'est le DHCP ; la résolution de noms, c'est le DNS.*

## 📝 Résumé

- Une adresse IPv4 fait 32 bits, écrite en 4 octets décimaux.
- Le masque sépare la partie réseau de la partie hôte ; le CIDR (`/24`) le note de façon compacte.
- Hôtes utilisables = 2^(bits hôte) − 2 ; on repère le réseau avec le « pas » du sous-réseau.
- Plages privées : 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16.
- Le NAT partage une adresse publique ; le DHCP distribue les adresses automatiquement.
- Segmenter un réseau limite la propagation d'une attaque.

## 🎓 Ce que tu as appris

✅ Convertir et lire des adresses IPv4 et des masques
✅ Calculer réseau, diffusion et nombre d'hôtes
✅ Découper un réseau en sous-réseaux cohérents
✅ Comprendre NAT, DHCP et la différence public/privé

## ➡️ Leçon suivante

**05 : DNS** : le « carnet d'adresses » d'Internet, comment un nom devient une adresse IP, les types d'enregistrements et les attaques associées. Fichier : `05-dns.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
