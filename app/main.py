from fastapi import FastAPI

from app.models import AnalyzeResponse, CarrierPayloadRequest
from app.normalizer import normalize_claim


# FastAPI application metadata appears in Swagger/OpenAPI documentation.
app = FastAPI(
    title="Carrier Change Intelligence Agent",
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
        "message": "Carrier Change Intelligence Agent is running."
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
    normalized_claim = normalize_claim(
        carrier=request.carrier,
        payload=request.payload,
    )

    requires_human_review = len(normalized_claim.warnings) > 0

    return AnalyzeResponse(
        carrier=request.carrier,
        normalized_claim=normalized_claim,
        warnings=normalized_claim.warnings,
        requires_human_review=requires_human_review,
        message="Carrier payload normalized successfully.",
    )