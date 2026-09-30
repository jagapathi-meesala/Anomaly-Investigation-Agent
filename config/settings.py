"""Environment-backed runtime settings with strict validation."""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass


class ConfigurationError(ValueError):
    """Raised when runtime configuration is invalid."""


def _env_str(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ConfigurationError(f"{name} must be set")
    return value


def _env_int(name: str, minimum: int) -> int:
    raw = os.getenv(name, "")
    if not raw:
        raise ConfigurationError(f"{name} must be set")
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer") from exc
    if value < minimum:
        raise ConfigurationError(f"{name} must be >= {minimum}")
    return value


def _env_float(name: str, minimum: float, maximum: float | None = None) -> float:
    raw = os.getenv(name, "")
    if not raw:
        raise ConfigurationError(f"{name} must be set")
    try:
        value = float(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be a number") from exc
    if value < minimum or (maximum is not None and value > maximum):
        bound = f"between {minimum} and {maximum}" if maximum is not None else f">= {minimum}"
        raise ConfigurationError(f"{name} must be {bound}")
    return value


@dataclass(frozen=True)
class Settings:
    log_level: str
    max_rows: int
    z_score_threshold: float
    iqr_multiplier: float
    max_candidates: int

    def configure_logging(self) -> None:
        logging.basicConfig(level=getattr(logging, self.log_level, logging.INFO))


def load_settings() -> Settings:
    level = _env_str("AGENT_LOG_LEVEL").upper()
    if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ConfigurationError("AGENT_LOG_LEVEL must be a standard logging level")
    return Settings(
        log_level=level,
        max_rows=_env_int("AGENT_MAX_ROWS", 1),
        z_score_threshold=_env_float("AGENT_Z_SCORE_THRESHOLD", 0.1),
        iqr_multiplier=_env_float("AGENT_IQR_MULTIPLIER", 0.1),
        max_candidates=_env_int("AGENT_MAX_CANDIDATES", 1),
    )
