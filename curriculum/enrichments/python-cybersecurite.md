## Enrichissement pédagogique — guide opératoire

### Positionnement
Python devient ici un instrument d’analyse reproductible : un petit programme doit être lisible, testable, limité dans son périmètre et explicite sur ses erreurs.

### Objectifs observables
L’apprenant sait choisir les types de données adaptés, écrire des fonctions testables, parcourir des collections, gérer les exceptions, lire et produire du JSON, utiliser des expressions régulières avec prudence, journaliser les résultats et séparer collecte, traitement et restitution.

### Prérequis
Leçons 1 et 2 recommandées. Utiliser Python dans un environnement virtuel et des données de laboratoire non sensibles.

### Checkpoints
Explique la différence entre chaîne, entier et booléen. Transforme un script monolithique en fonctions. Distingue erreur attendue et erreur inattendue. Montre comment une entrée utilisateur non validée peut produire une erreur ou un résultat trompeur.

### Pratique guidée
Écris un analyseur de journaux fourni par l’enseignant qui extrait des IP et événements, compte les occurrences, produit un JSON et signale les lignes impossibles à parser sans arrêter tout le traitement. Ajoute des tests sur des entrées vides et malformées.

### Challenge légal et éthique
Développe un outil local de synthèse d’artefacts fictifs. Le programme doit accepter un chemin explicitement fourni, refuser les répertoires hors périmètre, ne pas exécuter les données analysées et produire un rapport avec horodatage et checksum.

### Erreurs fréquentes
Attraper toutes les exceptions sans journaliser, construire des commandes shell à partir d’une entrée non contrôlée, confondre une expression régulière avec une validation complète, exposer des secrets dans les logs ou dépendre d’un résultat externe non versionné.

### Synthèse opérationnelle
Un script de cybersécurité professionnel privilégie la déterminisme, la validation, les erreurs explicites, les tests et la traçabilité plutôt que la complexité.
