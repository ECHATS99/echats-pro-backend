---
title: "Sherlock : Automatiser la Recherche de Pseudonymes"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 12
category: "osint"
tags: ["sherlock", "osint", "python", "automatisation", "pseudonyme", "faux-positifs"]
prerequisites: ["11-recherche-utilisateur", "04-fonctions-modules"]
learning_objectives:
  - "Installer et utiliser Sherlock pour rechercher un pseudonyme multi-plateformes"
  - "Interpréter les résultats en tenant compte des faux positifs et faux négatifs"
  - "Exporter et traiter les résultats avec Python"
  - "Appliquer le même cadre éthique que la leçon précédente à un outil automatisé"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Sherlock : Automatiser la Recherche de Pseudonymes

> 🔔 **IMPORTANT** — Comptez environ 40 minutes. Python et l'environnement virtuel du module Python vous seront utiles.

## 🎯 Ce que vous allez apprendre 🕵️‍♂️

La leçon précédente vous a fait cartographier manuellement votre présence en ligne, plateforme par plateforme — un exercice révélateur, mais lent. **Sherlock** automatise exactement cette démarche : interroger des centaines de sites en quelques secondes pour savoir où un pseudonyme donné possède un compte.

Vous allez :
- installer Sherlock et comprendre son principe de fonctionnement,
- l'utiliser pour cartographier automatiquement votre propre présence en ligne,
- apprendre à lire ses résultats avec esprit critique, en repérant les faux positifs,
- exporter et traiter ces résultats avec les compétences Python déjà acquises dans ce module.

> ⚠️ **AVERTISSEMENT** — Le cadre éthique posé dans la leçon précédente s'applique ici à l'identique, renforcé par la puissance de l'automatisation : Sherlock interroge des centaines de sites en quelques secondes, ce qui rend d'autant plus tentant — et d'autant plus grave — un usage sur une personne qui n'a pas consenti à cette recherche. Utilisez cet outil exclusivement sur votre propre pseudonyme, ou avec l'accord explicite d'un tiers pour cet exercice précis.

## 📚 Prérequis

- Leçon 11 : *Recherche de pseudonymes à travers les plateformes*
- Module Python, leçon 04 : *Fonctions, modules et gestion des erreurs* (pour la partie traitement des résultats)

## Comment fonctionne Sherlock

### Le principe : une requête par site, en parallèle

Sherlock maintient une liste de plusieurs centaines de sites et plateformes, chacun associé à un **motif d'URL** prévisible (`https://plateforme.exemple/nom-utilisateur`). Pour un pseudonyme donné, l'outil construit l'URL correspondante pour chaque site de sa liste, envoie une requête, et observe la réponse : un code de statut `200` suggère généralement qu'un profil existe à cette adresse, tandis qu'une erreur `404` suggère son absence — un principe que vous reconnaissez directement du module Python (leçon 06, sur les requêtes HTTP) et du fuzzing (module Sécurité Web, leçon 15), appliqué ici à un usage de reconnaissance plutôt que de test de sécurité.

```bash
python3 -m venv env && source env/bin/activate
pip install sherlock-project
sherlock votre_pseudonyme
```

`![Capture : terminal affichant le défilement des résultats de la commande sherlock, avec des lignes en vert précédées de [+] pour les comptes trouvés et des lignes grises ou rouges pour les sites où aucun compte n'a été détecté.](img/02-12-sherlock-terminal.png)`

### Les faux positifs et faux négatifs

