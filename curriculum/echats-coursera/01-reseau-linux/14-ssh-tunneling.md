---
title: "SSH et Tunneling"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 14
category: "reseau"
tags: ["ssh", "tunnel", "cles", "port-forwarding", "scp", "durcissement", "fail2ban"]
prerequisites: ["03-tcp-ip", "11-permissions-linux", "12-systemd-services"]
learning_objectives:
  - "Se connecter à une machine distante avec SSH et des clés"
  - "Transférer des fichiers de manière sécurisée avec scp et sftp"
  - "Comprendre et utiliser les redirections de ports (tunnels SSH)"
  - "Durcir la configuration d'un serveur SSH"
author: "ECHATS PRO"
language: "fr"
published: true
---

# SSH et Tunneling

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Te connecter à une machine distante avec SSH et des clés
- Transférer des fichiers de manière sécurisée avec `scp` et `sftp`
- Comprendre et utiliser les redirections de ports (tunnels SSH)
- Durcir la configuration d'un serveur SSH

## 📚 Prérequis

- Leçon 03 : *TCP/IP* (ports, connexions)
- Leçon 11 : *Permissions Linux*
- Leçon 12 : *Systemd et services* (gérer le service `ssh`)

## 🧭 Introduction

Un administrateur à Brazzaville doit intervenir sur un serveur hébergé à l'autre bout du monde. Comment prendre le contrôle de cette machine à distance, sans que personne n'espionne les commandes ni ne vole son mot de passe ? Avec **SSH** (*Secure Shell*).

SSH est le protocole standard d'administration à distance sous Linux et pour les équipements réseau. Il remplace l'ancien **Telnet**, qui envoyait tout en clair, mots de passe compris. SSH chiffre la connexion, authentifie le serveur et permet d'authentifier l'utilisateur par mot de passe ou, mieux, par **clé cryptographique**.

SSH est aussi un excellent sujet de sécurité : c'est l'une des cibles les plus attaquées d'Internet. Des robots balayent en permanence les serveurs en essayant des mots de passe courants sur le port 22. Savoir configurer SSH proprement est donc l'une des premières choses qu'un défenseur doit maîtriser. Enfin, SSH permet de créer des **tunnels** : des canaux chiffrés qui transportent d'autres protocoles, outil précieux pour l'administration comme pour le contournement de restrictions *légitimes* d'un laboratoire, mais aussi une technique à surveiller dans un réseau d'entreprise.

## 📖 Concepts clés

### 1. Comment SSH protège la connexion

1. **Authentification du serveur** : à la première connexion, le serveur présente son **empreinte de clé** (*host key fingerprint*). Le client la mémorise dans `~/.ssh/known_hosts`. Si elle change plus tard, SSH alerte : cela peut signaler une usurpation (homme du milieu) ou une réinstallation du serveur.
2. **Échange de clés** : client et serveur créent une clé de session secrète.
3. **Canal chiffré** : tout ce qui suit (identifiants, commandes, résultats) est chiffré et protégé contre la modification.
4. **Authentification de l'utilisateur** : par mot de passe ou par clé publique.

SSH utilise par défaut le **port TCP 22**.

### 2. Se connecter

```bash
ssh utilisateur@adresse
ssh etudiant@192.168.1.50
ssh -p 2222 etudiant@serveur.exemple.org     # port non standard
ssh etudiant@192.168.1.50 "uptime"           # exécute une commande et revient
```

À la première connexion :

```
The authenticity of host '192.168.1.50' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxx...
Are you sure you want to continue connecting (yes/no)?
```

**Ne réponds pas « yes » à la légère** : vérifie l'empreinte par un autre canal (l'administrateur du serveur, la console du fournisseur).

Pour quitter : `exit` ou `Ctrl+D`.

### 3. L'authentification par clés

