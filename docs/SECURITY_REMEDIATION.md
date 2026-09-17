# ECHATS PRO Backend — Rapport de remédiation sécurité

Date de l'audit : 13 août 2026.

## Périmètre

La remédiation couvre l'authentification interne, les refresh tokens, le 2FA/TOTP, les endpoints Labs REST, le terminal WebSocket Labs, le RBAC live et l'isolation institutionnelle. Le code conserve FastAPI, PostgreSQL/SQLAlchemy, Redis et Firebase Admin SDK.

## Fichiers modifiés

| Fichier | Modification |
|---|---|
| `app/api/v1/labs.py` | Authentification obligatoire sur start/stop/reset/status/destroy et endpoint de ticket WebSocket. |
| `app/modules/labs/service.py` | Contrôle centralisé d'ownership, tickets opaques à usage unique, expiration 60 secondes, validation d'état. |
| `app/modules/labs/schemas.py` | Schéma `LabWebSocketTicketOut`. |
| `app/websocket/terminal.py` | Suppression du JWT accepté en query string ; consommation du ticket lié au lab et à l'utilisateur. |
| `app/models/refresh_session.py` | Nouveau modèle de session refresh avec hash, expiration, révocation, rotation et métadonnées. |
| `app/models/__init__.py` | Enregistrement du nouveau modèle SQLAlchemy. |
| `alembic/versions/0002_refresh_sessions.py` | Migration PostgreSQL de la table `refresh_sessions`. |
| `app/security/jwt.py` | Claim `sid` et hash SHA-256 du refresh token. |
| `app/modules/auth/session_repository.py` | Persistance, verrouillage, révocation individuelle et révocation globale. |
| `app/modules/auth/service.py` | Création de session, rotation atomique, détection de réutilisation, révocation et rate limit 2FA. |
| `app/api/v1/auth.py` | Rotation du refresh token, retour du nouveau token et logout avec révocation optionnelle. |
| `app/security/totp.py` | Code TOTP à usage unique via Redis `SET NX`. |
| `app/core/settings.py` | Paramètres 2FA et validation stricte des secrets en production. |
| `app/modules/users/service.py` | Rate limit 2FA compte/IP, anti-réutilisation à l'activation, révocation des sessions à la désactivation. |
| `app/api/v1/users.py` | Injection Redis/IP dans l'activation 2FA. |
| `app/dependencies/permissions.py` | Permissions rechargées depuis PostgreSQL au lieu de dépendre uniquement du JWT. |
| `app/dependencies/roles.py` | Rôles rechargés depuis PostgreSQL. |
| `app/api/v1/organizations.py` et `app/modules/organizations/service.py` | Lecture d'une institution limitée à un admin ou au même tenant. |
| `app/api/v1/writeups.py` | Décision de modération basée sur le rôle PostgreSQL live. |
| `app/api/v1/forum.py` | Décision de modération basée sur le rôle PostgreSQL live. |
| `app/api/v1/orders.py` | Décision d'accès administrateur basée sur le rôle PostgreSQL live. |
| `tests/conftest.py` | Faux Redis étendu avec `SET NX` et `GETDEL`. |
| `tests/security/test_labs_security.py` | Tests ownership REST, tickets, replay, rebinding et non-authentification HTTP. |
| `tests/security/test_auth_security.py` | Tests TOTP single-use, rotation, expiration et replay refresh. |
| `README.md` | Documentation mise à jour. |
| `.env.example` | Variables 2FA documentées. |

## Vulnérabilités corrigées

### Labs REST

Les routes `POST /api/v1/labs/start`, `POST /api/v1/labs/stop`, `POST /api/v1/labs/reset` et `GET /api/v1/labs/status` exigent désormais un token valide. Le serveur récupère la session depuis Redis et vérifie que `session.user_id == current_user.id` avant toute opération. Un utilisateur authentifié mais non propriétaire reçoit un refus `403`; une session absente reçoit `404`.

Le même contrôle est appliqué à `destroy` et à la création d'un ticket WebSocket.

