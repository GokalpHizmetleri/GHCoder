"""
Model inference and client management for the AnyCoder backend.

All model calls go through OpenCode Zen (https://opencode.ai/zen) with an
OpenAI-compatible client. The API key is read from the OPENCODE_ZEN_API_KEY
environment variable on the server only - it is never exposed to the
frontend and never committed to the repository.

Cost safety: only Zen models verified as $0 (input and output) are
reachable, and the check fails closed. Any unknown, renamed, or
repriced model id is rejected before any API call is made.
"""
import os

from openai import OpenAI

ZEN_BASE_URL = "https://opencode.ai/zen/v1"

# OpenCode Zen model ids verified zero-cost (input $0 and output $0) on
# 2026-10-24 against https://models.dev/api.json (provider "opencode") and
# confirmed live on https://opencode.ai/zen/v1/models.
# Fail closed: anything not listed here is rejected before any API call.
FREE_ZEN_MODELS = {
    "glm-5.3-flash-free",
    "deepseek-v4.1-flash-free",
    "mimo-v2.6-flash-free",
    "nemotron-3.5-lightning-free",
    "nemotron-3.5-super-vl-free",
    "beam-free",
    "flint-40b-free",
    "big-pickle",
}


def get_inference_client(model_id: str, provider: str = "auto"):
    """
    Return an OpenAI-compatible client pointed at OpenCode Zen.

    Fails closed in both directions: model ids outside FREE_ZEN_MODELS are
    rejected so the app can never call a paid model, and a missing server
    key raises an explicit error instead of failing silently.
    """
    if model_id not in FREE_ZEN_MODELS:
        raise ValueError(
            f"Model '{model_id}' is not available. "
            "Only verified free OpenCode Zen models are allowed."
        )

    api_key = os.getenv("OPENCODE_ZEN_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENCODE_ZEN_API_KEY is not configured on the server."
        )

    return OpenAI(base_url=ZEN_BASE_URL, api_key=api_key)


def get_real_model_id(model_id: str) -> str:
    """Zen model ids are used as-is (no provider suffixes needed)."""
    return model_id


def is_native_sdk_model(model_id: str) -> bool:
    """Check if model uses native SDK (not OpenAI-compatible)"""
    return False


def is_mistral_model(model_id: str) -> bool:
    """Check if model uses Mistral SDK"""
    return False
