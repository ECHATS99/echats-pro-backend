---
title: "Analyse de Métadonnées : ce que les Fichiers Révèlent"
module: "Python & OSINT"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 15
category: "osint"
tags: ["metadonnees", "exif", "exiftool", "documents", "python", "nettoyage"]
prerequisites: ["14-shodan-censys", "05-fichiers-io"]
learning_objectives:
  - "Comprendre ce que sont les métadonnées et pourquoi elles existent"
  - "Extraire les métadonnées d'une photo et d'un document avec exiftool et Python"
  - "Identifier les métadonnées les plus sensibles à vérifier avant publication"
  - "Nettoyer les métadonnées d'un fichier avant de le partager"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Analyse de Métadonnées : ce que les Fichiers Révèlent

> 🔔 **IMPORTANT** — Comptez environ 40 minutes. Vous aurez besoin d'installer `exiftool` et d'avoir quelques photos ou documents de test sous la main.

## 🎯 Ce que vous allez apprendre 📎

Une photo semble montrer seulement une image. Un document PDF semble ne contenir que du texte. Pourtant, chaque fichier transporte souvent, invisible à l'affichage normal, une quantité surprenante d'informations : l'appareil qui a pris la photo, parfois sa position GPS exacte, le nom de l'auteur d'un document, le logiciel utilisé, l'historique des modifications. Ce sont les **métadonnées** — littéralement, des données sur les données — et elles constituent l'une des sources OSINT les plus sous-estimées, précisément parce qu'elles sont invisibles à l'œil nu.

Vous allez :
- comprendre ce que sont les métadonnées et pourquoi les fichiers en contiennent autant,
- extraire ces informations avec `exiftool` et avec Python,
- identifier les métadonnées les plus sensibles à vérifier systématiquement avant de publier un fichier,
- apprendre à nettoyer un fichier avant de le partager, pour votre propre protection.

> ⚠️ **AVERTISSEMENT** — Analyser les métadonnées d'un fichier que **vous possédez** ou qui vous a été **légitimement transmis** dans un cadre autorisé ne pose pas de problème particulier. Mais si cette analyse révèle des informations personnelles sur une tierce personne (localisation, identité), rappelez-vous le cadre déjà posé dans ce module (leçons 09 et 11) : ces informations restent protégées, et leur exploitation à des fins de surveillance ou de nuisance reste strictement interdite.

## 📚 Prérequis

- Leçon 14 : *Shodan et Censys*
- Module Python, leçon 05 : *Fichiers et entrées/sorties* (notion de signature de fichier)

## D'où viennent les métadonnées

### Un fichier, deux niveaux de contenu

Dans la leçon 05 du module Python, vous avez appris à lire les premiers octets d'un fichier pour en identifier le vrai type (sa **signature**). Les métadonnées prolongent cette idée : au-delà du contenu principal (les pixels d'une image, le texte d'un document), le format de fichier lui-même prévoit des emplacements dédiés pour stocker des informations **sur** ce contenu.

Pour les photos, ce standard s'appelle **EXIF** (*Exchangeable Image File Format*), intégré par défaut par la quasi-totalité des appareils photo et smartphones. Il peut contenir :

| Champ EXIF | Information |
|---|---|
| Date et heure de prise de vue | Horodatage précis |
| Modèle de l'appareil | Marque et modèle du téléphone ou de l'appareil photo |
| Paramètres techniques | Ouverture, vitesse, ISO, focale |
| **Coordonnées GPS** | Latitude et longitude exactes du lieu de prise de vue, si la géolocalisation était activée |
| Logiciel de traitement | Si l'image a été modifiée, par quel logiciel |

Les documents bureautiques (Word, PDF, tableurs) ont leurs propres métadonnées : auteur, organisation, logiciel et version utilisés, dates de création et de dernière modification, et parfois un **historique des révisions** ou des commentaires que l'auteur pensait avoir supprimés mais qui restent techniquement présents dans le fichier.

> 💡 **CONSEIL** — Les métadonnées existent pour des raisons légitimes : elles permettent à votre galerie photo de trier vos souvenirs par lieu et par date, à un logiciel de montage de régler automatiquement l'exposition d'une photo, à une équipe de savoir qui a rédigé quelle partie d'un document collaboratif. Le problème n'est pas leur existence, mais le fait qu'elles **voyagent avec le fichier** même quand on ne le souhaite plus au moment de le partager.

## Extraire les métadonnées

### Avec exiftool

**exiftool** est l'outil de référence, gratuit et très complet, pour lire (et modifier) les métadonnées de presque tous les formats de fichiers courants.

```bash
exiftool photo.jpg
```

```
Make                            : Apple
Camera Model Name               : iPhone 13
Date/Time Original              : 2026:03:15 14:32:07
GPS Latitude                    : 4 deg 16' 12.00" S
GPS Longitude                   : 15 deg 17' 24.00" E
GPS Position                    : 4 deg 16' 12.00" S, 15 deg 17' 24.00" E
```

