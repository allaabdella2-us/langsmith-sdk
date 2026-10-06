# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SessionResolveParams", "ResolveAddress"]


class SessionResolveParams(TypedDict, total=False):
    address: Required[ResolveAddress]
    """`address` names the tracing project to resolve."""


class ResolveAddress(TypedDict, total=False):
    """`address` names the tracing project to resolve."""

    kind: Required[Literal["AGENT", "EXPERIMENT", "EVALUATOR"]]
    """`kind` is the type of address."""

    id: str
    """
    `id` is the Agent's user-assigned id for AGENT, or the experiment's id for
    EXPERIMENT. It is not set for EVALUATOR.
    """

    environment: Literal["LOCAL", "DEVELOPMENT", "STAGING", "PRODUCTION"]
    """`environment` is the Agent environment. It is only set for AGENT."""
