---
title: "Permissions et Utilisateurs Linux"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 35
order: 11
category: "linux"
tags: ["linux", "permissions", "chmod", "chown", "suid", "utilisateurs", "sudo"]
prerequisites: ["10-commandes-linux-essentielles"]
learning_objectives:
  - "Lire les permissions rwx d'un fichier ou d'un dossier"
  - "Modifier les droits avec chmod (symbolique et octal) et chown"
  - "Comprendre utilisateurs, groupes, root et sudo"
  - "Reconnaître les permissions dangereuses (SUID, fichiers world-writable)"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Permissions et Utilisateurs Linux

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Lire les permissions `rwx` d'un fichier ou d'un dossier
- Modifier les droits avec `chmod` (symbolique et octal) et `chown`
- Comprendre utilisateurs, groupes, root et `sudo`
- Reconnaître les permissions dangereuses (SUID, fichiers modifiables par tous)

## 📚 Prérequis

- Leçon 10 : *Commandes Linux Essentielles*

## 🧭 Introduction

Linux est un système **multi-utilisateurs** : sur un même serveur, des dizaines de personnes et de services (serveur web, base de données, messagerie) cohabitent. Comment éviter que l'un lise les secrets de l'autre, ou qu'un service piraté prenne le contrôle de tout ? Grâce au **système de permissions**.

Chaque fichier et chaque dossier possède un propriétaire, un groupe et des droits précis. C'est un mécanisme simple en apparence, mais d'une importance énorme en sécurité. Une grande partie des incidents sur serveurs Linux vient de permissions trop larges : un fichier de mots de passe lisible par tous, un script modifiable par n'importe qui, un programme avec des droits excessifs.

