# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["SessionResolveResponse"]


class SessionResolveResponse(BaseModel):
    session_id: Optional[str] = None
    """`session_id` is the tracing project (session) of the Agent environment."""
