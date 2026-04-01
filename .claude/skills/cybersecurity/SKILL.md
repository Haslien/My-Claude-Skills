---
name: cybersecurity
description: Perform a structured security audit of a codebase. Use when the user asks for a security review, security analysis, vulnerability scan, sikkerhet, sikkerhetsanalyse, or wants to find security issues. Covers secrets in git history, authentication flaws, injection vulnerabilities, file uploads, rate limiting, inter-service auth, database security, mobile app security, web security, infrastructure, dependencies (CVE scan), and GDPR compliance.
---

# Cybersecurity Audit

Structured security audit for web/mobile/backend codebases. Produces a phased plan, executes parallel analysis across all attack surfaces, and delivers a prioritized report with remediation steps.

## Quick start

```
/cybersecurity
```

Claude will:
1. Explore the codebase and create a tailored audit plan
2. Run parallel analysis across all 12 phases
3. Deliver a full report with Critical/High/Medium/Low findings

---

## Instructions

### Phase 0: Explore and Plan

Before any analysis, explore the repo structure and create a written audit plan.

1. Read key files to understand the stack:
   - `package.json` / `pyproject.toml` — what frameworks/deps
   - `docker-compose*.yml` — infrastructure
   - Auth-related files (middleware, guards, JWT config)
   - `.env.example` — what secrets are expected
   - `README.md` / `CLAUDE.md` — project context

2. Run `git ls-files | head -100` to understand what's tracked in git.

3. Create `docs/cybersecurity/security_audit_plan.md` with:
   - Tailored checklist based on the actual stack
   - Which files to analyze per phase
   - Known risk areas based on architecture

4. **Stop and confirm with the user before proceeding to analysis.**

---

### Phase 1–12: Execute Analysis (in parallel)

Once the user confirms, launch parallel agents for each group of phases. See [checklist.md](checklist.md) for the full per-phase checklist.

**Group A — Authentication & Secrets (run together)**
- Phase 1: Secrets & credential management
- Phase 2: Authentication & authorization

**Group B — API Surface (run together)**
- Phase 3: Input validation & injection
- Phase 4: File upload security
- Phase 5: Rate limiting & DoS protection

**Group C — Infrastructure (run together)**
- Phase 6: Inter-service communication
- Phase 7: Database security
- Phase 10: Infrastructure & deployment

**Group D — Client & Compliance (run together)**
- Phase 8: Mobile app security (if applicable)
- Phase 9: Web application security (if applicable)
- Phase 11: Third-party dependencies (run `pnpm audit` / `npm audit` / `pip-audit`)
- Phase 12: GDPR & data privacy

---

### Phase 13: Compile Report

Write `docs/cybersecurity/security_audit_report.md` with this structure:

```markdown
# Security Audit Report

## Summary
Total X findings: Y Critical, Z High, ...

## Critical Findings
### C-1: [Title]
**File:** path/to/file:line
**Risk:** What can happen
**Fix:** Exact steps to remediate

## High Findings
...

## Prioritized Action Plan
| Priority | Action | Finding |
|---|---|---|
| 1 | ... | C-1 |

## Positive Findings
What is already well-implemented.
```

---

## Most common issues in vibe-coded projects

These are the patterns that appear most often. Always check these first:

### 1. Secrets in git history — the most common critical issue

**What to look for:**
```bash
# Files tracked that should not be
git ls-files | grep -E "\.env$|\.env\.|settings\.local"

# Secrets in commit history
git log --all -S "password" --oneline
git log --all -S "API_KEY" --oneline
git log --all -S "secret" --oneline

# Check tool config files for inline credentials
# Common culprits: .claude/settings.local.json, .vscode/settings.json,
# scripts/*.sh, docs/architecture/*.md, Makefiles
grep -r "password\|secret\|api_key\|mongodb+srv\|postgresql://" \
  --include="*.md" --include="*.sh" --include="*.json" \
  --exclude-dir=node_modules .
```

**Remediation if found:**
```bash
# 1. Rotate the credential immediately (before anything else)

# 2. Remove from git tracking
echo "the-file" >> .gitignore
git rm --cached the-file
git commit -m "chore: stop tracking secrets file"

# 3. Scrub git history with BFG
brew install bfg
bfg --delete-files filename --no-blob-protection
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force --all

# 4. Verify clean
git log --all -S "the-secret-value" --oneline  # must return nothing
```

---

### 2. Hardcoded fallback secrets

```typescript
// DANGEROUS — attacker can forge tokens if env var missing
secret: process.env.JWT_SECRET || "fallback-value-in-source-code"

// SAFE — fail fast
if (!process.env.JWT_SECRET) throw new Error("JWT_SECRET is required")
secret: process.env.JWT_SECRET
```

---

### 3. Unauthenticated internal services

Workers, background jobs, and internal APIs are often deployed without authentication because "they're internal." In cloud environments (Cloud Run, Lambda, etc.) they're often publicly reachable.

Check for:
- Cloud Run / Lambda functions with "allow unauthenticated"
- Pub/Sub push endpoints that don't verify the OIDC token
- `/test/*` or `/debug/*` routes active in production
- Internal HTTP endpoints reachable from the internet

---

### 4. CORS misconfiguration