`![Capture : terminal affichant la sortie complète de la commande exiftool sur une photo de test, avec les champs GPS Latitude et GPS Longitude mis en évidence par un encadré rouge.](img/02-15-exiftool-gps.png)`

Pour un document PDF ou Word :

```bash
exiftool rapport.pdf
```

```
Author                          : Prénom Nom
Creator                         : Microsoft Word
Create Date                     : 2026:01:10 09:15:00
Modify Date                     : 2026:03:02 16:40:12
```

### Avec Python

Les compétences du module Python s'appliquent directement à un traitement par lot. La bibliothèque `Pillow` extrait les métadonnées EXIF des images :

```python
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extraire_exif(chemin):
    image = Image.open(chemin)
    exif_brut = image._getexif()
    if not exif_brut:
        return {}
    return {TAGS.get(cle, cle): valeur for cle, valeur in exif_brut.items()}

donnees = extraire_exif("photo.jpg")
for cle, valeur in donnees.items():
    print(cle, ":", valeur)
```

Pour les coordonnées GPS, un traitement supplémentaire est nécessaire car elles sont stockées dans un format imbriqué spécifique (degrés, minutes, secondes) qu'il faut convertir en coordonnées décimales utilisables, par exemple, sur une carte.

## Défi : auditer vos propres fichiers

### Analyser une photo que vous avez prise

Choisissez une photo récente prise avec votre propre téléphone (pas une photo téléchargée depuis Internet, qui a souvent déjà perdu ses métadonnées lors de l'upload sur certaines plateformes qui les suppriment automatiquement). Exécutez `exiftool` dessus.

> ❓ **DÉFI** — Votre photo contient-elle des coordonnées GPS ? Si oui, correspondent-elles bien au lieu où vous avez réellement pris la photo ?
>
> <details>
> <summary>Voir un exemple de réflexion</summary>
>
> Si des coordonnées GPS apparaissent et correspondent au lieu réel de la prise de vue, vous venez de constater concrètement ce qu'une photo « anodine » publiée en ligne peut révéler de votre position exacte au moment où elle a été prise — y compris, potentiellement, votre domicile si la photo a été prise chez vous. Si aucune coordonnée n'apparaît, c'est soit que la géolocalisation était désactivée sur votre appareil au moment de la prise de vue, soit que le fichier a déjà transité par un service qui supprime ces métadonnées automatiquement (de nombreux réseaux sociaux le font, précisément pour cette raison de confidentialité).
> </details>

### Analyser un document

Si vous avez accès à un document PDF ou Word que vous avez créé (ou que votre organisation utilise, avec son accord), examinez ses métadonnées. Le champ « Auteur » correspond-il à une vraie personne identifiable ? Le champ « Entreprise » ou « Organisation » révèle-t-il le nom du logiciel utilisé en interne pour produire ce type de document ?

> 📝 **NOTE — Le cas John McAfee**
>
> En décembre 2012, John McAfee — fondateur de l'entreprise de logiciels antivirus du même nom — était recherché par les autorités du Belize comme personne d'intérêt dans une enquête pour homicide, et se trouvait en fuite. Le magazine Vice, dont des journalistes l'accompagnaient, a publié en ligne une photo de lui prise avec un iPhone. La photo contenait encore ses métadonnées EXIF complètes, avec des coordonnées GPS précises situant la prise de vue dans un complexe au Guatemala. Des observateurs ont immédiatement relevé cette donnée, révélant publiquement sa localisation. McAfee a ensuite affirmé avoir lui-même falsifié ces coordonnées pour semer volontairement les autorités — une version qui n'a jamais été confirmée avec certitude. Que la fuite ait été accidentelle ou mise en scène, ce cas, largement documenté dans la presse technologique de l'époque, reste un exemple de référence dans les formations en sécurité opérationnelle, pour illustrer à quel point une métadonnée oubliée peut trahir une information qu'aucun élément visible de la photo ne révélait.

### Nettoyer un fichier avant de le partager

Pour retirer les métadonnées avant de partager un fichier (une photo que vous publiez, un document que vous transmettez à l'extérieur de votre organisation) :

```bash
# Retirer toutes les métadonnées, en gardant une copie de l'original
exiftool -all= photo.jpg

# Vérifier que le nettoyage a bien fonctionné
exiftool photo_sans_exif.jpg
```

En Python, avec Pillow, il est possible de réenregistrer une image sans ses données EXIF :

```python
from PIL import Image

image = Image.open("photo.jpg")
donnees = list(image.getdata())
image_nettoyee = Image.new(image.mode, image.size)
image_nettoyee.putdata(donnees)
image_nettoyee.save("photo_nettoyee.jpg")
```

> 💡 **CONSEIL** — Prenez l'habitude de vérifier les métadonnées de tout fichier que vous vous apprêtez à publier publiquement — une photo sur un réseau social, un document partagé en ligne, un rapport destiné à un public externe. C'est un réflexe rapide une fois automatisé, et il évite de révéler involontairement une information que vous n'aviez pas l'intention de partager.

## Les métadonnées, côté défensif

Au-delà de la vigilance individuelle, une organisation peut mettre en place :
- une **politique de nettoyage automatique** des métadonnées avant toute publication externe de documents ;
- une **sensibilisation** des équipes communication et marketing, souvent les premières à publier des photos et documents sans y penser ;
- une **vérification systématique**, dans le cadre d'une reconnaissance OSINT de sa propre organisation (lien direct avec les leçons 09, 10 et 14 de ce module), des documents déjà publiés sur son propre site, qui peuvent révéler des informations accumulées sur plusieurs années.

## 🔍 Pour aller plus loin

- La documentation complète d'exiftool, qui couvre des centaines de formats de fichiers au-delà des photos et documents courants.
- Les bibliothèques Python `Pillow` et `python-docx`, pour un traitement par lot automatisé des métadonnées d'images et de documents Word.
- Le module Forensic Numérique, qui approfondit l'usage des métadonnées comme preuve dans une investigation.

## 🧪 Quiz de validation

**Question 1 : Que désigne le terme « métadonnées » appliqué à un fichier ?**
- A) Le contenu principal du fichier, comme le texte ou les pixels
- B) Des informations sur le fichier lui-même — auteur, date, appareil, parfois localisation — distinctes de son contenu principal ✅
- C) Un type de virus informatique
- D) Le nom du fichier uniquement

