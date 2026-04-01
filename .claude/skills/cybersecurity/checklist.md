# Cybersecurity Audit Checklist

Per-phase checklist for the cybersecurity audit skill. Use this during analysis to ensure complete coverage.

---

## Phase 1: Secrets & Credential Management

**Files to check:**
- `.env`, `.env.*`, `.env.example`
- `.gitignore` — is it properly excluding sensitive files?
- `docker-compose*.yml` — hardcoded env vars, volume mounts
- All Dockerfiles — ARG/ENV with secrets, multi-stage leaks
- Tool configs: `.claude/settings.local.json`, `.vscode/settings.json`, `Makefile`, scripts
- Documentation: `docs/**/*.md` — credentials in examples?

**Checks:**
- [ ] Run `git ls-files | grep -E "\.env"` — tracked .env files?
- [ ] Run `git log --all -S "password" --oneline` — passwords in history?
- [ ] Run `grep -r "postgresql://\|mongodb+srv://\|redis://" --include="*.md" --include="*.sh" .` — DB URIs in docs?
- [ ] Is `.env` in `.gitignore`? Does the pattern actually match the file?
- [ ] Are there hardcoded fallback secrets in code (`|| "fallback"` pattern)?
- [ ] Is there a secrets manager, or are all secrets in env vars?
- [ ] Are there leaked API keys in architecture docs or deployment guides?
- [ ] Is VPS/server IP in tracked files? (reveals attack target)
- [ ] Are there CI/CD secrets in workflow files?

---

## Phase 2: Authentication & Authorization

**Files to check:**
- Auth middleware / guards / decorators
- Login, token exchange, refresh, logout routes
- User schema / model
- Protected route definitions
- Any "admin" or "demo" access mechanisms

**Checks:**
- [ ] JWT secret — hardcoded fallback or fail-fast?
- [ ] JWT access token lifetime — is it longer than 1 hour?
- [ ] Refresh token — is it rotated on use? Can it be revoked?
- [ ] Logout — does it invalidate tokens server-side, or is it a no-op?
- [ ] Are JWT claims (role, status) validated against DB on each request, or trusted from token?
- [ ] Can a user escalate their own role/permissions via profile update?
- [ ] IDOR: Can user A access user B's resources by guessing IDs?
- [ ] Shared resources (groups, teams): does membership grant access to resources the member doesn't own?
- [ ] Demo/test accounts — are passwords hashed? Timing-safe comparison?
- [ ] Brute force protection on auth endpoints (stricter than global rate limit)?
- [ ] OAuth PKCE — is state parameter validated? Is code verifier random enough?
- [ ] Are suspended/deleted users denied access immediately, or on next token expiry?

---

## Phase 3: Input Validation & Injection

**Files to check:**
- All API route handlers
- Search/query endpoints (highest injection risk)
- Database query builders

**Checks:**
- [ ] Are all request bodies validated with a schema (Zod, Joi, Pydantic, etc.)?
- [ ] Are path parameters validated (UUID format, not just non-empty string)?
- [ ] Are query parameters bounded (max page size, whitelisted sort fields)?
- [ ] Raw SQL: are all user values parameterized (no string interpolation)?
- [ ] MongoDB: any `$where`, `$regex`, or `$function` operators with user input?
- [ ] LIKE/ILIKE queries: are wildcards (`%`, `_`) escaped in user input?
- [ ] Search endpoints: can they be used for user enumeration?
- [ ] Are Content-Type headers validated on all endpoints?
- [ ] Is there prototype pollution risk in JSON object merging?
- [ ] Are GraphQL queries (if used) depth-limited and cost-analyzed?

---

## Phase 4: File Upload Security

**Files to check:**
- Upload route handlers
- File processing services (image resize, PDF parse, etc.)
- Cloud storage integration

**Checks:**
- [ ] Is file type validated by magic bytes, not just Content-Type header (client-controlled)?
- [ ] Are SVG uploads allowed? (Can contain JavaScript)
- [ ] Is there a file size limit enforced at multiple layers (app + reverse proxy)?
- [ ] Are uploaded files stored with predictable names? (IDOR via filename)
- [ ] Can filenames contain path traversal sequences (`../`)?
- [ ] Can a user overwrite another user's files?
- [ ] Is image processing safe from decompression bombs? (set pixel limits)
- [ ] Are cloud storage signed URLs time-limited and read-only?
- [ ] Is there malware scanning on uploads?