```typescript
// DANGEROUS with credentials: true
origin: process.env.CORS_ORIGIN || true  // "true" = allow all

// SAFE
origin: process.env.CORS_ORIGIN  // fail if not set, never default to *
```

---

### 5. IDOR in shared resources

When users can share resources (groups, projects, teams), always verify:
- Does the user OWN the resource being added to the shared context?
- Can a member with editor access perform actions on resources they don't own?

```typescript
// DANGEROUS — checks group access but not receipt ownership
await addReceiptToGroup(groupId, receiptId, userId)

// SAFE — verify ownership first
const receipt = await getReceipt(receiptId)
if (receipt.owner_id !== userId) throw new ForbiddenError()
await addReceiptToGroup(groupId, receiptId, userId)
```

---

### 6. No token revocation

JWT-only auth with no server-side session state means:
- Logout is a no-op (token stays valid until expiry)
- Suspended users keep access until token expires
- Stolen tokens cannot be invalidated

Fix: Use short-lived access tokens (15–60 min) + rotating refresh tokens stored server-side.

---

### 7. GDPR promises not implemented

Privacy policies often promise features that haven't been built:
- "You can delete your account" — is the endpoint implemented? Does it delete GCS/S3 files too?
- "You can export your data" — is there a `GET /users/me/export` endpoint?
- "We delete your data after X days" — is there a cron job or lifecycle rule?

---

### 8. Dependency vulnerabilities

```bash
# Node.js
pnpm audit              # or: npm audit
pnpm audit --fix        # auto-fix where possible

# Python
pip-audit               # install: pip install pip-audit

# Filter to production only
pnpm audit --prod
```

Pay special attention to: web frameworks (fastify, express, django), image processing (sharp, pillow), archive handling (tar, zipfile), and auth libraries.

---

### 9. Supply chain attacks via unpinned dependencies

Popular packages get compromised. A malicious actor gains access to a maintainer's npm account and publishes a patch version containing a Remote Access Trojan. Every project using `"^x.y.z"` silently installs it on the next `npm install` — on developer machines, CI servers, and production deployments. Real examples: `event-stream` (2018), `colors`/`faker` (2022), `axios` (2026).

**The three symbols that enable this attack:**
```
"axios": "^1.7.0"  ← auto-installs any 1.x.x — a malicious 1.7.1 lands silently
"axios": "~1.7.0"  ← auto-installs any 1.7.x — slightly less exposure, still risky
"axios": "*"       ← installs anything — never in production
"axios": "1.7.0"   ← exact pin — only updates when you consciously change it ✅
```

**Check your project for unpinned versions:**
```bash
grep -r '"[^"]*": "[\^~>*]' --include="package.json" --exclude-dir=node_modules .
```

**The lock file is your second line of defense — but only if CI enforces it:**
```bash
pnpm install --frozen-lockfile  # fails if lock file doesn't match package.json
npm ci                           # same for npm
```

Without `--frozen-lockfile` in CI, a local `npm install` after a compromise updates the lock file — and the malicious version ships unnoticed.

**Recommended practice:**
- Pin all direct production dependencies to exact versions (no `^` or `~`)
- Commit the lock file and enforce it in CI with `--frozen-lockfile` / `npm ci`
- Use Dependabot or Renovate for controlled, reviewed version bumps (not auto-merge)
- Prefer native APIs when available — `fetch` over `axios`, `crypto` over custom libs
- Subscribe to advisories: [npmjs.com/advisories](https://www.npmjs.com/advisories), [osv.dev](https://osv.dev)

---

## Severity definitions

| Grade | Description | SLA |
|---|---|---|
| **Critical** | Directly exploitable, immediate data breach or takeover risk | Fix today |
| **High** | Exploitable with moderate effort, significant impact | Fix within days |
| **Medium** | Requires specific conditions, moderate impact | Fix within weeks |
| **Low** | Best practice gap, low direct impact | Fix at next maintenance |
| **Info** | Observation or positive finding | No action required |

---

## OWASP Top 10 coverage

Ensure the audit covers at minimum:

| OWASP | Check |
|---|---|
| A01 Broken Access Control | IDOR, privilege escalation, missing auth on endpoints |
| A02 Cryptographic Failures | Hardcoded secrets, weak hashing, plaintext storage |
| A03 Injection | SQL injection, NoSQL injection, command injection |
| A04 Insecure Design | Missing rate limits, no token revocation, logic flaws |
| A05 Security Misconfiguration | CORS, CSP, security headers, debug endpoints |
| A06 Vulnerable Components | `pnpm audit`, outdated deps with known CVEs |
| A07 Auth Failures | Weak JWT config, no refresh rotation, brute force |
| A08 Data Integrity | Unsigned OTA updates, unverified Pub/Sub messages |
| A09 Logging Failures | Sensitive data in logs, no audit trail |
| A10 SSRF | User-controlled URLs passed to server-side fetches |

---

## Output

Produces two files:
- `docs/cybersecurity/security_audit_plan.md` — phased checklist (created before analysis)
- `docs/cybersecurity/security_audit_report.md` — full findings report (created after analysis)

For detailed per-phase checklists, see [checklist.md](checklist.md).
