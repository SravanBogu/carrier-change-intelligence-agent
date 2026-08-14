from app.normalizer import normalize_claim


def test_lossdate_maps_to_date_of_loss() -> None:
    claim, warnings = normalize_claim(
        carrier="Northwind Mutual",
        payload={"lossdate": "2026-07-30"},
    )

    assert claim.date_of_loss == "2026-07-30"
    assert warnings == []


def test_date_loss_alias_maps_to_date_of_loss() -> None:
    claim, warnings = normalize_claim(
        carrier="Fabrikam Insurance",
        payload={"dateLoss": "2026-08-01"},
    )

    assert claim.date_of_loss == "2026-08-01"
    assert warnings == []


def test_policy_number_alias_maps_to_canonical_field() -> None:
    claim, warnings = normalize_claim(
        carrier="Northwind Mutual",
        payload={"policyNumber": "POL-20481"},
    )

    assert claim.policy_number == "POL-20481"
    assert warnings == []


def test_conflicting_date_fields_create_warning() -> None:
    claim, warnings = normalize_claim(
        carrier="Northwind Mutual",
        payload={
            "lossdate": "2026-07-30",
            "date_of_loss": "2026-07-29",
        },
    )

    assert claim.date_of_loss == "2026-07-30"
    assert len(warnings) == 1
    assert "Conflicting values received" in warnings[0]


def test_invalid_date_creates_warning() -> None:
    claim, warnings = normalize_claim(
        carrier="Northwind Mutual",
        payload={"lossdate": "07/30/2026"},
    )

    assert claim.date_of_loss is None
    assert len(warnings) == 1
    assert "YYYY-MM-DD" in warnings[0]


def test_unknown_field_creates_warning() -> None:
    claim, warnings = normalize_claim(
        carrier="Northwind Mutual",
        payload={"lossOccurredWhen": "2026-07-30"},
    )

    assert claim.date_of_loss is None
    assert len(warnings) == 1
    assert "Unmapped source field: lossOccurredWhen" in warnings[0]