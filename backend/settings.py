"""
Centralized runtime settings for GOVERN.AI.

Reads environment variables once at import time and exposes a singleton
``settings`` object. Sovereign-mode flags can also be overridden at runtime
(in-memory) through ``settings.set_sovereign_mode(bool)`` — used by the
``/api/settings/ai-mode`` endpoint so admins can flip provider without restart.

The legacy logic in ``routes/chat.py`` continues to read ``os.environ`` directly
for backwards compatibility; the LLM helper below is the new single source of
truth and is wired into ARIA without altering prompts or scoring code.
"""
import os
import logging
from typing import Optional

logger = logging.getLogger("govern_ai.settings")


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if raw in ("1", "true", "yes", "on"):
        return True
    if raw in ("0", "false", "no", "off"):
        return False
    return default


class Settings:
    """Single source of truth for runtime configuration."""

    def __init__(self) -> None:
        # Existing (do not change semantics)
        self.openai_api_key: str = os.environ.get("OPENAI_API_KEY", "") or os.environ.get("EMERGENT_LLM_KEY", "")
        self.default_model: str = os.environ.get("LLM_MODEL", "openai/gpt-4o")

        # Sovereign — Apertus (Swiss AI Initiative)
        self._sovereign_enabled: bool = _env_bool("LLM_SOVEREIGN_ENABLED", False)
        self.sovereign_model: str = os.environ.get(
            "LLM_SOVEREIGN_MODEL", "publicai/swiss-ai/apertus-70b-instruct"
        )
        self.sovereign_base_url: str = os.environ.get(
            "LLM_SOVEREIGN_BASE_URL", "https://platform.publicai.co/v1"
        )
        self.publicai_api_key: str = os.environ.get("PUBLICAI_API_KEY", "")

        # Runtime override slot (set by /api/settings/ai-mode); None = follow env
        self._sovereign_runtime_override: Optional[bool] = None

    # ── Sovereign state ──────────────────────────────────────────────
    @property
    def sovereign_enabled(self) -> bool:
        """Effective state: runtime override wins over env."""
        if self._sovereign_runtime_override is not None:
            return self._sovereign_runtime_override
        return self._sovereign_enabled

    @property
    def sovereign_configured(self) -> bool:
        """True only when the sovereign provider has a usable API key."""
        return bool(self.publicai_api_key) and self.publicai_api_key != "your_publicai_api_key_here"

    def set_sovereign_mode(self, enabled: bool) -> None:
        """In-memory toggle used by the admin API. Does not persist to disk."""
        self._sovereign_runtime_override = bool(enabled)
        logger.info("Sovereign mode runtime override set to %s", self._sovereign_runtime_override)

    # ── LLM routing ──────────────────────────────────────────────────
    def get_llm_model(self) -> dict:
        """
        Return the LLM call kwargs to use right now.

        Falls back to GPT-4o when sovereign is disabled OR not properly configured.
        """
        if self.sovereign_enabled and self.sovereign_configured:
            return {
                "provider": "sovereign",
                "model": self.sovereign_model,
                "api_base": self.sovereign_base_url,
                "api_key": self.publicai_api_key,
            }
        return {
            "provider": "performance",
            "model": self.default_model,
            "api_key": self.openai_api_key,
        }

    def get_fallback_model(self) -> dict:
        """Standard GPT-4o configuration used when sovereign call fails."""
        return {
            "provider": "performance",
            "model": self.default_model,
            "api_key": self.openai_api_key,
        }


# Module-level singleton
settings = Settings()
