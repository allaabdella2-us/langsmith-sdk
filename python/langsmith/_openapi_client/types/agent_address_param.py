# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["AgentAddressParam"]


class AgentAddressParam(TypedDict, total=False):
    id: Required[str]
    """`id` is the Agent's user-assigned id."""

    environment: Required[Literal["LOCAL", "DEVELOPMENT", "STAGING", "PRODUCTION"]]
    """`environment` is the Agent environment."""

    kind: Required[Literal["AGENT"]]
    """`kind` is always `AGENT`."""
