---
title: "Maltego : Visualiser les Relations entre Entités"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 45
order: 13
category: "osint"
tags: ["maltego", "osint", "transforms", "graphe", "visualisation", "entites"]
prerequisites: ["12-sherlock-osint", "05-dns"]
learning_objectives:
  - "Comprendre le principe des entités et des transforms dans Maltego"
  - "Construire un graphe de reconnaissance sur un domaine de son choix"
  - "Lire et interpréter visuellement des relations entre entités"
  - "Situer Maltego parmi les outils OSINT déjà rencontrés dans ce module"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Maltego : Visualiser les Relations entre Entités

> 🔔 **IMPORTANT** — Comptez environ 45 minutes. Vous aurez besoin d'installer Maltego Community Edition (gratuite, avec inscription).

## 🎯 Ce que vous allez apprendre 🕸️

Jusqu'ici, vos résultats OSINT ont pris la forme de tableaux et de listes : des sous-domaines, des comptes trouvés, des informations WHOIS. C'est efficace pour une petite enquête, mais dès que le nombre d'éléments grandit — des dizaines de sous-domaines, de comptes, d'adresses e-mail liées entre eux — un tableau devient difficile à lire. **Maltego** répond à ce problème en représentant vos découvertes sous forme de **graphe visuel**, où chaque information est un nœud relié aux autres par des liens explicites.

Vous allez :
- comprendre le principe des entités et des transforms, le vocabulaire propre à Maltego,
- construire votre premier graphe de reconnaissance sur un domaine que vous possédez,
- apprendre à lire visuellement des relations qu'un tableau masquerait,
- situer cet outil parmi tout ce que vous avez déjà appris dans ce module.

> ⚠️ **AVERTISSEMENT** — Maltego automatise des recherches qui, pour certaines de ses extensions (appelées *transforms*), interrogent des services tiers avec leurs propres conditions d'utilisation. Restez, comme pour chaque leçon de ce bloc, sur une cible que vous possédez ou sur une recherche purement passive à partir de sources publiques — jamais d'action active non autorisée sur un système tiers.

## 📚 Prérequis

- Leçon 12 : *Sherlock*
- Module Réseau & Linux, leçon 05 : *DNS*

## Le vocabulaire de Maltego

### Entités et transforms

Une **entité** est un objet que Maltego sait représenter : un domaine, une adresse IP, une adresse e-mail, un nom de personne, un document, un réseau social. Un **transform** est une action qui part d'une entité existante et en découvre de nouvelles qui lui sont liées — par exemple, partir d'un domaine et exécuter le transform « À DNS Name » pour découvrir ses sous-domaines, ou partir d'une adresse e-mail et exécuter un transform qui recherche les comptes associés sur certains services.

```
[Domaine : exemple.cg]
        │  transform "À DNS Name"
        ▼
[Sous-domaine : mail.exemple.cg] ─── [Sous-domaine : dev.exemple.cg]
```

Chaque transform que vous exécutez **étend le graphe** : les nouvelles entités découvertes apparaissent, reliées par une ligne à l'entité de départ, et vous pouvez immédiatement exécuter de nouveaux transforms sur ces nouvelles entités — construisant progressivement une carte de plus en plus riche.

> 💡 **CONSEIL** — Vous reconnaissez ici, sous une forme visuelle, exactement les mêmes techniques que celles de la leçon 14 du module Sécurité Web (énumération de sous-domaines) : journaux de transparence des certificats, résolution DNS, recherches WHOIS. Maltego ne invente pas de nouvelles sources — il orchestre et visualise des sources que vous connaissez déjà, ce qui en fait un très bon outil pour **synthétiser** une enquête menée avec les techniques des leçons précédentes.

### L'écosystème de transforms

