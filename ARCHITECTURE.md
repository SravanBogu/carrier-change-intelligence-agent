# Architecture

## Current local architecture

```text
Swagger UI / Browser
        |
        v
FastAPI application
        |
        +--> Pydantic request validation
        |
        +--> Carrier field normalizer
        |
        +--> Local carrier knowledge retriever
        |
        +--> Grounded response service
        |
        v
JSON response with warnings, citations, and human-review flag
```

## Azure target architecture

```text
User / Web UI / Copilot Studio
        |
        v
FastAPI application or Azure Function
        |
        +--> Pydantic validation and field normalization
        |
        +--> Azure AI Search
        |      - carrier filter
        |      - active status filter
        |      - effective date filter
        |      - source/version metadata
        |
        +--> Microsoft Foundry / Azure OpenAI model
        |      - grounded prompt
        |      - low temperature
        |      - structured response
        |
        +--> Application Insights / tracing / evaluations
        |
        v
Grounded response + citation + human-review fallback
```

## Environment strategy

```text
Local developer machine
        ↓
Azure Dev
        ↓
Azure UAT
        ↓
Azure Production
```

## Security design

- Do not commit secrets to GitHub.
- `.env.example` contains names only.
- Local `.env` is ignored by Git.
- Production uses Microsoft Entra ID, RBAC, and managed identity where supported.
- Query-only runtime access uses Search Index Data Reader.
- Content ingestion requires Search Index Data Contributor.
- Search object/index administration requires Search Service Contributor.