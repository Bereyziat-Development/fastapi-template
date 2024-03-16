import secrets
from enum import Enum
from typing import List, Optional, Union

from pydantic import (
    AnyHttpUrl,
    EmailStr,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(str, Enum):
    DEV = "dev"
    STAG = "staging"
    PROD = "prod"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # By default: 60 seconds * 60 minutes * 24 hours * 1 days = 1 days
    ACCESS_TOKEN_EXPIRES_SECONDS: int = 60 * 60 * 24 * 1
    # By default: 60 seconds * 60 minutes * 24 hours * 365 days = 1 year
    REFRESH_TOKEN_EXPIRES_SECONDS: int = 60 * 60 * 24 * 8
    # By default: 30 seconds
    SSO_CONFIRMATION_TOKEN_EXPIRES_SECONDS: int = 30
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", ...]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ENV_CONFIG: EnvConfig = EnvConfig.DEV

    PROJECT_NAME: str
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "app"
    SQLALCHEMY_DATABASE_URI: str = ""
    SMTP_TLS: bool = False
    SMTP_SSL: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    WEB_APP_URL: Optional[str] = None

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email_service/templates/build"
    EMAILS_ENABLED: bool = False

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_SSO_ENABLED: bool = False

    FACEBOOK_CLIENT_ID: Optional[str] = None
    FACEBOOK_CLIENT_SECRET: Optional[str] = None
    FACEBOOK_SSO_ENABLED: bool = False

    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GITHUB_SSO_ENABLED: bool = False

    FILE_PATH: str = "/app/app/files/"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(
        cls, v: Union[str, List[str]], info: ValidationInfo
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @model_validator(mode="after")
    def set_email_service(self) -> "Settings":
        if self.EMAILS_FROM_EMAIL is None:
            self.EMAILS_FROM_EMAIL = self.PROJECT_NAME
        # Enable emails sending if all the information is provided.
        self.EMAILS_ENABLED = bool(
            self.SMTP_HOST and self.SMTP_PORT and self.EMAILS_FROM_EMAIL
        )
        return self

    @model_validator(mode="after")
    def set_sso_services(self) -> "Settings":
        # Enable Google SSO if all the information is provided.
        self.GOOGLE_SSO_ENABLED = bool(
            self.GOOGLE_CLIENT_ID and self.GOOGLE_CLIENT_SECRET
        )
        # Enable Facebook SSO if all the information is provided.
        self.FACEBOOK_SSO_ENABLED = bool(
            self.FACEBOOK_CLIENT_ID and self.FACEBOOK_CLIENT_SECRET
        )

        # Enable GitHub SSO if all the information is provided.
        self.GITHUB_SSO_ENABLED = bool(
            self.GITHUB_CLIENT_ID and self.GITHUB_CLIENT_SECRET
        )
        return self

    @model_validator(mode="after")
    def set_db_url(self) -> "Settings":
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        server = self.POSTGRES_SERVER
        db = self.POSTGRES_DB
        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{server}/{db}"
        return self


settings = Settings()
