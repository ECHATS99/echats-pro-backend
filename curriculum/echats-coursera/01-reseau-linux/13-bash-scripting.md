---
title: "Bash Scripting pour la Sécurité"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 13
category: "linux"
tags: ["linux", "bash", "script", "automatisation", "variables", "boucles", "fonctions"]
prerequisites: ["10-commandes-linux-essentielles", "11-permissions-linux"]
learning_objectives:
  - "Écrire et exécuter un script Bash avec variables, conditions et boucles"
  - "Utiliser arguments, fonctions et codes de retour"
  - "Automatiser des tâches de contrôle et d'analyse de logs"
  - "Appliquer les bonnes pratiques de sécurité dans un script"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Bash Scripting pour la Sécurité

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Écrire et exécuter un script Bash avec variables, conditions et boucles
- Utiliser arguments, fonctions et codes de retour
- Automatiser des tâches de contrôle et d'analyse de journaux
- Appliquer les bonnes pratiques de sécurité dans un script

## 📚 Prérequis

- Leçon 10 : *Commandes Linux Essentielles*
- Leçon 11 : *Permissions et Utilisateurs Linux*

## 🧭 Introduction

Dans la leçon 10, tu as enchaîné des commandes avec des pipes. Mais si tu dois répéter la même séquence tous les jours, sur dix serveurs, tu ne veux pas la retaper. Tu l'écris **une fois** dans un fichier : c'est un **script**.

Un script Bash est un fichier texte contenant des commandes que le shell exécute les unes après les autres, avec en plus de la logique : variables, conditions, boucles, fonctions. C'est le « couteau suisse » de l'administrateur système et de l'analyste sécurité.

En cybersécurité, on écrit des scripts pour : analyser des journaux, vérifier la configuration de machines, tester l'état de services, sauvegarder des fichiers, automatiser la collecte d'informations lors d'un incident, ou enchaîner des outils pendant un audit autorisé. Beaucoup de professionnels passent à Python pour les tâches plus complexes (module suivant), mais Bash reste imbattable pour la « colle » entre les commandes du système.

## 📖 Concepts clés

### 1. Premier script

Crée `bonjour.sh` :

```bash
#!/bin/bash
# Mon premier script
echo "Bonjour, $USER !"
echo "Nous sommes le $(date +%d/%m/%Y)"
```

- `#!/bin/bash` (le **shebang**) indique quel interpréteur utiliser ;
- `#` introduit un commentaire ;
- `$(commande)` insère la sortie d'une commande.

Exécution :

```bash
chmod +x bonjour.sh
./bonjour.sh
# ou, sans droit d'exécution :
bash bonjour.sh
```

### 2. Variables

```bash
nom="Alice"              # pas d'espaces autour du =
age=25
echo "Je m'appelle $nom"
echo "Dans 5 ans : $((age + 5)) ans"
fichier="/var/log/auth.log"
echo "${nom}_backup"     # accolades pour délimiter le nom
```

Règles :
- **pas d'espace** autour du `=` ;
- on lit une variable avec `$` ;
- les **guillemets doubles** `" "` permettent l'expansion des variables, les **guillemets simples** `' '` affichent le texte tel quel ;
- **toujours** mettre les variables entre guillemets : `"$fichier"` (évite les bugs avec les espaces et les caractères spéciaux).

Variables prédéfinies utiles :

| Variable | Contenu |
|---|---|
| `$0` | Nom du script |
| `$1`, `$2`… | Arguments passés au script |
| `$#` | Nombre d'arguments |
| `$@` | Tous les arguments |
| `$?` | Code de retour de la dernière commande |
| `$USER`, `$HOME` | Utilisateur et dossier personnel |
| `$$` | PID du script |

### 3. Lire une saisie et des arguments

```bash
#!/bin/bash
read -p "Quel est ton nom ? " nom
echo "Salut $nom"

# Arguments
echo "Premier argument : $1"
echo "Nombre d'arguments : $#"
```

Exemple : `./script.sh alpha beta` → `$1` = alpha, `$2` = beta, `$#` = 2.

### 4. Codes de retour

Chaque commande renvoie un **code de retour** : **0** = succès, **non nul** = erreur.

```bash
ls /etc > /dev/null
echo $?        # 0

ls /dossier_inexistant 2> /dev/null
echo $?        # 2
```

On utilise ces codes dans les conditions, et un script bien écrit **retourne un code approprié** avec `exit 0` (succès) ou `exit 1` (erreur).

### 5. Conditions : if, elif, else

