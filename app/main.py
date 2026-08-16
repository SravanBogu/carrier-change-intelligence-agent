from fastapi import FastAPI

from app.models import AnalyzeResponse, CarrierPayloadRequest
from app.normalizer import normalize_claim


# FastAPI application metadata appears in Swagger/OpenAPI documentation.
app = FastAPI(
    title="Carrier Change Intelligence Agent API",
    description=(
        "A code-first demonstration of carrier payload normalization, "
        "grounded knowledge retrieval, and safe human-review fallback."
    ),
    version="0.2.0",
)


# Simple endpoint used to confirm that the API is running.
@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "Carrier Change Intelligence Agent API is running."
    }


# Health endpoint for local checks and future deployment monitoring.
@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": "local",
    }


# Validates the request, normalizes carrier fields, and returns a typed response.
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_payload(request: CarrierPayloadRequest) -> AnalyzeResponse:
    normalized_claim, warnings = normalize_claim(
        carrier=request.carrier,
        payload=request.payload,
    )

    requires_human_review = bool(warnings)

    return AnalyzeResponse(
        carrier=request.carrier,
        normalized_claim=normalized_claim,
        warnings=warnings,
        requires_human_review=requires_human_review,
        message=(
            "Carrier payload normalized successfully."
            if not warnings
            else "Carrier payload normalized with warnings and requires human review."
        ),
    )