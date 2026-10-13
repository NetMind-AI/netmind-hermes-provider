from __future__ import annotations

import importlib
import os
import shutil
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
HERMES_ROOT = os.environ.get("HERMES_AGENT_ROOT")


@pytest.fixture
def hermes_providers(monkeypatch: pytest.MonkeyPatch):
    if not HERMES_ROOT or not (Path(HERMES_ROOT) / "providers" / "base.py").is_file():
        pytest.skip("set HERMES_AGENT_ROOT to a Hermes Agent checkout")

    monkeypatch.syspath_prepend(str(HERMES_ROOT))
    for module_name in list(sys.modules):
        if module_name == "providers" or module_name.startswith("providers."):
            sys.modules.pop(module_name)
    return importlib.import_module("providers")


def test_plugin_registers_through_hermes_user_discovery(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    hermes_providers,
):
    plugin_dir = tmp_path / "plugins" / "netmind-provider"
    shutil.copytree(
        PLUGIN_ROOT, plugin_dir,
        ignore=shutil.ignore_patterns("tests", "__pycache__", ".git", ".pytest_cache", ".ruff_cache", ".env"),
    )

    layer = hermes_providers._HomeLayer()
    monkeypatch.setattr(hermes_providers, "_user_plugins_dir", lambda: None)
    monkeypatch.setattr(
        hermes_providers, "_installed_plugins_dir", lambda: plugin_dir.parent
    )
    hermes_providers._scan_home_layer(layer, "netmind-test-home")

    profile = layer.registry.get("netmind")
    assert profile is not None
    assert layer.aliases["netmind-ai"] == "netmind"
    assert profile.api_mode == "chat_completions"
    assert profile.base_url == "https://api.netmind.ai/inference-api/v1"
    assert profile.env_vars == ("NETMIND_API_KEY",)
    assert profile.supports_model_listing is False
    assert profile.supports_health_check is False

    assert len(profile.fallback_models) == 31
    assert profile.fallback_models[0] == "openai/gpt-6-astra"
    assert "anthropic/claude-opus-5-5" in profile.fallback_models
    capabilities = profile.model_capabilities["openai/gpt-6-astra"]
    assert capabilities["supports_tools"] is False
    assert capabilities["supports_reasoning"] is True
    assert capabilities["supports_vision"] is True
    assert capabilities["context_window"] == 1000000
    assert profile.get_max_tokens("openai/gpt-6-astra") == 128000

    claude = profile.model_capabilities["anthropic/claude-opus-5-5"]
    assert claude["supports_tools"] is True
    assert claude["supports_reasoning"] is True
    assert claude["supports_vision"] is True
    assert claude["context_window"] == 1000000
    assert profile.get_max_tokens("anthropic/claude-opus-5-5") == 128000