Maltego Community Edition est livrée avec un ensemble de transforms gratuits (le *Maltego Standard Transforms*), couvrant DNS, WHOIS, et quelques sources publiques courantes. Des extensions tierces, parfois payantes, ajoutent des transforms vers des services spécialisés (réputation d'adresses IP, recherche de documents, réseaux sociaux). Pour cette leçon, les transforms gratuits standards suffisent amplement.

## Défi : construire votre premier graphe

### Installer Maltego

Téléchargez Maltego Community Edition depuis le site officiel, créez un compte gratuit (nécessaire pour utiliser les transforms standards), et lancez l'application. Au premier lancement, choisissez de démarrer avec un graphe vide.

### Créer votre entité de départ

Faites glisser une entité de type **Domain** depuis le panneau d'entités vers votre graphe, puis double-cliquez dessus pour en modifier la valeur : saisissez un domaine que vous possédez, ou à défaut `example.com`.

`![Capture : interface de Maltego avec une seule entité de type Domain placée au centre d'un graphe vide, le panneau d'entités visible sur le côté gauche de l'écran.](img/02-13-maltego-entite-depart.png)`

### Exécuter vos premiers transforms

Faites un clic droit sur votre entité de domaine, et explorez le menu des transforms disponibles. Exécutez successivement :
1. un transform de résolution vers des noms DNS (pour découvrir des sous-domaines),
2. un transform WHOIS (pour afficher les informations d'enregistrement),
3. un transform vers les serveurs de messagerie (enregistrements MX).

`![Capture : graphe Maltego après exécution de plusieurs transforms, montrant l'entité Domain centrale reliée à plusieurs entités DNS Name et à une entité WHOIS Record, disposées en étoile autour du nœud de départ.](img/02-13-maltego-graphe-etendu.png)`

Observez comment le graphe s'enrichit visuellement à chaque transform. Contrairement aux commandes `dig` et `whois` de la leçon DNS (module Réseau & Linux, leçon 05), qui produisent chacune un résultat isolé dans un terminal, Maltego **accumule et relie** visuellement tout ce que vous découvrez au même endroit.

> ❓ **DÉFI** — Sur votre graphe, combien de niveaux de profondeur avez-vous atteints en enchaînant les transforms (c'est-à-dire : combien de fois avez-vous exécuté un transform sur une entité elle-même découverte par un transform précédent, plutôt que sur votre entité de départ) ?
>
> <details>
> <summary>Voir un exemple de réflexion</summary>
>
> Même un seul niveau supplémentaire — par exemple, exécuter un transform DNS sur un sous-domaine que vous venez de découvrir, plutôt que sur le domaine principal — illustre le principe central de Maltego : chaque découverte devient un nouveau point de départ. C'est cette capacité à **enchaîner** les transforms, en suivant les relations découvertes plutôt qu'en se limitant à sa requête initiale, qui distingue réellement Maltego d'une simple série de commandes `dig` et `whois` exécutées séparément.
> </details>

### Organiser et lire le graphe

Avec de nombreuses entités, un graphe devient vite difficile à lire. Maltego propose plusieurs modes d'organisation automatique (en cercle, en bloc, hiérarchique) accessibles depuis la barre d'outils — testez-en plusieurs pour voir lequel rend votre graphe le plus lisible selon le nombre d'entités que vous avez accumulées.

> 📝 **NOTE — Maltego et les enquêtes journalistiques**
>
> Maltego est largement utilisé au-delà de la cybersécurité : des journalistes d'investigation et des organisations de lutte contre la fraude l'emploient pour cartographier des réseaux d'entreprises liées entre elles (actionnaires communs, adresses partagées, dirigeants en commun), à partir de registres publics du commerce. Le même principe de « partir d'une entité connue et suivre les relations qu'elle révèle » s'applique aussi bien à un domaine technique qu'à un réseau d'entreprises — ce qui illustre, une fois de plus, que la méthode OSINT transcende largement le seul domaine de la cybersécurité.

## Comparer avec vos outils précédents

| Outil | Ce qu'il apporte | Limite |
|---|---|---|
| `dig` / `whois` (module Réseau & Linux) | Rapide, scriptable, précis | Résultat isolé, pas de vue d'ensemble |
| Sherlock (leçon 12) | Automatise une recherche large et répétitive | Spécialisé sur les pseudonymes uniquement |
| Maltego | Visualise les relations entre entités variées, accumule les découvertes | Interface plus lourde, certains transforms avancés payants |

Aucun de ces outils ne remplace les autres : un analyste OSINT expérimenté passe naturellement de l'un à l'autre selon l'étape de son enquête — une recherche ciblée avec `dig`, une automatisation large avec Sherlock, une synthèse visuelle avec Maltego quand le nombre d'entités le justifie.

## 🔍 Pour aller plus loin

- La documentation officielle de Maltego, avec ses tutoriels sur les transforms avancés.
- Le *Maltego Transform Hub*, qui recense les extensions disponibles, gratuites et payantes.
- La leçon 14 de ce module, sur Shodan et Censys, deux sources que des transforms Maltego spécialisés peuvent également exploiter.

## 🧪 Quiz de validation

**Question 1 : Qu'est-ce qu'un transform dans Maltego ?**
- A) Un filtre visuel appliqué au graphe
- B) Une action qui part d'une entité existante et en découvre de nouvelles qui lui sont liées ✅
- C) Un format d'exportation de données
- D) Un type d'entité réservé aux adresses IP

