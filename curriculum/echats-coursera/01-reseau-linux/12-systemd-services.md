---
title: "Systemd et Gestion des Services"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 35
order: 12
category: "linux"
tags: ["linux", "systemd", "systemctl", "journalctl", "services", "demarrage", "cron"]
prerequisites: ["10-commandes-linux-essentielles", "11-permissions-linux"]
learning_objectives:
  - "Expliquer le rôle de systemd et la notion d'unité"
  - "Démarrer, arrêter, activer et inspecter un service avec systemctl"
  - "Lire les journaux avec journalctl"
  - "Créer un service simple et le durcir"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Systemd et Gestion des Services

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Expliquer le rôle de systemd et la notion d'unité
- Démarrer, arrêter, activer et inspecter un service avec `systemctl`
- Lire les journaux avec `journalctl`
- Créer un service simple et le durcir

## 📚 Prérequis

- Leçon 10 : *Commandes Linux Essentielles*
- Leçon 11 : *Permissions et Utilisateurs Linux*

## 🧭 Introduction

Quand un serveur Linux démarre, il lance des dizaines de programmes en arrière-plan sans que personne ne clique nulle part : serveur web, base de données, accès SSH, pare-feu, planificateur de tâches. Ces programmes qui tournent en continu s'appellent des **services** (ou **démons**).

Quelqu'un doit les démarrer dans le bon ordre, les redémarrer s'ils plantent, et garder trace de ce qu'ils font. Sur la quasi-totalité des distributions modernes (Debian, Ubuntu, Kali, Fedora, CentOS/RHEL), c'est le rôle de **systemd**.

Pour la cybersécurité, systemd est important pour trois raisons :
1. **Savoir ce qui tourne** sur une machine : chaque service actif est une surface d'attaque potentielle.
2. **Investiguer** : les journaux systemd racontent ce qui s'est passé (connexions SSH, erreurs, arrêts suspects).
3. **Persistance** : un attaquant installe souvent un service ou une tâche planifiée pour survivre au redémarrage. Savoir les repérer est une compétence centrale en réponse à incident.

## 📖 Concepts clés

### 1. Du démarrage aux services

Séquence simplifiée du démarrage d'un système Linux :

1. **Firmware** (BIOS/UEFI) : teste le matériel, lance le chargeur de démarrage.
2. **Chargeur de démarrage** (GRUB) : charge le noyau.
3. **Noyau Linux** : initialise le matériel et monte le système de fichiers.
4. **Systemd (PID 1)** : premier processus lancé, il démarre tout le reste.
5. **Services et cible finale** : réseau, SSH, serveur web, interface graphique…

`systemd` porte toujours le **PID 1**. Si tu le tues, le système plante.

### 2. Les unités (units)

Systemd gère des **unités**, décrites par des fichiers de configuration. Les plus courantes :

| Type | Extension | Rôle |
|---|---|---|
| Service | `.service` | Un programme en arrière-plan (ex. `ssh.service`) |
| Socket | `.socket` | Démarre un service à la demande quand une connexion arrive |
| Timer | `.timer` | Déclenche un service à une heure donnée (équivalent moderne de cron) |
| Target | `.target` | Groupe d'unités représentant un état (ex. `multi-user.target`) |
| Mount | `.mount` | Point de montage |

Emplacements des fichiers d'unités :

| Dossier | Contenu |
|---|---|
| `/lib/systemd/system/` ou `/usr/lib/systemd/system/` | Unités installées par les paquets |
| `/etc/systemd/system/` | Unités de l'administrateur (prioritaires) |
| `/run/systemd/system/` | Unités temporaires |

**Pour la sécurité** : `/etc/systemd/system/` est l'endroit à inspecter en priorité à la recherche d'un service ajouté par un attaquant.

### 3. Gérer les services avec systemctl

```bash
# État d'un service
systemctl status ssh

# Démarrer / arrêter / redémarrer
sudo systemctl start ssh
sudo systemctl stop ssh
sudo systemctl restart ssh
sudo systemctl reload ssh      # recharge la configuration sans couper

# Activer / désactiver au démarrage
sudo systemctl enable ssh
sudo systemctl disable ssh
sudo systemctl enable --now ssh     # activer ET démarrer

# Savoir si actif / activé
systemctl is-active ssh
systemctl is-enabled ssh
```

Distinction essentielle :

| | Maintenant | Au prochain démarrage |
|---|---|---|
| `start` / `stop` | Oui | Non |
| `enable` / `disable` | Non | Oui |