Un mot de passe peut être deviné, volé ou réutilisé. Une **paire de clés** est bien plus solide :
- la **clé privée** reste **secrète** sur ton ordinateur ;
- la **clé publique** se dépose sur le serveur, dans `~/.ssh/authorized_keys`.

Au lieu d'envoyer un secret, le client **prouve qu'il possède la clé privée** par un défi cryptographique. Rien de secret ne circule sur le réseau.

Générer une paire :

```bash
ssh-keygen -t ed25519 -C "etudiant@echats"
# Choisis un emplacement (par défaut ~/.ssh/id_ed25519)
# Définis une PASSPHRASE : elle protège la clé privée si elle est volée
```

Fichiers créés :
- `~/.ssh/id_ed25519` : **clé privée** (permissions **600**, ne jamais partager) ;
- `~/.ssh/id_ed25519.pub` : **clé publique** (partageable).

Copier la clé publique sur le serveur :

```bash
ssh-copy-id etudiant@192.168.1.50
```

Ensuite, `ssh etudiant@192.168.1.50` n'exige que la passphrase de ta clé (ou rien si tu utilises un agent).

**Permissions obligatoires** (sinon SSH refuse de les utiliser) :

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/authorized_keys
```

**ssh-agent** garde la clé déchiffrée en mémoire le temps de la session, pour ne pas retaper la passphrase :

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 4. Le fichier de configuration client

`~/.ssh/config` simplifie les connexions :

```
Host serveur-web
    HostName 192.168.1.50
    User etudiant
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host *
    ServerAliveInterval 60
```

Il suffit alors de taper `ssh serveur-web`.

### 5. Transférer des fichiers

**scp** (copie sécurisée) :

```bash
scp rapport.pdf etudiant@192.168.1.50:/home/etudiant/        # local → distant
scp etudiant@192.168.1.50:/var/log/auth.log ./               # distant → local
scp -r dossier/ etudiant@192.168.1.50:/tmp/                  # dossier entier
```

**sftp** (session interactive, commandes `get`, `put`, `ls`, `cd`) :

```bash
sftp etudiant@192.168.1.50
sftp> put fichier.txt
sftp> get journal.log
sftp> exit
```

**rsync** sur SSH, pratique pour des sauvegardes :

```bash
rsync -avz -e ssh dossier/ etudiant@192.168.1.50:/sauvegardes/
```

### 6. Les tunnels SSH (redirection de ports)

Un **tunnel SSH** fait passer du trafic quelconque à l'intérieur d'une connexion SSH chiffrée. Trois types.

**a) Redirection locale (`-L`)** : « j'ouvre un port **chez moi** qui mène à un service **accessible depuis le serveur** ».

```bash
ssh -L 8080:127.0.0.1:80 etudiant@serveur
```

Après cette commande, ouvrir `http://localhost:8080` sur ta machine affiche ce que sert le port 80 **vu depuis le serveur**.

Schéma :

```
[ton navigateur] → localhost:8080 ═══ tunnel SSH ═══> [serveur] → 127.0.0.1:80
```

Cas d'usage légitime : accéder à une interface d'administration qui n'écoute que sur `127.0.0.1` du serveur (une base de données, un panneau de supervision) **sans l'exposer sur Internet**. C'est beaucoup plus sûr que d'ouvrir ce port au public.

**b) Redirection distante (`-R`)** : « j'ouvre un port **sur le serveur** qui mène vers un service **chez moi** ».

```bash
ssh -R 9000:127.0.0.1:3000 etudiant@serveur
```

Utile pour montrer temporairement un site de développement local. **Attention en sécurité** : un `-R` permet de **faire entrer** du trafic dans un réseau depuis l'extérieur à travers un canal sortant autorisé. Les équipes de défense surveillent ce type de tunnels, car des attaquants peuvent les utiliser pour contourner un pare-feu.

**c) Redirection dynamique (`-D`)** : crée un **proxy SOCKS** local.

```bash
ssh -D 1080 etudiant@serveur
```

