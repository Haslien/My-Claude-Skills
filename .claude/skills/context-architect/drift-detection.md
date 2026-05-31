# Drift Detection — Plan

> Status: exploratory. Not implemented. Decide whether to build, then how.

## The problem

`CONTEXT.md` files drift the moment the surrounding code moves. The skill auto-fires on structural changes inside one Claude session, but:

- A teammate commits new files without Claude in the loop → drift.
- Claude makes structural changes in another session and forgets to update the parent map → drift.
- A merge brings in a sibling branch's new folder → drift.
- Renames and deletions silently invalidate routes.

The agent has no cheap way to *notice* drift. Asking it to scan the tree on every session burns tokens and is slow. Worse: if the agent doesn't notice, it acts on a lying map and produces wrong work.

**Constraint:** any solution must not require the agent to scan files for changes. Detection must be deterministic and pre-computed; the agent only acts on a small, focused report.

---

## Core insight

This is exactly the **harness vs decision** split from the Liu et al. paper. ~98% of an agent system should be deterministic infrastructure; the model only handles the irreducibly judgmental part. Drift detection is mechanical:

- "What changed since the last sync?" — git knows.
- "Which `CONTEXT.md` files cover those changed paths?" — filesystem knows.
- "Is the change a structural one?" — heuristic on file-tree diff (added / removed / renamed paths).

None of those questions need a model. The model's job starts at: *given this drift report, rewrite these specific routes.*

---

## Three approaches, compared honestly

### A. Pure git mtime comparison (no metadata)

For each `CONTEXT.md`:
```
last_ctx_commit  = git log -1 --format=%H -- <path>/CONTEXT.md
last_folder_commit = git log -1 --format=%H -- <path>/
```
If `last_folder_commit` is newer than `last_ctx_commit` → potentially stale.

**Pros:** zero metadata to maintain. Works on any repo immediately. Easy to reason about.
**Cons:** noisy. Edits to *content* inside files in the folder mark the folder "newer" even when the map is still correct. False positives are common. The "structural change vs content change" filter has to happen at report-rendering time.

### B. Frontmatter sync hash

Each `CONTEXT.md` carries:
```yaml
---
synced_at: <commit-hash-or-date>
---
```
On a check, diff the folder against `synced_at` and report what's changed since.

**Pros:** explicit. Survives clones. Clearly distinguishes "I last verified this map at commit X" from "the file was last edited at commit Y." Lets the skill update *only* the timestamp when verifying a still-correct map.
**Cons:** more moving parts. Requires the skill to actually update the field every time it touches the map. Humans editing manually will forget.

### C. External manifest

One `.claude/skills/context-architect/state.json`:
```json
{ "src/api/CONTEXT.md": "a4f3b21", "src/web/CONTEXT.md": "b8c4d12" }
```
Centralized; one file to read.

**Pros:** quick scan; one file diff in PRs.
**Cons:** breaks on rename; centralized state rots; another file to keep in sync. Worst of both worlds.

### Recommendation

**Start with A. Move to B only if false positives become annoying.**

A is one script and zero schema changes. Most "newer commit in folder" cases will *also* be structural changes worth a one-line update — so the false positive rate is acceptable in practice. If it turns out to be noisy, B is a clean upgrade path: add a frontmatter field, fall back to mtime when missing.

C is rejected. Single-source-of-truth in a separate file always rots in a multi-contributor repo.

---

## What the script outputs (the drift report)

The output is a **prompt fragment** — small, focused, ready to paste or auto-load into a Claude session. Goal: ≤ 100 lines for typical repos.

```
DRIFT REPORT — generated 2026-05-08
Repo HEAD: 604c13f
3 folders flagged.

────────────────────────────────────
src/api/   (CONTEXT.md last touched 2 weeks ago, 12 commits behind)
  + added    src/api/webhooks.ts        a4f3b21  "feat: stripe webhooks"
  + added    src/api/billing.ts         b8c4d12  "feat: billing endpoints"
  - removed  src/api/legacy_auth.ts     d3e2f1a  "chore: remove deprecated"
  ! CONTEXT.md "Files in this folder" is missing webhooks.ts, billing.ts
  ! CONTEXT.md still lists legacy_auth.ts

src/components/forms/
  ~ renamed  TextField.tsx → InputField.tsx   c9d5e23
  ! CONTEXT.md still references TextField.tsx

src/utils/   (NEW FOLDER — no CONTEXT.md)
  + 5 new files since folder creation
  ! No CONTEXT.md exists in this folder
  ! Parent (src/CONTEXT.md) has no route to src/utils/
────────────────────────────────────

Recommended actions:
1. Update src/api/CONTEXT.md: replace legacy_auth row, add webhooks/billing.
2. Update src/components/forms/CONTEXT.md: rename row.
3. Bootstrap src/utils/CONTEXT.md and add a route from src/CONTEXT.md.
```

The agent reads this, acts on each item, done. No tree walk. No grep. No "is this map still correct?" pondering.

