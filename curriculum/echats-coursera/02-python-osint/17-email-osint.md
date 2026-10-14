---
title: "E-mail et OSINT : ce qu'une Adresse Révèle"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 17
category: "osint"
tags: ["email", "osint", "entetes", "phishing", "fuites-identifiants", "spf-dkim-dmarc"]
prerequisites: ["16-geolocalisation-image", "06-http-https"]
learning_objectives:
  - "Décomposer la structure d'une adresse e-mail pour en tirer des informations OSINT"
  - "Lire les en-têtes complets d'un e-mail pour en retracer le trajet"
  - "Vérifier si une adresse e-mail apparaît dans une fuite de données connue, de façon éthique"
  - "Reconnaître les indices d'un e-mail de phishing à partir de ses en-têtes"
author: "ECHATS PRO"
language: "fr"
published: true
---

# E-mail et OSINT : ce qu'une Adresse Révèle

> 🔔 **IMPORTANT** — Comptez environ 40 minutes. Vous aurez besoin d'accéder aux en-têtes complets d'un e-mail que vous avez reçu.

## 🎯 Ce que vous allez apprendre 📧

Une adresse e-mail semble être une simple chaîne de caractères. En réalité, c'est souvent un point d'entrée riche en informations OSINT : elle révèle parfois une organisation, un format de nommage interne, et surtout, les **en-têtes techniques** qui accompagnent chaque e-mail racontent un véritable trajet — quels serveurs il a traversés, à quelle heure, et avec quelles vérifications de sécurité.

Vous allez :
- décomposer une adresse e-mail pour comprendre ce qu'elle révèle à elle seule,
- lire les en-têtes complets d'un e-mail pour en retracer le trajet technique,
- apprendre à vérifier, de façon éthique, si une adresse apparaît dans une fuite de données connue,
- reconnaître dans les en-têtes les indices caractéristiques d'un e-mail de phishing.

> ⚠️ **AVERTISSEMENT** — Analyser vos propres e-mails, ou ceux qu'une organisation vous a explicitement demandé d'examiner dans un cadre professionnel défini, ne pose pas de problème. Mais consulter les en-têtes ou l'historique d'un e-mail appartenant à un tiers sans autorisation, ou tenter d'accéder à une boîte de réception qui n'est pas la vôtre, reste strictement interdit — exactement les mêmes limites déjà posées dans ce module à propos de toute autre source personnelle.

## 📚 Prérequis

- Leçon 16 : *Géolocalisation d'image*
- Module Réseau & Linux, leçon 06 : *HTTP et HTTPS* (pour le parallèle avec les en-têtes)

## Ce que révèle une adresse, avant même de l'analyser

### La structure de base

```
prenom.nom@organisation.cg
   │         │
 partie     domaine
 locale
```

La **partie locale** (avant le `@`) suit souvent une convention de nommage propre à l'organisation : `prenom.nom`, `p.nom`, `pnom`, ou un simple pseudonyme. Une fois cette convention identifiée — par exemple en observant une seule adresse publiée sur le site d'une organisation, dans une mention légale ou une offre d'emploi — il devient souvent possible de **déduire** l'adresse probable d'une autre personne de la même organisation dont on connaît seulement le nom, sans l'avoir jamais vue publiée.

> 💡 **CONSEIL** — Cette déduction reste une hypothèse, jamais une certitude : certaines organisations changent leur convention au fil du temps, ou utilisent des exceptions pour les homonymes. Comme pour toute conclusion OSINT (leçon 09), présentez une adresse déduite comme une hypothèse « probable », jamais comme un fait confirmé, tant qu'elle n'a pas été vérifiée par une autre source.

### Le domaine : une fenêtre sur l'infrastructure

Le domaine d'une adresse e-mail renvoie directement aux techniques déjà vues dans ce module et dans le module Réseau & Linux : une recherche des enregistrements **MX** (module Réseau & Linux, leçon 05) révèle quel service de messagerie l'organisation utilise réellement (une solution hébergée en interne, ou un service cloud tiers), une information parfois utile pour comprendre son niveau de maturité technique.

```bash
dig exemple.cg MX
```

## Lire les en-têtes complets d'un e-mail

### Où les trouver

La plupart des clients de messagerie masquent, par défaut, les en-têtes techniques d'un e-mail pour ne montrer que l'expéditeur, l'objet et le corps du message. Pour les afficher dans leur intégralité, cherchez une option souvent nommée « Afficher l'original », « Afficher la source » ou « En-têtes complets », généralement accessible depuis un menu contextuel ou les trois points d'options d'un message ouvert.

`![Capture : interface d'un client de messagerie avec le menu contextuel ouvert sur un e-mail, l'option "Afficher l'original" ou équivalente mise en évidence par un encadré.](img/02-17-afficher-original.png)`

### Anatomie des en-têtes

