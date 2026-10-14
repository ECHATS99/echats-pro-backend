---
title: "Analyse Réseau avec Wireshark"
module: "Réseau & Linux"
track: "Fondamentaux Cybersécurité"
difficulty: "intermediaire"
duration_minutes: 40
order: 15
category: "reseau"
tags: ["wireshark", "tcpdump", "capture", "analyse-reseau", "filtres", "pcap", "forensic"]
prerequisites: ["02-modele-osi", "03-tcp-ip", "05-dns", "06-http-https"]
learning_objectives:
  - "Capturer du trafic sur son propre réseau avec Wireshark et tcpdump"
  - "Utiliser filtres de capture et filtres d'affichage"
  - "Suivre une conversation TCP et analyser DNS, HTTP et TLS"
  - "Repérer des anomalies courantes dans un fichier de capture"
author: "ECHATS PRO"
language: "fr"
published: true
---

# Analyse Réseau avec Wireshark

## 🎯 Objectifs pédagogiques

À la fin de cette leçon, tu seras capable de :
- Capturer du trafic sur ton propre réseau avec Wireshark et `tcpdump`
- Utiliser filtres de capture et filtres d'affichage
- Suivre une conversation TCP et analyser DNS, HTTP et TLS
- Repérer des anomalies courantes dans un fichier de capture

## 📚 Prérequis

- Leçons 02, 03, 05 et 06 : modèle OSI, TCP/IP, DNS, HTTP/HTTPS

## 🧭 Introduction

Jusqu'ici, tu as appris la théorie des réseaux. **Wireshark** te permet de la **voir**. C'est un analyseur de paquets (*packet sniffer*) : il capture les trames qui passent sur une interface réseau et les décode, couche par couche, en un format lisible. C'est le microscope du réseau.

Il est utilisé tous les jours par les administrateurs pour diagnostiquer des lenteurs et des pannes, par les analystes SOC pour comprendre une alerte, par les équipes forensic pour reconstituer un incident à partir d'une capture, et par les participants de CTF pour résoudre des défis d'analyse de trafic.

C'est aussi un outil à haute responsabilité. Capturer le trafic d'autrui peut révéler des mots de passe, des messages privés, des données personnelles. **Capturer sur un réseau qui n'est pas le tien, ou sans autorisation, est illégal** dans la plupart des juridictions, et contraire à l'éthique. Dans cette leçon, tu captureras uniquement **ton propre trafic** sur **ta propre machine**.

## 📖 Concepts clés

### 1. Comment fonctionne une capture

Ta carte réseau ne transmet normalement au système que les trames qui lui sont **destinées** (ou diffusées). Pour capturer, l'outil s'appuie sur une bibliothèque (**libpcap** sous Linux/macOS, **Npcap** sous Windows) qui lit les trames de l'interface.

Le **mode promiscuité** (*promiscuous mode*) permet à la carte d'accepter **toutes** les trames qui passent sur le support, pas seulement les siennes. Sur un réseau commuté (switch), tu ne verras toutefois que ton propre trafic et les diffusions, car le switch n'envoie à chaque port que ce qui le concerne (voir leçon 08). Sur le Wi-Fi, le chiffrement du réseau limite aussi ce que tu peux lire du trafic des autres.

Les captures s'enregistrent au format **PCAP** ou **PCAPNG** (extensions `.pcap`, `.pcapng`), échangeables entre outils et idéales pour l'analyse après coup.

### 2. L'interface de Wireshark

Trois panneaux principaux :

```
┌──────────────────────────────────────────────────────┐
│ Barre de filtre d'affichage  [ tcp.port == 443      ] │
├──────────────────────────────────────────────────────┤
│ 1. Liste des paquets (N°, Temps, Source, Destination, │
│    Protocole, Longueur, Info)                         │
├──────────────────────────────────────────────────────┤
│ 2. Détail du paquet sélectionné (couche par couche)   │
├──────────────────────────────────────────────────────┤
│ 3. Octets bruts en hexadécimal et ASCII               │
└──────────────────────────────────────────────────────┘
```

Le panneau de détail reflète l'encapsulation (leçon 02) : *Frame* → *Ethernet* → *IP* → *TCP/UDP* → protocole applicatif.

**Code couleur par défaut** (modifiable) : vert clair pour TCP, bleu clair pour UDP/DNS, noir avec texte rouge pour les erreurs TCP, etc.

