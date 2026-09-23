import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    max_memory_buffer_size_mb: float
    fallback_decryption_password: Optional[str]


def load_config() -> Config:
    """Load ingestor configuration from environment variables (see .env)."""
    raw_max_mb = os.getenv("MAX_MEMORY_BUFFER_SIZE_MB", "50")
    try:
        max_mb = float(raw_max_mb)
    except ValueError as exc:
        raise ValueError(
            f"MAX_MEMORY_BUFFER_SIZE_MB must be a number, got: {raw_max_mb!r}"
        ) from exc
    if max_mb <= 0:
        raise ValueError("MAX_MEMORY_BUFFER_SIZE_MB must be greater than 0")

    fallback_password = os.getenv("FALLBACK_DECRYPTION_PASSWORD") or None

    return Config(
        max_memory_buffer_size_mb=max_mb,
        fallback_decryption_password=fallback_password,
    )
