## Enrichissement pédagogique — guide opératoire

### Positionnement
Cette leçon transforme la ligne de commande Linux en compétence d’analyse : se repérer, observer sans dégrader, comprendre les privilèges et automatiser des contrôles reproductibles.

### Objectifs observables
L’apprenant sait naviguer dans l’arborescence, expliquer la différence entre propriétaire, groupe et autres, convertir les permissions octales, identifier les processus et sockets en écoute, lire les journaux avec prudence et écrire un script Bash défensif avec validation des entrées.

### Prérequis
Leçon 1 recommandée. Travail sur une VM, un conteneur ou un compte utilisateur contrôlé. Les commandes destructives ne sont jamais exécutées dans un environnement de production.

### Checkpoints
Convertis plusieurs permissions symboliques en octal. Explique pourquoi `/etc/shadow`, `/var/log` et `/proc` n’ont pas le même niveau de sensibilité. Relie un processus, son parent, son utilisateur et ses connexions réseau. Explique pourquoi SUID et `sudo` exigent une revue d’autorisation.

### Pratique guidée
Construis un inventaire local non destructif avec `whoami`, `id`, `uname -a`, `ps aux`, `ss -tuln`, `df -h` et une lecture ciblée des journaux accessibles. Enregistre la date, le contexte et les limites de chaque observation.

### Challenge légal et éthique
Réalise un mini-audit d’une VM de laboratoire fournie par l’enseignant. Le livrable doit présenter cinq observations, leur niveau de risque, les preuves, les faux positifs possibles et des recommandations de durcissement. Ne modifie aucun compte ni permission.

### Erreurs fréquentes
Confondre lecture et exécution, appliquer `777` par facilité, interpréter tout SUID comme une compromission, utiliser `kill -9` sans comprendre l’impact, ou lancer une recherche récursive sur `/` sans mesurer le coût et les droits nécessaires.

### Synthèse opérationnelle
Linux est un système d’objets, de permissions, de processus, de sockets et de journaux. Une bonne analyse commence par l’observation, reste traçable et privilégie les commandes réversibles.