```bash
#!/bin/bash
if [ "$1" -gt 10 ]; then
    echo "Plus grand que 10"
elif [ "$1" -eq 10 ]; then
    echo "Égal à 10"
else
    echo "Plus petit que 10"
fi
```

Tests courants (entre `[ ... ]`, avec des espaces à l'intérieur !) :

| Test | Signification |
|---|---|
| `-eq`, `-ne`, `-gt`, `-lt`, `-ge`, `-le` | Comparaisons de nombres |
| `=`, `!=` | Égalité de chaînes |
| `-z "$x"` / `-n "$x"` | Chaîne vide / non vide |
| `-f fichier` | Fichier existe |
| `-d dossier` | Dossier existe |
| `-r`, `-w`, `-x` | Lisible, modifiable, exécutable |
| `&&`, `\|\|` | ET, OU (entre commandes ou tests) |

Raccourcis très utilisés :

```bash
mkdir sauvegarde && echo "Dossier créé"          # si succès
ping -c1 8.8.8.8 > /dev/null || echo "Réseau KO"  # si échec
```

### 6. Boucles

**for** :

```bash
for fruit in pomme banane mangue; do
    echo "J'aime la $fruit"
done

for i in {1..5}; do
    echo "Tour $i"
done

for f in /var/log/*.log; do
    echo "Fichier : $f"
done
```

**while** :

```bash
compteur=1
while [ $compteur -le 3 ]; do
    echo "Compteur : $compteur"
    ((compteur++))
done
```

**Lire un fichier ligne par ligne** :

```bash
while IFS= read -r ligne; do
    echo "Ligne : $ligne"
done < fichier.txt
```

### 7. Fonctions

```bash
#!/bin/bash
verifier_port() {
    local hote="$1"
    local port="$2"
    if timeout 2 bash -c "</dev/tcp/$hote/$port" 2>/dev/null; then
        echo "Port $port ouvert sur $hote"
    else
        echo "Port $port fermé ou filtré sur $hote"
    fi
}

verifier_port 127.0.0.1 22
verifier_port 127.0.0.1 80
```

`local` limite la portée d'une variable à la fonction. Les fonctions rendent un script lisible et réutilisable.

### 8. Traitement de texte avec awk, sed, cut, sort, uniq

Ces outils, associés par des pipes, sont au cœur de l'analyse de journaux.

```bash
# Extraire une colonne
awk '{print $1}' acces.log

# Remplacer du texte
sed 's/ancien/nouveau/g' fichier.txt

# Compter les occurrences par valeur, trier du plus fréquent au moins fréquent
awk '{print $1}' acces.log | sort | uniq -c | sort -nr | head
```

La dernière commande est un classique : elle donne les adresses IP les plus actives dans un journal d'accès web (la première colonne contient l'IP source).

### 9. Un exemple de script de défense : détection d'échecs de connexion

```bash
#!/bin/bash
# Usage : ./echecs_ssh.sh [seuil]
# Liste les adresses IP ayant plus de <seuil> échecs de connexion SSH

seuil="${1:-5}"
journal="/var/log/auth.log"

if [ ! -r "$journal" ]; then
    echo "Erreur : impossible de lire $journal (essaie avec sudo)" >&2
    exit 1
fi

grep "Failed password" "$journal" \
  | grep -oE "from [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" \
  | awk '{print $2}' \
  | sort | uniq -c | sort -nr \
  | awk -v s="$seuil" '$1 > s {print $2 " : " $1 " échecs"}'
```

Explication :
1. vérifie que le journal est lisible, sinon quitte avec un code d'erreur ;
2. extrait les lignes d'échec ;
3. isole l'adresse IP après le mot « from » ;
4. compte les occurrences par IP ;
5. n'affiche que celles qui dépassent le seuil.

`${1:-5}` signifie : « utilise le premier argument, ou 5 s'il n'est pas fourni ».

Un script de ce type alimente ensuite une règle de pare-feu ou un outil comme **fail2ban**, qui automatise le blocage des adresses insistantes.

### 10. Planifier un script

Pour exécuter un script tous les jours à 3h :

```bash
crontab -e
# Ajouter :
0 3 * * * /home/etudiant/scripts/sauvegarde.sh >> /var/log/sauvegarde.log 2>&1
```

Toujours utiliser des **chemins absolus** dans cron, car l'environnement y est minimal.

### 11. Écrire des scripts sûrs

Un script mal écrit peut devenir lui-même une faille. Bonnes pratiques :

