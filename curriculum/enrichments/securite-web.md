## Enrichissement pédagogique — guide opératoire

### Positionnement
Cette leçon relie les vulnérabilités web à leurs défenses : entrées, traitement, autorisation, stockage, navigateur et en-têtes de sécurité.

### Objectifs observables
L’apprenant sait expliquer SQLi, XSS, CSRF et IDOR, distinguer authentification et autorisation, recommander des requêtes paramétrées et un encodage contextuel, identifier les limites d’un token CSRF et rédiger une preuve de concept confinée à un laboratoire.

### Prérequis
Leçons 1 à 4 recommandées. Les tests actifs se font exclusivement sur une application locale ou un lab explicitement autorisé, avec données synthétiques.

### Checkpoints
Pour chaque faille, indique la cause, le prérequis, l’impact, la preuve minimale et la correction. Explique pourquoi la validation côté client ne remplace pas la validation serveur. Distingue XSS stocké, réfléchi et DOM-based.

### Pratique guidée
Analyse une application de laboratoire volontairement vulnérable. Observe les requêtes, identifie le contrôle manquant, applique une correction et vérifie qu’elle ne casse pas le scénario légitime. Ne cible aucun domaine public.

### Challenge légal et éthique
Rédige un rapport web avec périmètre, méthode, preuve minimale non destructive, impact, sévérité, correction et test de régression. Les charges doivent rester dans le lab et ne jamais extraire de données réelles.

### Erreurs fréquentes
Confondre échappement HTML et validation SQL, croire qu’une CSP corrige seule un XSS, oublier l’autorisation objet par objet, journaliser des tokens, ou publier un payload réutilisable contre des tiers.

### Synthèse opérationnelle
La défense web est une chaîne : modèle de menace, validation serveur, requêtes paramétrées, encodage contextuel, autorisation, cookies et journalisation contrôlée.