Un code `200` ne garantit pas toujours qu'un profil existe réellement : certains sites renvoient ce code même pour un nom d'utilisateur inexistant (en affichant une page « utilisateur introuvable » avec un statut de succès plutôt qu'une vraie erreur 404) — un comportement que Sherlock tente de détecter et de compenser en vérifiant aussi le contenu de la page, mais qui reste une source possible de **faux positifs**. À l'inverse, un site qui a changé sa structure d'URL depuis la dernière mise à jour de la liste de Sherlock produira un **faux négatif** : l'outil ne trouvera rien, alors qu'un compte existe bel et bien.

> 💡 **CONSEIL** — Ne traitez jamais un résultat Sherlock comme une certitude absolue. Pour toute plateforme qui vous semble importante dans votre recherche, **vérifiez manuellement** en ouvrant l'URL indiquée dans votre navigateur — exactement la même discipline que celle déjà recommandée pour les scanners automatisés du module Sécurité Web (leçons 12 et 15) : l'automatisation accélère la collecte, elle ne dispense jamais de la vérification humaine.

## Défi : votre cartographie automatisée

### Lancer une première recherche

Sur votre propre pseudonyme (celui déjà utilisé en leçon 11, ou un autre de votre choix), lancez :

```bash
sherlock votre_pseudonyme --print-found
```

L'option `--print-found` limite l'affichage aux seuls résultats positifs, pour une lecture plus rapide sur un pseudonyme testé sur plusieurs centaines de sites.

### Comparer avec votre recherche manuelle

Reprenez le tableau que vous aviez construit en leçon 11. Sherlock a-t-il retrouvé les mêmes plateformes que votre recherche manuelle ? En a-t-il trouvé **d'autres**, auxquelles vous n'aviez pas pensé ?

> ❓ **DÉFI** — Parmi les résultats positifs renvoyés par Sherlock, combien, après vérification manuelle, se révèlent être de véritables faux positifs (la page existe, mais ne correspond pas réellement à un compte actif) ?
>
> <details>
> <summary>Voir un exemple de réflexion</summary>
>
> Le taux exact varie selon le pseudonyme testé et l'état de la liste de sites de Sherlock au moment de l'exercice. L'essentiel est la démarche : vérifiez manuellement trois ou quatre résultats parmi les moins familiers de la liste, et notez combien correspondent réellement à un profil existant contenant des informations vous concernant, par opposition à une page générique, une erreur mal interprétée, ou un profil appartenant en réalité à quelqu'un d'autre portant le même pseudonyme par coïncidence.
> </details>

### Exporter et traiter les résultats avec Python

Sherlock peut exporter ses résultats en JSON, directement exploitable avec les compétences du module Python :

```bash
sherlock votre_pseudonyme --output resultats.json
```

```python
import json

with open("resultats.json", encoding="utf-8") as f:
    resultats = json.load(f)

trouves = [site for site, info in resultats.items() if info.get("status", {}).get("status") == "Claimed"]
print(f"{len(trouves)} comptes trouvés sur {len(resultats)} sites testés")
for site in trouves:
    print("-", site)
```

(La structure exacte du fichier JSON peut varier selon la version de Sherlock installée — inspectez le fichier produit avec `python3 -m json.tool resultats.json` avant d'écrire votre script d'analyse, une habitude déjà recommandée dans le module Python, leçon 05.)

> 📝 **NOTE — Sherlock et la modération en ligne**
>
> Sherlock, créé et maintenu par une communauté open source depuis 2018, est aujourd'hui l'un des outils OSINT les plus utilisés et les plus cités dans les formations en cybersécurité à travers le monde — y compris par des équipes de confiance et sécurité de grandes plateformes, qui l'utilisent pour identifier rapidement si un compte signalé pour abus en possède d'autres, dans le cadre de leurs propres politiques de modération. Cet usage professionnel illustre, une fois de plus, que la légitimité d'un outil OSINT ne tient jamais à sa puissance technique, mais toujours au mandat et au cadre dans lesquels il est employé.

## 🔍 Pour aller plus loin

- Le dépôt officiel de Sherlock sur GitHub, qui documente régulièrement les nouveaux sites ajoutés à sa liste et les options avancées de la ligne de commande.
- L'**OSINT Framework**, qui référence d'autres outils similaires, certains spécialisés sur une catégorie précise de plateformes.
- Le module Sécurité Web & Pentest, leçon 12, sur l'interprétation critique des résultats d'un outil automatisé — directement applicable ici.

## 🧪 Quiz de validation

**Question 1 : Sur quel principe repose le fonctionnement de Sherlock ?**
- A) Il devine les mots de passe associés à un pseudonyme
- B) Il construit une URL prévisible pour chaque site de sa liste et observe la réponse du serveur pour en déduire l'existence d'un profil ✅
- C) Il accède à des bases de données privées des plateformes
- D) Il ne fonctionne que sur les réseaux sociaux les plus connus