| Pratique | Pourquoi |
|---|---|
| `set -euo pipefail` en début de script | Arrête le script en cas d'erreur, de variable non définie ou d'échec dans un pipe |
| Toujours mettre `"$variable"` entre guillemets | Évite les injections de commande et les problèmes d'espaces |
| Valider les arguments et les entrées | Ne jamais faire confiance à ce qu'un utilisateur ou un fichier fournit |
| Ne pas utiliser `eval` sur des données externes | Exécuterait n'importe quelle commande injectée |
| Ne jamais écrire de mot de passe en dur | Les secrets vont dans des variables d'environnement ou un gestionnaire de secrets, avec des droits restreints |
| Fichiers temporaires avec `mktemp` | Évite les noms prévisibles exploitables par un autre utilisateur |
| Droits restrictifs sur le script (`chmod 700`) | Empêche une modification par un autre utilisateur |
| Utiliser `shellcheck` | Outil gratuit qui détecte erreurs et mauvaises pratiques |

Exemple d'**injection de commande** à éviter :

```bash
# DANGEREUX : si $1 contient "; rm -rf ~", il sera exécuté
eval "ping -c1 $1"

# Mieux : pas d'eval, variable entre guillemets, validation
if [[ "$1" =~ ^[a-zA-Z0-9.-]+$ ]]; then
    ping -c1 -- "$1"
else
    echo "Hôte invalide" >&2; exit 1
fi
```

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : tes scripts ne doivent agir que sur **ta machine, ta VM ou des systèmes autorisés par écrit**. Un script qui teste des ports ou des mots de passe sur un système tiers sans autorisation est illégal.

### Exercice 1 — Premier script interactif

Écris `accueil.sh` qui demande ton prénom, puis affiche : « Bienvenue sur ECHATS PRO, <prénom> ! Date : <date> ». Rends-le exécutable et lance-le.

### Exercice 2 — Arguments et conditions

Écris `verifier_fichier.sh` qui :
1. prend un chemin en argument ;
2. affiche une erreur et quitte avec le code 1 si aucun argument n'est fourni ;
3. dit si c'est un fichier, un dossier, ou s'il n'existe pas ;
4. si c'est un fichier, affiche ses permissions avec `ls -l`.

Exemple de solution :

```bash
#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Usage : $0 <chemin>" >&2
    exit 1
fi
if [ -f "$1" ]; then
    echo "$1 est un fichier"
    ls -l -- "$1"
elif [ -d "$1" ]; then
    echo "$1 est un dossier"
else
    echo "$1 n'existe pas"
    exit 2
fi
```

### Exercice 3 — Boucle sur une liste de ports locaux

Reprends la fonction `verifier_port` de la section 7 et fais-la tourner en boucle sur `22 80 443 3306` pour `127.0.0.1` uniquement (ta machine). Comment sais-tu quels ports sont réellement ouverts ? Compare avec `ss -tuln`.

### Exercice 4 — Analyser un journal

1. Crée un faux journal de test :

```bash
cat > acces.log << 'EOF'
192.168.1.10 - - [03/Oct/2026:10:00:01] "GET /index.html" 200
192.168.1.10 - - [03/Oct/2026:10:00:02] "GET /logo.png" 200
10.0.0.5 - - [03/Oct/2026:10:00:03] "GET /admin" 403
10.0.0.5 - - [03/Oct/2026:10:00:04] "GET /admin" 403
10.0.0.5 - - [03/Oct/2026:10:00:05] "GET /login" 200
172.16.0.9 - - [03/Oct/2026:10:00:06] "GET /index.html" 200
EOF
```

2. Écris un pipeline qui affiche les IP classées par nombre de requêtes :

```bash
awk '{print $1}' acces.log | sort | uniq -c | sort -nr
```

3. Écris un pipeline qui compte les réponses 403 par IP :

```bash
grep '" 403' acces.log | awk '{print $1}' | sort | uniq -c
```

Question guidée : que peut signaler un grand nombre de 403 venant d'une même IP ? (Des tentatives d'accès à des ressources interdites, parfois une énumération.)

### Exercice 5 — Script d'audit de ta machine

Écris `audit_local.sh` qui affiche :
- l'utilisateur, le nom de la machine et la date ;
- les ports TCP en écoute (`ss -tuln`) ;
- les comptes ayant un shell de connexion ;
- les 5 plus gros fichiers de ton dossier personnel ;
- l'espace disque disponible.

Utilise `set -euo pipefail`, des fonctions et des sections claires. Enregistre la sortie dans un fichier daté :

```bash
./audit_local.sh > "audit_$(date +%Y%m%d).txt"
```

### Exercice 6 — Défi : script de sauvegarde sécurisée