Le nom du service SSH est `ssh` sur Debian/Ubuntu et `sshd` sur Red Hat/CentOS/Fedora.

### 4. Lister et inspecter

```bash
systemctl list-units --type=service              # services chargés
systemctl list-units --type=service --state=running
systemctl list-unit-files --type=service         # tous les services et leur activation
systemctl --failed                               # services en échec
systemctl cat ssh                                # affiche le fichier d'unité
systemctl list-timers                            # minuteurs planifiés
```

La sortie de `systemctl status` donne beaucoup d'informations :

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled)
     Active: active (running) since Sat 2026-10-03 09:12:45 WAT; 1h ago
   Main PID: 842 (sshd)
      Tasks: 1
     Memory: 6.4M
```

On y lit : si le service est chargé et activé, son état, son PID, sa consommation et les dernières lignes de journal.

### 5. Les journaux avec journalctl

Systemd centralise les journaux (*logs*) de tous les services dans un **journal binaire** interrogeable par `journalctl` :

```bash
journalctl                          # tout le journal
journalctl -u ssh                   # journaux d'un service
journalctl -u ssh --since "1 hour ago"
journalctl -u ssh --since today --no-pager
journalctl -f                       # suivre en direct (comme tail -f)
journalctl -p err                   # seulement les erreurs et pires
journalctl -b                       # depuis le dernier démarrage
journalctl -b -1                    # du démarrage précédent
journalctl _UID=1000                # activités d'un utilisateur
journalctl --disk-usage             # espace occupé
```

Niveaux de priorité (du plus grave au moins grave) : `emerg`, `alert`, `crit`, `err`, `warning`, `notice`, `info`, `debug`.

**Usage en investigation** : le journal du service SSH montre les connexions réussies et échouées, les adresses d'origine, les comptes ciblés. Une avalanche d'échecs en peu de temps est le signe d'une attaque par forçage de mot de passe.

### 6. Anatomie d'un fichier de service

Exemple de fichier `/etc/systemd/system/mon-app.service` :

```ini
[Unit]
Description=Mon application de démonstration
After=network.target

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/mon-app
ExecStart=/usr/bin/python3 /opt/mon-app/app.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Sections :
- **[Unit]** : description et dépendances (`After`, `Requires`, `Wants`).
- **[Service]** : comment lancer le programme (`ExecStart`), sous quel compte (`User`), quand le relancer (`Restart`).
- **[Install]** : à quelle cible rattacher le service lors de l'activation (`WantedBy`).