---

## Phase 5: Rate Limiting & DoS Protection

**Files to check:**
- Server setup / middleware configuration
- Nginx / reverse proxy config
- Auth and upload endpoints specifically

**Checks:**
- [ ] Is rate limiting per-IP only, or also per-user/account?
- [ ] Are auth endpoints rate-limited more strictly than general endpoints?
- [ ] Are file upload endpoints rate-limited separately?
- [ ] Are expensive operations (AI calls, DB aggregations) rate-limited?
- [ ] Nginx burst config — is `nodelay` appropriate, or does it allow burst attacks?
- [ ] Are there connection timeouts and keep-alive limits?
- [ ] Are there defined memory/CPU limits per request?
- [ ] Is there protection against slow-body attacks (slowloris)?

---

## Phase 6: Inter-Service Communication

**Files to check:**
- Message queue / Pub/Sub consumers
- Internal HTTP clients
- Service mesh / API gateway config
- Docker network config

**Checks:**
- [ ] Do internal services (workers, lambdas) require authentication?
- [ ] Are message queue push endpoints (Pub/Sub, SNS, etc.) verifying the source?
- [ ] Are `/test/*`, `/debug/*`, or `/admin/*` endpoints disabled in production?
- [ ] Is internal traffic TLS-encrypted, or is it trusted on a private network?
- [ ] Are message payloads validated (not just assumed trusted because "internal")?
- [ ] Is Docker/K8s network segmented so services can't reach each other freely?
- [ ] Are there any services bound to `0.0.0.0` that should be internal-only?
- [ ] Is there a dead letter queue to prevent message processing loops?

---

## Phase 7: Database Security

**Files to check:**
- Database client initialization
- Schema definitions
- Migration files
- Seed scripts

**Checks:**
- [ ] Are DB connections TLS-encrypted (explicit SSL config, not just assumed)?
- [ ] Are DB credentials rotated? Are there multiple credential sets in history?
- [ ] Is Row-Level Security (RLS) used, or is access control app-layer only?
- [ ] Is PII (email, phone, DOB) encrypted at the column level?
- [ ] Are passwords hashed with a proper KDF (bcrypt, argon2, scrypt)?
- [ ] Are password reset codes hashed (not stored plaintext)?
- [ ] Is there a soft-delete or audit trail for sensitive data changes?
- [ ] Do DB migrations contain destructive operations (DROP TABLE, TRUNCATE)?
- [ ] Is the DB accessible from the internet, or only from the app network?
- [ ] Are backups encrypted and access-controlled?
- [ ] Is there connection pooling with appropriate limits?

---

## Phase 8: Mobile App Security

**Files to check:**
- App config (`app.json`, `Info.plist`, `AndroidManifest.xml`)
- Auth token storage
- API client
- Deep link / URL scheme handling
- Build config (`eas.json`, `gradle.properties`)

**Checks:**
- [ ] `NSAllowsArbitraryLoads: true`? (iOS ATS disabled — Apple may reject)
- [ ] Are tokens stored in Keychain/Keystore (not AsyncStorage / SharedPreferences)?
- [ ] Is certificate pinning implemented?
- [ ] Are there hardcoded secrets or API keys in the JS/native bundle?
- [ ] Deep links: can a malicious app intercept the OAuth callback scheme?
- [ ] Is PKCE state validated on OAuth callback?
- [ ] Is there a token refresh race condition (no mutex for concurrent 401s)?
- [ ] Are OTA updates (Expo, CodePush) code-signed?
- [ ] Is sensitive data logged via `console.log` in production builds?
- [ ] Are Android permissions minimal (no unnecessary CAMERA, RECORD_AUDIO, etc.)?
- [ ] Is screen capture protection enabled on sensitive screens?
- [ ] Is there jailbreak/root detection (if required by data sensitivity)?

---

## Phase 9: Web Application Security

**Files to check:**
- `index.html` — CSP meta tags, external scripts
- Nginx/server config — security headers
- Components that render user content
- Form submission handlers