### WebSocket Labs

Le JWT n'est plus accepté directement dans l'URL. Le client doit appeler `POST /api/v1/labs/{lab_id}/ws-ticket`, puis ouvrir `/ws/labs?ticket=...`. Le ticket est aléatoire, opaque, haché avant stockage Redis, lié au couple utilisateur/lab, valable 60 secondes et consommé atomiquement avec `GETDEL`. Un replay ou un ticket modifié est refusé. L'état et l'ownership du lab sont revalidés avant ouverture du terminal.

### Refresh tokens

Chaque refresh token possède un `sid` et une ligne `refresh_sessions` en base. Seul le hash du token est stocké. Le refresh effectue une rotation : l'ancien token est immédiatement révoqué et un nouveau refresh token est retourné. La réutilisation d'un token déjà révoqué déclenche la révocation de toutes les sessions de l'utilisateur. Le logout peut révoquer individuellement le refresh token fourni.

### 2FA

Le flux `/auth/2fa/verify` est limité par compte et par IP. Les codes TOTP acceptés sont enregistrés en Redis par compteur et ne peuvent pas être réutilisés pendant leur période de validité. L'activation 2FA applique le même mécanisme. La désactivation révoque les sessions existantes.

### RBAC et multi-tenant

Les contrôles `require_permission` et `require_role` rechargent maintenant le compte, le rôle et les permissions depuis PostgreSQL. Les décisions de modération sur writeups/forum et les décisions administrateur sur les commandes ne dépendent plus uniquement d'anciens claims JWT. La lecture d'une institution est limitée à l'admin ou au tenant correspondant.

### Secrets et logs

En production, l'application refuse de démarrer si les secrets JWT, la clé Chambre Close, la signature certificats ou l'URL PostgreSQL sont absents. Les secrets de signature sont contrôlés en longueur minimale et `DEBUG=true` est interdit. La revue statique des logs n'a trouvé aucun logger qui écrit un JWT, refresh token, ticket complet, mot de passe, clé API ou secret Firebase.

## Vérifications réalisées

- Compilation Python de tous les fichiers : **OK**.
- Tests unitaires et sécurité : **51 passed**.
- Smoke test FastAPI : santé HTTP `200`, routes Labs présentes dans OpenAPI, routes Labs sensibles sans authentification : `401`, ticket WebSocket invalide : fermeture `4401`.
- Le smoke test a signalé que Redis n'est pas démarré dans l'environnement de validation local. Le code continue à démarrer en mode best-effort, mais la rotation, le rate limiting, les tickets et le 2FA doivent être validés avec un Redis réel en staging.
- PostgreSQL, Firebase Admin, Judge0, GitHub Codespaces et les fournisseurs de paiement n'ont pas été exercés avec des identifiants de production.

## Migration et déploiement

La migration `0002_refresh_sessions` est appliquée automatiquement par la commande Render déjà présente :

```bash
alembic upgrade head
```

Pour un démarrage local :

```bash
cp .env.example .env
# renseigner DATABASE_URL, REDIS_URL, JWT_SECRET, JWT_REFRESH_SECRET,
# FIREBASE_CREDENTIALS_JSON et les intégrations nécessaires
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

Redis **6.2 ou supérieur** est requis pour garantir l'opération atomique `GETDEL` des tickets WebSocket. Les nouvelles variables optionnelles sont `RATE_LIMIT_2FA_PER_MINUTE` et `TOTP_USED_TTL_SECONDS`; leurs valeurs par défaut sont respectivement `5` et `120`.

## Conclusion

Les endpoints Labs sont désormais protégés contre l'accès horizontal. Le WebSocket vérifie l'ownership et l'état du lab avant d'ouvrir le terminal. Les refresh tokens sont persistés sous forme de hash, rotatifs et révocables. Les secrets ne sont pas exposés dans les logs. Une validation finale en staging avec PostgreSQL, Redis et Firebase réels reste obligatoire avant mise en production.