Après toute création ou modification d'un fichier d'unité :

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mon-app
```

### 7. Durcir un service avec systemd

Systemd propose de nombreuses options qui **isolent** un service, limitant les dégâts en cas de compromission :

```ini
[Service]
User=appuser
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/mon-app
CapabilityBoundingSet=
RestrictAddressFamilies=AF_INET AF_INET6
```

| Option | Effet |
|---|---|
| `User=` | Le service tourne sous un compte non privilégié |
| `NoNewPrivileges=true` | Interdit l'élévation de privilèges (y compris via SUID) |
| `PrivateTmp=true` | Donne au service son propre `/tmp` isolé |
| `ProtectSystem=strict` | Système de fichiers en lecture seule sauf chemins autorisés |
| `ProtectHome=true` | Cache `/home` au service |
| `ReadWritePaths=` | Seuls chemins où le service peut écrire |
| `RestrictAddressFamilies=` | Limite les types de connexions réseau |

L'outil intégré **`systemd-analyze security <service>`** attribue une note d'exposition à un service et liste les durcissements possibles.

### 8. Les tâches planifiées : cron et timers

Deux mécanismes pour lancer des tâches à heure fixe :

**cron** : le classique.

```bash
crontab -l            # voir les tâches de l'utilisateur courant
crontab -e            # les éditer
```

Format : `minute heure jour mois jour_semaine commande`

```
30 2 * * *  /opt/sauvegarde.sh        # tous les jours à 2h30
*/15 * * * * /usr/bin/curl -s http://exemple.local/ping   # toutes les 15 min
```

Fichiers à connaître : `/etc/crontab`, `/etc/cron.d/`, `/etc/cron.daily/`, `/var/spool/cron/`.

**Timers systemd** : un fichier `.timer` associé à un `.service` (journalisation intégrée, dépendances, exécution manquée rattrapée).

### 9. Services, persistance et réponse à incident

Un attaquant qui prend pied sur une machine veut **survivre** au redémarrage. Il peut :
- créer un **service** dans `/etc/systemd/system/` ;
- ajouter une **tâche cron** ou un **timer** ;
- modifier un service existant ;
- ajouter des commandes dans les fichiers de démarrage du shell.

**Checklist de contrôle d'une machine suspecte (à faire sur *tes* machines ou avec autorisation) :**

```bash
systemctl list-unit-files --state=enabled --type=service
ls -la /etc/systemd/system/
systemctl list-timers --all
crontab -l ; sudo ls -la /etc/cron.* /var/spool/cron/ 2>/dev/null
sudo find /etc/systemd /lib/systemd -newermt "2026-09-25" -type f 2>/dev/null
journalctl -p warning -b | tail -n 50
```

Repère les services au nom étrange, aux chemins inhabituels (`/tmp`, `/dev/shm`), aux dates de création récentes et inexpliquées, ou qui lancent des commandes réseau.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : ces exercices sont à réaliser dans **ta VM ou ta machine**. Ne crée jamais de service ni de tâche planifiée sur un système qui ne t'appartient pas. Attention à ne pas arrêter un service dont dépend ta session (par exemple SSH sur un serveur distant).

### Exercice 1 — Explorer les services de ta machine

```bash
systemctl list-units --type=service --state=running
systemctl list-unit-files --state=enabled --type=service
systemctl --failed
```

Questions guidées :
1. Combien de services tournent ? Lesquels reconnais-tu ?
2. Y en a-t-il que tu ne comprends pas ? Cherche leur rôle avec `systemctl status <nom>` et `man <nom>`.
3. Y a-t-il des services en échec ?

### Exercice 2 — Cycle de vie d'un service

Utilise un service sans risque (ex. `cron`) :

```bash
systemctl status cron
sudo systemctl stop cron
systemctl is-active cron
sudo systemctl start cron
systemctl is-active cron
systemctl is-enabled cron
```

Vérifie que `stop` ne change pas `is-enabled`.

### Exercice 3 — Lire des journaux

```bash
journalctl -u ssh --since today --no-pager | tail -n 20
journalctl -p err -b --no-pager | tail -n 20
journalctl -f              # puis ouvre un autre terminal et fais : sudo ls
                           # Ctrl+C pour arrêter
```

Observe l'apparition de lignes liées à `sudo` en direct. Si SSH n'est pas installé, remplace par un service présent sur ta machine.

### Exercice 4 — Créer ton propre service

1. Crée un script simple :

```bash
sudo mkdir -p /opt/demo
sudo tee /opt/demo/heartbeat.sh > /dev/null << 'EOF'
#!/bin/bash
while true; do
  echo "Service ECHATS actif : $(date)" >> /tmp/heartbeat.log
  sleep 10
done
EOF
sudo chmod 755 /opt/demo/heartbeat.sh
```

2. Crée le fichier d'unité :

```bash
sudo tee /etc/systemd/system/heartbeat.service > /dev/null << 'EOF'
[Unit]
Description=Demo heartbeat ECHATS

[Service]
ExecStart=/opt/demo/heartbeat.sh
Restart=on-failure
NoNewPrivileges=true
PrivateTmp=false

[Install]
WantedBy=multi-user.target
EOF
```

3. Active et teste :

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now heartbeat
systemctl status heartbeat
sleep 25; tail /tmp/heartbeat.log
journalctl -u heartbeat --no-pager | tail
```

4. Fais ensuite planter le service et observe le redémarrage :

```bash
sudo pkill -f heartbeat.sh
sleep 6
systemctl status heartbeat
```

5. **Nettoie** :

```bash
sudo systemctl disable --now heartbeat
sudo rm /etc/systemd/system/heartbeat.service
sudo systemctl daemon-reload
sudo rm -rf /opt/demo /tmp/heartbeat.log
```

### Exercice 5 — Évaluer l'exposition d'un service

```bash
systemd-analyze security ssh
systemd-analyze security | head -n 20
```

Repère la colonne d'exposition : « UNSAFE », « EXPOSED », « MEDIUM », « OK ». Choisis un service bien noté et un mal noté, et compare leurs options.

### Exercice 6 — Chasse à la persistance (sur ta VM)

