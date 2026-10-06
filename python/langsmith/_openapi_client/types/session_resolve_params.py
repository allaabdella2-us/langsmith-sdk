# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .agent_address_param import AgentAddressParam

__all__ = ["SessionResolveParams"]


class SessionResolveParams(TypedDict, total=False):
    address: Required[AgentAddressParam]
    """`address` is the Agent environment address to resolve."""
