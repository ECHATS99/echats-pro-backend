# Curriculum cybersécurité — import manuel

Ce dossier contient les **11 sources `.txt`**, les enrichissements pédagogiques séparés, les quiz privés et le manifeste canonique destinés à un import ponctuel dans PostgreSQL.

## Garanties

Le texte des sources est conservé sans réécriture silencieuse. Le manifeste contient un SHA-256 pour chaque fichier. L’importateur concatène l’enrichissement identifiable et le bloc source original dans `Lesson.content`. Les bonnes réponses des quiz restent dans les fichiers privés et dans `Answer.correct` côté serveur; elles ne doivent jamais être exposées au frontend.

Le contenu est publié en statut `draft` par défaut. Les préambules conversationnels sont signalés dans le dry-run. Les leçons de pentest, OSINT, sécurité web, malware et Red Team restent limitées à des environnements possédés ou explicitement autorisés.

## Dry-run obligatoire

Depuis la racine du backend :

```bash
python3 scripts/import_lessons_to_postgres.py \
  --manifest curriculum/curriculum_manifest.json \
  --source-dir curriculum \
  --dry-run
```

Le mode par défaut est également `dry-run`; cette commande ne crée ni track, ni module, ni leçon, ni quiz.

## Import réel, après validation

L’import réel doit être lancé manuellement dans un environnement local disposant d’un `DATABASE_URL` PostgreSQL valide :

```bash
python3 scripts/import_lessons_to_postgres.py \
  --manifest curriculum/curriculum_manifest.json \
  --source-dir curriculum \
  --apply
```

Le script vérifie les collisions par parent, ordre et titre, refuse de remplacer un contenu existant dont le checksum diffère et exécute les écritures dans une transaction unique. Il est donc préférable de conserver la sortie JSON du dry-run avant de lancer `--apply`.

## Vérifications post-import

Après un `--apply` réussi, vérifier l’API réelle avec un token utilisateur approprié :

```text
GET https://echats-pro-backend.onrender.com/api/v1/tracks
GET https://echats-pro-backend.onrender.com/api/v1/modules/by-track/{track_id}
GET https://echats-pro-backend.onrender.com/api/v1/lessons/by-module/{module_id}
GET https://echats-pro-backend.onrender.com/api/v1/quizzes/by-lesson/{lesson_id}
```

Les réponses publiques du quiz doivent contenir les questions et choix, mais aucun champ `correct`. La soumission doit passer par `POST /api/v1/quizzes/{quiz_id}/submit`; la correction et le score restent côté backend.

## Données sensibles

Ne jamais committer `DATABASE_URL`, des credentials Firebase Admin, des tokens, des mots de passe ou des fichiers de service. Les fichiers `quizzes-private` contiennent volontairement les corrections et doivent rester accessibles uniquement au dépôt ou à l’environnement backend de confiance.
