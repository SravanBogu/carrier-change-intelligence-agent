# Architecture Decisions

This document records the key design choices for the Carrier Change Intelligence Agent.

**Version:** 0.1  
**Last updated:** 2026-08-13  
**Status:** Active  
**Author:** Sravan Bogu

## ADR-001: Use Python and FastAPI

**Date:** 2026-08-13  
**Status:** Accepted

**Decision:** Use Python and FastAPI for the initial application API.

**Reason:** Python is well suited for data processing, API development, Azure AI integrations, and evaluation tooling. FastAPI provides typed request validation and automatic Swagger/OpenAPI documentation.

**Consequences:**

- The application exposes HTTP endpoints that can later be used by a web UI, Power Automate flow, Copilot Studio action, or other approved client.
- Pydantic models validate API requests and responses.
- The application can be deployed later to Azure App Service, Container Apps, or an Azure Functions-based API pattern.

## ADR-002: Build local functionality first

**Date:** 2026-08-13  
**Status:** Accepted

**Decision:** **Decision:** Build deterministic normalization, validation, local retrieval, and unit tests before integrating Azure AI Search or Microsoft Foundry services.

**Reason:** Local development is faster to debug and keeps business logic separate from Azure quota, authentication, region, and configuration issues.

**Consequences:**

- The project remains demo-ready when cloud services are unavailable.
- Unit tests run without cloud dependencies.
- Local components can later be replaced by Azure AI Search and Microsoft Foundry integrations.

## ADR-003: Normalize carrier fields into a canonical schema

**Date:** 2026-08-13  
**Status:** Accepted

**Decision:** Map carrier-specific source fields to a canonical internal claims schema before retrieval or AI processing.

**Reason:** Different carriers can use different field names for the same value. For example, `lossdate`, `dateLoss`, and `date_of_loss` can represent the same business field.

**Consequences:**

- The application uses explicit field mappings rather than asking a model to infer data structure.
- Invalid, unknown, missing, or conflicting values generate warnings or human-review flags.
- Downstream retrieval and workflow logic uses a consistent schema.

## ADR-004: Keep retrieval replaceable

**Date:** 2026-08-13  
**Status:** Accepted

**Decision:** Start with local carrier documents and a local retrieval implementation, then add Azure AI Search through the same application interface.

**Reason:** The business logic should not depend directly on a specific search technology during early development.

**Consequences:**

- Local development uses dummy carrier documents.
- Azure AI Search can later provide metadata filtering by carrier, status, effective date, source, and document version.
- The application retains source metadata for citations.

## ADR-005: Ground responses and require human review when needed

**Date:** 2026-08-13  
**Status:** Accepted

**Decision:** Generate responses only from approved retrieved evidence and route unsupported or consequential questions to human review.

**Reason:** The application must not invent carrier rules or make insurance decisions such as coverage, payment, deductible, fraud, fault, liability, approval, or denial.

**Consequences:**

- The model receives only relevant retrieved evidence.
- Responses include source metadata or citations.
- Missing, conflicting, or unsupported evidence returns a safe human-review response.
- The project demonstrates intake and guidance support, not claim adjudication.

## ADR-006: Keep consequential insurance decisions out of scope

**Date:** 2026-08-13  
**Status:** Accepted

**Decision:** The application will provide intake assistance and approved procedural guidance only. It will not determine coverage, payment, deductible, fault, liability, fraud, claim approval, or claim denial.

**Reason:** These decisions require authorized systems, policy interpretation, and qualified human review.

**Consequences:**

- The application returns a human-review response for consequential or unsupported requests.
- The solution can later create a review ticket or route the request to an authorized queue.
- The application does not represent generated output as a claim decision.

## ADR-007: Use GitHub Flow and pull requests

**Date:** 2026-08-13  
**Status:** Accepted

**Decision:** Use `main` as the stable integration branch and `feature/*` branches for focused work. Merge completed work through pull requests.

**Reason:** This creates a clear history of changes, review points, validation evidence, and a releasable baseline.

**Consequences:**

- Each feature branch contains one focused change.
- Pull requests include summary, validation steps, and follow-up work.
- Changes are reviewed for documentation, tests, and accidental secrets before merge.
- Release tags can identify tested Dev, UAT, and Production baselines.