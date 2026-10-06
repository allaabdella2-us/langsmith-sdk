# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SessionResolveResponse", "Result", "ResultAddress"]


class ResultAddress(BaseModel):
    """`address` is the address as requested."""

    id: str
    """`id` is the Agent's user-assigned id."""

    environment: Literal["LOCAL", "DEVELOPMENT", "STAGING", "PRODUCTION"]
    """`environment` is the Agent environment."""

    kind: Literal["AGENT"]
    """`kind` is always `AGENT`."""


class Result(BaseModel):
    address: Optional[ResultAddress] = None
    """`address` is the address as requested."""

    session_id: Optional[str] = None
    """`session_id` is the tracing project (session) of the Agent environment."""


class SessionResolveResponse(BaseModel):
    results: Optional[List[Result]] = None
