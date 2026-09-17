## Enrichissement pédagogique — guide opératoire

### Positionnement
Cette leçon fournit le vocabulaire pour évaluer une protection de l’information : objectif de sécurité, primitive, protocole, gestion des clés et preuve d’intégrité.

### Objectifs observables
L’apprenant distingue hachage, encodage et chiffrement, explique confidentialité/intégrité/authenticité, compare chiffrement symétrique et asymétrique, reconnaît un mode AEAD adapté, décrit le rôle d’un certificat TLS et identifie les erreurs de gestion des mots de passe et des clés.

### Prérequis
Bases réseau et Python recommandées. Les démonstrations cryptographiques utilisent des données fictives et des bibliothèques maintenues; aucune clé réelle ni donnée sensible ne doit être placée dans un notebook partagé.

### Checkpoints
Pour chaque mécanisme, indique l’objectif garanti et ce qu’il ne garantit pas. Explique pourquoi un hash n’est pas un chiffrement. Justifie l’emploi d’un sel et d’un dérivé de clé lent pour les mots de passe. Distingue clé publique, clé privée, nonce et certificat.

### Pratique guidée
Compare deux messages proches avec SHA-256, puis chiffre un texte de test avec un mode authentifié. Vérifie la détection d’une modification et documente le cycle de vie de la clé sans afficher la clé dans le rapport.

### Challenge légal et éthique
Analyse un jeu de données fictif de mots de passe hachés et une configuration TLS simulée. Le livrable doit identifier les faiblesses, leur impact, la preuve et une remédiation; il ne doit pas tenter de casser des comptes réels.

### Erreurs fréquentes
Présenter SHA-256 comme solution de stockage de mots de passe, réutiliser un nonce avec la même clé, utiliser ECB, confondre certificat et chiffrement, ou publier une clé privée dans un dépôt.

### Synthèse opérationnelle
La cryptographie ne compense pas une mauvaise gestion des clés, des identités ou des protocoles. Toujours relier primitive, contexte, menace, implémentation et rotation.
