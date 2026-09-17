from app.core.settings import Settings


def build_settings(**overrides):
    values = {
        "APP_ENV": "development",
        "CORS_ALLOWED_ORIGINS": ["https://echats-808c4.web.app"],
        "CORS_DEV_ORIGINS": ["http://127.0.0.1:3002", "http://localhost:3002"],
        "CORS_TEMPORARY_ORIGINS": [],
        "ENABLE_TEMPORARY_CORS": False,
    }
    values.update(overrides)
    return Settings.model_validate(values)


def test_development_can_add_local_origins_from_environment():
    settings = build_settings()

    assert "http://127.0.0.1:3002" in settings.CORS_ALLOWED_ORIGINS
    assert "http://localhost:3002" in settings.CORS_ALLOWED_ORIGINS
    assert "https://echats-808c4.web.app" in settings.CORS_ALLOWED_ORIGINS


def test_production_ignores_local_origins_by_default():
    settings = build_settings(
        APP_ENV="production",
        CORS_ALLOWED_ORIGINS=[
            "https://echats-808c4.web.app",
            "http://127.0.0.1:3002",
            "http://localhost:3002",
        ],
        CORS_DEV_ORIGINS=["http://127.0.0.1:3002", "http://localhost:3002"],
        CORS_TEMPORARY_ORIGINS=["http://127.0.0.1:3002", "http://localhost:3002"],
        DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/echats_pro",
        JWT_SECRET="a" * 32,
        JWT_REFRESH_SECRET="b" * 32,
        CHAMBER_CLOSE_ENCRYPTION_KEY="c" * 32,
        CERTIFICATE_SIGNING_SECRET="d" * 32,
    )

    assert settings.CORS_ALLOWED_ORIGINS == ["https://echats-808c4.web.app"]


def test_production_can_enable_explicit_temporary_origins():
    settings = build_settings(
        APP_ENV="production",
        CORS_TEMPORARY_ORIGINS=["http://127.0.0.1:3002", "http://localhost:3002"],
        ENABLE_TEMPORARY_CORS=True,
        DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/echats_pro",
        JWT_SECRET="a" * 32,
        JWT_REFRESH_SECRET="b" * 32,
        CHAMBER_CLOSE_ENCRYPTION_KEY="c" * 32,
        CERTIFICATE_SIGNING_SECRET="d" * 32,
    )

    assert settings.CORS_ALLOWED_ORIGINS == [
        "https://echats-808c4.web.app",
        "http://127.0.0.1:3002",
        "http://localhost:3002",
    ]


def test_explicit_temporary_origins_work_when_environment_defaults_to_development():
    settings = build_settings(
        APP_ENV="development",
        CORS_DEV_ORIGINS=[],
        CORS_TEMPORARY_ORIGINS=["http://127.0.0.1:3002", "http://localhost:3002"],
        ENABLE_TEMPORARY_CORS=True,
    )

    assert settings.CORS_ALLOWED_ORIGINS == [
        "https://echats-808c4.web.app",
        "http://127.0.0.1:3002",
        "http://localhost:3002",
    ]
