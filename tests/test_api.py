from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_valid_payload_returns_normalized_claim() -> None:
    response = client.post(
        "/analyze",
        json={
            "carrier": "Northwind Mutual",
            "payload": {
                "claimId": "C-1001",
                "policyNumber": "POL-20481",
                "lossdate": "2026-07-30",
                "lossType": "Windshield damage",
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["carrier"] == "Northwind Mutual"
    assert body["normalized_claim"]["claim_id"] == "C-1001"
    assert body["normalized_claim"]["policy_number"] == "POL-20481"
    assert body["normalized_claim"]["date_of_loss"] == "2026-07-30"
    assert body["normalized_claim"]["loss_type"] == "Windshield damage"
    assert body["warnings"] == []
    assert body["requires_human_review"] is False
    assert "warnings" not in body["normalized_claim"]


def test_analyze_unknown_field_requires_human_review() -> None:
    response = client.post(
        "/analyze",
        json={
            "carrier": "Northwind Mutual",
            "payload": {
                "lossOccurredWhen": "2026-07-30",
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["normalized_claim"]["date_of_loss"] is None
    assert body["requires_human_review"] is True
    assert len(body["warnings"]) == 1
    assert "Unmapped source field: lossOccurredWhen" in body["warnings"][0]


def test_analyze_missing_carrier_returns_validation_error() -> None:
    response = client.post(
        "/analyze",
        json={
            "payload": {
                "lossdate": "2026-07-30",
            },
        },
    )

    assert response.status_code == 422