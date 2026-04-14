from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


def _config_toml() -> str | None:
    for parent in Path(__file__).parents:
        if (parent / "pyproject.toml").exists():
            return str(parent / "config.toml")
    return None


class ManagerConfig(BaseModel):
    address: str
    heartbeat_interval_s: int


class ServiceConfig(BaseModel):
    name: str
    description: str
    host: str
    port: int


class H2PConfig(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file=_config_toml(),
        env_nested_delimiter="__",
    )
    manager: ManagerConfig
    service: ServiceConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (env_settings, TomlConfigSettingsSource(settings_cls))