Écris `sauvegarde.sh` qui :
1. prend un dossier source en argument et vérifie qu'il existe ;
2. crée une archive `tar.gz` datée dans `~/sauvegardes` (créé s'il n'existe pas) ;
3. applique `chmod 600` à l'archive ;
4. conserve seulement les 5 dernières archives ;
5. écrit une ligne de journal avec succès ou échec.

Indices : `tar -czf`, `ls -t`, `tail -n +6`, `xargs rm --`.

### Exercice 7 — Vérifier avec ShellCheck

```bash
sudo apt install shellcheck
shellcheck audit_local.sh
```

Corrige les avertissements. ShellCheck est un excellent professeur.

## 🔍 Approfondissement

### Pour aller plus loin

- Le **Bash Reference Manual** et le *Bash Guide for Beginners* (Linux Documentation Project).
- Le site **shellcheck.net** : colle ton script pour une analyse en ligne.
- Le module « Bash Scripting » de TryHackMe et les défis OverTheWire : Bandit (niveaux avancés).

### Pièges courants

- ❌ **Erreur fréquente 1** : mettre des espaces autour du `=` d'une affectation (`nom = "Alice"`).
- ✅ **Bonne pratique** : `nom="Alice"`, sans espaces.
- ❌ **Erreur fréquente 2** : oublier les guillemets autour des variables.
- ✅ **Bonne pratique** : écrire `"$variable"` partout, sauf cas particuliers.
- ❌ **Erreur fréquente 3** : oublier les espaces dans `[ ... ]` (`[$x -eq 1]` ne marche pas).
- ✅ **Bonne pratique** : `[ "$x" -eq 1 ]`, un espace après `[` et avant `]`.
- ❌ **Erreur fréquente 4** : mots de passe en clair dans un script.
- ✅ **Bonne pratique** : variables d'environnement, fichier de secrets en 600, ou gestionnaire de secrets.

## 🧪 Quiz de validation

**Question 1 : Que signifie `#!/bin/bash` en première ligne ?**
- A) Un commentaire sans importance
- B) Le shebang, qui indique l'interpréteur à utiliser ✅
- C) Une redirection
- D) Une variable

*Explication : le shebang indique au système quel programme exécutera le script.*

**Question 2 : Que contient la variable `$?` ?**
- A) Le nombre d'arguments
- B) Le PID du script
- C) Le code de retour de la dernière commande ✅
- D) Le nom de l'utilisateur

*Explication : 0 signifie succès, toute autre valeur indique une erreur.*

**Question 3 : Quelle écriture d'affectation est correcte ?**
- A) `nom = "Alice"`
- B) `nom="Alice"` ✅
- C) `$nom="Alice"`
- D) `set nom Alice`

*Explication : en Bash, il ne doit y avoir aucun espace autour du signe égal.*

**Question 4 : Pourquoi mettre `"$variable"` entre guillemets ?**
- A) Pour la chiffrer
- B) Pour éviter les erreurs avec les espaces et les caractères spéciaux, et limiter les injections ✅
- C) Pour qu'elle soit plus rapide
- D) C'est purement esthétique

*Explication : sans guillemets, le shell découpe et interprète le contenu, ce qui provoque des bugs et des failles.*

**Question 5 : Que fait `set -euo pipefail` ?**
- A) Il chiffre le script
- B) Il fait échouer le script en cas d'erreur, de variable non définie ou d'échec dans un pipe ✅
- C) Il supprime les commentaires
- D) Il lance le script en arrière-plan

*Explication : ces options rendent le script plus strict et évitent de continuer silencieusement après une erreur.*

## 📝 Résumé

- Un script Bash est un fichier de commandes avec variables, conditions, boucles et fonctions ; le shebang indique l'interpréteur.
- Les arguments (`$1`, `$#`, `$@`) et les codes de retour (`$?`, `exit`) permettent d'écrire des outils réutilisables.
- `awk`, `sed`, `cut`, `sort` et `uniq`, combinés par des pipes, servent à analyser les journaux.
- Planifier avec `cron` automatise les contrôles réguliers.
- Un script sûr utilise `set -euo pipefail`, des guillemets, une validation des entrées, pas d'`eval` sur des données externes et aucun secret en clair.

## 🎓 Ce que tu as appris

✅ Écrire des scripts avec variables, conditions, boucles et fonctions
✅ Analyser un journal pour repérer des activités suspectes
✅ Automatiser et planifier des tâches de contrôle
✅ Éviter les erreurs de sécurité courantes dans les scripts

## ➡️ Leçon suivante

**14 : SSH et tunneling** : connexion sécurisée à distance, clés SSH, durcissement du serveur, redirection de ports. Fichier : `14-ssh-tunneling.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