Et côté offensif (dans un cadre légal de test d'intrusion ou de CTF), l'**élévation de privilèges** consiste très souvent à exploiter une mauvaise configuration de permissions. Comprendre ce système, c'est comprendre à la fois comment protéger un serveur et comment les audits en détectent les faiblesses.

## 📖 Concepts clés

### 1. Utilisateurs, groupes et root

- **Utilisateur** : identité qui exécute des actions (une personne, un service). Chaque utilisateur a un **UID** (numéro).
- **Groupe** : ensemble d'utilisateurs partageant des droits. Chaque groupe a un **GID**.
- **root** : super-utilisateur (UID 0). Il peut tout faire sur le système. Un attaquant qui devient root a pris le contrôle total.

Fichiers importants :

| Fichier | Contenu |
|---|---|
| `/etc/passwd` | Liste des comptes (nom, UID, GID, dossier personnel, shell). Lisible par tous |
| `/etc/shadow` | Empreintes (hash) des mots de passe. Lisible **uniquement par root** |
| `/etc/group` | Liste des groupes et de leurs membres |
| `/etc/sudoers` | Qui a le droit d'utiliser `sudo` |

Commandes utiles :

```bash
whoami           # utilisateur courant
id               # UID, GID et groupes
groups           # groupes de l'utilisateur
who              # qui est connecté
```

### 2. Lire les permissions

```bash
ls -l
-rwxr-xr--  1  etudiant  formation  2048  oct 3 10:15  script.sh
```

Décomposition de `-rwxr-xr--` :

```
-   rwx   r-x   r--
│    │     │     │
│    │     │     └─ autres (others)
│    │     └─────── groupe (group)
│    └───────────── propriétaire (user/owner)
└────────────────── type : - fichier, d dossier, l lien
```

Les trois droits :

| Lettre | Sur un fichier | Sur un dossier |
|---|---|---|
| `r` (read) | Lire le contenu | Lister le contenu |
| `w` (write) | Modifier le contenu | Créer, supprimer, renommer des éléments dedans |
| `x` (execute) | Exécuter comme un programme | Entrer dans le dossier (`cd`) et accéder à ce qu'il contient |

Dans l'exemple : le propriétaire `etudiant` peut lire, écrire et exécuter ; les membres du groupe `formation` peuvent lire et exécuter ; les autres peuvent seulement lire.

**Un point important sur les dossiers** : pour supprimer un fichier, ce n'est pas le droit sur le fichier qui compte, mais le droit **d'écriture sur le dossier** qui le contient.

### 3. La notation octale

Chaque droit a une valeur : **r = 4, w = 2, x = 1**. On additionne par groupe de trois :

| Droits | Calcul | Valeur |
|---|---|---|
| `rwx` | 4+2+1 | **7** |
| `rw-` | 4+2 | **6** |
| `r-x` | 4+1 | **5** |
| `r--` | 4 | **4** |
| `---` | 0 | **0** |

`rwxr-xr--` = 7 (propriétaire), 5 (groupe), 4 (autres) = **754**.

Valeurs courantes :

| Octal | Symbolique | Usage typique |
|---|---|---|
| 600 | `rw-------` | Fichiers privés (clés SSH privées) |
| 644 | `rw-r--r--` | Fichiers ordinaires lisibles par tous |
| 700 | `rwx------` | Dossier privé, script personnel |
| 755 | `rwxr-xr-x` | Programmes, dossiers publics |
| 777 | `rwxrwxrwx` | **Tout pour tout le monde : à éviter** |

### 4. Modifier les droits : chmod

**Notation symbolique** : `chmod [qui][+/-/=][droits] fichier`
- qui : `u` (user), `g` (group), `o` (others), `a` (all) ;
- `+` ajoute, `-` retire, `=` fixe.

```bash
chmod u+x script.sh        # ajoute l'exécution pour le propriétaire
chmod g-w fichier.txt      # retire l'écriture au groupe
chmod o-rwx secret.txt     # retire tous les droits aux autres
chmod a+r public.txt       # lecture pour tous
chmod u=rwx,g=rx,o= prog   # fixe précisément
```

**Notation octale** :

```bash
chmod 755 script.sh
chmod 600 ~/.ssh/id_rsa
chmod -R 750 dossier/      # -R : récursif
```

### 5. Changer propriétaire et groupe : chown, chgrp

```bash
sudo chown alice fichier.txt            # change le propriétaire
sudo chown alice:equipe fichier.txt     # propriétaire et groupe
sudo chown -R www-data:www-data /var/www/site   # récursif
sudo chgrp equipe fichier.txt           # change seulement le groupe
```

Seul **root** peut changer le propriétaire d'un fichier.

### 6. Les permissions par défaut : umask

Quand tu crées un fichier, ses droits dépendent de l'**umask**, qui **retire** des droits à la valeur maximale (666 pour un fichier, 777 pour un dossier). Avec `umask 022` : fichier = 644, dossier = 755.

```bash
umask          # affiche la valeur actuelle
umask 027      # fichiers: 640, dossiers: 750 (plus restrictif)
```

### 7. sudo : des droits à la demande

`sudo` permet à un utilisateur autorisé d'exécuter une commande **en tant que root** (ou un autre utilisateur), après avoir saisi **son propre** mot de passe.

```bash
sudo cat /etc/shadow
sudo -l            # liste ce que l'utilisateur a le droit de faire avec sudo
sudo -u alice ls   # exécuter en tant qu'un autre utilisateur
```

Les règles se définissent avec `visudo` (jamais en éditant `/etc/sudoers` directement). Bonne pratique : donner à chaque utilisateur uniquement les **commandes précises** dont il a besoin, plutôt que `ALL`.

### 8. Permissions spéciales : SUID, SGID, sticky bit

| Bit | Effet | Notation |
|---|---|---|
| **SUID** | Le programme s'exécute avec les droits de **son propriétaire** (pas de celui qui le lance) | `rws` ; octal 4xxx |
| **SGID** | Le programme s'exécute avec les droits du **groupe** ; sur un dossier, les nouveaux fichiers héritent du groupe | `rws` côté groupe ; 2xxx |
| **Sticky bit** | Dans un dossier partagé, seul le propriétaire d'un fichier peut le supprimer | `t` ; 1xxx |

Exemples : `/usr/bin/passwd` a le bit SUID (appartient à root), ce qui permet à un utilisateur ordinaire de changer son mot de passe (écriture dans `/etc/shadow`). `/tmp` a le sticky bit : tout le monde y écrit, mais chacun ne supprime que ses propres fichiers.

```bash
ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 59976 ... /usr/bin/passwd
ls -ld /tmp
drwxrwxrwt 15 root root 4096 ... /tmp
```

**Sécurité** : un programme SUID root est une **cible de choix**. S'il est vulnérable ou mal configuré (par exemple un éditeur ou un interpréteur), un utilisateur normal peut en tirer les droits de root. Lister les binaires SUID est un geste de base d'audit :

```bash
find / -perm -4000 -type f 2>/dev/null
```

Il faut ensuite vérifier que **chacun** est légitime et à jour. Des bases comme GTFOBins recensent les programmes courants détournables lorsqu'ils sont mal configurés. Elle sert aussi bien aux défenseurs (durcissement) qu'en CTF.

### 9. Les ACL : des droits plus fins

Les permissions classiques ne gèrent qu'un propriétaire, un groupe et « les autres ». Les **ACL** (*Access Control Lists*) permettent d'accorder des droits à des utilisateurs ou groupes supplémentaires :

```bash
setfacl -m u:bob:r-- rapport.txt    # donne la lecture à bob
getfacl rapport.txt                 # affiche les ACL
```

### 10. Bonnes pratiques de durcissement

- **Moindre privilège** : chaque utilisateur et chaque service n'a que les droits nécessaires.
- Pas de **777**, jamais : si tu en as besoin, c'est que la conception est à revoir.
- Les services (serveur web, base de données) tournent sous **leur propre compte non privilégié**.
- Les clés SSH privées en **600**, le dossier `~/.ssh` en **700**.
- Les fichiers de configuration contenant des mots de passe en **600** ou **640**.
- Auditer régulièrement : fichiers modifiables par tous, binaires SUID, comptes inutiles, comptes sans mot de passe.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : travaille dans **ta VM ou ta machine**, dans un dossier de test. Les recherches de fichiers SUID et de permissions faibles ne s'appliquent qu'à **tes** systèmes ou à des systèmes pour lesquels tu as une autorisation écrite.

### Exercice 1 — Lire des permissions

```bash
ls -l /etc/passwd /etc/shadow /usr/bin/passwd /tmp
```

Pour chaque ligne, note : le type, les droits du propriétaire, du groupe, des autres, et le propriétaire.

Questions guidées :
1. Pourquoi `/etc/shadow` n'est-il pas lisible par tout le monde ? (Il contient les empreintes des mots de passe.)
2. Pourquoi `/usr/bin/passwd` porte-t-il un `s` ? (Bit SUID, il doit modifier `/etc/shadow`.)

### Exercice 2 — Jouer avec chmod

```bash
cd ~/laboratoire
touch fichier_test.txt
ls -l fichier_test.txt

chmod 600 fichier_test.txt
ls -l fichier_test.txt

chmod g+r,o+r fichier_test.txt
ls -l fichier_test.txt

chmod 000 fichier_test.txt
cat fichier_test.txt      # que se passe-t-il ?
chmod 644 fichier_test.txt
```

Résultat attendu : après `chmod 000`, `cat` répond « Permission non accordée ». Sans aucun droit, même le propriétaire ne peut pas lire (mais il peut toujours rétablir les droits).

### Exercice 3 — Rendre un script exécutable

```bash
cat > bonjour.sh << 'EOF'
#!/bin/bash
echo "Bonjour depuis ECHATS PRO !"
EOF

./bonjour.sh                 # Permission non accordée
chmod u+x bonjour.sh
./bonjour.sh                 # fonctionne
```

Pourquoi le premier appel échoue-t-il ? (Le fichier n'a pas le droit `x`.)

### Exercice 4 — Dossiers et droit d'exécution

```bash
mkdir dossier_secret
echo "contenu" > dossier_secret/info.txt
chmod 600 dossier_secret           # retire le x
ls dossier_secret                  # essaie
cat dossier_secret/info.txt        # essaie
chmod 700 dossier_secret
cat dossier_secret/info.txt
```

Tu constates que sans `x` sur un dossier, tu ne peux pas accéder à son contenu.

### Exercice 5 — Propriétaire et groupe

```bash
sudo useradd -m testeur           # crée un utilisateur de test (VM)
sudo chown testeur:testeur fichier_test.txt
ls -l fichier_test.txt
chmod 600 fichier_test.txt
cat fichier_test.txt              # accès refusé ?
sudo -u testeur cat fichier_test.txt   # accès autorisé
```

Nettoyage à la fin : `sudo userdel -r testeur`.

### Exercice 6 — Audit de base sur ta VM

```bash
# Fichiers SUID
find / -perm -4000 -type f 2>/dev/null

# Fichiers modifiables par tout le monde (hors /proc et /sys)
find / -xdev -type f -perm -0002 2>/dev/null | head

# Comptes ayant un shell de connexion
grep -v "nologin\|false" /etc/passwd
```

Questions guidées :
1. Reconnais-tu les programmes SUID listés ? (`passwd`, `sudo`, `mount`… sont normaux.)
2. Y a-t-il des fichiers world-writable en dehors de `/tmp` ? Si oui, pourquoi ?

### Exercice 7 — Calculer l'octal (papier-crayon)

Convertis :

| Symbolique | Octal |
|---|---|
| `rwxr-xr-x` | ? |
| `rw-r-----` | ? |
| `rwx------` | ? |
| `r--r--r--` | ? |

**Corrigé :** 755, 640, 700, 444.

## 🔍 Approfondissement

### Pour aller plus loin

- Le manuel de `chmod`, `chown`, `sudoers` (`man sudoers`).
- GTFOBins (gtfobins.github.io) : référence sur les binaires détournables en cas de mauvaise configuration.
- Le jeu **OverTheWire : Bandit** pour pratiquer les permissions.

### Pièges courants

- ❌ **Erreur fréquente 1** : « ça ne marche pas, donc `chmod 777` ». Cela ouvre une faille sans résoudre la cause.
- ✅ **Bonne pratique** : identifier quel utilisateur a besoin de quel droit, et ne donner que celui-là.
- ❌ **Erreur fréquente 2** : confondre le droit `x` sur un fichier et sur un dossier.
- ✅ **Bonne pratique** : sur un dossier, `x` = « le traverser ».
- ❌ **Erreur fréquente 3** : lancer un serveur web ou une application sous root.
- ✅ **Bonne pratique** : utiliser un compte de service dédié et sans privilèges.
- ❌ **Erreur fréquente 4** : ajouter `NOPASSWD: ALL` dans sudoers « pour simplifier ».
- ✅ **Bonne pratique** : limiter `sudo` à des commandes précises et journaliser son usage.

## 🧪 Quiz de validation

**Question 1 : Que signifie `-rwxr-xr--` ?**
- A) Propriétaire : rwx, groupe : r-x, autres : r-- ✅
- B) Propriétaire : r-x, groupe : rwx, autres : r--
- C) Tout le monde peut tout faire
- D) Fichier exécutable uniquement par root