**Checks:**
- [ ] Is Content-Security-Policy set (header or meta tag)?
- [ ] Is `X-Content-Type-Options: nosniff` set?
- [ ] Is `X-Frame-Options: DENY` (or `SAMEORIGIN`) set?
- [ ] Is `Referrer-Policy` set?
- [ ] Is `Permissions-Policy` set?
- [ ] Is HSTS set with `includeSubDomains` (and `preload` if possible)?
- [ ] Is there any `dangerouslySetInnerHTML` with user content?
- [ ] Is user-supplied markdown/HTML rendered safely (no `rehype-raw` with untrusted input)?
- [ ] Are CSRF tokens used on state-changing forms?
- [ ] Are cookies set with `HttpOnly`, `Secure`, `SameSite=Strict`?
- [ ] Are external scripts loaded with Subresource Integrity (SRI)?
- [ ] Is there an open redirect vulnerability?
- [ ] Is sensitive data in the frontend JS bundle (API keys, internal URLs)?

---

## Phase 10: Infrastructure & Deployment

**Files to check:**
- All Dockerfiles
- `docker-compose.prod.yml`
- Nginx / reverse proxy config
- CI/CD pipeline files
- Deployment scripts

**Checks:**
- [ ] Do containers run as non-root? (check for `USER` directive)
- [ ] Are base images pinned to digest or specific version? (not `:latest`)
- [ ] TLS config: are deprecated protocols disabled (`ssl_protocols TLSv1.2 TLSv1.3`)?
- [ ] Are modern cipher suites configured?
- [ ] Is OCSP stapling enabled?
- [ ] Is HSTS preload configured?
- [ ] Is the Docker socket mounted anywhere? (`/var/run/docker.sock`)
- [ ] Are SSH keys or deploy credentials in the repo?
- [ ] Is there a CI/CD pipeline? Are secrets stored in CI secrets (not hardcoded)?
- [ ] Are security headers applied to ALL server blocks (not just API)?
- [ ] Is there automated security scanning (Dependabot, Snyk, Trivy)?
- [ ] Are there health check endpoints that leak version/env info?
- [ ] Is server IP exposed in docs, scripts, or commit messages?

---

## Phase 11: Third-Party Dependencies

**Commands to run:**
```bash
# Node.js / pnpm
pnpm audit
pnpm audit --prod   # production only

# Node.js / npm
npm audit

# Python
pip-audit

# Docker images
trivy image myapp:latest
```

**Checks:**
- [ ] Any Critical or High CVEs in production dependencies?
- [ ] Are security-critical packages on latest minor version? (fastify, express, django, sharp)
- [ ] Are there unnecessary dependencies increasing attack surface?
- [ ] Is the lock file committed and integrity-checked?
- [ ] Are there typosquatted package names? (similar to common packages)
- [ ] Are there `overrides`/`resolutions` pinning vulnerable transitive deps?
- [ ] Are dev dependencies kept strictly out of production images?
- [ ] Are direct dependencies pinned to exact versions (`"1.2.3"` not `"^1.2.3"`)? Ranges allow automatic install of a compromised patch release.
- [ ] Is the lock file (`pnpm-lock.yaml`, `package-lock.json`, `poetry.lock`) committed and verified? A missing or tampered lock file means unverified versions get installed.
- [ ] Subscribe to security advisories for your core packages (GitHub Dependabot, `npm security advisories`, OSV.dev)?

---

## Phase 12: GDPR & Data Privacy

**Files to check:**
- Privacy policy / terms of service
- User deletion endpoint
- Data export endpoint
- Analytics setup (PostHog, Mixpanel, GA)
- Session/log storage
- All PII field definitions in DB schema

**Checks:**
- [ ] Is there a "delete my account" endpoint? Does it delete ALL user data (including cloud storage files)?
- [ ] Is there a "export my data" endpoint (GDPR Art. 20)?
- [ ] Is user consent tracked (which version of policy was accepted, when)?
- [ ] Is there a mechanism to re-collect consent when the privacy policy changes?
- [ ] Is PII (email, phone, DOB) encrypted at rest or just DB-level encryption?
- [ ] Are IP addresses stored? If so, is there a retention/deletion policy?
- [ ] Is analytics configured for GDPR compliance (EU hosting, IP anonymization)?
- [ ] Does the privacy policy accurately describe what is actually implemented?
- [ ] Are there data retention promises (e.g., "deleted after 90 days") with actual implementation (cron job / lifecycle rule)?
- [ ] Are third-party processors covered by Data Processing Agreements (DPAs)?
- [ ] Is the legal basis for each processing activity documented?
- [ ] Are child safety provisions in place if minors might use the product?
