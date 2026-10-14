---
title: "OSINT : enquêter avec les sources ouvertes"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 50
order: 9
category: "osint"
tags: ["osint", "renseignement", "sources-ouvertes", "ethique", "cycle-du-renseignement"]
prerequisites: ["08-api-rest-python", "13-reconnaissance-web"]
learning_objectives:
  - "Définir l'OSINT et le cycle du renseignement"
  - "Distinguer une source fiable d'une source douteuse"
  - "Mener une première enquête OSINT sur une entité publique, dans un cadre éthique"
  - "Documenter ses découvertes de façon traçable et vérifiable"
author: "ECHATS PRO"
language: "fr"
published: true
---

# OSINT : enquêter avec les sources ouvertes

> 🔔 **IMPORTANT** — Cette leçon ouvre un nouveau bloc du module, consacré à l'OSINT. Comptez environ 50 minutes, une connexion Internet, et un esprit méthodique.

## 🎯 Ce que vous allez apprendre 🕵️

Vous avez déjà cherché le nom d'un restaurant avant d'y aller, vérifié les avis d'un vendeur avant d'acheter, ou retrouvé le site officiel d'une entreprise avant de la contacter. Sans le savoir, vous avez déjà fait de l'**OSINT** — à une échelle modeste. Cette leçon vous apprend à transformer ce réflexe quotidien en une **méthode structurée**, utilisée aussi bien par des journalistes d'investigation, des enquêteurs, des analystes en cybersécurité, que par des équipes de sécurité qui veulent savoir ce que leur propre organisation expose publiquement.

Vous allez :
- comprendre ce qu'est l'OSINT et en quoi il diffère d'une simple recherche web,
- apprendre le cycle du renseignement, la méthode derrière toute enquête sérieuse,
- évaluer la fiabilité d'une source avant de lui faire confiance,
- mener votre première enquête, sur une cible publique et dans un cadre strictement éthique.

> ⚠️ **AVERTISSEMENT** — L'OSINT porte sur des informations **publiques**, mais « public » ne veut pas dire « sans limite ». Collecter des informations sur une **personne privée** sans son consentement, à des fins de surveillance, de harcèlement ou d'intimidation, est illégal dans la quasi-totalité des juridictions, y compris quand chaque information prise isolément était publique. Dans cette leçon, vous enquêterez exclusivement sur des **entités publiques** (organisations, administrations) ou sur **vous-même**, jamais sur une personne tierce sans son accord explicite.

## 📚 Prérequis

- Leçon 08 : *API REST en Python*
- Module Sécurité Web & Pentest, leçon 13 : *Reconnaissance web* (si déjà suivie)

## Qu'est-ce que l'OSINT ?

### Une discipline, pas juste une recherche Google

**OSINT** signifie *Open Source Intelligence*, renseignement de sources ouvertes. Le terme « source ouverte » ne désigne pas uniquement Internet : il couvre toute information **légalement accessible au public**, sans avoir besoin d'un accès privilégié, d'un piratage ou d'une autorisation spéciale — un site web, un registre public, une publication officielle, un article de presse, un document gouvernemental, voire une émission de radio.

Ce qui distingue l'OSINT d'une simple recherche en ligne, c'est la **méthode**. N'importe qui peut taper un nom dans un moteur de recherche. Un analyste OSINT structure sa démarche : il définit un objectif précis, choisit ses sources avec discernement, vérifie chaque information par recoupement, et documente son raisonnement pour que quelqu'un d'autre puisse le suivre et le vérifier.