### 3. Filtres de capture et filtres d'affichage

Deux types de filtres, souvent confondus :

| | Filtre de **capture** | Filtre d'**affichage** |
|---|---|---|
| Quand | **Avant** de capturer | **Après**, sur ce qui est capturé |
| Effet | Seuls les paquets correspondants sont enregistrés | Tout est enregistré, on n'affiche qu'une partie |
| Syntaxe | BPF (Berkeley Packet Filter) | Langage propre à Wireshark |
| Exemple | `tcp port 80` | `tcp.port == 80` |
| Usage | Gros volumes, limiter la taille du fichier | Analyse fine |

**Filtres de capture (BPF) fréquents :**

```
host 192.168.1.25            # trafic vers ou depuis cette IP
net 192.168.1.0/24           # un sous-réseau
port 53                      # un port (DNS)
tcp port 443                 # TCP sur le port 443
not port 22                  # tout sauf SSH
host 8.8.8.8 and udp port 53 # combinaison
```

**Filtres d'affichage fréquents :**

```
ip.addr == 192.168.1.25         # IP source ou destination
ip.src == 192.168.1.25
ip.dst == 8.8.8.8
tcp.port == 443
udp.port == 53
dns                              # tout le trafic DNS
http                             # requêtes et réponses HTTP en clair
tls                              # trafic TLS
icmp
arp
tcp.flags.syn == 1 && tcp.flags.ack == 0    # uniquement les SYN initiaux
http.request.method == "POST"
dns.qry.name contains "exemple"
frame contains "password"       # recherche d'un texte dans les paquets
tcp.analysis.retransmission     # retransmissions TCP
!(arp || dns)                    # tout sauf ARP et DNS
```

Les opérateurs : `==`, `!=`, `>`, `<`, `contains`, `matches`, et pour combiner `&&` (et), `||` (ou), `!` (non).

La barre de filtre devient **verte** si la syntaxe est valide, **rouge** sinon.

### 4. Suivre une conversation

Une page web, c'est des dizaines de paquets mélangés. Pour reconstituer **un échange complet** : clic droit sur un paquet → **Suivre → Flux TCP** (*Follow → TCP Stream*). Wireshark réassemble les données dans l'ordre :
- en **rouge** : ce que le client a envoyé ;
- en **bleu** : ce que le serveur a répondu.

C'est ainsi qu'on voit une requête HTTP complète, une session Telnet ou FTP en clair, ou un échange de messagerie non chiffré. Équivalents : *UDP Stream*, *TLS Stream*, *HTTP Stream*.

**Statistiques utiles** (menu *Statistiques*) :
- **Conversations** : qui parle avec qui, combien d'octets, combien de paquets ;
- **Endpoints** : volumétrie par adresse ;
- **Hiérarchie des protocoles** : répartition du trafic par protocole ;
- **Graphique des E/S** : le trafic dans le temps (pics, régularités).

### 5. Lire les protocoles courants

**ARP** : repère les requêtes (*Who has…?*) et les réponses (*is at…*). Des réponses ARP répétées et non sollicitées, ou deux adresses IP associées à une même MAC, sont des signes possibles d'empoisonnement ARP.

**DNS** : requête (*Standard query*) et réponse (*Standard query response*). On lit le nom demandé, le type (A, AAAA, MX…), les adresses renvoyées. Des requêtes DNS vers des noms aléatoires très longs ou très nombreux peuvent signaler un tunnel DNS ou un malware.

**TCP** : poignée de main SYN, SYN-ACK, ACK ; flags FIN et RST pour la fermeture. Les retransmissions et les « Dup ACK » signalent des pertes ou de la congestion. Wireshark les colore automatiquement.

**HTTP (en clair)** : lignes de requête (`GET /index.html`), en-têtes, corps. Les formulaires envoyés en HTTP non chiffré exposent leurs données.

**TLS** : la poignée de main (*Client Hello*, *Server Hello*, certificat) est lisible ; le contenu applicatif ne l'est pas. Dans le *Client Hello*, l'extension **SNI** (*Server Name Indication*) révèle souvent le nom du site visité, même en HTTPS.

### 6. Capturer en ligne de commande avec tcpdump

Sur les serveurs sans interface graphique, on utilise **tcpdump** :

