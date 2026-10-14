---
title: "WHOIS Approfondi : Au-delà des Bases"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 18
category: "osint"
tags: ["whois", "rdap", "osint", "rgpd", "typosquatting", "python"]
prerequisites: ["17-email-osint", "04-fonctions-modules"]
learning_objectives:
  - "Comprendre pourquoi WHOIS a changé depuis l'arrivée du RGPD"
  - "Utiliser RDAP, le protocole moderne qui remplace progressivement WHOIS"
  - "Automatiser des recherches WHOIS avec Python pour surveiller un ensemble de domaines"
  - "Reconnaître les indices WHOIS d'un domaine de typosquatting"
author: "ECHATS PRO"
language: "fr"
published: true
---

# WHOIS Approfondi : Au-delà des Bases

> 🔔 **IMPORTANT** — Comptez environ 40 minutes. Cette leçon prolonge les bases WHOIS déjà vues en leçon 09 ; relisez-la rapidement si besoin avant de continuer.

## 🎯 Ce que vous allez apprendre 📇

En leçon 09, vous avez utilisé `whois` pour une première reconnaissance. Mais WHOIS a beaucoup changé ces dernières années, notamment sous l'effet des réglementations sur la protection des données personnelles, qui ont considérablement réduit ce que cette base révèle publiquement. Cette leçon approfondit ce que WHOIS peut encore vous apprendre aujourd'hui, introduit son successeur technique (RDAP), et vous montre comment automatiser cette surveillance avec Python.

Vous allez :
- comprendre pourquoi les résultats WHOIS sont aujourd'hui souvent masqués, et ce qui reste malgré tout exploitable,
- utiliser RDAP, le protocole structuré qui remplace progressivement WHOIS,
- automatiser une surveillance de plusieurs domaines avec Python,
- reconnaître, à partir des données d'enregistrement, les indices d'un domaine de typosquatting.

> ⚠️ **AVERTISSEMENT** — Les techniques de cette leçon restent, comme pour toute la reconnaissance passive de ce module, limitées à la consultation d'informations publiques. Automatiser des requêtes WHOIS à très grande échelle peut, selon les registres consultés, être soumis à des limites de débit ou à des conditions d'utilisation spécifiques — respectez-les, comme vous respecteriez celles de toute API (module Python, leçon 06).

## 📚 Prérequis

- Leçon 17 : *E-mail et OSINT*
- Module Python, leçon 04 : *Fonctions, modules et gestion des erreurs*

## Pourquoi WHOIS a changé

### Avant et après le RGPD

Historiquement, une recherche WHOIS révélait souvent le nom complet, l'adresse postale, le numéro de téléphone et l'adresse e-mail du titulaire d'un nom de domaine — une mine d'informations personnelles directement accessible à quiconque. Depuis l'entrée en vigueur du **RGPD** en Europe, et de réglementations similaires dans d'autres régions du monde, la plupart des registres de domaines ont dû **masquer** ces informations personnelles par défaut, à moins que le titulaire ne soit explicitement une organisation (pas une personne physique) ou qu'il ait consenti à leur publication.

```
Registrant Name: REDACTED FOR PRIVACY
Registrant Organization: REDACTED FOR PRIVACY
Registrant Email: Please query the RDDS service of the Registrar...
```

> 💡 **CONSEIL** — Ce masquage n'est pas une mauvaise nouvelle pour l'OSINT, c'est une évolution légitime de la protection des données personnelles — exactement le même principe que celui déjà rappelé tout au long de ce module : une information techniquement accessible autrefois ne doit pas nécessairement le rester, si sa divulgation systématique nuit à la vie privée de millions de personnes sans bénéfice proportionné.

### Ce qui reste exploitable malgré le masquage

Même avec ce masquage des données personnelles, une requête WHOIS révèle encore des informations précieuses pour une reconnaissance OSINT :

| Champ encore visible | Utilité |
|---|---|
| **Registrar** | Le bureau d'enregistrement utilisé, parfois révélateur d'une pratique courante dans un secteur ou un pays |
| **Dates de création et d'expiration** | L'ancienneté d'un domaine — un domaine créé il y a quelques jours seulement est un signal d'alerte classique, notamment en analyse de phishing |
| **Serveurs de noms (NS)** | L'infrastructure DNS utilisée, parfois révélatrice d'un hébergeur ou d'un fournisseur cloud |
| **Statut du domaine** | Des indicateurs techniques comme un verrouillage contre le transfert |
| **Organisation du titulaire**, si c'en est une | De nombreuses entreprises choisissent, à l'inverse des particuliers, de laisser leurs informations visibles à des fins de transparence commerciale |

## RDAP : le successeur de WHOIS

### Pourquoi un nouveau protocole

WHOIS, conçu dans les années 1980, renvoie du **texte libre**, sans structure standardisée : chaque registre peut formater sa réponse différemment, ce qui complique l'analyse automatisée. **RDAP** (*Registration Data Access Protocol*), déployé progressivement par les registres depuis plusieurs années, répond en **JSON structuré** — directement exploitable avec les compétences déjà acquises dans ce module (leçon 05, le module `json`).

