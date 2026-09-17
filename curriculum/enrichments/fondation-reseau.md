## Enrichissement pédagogique — guide opératoire

### Positionnement
Cette leçon ouvre le parcours vers la cyberdéfense opérationnelle de niveau institutionnel. Elle ne constitue pas une accréditation officielle; elle installe les fondations nécessaires à l’administration système, au développement sécurisé, à l’investigation et à la détection.

### Objectifs observables
À la fin de la séance, l’apprenant sait expliquer les couches OSI et leur relation avec TCP/IP, distinguer TCP et UDP, interpréter une adresse IPv4 et une notation CIDR, relier IP, port et service, expliquer DNS et ARP, puis rédiger une note séparant observation, hypothèse et preuve.

### Prérequis
Aucun prérequis technique formel. Toute manipulation reste limitée au propre appareil, à un laboratoire local ou à un système explicitement autorisé.

### Checkpoints
Après OSI, explique pourquoi HTTPS mobilise plusieurs couches. Après TCP/UDP, choisis le protocole adapté à trois scénarios. Après l’adressage, calcule `/24` et `/30` et explique le cas `/32`. Après DNS/ARP, distingue résolution de nom, association locale et routage.

### Pratique guidée
Sur un environnement autorisé, observe `ip addr`, `ip route`, `ip neigh`, `ss -tuln` et `getent hosts example.com`. Pour chaque observation, consigne la commande, le résultat utile, l’interprétation, la limite et le test de confirmation.

### Challenge légal et éthique
À partir d’une sortie réseau fournie par l’enseignant, rédige une note d’une page avec périmètre, actifs, protocoles, preuves, hypothèses, limites et trois recommandations défensives priorisées. Aucun scan de tiers n’est demandé.

### Précisions et erreurs fréquentes
ARP est généralement rattaché à la liaison de données tout en faisant le lien avec l’adressage réseau. DNS utilise souvent UDP mais peut utiliser TCP selon le contexte. Un port ouvert est un indice de surface exposée, pas une vulnérabilité confirmée. Une route `/32` ne doit pas être décrite comme un sous-réseau classique sans préciser le contexte.

### Synthèse opérationnelle
L’analyste relie couche, protocole, adresse, port, service, observation et preuve. Il distingue toujours ce qui est connu de ce qui est supposé et de ce qui reste à vérifier.
