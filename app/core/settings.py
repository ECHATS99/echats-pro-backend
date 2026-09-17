"""Configuration Pydantic Settings : lit toutes les variables d'environnement (voir .env.example).
Source unique de vérité pour la config. Aucune valeur sensible en dur dans le code.
"""
from functools import lru_cache
from typing import ClassVar, List

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App ---
    APP_NAME: str = "ECHATS PRO Backend"
    APP_ENV: str = Field(default="development")  # development | staging | production
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # --- CORS ---
    DEFAULT_CORS_ORIGINS: ClassVar[list[str]] = [
        "https://echatspro.web.app",
        "https://echats-808c4.web.app",
        "https://echatpro-xnrzv8cz.manus.space",
    ]
    CORS_ALLOWED_ORIGINS: List[str] | str = DEFAULT_CORS_ORIGINS
    # Origines locales injectées uniquement dans l'environnement de développement.
    # Elles ne sont jamais ajoutées à la whitelist de production.
    CORS_DEV_ORIGINS: List[str] | str = []
    CORS_TEMPORARY_ORIGINS: List[str] | str = []
    ENABLE_TEMPORARY_CORS: bool = False
    PRODUCTION_CORS_ORIGINS: ClassVar[list[str]] = [
        "https://echats-808c4.web.app",
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_cors_origins(cls, values: dict) -> dict:
        import json

        def parse_origins(raw: object) -> list[str]:
            if isinstance(raw, list):
                return [str(origin).strip() for origin in raw if str(origin).strip()]
            if isinstance(raw, str):
                try:
                    decoded = json.loads(raw)
                    if isinstance(decoded, list):
                        return [str(origin).strip() for origin in decoded if str(origin).strip()]
                except (TypeError, ValueError):
                    pass
                return [origin.strip() for origin in raw.split(",") if origin.strip()]
            return []

        app_env = str(values.get("APP_ENV", "development")).strip().lower()
        configured_origins = parse_origins(values.get("CORS_ALLOWED_ORIGINS"))
        if not configured_origins:
            configured_origins = list(cls.DEFAULT_CORS_ORIGINS)

        temporary_enabled = str(values.get("ENABLE_TEMPORARY_CORS", "false")).strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

        if app_env == "production":
            # Production reste limitée au domaine Firebase officiel par défaut.
            # Un élargissement temporaire nécessite deux variables explicites,
            # activées uniquement pendant un test contrôlé puis supprimées.
            production_origins = list(cls.PRODUCTION_CORS_ORIGINS)
            if temporary_enabled:
                production_origins = list(
                    dict.fromkeys(
                        production_origins + parse_origins(values.get("CORS_TEMPORARY_ORIGINS"))
                    )
                )
            values["CORS_ALLOWED_ORIGINS"] = production_origins
        else:
            dev_origins = parse_origins(values.get("CORS_DEV_ORIGINS"))
            values["CORS_ALLOWED_ORIGINS"] = list(
                dict.fromkeys(configured_origins + dev_origins)
            )

        # Gate explicite pour un test temporaire contrôlé. Il reste désactivé
        # par défaut et ne peut élargir la whitelist que si les deux variables
        # d'environnement sont fournies volontairement.
        if app_env != "production" and temporary_enabled:
            values["CORS_ALLOWED_ORIGINS"] = list(
                dict.fromkeys(
                    parse_origins(values.get("CORS_ALLOWED_ORIGINS"))
                    + parse_origins(values.get("CORS_TEMPORARY_ORIGINS"))
                )
            )
        return values

    # --- Database ---
    DATABASE_URL: str = ""
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- Firebase ---
    FIREBASE_CREDENTIALS_JSON: str = ""

    # --- ECHATS IA (api.echats.ai) ---
    ECHATS_AI_BACKEND_URL: str = "https://blackhawk-ai-core.onrender.com"
    ECHATS_AI_API_KEY: str = ""

    # --- Cloudinary ---
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # --- Paiements ---
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    PAYPAL_CLIENT_ID: str = ""
    PAYPAL_CLIENT_SECRET: str = ""
    MOBILE_MONEY_API_KEY: str = ""
    PARABEN_REVENUE_ACCOUNT: str = ""

    # --- Email ---
    SENDGRID_API_KEY: str = ""
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "no-reply@echatspro.com"

    # --- Labs ---
    JUDGE0_API_URL: str = ""
    GITHUB_TOKEN: str = ""

    # --- JWT interne ---
    JWT_SECRET: str = ""
    JWT_REFRESH_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # --- Rate limiting (valeurs par défaut, voir Partie 4.17 du SRS) ---
    RATE_LIMIT_LOGIN_PER_MINUTE: int = 5
    RATE_LIMIT_UPLOAD_PER_DAY: int = 50
    RATE_LIMIT_PAYMENT_PER_HOUR: int = 20
    RATE_LIMIT_SEARCH_PER_MINUTE: int = 200
    RATE_LIMIT_CTF_CREATE_PER_HOUR: int = 10
    RATE_LIMIT_FLAG_ATTEMPTS_PER_HOUR: int = 10
    RATE_LIMIT_2FA_PER_MINUTE: int = 5
    TOTP_USED_TTL_SECONDS: int = 120

    # --- 2FA ---
    TOTP_ISSUER_NAME: str = "ECHATS PRO"

    # --- Chambre Close : clé de chiffrement dédiée (Fernet, 32 bytes urlsafe base64) ---
    CHAMBER_CLOSE_ENCRYPTION_KEY: str = ""

    # --- Certificats : clé de signature HMAC (vérification d'authenticité publique) ---
    CERTIFICATE_SIGNING_SECRET: str = ""

    @model_validator(mode="after")
    def validate_production_security(self):
        if self.APP_ENV == "production":
            required = {
                "DATABASE_URL": self.DATABASE_URL,
                "JWT_SECRET": self.JWT_SECRET,
                "JWT_REFRESH_SECRET": self.JWT_REFRESH_SECRET,
                "CHAMBER_CLOSE_ENCRYPTION_KEY": self.CHAMBER_CLOSE_ENCRYPTION_KEY,
                "CERTIFICATE_SIGNING_SECRET": self.CERTIFICATE_SIGNING_SECRET,
            }
            missing = [name for name, value in required.items() if not value]
            if missing:
                raise ValueError(
                    "Configuration production incomplète : secrets obligatoires absents "
                    + ", ".join(missing)
                )
            weak = [name for name, value in required.items() if name.endswith("SECRET") and len(value) < 32]
            if weak:
                raise ValueError("Secrets de production trop courts : " + ", ".join(weak))
            if self.DEBUG:
                raise ValueError("DEBUG doit être false en production.")
        return self


@lru_cache
def get_settings() -> Settings:
    """Retourne l'instance unique (mise en cache) des settings."""
    return Settings()


settings = get_settings()
