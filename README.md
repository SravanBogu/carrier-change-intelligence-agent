# Carrier Change Intelligence Agent API

A code-first FastAPI service that normalizes changing insurance-carrier claim payloads into a canonical schema, identifies data-quality issues, and flags submissions that require human review.

> This repository currently contains the payload-normalization API. Grounded knowledge retrieval, Copilot Studio orchestration, and Azure AI Foundry integration are planned future enhancements.

## Problem

Insurance carriers can send similar claim data using different field names and formats.

For example, the same business concept may arrive as:

```json
{
  "lossdate": "2026-07-30"
}
```

or:

```json
{
  "dateLoss": "2026-07-30"
}
```

This service converts recognized carrier-specific fields into a consistent internal claim schema. It also produces warnings when data is unknown, invalid, or conflicting, so uncertain payloads can be routed to a human reviewer rather than silently accepted.

## Current capabilities

- FastAPI endpoints for local health and payload-analysis checks
- Canonical Pydantic models for carrier payloads and normalized claims
- Alias mapping for common carrier field variations
- ISO date validation using `YYYY-MM-DD`
- Warnings for unmapped source fields
- Warnings for conflicting values that map to the same canonical field
- Human-review flag when one or more warnings are present
- Pytest coverage for the primary normalization scenarios

## Architecture

```text
Carrier payload
    ↓
POST /analyze
    ↓
Field alias normalization
    ↓
Canonical normalized claim + processing warnings
    ↓
Human-review decision
    ↓
Typed API response
```

## Project structure

```text
carrier-change-intelligence-agent/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── normalizer.py
├── tests/
│   └── test_normalizer.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Setup

### Prerequisites

- Python 3.11 or later
- A terminal such as PowerShell
- Visual Studio Code is recommended

### Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

If you do not yet have a `requirements.txt`, install the current project dependencies:

```powershell
python -m pip install fastapi "uvicorn[standard]" pytest
```

## Run the API

From the project root:

```powershell
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Useful local endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /` | Confirms the service is running |
| `GET /health` | Returns a simple local health status |
| `POST /analyze` | Normalizes a carrier payload and returns warnings/review status |

## Example request

Send this request to `POST /analyze` through Swagger UI:

```json
{
  "carrier": "Northwind Mutual",
  "payload": {
    "claimId": "C-1001",
    "policyNumber": "POL-20481",
    "lossdate": "2026-07-30",
    "lossType": "Windshield damage"
  }
}
```

## Example response

```json
{
  "carrier": "Northwind Mutual",
  "normalized_claim": {
    "carrier": "Northwind Mutual",
    "claim_id": "C-1001",
    "policy_number": "POL-20481",
    "date_of_loss": "2026-07-30",
    "date_reported": null,
    "loss_type": "Windshield damage"
  },
  "warnings": [],
  "requires_human_review": false,
  "message": "Carrier payload normalized successfully."
}
```

## Supported field aliases

| Canonical field | Recognized source fields |
|---|---|
| `claim_id` | `claimId`, `claim_id`, `claimNo` |
| `policy_number` | `policyNumber`, `policy_number`, `policy_no` |
| `date_of_loss` | `lossdate`, `dateLoss`, `date_of_loss`, `incidentDate` |
| `date_reported` | `reportDate`, `date_reported`, `reported_at` |
| `loss_type` | `lossType`, `loss_type`, `incident_type` |

## Warning and review behavior

The API returns `requires_human_review: true` when one or more processing warnings occur.

Examples include:

- An unrecognized field, such as `lossOccurredWhen`
- An invalid date, such as `07/30/2026` instead of `2026-07-30`
- Conflicting source values mapped to the same canonical field

Example conflict payload:

```json
{
  "carrier": "Northwind Mutual",
  "payload": {
    "lossdate": "2026-07-30",
    "date_of_loss": "2026-07-29"
  }
}
```

In this case, the first recognized value is retained, a warning is returned, and the payload is flagged for human review.

## Run tests

From the project root with the virtual environment activated:

```powershell
python -m pytest -q
```

The suite includes:

- Unit tests for field alias mapping, invalid dates, conflicts, and unmapped fields
- API endpoint tests for a successful request, human-review behavior, and request validation

## Development notes

- All carrier names, policy numbers, claim identifiers, and payloads in this repository are dummy examples.
- `NormalizedClaim` contains only canonical claim data.
- Processing diagnostics are returned once at the top level of `AnalyzeResponse`.
- The current conflict policy retains the first recognized source value and creates a warning for later conflicting values.

## Roadmap

- Add API test coverage reporting and minimum coverage thresholds
- Add structured logging and correlation IDs
- Add configuration-driven carrier alias maps
- Add authenticated API access and production deployment configuration
- Add grounded carrier-policy retrieval with Azure AI Foundry
- Add Copilot Studio and Power Automate orchestration
- Add human-review workflow integration
- Add observability, evaluation, and tracing for AI-assisted responses

## License

This project is provided as a portfolio and learning demonstration. Add a formal license before using it in another project or production environment.