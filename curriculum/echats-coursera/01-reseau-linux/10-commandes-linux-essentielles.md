---
title: "Commandes Linux Essentielles"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 40
order: 10
category: "linux"
tags: ["linux", "terminal", "bash", "commandes", "fichiers", "pipes", "grep"]
prerequisites: []
learning_objectives:
  - "Naviguer dans l'arborescence Linux au terminal"
  - "Créer, copier, déplacer et supprimer fichiers et dossiers"
  - "Lire et filtrer du texte avec cat, grep, head, tail"
  - "Enchaîner des commandes avec les redirections et les pipes"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Commandes Linux Essentielles

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Naviguer dans l'arborescence Linux au terminal
- Créer, copier, déplacer et supprimer fichiers et dossiers
- Lire et filtrer du texte avec `cat`, `grep`, `head`, `tail`
- Enchaîner des commandes avec les redirections et les pipes

## 📚 Prérequis

Aucun prérequis technique. Il te faut seulement un environnement Linux : une machine Linux, une machine virtuelle (VirtualBox avec Ubuntu ou Kali), WSL sous Windows, ou un terminal en ligne.

## 🧭 Introduction

Presque tous les serveurs d'Internet tournent sous Linux. La majorité des outils de cybersécurité (Nmap, Wireshark, Metasploit, Burp, outils d'analyse forensic) sont conçus pour Linux ou y fonctionnent le mieux. Les plateformes de CTF et de formation comme ECHATS PRO s'appuient sur des machines Linux. Si tu veux travailler en cybersécurité, **le terminal Linux est ton outil de base**.

Le terminal peut paraître intimidant : pas de boutons, juste un curseur qui clignote. Mais il est en réalité plus puissant et plus rapide que l'interface graphique, une fois qu'on connaît une vingtaine de commandes. Il permet aussi d'**automatiser** : une tâche que tu feras mille fois peut être scriptée une fois pour toutes.

Cette leçon te donne le socle : se repérer, manipuler des fichiers, lire du texte et enchaîner les commandes. Pratique chaque exemple : on n'apprend pas le terminal en lisant, mais en tapant.

## 📖 Concepts clés

### 1. Le terminal, le shell et l'invite de commande

Le **terminal** est la fenêtre. Le **shell** (le plus courant : **bash**) est le programme qui interprète tes commandes. L'**invite** (*prompt*) ressemble à :

```
etudiant@laboratoire:~$
```