**Filtering rules (what the script omits):**
- Pure content edits inside an existing file → skip (the map describes roles, not contents).
- Whitespace, lockfile-only, comment-only commits → skip.
- Files matched by `.gitignore` → never tracked anyway.
- Ignored extensions (configurable): images, fonts, generated bundles.

The filter is the whole point — without it, every commit looks structural and the report becomes noise.

---

## Trigger options

| Trigger | Pros | Cons | Verdict |
|---|---|---|---|
| Manual: user runs `python check_drift.py` | Zero magic, easy to reason about | Humans forget | Ship as v1 |
| Slash command: `/context-architect-check` | Discoverable from inside Claude | Needs slash command setup | Nice v2 |
| Git pre-commit hook | Catches drift before it lands | Aggressive: blocks commits | Bad default. Optional opt-in. |
| Git post-commit hook | Warning, not blocker | Output is easy to miss | OK opt-in |
| Claude Code session-start hook | Auto-loads report into every session | Could bloat context if drift is large | Maybe v3 — add a size cap |
| CI on every PR | Team-scale enforcement | Needs CI infra | Right for shared repos |

Default plan: ship **manual + slash command** in v1. Hooks and CI are opt-in for teams that want them.

---

## Implementation sketch

A single Python script at `.claude/skills/context-architect/scripts/check_drift.py`:

```
1. Find all CONTEXT.md files (Glob).
2. For each, get its last-touched commit hash via `git log -1`.
3. For each, get the list of commits touching its folder since that hash.
4. For each such commit, get the file-tree diff (added/removed/renamed only).
5. Filter out content-only edits and ignored extensions.
6. For each CONTEXT.md, parse it lightly to find which file paths it references.
7. Cross-reference: which referenced paths no longer exist? which new paths aren't referenced?
8. Detect folders that are NEW (no CONTEXT.md) and have ≥ N files.
9. Render the report.
```

~150 lines of Python. No external deps beyond the stdlib (`subprocess` for git, `pathlib`, `re` for the lightweight CONTEXT.md parse).

The CONTEXT.md parse can be naive: extract every backtick-quoted filename and every markdown link target. Imperfect but enough.

---

## Where this fits in the skill

The script is **opt-in infrastructure**, not part of the skill's core flow. The skill's spine stays: fire on every structural change *during* a session. The drift script handles changes that happen *between* sessions or in *other* clients.

`SKILL.md` gets one new section, near the bottom:

```markdown
## Detecting drift between sessions

If the project may have changed since you last ran this skill (teammate commits,
another Claude session, a merge), run `scripts/check_drift.py` first. It outputs
a drift report listing exactly which CONTEXT.md files need attention. Act on the
report's recommendations, then proceed normally.
```

That's it. One paragraph. The rest of the skill stays unchanged.

---

## When this is overkill

Be honest: this script is most valuable when *one or more* of these holds:

- Multiple contributors push to the same repo.
- Long-running project (months+) where memory of "last sync" is unreliable.
- Active branching/merging — drift comes from sibling branches.
- The agent runs in CI and needs deterministic state.

For a solo developer on a young repo who runs `context-architect` reflexively while editing — the skill alone is enough. The script adds maintenance without much payoff.

So: **build it, but document it as optional**. Don't make the core skill depend on it.

---

## Open questions

1. **How to filter "structural" vs "content" changes precisely?** v1 heuristic: if `git log --name-status` shows only `M` (modified) entries inside files that already existed when CONTEXT.md was last touched, it's content-only. If there are any `A` / `D` / `R` entries, it's structural. Probably good enough.

2. **What about renames inside the report?** Git's rename detection is heuristic. Consider running `git log --follow --name-status` for the folder, or `git diff -M`. v1 can use `git log --name-status` and post-process; if quality is poor, switch to `git diff -M --find-renames`.

3. **How to handle a CONTEXT.md that was never committed?** Its "last commit" is null. Treat as: "needs initial review" — list it as bootstrap-pending.

4. **Should the report cap its own length?** Yes. If drift is huge (e.g. fresh fork with no maps), report says "too much drift to itemize — bootstrap is required" and points to Workflow A in the skill. Prevents context bloat from a runaway report.

5. **Should `synced_at` be added to CONTEXT.md frontmatter as preparation for v2?** No. Adding metadata that nothing reads is dead weight. Add it only when v2 is actually being built.

6. **How does this interact with branches?** Report is always against `HEAD`. On a feature branch, drift includes the branch's own changes — which is correct: those changes need their CONTEXT.md updates landed before merge.

---

## Decision points

Before building:

- [ ] Is approach A (pure git) acceptable for the false-positive rate, or should we start at B?
- [ ] Manual-only, or also ship a git post-commit hook template?
- [ ] Python or shell script? (Python: clearer, cross-platform. Shell: zero dependency but Windows-painful.)
- [ ] Where does the report go: stdout, a file in `output/`, or directly into Claude's context?

Recommendation for all four: **A, manual + optional hook template, Python, stdout (with optional `--out FILE`)**. Lowest friction, no decisions locked in.
