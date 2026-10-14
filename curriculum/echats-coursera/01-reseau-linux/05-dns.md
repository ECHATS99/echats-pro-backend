---
title: "Le DNS : l'annuaire d'Internet"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "debutant"
duration_minutes: 30
order: 5
category: "reseau"
tags: ["reseau", "dns", "resolution", "nslookup", "dig", "dns-spoofing"]
prerequisites: ["04-adressage-ip"]
learning_objectives:
  - "Expliquer comment un nom de domaine est transformé en adresse IP"
  - "Connaître les principaux types d'enregistrements DNS"
  - "Interroger le DNS avec nslookup et dig"
  - "Identifier les attaques courantes visant le DNS"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Le DNS : l'annuaire d'Internet

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Expliquer comment un nom de domaine est transformé en adresse IP
- Connaître les principaux types d'enregistrements DNS
- Interroger le DNS avec `nslookup` et `dig`
- Identifier les attaques courantes visant le DNS

## 📚 Prérequis

- Leçon 04 : *Adressage IP et Sous-réseaux*

## 🧭 Introduction

Personne ne retient `142.250.74.46`. On retient `google.com`. Le **DNS** (*Domain Name System*) est le système qui traduit les noms que nous lisons en adresses IP que les machines utilisent. C'est l'annuaire téléphonique d'Internet : tu cherches un nom, il te donne un numéro.

Sans DNS, le web resterait utilisable, mais uniquement si tu connaissais toutes les adresses par cœur. Et si le DNS tombe en panne, « Internet ne marche plus » pour l'utilisateur, alors que le réseau fonctionne très bien.

En cybersécurité, le DNS est à la fois une **mine d'informations** et une **cible**. En reconnaissance, il révèle les sous-domaines, les serveurs de messagerie, les prestataires d'un organisme. En attaque, on le détourne pour rediriger des victimes vers de faux sites (phishing) ou pour exfiltrer des données. En défense, on le surveille, car un malware doit presque toujours résoudre un nom pour joindre son serveur de commande.

## 📖 Concepts clés

### 1. La structure d'un nom de domaine

Un nom de domaine se lit **de droite à gauche**, du plus général au plus précis :

```
www . exemple . cg .
 |       |      |   └─ racine (root), notée par un point final
 |       |      └──── TLD (domaine de premier niveau) : .cg, .com, .org
 |       └─────────── domaine de second niveau : exemple
 └─────────────────── sous-domaine : www
```

- **TLD** génériques : `.com`, `.org`, `.net` ; **TLD** nationaux (ccTLD) : `.cg` (Congo), `.cm` (Cameroun), `.sn` (Sénégal), `.fr`…
- **FQDN** (*Fully Qualified Domain Name*) : le nom complet, par exemple `mail.exemple.cg.`

### 2. Les acteurs de la résolution

| Acteur | Rôle |
|---|---|
| Client (résolveur stub) | Ta machine : pose la question |
| Résolveur récursif | Fait tout le travail pour toi (celui de ton opérateur, ou 1.1.1.1, 8.8.8.8…) |
| Serveurs racine | Savent qui gère chaque TLD |
| Serveurs de TLD | Savent qui gère chaque domaine (.com, .cg…) |
| Serveurs faisant autorité | Détiennent la réponse définitive pour un domaine |

### 3. Le déroulement d'une résolution

Tu tapes `www.exemple.cg`. Si la réponse n'est pas déjà en mémoire (cache), voici ce qui se passe :

1. Ta machine interroge le **résolveur récursif**.
2. Le résolveur demande à un **serveur racine** : « qui gère `.cg` ? » → il indique les serveurs du TLD `.cg`.
3. Il demande au **serveur du TLD** : « qui gère `exemple.cg` ? » → il indique les serveurs faisant autorité du domaine.
4. Il demande au **serveur faisant autorité** : « quelle est l'IP de `www.exemple.cg` ? » → réponse : `203.0.113.10`.
5. Le résolveur renvoie la réponse à ta machine **et la garde en cache** pendant un temps donné (le **TTL**).

Le cache accélère tout : la plupart des requêtes ne remontent jamais jusqu'à la racine. Le DNS utilise surtout **UDP port 53**, et TCP port 53 pour les réponses volumineuses et les transferts de zone.

### 4. Les types d'enregistrements

Un domaine possède une **zone** : un fichier d'enregistrements (*records*).