- `etudiant` : ton nom d'utilisateur ;
- `laboratoire` : le nom de la machine ;
- `~` : le dossier courant (`~` = ton dossier personnel) ;
- `$` : tu es un utilisateur normal (`#` signale l'administrateur **root**).

Une commande s'écrit : `commande [options] [arguments]`. Exemple : `ls -l /etc`.
- `ls` : la commande ;
- `-l` : une option ;
- `/etc` : l'argument.

> 💡 **Astuces** : `Tab` complète automatiquement un nom ; flèche haut rappelle les commandes précédentes ; `Ctrl+C` interrompt une commande ; `Ctrl+L` nettoie l'écran.

### 2. L'arborescence Linux

Tout part de la **racine** `/`. Pas de lecteurs C: ou D: : tout est dans un seul arbre.

| Dossier | Contenu |
|---|---|
| `/` | Racine du système |
| `/home` | Dossiers personnels des utilisateurs |
| `/root` | Dossier personnel de l'administrateur |
| `/etc` | Fichiers de configuration |
| `/var` | Données variables : journaux (`/var/log`), sites web (`/var/www`) |
| `/tmp` | Fichiers temporaires |
| `/bin`, `/usr/bin` | Programmes (commandes) |
| `/dev` | Périphériques (disques, terminaux) |
| `/proc` | Informations sur les processus et le noyau |

Un **chemin absolu** commence par `/` (ex. `/home/etudiant/notes.txt`). Un **chemin relatif** part du dossier courant. Raccourcis : `.` = dossier courant, `..` = dossier parent, `~` = dossier personnel.

**Important** : Linux est **sensible à la casse**. `Notes.txt` et `notes.txt` sont deux fichiers différents.

### 3. Se repérer et se déplacer

| Commande | Rôle | Exemple |
|---|---|---|
| `pwd` | Affiche le dossier courant | `pwd` |
| `ls` | Liste le contenu | `ls -la` (détails + fichiers cachés) |
| `cd` | Change de dossier | `cd /etc`, `cd ..`, `cd ~`, `cd -` |
| `tree` | Affiche l'arbre (si installé) | `tree -L 2` |

Les fichiers cachés commencent par un point (`.bashrc`). `ls -la` les montre.

Lecture de `ls -l` :

```
-rw-r--r-- 1 etudiant etudiant 1520 oct  3 10:15 notes.txt
drwxr-xr-x 2 etudiant etudiant 4096 oct  3 09:40 documents
```

- Premier caractère : `-` fichier, `d` dossier ;
- les 9 caractères suivants : permissions (voir leçon 11) ;
- propriétaire, groupe, taille en octets, date, nom.

### 4. Manipuler fichiers et dossiers

| Commande | Rôle | Exemple |
|---|---|---|
| `mkdir` | Créer un dossier | `mkdir projets`, `mkdir -p a/b/c` |
| `touch` | Créer un fichier vide | `touch notes.txt` |
| `cp` | Copier | `cp notes.txt copie.txt`, `cp -r dossier1 dossier2` |
| `mv` | Déplacer / renommer | `mv notes.txt ../`, `mv ancien.txt nouveau.txt` |
| `rm` | Supprimer | `rm notes.txt`, `rm -r dossier` |
| `rmdir` | Supprimer un dossier vide | `rmdir vide` |

⚠️ **Il n'y a pas de corbeille en ligne de commande.** `rm` supprime **définitivement**. Quelques précautions :
- utilise `rm -i` (demande confirmation) tant que tu débutes ;
- relis ta commande **avant** d'appuyer sur Entrée ;
- ne tape jamais `rm -rf` avec un chemin que tu ne maîtrises pas, surtout en administrateur.

### 5. Lire et afficher du contenu

| Commande | Rôle |
|---|---|
| `cat fichier` | Affiche tout le fichier |
| `less fichier` | Lecture paginée (`q` pour quitter, `/mot` pour chercher) |
| `head -n 10 fichier` | Les 10 premières lignes |
| `tail -n 10 fichier` | Les 10 dernières lignes |
| `tail -f fichier` | Suit un fichier en temps réel (très utile pour les journaux) |
| `wc -l fichier` | Compte les lignes (`-w` mots, `-c` octets) |
| `file fichier` | Identifie le type réel d'un fichier |
| `echo "texte"` | Affiche du texte |

### 6. Chercher : grep, find, locate

**`grep`** cherche un motif **dans le contenu** des fichiers :

```bash
grep "erreur" journal.log          # lignes contenant « erreur »
grep -i "erreur" journal.log       # insensible à la casse
grep -n "erreur" journal.log       # avec numéro de ligne
grep -v "info" journal.log         # lignes NE contenant PAS « info »
grep -r "mot" /chemin/             # recherche récursive dans un dossier
grep -c "erreur" journal.log       # compte les occurrences
```

**`find`** cherche des **fichiers** (par nom, type, taille, date) :

```bash
find /home -name "*.txt"           # fichiers .txt
find . -type d -name "projets"     # dossiers nommés « projets »
find / -size +100M 2>/dev/null     # fichiers de plus de 100 Mo
find . -mtime -1                   # modifiés depuis moins d'1 jour
```

(`2>/dev/null` masque les messages d'erreur « Permission refusée ».)

**`locate`** retrouve un fichier très vite grâce à une base indexée (mise à jour avec `sudo updatedb`).

### 7. Redirections et pipes : le cœur de la puissance Linux

Chaque programme possède trois flux : **entrée standard (stdin)**, **sortie standard (stdout)**, **erreurs (stderr)**.

| Symbole | Effet | Exemple |
|---|---|---|
| `>` | Écrit la sortie dans un fichier (écrase) | `ls > liste.txt` |
| `>>` | Ajoute à la fin d'un fichier | `echo "ligne" >> liste.txt` |
| `<` | Lit l'entrée depuis un fichier | `wc -l < liste.txt` |
| `2>` | Redirige les erreurs | `commande 2> erreurs.txt` |
| `\|` (pipe) | Envoie la sortie d'une commande vers l'entrée de la suivante | `ls \| wc -l` |

Le **pipe** permet de construire des « chaînes de montage » à partir de petits outils :

```bash
# Combien de fichiers .log dans /var/log ?
ls /var/log | grep ".log" | wc -l

# Les 5 lignes d'erreur les plus récentes
grep -i "error" /var/log/syslog | tail -n 5

# Lister les utilisateurs du système, triés
cut -d: -f1 /etc/passwd | sort
```

Quelques outils de traitement de texte à connaître : `sort` (trier), `uniq` (dédoublonner, avec `-c` pour compter), `cut` (extraire des colonnes), `tr` (remplacer des caractères), `awk` et `sed` (traitements avancés).

### 8. Aide et documentation

```bash
man ls              # manuel de la commande ls (q pour quitter)
ls --help           # aide rapide
whatis ls           # description en une ligne
which python3       # où se trouve une commande
type cd             # type de commande
```

Savoir lire un `man` est une compétence clé : c'est la documentation officielle, toujours disponible hors ligne.

### 9. Processus et système

| Commande | Rôle |
|---|---|
| `whoami` | Qui suis-je ? |
| `id` | Mon identifiant, mes groupes |
| `hostname` | Nom de la machine |
| `uname -a` | Informations sur le système et le noyau |
| `date` | Date et heure |
| `uptime` | Depuis quand la machine tourne |
| `ps aux` | Liste des processus |
| `top` / `htop` | Processus en temps réel |
| `kill PID` | Arrête un processus (par son numéro) |
| `df -h` | Espace disque par partition |
| `du -sh dossier` | Taille d'un dossier |
| `free -h` | Mémoire utilisée |

### 10. Droits d'administrateur : sudo

La plupart des commandes d'administration exigent des privilèges **root**. On utilise **`sudo`** pour exécuter **une commande** avec ces droits :

```bash
sudo apt update          # mettre à jour la liste des paquets
sudo apt install nmap    # installer un programme
```

Principe de sécurité : **ne travaille pas en root en permanence**. Utilise un compte normal et `sudo` seulement quand c'est nécessaire.

### 11. Gérer les paquets (Debian, Ubuntu, Kali)

```bash
sudo apt update              # actualise la liste
sudo apt upgrade             # met à jour les programmes installés
sudo apt install <paquet>    # installe
sudo apt remove <paquet>     # désinstalle
apt search <mot>             # cherche un paquet
```

Mettre à jour régulièrement est la mesure de sécurité la plus rentable.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : ces exercices se font sur **ta machine ou une VM**. Les commandes de suppression sont définitives : travaille dans un dossier de test créé pour l'occasion.

### Exercice 1 — Se repérer

```bash
pwd
ls
ls -la
cd /
ls
cd /etc
pwd
cd ~
pwd
```

Questions guidées :
1. Où es-tu après `cd ~` ? (Dans ton dossier personnel.)
2. Que fait `cd ..` depuis `/home/etudiant` ? (Tu montes à `/home`.)

### Exercice 2 — Créer une petite arborescence

```bash
cd ~
mkdir -p laboratoire/notes laboratoire/scripts laboratoire/logs
cd laboratoire
touch notes/linux.txt notes/reseau.txt
echo "Premier cours de Linux" > notes/linux.txt
echo "Adressage IP et DNS" >> notes/linux.txt
cat notes/linux.txt
tree .        # ou : ls -R
```

Résultat attendu : le fichier `linux.txt` contient deux lignes.

### Exercice 3 — Copier, déplacer, supprimer

```bash
cp notes/linux.txt notes/linux_copie.txt
mv notes/reseau.txt notes/reseaux.txt
ls notes
rm -i notes/linux_copie.txt
ls notes
```

Confirme la suppression quand `rm -i` demande. Vérifie que le fichier a disparu.

### Exercice 4 — Chercher dans un journal

```bash
# Linux courant : journal système
sudo head -n 20 /var/log/syslog        # ou /var/log/auth.log
sudo grep -i "fail" /var/log/auth.log | tail -n 5
sudo grep -c "session opened" /var/log/auth.log
```

(Sur certaines distributions, les noms de fichiers diffèrent : utilise `ls /var/log` pour repérer ce qui existe.)

Question guidée : à quoi sert un journal d'authentification pour un analyste ? (À repérer des tentatives de connexion échouées, donc des attaques par forçage de mot de passe.)

### Exercice 5 — Construire des pipelines

```bash
# 1. Combien d'utilisateurs dans /etc/passwd ?
cat /etc/passwd | wc -l

# 2. Quels sont les shells utilisés, et combien de fois ?
cut -d: -f7 /etc/passwd | sort | uniq -c | sort -nr

# 3. Les 5 plus gros dossiers de /var (peut afficher des erreurs)
sudo du -sh /var/* 2>/dev/null | sort -rh | head -n 5
```

Pour chaque commande, explique chaque maillon du pipe avant d'exécuter, puis compare avec le résultat.

### Exercice 6 — Trouver des fichiers

```bash
find ~ -name "*.txt"
find ~/laboratoire -type f
find /etc -name "*.conf" 2>/dev/null | head
```

### Exercice 7 — Mini-défi : ton premier script de collecte

Crée un fichier `rapport.sh` :

```bash
#!/bin/bash
echo "=== Rapport système ===" > rapport.txt
date >> rapport.txt
whoami >> rapport.txt
hostname >> rapport.txt
uname -a >> rapport.txt
df -h >> rapport.txt
cat rapport.txt
```

Exécute-le :

```bash
chmod +x rapport.sh
./rapport.sh
```

(`chmod` sera expliqué dans la leçon 11. Le script automatise la collecte d'informations de base : c'est un premier geste de réponse à incident.)

## 🔍 Approfondissement

### Pour aller plus loin

- Le jeu **OverTheWire : Bandit** (gratuit) : apprentissage du terminal par des défis progressifs.
- Le module « Linux Fundamentals » de TryHackMe.
- Le livre en ligne « Linux en ligne de commande » et la documentation Ubuntu (en français).

### Pièges courants

- ❌ **Erreur fréquente 1** : `rm -rf` avec un mauvais chemin (par exemple une variable vide qui devient `/`).
- ✅ **Bonne pratique** : relire chaque commande destructive, utiliser `-i`, éviter `rm -rf` en root.
- ❌ **Erreur fréquente 2** : oublier la sensibilité à la casse (`Documents` ≠ `documents`).
- ✅ **Bonne pratique** : utiliser la touche `Tab` pour compléter les noms exactement.
- ❌ **Erreur fréquente 3** : taper des commandes copiées sur Internet sans les comprendre.
- ✅ **Bonne pratique** : lire chaque commande, consulter `man`, tester dans une VM.
- ❌ **Erreur fréquente 4** : travailler en root « pour que ça marche ».
- ✅ **Bonne pratique** : comprendre pourquoi une permission est refusée avant de la contourner avec `sudo`.

## 🧪 Quiz de validation

**Question 1 : Quelle commande affiche le dossier courant ?**
- A) `ls`
- B) `cd`
- C) `pwd` ✅
- D) `whoami`