```bash
curl -s "https://rdap.org/domain/example.com" | python3 -m json.tool
```

```json
{
  "objectClassName": "domain",
  "ldhName": "EXAMPLE.COM",
  "events": [
    {"eventAction": "registration", "eventDate": "1995-08-14T04:00:00Z"},
    {"eventAction": "expiration", "eventDate": "2026-08-13T04:00:00Z"}
  ],
  "nameservers": [...]
}
```

> 📝 **NOTE — Une transition encore en cours**
>
> RDAP ne remplace pas totalement WHOIS du jour au lendemain : selon le registre concerné (le gestionnaire d'une extension de domaine donnée, comme `.com`, `.cg`, ou `.org`), la disponibilité et la richesse des données RDAP varient encore. En pratique, un bon réflexe de reconnaissance consiste à **essayer RDAP en premier** pour sa structure exploitable automatiquement, et à se rabattre sur WHOIS classique si RDAP n'est pas encore disponible pour l'extension concernée.

## Défi : automatiser une surveillance de domaines avec Python

### Construire une fonction de requête RDAP

```python
import requests

def interroger_rdap(domaine):
    url = f"https://rdap.org/domain/{domaine}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur pour {domaine} : {e}")
        return None

donnees = interroger_rdap("example.com")
if donnees:
    for evenement in donnees.get("events", []):
        print(evenement["eventAction"], ":", evenement["eventDate"])
```

Cette fonction reprend directement les bonnes pratiques du module Python (leçon 06) : gestion des erreurs, `timeout`, et traitement de la réponse JSON — appliquées ici à une nouvelle source de données.

### Extraire l'ancienneté d'un domaine

```python
from datetime import datetime, timezone

def anciennete_domaine(domaine):
    donnees = interroger_rdap(domaine)
    if not donnees:
        return None
    for evenement in donnees.get("events", []):
        if evenement["eventAction"] == "registration":
            date_creation = datetime.fromisoformat(evenement["eventDate"].replace("Z", "+00:00"))
            jours = (datetime.now(timezone.utc) - date_creation).days
            return jours
    return None

print(f"Domaine créé il y a {anciennete_domaine('example.com')} jours")
```

`![Capture : terminal exécutant le script Python d'interrogation RDAP, affichant l'ancienneté calculée en jours pour un domaine de test.](img/02-18-rdap-anciennete.png)`

### Surveiller plusieurs domaines à la fois

```python
import time

domaines_a_surveiller = ["example.com", "example.org", "example.net"]

for domaine in domaines_a_surveiller:
    jours = anciennete_domaine(domaine)
    if jours is not None:
        alerte = " ⚠️ DOMAINE RÉCENT" if jours < 30 else ""
        print(f"{domaine:20s} {jours:5d} jours{alerte}")
    time.sleep(1)   # politesse envers le service interrogé, module Python leçon 06
```

> ❓ **DÉFI** — En adaptant ce script à une liste de domaines de votre choix (les vôtres, ou des domaines de test), combien d'entre eux ont moins de 30 jours d'ancienneté ?
>
> <details>
> <summary>Voir un exemple de réflexion</summary>
>
> Sur une liste de domaines légitimes et établis, le résultat attendu est généralement zéro — c'est précisément ce qui rend ce type de script utile en pratique : dans un contexte réel de supervision (par exemple, surveiller des domaines qui ressemblent à celui de votre organisation), un domaine très récent est un signal qui mérite une vérification manuelle immédiate, car il pourrait correspondre à une tentative de typosquatting fraîchement enregistrée.
> </details>

## Reconnaître le typosquatting via WHOIS

Le **typosquatting** consiste à enregistrer un nom de domaine très proche d'un domaine légitime (une faute de frappe courante, un caractère substitué) pour tromper des utilisateurs inattentifs — une technique déjà évoquée dans le module Réseau & Linux (leçon 05, à propos du DNS) comme risque de sécurité. Les données WHOIS ou RDAP fournissent plusieurs indices caractéristiques :

| Indice | Signification |
|---|---|
| Domaine créé très récemment | Un domaine légitime existe depuis des années ; un domaine de typosquatting est souvent enregistré juste avant une campagne |
| Registrar peu habituel pour ce secteur | Certains registrars sont régulièrement associés à des usages abusifs, sans que ce soit systématique |
| Informations de titulaire masquées via un service tiers générique | Fréquent pour masquer l'identité réelle derrière un domaine malveillant, bien que ce ne soit pas, à lui seul, une preuve |
| Serveurs de noms différents de ceux du domaine légitime qu'il imite | Signale une infrastructure totalement distincte, cohérente avec une usurpation |

> 💡 **CONSEIL** — Aucun de ces indices, pris isolément, ne prouve une intention malveillante — un nouveau projet légitime crée aussi, légitimement, un domaine récent. C'est le même principe de recoupement déjà répété tout au long de ce module : combinez plusieurs indices avant de conclure, et confrontez-les, si possible, au contenu réel du site (reprend-il visuellement l'identité visuelle d'une marque connue ?) avant toute conclusion.

## WHOIS, côté défensif

Une organisation peut utiliser ces mêmes techniques pour se protéger :
- **surveiller périodiquement** l'enregistrement de domaines proches du sien (variantes orthographiques, extensions différentes) pour détecter rapidement une tentative de typosquatting ;
- **enregistrer préventivement** les variantes les plus évidentes de son propre nom de domaine, une pratique courante chez les grandes marques ;
- **intégrer cette veille** dans le même type de script de supervision que celui construit dans cette leçon, à exécuter périodiquement plutôt qu'une seule fois.

## 🔍 Pour aller plus loin

- La documentation du protocole RDAP (rdap.org), avec la liste des registres qui le prennent en charge.
- L'ICANN publie régulièrement des ressources sur l'évolution de WHOIS face aux réglementations de protection des données.
- Le module Sécurité Web & Pentest, leçon 14, sur l'énumération de sous-domaines, qui complète cette surveillance de domaines par une dimension technique supplémentaire.

## 🧪 Quiz de validation

**Question 1 : Pourquoi de nombreuses informations personnelles ont-elles disparu des résultats WHOIS ces dernières années ?**
- A) Parce que WHOIS a été entièrement remplacé
- B) Sous l'effet de réglementations de protection des données comme le RGPD, qui imposent de masquer les données personnelles par défaut ✅
- C) Parce que les registres ont cessé de collecter ces informations
- D) Parce que ces informations n'ont jamais été publiques

