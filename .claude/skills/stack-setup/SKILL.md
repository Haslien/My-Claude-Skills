---
name: stack-setup
description: Scaffold or set up our standard monorepo stack. Use when starting a new project, adding a new service, or when the user asks to set up a stack. Stack includes: pnpm monorepo, React+Vite (web), React Native+Expo (mobile), Fastify (backend), PostgreSQL 18+Drizzle, MongoDB, Qdrant, Docker Compose for databases, Zod/Pydantic strict typing, Lucide React icons.
---

# Standard Project Stack

This skill governs how we set up and scaffold projects. Apply these conventions whenever starting a new project, adding a service, or scaffolding infrastructure — unless the user explicitly overrides a specific choice.

---

## Monorepo Layout

Use **pnpm workspaces**. All projects are monorepos unless explicitly told otherwise.

```
project-name/
├── apps/
│   ├── web/          # React + Vite
│   ├── mobile/       # React Native + Expo
│   └── api/          # Fastify backend
├── packages/
│   └── shared/       # Shared Zod schemas, types, utils
├── infra/
│   └── docker-compose.yml
├── package.json      # pnpm workspace root
└── pnpm-workspace.yaml
```

**pnpm-workspace.yaml**:
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

Root `package.json` should have `"private": true` and workspace-level dev dependencies (TypeScript, ESLint, Prettier).

---

## Frontend — Web (React + Vite)

- **Framework:** React 18+ with TypeScript
- **Bundler:** Vite
- **Icons:** `lucide-react` — always. Never use emojis as icons or decorative elements.
- **Styling:** Tailwind CSS (default) unless another system is requested
- **Data fetching:** TanStack Query (React Query)
- **Routing:** TanStack Router or React Router v7

Bootstrap:
```bash
pnpm create vite apps/web --template react-ts
```

---

## Frontend — Mobile (React Native + Expo)

- **Framework:** React Native with TypeScript
- **Toolchain:** Expo (SDK 51+), tested via **Expo Go** during development
- **Icons:** `lucide-react-native` + `react-native-svg` — always. Never use emojis.
- **Navigation:** Expo Router (file-based)
- **Data fetching:** TanStack Query

Bootstrap:
```bash
pnpm create expo-app apps/mobile --template tabs
```

---

## Backend — Fastify

- **Framework:** Fastify with TypeScript
- **Validation:** Zod schemas on every route (request body, query params, response)
- **Structure:**

```
apps/api/
├── src/
│   ├── index.ts          # Entry point, server bootstrap
│   ├── routes/           # Route handlers grouped by domain
│   ├── plugins/          # Fastify plugins (auth, db, etc.)
│   ├── services/         # Business logic
│   ├── schemas/          # Zod schemas for this service
│   └── env.ts            # Zod-validated env config
├── package.json
└── tsconfig.json
```

**Env validation** (always in `env.ts`):
```typescript
import { z } from 'zod'

const EnvSchema = z.object({
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  MONGODB_URL: z.string().url().optional(),
})

export const env = EnvSchema.parse(process.env)
```

**Route example** with Zod:
```typescript
import { z } from 'zod'
import { zodToJsonSchema } from 'zod-to-json-schema'

const BodySchema = z.object({ name: z.string().min(1) })
const ReplySchema = z.object({ id: z.string(), name: z.string() })

fastify.post('/items', {
  schema: {
    body: zodToJsonSchema(BodySchema),
    response: { 201: zodToJsonSchema(ReplySchema) },
  },
  async handler(req) {
    const body = BodySchema.parse(req.body)
    // ...
  },
})
```

---

## Databases — Docker Compose

All databases run in Docker Compose. **Always name the Compose stack** using the project name to avoid conflicts with other running stacks.

```bash
docker compose -p <project-name> up -d
```

Or set `name:` at the top of `docker-compose.yml`:

```yaml
name: project-name   # <-- always set this
```

### docker-compose.yml template

```yaml
name: project-name

services:
  postgres:
    image: postgres:18-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mongodb:
    image: mongo:7
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: app
      MONGO_INITDB_ROOT_PASSWORD: secret
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  qdrant:
    image: qdrant/qdrant:latest
    restart: unless-stopped
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  postgres_data:
  mongo_data:
  qdrant_data:
```

Only include the databases the project actually uses. Don't add all three by default — ask or infer from context.

---

## PostgreSQL 18 + Drizzle ORM

Use **PostgreSQL 18** for relational data. Define schema with **Drizzle ORM**.

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

---

## MongoDB

Use for document-based storage. Use **Mongoose** or the native `mongodb` driver with Zod validation on top.

Always define a Zod schema for any document shape before writing queries — never use raw untyped documents.

---

## Qdrant

Use for vector/semantic search. Connect via the `@qdrant/js-client-rest` SDK. Define collection schemas explicitly on startup.

---

## Type Safety

Follow the same rules as the `type-safety` skill:

- **Never use `as any`, `any`, or `// @ts-ignore`**
- **Zod** on every external boundary in TypeScript (API input/output, env vars, API responses)
- **Pydantic** on every external boundary in Python (if a Python service is added)
- Types are inferred from schemas: `z.infer<typeof Schema>` — never write a duplicate `interface`
- Cross-service contracts live in `packages/shared/src/schemas/`
- `tsconfig.json` always has `"strict": true`

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
| `infra/docker-compose.yml` | All database services with named stack |
| `.env` | Real secrets and config — **always at monorepo root**, never committed |
| `.env.example` | All required env vars with placeholder values (never real secrets) |
| `.gitignore` | At monorepo root — must include `.env` and common ignores |
| `README.md` | Setup instructions: install, start db, run dev |
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
dist/
build/
.expo/

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

- [ ] `pnpm-workspace.yaml` defines all app and package paths
- [ ] `docker-compose.yml` has `name: <project-name>` set
- [ ] `.env.example` covers all env vars used in code
- [ ] Zod `EnvSchema` validates env at startup in every service
- [ ] `tsconfig.json` has `strict: true` in every package
- [ ] Lucide icons installed (not emojis)
- [ ] `README.md` with setup steps exists
- [ ] Root `package.json` has workspace-wide `dev`, `build`, `typecheck` scripts
