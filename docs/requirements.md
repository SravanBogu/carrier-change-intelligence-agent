# Carrier Change Intelligence Agent API - Requirements

## Business problem

Carrier integrations may use different field names for the same business value.

Examples:

- `lossdate`
- `dateLoss`
- `date_of_loss`
- `incidentDate`

If downstream automation expects only one field name, it can miss or misinterpret the date of loss. This can create incomplete intake data, incorrect routing, inaccurate search, or unsupported AI responses.

## Goal

Create a code-first application that normalizes incoming carrier payloads, retrieves approved carrier guidance, and produces grounded responses with clear safety boundaries.

## Users

- Claims intake representative
- Customer-service representative
- Claims reviewer or adjuster
- Integration support team
- Application administrator

## In scope

- Receive a carrier name and JSON payload through an API.
- Normalize carrier-specific field aliases to canonical names.
- Validate missing, invalid, unknown, and conflicting input values.
- Retrieve only active carrier guidance.
- Return citation/source metadata with grounded response.
- Route missing, ambiguous, or unsupported requests to human review.
- Use dummy data only.
- Demonstrate GitHub, tests, and Dev/UAT design.

## Out of scope

- Real insurance data
- Claim payment
- Coverage determination
- Deductible calculation
- Fraud determination
- Liability or fault determination
- Claim approval or denial
- Production policy-administration system integration

## Success criteria

- `lossdate`, `dateLoss`, and `date_of_loss` normalize to `date_of_loss`.
- Invalid or conflicting date values create warnings.
- The application retrieves carrier-specific active guidance.
- The response shows source metadata.
- Unsupported questions return a safe human-review response.
- Unit tests pass.
- The project can run locally using documented instructions.