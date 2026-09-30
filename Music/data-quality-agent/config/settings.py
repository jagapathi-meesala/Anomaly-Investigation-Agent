"""Environment-backed runtime configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigurationError(ValueError):
    pass


def _required(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise ConfigurationError(f"Required environment variable {name} is not set")
    return value.strip()


@dataclass(frozen=True)
class Settings:
    environment: str
    log_level: str
    max_records: int

    @classmethod
    def from_environment(cls) -> "Settings":
        try:
            max_records = int(_required("DATA_QUALITY_MAX_RECORDS"))
        except ValueError as exc:
            raise ConfigurationError("DATA_QUALITY_MAX_RECORDS must be an integer") from exc
        if max_records <= 0:
            raise ConfigurationError("DATA_QUALITY_MAX_RECORDS must be positive")
        return cls(
            environment=_required("DATA_QUALITY_ENVIRONMENT"),
            log_level=_required("DATA_QUALITY_LOG_LEVEL"),
            max_records=max_records,
        )