Tu configures ensuite ton navigateur pour utiliser le proxy SOCKS `127.0.0.1:1080` : tout son trafic web transite par le serveur SSH (chiffré jusqu'au serveur). Utile pour sécuriser sa navigation sur un Wi-Fi public avec un serveur dont on est responsable.

Options pratiques : `-N` (ne pas ouvrir de shell, seulement le tunnel), `-f` (passer en arrière-plan), `-J` (rebond via un hôte intermédiaire, « jump host »).

```bash
ssh -N -f -L 5433:127.0.0.1:5432 etudiant@serveur     # tunnel vers une base PostgreSQL distante
ssh -J bastion@passerelle.exemple.org etudiant@serveur-interne
```

Le **bastion** (ou « jump host ») est une machine unique, bien protégée, par laquelle passent toutes les administrations d'un réseau interne : bonne pratique d'architecture.

### 7. Durcir un serveur SSH

Le fichier de configuration du serveur est `/etc/ssh/sshd_config`. Réglages recommandés :

```
Port 22                      # changer le port réduit le bruit mais N'EST PAS une vraie protection
PermitRootLogin no           # interdit la connexion directe en root
PasswordAuthentication no    # uniquement les clés (après les avoir déployées !)
PubkeyAuthentication yes
PermitEmptyPasswords no
MaxAuthTries 3
LoginGraceTime 30
AllowUsers etudiant admin    # liste blanche d'utilisateurs
X11Forwarding no
AllowTcpForwarding no        # sauf si les tunnels sont nécessaires
ClientAliveInterval 300
ClientAliveCountMax 2
```

⚠️ **Procédure sûre pour ne pas te couper l'accès :**
1. garde une session SSH **ouverte** pendant la modification ;
2. teste la configuration : `sudo sshd -t` ;
3. recharge : `sudo systemctl reload ssh` ;
4. ouvre une **nouvelle** session pour vérifier qu'elle fonctionne **avant** de fermer l'ancienne.

**Mesures complémentaires :**
- **fail2ban** : bannit automatiquement les adresses IP qui échouent plusieurs fois.
- **Pare-feu** : n'autoriser SSH que depuis des adresses connues (voir leçon 09).
- **Authentification à deux facteurs** (clé + code temporaire) pour les serveurs sensibles.
- **Mises à jour** régulières d'OpenSSH.
- **Journalisation** : surveiller `journalctl -u ssh` ou `/var/log/auth.log`.

### 8. Ce que montrent les journaux

Un échec de connexion typique :

```
Failed password for invalid user admin from 203.0.113.77 port 51822 ssh2
```

Une connexion réussie :

```
Accepted publickey for etudiant from 192.168.1.20 port 40322 ssh2
```

Indices d'attaque : rafales d'échecs en quelques secondes, noms d'utilisateurs génériques (`admin`, `root`, `test`, `oracle`), provenance d'adresses multiples. Avec l'authentification par clé uniquement, ces tentatives échouent toutes.

### 9. SSH et sécurité : points d'attention

- **Perte ou vol de la clé privée** : sans passphrase, le voleur accède à tous les serveurs qui font confiance à cette clé. Protège-la, et retire sa clé publique des `authorized_keys` en cas de doute.
- **Clés partagées ou oubliées** : tout compte quitté doit voir sa clé publique supprimée.
- **Agent forwarding (`-A`)** : transmet ton agent au serveur ; si ce serveur est compromis, l'attaquant peut utiliser ton agent le temps de la session. À éviter, préférer `-J`.
- **Tunnels non contrôlés** : un utilisateur peut créer un tunnel qui contourne le pare-feu de l'entreprise ; la politique de sécurité doit définir ce qui est permis.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : connecte-toi uniquement à **tes machines** (VM, Raspberry Pi, serveur personnel) ou à des systèmes sur lesquels tu as une **autorisation écrite**. Tenter de deviner des mots de passe SSH sur un serveur qui ne t'appartient pas est une infraction.

### Exercice 1 — Installer un serveur SSH sur ta VM

```bash
sudo apt update && sudo apt install openssh-server
sudo systemctl enable --now ssh
systemctl status ssh
ss -tln | grep :22
ip -4 addr show       # note l'adresse IP de la VM
```

Depuis ta machine hôte (ou une deuxième VM) :

```bash
ssh etudiant@<ip-de-la-vm>
```

Observe l'avertissement d'empreinte à la première connexion. Regarde le fichier `~/.ssh/known_hosts` ensuite.

### Exercice 2 — Passer aux clés

```bash
ssh-keygen -t ed25519 -C "labo-echats"
ssh-copy-id etudiant@<ip-de-la-vm>
ssh etudiant@<ip-de-la-vm>      # te demande seulement la passphrase de la clé
ls -l ~/.ssh
```

Vérifie les permissions de `~/.ssh` et de la clé privée.

### Exercice 3 — Transfert de fichiers

```bash
echo "Test ECHATS" > test.txt
scp test.txt etudiant@<ip-de-la-vm>:/tmp/
ssh etudiant@<ip-de-la-vm> "cat /tmp/test.txt"
scp etudiant@<ip-de-la-vm>:/etc/hostname ./hostname_distant.txt
```

### Exercice 4 — Un tunnel local

Sur la VM, démarre un serveur web local lié à `127.0.0.1` uniquement :

```bash
# sur la VM
mkdir -p ~/site && echo "<h1>Page privée de la VM</h1>" > ~/site/index.html
cd ~/site && python3 -m http.server 8000 --bind 127.0.0.1
```

Depuis ta machine :
1. essaie `curl http://<ip-de-la-vm>:8000` : échec (le service n'écoute que sur la boucle locale) ;
2. crée le tunnel :

```bash
ssh -N -L 8080:127.0.0.1:8000 etudiant@<ip-de-la-vm>
```

3. dans un autre terminal : `curl http://localhost:8080` : tu obtiens « Page privée de la VM ».

Tu viens d'accéder à un service **non exposé** à travers un tunnel chiffré.

### Exercice 5 — Proxy SOCKS

```bash
ssh -N -D 1080 etudiant@<ip-de-la-vm>
curl --socks5-hostname 127.0.0.1:1080 http://example.com
```

Le trafic de `curl` passe par la VM.

### Exercice 6 — Durcir le serveur (sur ta VM)

1. Garde une session SSH ouverte.
2. Édite `sudo nano /etc/ssh/sshd_config` : applique `PermitRootLogin no`, `PasswordAuthentication no`, `MaxAuthTries 3`.
3. `sudo sshd -t` : aucune sortie = configuration valide.
4. `sudo systemctl reload ssh`.
5. Ouvre une **nouvelle** session : doit fonctionner avec la clé.
6. Essaie de te connecter avec un mot de passe depuis une autre machine sans clé : l'accès est refusé.

### Exercice 7 — Lire les journaux et installer fail2ban

```bash
journalctl -u ssh --since "30 min ago" --no-pager | tail -n 20
sudo apt install fail2ban
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
```

Fais volontairement 4 ou 5 tentatives avec un mauvais mot de passe depuis une **de tes** machines et observe le bannissement (`sudo fail2ban-client status sshd`). Débanne-la ensuite : `sudo fail2ban-client set sshd unbanip <ip>`.

## 🔍 Approfondissement

### Pour aller plus loin

- `man ssh`, `man sshd_config`, `man ssh_config`.
- Les recommandations de l'ANSSI sur l'usage d'OpenSSH (guide en français).
- Le module « SSH » de TryHackMe et le jeu **OverTheWire : Bandit**, qui se joue entièrement en SSH.

### Pièges courants

- ❌ **Erreur fréquente 1** : désactiver l'authentification par mot de passe avant d'avoir testé la clé, et se retrouver bloqué.
- ✅ **Bonne pratique** : tester la clé et garder une session ouverte avant de désactiver le mot de passe.
- ❌ **Erreur fréquente 2** : clé privée sans passphrase, ou envoyée par e-mail, ou publiée sur un dépôt Git.
- ✅ **Bonne pratique** : passphrase, permissions 600, et ne jamais publier une clé privée. Si c'est arrivé, révoquer la clé.
- ❌ **Erreur fréquente 3** : croire que changer le port 22 sécurise le serveur.
- ✅ **Bonne pratique** : c'est une réduction du bruit, pas une protection. Les clés, le pare-feu et fail2ban comptent bien plus.
- ❌ **Erreur fréquente 4** : accepter aveuglément une nouvelle empreinte de serveur ou ignorer l'alerte « REMOTE HOST IDENTIFICATION HAS CHANGED ».
- ✅ **Bonne pratique** : vérifier l'empreinte hors bande, et enquêter si elle change sans raison.

## 🧪 Quiz de validation

**Question 1 : Quel est le port par défaut de SSH ?**
- A) 21
- B) 22 ✅
- C) 23
- D) 80