Exécute la checklist de la section 9. Puis, pour t'entraîner :
1. Crée un service nommé `systeme-mise-a-jour.service` qui écrit une ligne dans un fichier (comme à l'exercice 4).
2. Demande à un camarade, ou retrouve-le toi-même **uniquement avec la checklist**, parmi la liste des services activés.
3. Note les indices qui te l'ont fait repérer (date de création, chemin du script, nom trompeur).
4. Supprime-le.

Cet exercice illustre comment un défenseur retrouve une persistance.

## 🔍 Approfondissement

### Pour aller plus loin

- `man systemd.service`, `man systemd.exec` (options de durcissement), `man journalctl`.
- La documentation de systemd (freedesktop.org) et le wiki ArchWiki sur systemd (en anglais, très complet).
- Module « Linux Fundamentals Part 3 » de TryHackMe.

### Pièges courants

- ❌ **Erreur fréquente 1** : oublier `daemon-reload` après avoir modifié un fichier d'unité.
- ✅ **Bonne pratique** : toujours exécuter `sudo systemctl daemon-reload` après un changement.
- ❌ **Erreur fréquente 2** : confondre `start` et `enable`.
- ✅ **Bonne pratique** : `start` agit maintenant, `enable` agit au prochain démarrage ; `enable --now` fait les deux.
- ❌ **Erreur fréquente 3** : faire tourner un service sous root par facilité.
- ✅ **Bonne pratique** : un compte dédié et les options de durcissement (`NoNewPrivileges`, `ProtectSystem`…).
- ❌ **Erreur fréquente 4** : ne jamais regarder les journaux, ou laisser leur rotation les effacer sans sauvegarde.
- ✅ **Bonne pratique** : centraliser les journaux importants sur une autre machine pour qu'un attaquant ne puisse pas les effacer.

## 🧪 Quiz de validation

**Question 1 : Quel est le rôle de systemd ?**
- A) Un antivirus
- B) Le premier processus (PID 1), qui démarre et gère les services ✅
- C) Un éditeur de texte
- D) Un pare-feu

*Explication : systemd initialise l'espace utilisateur, lance les services et surveille leur état.*

**Question 2 : Quelle commande active un service au démarrage ET le lance immédiatement ?**
- A) `systemctl start --enable`
- B) `systemctl enable --now service` ✅
- C) `systemctl boot service`
- D) `systemctl on service`

*Explication : `enable` configure le démarrage automatique, `--now` démarre aussi le service tout de suite.*

**Question 3 : Quelle commande affiche les journaux d'un service nommé `ssh` ?**
- A) `systemctl logs ssh`
- B) `cat /var/ssh.log`
- C) `journalctl -u ssh` ✅
- D) `ssh --journal`

*Explication : `journalctl -u` filtre le journal systemd sur une unité précise.*

**Question 4 : Après modification d'un fichier `.service`, que faut-il exécuter ?**
- A) `systemctl daemon-reload` ✅
- B) `reboot` obligatoirement
- C) `chmod 777`
- D) Rien du tout

*Explication : systemd doit relire les fichiers d'unité pour prendre en compte les changements.*

**Question 5 : Pourquoi inspecter `/etc/systemd/system/` lors d'une investigation ?**
- A) Pour y trouver des documents personnels
- B) Parce qu'un attaquant peut y ajouter un service assurant sa persistance ✅
- C) Pour modifier le noyau
- D) Pour changer l'heure

*Explication : un service malveillant installé là redémarre automatiquement avec la machine.*

## 📝 Résumé

- Systemd (PID 1) démarre et supervise les services, décrits par des unités (`.service`, `.timer`, `.target`…).
- `systemctl` gère l'état (start, stop, restart) et le démarrage automatique (enable, disable) ; `list-units`, `status`, `--failed` aident à inspecter.
- `journalctl` permet de lire, filtrer et suivre les journaux de tous les services.
- Un fichier d'unité comporte les sections `[Unit]`, `[Service]` et `[Install]` ; `daemon-reload` est nécessaire après toute modification.
- Les options `User`, `NoNewPrivileges`, `ProtectSystem`, `PrivateTmp` durcissent un service ; `systemd-analyze security` évalue son exposition.
- Services, cron et timers sont des mécanismes de persistance classiques à contrôler lors d'une analyse.

## 🎓 Ce que tu as appris

✅ Gérer et inspecter des services avec `systemctl`
✅ Exploiter les journaux avec `journalctl`
✅ Créer et durcir un service systemd
✅ Repérer les traces de persistance sur une machine

## ➡️ Leçon suivante

**13 : Bash scripting** : variables, conditions, boucles, fonctions et automatisation de tâches de sécurité. Fichier : `13-bash-scripting.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
