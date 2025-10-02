from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings are loaded from environment variables.
    Pydantic v2's BaseSettings handles the loading and validation.
    """

    APP_NAME: str = "EML Parser API"
    APP_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"

    # Telemetry Settings
    OTEL_SERVICE_NAME: str = "eml-parser-api"
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://otel-collector:4317"

    # Ollama Settings
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "llama3"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Instantiate the settings
settings = Settings()