*Explication : les métadonnées décrivent le contexte de création d'un fichier, séparément de son contenu visible.*

**Question 2 : Quel standard regroupe les métadonnées techniques des photos, incluant parfois des coordonnées GPS ?**
- A) HTML
- B) EXIF ✅
- C) CSV
- D) DNS

*Explication : EXIF est le format standard intégré par défaut par la quasi-totalité des appareils photo et smartphones.*

**Question 3 : Pourquoi une photo téléchargée depuis certains réseaux sociaux a-t-elle souvent perdu ses métadonnées EXIF ?**
- A) Parce que les réseaux sociaux ne peuvent pas techniquement les afficher
- B) Parce que de nombreuses plateformes les suppriment automatiquement, notamment pour des raisons de confidentialité ✅
- C) Parce que les métadonnées disparaissent naturellement avec le temps
- D) Parce que seules les photos prises avec un appareil professionnel en contiennent

*Explication : cette suppression automatique, pratiquée par plusieurs grandes plateformes, répond précisément au risque de confidentialité illustré dans cette leçon.*

**Question 4 : Que révélait la métadonnée GPS dans le cas John McAfee cité dans cette leçon ?**
- A) Le mot de passe de son ordinateur
- B) Les coordonnées précises du lieu où la photo publiée en ligne avait été prise ✅
- C) Son numéro de téléphone
- D) Son adresse e-mail

*Explication : les coordonnées GPS intégrées à la photo publiée par Vice situaient précisément sa localisation au Guatemala, qu'il ait ou non falsifié ces données par la suite.*

**Question 5 : Quelle commande exiftool permet de retirer toutes les métadonnées d'un fichier avant de le partager ?**
- A) `exiftool -list photo.jpg`
- B) `exiftool -all= photo.jpg` ✅
- C) `exiftool -gps photo.jpg`
- D) `exiftool -copy photo.jpg`

*Explication : l'option `-all=` indique à exiftool de supprimer l'ensemble des champs de métadonnées du fichier, tout en conservant son contenu principal.*

## 📝 Résumé

- Les métadonnées sont des informations sur un fichier, distinctes de son contenu principal, existant pour des raisons légitimes mais qui voyagent avec le fichier au-delà de leur usage initial.
- EXIF regroupe les métadonnées des photos, incluant potentiellement des coordonnées GPS précises ; les documents bureautiques ont leurs propres champs (auteur, dates, historique).
- `exiftool` et les bibliothèques Python comme Pillow permettent d'extraire et de traiter ces informations.
- Un cas réel documenté montre comment une métadonnée oubliée a permis de localiser une personne à partir d'une simple photo partagée en ligne.
- Nettoyer systématiquement les métadonnées avant publication externe est une bonne pratique individuelle et organisationnelle.

## 🎓 Ce que vous avez appris

✅ Comprendre ce que sont les métadonnées et pourquoi les fichiers en contiennent
✅ Extraire des métadonnées EXIF et documentaires avec exiftool et Python
✅ Identifier les champs les plus sensibles à vérifier avant publication
✅ Nettoyer un fichier de ses métadonnées avant de le partager

## ➡️ Leçon suivante

**16 : Géolocalisation d'image** : retrouver le lieu de prise de vue d'une photo à partir d'indices visuels, quand les métadonnées ont été supprimées. Fichier : `16-geolocalisation-image.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