*Explication : les trois blocs de trois caractères correspondent dans l'ordre au propriétaire, au groupe et aux autres.*

**Question 2 : Quelle est la valeur octale de `rw-r--r--` ?**
- A) 755
- B) 644 ✅
- C) 600
- D) 777

*Explication : rw- = 6, r-- = 4, r-- = 4, donc 644.*

**Question 3 : Quelle commande rend un script exécutable pour son propriétaire ?**
- A) `chown +x script.sh`
- B) `chmod u+x script.sh` ✅
- C) `chmod 000 script.sh`
- D) `exec script.sh`

*Explication : `chmod u+x` ajoute le droit d'exécution au propriétaire.*

**Question 4 : Pourquoi un binaire SUID root mal sécurisé est-il dangereux ?**
- A) Il consomme beaucoup de mémoire
- B) Il s'exécute avec les droits de root et peut être détourné pour élever ses privilèges ✅
- C) Il ne peut pas être supprimé
- D) Il bloque le réseau

*Explication : tout défaut dans un programme SUID root peut donner à un utilisateur ordinaire des droits administrateur.*

**Question 5 : Qui peut lire `/etc/shadow` par défaut ?**
- A) Tous les utilisateurs
- B) Uniquement root (et certains groupes de service) ✅
- C) Uniquement les utilisateurs connectés
- D) Personne, même pas root

*Explication : il contient les empreintes de mots de passe, son accès est donc strictement limité.*

## 📝 Résumé

- Chaque fichier a un propriétaire, un groupe et des droits `r`, `w`, `x` pour user, group et others.
- En octal : r = 4, w = 2, x = 1 ; 755 et 644 sont les valeurs les plus courantes, 777 est à proscrire.
- `chmod` modifie les droits, `chown` le propriétaire, `umask` définit les droits par défaut.
- `sudo` délègue des droits root de façon contrôlée ; on applique le moindre privilège.
- SUID, SGID et sticky bit sont des permissions spéciales : à auditer, car elles sont sensibles.
- Les services doivent tourner sous des comptes dédiés sans privilèges.

## 🎓 Ce que tu as appris

✅ Lire et interpréter les permissions Linux
✅ Modifier droits et propriétaires avec `chmod` et `chown`
✅ Comprendre sudo et les permissions spéciales
✅ Réaliser un audit de base de permissions faibles

## ➡️ Leçon suivante

**12 : Systemd et services** : gérer les services, les démarrages, les journaux avec `systemctl` et `journalctl`, et sécuriser les services. Fichier : `12-systemd-services.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
