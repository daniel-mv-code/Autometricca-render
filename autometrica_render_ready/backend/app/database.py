import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "AutoMétrica"
    SMTP_FROM_EMAIL: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    RESEND_API_KEY: str = ""
    RESEND_FROM: str = "AutoMétrica <onboarding@resend.dev>"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
environment = os.getenv("ENVIRONMENT", "development").lower()
database_url = settings.DATABASE_URL.strip()

# SQLite is permitted only for local development. Production must use Render PostgreSQL.
if not database_url:
    if environment == "production":
        raise RuntimeError("DATABASE_URL es obligatorio en producción; no se permite SQLite.")
    database_url = "sqlite:///./autometrica_db.db"

# Render may provide postgres://; SQLAlchemy expects postgresql://.
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

engine_options = {"pool_pre_ping": True}
if database_url.startswith("sqlite"):
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(database_url, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
