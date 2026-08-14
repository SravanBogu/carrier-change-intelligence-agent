from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel


# FastAPI application metadata appears in Swagger/OpenAPI documentation.
app = FastAPI(
    title="Carrier Change Intelligence Agent",
    description=(
        "A code-first demonstration of carrier payload normalization, "
        "grounded knowledge retrieval, and safe human-review fallback."
    ),
    version="0.1.0",
)


# Accepts a carrier identifier and its source-specific JSON payload.
class CarrierPayloadRequest(BaseModel):
    carrier: str
    payload: dict[str, Any]


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


# Receives a validated payload. Normalization will be added in the next feature.
@app.post("/analyze")
def analyze_payload(request: CarrierPayloadRequest) -> dict[str, Any]:
    return {
        "carrier": request.carrier,
        "received_payload": request.payload,
        "message": "Payload received. Field normalization will be added next.",
    }