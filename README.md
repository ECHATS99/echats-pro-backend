# ECHATS PRO — Backend

Squelette généré automatiquement. Voir chaque fichier pour sa responsabilité exacte (commentaire en tête de fichier).

## État d'implémentation — Phase 1 (livrée)

Implémenté avec du vrai code (aucun mock) :

- `core/` : settings, database, redis, exceptions, logging, constants
- `security/` : jwt, rbac, hash (flags SHA256+sel), totp (2FA), rate_limit, csrf, headers, encryption, validator
- `dependencies/` + `middlewares/`
- Modèles SQLAlchemy : `User`, `Role`/`Permission` (RBAC dynamique), `Plan`, `Subscription`, `Institution`, `AuditLog`
- Intégration Firebase (`integrations/firebase/`) : vérification du token uniquement
- Domaine `auth` complet : login Firebase → auto-provisioning → JWT interne, 2FA obligatoire pour les rôles sensibles, sessions refresh persistantes, rotation et révocation serveur
- Domaine `users` complet : profil, mise à jour, statistiques (partielles, voir note plus bas), recherche paginée
- `app/main.py`, `app/lifespan.py`, `api/v1/router.py`, `api/v1/health.py`, `api/v1/auth.py`, `api/v1/users.py`
- Migrations Alembic : `0001_phase1_core_auth.py` et `0002_refresh_sessions.py`
- `scripts/seed.py` (rôles/permissions/plans de base) et `scripts/create_admin.py`

## Limites connues de cette Phase 1 (transparence)

- **Validation locale effectuée** : vérification syntaxique complète, 51 tests unitaires/sécurité et smoke test FastAPI. Les tests nécessitant une instance PostgreSQL/Redis/Firebase réelles restent à exécuter en staging.
- `modules/users/service.get_statistics` dépend des tables de progression, CTF, certificats et badges présentes dans la base cible ; leur couverture d'intégration doit être validée avec les migrations métier complètes.
- `CHAMBER_CLOSE_ENCRYPTION_KEY` doit être générée manuellement (`Fernet.generate_key()`) et injectée en variable d'environnement — aucune valeur par défaut n'est fournie par sécurité.
- Les intégrations externes (Firebase, PostgreSQL, Redis, GitHub Codespaces, Judge0 et api.echats.ai) doivent être vérifiées dans un environnement de staging avant production.
- Les tickets WebSocket Labs nécessitent Redis 6.2+ pour garantir l'opération atomique `GETDEL`.
- Les secrets de production sont obligatoires et validés au démarrage lorsque `APP_ENV=production`.

## Démarrage (une fois `pip install -r requirements.txt` fait)

```bash
cp .env.example .env  # puis renseigner les variables
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```