```bash
sudo tcpdump -D                          # liste les interfaces
sudo tcpdump -i eth0                     # capture sur eth0
sudo tcpdump -i eth0 -n                  # sans résolution de noms
sudo tcpdump -i eth0 -n port 53          # filtre : DNS
sudo tcpdump -i eth0 -n host 192.168.1.1 and icmp
sudo tcpdump -i eth0 -c 100 -w capture.pcap   # 100 paquets, écrits dans un fichier
sudo tcpdump -r capture.pcap -n          # relire un fichier
```

Le fichier `capture.pcap` s'ouvre ensuite dans Wireshark pour une analyse confortable. **tshark** est la version ligne de commande de Wireshark, qui accepte les filtres d'affichage :

```bash
tshark -r capture.pcap -Y "dns" -T fields -e ip.src -e dns.qry.name
```

### 7. Déchiffrer ou non le trafic

Le trafic HTTPS n'est lisible que si l'on dispose des **clés de session**. Les navigateurs peuvent les exporter dans un fichier si on définit la variable d'environnement `SSLKEYLOGFILE`. Wireshark peut alors déchiffrer **ta propre** navigation (*Édition → Préférences → Protocoles → TLS → (Pre)-Master-Secret log filename*). C'est utile pour déboguer **tes** applications, pas pour espionner autrui, ce que le chiffrement empêche précisément.

### 8. Quelques scénarios d'analyse en sécurité

| Observation | Hypothèse | Vérification |
|---|---|---|
| Beaucoup de SYN sans ACK depuis une IP, vers de nombreux ports | Scan de ports | Filtre `tcp.flags.syn==1 && tcp.flags.ack==0`, statistiques de conversations |
| Rafale de SYN vers un seul port, adresses sources variées | SYN flood (déni de service) | Graphique E/S, conversations |
| Identifiants visibles dans un flux HTTP/FTP/Telnet | Protocole non chiffré | *Follow TCP Stream* |
| Requêtes DNS longues, périodiques, vers un domaine inconnu | Balise de malware ou tunnel DNS | Filtre `dns`, noms interrogés, régularité temporelle |
| Connexions sortantes régulières (toutes les 60 s) vers une IP étrangère | Balise de commande et contrôle (C2) | Statistiques, intervalles, destination |
| Réponses ARP en masse, MAC dupliquée | Empoisonnement ARP | Filtre `arp`, comparaison IP ↔ MAC |
| Nombreuses retransmissions | Problème réseau, pas forcément malveillant | `tcp.analysis.retransmission` |

La méthode : **hypothèse → filtre → preuve**, puis documenter ce qu'on voit, avec les numéros de paquets.

### 9. Éthique et légalité de la capture

- Ne capture que **ton réseau** ou un réseau pour lequel tu as une **autorisation écrite**.
- Les captures contiennent des **données personnelles** : stocke-les de façon sécurisée, limite leur durée de conservation, partage-les uniquement après **anonymisation** (par exemple avec `tcprewrite` ou en supprimant les contenus sensibles).
- Dans une entreprise, la surveillance du trafic des employés est encadrée par la loi et le règlement intérieur.
- Pour t'entraîner sur du trafic « réel » sans risque : captures **publiques** de formation (exercices PCAP, challenges CTF).

## 🛠️ Mise en pratique

> ⚖️ **Rappel légal** : tu captures **uniquement ton propre trafic**, sur **ta propre machine ou un laboratoire que tu possèdes**. Ne lance pas de capture sur un réseau d'école, de cybercafé, d'entreprise ou de Wi-Fi public.

### Exercice 1 — Installer et lancer une première capture

1. Installe Wireshark (wireshark.org). Sous Linux : `sudo apt install wireshark` (accepte l'option pour les utilisateurs non-root, puis ajoute-toi au groupe `wireshark`).
2. Ouvre Wireshark, choisis ton interface active (Wi-Fi ou Ethernet), double-clique.
3. Navigue sur quelques sites pendant 30 secondes.
4. Arrête la capture (carré rouge) et enregistre-la : `capture1.pcapng`.

Observe : le nombre de paquets, la variété des protocoles dans la colonne *Protocol*.

### Exercice 2 — Maîtriser les filtres d'affichage

Sur `capture1.pcapng`, applique successivement : `dns`, `tcp.port == 443`, `arp`, `icmp`, `!(tcp || udp)`.

Pour chacun, note :
1. combien de paquets s'affichent (barre d'état) ;
2. une information intéressante (un nom de domaine, une adresse).

