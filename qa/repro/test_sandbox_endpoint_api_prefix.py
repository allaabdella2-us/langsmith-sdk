"""Repro for finding 91293c5a: sandbox clients ignore the shared base-URL rule.

The main ``Client`` turns ``LANGSMITH_ENDPOINT`` into the base URL for the
``/api/v2/...`` routes with ``langsmith.client._get_openapi_base_url``, which
strips a trailing ``/api/v1`` or ``/api``. ``SandboxClient`` and
``AsyncSandboxClient`` do not use that rule. They append ``/v2/sandboxes`` to the
raw endpoint, and for registries they strip only ``/v2/sandboxes``. With a
self-hosted endpoint such as ``https://host/api/v1``, sandbox requests leave the
SDK with a doubled API prefix:

    boxes:      https://host/api/v1/v2/sandboxes/boxes
    registries: https://host/api/v1/api/v2/sandboxes/registries
    (endpoint https://host/api) registries: https://host/api/api/v2/...

Each test asserts the URL that the main Client's rule produces for the same
endpoint. The tests fail now and pass once the sandbox clients reuse that rule.
No server is involved: these tests check the URL the SDK builds. They do not
check how any gateway routes it.

Run from python/ (PYTHONPATH matches `make tests`, which aliases httpx to the
httpx2 backend so pytest_httpx can intercept it):

    PYTHONPATH=tests/httpx2_alias .venv/bin/pytest \
        ../qa/repro/test_sandbox_endpoint_api_prefix.py
"""

from __future__ import annotations

import asyncio

import pytest
from pytest_httpx import HTTPXMock

from langsmith import utils as ls_utils
from langsmith.client import _get_openapi_base_url
from langsmith.sandbox import AsyncSandboxClient, SandboxClient


@pytest.fixture(autouse=True)
def _fresh_env(monkeypatch):
    for var in ("LANGCHAIN_ENDPOINT", "LANGSMITH_ENDPOINT"):
        monkeypatch.delenv(var, raising=False)
    ls_utils.get_env_var.cache_clear()
    yield
    ls_utils.get_env_var.cache_clear()


def _expected(endpoint: str, path: str) -> str:
    """URL the main Client's shared rule yields for an /api/v2 route."""
    return _get_openapi_base_url(endpoint) + path


def _only_request_url(httpx_mock: HTTPXMock) -> str:
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    return str(requests[0].url).split("?")[0]


def test_box_url_with_api_v1_endpoint(monkeypatch, httpx_mock: HTTPXMock):
    endpoint = "https://host/api/v1"
    monkeypatch.setenv("LANGSMITH_ENDPOINT", endpoint)
    httpx_mock.add_response(json={"sandboxes": []})

    with SandboxClient(api_key="k", max_retries=0) as client:
        client.list_sandboxes()

    # Actual today: https://host/api/v1/v2/sandboxes/boxes
    assert _only_request_url(httpx_mock) == _expected(
        endpoint, "/api/v2/sandboxes/boxes"
    )


def test_registry_url_with_api_v1_endpoint(monkeypatch, httpx_mock: HTTPXMock):
    endpoint = "https://host/api/v1"
    monkeypatch.setenv("LANGSMITH_ENDPOINT", endpoint)
    httpx_mock.add_response(json={"registries": []})

    with SandboxClient(api_key="k", max_retries=0) as client:
        client.registries.list()

    # Actual today: https://host/api/v1/api/v2/sandboxes/registries
    assert _only_request_url(httpx_mock) == _expected(
        endpoint, "/api/v2/sandboxes/registries"
    )


def test_registry_url_with_api_endpoint(monkeypatch, httpx_mock: HTTPXMock):
    endpoint = "https://host/api"
    monkeypatch.setenv("LANGSMITH_ENDPOINT", endpoint)
    httpx_mock.add_response(json={"registries": []})

    with SandboxClient(api_key="k", max_retries=0) as client:
        client.registries.list()

    # Actual today: https://host/api/api/v2/sandboxes/registries
    assert _only_request_url(httpx_mock) == _expected(
        endpoint, "/api/v2/sandboxes/registries"
    )


def test_async_registry_url_with_api_v1_endpoint(monkeypatch, httpx_mock: HTTPXMock):
    endpoint = "https://host/api/v1"
    monkeypatch.setenv("LANGSMITH_ENDPOINT", endpoint)
    httpx_mock.add_response(json={"registries": []})

    async def _call() -> None:
        async with AsyncSandboxClient(api_key="k", max_retries=0) as client:
            await client.registries.list()

    # asyncio.run keeps this independent of pytest-asyncio config, which is not
    # picked up when the file is collected from outside python/.
    asyncio.run(_call())

    # Actual today: https://host/api/v1/api/v2/sandboxes/registries
    assert _only_request_url(httpx_mock) == _expected(
        endpoint, "/api/v2/sandboxes/registries"
    )