```
Received: from mail.exemple.cg (mail.exemple.cg [203.0.113.10])
    by mx.destinataire.cg with ESMTP id abc123
    for <vous@destinataire.cg>; Mon, 15 Mar 2026 09:12:03 +0100
From: contact@exemple.cg
To: vous@destinataire.cg
Subject: Objet du message
Date: Mon, 15 Mar 2026 09:12:00 +0100
Message-ID: <unique-id@exemple.cg>
SPF: pass (domaine exemple.cg autorisé à envoyer pour cette adresse)
DKIM: pass
DMARC: pass
```

Chaque bloc **Received** correspond à un **saut** dans le trajet de l'e-mail — un principe qui rejoint directement le fonctionnement du routage et de `traceroute` déjà vu dans le module Réseau & Linux (leçons 07 et 15). Un e-mail légitime traverse généralement un nombre limité et cohérent de serveurs, tous appartenant soit à l'expéditeur, soit à des relais de messagerie reconnus ; une chaîne de sauts incohérente, passant par des serveurs inattendus ou dans un ordre suspect, est un signal d'alerte.

Les champs **SPF**, **DKIM** et **DMARC**, déjà mentionnés dans le module Réseau & Linux (leçon 05, à propos des enregistrements TXT), indiquent si le serveur receveur a pu **vérifier** que l'e-mail provient réellement du domaine qu'il prétend représenter. Un `FAIL` sur l'un de ces champs est un indice fort — bien que pas automatiquement une preuve absolue — qu'un e-mail pourrait être falsifié.

## Défi : analyser un e-mail reçu

### Examiner vos propres en-têtes

Choisissez un e-mail récent dans votre propre boîte de réception, affichez ses en-têtes complets, et répondez :

1. Combien de sauts **Received** apparaissent-ils dans la chaîne ?
2. Les champs SPF, DKIM et DMARC indiquent-ils tous `pass` ?
3. L'adresse IP du premier serveur `Received` correspond-elle, selon une recherche WHOIS rapide (leçon 09), à une organisation cohérente avec l'expéditeur annoncé ?

`![Capture : fenêtre affichant le texte brut des en-têtes complets d'un e-mail, avec les champs Received, SPF, DKIM et DMARC encadrés et numérotés.](img/02-17-entetes-brutes.png)`

> ❓ **DÉFI** — Sur l'e-mail que vous avez analysé, l'adresse IP du premier serveur Received correspond-elle bien, selon WHOIS, à l'organisation que vous attendiez ?
>
> <details>
> <summary>Voir un exemple de réflexion</summary>
>
> Sur un e-mail légitime provenant d'une organisation que vous connaissez, cette adresse IP devrait correspondre à un bloc d'adresses enregistré au nom de cette organisation, ou à un grand fournisseur de messagerie reconnu si elle externalise cette fonction. Si l'adresse IP correspond à un hébergeur totalement sans rapport, ou à un pays inattendu par rapport à l'organisation annoncée, c'est exactement ce type d'incohérence qui doit éveiller la méfiance — la même logique de recoupement de sources déjà appliquée tout au long de ce module.
> </details>

### Vérifier une fuite de données, de façon éthique

Plusieurs services publics et réputés permettent de vérifier si une adresse e-mail est apparue dans une fuite de données connue, sans jamais révéler le mot de passe associé — uniquement le fait que l'adresse figure dans un jeu de données compromis publiquement documenté.

> ⚠️ **AVERTISSEMENT** — N'utilisez ce type de service **que sur vos propres adresses**. Interroger l'adresse d'un tiers, même par simple curiosité, sans son consentement, sort du cadre éthique de ce cours.

Si votre adresse apparaît dans une ou plusieurs fuites, c'est l'occasion de vérifier que vous n'utilisez plus, nulle part, le mot de passe qui était associé à ce compte au moment de la fuite — un rappel direct de l'importance de ne jamais réutiliser un même mot de passe sur plusieurs services (module Python, leçon 04, à propos du module `secrets`).

## Les en-têtes face au phishing

Les techniques de cette leçon s'appliquent directement à l'analyse d'un e-mail de phishing suspect — un sujet qui rejoint les techniques d'ingénierie sociale abordées plus largement dans le module Red Team. Quelques signaux caractéristiques, visibles uniquement dans les en-têtes complets, souvent invisibles dans l'affichage simplifié par défaut :

| Signal dans les en-têtes | Ce qu'il peut indiquer |
|---|---|
| Champ `From` affiché différent du domaine réel dans `Received` | Usurpation de l'adresse affichée (*spoofing*) |
| SPF ou DKIM en échec | L'e-mail n'a pas pu être authentifié comme venant réellement du domaine annoncé |
| `Reply-To` différent de `From` | Les réponses sont redirigées vers une adresse différente de l'expéditeur apparent |
| Chaîne de sauts incohérente ou excessive | Trajet technique suspect, ne correspondant pas à un envoi direct attendu |