*Explication : 21 est FTP, 23 Telnet, 80 HTTP ; SSH utilise TCP 22.*

**Question 2 : Quelle clé doit rester secrète ?**
- A) La clé publique
- B) La clé privée ✅
- C) Les deux
- D) Aucune

*Explication : la clé privée prouve ton identité ; la publique peut être déposée sur les serveurs.*

**Question 3 : Que fait `ssh -L 8080:127.0.0.1:80 user@serveur` ?**
- A) Il ouvre le port 8080 sur le serveur
- B) Il ouvre le port local 8080 qui mène au port 80 vu depuis le serveur, via un tunnel chiffré ✅
- C) Il copie un fichier
- D) Il supprime la connexion

*Explication : c'est une redirection locale (-L) : le trafic vers localhost:8080 est transporté par SSH jusqu'au port 80 côté serveur.*

**Question 4 : Quel réglage empêche la connexion directe du compte administrateur ?**
- A) `PermitRootLogin no` ✅
- B) `X11Forwarding yes`
- C) `PermitEmptyPasswords yes`
- D) `Port 22`

*Explication : l'interdiction de la connexion root oblige à passer par un compte nominatif puis `sudo`, ce qui améliore la traçabilité.*

**Question 5 : Quel outil bannit automatiquement les adresses qui multiplient les échecs de connexion ?**
- A) nmap
- B) fail2ban ✅
- C) scp
- D) tcpdump

