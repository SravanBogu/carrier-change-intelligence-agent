from datetime import date
from typing import Any

from app.models import NormalizedClaim


FIELD_ALIASES = {
    "claimId": "claim_id",
    "claim_id": "claim_id",
    "claimNo": "claim_id",
    "policyNumber": "policy_number",
    "policy_number": "policy_number",
    "policy_no": "policy_number",
    "lossdate": "date_of_loss",
    "dateLoss": "date_of_loss",
    "date_of_loss": "date_of_loss",
    "incidentDate": "date_of_loss",
    "reportDate": "date_reported",
    "date_reported": "date_reported",
    "reported_at": "date_reported",
    "lossType": "loss_type",
    "loss_type": "loss_type",
    "incident_type": "loss_type",
}


def normalize_claim(
    carrier: str,
    payload: dict[str, Any],
) -> NormalizedClaim:
    normalized: dict[str, Any] = {}
    warnings: list[str] = []

    for source_field, value in payload.items():
        target_field = FIELD_ALIASES.get(source_field)

        if target_field is None:
            warnings.append(f"Unmapped source field: {source_field}")
            continue

        if target_field in normalized and normalized[target_field] != value:
            warnings.append(
                f"Conflicting values received for canonical field: {target_field}"
            )
            continue

        normalized[target_field] = value

    for date_field in ("date_of_loss", "date_reported"):
        if date_field in normalized and normalized[date_field] is not None:
            normalized[date_field] = normalize_date(
                field_name=date_field,
                value=normalized[date_field],
                warnings=warnings,
            )

    return NormalizedClaim(
        carrier=carrier,
        warnings=warnings,
        **normalized,
    )


def normalize_date(
    field_name: str,
    value: Any,
    warnings: list[str],
) -> str | None:
    if not isinstance(value, str):
        warnings.append(f"{field_name} must be a date string in YYYY-MM-DD format")
        return None

    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        warnings.append(f"{field_name} must use YYYY-MM-DD format")
        return None