> 📝 **NOTE — SPF, DKIM, DMARC : trois couches complémentaires**
>
> Ces trois mécanismes, publiés via des enregistrements DNS TXT (module Réseau & Linux, leçon 05), ne protègent pas de la même façon. **SPF** vérifie que le serveur d'envoi est autorisé pour ce domaine. **DKIM** ajoute une signature cryptographique au message, garantissant qu'il n'a pas été modifié en chemin. **DMARC** définit la politique à appliquer quand SPF ou DKIM échouent (rejeter le message, le marquer comme suspect, ou ne rien faire). Une organisation qui n'a configuré aucun de ces trois mécanismes rend son propre domaine bien plus facile à usurper dans des campagnes de phishing ciblant ses partenaires ou ses clients — un exemple concret de mauvaise configuration de sécurité (catégorie A05 de l'OWASP Top 10, module Sécurité Web, leçon 02).

## 🔍 Pour aller plus loin

- La documentation de votre client de messagerie sur l'affichage des en-têtes complets, dont l'emplacement exact varie d'un logiciel à l'autre.
- Les guides de l'ANSSI ou d'organismes équivalents sur la mise en place de SPF, DKIM et DMARC pour un domaine professionnel.
- Le module Red Team & IA, pour approfondir l'ingénierie sociale et le phishing sous l'angle offensif et défensif.

## 🧪 Quiz de validation

**Question 1 : Que révèle généralement la partie locale d'une adresse e-mail professionnelle (avant le @) ?**
- A) Le mot de passe de la personne
- B) Souvent une convention de nommage propre à l'organisation, permettant parfois de déduire d'autres adresses probables ✅
- C) L'adresse physique de l'organisation
- D) Rien d'exploitable en OSINT

*Explication : une fois la convention identifiée sur une adresse connue, elle peut permettre de formuler une hypothèse sur l'adresse d'une autre personne de la même organisation.*

**Question 2 : À quoi correspond chaque bloc Received dans les en-têtes d'un e-mail ?**
- A) Au contenu du message
- B) À un saut, un serveur traversé par l'e-mail durant son trajet ✅
- C) À une pièce jointe
- D) À l'adresse du destinataire uniquement

*Explication : ce principe rejoint directement celui du routage et de traceroute, chaque saut correspondant à une étape du trajet technique du message.*

**Question 3 : Que vérifie le mécanisme SPF ?**
- A) Que le contenu du message n'a pas été modifié
- B) Que le serveur qui a envoyé l'e-mail est bien autorisé à le faire pour ce domaine ✅
- C) Que l'e-mail ne contient aucune pièce jointe dangereuse
- D) Que le destinataire a bien reçu le message

*Explication : SPF vérifie l'autorisation du serveur d'envoi ; DKIM vérifie l'intégrité du message ; DMARC définit la politique en cas d'échec de l'un ou l'autre.*

**Question 4 : Pourquoi faut-il se limiter à vérifier ses propres adresses dans un service de recherche de fuites de données ?**
- A) Parce que ces services sont payants pour les adresses de tiers
- B) Parce qu'interroger l'adresse d'un tiers sans son consentement sort du cadre éthique posé dans ce module ✅
- C) Parce que ces services ne fonctionnent que sur ses propres adresses techniquement
- D) Il n'y a aucune restriction particulière

*Explication : ce principe prolonge directement le cadre éthique déjà posé pour toute recherche OSINT portant sur des informations personnelles.*

**Question 5 : Lequel de ces signaux, visible dans les en-têtes complets, est caractéristique d'un possible e-mail de phishing ?**
- A) Un champ Date cohérent avec l'heure de réception
- B) Un champ Reply-To différent du champ From, redirigeant les réponses vers une autre adresse ✅
- C) Un seul saut Received, correspondant à un envoi direct
- D) SPF, DKIM et DMARC tous en pass

*Explication : rediriger les réponses vers une adresse différente de l'expéditeur apparent est une technique fréquente dans les campagnes de phishing.*

## 📝 Résumé

- Une adresse e-mail révèle souvent une convention de nommage organisationnelle, exploitable pour formuler des hypothèses sur d'autres adresses.
- Les en-têtes complets d'un e-mail retracent son trajet technique saut par saut, et incluent des vérifications d'authenticité (SPF, DKIM, DMARC).
- Une incohérence dans la chaîne de sauts, ou un échec de ces vérifications, constitue un signal d'alerte à analyser.
- La vérification de fuites de données ne se pratique que sur ses propres adresses, jamais sur celles d'un tiers sans consentement.
- L'analyse des en-têtes est un outil direct de détection du phishing, en complément de la vigilance sur le contenu visible du message.

## 🎓 Ce que vous avez appris

✅ Décomposer une adresse e-mail pour en tirer des indices OSINT
✅ Lire et interpréter les en-têtes complets d'un e-mail
✅ Vérifier une fuite de données de façon éthique
✅ Reconnaître les signaux de phishing dans les en-têtes techniques

## ➡️ Leçon suivante

**18 : WHOIS et approfondissement des domaines** : au-delà des bases déjà vues, les subtilités et les limites de l'information WHOIS moderne. Fichier : `18-domaine-whois.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