### Exercice 3 — Analyser DNS

1. Filtre : `dns`.
2. Vide ton cache DNS (`sudo resolvectl flush-caches` sous Linux, `ipconfig /flushdns` sous Windows).
3. Lance une nouvelle capture, puis ouvre un site ou tape `nslookup example.com`.
4. Relève la requête et la réponse : nom demandé, type, adresses retournées, TTL.

Question guidée : que peut déduire de ta navigation quelqu'un qui verrait tes requêtes DNS en clair ? (La liste des sites que tu visites.)

### Exercice 4 — Voir un mot de passe circuler en clair... dans ton laboratoire

Pour comprendre **pourquoi les protocoles chiffrés sont indispensables**, utilise **ta VM** :

1. Dans la VM, lance un serveur HTTP simple avec un formulaire de test :

```bash
mkdir -p ~/formtest && cd ~/formtest
cat > index.html << 'EOF'
<form method="POST" action="/">
  Utilisateur <input name="user"><br>
  Mot de passe <input name="pass" type="password"><br>
  <button>Envoyer</button>
</form>
EOF
python3 -m http.server 8000
```

2. Sur ta machine, ouvre `http://<ip-vm>:8000`, remplis avec des **identifiants fictifs** (ex. `demo` / `motdepasse-test`).
3. Capture avec le filtre `http.request.method == "POST"` ou `tcp.port == 8000`.
4. Clique droit → *Suivre → Flux TCP*.

Résultat : le serveur Python simple répond « 501 Unsupported method », mais **la requête POST avec les champs est bien visible en clair dans la capture**. Conclusion : sans HTTPS, un identifiant saisi dans un formulaire est lisible par quiconque capture le trafic.

### Exercice 5 — Comparer avec HTTPS

Capture la visite d'un site HTTPS. Filtre : `tls`. Repère :
1. le *Client Hello* et le champ **Server Name** (SNI) ;
2. le certificat du serveur dans le *Server Hello / Certificate* ;
3. les paquets *Application Data*, dont le contenu est illisible.

### Exercice 6 — Ligne de commande

```bash
sudo tcpdump -i any -n -c 20 port 53 -w dns.pcap
nslookup example.com            # dans un autre terminal
sudo tcpdump -r dns.pcap -n
tshark -r dns.pcap -Y "dns.flags.response == 1" -T fields -e dns.qry.name -e dns.a
```

### Exercice 7 — Détecter un scan de ports (dans ton labo)

1. Dans ta VM, installe nmap (voir leçon 16) ou utilise une seconde VM.
2. Lance une capture sur la VM cible, puis un scan **depuis ta propre machine vers ta propre VM** : `nmap -sS <ip-vm>`.
3. Dans Wireshark, filtre : `tcp.flags.syn == 1 && tcp.flags.ack == 0`.
4. Ouvre *Statistiques → Conversations → TCP* : une même IP source ouvre des connexions vers de nombreux ports de destination.
5. Repère les réponses `RST, ACK` des ports fermés.

Tu viens de voir un scan **depuis le point de vue du défenseur**.

### Exercice 8 — Défi : analyser une capture publique d'entraînement

Télécharge une capture d'entraînement sur un site de formation reconnu (par exemple les exercices de *Malware Traffic Analysis* ou les captures d'exemple du wiki Wireshark) et réponds :
1. Combien d'adresses IP distinctes ? (*Statistiques → Endpoints*)
2. Quel protocole domine ? (*Hiérarchie des protocoles*)
3. Y a-t-il des identifiants en clair ?
4. Quelle machine semble se comporter de façon inhabituelle ?

Rédige 5 lignes de conclusion avec **numéros de paquets** à l'appui.

## 🔍 Approfondissement

### Pour aller plus loin

- La documentation officielle : *Wireshark User's Guide* et le wiki (captures d'exemple).
- Le module « Wireshark: The Basics » et « Wireshark: Packet Operations » de TryHackMe.
- Le site *malware-traffic-analysis.net* (exercices PCAP) pour s'entraîner à l'analyse d'incidents.

### Pièges courants