| Type | Contenu | Exemple |
|---|---|---|
| A | Nom → adresse IPv4 | `www.exemple.cg → 203.0.113.10` |
| AAAA | Nom → adresse IPv6 | `www → 2001:db8::10` |
| CNAME | Alias vers un autre nom | `blog → www.exemple.cg` |
| MX | Serveur de messagerie du domaine | `mail.exemple.cg (priorité 10)` |
| NS | Serveurs de noms faisant autorité | `ns1.exemple.cg` |
| TXT | Texte libre (SPF, DKIM, vérifications) | `"v=spf1 include:... -all"` |
| PTR | Adresse IP → nom (résolution inverse) | `10.113.0.203 → www.exemple.cg` |
| SOA | Informations administratives de la zone | numéro de série, durées |

Les enregistrements **TXT** sont importants en sécurité : SPF, DKIM et DMARC y publient les règles qui permettent de vérifier qu'un e-mail vient bien du domaine annoncé, ce qui limite l'usurpation (phishing).

### 5. Le cache et le TTL

Chaque enregistrement porte un **TTL** (durée de vie en secondes). Pendant ce temps, les résolveurs gardent la réponse sans reposer la question. Un TTL court (300 s) permet de changer vite une adresse ; un TTL long (86 400 s) réduit la charge. Conséquence pratique : après un changement de DNS, il faut parfois attendre pour que tout le monde voie la nouvelle valeur (« propagation »).

### 6. Le fichier hosts

Avant de questionner le DNS, ta machine consulte un fichier local de correspondances :
- Windows : `C:\Windows\System32\drivers\etc\hosts`
- Linux/macOS : `/etc/hosts`

Un malware peut y ajouter une ligne pour rediriger `banque.exemple` vers une fausse adresse. Vérifier ce fichier est un réflexe d'investigation.

### 7. DNS et sécurité : les attaques classiques

| Attaque | Principe | Défense |
|---|---|---|
| **Empoisonnement de cache** (*cache poisoning*) | Injecter de fausses réponses dans le cache d'un résolveur pour rediriger les utilisateurs | DNSSEC, ports et identifiants aléatoires, résolveurs à jour |
| **Détournement DNS** (*DNS hijacking*) | Modifier les paramètres DNS d'un routeur, d'un poste ou d'un compte chez le registrar | Changer les mots de passe par défaut, authentification forte sur le compte du domaine |
| **Typosquatting** | Enregistrer un nom proche (`g00gle.com`) pour piéger les distraits | Vigilance, filtrage, surveillance de marque |
| **Tunnel DNS** | Cacher des données dans des requêtes DNS pour exfiltrer ou commander un malware | Surveillance du volume et de la forme des requêtes |
| **Amplification DNS (DDoS)** | Utiliser des résolveurs ouverts pour amplifier un trafic vers une victime | Fermer les résolveurs ouverts, limiter le débit |
| **Transfert de zone non protégé** | Un serveur renvoie toute sa zone à quiconque la demande (AXFR) | Restreindre les transferts aux serveurs secondaires autorisés |

**DNSSEC** ajoute des signatures cryptographiques aux réponses pour vérifier leur authenticité. **DoH** (DNS over HTTPS) et **DoT** (DNS over TLS) chiffrent les requêtes entre ton appareil et le résolveur : ton fournisseur d'accès ne lit plus tes requêtes en clair, mais le résolveur, lui, les voit.

### 8. DNS et reconnaissance (OSINT)

Les informations DNS publiques aident à cartographier une organisation : sous-domaines oubliés, serveurs de messagerie, services tiers. Interroger des enregistrements **publics** est légal et courant ; en revanche, tenter des transferts de zone ou des énumérations massives sur un domaine qui n'est pas le tien relève, selon les cas, de l'abus. On y reviendra dans le module OSINT.

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : les requêtes DNS simples vers des domaines publics sont inoffensives. Pour tout ce qui va plus loin (énumération intensive, tentatives de transfert de zone), travaille uniquement sur **tes propres domaines** ou avec une autorisation écrite.

### Exercice 1 — Résolution simple avec nslookup

```bash
nslookup example.com
```

Résultat attendu : le serveur DNS utilisé (ton résolveur) puis une ou plusieurs adresses IP. Observe la mention « Non-authoritative answer » : la réponse vient d'un cache, pas du serveur qui fait autorité.

### Exercice 2 — Interroger des types précis avec dig

```bash
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com NS
dig example.com TXT
```

Repère dans la sortie :
- la section **ANSWER** (la réponse) ;
- le **TTL** (nombre à gauche de la valeur) ;
- le temps de requête (`Query time`).

Sous Windows, `nslookup -type=MX example.com` donne un résultat équivalent.

### Exercice 3 — Voir le cache en action

```bash
dig example.com | grep "Query time"
dig example.com | grep "Query time"
```

La seconde requête est généralement plus rapide : le résolveur a mis la réponse en cache. Relance une troisième fois en regardant le TTL qui diminue.

### Exercice 4 — Résolution inverse

```bash
dig -x 8.8.8.8
```