> 💡 **CONSEIL** — L'OSINT n'est pas réservé aux enquêteurs professionnels. En cybersécurité, c'est une compétence transversale : un analyste l'utilise pour évaluer la surface d'attaque d'une organisation (ce qu'elle expose sans le savoir), un répondant à incident l'utilise pour comprendre un attaquant à partir de traces publiques, et une équipe de sécurité l'utilise pour surveiller ce que sa propre entreprise révèle involontairement en ligne.

### Le cycle du renseignement

Une enquête OSINT sérieuse suit un cycle en plusieurs étapes, que vous retrouverez dans toute la suite de ce module :

1. **Définir l'objectif** — Que cherchez-vous exactement à savoir ? Une question vague (« tout savoir sur cette entreprise ») produit une recherche sans fin ; une question précise (« quels sous-domaines cette entreprise expose-t-elle publiquement ? ») oriente efficacement la collecte.
2. **Collecter** — Rassembler les informations depuis des sources variées, en notant systématiquement leur provenance.
3. **Traiter** — Trier, recouper, éliminer le bruit et les doublons.
4. **Analyser** — Donner du sens à ce qui a été rassemblé : quelles informations répondent réellement à l'objectif ?
5. **Diffuser** — Présenter les résultats de façon claire, avec leurs sources, à qui en a besoin.

Ce cycle n'est pas linéaire : une découverte en phase d'analyse amène souvent à revenir collecter davantage d'informations sur un point précis. C'est normal — une enquête OSINT progresse par itérations.

> 📝 **NOTE — Bellingcat et le vol MH17**
>
> En 2014, le vol MH17 de Malaysia Airlines a été abattu au-dessus de l'est de l'Ukraine. **Bellingcat**, un collectif de journalistes spécialisés en OSINT, a publié une enquête reconstituant le trajet du système de missile responsable, en croisant des **photos et vidéos publiées sur les réseaux sociaux**, des images satellite accessibles publiquement, et des relevés d'ombres portées permettant d'en déduire l'heure et le lieu de prise de vue. Aucune de ces sources n'était secrète : c'est le **recoupement méthodique** de données publiques, chacune insignifiante prise isolément, qui a permis de reconstituer un événement avec une précision que seules des agences de renseignement officielles obtenaient auparavant. Ce cas illustre la force de l'OSINT bien mené : la méthode compte souvent plus que l'accès à des sources rares.

## Évaluer la fiabilité d'une source

Toute information trouvée n'a pas la même valeur. Les services de renseignement utilisent depuis longtemps une grille à deux critères, encore enseignée aujourd'hui, pour évaluer ce qu'ils collectent :

| | Source fiable | Source peu fiable |
|---|---|---|
| **Fiabilité de la source elle-même** | Site officiel, document gouvernemental, journaliste reconnu avec historique vérifiable | Compte anonyme, site sans mentions légales, forum sans modération |
| **Vraisemblance de l'information** | Confirmée par plusieurs sources indépendantes | Information isolée, invérifiable, ou contredite ailleurs |

Une information peut venir d'une source réputée fiable tout en étant, cette fois, inexacte (une erreur, une donnée périmée) ; à l'inverse, une source habituellement douteuse peut, ponctuellement, publier une information exacte. D'où la règle d'or de l'OSINT : **ne jamais se fier à une seule source pour un fait important** — toujours chercher au moins une confirmation indépendante.

> 💡 **CONSEIL** — Posez-vous systématiquement trois questions face à une information : *Qui l'a publiée, et pourquoi ?* *Quand a-t-elle été publiée — est-elle encore d'actualité ?* *Une autre source indépendante dit-elle la même chose ?* Ces trois réflexes éliminent la majorité des erreurs de débutant en OSINT.

## Défi : votre première enquête OSINT

### Choisir une cible éthique

Pour ce premier exercice, vous allez enquêter sur une **organisation publique** de votre choix — une administration, une université, une grande entreprise cotée, ou votre propre organisation si vous en avez une. L'objectif : répondre à une question précise définie à l'avance, en suivant le cycle du renseignement, et en documentant chaque source utilisée.

> 🔔 **IMPORTANT** — Avant de commencer, formulez votre objectif par écrit, en une phrase précise. Exemple : *« Quels sont les sous-domaines publics connus de cette organisation, et quelles technologies web utilise son site principal ? »* Un objectif flou produira une collecte sans fin et un rapport impossible à synthétiser.

### Collecter méthodiquement

Pour cette première enquête, limitez-vous à des sources déjà rencontrées dans ce cours :

1. Le site officiel de l'organisation : explorez ses pages « À propos », mentions légales, offres d'emploi (souvent riches en indices techniques — un poste qui mentionne une technologie précise révèle ce que l'organisation utilise réellement).
2. Une recherche WHOIS sur son nom de domaine principal (module Sécurité Web, leçon 13).
3. Les enregistrements DNS publics (module Réseau & Linux, leçon 05).
4. Une recherche avec l'opérateur `site:` pour explorer ce que les moteurs de recherche ont indexé de ce domaine.

`![Capture : terminal affichant côte à côte les résultats d'une commande whois et d'une commande dig sur un même nom de domaine, avec les champs pertinents (registrar, date de création, serveurs DNS) mis en évidence.](img/02-09-whois-dig.png)`

Pour chaque information trouvée, notez immédiatement : **quoi**, **où** (l'URL ou la commande exacte), et **quand** (la date — une information OSINT se périme). Un tableau simple suffit à ce stade :

| Information | Source | Date de consultation |
|---|---|---|
| Date de création du domaine | whois | aujourd'hui |
| Serveur de messagerie (MX) | dig MX | aujourd'hui |
| ... | ... | ... |

> ⚠️ **AVERTISSEMENT** — Cette leçon se limite à de la **collecte passive** : consulter des sources déjà publiques, sans interagir directement avec les systèmes de la cible. N'allez pas au-delà — pas de scan de ports, pas de tentative de connexion, pas d'énumération active. Ces techniques, qui nécessitent une autorisation explicite, sont traitées dans le module Sécurité Web & Pentest (leçons 13 à 16).

### Recouper et analyser

Une fois votre collecte terminée, reprenez votre objectif de départ. Pour chaque élément de réponse, demandez-vous : *ai-je au moins deux sources indépendantes qui le confirment ?* Si une information ne repose que sur une seule source peu fiable, signalez-la comme « à confirmer » plutôt que de la présenter comme un fait établi.

> ❓ **DÉFI** — Pour l'organisation que vous avez choisie, combien de sources **indépendantes** avez-vous utilisées pour confirmer au moins une information de votre enquête ?
>
> <details>
> <summary>Voir un exemple de réponse</summary>
>
> Il n'y a pas de bon chiffre universel — l'important est la démarche. Un exemple concret : si WHOIS indique que le domaine a été créé en 2010, et que le site officiel mentionne dans sa page « À propos » être en ligne « depuis 2010 », vous avez deux sources indépendantes qui se recoupent sur ce point précis. Si vous n'avez qu'une seule source pour une information donnée, c'est le signal qu'il faut soit chercher une confirmation supplémentaire, soit la présenter avec la réserve appropriée dans votre rapport final.
> </details>

## Diffuser : rédiger une note de synthèse

Terminez votre enquête par une courte **note de synthèse** (une demi-page suffit) qui répond à votre objectif de départ, avec :
- la réponse à la question posée,
- les sources utilisées pour chaque élément clé,
- les points qui restent incertains ou non confirmés.

Cette discipline de rédaction — séparer clairement ce qui est **établi** de ce qui est **probable** ou **incertain** — est la marque d'une enquête OSINT rigoureuse, et vous la retrouverez, sous une forme proche, dans la rédaction d'un rapport de pentest (module Sécurité Web, leçon 20).

## 🔍 Pour aller plus loin

- Le site **Bellingcat** publie régulièrement des enquêtes OSINT complètes, avec leur méthodologie détaillée — une excellente source d'inspiration pour comprendre le recoupement de sources en pratique.
- L'**OSINT Framework** (osintframework.com) recense, par catégorie, des centaines d'outils et de sources utilisées par la communauté.
- La leçon 13 du module Sécurité Web & Pentest, qui applique des principes très proches à une cible technique précise.

## 🧪 Quiz de validation

**Question 1 : Que signifie OSINT ?**
- A) Online Security Investigation
- B) Open Source Intelligence, renseignement de sources ouvertes ✅
- C) Offensive Security International
- D) Open Standard Internet Tracking

