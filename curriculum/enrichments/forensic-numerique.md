## Enrichissement pédagogique — guide opératoire

### Positionnement
Le forensic vise la reconstruction fiable d’un événement à partir de preuves préservées. L’objectif est la vérité reproductible, pas la simple découverte d’un artefact spectaculaire.

### Objectifs observables
L’apprenant sait expliquer l’ordre de volatilité, préserver une preuve, calculer et vérifier un hash, tenir une chaîne de garde, analyser des journaux Linux/Windows, construire une timeline et exprimer les limites d’une conclusion.

### Prérequis
Leçons 1 et 2 recommandées. Les acquisitions doivent s’effectuer sur des images ou journaux de laboratoire, jamais sur un poste réel sans autorisation et procédure approuvée.

### Checkpoints
Justifie l’ordre de collecte. Distingue atime, mtime et ctime. Relie un événement Windows à une hypothèse sans le traiter comme preuve unique. Explique pourquoi l’analyse se fait sur une copie et comment vérifier son intégrité.

### Pratique guidée
À partir d’un dossier de logs fourni, calcule des checksums, extrait les événements, normalise les dates UTC, construit une timeline et marque chaque élément par source, fiabilité et niveau de confiance.

### Challenge légal et éthique
Reconstitue une intrusion fictive avec un dossier d’artefacts. Le rapport doit inclure chaîne de garde, méthode, chronologie, hypothèses alternatives, indicateurs de compromission et recommandations de conservation. Ne collecte aucune donnée personnelle réelle.

### Erreurs fréquentes
Démarrer par l’analyse au lieu de préserver, modifier les fichiers originaux, mélanger heure locale et UTC, déduire l’intention depuis un seul événement ou oublier de consigner les outils et versions.

### Synthèse opérationnelle
Une preuve utile est préservée, identifiée, horodatée, vérifiable et interprétée avec ses limites. La discipline documentaire est aussi importante que la commande utilisée.
