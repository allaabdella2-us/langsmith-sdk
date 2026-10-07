"""Sandbox clients derive their URLs with the main Client's base-URL rule.

``LANGSMITH_ENDPOINT`` may be a bare host, or end in ``/api`` or ``/api/v1``
(self-hosted). Every form must give the same ``/api/v2/sandboxes`` box base and
the same registries root, with no doubled ``/api`` or ``/api/v1`` prefix (QAAS-62).
"""

import pytest

from langsmith import utils as ls_utils
from langsmith.sandbox import AsyncSandboxClient, SandboxClient

CLIENTS = [SandboxClient, AsyncSandboxClient]


@pytest.fixture(autouse=True)
def _fresh_env(monkeypatch):
    for var in ("LANGCHAIN_ENDPOINT", "LANGSMITH_ENDPOINT"):
        monkeypatch.delenv(var, raising=False)
    ls_utils.get_env_var.cache_clear()
    yield
    ls_utils.get_env_var.cache_clear()


@pytest.mark.parametrize("client_cls", CLIENTS)
@pytest.mark.parametrize(
    "endpoint, box_base, api_root",
    [
        (
            "https://host/api/v1",
            "https://host/api/v2/sandboxes",
            "https://host",
        ),
        (
            "https://host/api/v1/",
            "https://host/api/v2/sandboxes",
            "https://host",
        ),
        ("https://host/api", "https://host/api/v2/sandboxes", "https://host"),
        ("https://host", "https://host/api/v2/sandboxes", "https://host"),
        (
            "https://api.smith.langchain.com",
            "https://api.smith.langchain.com/api/v2/sandboxes",
            "https://api.smith.langchain.com",
        ),
    ],
)
def test_env_endpoint_forms(monkeypatch, client_cls, endpoint, box_base, api_root):
    monkeypatch.setenv("LANGSMITH_ENDPOINT", endpoint)
    client = client_cls(api_key="k")
    assert client._base_url == box_base
    assert client._api_root() == api_root


@pytest.mark.parametrize("client_cls", CLIENTS)
@pytest.mark.parametrize(
    "api_endpoint, api_root",
    [
        # The documented explicit form, and the self-hosted equivalent of it.
        (
            "https://api.smith.langchain.com/v2/sandboxes",
            "https://api.smith.langchain.com",
        ),
        ("https://host/api/v2/sandboxes", "https://host"),
        ("http://test-server:8080", "http://test-server:8080"),
    ],
)
def test_explicit_endpoint_registries_root(client_cls, api_endpoint, api_root):
    client = client_cls(api_endpoint=api_endpoint, api_key="k")
    assert client._base_url == api_endpoint
    assert client._api_root() == api_root