*Explication : `pwd` (print working directory) affiche le chemin absolu du dossier où tu te trouves.*

**Question 2 : Quelle commande supprime définitivement un dossier et son contenu ?**
- A) `rm -r dossier` ✅
- B) `mv dossier /tmp`
- C) `cp -r dossier`
- D) `rmdir -f dossier`

*Explication : `rm -r` supprime récursivement ; il n'y a pas de corbeille, il faut donc l'utiliser avec prudence.*

**Question 3 : Que fait `grep -i "erreur" journal.log` ?**
- A) Supprime les lignes contenant « erreur »
- B) Cherche « erreur » sans tenir compte de la casse ✅
- C) Remplace « erreur » par « i »
- D) Compte les fichiers

*Explication : `-i` rend la recherche insensible à la casse (erreur, Erreur, ERREUR).*

**Question 4 : Que fait le symbole `|` (pipe) ?**
- A) Il écrit dans un fichier
- B) Il envoie la sortie d'une commande vers l'entrée de la suivante ✅
- C) Il lance une commande en arrière-plan
- D) Il supprime un fichier

*Explication : le pipe permet de chaîner des commandes simples pour effectuer un traitement complexe.*

**Question 5 : Quelle différence entre `>` et `>>` ?**
- A) Aucune
- B) `>` écrase le fichier, `>>` ajoute à la fin ✅
- C) `>` ajoute, `>>` écrase
- D) `>>` lit un fichier