- ❌ **Erreur fréquente 1** : confondre filtre de capture et filtre d'affichage, et se demander pourquoi `tcp.port == 80` ne marche pas comme filtre de capture.
- ✅ **Bonne pratique** : capture = syntaxe BPF (`tcp port 80`), affichage = syntaxe Wireshark (`tcp.port == 80`).
- ❌ **Erreur fréquente 2** : lancer une capture sans filtre pendant des heures et saturer le disque.
- ✅ **Bonne pratique** : limiter par taille ou par durée (`-c`, `-G`, option « Fichiers multiples »), utiliser un filtre de capture.
- ❌ **Erreur fréquente 3** : conclure à une attaque à partir d'un seul paquet inhabituel.
- ✅ **Bonne pratique** : confirmer une hypothèse avec plusieurs indices (temps, volume, destinations).
- ❌ **Erreur fréquente 4** : partager un fichier PCAP brut contenant des identifiants ou des données de tiers.
- ✅ **Bonne pratique** : anonymiser, minimiser, chiffrer les captures stockées.

## 🧪 Quiz de validation

**Question 1 : Quelle est la différence entre un filtre de capture et un filtre d'affichage ?**
- A) Il n'y en a pas
- B) Le filtre de capture limite ce qui est enregistré, le filtre d'affichage trie ce qui est déjà capturé ✅
- C) Le filtre d'affichage chiffre le trafic
- D) Le filtre de capture ne fonctionne que sous Windows

*Explication : le filtre de capture (BPF) agit avant l'enregistrement ; le filtre d'affichage agit après, sur les paquets déjà capturés.*

**Question 2 : Quel filtre d'affichage montre uniquement le trafic DNS ?**
- A) `dns` ✅
- B) `show dns`
- C) `port == dns`
- D) `tcp.dns`

*Explication : `dns` suffit à sélectionner les paquets décodés comme DNS.*

**Question 3 : À quoi sert « Suivre le flux TCP » ?**
- A) À bloquer une connexion
- B) À reconstituer et lire une conversation complète entre un client et un serveur ✅
- C) À chiffrer la capture
- D) À changer l'adresse IP

*Explication : Wireshark réassemble les paquets du flux dans l'ordre, côté client et côté serveur.*

**Question 4 : Pourquoi ne voit-on pas le contenu d'une page en HTTPS dans Wireshark ?**
- A) Parce que Wireshark est limité
- B) Parce que le contenu est chiffré par TLS ✅
- C) Parce que HTTPS n'utilise pas TCP
- D) Parce que la capture est trop lente

*Explication : seule la poignée de main et certaines métadonnées (comme le SNI) restent visibles.*

**Question 5 : Quel comportement dans une capture évoque un scan de ports ?**
- A) Un seul long téléchargement
- B) Une même IP envoyant des SYN vers de nombreux ports de destination, avec beaucoup de RST en retour ✅
- C) Des requêtes DNS vers un seul domaine
- D) Des paquets ARP normaux

*Explication : un scan teste de nombreux ports en peu de temps ; les ports fermés répondent par RST.*

## 📝 Résumé

- Wireshark capture et décode le trafic réseau couche par couche ; `tcpdump` et `tshark` le font en ligne de commande.
- Les filtres de capture (BPF) limitent l'enregistrement ; les filtres d'affichage (`ip.addr`, `tcp.port`, `dns`, `http`…) servent à l'analyse.
- *Suivre le flux TCP*, *Conversations* et *Hiérarchie des protocoles* sont les fonctions d'analyse les plus utiles.
- Les protocoles en clair (HTTP, FTP, Telnet) exposent les données ; TLS laisse visibles seulement certaines métadonnées.
- Une analyse sérieuse suit : hypothèse, filtre, preuve, documentation.
- La capture doit se limiter à ton propre réseau ou à un périmètre autorisé, et les fichiers PCAP se protègent comme des données sensibles.

## 🎓 Ce que tu as appris

✅ Capturer du trafic de façon légale et maîtrisée
✅ Utiliser les filtres de capture et d'affichage
✅ Analyser ARP, DNS, TCP, HTTP et TLS
✅ Repérer scans, protocoles non chiffrés et comportements anormaux

## ➡️ Leçon suivante

**16 : Scan réseau avec Nmap** : découverte d'hôtes, scan de ports, détection de services, scripts, et bonnes pratiques de scan autorisé. Fichier : `16-nmap-scan.md`.

---

© 2026 ECHATS PRO — Tous droits réservés
