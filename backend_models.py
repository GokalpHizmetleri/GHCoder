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
import json
import os
import threading
import time
import urllib.request

from openai import OpenAI

ZEN_BASE_URL = "https://opencode.ai/zen/v1"

# Pricing revalidation. Zen exposes no public priced model API of its own,
# so prices are re-checked against models.dev (the open model/pricing
# database the OpenCode team maintains and links from its docs).
_PRICING_URL = "https://models.dev/api.json"
_PRICING_TTL_SECONDS = 3600  # re-verify prices at most once an hour
_pricing_lock = threading.Lock()
_pricing_snapshot = {"checked_at": 0.0, "zero_cost_ids": None}

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


def _fetch_zero_cost_ids():
    """Return Zen model ids currently priced at exactly $0 in/$0 out.

    Returns None when pricing cannot be confirmed (fetch/parse failure or
    missing data) so callers can fail closed.
    """
    try:
        req = urllib.request.Request(
            _PRICING_URL, headers={"User-Agent": "anycoder-backend"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        models = data["opencode"]["models"]
        return {
            mid
            for mid, m in models.items()
            if m.get("cost", {}).get("input") == 0
            and m.get("cost", {}).get("output") == 0
        }
    except Exception as exc:
        print(f"[Pricing] WARNING: cannot confirm OpenCode Zen pricing: {exc}")
        return None


def get_allowed_models():
    """Model ids that may be called right now.

    An id is allowed only when it is on the build-time free allowlist AND
    a recent pricing check confirmed it still costs $0. Fails closed in
    both directions: when pricing has never been confirmed, and when a
    stale snapshot cannot be re-confirmed, nothing is allowed. Note this
    is best-effort: an aggregator price check cannot guarantee what the
    provider actually bills.
    """
    now = time.time()
    with _pricing_lock:
        snapshot = _pricing_snapshot["zero_cost_ids"]
        stale = now - _pricing_snapshot["checked_at"] > _PRICING_TTL_SECONDS
        if snapshot is None or stale:
            ids = _fetch_zero_cost_ids()
            if ids is not None:
                _pricing_snapshot["zero_cost_ids"] = ids
                _pricing_snapshot["checked_at"] = now
                snapshot = ids
            else:
                # Cannot confirm current pricing: drop the stale snapshot
                # and block all model calls until confirmation succeeds.
                snapshot = None
    if snapshot is None:
        return set()
    return FREE_ZEN_MODELS & snapshot


def get_inference_client(model_id: str, provider: str = "auto"):
    """
    Return an OpenAI-compatible client pointed at OpenCode Zen.

    Fails closed in both directions: a model id is accepted only while it
    is on the free allowlist AND currently confirmed $0 (re-checked against
    live pricing at least hourly), so a repriced or renamed model can never
    be called. A missing server key raises an explicit error.
    """
    if model_id not in get_allowed_models():
        raise ValueError(
            f"Model '{model_id}' is not available. Only OpenCode Zen models "
            "currently confirmed free ($0) are allowed."
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