*Explication : chaque transform exécuté enrichit le graphe de nouvelles entités reliées à celle sur laquelle il a été lancé.*

**Question 2 : En quoi Maltego diffère-t-il fondamentalement des commandes dig et whois pour une reconnaissance DNS ?**
- A) Il utilise des sources d'information totalement différentes
- B) Il visualise et accumule les relations entre découvertes sous forme de graphe, plutôt que de produire des résultats isolés ✅
- C) Il ne fonctionne que sur des domaines payants
- D) Il remplace entièrement le besoin de comprendre le DNS

*Explication : Maltego orchestre souvent les mêmes sources que dig et whois, mais les relie visuellement plutôt que de les afficher séparément.*

**Question 3 : Pourquoi organiser automatiquement un graphe Maltego devient-il utile avec de nombreuses entités ?**
- A) Parce que Maltego n'affiche pas les entités sans organisation automatique
- B) Parce qu'un graphe dense devient rapidement illisible sans une disposition claire ✅
- C) Parce que l'organisation automatique ajoute de nouvelles entités
- D) Ce n'est jamais nécessaire, quel que soit le nombre d'entités

*Explication : les modes d'organisation (cercle, hiérarchique...) améliorent la lisibilité à mesure que le graphe grandit.*

**Question 4 : Pourquoi Maltego est-il également utilisé par des journalistes d'investigation, au-delà de la cybersécurité ?**
- A) Parce qu'il est gratuit pour la presse uniquement
- B) Parce que le principe de suivre des relations entre entités s'applique aussi bien à des réseaux d'entreprises qu'à une infrastructure technique ✅
- C) Parce qu'il donne accès à des bases de données confidentielles
- D) Parce qu'il remplace le travail d'enquête humain

*Explication : la méthode OSINT — partir d'une entité connue et suivre ses relations — dépasse largement le seul cadre technique de la cybersécurité.*

**Question 5 : Quelle affirmation décrit le mieux la relation entre Maltego, Sherlock et dig/whois ?**
- A) Maltego remplace entièrement les deux autres outils
- B) Ce sont des outils complémentaires, chacun adapté à une étape différente d'une enquête OSINT ✅
- C) Ils font exactement la même chose avec une interface différente
- D) Seul Maltego est utilisable dans un cadre professionnel

*Explication : un analyste expérimenté combine ces outils selon le besoin — ciblé et scriptable, automatisé et large, ou visuel et synthétique.*

## 📝 Résumé

- Maltego représente les découvertes OSINT sous forme de graphe, où des entités sont reliées par les transforms exécutés.
- Un transform part d'une entité existante pour en révéler de nouvelles, souvent à partir des mêmes sources déjà rencontrées dans ce cours (DNS, WHOIS).
- Le graphe peut être organisé automatiquement pour rester lisible à mesure qu'il s'enrichit.
- Maltego ne remplace pas les outils précédents du module, mais apporte une capacité de synthèse visuelle quand le nombre d'entités le justifie.
- L'usage de Maltego dépasse la cybersécurité, notamment dans l'investigation journalistique et la lutte contre la fraude.

## 🎓 Ce que vous avez appris

✅ Comprendre le vocabulaire des entités et des transforms
✅ Construire et enrichir un graphe de reconnaissance
✅ Lire et organiser visuellement des relations entre entités
✅ Situer Maltego parmi les outils OSINT déjà maîtrisés

## ➡️ Leçon suivante

**14 : Shodan et Censys** : des moteurs de recherche spécialisés dans les appareils et services exposés sur Internet. Fichier : `14-shodan-censys.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