*Explication : « sources ouvertes » désigne toute information légalement accessible au public, pas uniquement les sources en ligne.*

**Question 2 : Quelle est la règle d'or face à une information importante en OSINT ?**
- A) La publier immédiatement si elle semble crédible
- B) Toujours chercher au moins une source indépendante qui la confirme avant de la considérer comme établie ✅
- C) Ne se fier qu'aux sources gouvernementales
- D) Ignorer toute information qui vient d'un réseau social

*Explication : une source réputée fiable peut se tromper ; le recoupement avec une source indépendante reste la meilleure protection contre l'erreur.*

**Question 3 : Dans le cycle du renseignement, pourquoi la première étape (définir l'objectif) est-elle si importante ?**
- A) Parce que la loi l'exige
- B) Parce qu'un objectif flou produit une collecte sans fin et un résultat impossible à synthétiser ✅
- C) Parce qu'elle détermine automatiquement les outils à utiliser
- D) Elle n'est pas réellement nécessaire pour une enquête simple

*Explication : une question précise oriente efficacement toute la suite du cycle, de la collecte à la diffusion.*

**Question 4 : Pourquoi l'enquête de Bellingcat sur le vol MH17 est-elle un exemple marquant d'OSINT ?**
- A) Parce qu'elle s'appuyait sur des documents classifiés obtenus illégalement
- B) Parce qu'elle a reconstitué un événement précis en recoupant méthodiquement des sources entièrement publiques ✅
- C) Parce qu'elle a été menée par une agence de renseignement officielle
- D) Parce qu'elle ne reposait que sur une seule source

*Explication : c'est la méthode de recoupement de données publiques, chacune anodine isolément, qui a permis cette reconstitution précise.*

**Question 5 : Que doit-on strictement éviter lors d'une collecte OSINT purement passive ?**
- A) Consulter le site officiel d'une organisation
- B) Interagir directement avec les systèmes de la cible, comme un scan de ports ✅
- C) Utiliser une commande whois
- D) Lire les enregistrements DNS publics

*Explication : la collecte passive se limite à des sources déjà publiques, sans interaction directe avec les systèmes de la cible, ce qui relève de la reconnaissance active et exige une autorisation.*

## 📝 Résumé

- L'OSINT est une discipline structurée de collecte d'informations publiques, pas une simple recherche en ligne.
- Le cycle du renseignement (objectif, collecte, traitement, analyse, diffusion) structure toute enquête sérieuse.
- La fiabilité d'une information dépend à la fois de la fiabilité de la source et de sa vraisemblance, confirmée par recoupement.
- Une enquête OSINT documente systématiquement ses sources, pour rester vérifiable et traçable.
- « Information publique » ne signifie jamais « sans limite éthique » : la collecte porte ici sur des entités publiques, jamais sur des personnes privées sans leur consentement.

## 🎓 Ce que vous avez appris

✅ Définir l'OSINT et le cycle du renseignement
✅ Évaluer la fiabilité d'une source par recoupement
✅ Mener une enquête OSINT passive sur une entité publique
✅ Rédiger une note de synthèse qui distingue le confirmé de l'incertain

## ➡️ Leçon suivante

**10 : Le Google Dorking** : utiliser les opérateurs de recherche avancés pour révéler des informations que les moteurs de recherche ont indexées sans le vouloir. Fichier : `10-google-dorking.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