*Explication : c'est une application directe des principes HTTP déjà étudiés — codes de statut et motifs d'URL — à un usage de reconnaissance.*

**Question 2 : Pourquoi un résultat positif de Sherlock peut-il être un faux positif ?**
- A) Parce que Sherlock invente des résultats aléatoirement
- B) Parce que certains sites renvoient un code de succès même pour un nom d'utilisateur inexistant ✅
- C) Parce que Sherlock ne teste jamais réellement les sites
- D) Les faux positifs sont impossibles avec cet outil

*Explication : la détection automatique du statut d'un compte peut être trompée par un comportement non standard du site testé.*

**Question 3 : Que faut-il faire avant de considérer un résultat Sherlock comme fiable pour une plateforme importante ?**
- A) Rien, les résultats sont toujours exacts
- B) Vérifier manuellement en ouvrant l'URL indiquée dans son propre navigateur ✅
- C) Relancer Sherlock plusieurs fois de suite
- D) Contacter directement la plateforme concernée

*Explication : cette vérification humaine reste indispensable, comme pour tout outil automatisé rencontré dans ce cours.*

**Question 4 : Pourquoi certaines équipes de confiance et sécurité de grandes plateformes utilisent-elles légitimement un outil comme Sherlock ?**
- A) Pour espionner leurs utilisateurs sans raison
- B) Pour identifier, dans le cadre de leurs politiques de modération, si un compte signalé pour abus en possède d'autres ✅
- C) Parce que la loi les y oblige systématiquement
- D) Pour vendre les données trouvées à des tiers

*Explication : cet usage s'inscrit dans un mandat professionnel défini, ce qui en fait un usage légitime au même titre que les autres exemples déjà vus dans ce cours.*

**Question 5 : Pourquoi l'automatisation offerte par Sherlock rend-elle le cadre éthique de la leçon précédente encore plus important à respecter ?**
- A) Parce que l'automatisation est interdite par la loi
- B) Parce qu'elle permet d'interroger des centaines de sites en quelques secondes, rendant d'autant plus grave un usage non consenti sur une personne réelle ✅
- C) Parce que Sherlock nécessite une autorisation spéciale pour être installé
- D) L'automatisation ne change rien au cadre éthique

*Explication : la puissance d'un outil amplifie les conséquences d'un usage inapproprié, ce qui renforce — plutôt qu'il ne dispense de — la nécessité du cadre éthique déjà posé.*

## 📝 Résumé

- Sherlock automatise la recherche manuelle de la leçon précédente, en testant des centaines de sites en quelques secondes à partir d'un motif d'URL prévisible.
- Les résultats peuvent contenir des faux positifs et des faux négatifs, et doivent toujours être vérifiés manuellement avant d'être considérés comme fiables.
- Les résultats s'exportent en JSON et se traitent directement avec les compétences Python déjà acquises dans ce module.
- Des usages professionnels légitimes existent (modération, enquête mandatée), toujours encadrés par un mandat ou un consentement explicite.
- La puissance de l'automatisation renforce, plutôt qu'elle ne réduit, l'importance du cadre éthique déjà posé en leçon 11.

## 🎓 Ce que vous avez appris

✅ Installer et utiliser Sherlock pour une recherche multi-plateforme
✅ Identifier et vérifier les faux positifs dans ses résultats
✅ Exporter et traiter les résultats avec Python
✅ Appliquer un cadre éthique rigoureux à un outil d'automatisation puissant

## ➡️ Leçon suivante

**13 : Maltego** : visualiser et explorer des relations entre entités (personnes, organisations, infrastructures) à l'aide d'un outil graphique dédié à l'OSINT. Fichier : `13-maltego.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