*Explication : fail2ban analyse les journaux et ajoute des règles de pare-feu contre les adresses insistantes.*

## 📝 Résumé

- SSH chiffre la connexion, authentifie le serveur (empreinte, `known_hosts`) et l'utilisateur (mot de passe ou clé).
- L'authentification par paire de clés (ed25519) avec passphrase est bien plus sûre que les mots de passe.
- `scp`, `sftp` et `rsync` transfèrent des fichiers via SSH.
- Les tunnels `-L`, `-R` et `-D` transportent d'autres protocoles dans SSH ; utiles pour l'administration, à surveiller en sécurité.
- Durcir : pas de root, pas de mot de passe, liste blanche d'utilisateurs, `MaxAuthTries`, pare-feu, fail2ban, mises à jour.
- Toujours tester une modification de configuration SSH avec une session de secours ouverte.

## 🎓 Ce que tu as appris

✅ Te connecter à distance avec SSH et des clés
✅ Transférer des fichiers de façon sécurisée
✅ Créer des tunnels SSH locaux et dynamiques
✅ Durcir un serveur SSH et lire ses journaux

## ➡️ Leçon suivante

**15 : Analyse réseau avec Wireshark** : capturer, filtrer et interpréter le trafic réseau sur ton propre réseau. Fichier : `15-wireshark-analyse.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