*Explication : le masquage par défaut répond à une exigence légale de protection de la vie privée des titulaires de domaines, particuliers notamment.*

**Question 2 : Quel est l'avantage principal de RDAP par rapport à WHOIS classique ?**
- A) RDAP est gratuit alors que WHOIS est payant
- B) RDAP renvoie des données structurées en JSON, directement exploitables automatiquement, contrairement au texte libre de WHOIS ✅
- C) RDAP ne fonctionne que pour les domaines récents
- D) RDAP ne masque jamais aucune information

*Explication : cette structuration facilite grandement le traitement automatisé par un script, contrairement au format texte non standardisé de WHOIS.*

**Question 3 : Pourquoi l'ancienneté d'un domaine est-elle un indicateur utile en analyse OSINT ?**
- A) Parce qu'un domaine ancien ne peut jamais être malveillant
- B) Parce qu'un domaine très récent, notamment s'il imite un domaine légitime, est un signal fréquent de typosquatting ou de campagne malveillante ✅
- C) Parce que WHOIS n'indique jamais la date de création
- D) Ce n'est jamais un indicateur pertinent

*Explication : combiné à d'autres indices, l'âge d'un domaine aide à distinguer un projet légitime récent d'une tentative d'usurpation.*

**Question 4 : Pourquoi aucun indice de typosquatting, pris isolément, ne constitue-t-il une preuve suffisante ?**
- A) Parce que le typosquatting n'existe pas réellement
- B) Parce qu'un domaine récent ou des informations masquées peuvent aussi correspondre à un usage parfaitement légitime ✅
- C) Parce que WHOIS ne fournit jamais d'indices utiles
- D) Parce que seul un expert judiciaire peut évaluer ces indices

*Explication : le principe de recoupement, déjà posé tout au long de ce module, s'applique ici : combiner plusieurs indices avant de conclure.*

**Question 5 : Quelle mesure défensive une organisation peut-elle mettre en place à partir des techniques de cette leçon ?**
- A) Désactiver complètement son propre nom de domaine
- B) Surveiller périodiquement l'enregistrement de domaines proches du sien, pour détecter rapidement une tentative de typosquatting ✅
- C) Supprimer tous ses enregistrements DNS
- D) Masquer son propre domaine de tout moteur de recherche

*Explication : une veille automatisée, construite sur le même principe que le script de cette leçon, permet une détection précoce de ce risque.*

## 📝 Résumé

- Les réglementations de protection des données ont considérablement réduit les informations personnelles visibles dans WHOIS, sans pour autant le rendre inutile.
- Registrar, dates, serveurs de noms et statut du domaine restent exploitables malgré le masquage.
- RDAP, le successeur structuré de WHOIS, renvoie des données JSON directement traitables avec Python.
- L'automatisation permet une surveillance régulière d'un ensemble de domaines, notamment pour détecter précocement une tentative de typosquatting.
- Aucun indice WHOIS isolé ne constitue une preuve ; le recoupement avec d'autres sources reste indispensable.

## 🎓 Ce que vous avez appris

✅ Comprendre l'évolution de WHOIS face aux réglementations de protection des données
✅ Utiliser RDAP pour des requêtes structurées et automatisables
✅ Automatiser une surveillance de plusieurs domaines avec Python
✅ Reconnaître les indices WHOIS caractéristiques du typosquatting

## ➡️ Leçon suivante

**19 : Rédiger un rapport OSINT** : synthétiser une enquête complète en un document clair, traçable et actionnable — la conclusion du bloc OSINT de ce module. Fichier : `19-rapport-osint.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
