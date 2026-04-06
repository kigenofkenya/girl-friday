"""Application configuration.

Defaults can be overridden via environment variables:
    GIRL_FRIDAY_WHISPER_MODEL   (default: base)
    GIRL_FRIDAY_OLLAMA_MODEL     (default: neural-chat)
    GIRL_FRIDAY_RECORD_DURATION  (default: 5)
    GIRL_FRIDAY_SAMPLE_RATE      (default: 16000)
"""
import os


class Config:
    """Application configuration with environment variable overrides."""

    WHISPER_MODEL = os.environ.get("GIRL_FRIDAY_WHISPER_MODEL", "base")
    OLLAMA_MODEL = os.environ.get("GIRL_FRIDAY_OLLAMA_MODEL", "neural-chat")
    RECORD_DURATION = int(os.environ.get("GIRL_FRIDAY_RECORD_DURATION", "5"))
    SAMPLE_RATE = int(os.environ.get("GIRL_FRIDAY_SAMPLE_RATE", "16000"))

    # Optional system prompt for the AI
    SYSTEM_PROMPT = os.environ.get("GIRL_FRIDAY_SYSTEM_PROMPT", None)
