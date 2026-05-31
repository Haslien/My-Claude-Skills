---
name: stack-setup
description: Scaffold or set up our standard Vercel-focused monorepo stack. Use when starting a new project, adding a new service, or when the user asks to set up a stack. Stack includes: pnpm monorepo, three backend tiers (apps/web frontend, apps/api light API, apps/services/* heavy services), Next.js App Router on Vercel, React Native+Expo (mobile), Fastify or Python+FastAPI for heavy services, SCSS, SWR, Redux Toolkit, PostgreSQL 18+Drizzle, pgvector for vector search, Docker Compose for local databases, Zod/Pydantic strict typing, Lucide React icons.
---

# Standard Project Stack (Vercel-focused)

This skill governs how we set up and scaffold projects. Apply these conventions whenever starting a new project, adding a service, or scaffolding infrastructure — unless the user explicitly overrides a specific choice.

The stack is built to deploy on **Vercel**: the web app and its API live in a single Next.js app, the database is any managed PostgreSQL with the **pgvector** extension, and there is no separate server to maintain unless a project genuinely needs one.

> Older versions of this skill are archived under `old-setups/`.

---

## Monorepo Layout

Use **pnpm workspaces**. All projects are monorepos unless explicitly told otherwise.

```
project-name/
├── apps/
│   ├── web/          # Next.js App Router — frontend UI
│   ├── mobile/       # React Native + Expo
│   ├── api/          # Light API layer — CRUD, auth, DB access (serverless on Vercel)
│   └── services/     # Heavy / specialized services, one folder each (added as needed)
│       └── <name>/   #   e.g. ai-worker (Python), media (Node)
├── packages/
│   └── shared/       # Shared Zod schemas, types, Drizzle schema, utils
├── infra/
│   └── docker-compose.yml   # Local dev databases only
├── package.json      # pnpm workspace root
└── pnpm-workspace.yaml
```

**pnpm-workspace.yaml**:
```yaml
packages:
  - 'apps/*'
  - 'apps/services/*'
  - 'packages/*'
```

Root `package.json` should have `"private": true` and workspace-level dev dependencies (TypeScript, ESLint, Prettier).

`apps/web` and `apps/api` exist from the start. `apps/services/` is empty until a heavy or language-specific workload appears — see [Application tiers](#application-tiers--where-backend-code-goes) for the rule on what goes where.

---

## Application tiers — where backend code goes

Backend work is split across three tiers **by the weight of the work**. This keeps the fast path fast and isolates anything slow, stateful, or language-specific into its own deployable.

| Tier | Folder | What lives here | Runs on | Default stack |
|------|--------|-----------------|---------|---------------|
| **Frontend** | `apps/web`, `apps/mobile` | UI only. The web app may keep BFF-only route handlers (auth callbacks, trivial form posts tied to a page) — but no business/data API. | Vercel / Expo | Next.js, Expo |
| **Light API** | `apps/api` | The canonical backend clients talk to. Thin, fast, stateless: validation, auth, CRUD, reads/writes to Postgres, and **orchestrating** heavy services. | Vercel (serverless) | Next.js Route Handlers (→ Fastify if it must be a persistent server) |
| **Heavy services** | `apps/services/<name>` | Anything slow, stateful, long-running, GPU/CPU-bound, or language-specific: AI/ML inference, embeddings, image/video, background jobs, queue workers, websockets. One folder per service. | Own deploy (container / worker) | Node + Fastify **or** Python + FastAPI |

**Golden rule — call direction:** `clients → apps/api → apps/services/*`.
The frontend never calls a heavy service directly; `apps/api` is the single front door and orchestrates the rest. A service never reaches into another service's (or the API's) database directly — it talks back over HTTP or a queue.

**When to add a service** (instead of keeping it in `apps/api`): the work exceeds serverless time/memory limits, needs a persistent connection, needs a GPU or heavy native deps, or is better written in another language. Until one of those is true, keep it in `apps/api`.

---

## Frontend — Web (Next.js App Router, Vercel)

`apps/web` is UI-first. It deploys to Vercel.

- **Framework:** Next.js (App Router) with TypeScript
- **Hosting:** Vercel (serverless / edge where it fits)
- **API in here?** Only BFF glue tightly coupled to the UI (auth callbacks, a trivial form post). Real data/business endpoints belong in `apps/api`.
- **Icons:** `lucide-react` — always. Never use emojis as icons or decorative elements.
- **Styling:** **SCSS / SASS** with CSS Modules (`*.module.scss`). Keep shared variables and mixins in a `styles/` folder. Tailwind is not the default here.
- **Data fetching (client):** **SWR** (`useSWR`)
- **Global state:** **Redux Toolkit** when there is genuine cross-cutting client state (sessions, multi-step flows, shared caches). Don't add it for trivial local state — `useState` / `useSWR` first.

Bootstrap:
```bash
pnpm create next-app apps/web --ts --app --src-dir --eslint
```

```
apps/web/
├── app/                      # Route groups for UI sections
├── features/                 # Domain logic, components, hooks (grouped by feature)
├── store/                    # Redux Toolkit store + slices (only if used)
│   ├── index.ts
│   └── <name>Slice.ts
├── styles/                   # SCSS — _variables.scss, _mixins.scss, globals.scss
└── env.ts                    # Zod-validated env config
```

---

## Light API — `apps/api` (Vercel)

The single front door for `apps/web` and `apps/mobile`. Keep it thin: validate input, check auth, read/write the database, and hand heavy work off to a service. Default to Next.js Route Handlers so it stays serverless on Vercel; switch the same folder to **Fastify** only if it must run as a persistent server.

```
apps/api/
├── app/
│   └── api/
│       └── <domain>/route.ts   # Route Handlers grouped by domain
├── services/                   # Thin business logic / DB calls (NOT heavy compute)
├── lib/                        # Clients for calling apps/services/* and external APIs
└── env.ts                      # Zod-validated env config
```

### Route Handler example (Zod on every boundary)

```typescript
import { z } from 'zod'
import { NextResponse } from 'next/server'

const BodySchema = z.object({ name: z.string().min(1) })

export async function POST(req: Request) {
  const body = BodySchema.parse(await req.json())
  // light work: read/write DB, or call a heavy service in apps/services/*
  return NextResponse.json({ id: '...', name: body.name }, { status: 201 })
}
```

If a project is genuinely tiny and will never have a separate backend, the API may instead live as route handlers inside `apps/web`. The moment there's real backend logic, give it its own `apps/api`.

---

## Heavy services — `apps/services/<name>`

One folder per service, each independently deployable. Reach here for AI/ML processing, embeddings, media transforms, long jobs, queue workers, or websockets — anything that doesn't belong on the serverless fast path.

**Choosing a language per service:**

- **TypeScript (Fastify)** — default. Use when the work is plain compute/IO and you want to share Zod schemas and types from `packages/shared` directly.
- **Python (FastAPI)** — when the ecosystem demands it: ML/AI inference, data science, native libraries (PyTorch, transformers, OpenCV, etc.). Validate every boundary with **Pydantic**.

```
apps/services/
├── ai-worker/                # Python + FastAPI — e.g. embeddings, inference
│   ├── app/
│   ├── pyproject.toml
│   └── .env.example          # mirrors this service's config
└── media/                    # Node + Fastify — e.g. image/video processing
    ├── src/
    ├── package.json
    └── tsconfig.json
```

**Crossing the language boundary:** TS services import contracts from `packages/shared/src/schemas/`. Python services define **Pydantic** models that mirror the same shapes — keep the field names and types identical so the HTTP contract holds. When a contract is shared across languages, treat the Zod schema in `packages/shared` as the source of truth and mirror it in Python by hand (or generate from a shared JSON Schema / OpenAPI doc).

---

## Frontend — Mobile (React Native + Expo)

- **Framework:** React Native with TypeScript
- **Toolchain:** Expo (SDK 52+), tested via **Expo Go** during development; **EAS Build** for distribution
- **Icons:** `lucide-react-native` + `react-native-svg` — always. Never use emojis.
- **Navigation:** Expo Router (file-based)
- **Data fetching:** **SWR** — keep it consistent with web
- **Global state:** **Redux Toolkit** when needed (same rule as web)

Bootstrap:
```bash
pnpm create expo-app apps/mobile --template tabs
```

---

## Database — PostgreSQL 18 + Drizzle + pgvector

Use **PostgreSQL 18** for relational data, with the **pgvector** extension for vector/semantic search. Define schema with **Drizzle ORM**. This is the default for everything — relational data *and* embeddings live in the same Postgres instance.

- **Local dev:** Postgres runs in Docker Compose (see below)
- **Production:** any managed PostgreSQL provider that supports the `pgvector` extension. Keep the app provider-agnostic — it only ever sees `DATABASE_URL`.

The Drizzle schema lives in `packages/shared` so both the web app and any other service share one source of truth:

```
packages/shared/
└── src/
    └── db/
        ├── schema.ts      # Drizzle table definitions
        ├── index.ts       # db client export
        └── migrations/    # drizzle-kit generated migrations
```

**schema.ts example**:
```typescript
import { pgTable, uuid, text, timestamp } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
})
```

**ID conventions:**

- Default to **UUIDv7** for all primary keys — sortable, globally unique, safe for distributed systems
- Exception: small lookup/normalization tables where the full set of rows is known, static, and typically fewer than ~10–20 entries (e.g. category, status, unit_type) may use a simple `serial` / `integer` ID. The rule of thumb: if a developer could plausibly hardcode all the IDs in the app without it feeling wrong, a serial ID is fine.

```typescript
import { pgTable, uuid, serial, text } from 'drizzle-orm/pg-core'

// Standard table — UUIDv7
export const products = pgTable('products', {
  id: uuid('id').primaryKey().$defaultFn(() => generateUUIDv7()),
  name: text('name').notNull(),
})

// Small lookup table — serial is fine
export const categories = pgTable('categories', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
})
```

Run migrations with `drizzle-kit`:
```bash
pnpm drizzle-kit generate
pnpm drizzle-kit migrate
```

### Vector search with pgvector

Default to **pgvector** for embeddings and semantic search — no extra service to run, and it sits right next to the relational data.

- Enable the extension once: `CREATE EXTENSION IF NOT EXISTS vector;`
- Store embeddings as a `vector(N)` column on the relevant table
- Add an index (`ivfflat` or `hnsw`) for similarity queries at scale

```typescript
import { pgTable, uuid, text, vector } from 'drizzle-orm/pg-core'

export const documents = pgTable('documents', {
  id: uuid('id').primaryKey().$defaultFn(() => generateUUIDv7()),
  content: text('content').notNull(),
  embedding: vector('embedding', { dimensions: 1536 }),
})
```

Reach for a dedicated vector database (e.g. **Qdrant** via `@qdrant/js-client-rest`) only when scale or workload genuinely outgrows pgvector — not by default.

---

## Databases — Docker Compose (local dev only)

Local development runs the database(s) in Docker Compose. Production uses a managed provider; Compose is **not** for prod. **Always name the Compose stack** with the project name to avoid conflicts with other running stacks.

```bash
docker compose -p <project-name> up -d
```

### docker-compose.yml template

Use the `pgvector` image so the extension is available locally out of the box:

```yaml
name: project-name   # <-- always set this

services:
  postgres:
    image: pgvector/pgvector:pg18
    restart: unless-stopped
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Add other services (e.g. Qdrant) only if the project actually uses them — don't include them by default.

---

## Type Safety

Follow the same rules as the `type-safety` skill:

- **Never use `as any`, `any`, or `// @ts-ignore`**
- **Zod** on every external boundary in TypeScript (route handler input/output, env vars, third-party API responses)
- **Pydantic** on every external boundary in Python (if a Python service is added)
- Types are inferred from schemas: `z.infer<typeof Schema>` — never write a duplicate `interface`
- Cross-service / cross-app contracts live in `packages/shared/src/schemas/`
- `tsconfig.json` always has `"strict": true`

**Env validation** (always in an `env.ts`, per app/service):
```typescript
import { z } from 'zod'

const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
})

export const env = EnvSchema.parse(process.env)
```

---

## Icons

- **Web:** `lucide-react`
- **Mobile:** `lucide-react-native` (requires `react-native-svg`)
- **Never** use emojis as icons or decorative elements — they are inconsistent across platforms

---

## Bootstrap Files

Every project must include these files to make it easy to set up anywhere:

| File | Purpose |
|------|---------|
| `infra/docker-compose.yml` | Local dev database services with a named stack |
| `.env` | Real secrets and config — **always at monorepo root**, never committed |
| `.env.example` | All required env vars with placeholder values (never real secrets) |
| `.gitignore` | At monorepo root — must include `.env` and common ignores |
| `README.md` | Setup instructions: install, start db, run dev, deploy to Vercel |
| `package.json` (root) | `dev`, `build`, `lint`, `typecheck` scripts wired across workspaces |

**Rules:**
- `.env` lives at the **monorepo root** — one file, not per-app
- `.env.example` must mirror every variable in every service's Zod `EnvSchema`. If a var is required in code, it must appear in `.env.example`
- `.gitignore` must always exist at root and at minimum include:

```gitignore
# Environment
.env
.env.local
.env.*.local

# Dependencies
node_modules/

# Build output
.next/
dist/
build/
.expo/

# Vercel
.vercel/

# Misc
.DS_Store
*.log
```

---

## File Organization

- Group files by **domain/feature**, not by type (avoid flat `components/`, `hooks/`, `utils/` folders at the root level)
- Keep files small and focused — one export per file for components
- Co-locate tests with source: `foo.ts` → `foo.test.ts`
- Shared code that crosses app boundaries goes in `packages/shared/`
- No barrel `index.ts` re-exports unless the package is a published library

---

## Checklist when scaffolding a new project

- [ ] `pnpm-workspace.yaml` defines all app, service, and package paths (`apps/*`, `apps/services/*`, `packages/*`)
- [ ] `apps/web` (UI) and `apps/api` (light API) exist; heavy work is split into `apps/services/<name>`
- [ ] Call direction holds: clients → `apps/api` → `apps/services/*` (frontend never calls a heavy service directly)
- [ ] `docker-compose.yml` uses the `pgvector/pgvector` image and has `name: <project-name>` set
- [ ] Production `DATABASE_URL` points at a managed Postgres with the `pgvector` extension
- [ ] `.env.example` covers all env vars used in code
- [ ] Zod `EnvSchema` validates env at startup in every app/service
- [ ] `tsconfig.json` has `strict: true` in every package
- [ ] Styling uses SCSS modules; SWR for fetching; Redux Toolkit only where cross-cutting state is real
- [ ] Lucide icons installed (not emojis)
- [ ] `README.md` with setup + Vercel deploy steps exists
- [ ] Root `package.json` has workspace-wide `dev`, `build`, `typecheck` scripts
