# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["SessionResolveParams", "Address"]


class SessionResolveParams(TypedDict, total=False):
    addresses: Required[Iterable[Address]]
    """`addresses` are the Agent environment addresses to resolve."""


class Address(TypedDict, total=False):
    id: Required[str]
    """`id` is the Agent's user-assigned id."""

    environment: Required[Literal["LOCAL", "DEVELOPMENT", "STAGING", "PRODUCTION"]]
    """`environment` is the Agent environment."""

    kind: Required[Literal["AGENT"]]
    """`kind` is always `AGENT`."""