Tu obtiens le nom associé à l'adresse (enregistrement PTR). Teste avec une autre adresse publique connue.

### Exercice 5 — Choisir le résolveur

```bash
dig @1.1.1.1 example.com
dig @8.8.8.8 example.com
```

Compare les réponses et les temps. Tu observes que le résolveur est un choix, et que changer de résolveur modifie qui voit tes requêtes.

### Exercice 6 — Inspecter ton fichier hosts

```bash
# Linux/macOS
cat /etc/hosts

# Windows
type C:\Windows\System32\drivers\etc\hosts
```

Tu dois y voir surtout des commentaires et `127.0.0.1 localhost`. Toute ligne inconnue mérite d'être comprise.

### Exercice 7 — Capturer une requête DNS

Dans Wireshark, filtre `dns`, puis ouvre un site : repère la requête (« Standard query ») et la réponse (« Standard query response »). Note que le nom demandé est visible en clair.

## 🔍 Approfondissement

### Pour aller plus loin

- La documentation de `dig` (`man dig`).
- Le guide « DNS » de Cloudflare Learning Center.
- RFC 1034 et 1035 pour les fondamentaux du DNS.

### Pièges courants

- ❌ **Erreur fréquente 1** : dire « le site est en panne » alors que seul le DNS pose problème. Si `ping 8.8.8.8` fonctionne mais `ping example.com` échoue, le défaut est dans la résolution de noms.
- ✅ **Bonne pratique** : tester par adresse IP puis par nom pour isoler le problème.
- ❌ **Erreur fréquente 2** : croire que les requêtes DNS sont chiffrées par défaut. Elles circulent généralement en clair.
- ✅ **Bonne pratique** : activer DoH ou DoT quand c'est possible, et comprendre à qui l'on fait confiance.
- ❌ **Erreur fréquente 3** : négliger la sécurité du compte chez le registrar. Quiconque contrôle ce compte contrôle le domaine entier.
- ✅ **Bonne pratique** : authentification à deux facteurs, verrouillage du domaine, surveillance des changements d'enregistrements.

## 🧪 Quiz de validation

**Question 1 : Quel enregistrement associe un nom à une adresse IPv4 ?**
- A) MX
- B) CNAME
- C) A ✅
- D) TXT

*Explication : l'enregistrement A fait correspondre un nom à une IPv4 ; AAAA fait de même pour l'IPv6.*

**Question 2 : Quel protocole et quel port utilise principalement le DNS ?**
- A) TCP 80
- B) UDP 53 ✅
- C) TCP 443
- D) UDP 67

*Explication : les requêtes DNS standard passent en UDP port 53, avec repli sur TCP 53 quand c'est nécessaire.*

**Question 3 : À quoi sert le TTL d'un enregistrement ?**
- A) À chiffrer la réponse
- B) À indiquer combien de temps la réponse peut rester en cache ✅
- C) À choisir le serveur de messagerie
- D) À bloquer un domaine

*Explication : le TTL fixe la durée pendant laquelle un résolveur garde la réponse avant de la redemander.*

**Question 4 : L'empoisonnement de cache DNS consiste à…**
- A) Surcharger un serveur de requêtes
- B) Injecter de fausses réponses dans le cache d'un résolveur ✅
- C) Chiffrer le trafic DNS
- D) Supprimer un domaine du registre

*Explication : les utilisateurs du résolveur sont alors redirigés vers de fausses adresses.*

**Question 5 : Quel mécanisme ajoute des signatures pour authentifier les réponses DNS ?**
- A) DHCP
- B) NAT
- C) DNSSEC ✅
- D) ARP

*Explication : DNSSEC permet de vérifier que la réponse provient bien du serveur légitime et n'a pas été modifiée.*

## 📝 Résumé

- Le DNS traduit les noms de domaine en adresses IP, par une chaîne : résolveur → racine → TLD → serveur faisant autorité.
- Les enregistrements A, AAAA, CNAME, MX, NS, TXT et PTR décrivent un domaine.
- Le cache et le TTL accélèrent les réponses mais retardent la propagation des changements.
- `nslookup` et `dig` sont les outils de base pour interroger le DNS.
- Le DNS est exposé à l'empoisonnement de cache, au détournement, au typosquatting, au tunnel DNS et à l'amplification ; DNSSEC, DoH et DoT en limitent les risques.

## 🎓 Ce que tu as appris

✅ Décrire une résolution DNS complète
✅ Lire les principaux enregistrements d'un domaine
✅ Interroger le DNS avec `nslookup` et `dig`
✅ Reconnaître les attaques DNS et leurs parades

## ➡️ Leçon suivante

**06 : HTTP et HTTPS** : le protocole du web, les requêtes et réponses, les codes d'état, les cookies et le rôle de TLS. Fichier : `06-http-https.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
