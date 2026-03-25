---
name: type-safety
description: Enforce type safety, schema centralization, and strict typing across this monorepo. Use when adding types, writing Zod schemas, reviewing code for `as any`, placing types in the wrong location, or when there is a risk of duplicated contracts between services. Also use when setting up or reviewing ESLint/Pyright config.
---

# Type Safety and Schema Centralization

## Mission

Keep all cross-service data contracts defined exactly once in `shared/schemas/` and
reused everywhere. Prevent duplicated type definitions between services. Maintain
a strict boundary between shared contracts, service-internal types, and UI-only types.

This project is a mixed TypeScript + Python monorepo. The rules apply to both sides —
Zod for TypeScript, Pydantic for Python, JSON Schema as the canonical source of truth.

---

## Non-negotiable rules

1. **Never use `as any`, `any`, or `// @ts-ignore`** to bypass typing. If the type
   is unknown, model it properly as a discriminated union or `z.unknown()` with an
   explicit comment explaining why.

2. **Cross-service contracts live in `shared/schemas/`** as:
   - `shared/schemas/subjects.json` — JSON Schema (source of truth)
   - `shared/schemas/kafka-messages.ts` — Zod schemas (TypeScript)
   - `shared/schemas/kafka_messages.py` — Pydantic models (Python)

3. **Service-internal types stay inside the service.** Do not export them to `shared/`.
   DB row types, repository types, internal state — all stay local.

4. **Frontend-only types live in `services/frontend/src/types/`.**
   Never import these from anywhere outside the frontend service.

5. **Zod is the validator on every external boundary in TypeScript:**
   - API request bodies
   - API response parsing
   - Kafka message deserialization
   - Config/env variable parsing

6. **Pydantic is the validator on every external boundary in Python:**
   - FastAPI request/response models
   - Kafka message deserialization
   - Config parsing (pydantic-settings)

7. **`z.infer<typeof Schema>` / Pydantic's `.model_fields` are the types.**
   Never write a separate `interface` or `TypedDict` that duplicates a schema.

---

## Where types live — decision tree

For any type or interface you are about to write, follow this tree:

```
Is this type about data that crosses a service boundary
(Kafka message, HTTP request/response, shared domain object)?
│
├─ YES → shared/schemas/
│         - Add to subjects.json (JSON Schema)
│         - Add Zod schema in kafka-messages.ts
│         - Add Pydantic model in kafka_messages.py
│         - Never duplicate — import from here everywhere
│
└─ NO
   │
   Is this a database row type or ORM model?
   │
   ├─ YES → Keep it in the repo file (e.g., models.py, *.repo.ts)
   │         DO NOT export it. It is an implementation detail.
   │
   └─ NO
      │
      Is this type only used in the frontend UI
      (component props, page state, UI events, nav types)?
      │
      ├─ YES → services/frontend/src/types/
      │         Organize by domain:
      │           components.ts  — component prop interfaces
      │           pages.ts       — page-level state and params
      │           ui.ts          — shared UI primitives (icons, sizes)
      │           api.ts         — inferred types from Zod API schemas
      │
      └─ NO (service-internal logic type)
            → Keep it in the file where it is used, or a
              local types.ts inside that service's src/.
              Do not export across service boundaries.
```

---

## How to work with schemas

### Adding a new Kafka message type

1. Define the shape in `shared/schemas/subjects.json` (JSON Schema)
2. Add a Zod schema in `shared/schemas/kafka-messages.ts`:
   ```typescript
   export const SceneDetectedEventSchema = z.object({
     job_id: z.string().uuid(),
     scene_id: z.string().uuid(),
     start_ms: z.number().int().nonnegative(),
     end_ms: z.number().int().nonnegative(),
     frame_path: z.string(),
   })
   export type SceneDetectedEvent = z.infer<typeof SceneDetectedEventSchema>
   ```
3. Add the equivalent Pydantic model in `shared/schemas/kafka_messages.py`:
   ```python
   class SceneDetectedEvent(BaseModel):
       job_id: UUID
       scene_id: UUID
       start_ms: int
       end_ms: int
       frame_path: str
   ```
4. Both services import from `shared/schemas/` — never redefine locally.

### Adding a new API endpoint

TypeScript (`ingest-api`, `query-api`):
```typescript
// Define Zod schemas for request and response
const IngestRequestSchema = z.object({ ... })
const IngestResponseSchema = z.object({ ... })

// Use z.infer — never write a separate interface
type IngestRequest = z.infer<typeof IngestRequestSchema>
type IngestResponse = z.infer<typeof IngestResponseSchema>

// Validate incoming at the boundary
const body = IngestRequestSchema.parse(request.body) // throws on invalid
```

Python (FastAPI services):
```python
# Pydantic model IS the type — no separate TypedDict
class IngestRequest(BaseModel):
    source: str
    media_title: str | None = None

# FastAPI validates automatically when used as parameter type
@app.post("/ingest")
async def ingest(body: IngestRequest) -> IngestResponse:
    ...
```

### Validating API responses on the frontend

Always parse API responses through Zod before using them. Never trust the shape
of an API response without validation.

```typescript
// api/subjects.ts
import { SubjectSchema } from '../schemas/subject'

export async function fetchSubject(id: string) {
  const res = await fetch(`/api/subjects/${id}`)
  const json = await res.json()
  return SubjectSchema.parse(json) // throws ZodError if shape is wrong
}
```

---

## What to flag in code review

- Any `as any`, `any` type annotation, or `// @ts-ignore`
- A type/interface defined locally that duplicates something in `shared/schemas/`
- A Kafka consumer that deserializes a message without Zod/Pydantic validation
- An API endpoint that returns data without a typed response schema
- Frontend importing types from a backend service directly (instead of `shared/schemas/`)
- A `TypedDict` or `dataclass` in Python that duplicates an existing Pydantic model
- `z.any()` or `z.unknown()` without a comment explaining why it is intentional
- `dict` used as a return type in Python where a Pydantic model should be used

---

## Python-specific rules

- **Use `pydantic-settings`** for all config and env variable parsing. Never read
  `os.environ` directly in service code.
  ```python
  from pydantic_settings import BaseSettings

  class Settings(BaseSettings):
      kafka_broker: str
      gemini_api_key: str
      qdrant_url: str = "http://qdrant:6333"

  settings = Settings()  # validates and raises on missing required vars
  ```

- **FastAPI response models are mandatory.** Every endpoint must declare
  `response_model=SomeModel`. Never return a raw `dict`.

- **Adapter return types are typed.** The `VideoAnalyzerAdapter` base class
  declares the return type. Concrete implementations must match it exactly.

---

## TypeScript-specific rules

- **`tsconfig.json` strict mode is always on:**
  ```json
  {
    "compilerOptions": {
      "strict": true,
      "noUncheckedIndexedAccess": true,
      "exactOptionalPropertyTypes": true
    }
  }
  ```

- **Environment variables are parsed with Zod** at startup, not inline:
  ```typescript
  const EnvSchema = z.object({
    KAFKA_BROKER: z.string(),
    PORT: z.coerce.number().default(3000),
  })
  export const env = EnvSchema.parse(process.env)
  ```

- **No `!` non-null assertions** except where you have just checked the value and
  TypeScript cannot narrow it (rare). Add a comment if you use one.
