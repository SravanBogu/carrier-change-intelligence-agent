from typing import Any

from pydantic import BaseModel


class CarrierPayloadRequest(BaseModel):
    carrier: str
    payload: dict[str, Any]


class NormalizedClaim(BaseModel):
    carrier: str
    claim_id: str | None = None
    policy_number: str | None = None
    date_of_loss: str | None = None
    date_reported: str | None = None
    loss_type: str | None = None


class AnalyzeResponse(BaseModel):
    carrier: str
    normalized_claim: NormalizedClaim
    warnings: list[str]
    requires_human_review: bool
    message: str