*Explication : `>` remplace le contenu du fichier, `>>` conserve le contenu existant et ajoute à la suite.*

## 📝 Résumé

- Le shell (bash) interprète tes commandes ; tout part de la racine `/`, et Linux est sensible à la casse.
- `pwd`, `ls`, `cd` pour se repérer ; `mkdir`, `touch`, `cp`, `mv`, `rm` pour manipuler ; `cat`, `less`, `head`, `tail` pour lire.
- `grep` cherche dans le contenu, `find` cherche des fichiers.
- Redirections (`>`, `>>`, `2>`) et pipes (`|`) permettent d'enchaîner des outils simples.
- `man` et `--help` donnent la documentation ; `sudo` donne temporairement les droits root.
- Mettre à jour régulièrement (`apt update && apt upgrade`) est une base de sécurité.

## 🎓 Ce que tu as appris

✅ Naviguer et manipuler fichiers et dossiers
✅ Lire, filtrer et chercher dans du texte
✅ Construire des pipelines de commandes
✅ Écrire un premier script de collecte d'informations

## ➡️ Leçon suivante

**11 : Permissions Linux** : lire et modifier les droits (`rwx`), propriétaires, groupes, `chmod`, `chown`, SUID et bonnes pratiques de sécurité. Fichier : `11-permissions-linux.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
