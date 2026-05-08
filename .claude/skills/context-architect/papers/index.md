# Papers Index — Context Architecture for AI Agents

Two foundational papers that motivate the `context-architect` skill. Both argue that **the structure surrounding the model matters more than the model itself**, but they reach this conclusion from opposite directions.

---

## 1. Interpretable Context Methodology: Folder Structure as Agent Architecture

**File:** [interpretable_context_methodology.pdf](interpretable_context_methodology.pdf)
**Authors:** Jake Van Clief, David McDermott (Eduba, University of Edinburgh) — March 2026
**Source:** [arXiv:2603.16021v1](https://arxiv.org/abs/2603.16021)
**Reference repo:** [Model-Workspace-Protocol-MWP](https://github.com/RinDig/Model-Workspace-Protocol-MWP-)
**Author talk (recommended for a quick start):** Jake Van Clief — ["Stop Building AI Agents. Use This Folder System Instead."](https://youtu.be/MkN-ss2Nl10) on YouTube. A more accessible walkthrough of the same ideas straight from the first author; useful if the paper is heavier than you need or you want to hear the motivation in plain language before reading.

### One-line thesis

Replace framework-level orchestration (LangChain, AutoGen, CrewAI) with **filesystem structure**: numbered folders are stages, plain markdown files carry the prompts, and one orchestrating agent reads the right files at the right moment.

### Why it matters for this skill

This paper is the **direct philosophical foundation** of the `context-architect` skill. It introduces:

- **The five-layer context hierarchy** (page 5, Figure 1) — the core mental model the skill operationalizes
- **Stage contracts** with explicit Inputs / Process / Outputs (page 9)
- **The factory/product distinction** between reference material (Layer 3) and working artifacts (Layer 4) (page 6, Table 2)
- **Layered context loading** as prevention of the "lost in the middle" problem (page 4)

### Key concepts and where to find them

| Concept | Page | Notes |
|---|---|---|
| Framework-vs-MWP comparison table | 2 (Table 1) | Ten dimensions where filesystem structure simplifies or constrains |
| Unix tradition & pipe-and-filter heritage | 2–3 | McIlroy, Kernighan/Pike, Parnas, Dijkstra — why this is "going backward to go forward" |
| Context engineering background | 3–4 | Karpathy's term, Lance Martin's write/select/compress/isolate taxonomy |
| MWP vs MCP distinction | 4 | MCP = how models reach external tools. MWP = how context is structured across stages. They compose. |
| **Five-layer hierarchy** | 5 (Figure 1) | Layer 0 (CLAUDE.md, ~800 tok) → Layer 1 (CONTEXT.md routing, ~300 tok) → Layer 2 (Stage CONTEXT.md, 200–500 tok) → Layer 3 (reference, 500–2k tok) → Layer 4 (working artifacts, varies) |
| Five design principles | 5 | One stage / one job · plain text interface · layered loading · every output is an edit surface · configure the factory not the product |
| **Layer 3 vs Layer 4 table** | 6 (Table 2) | Reference (stable, factory) vs working (per-run, ingredients) |
| Folder structure example | 7 (Figure 2) | Color-coded workspace tree |
| Token-budget composition by stage | 8 (Figure 3) | Each MWP stage uses 2k–8k tokens vs ~42k monolithic |
| Stage contract format | 9 (literal example) | The `## Inputs / ## Process / ## Outputs` template |
| Pipeline flow with review gates | 9 (Figure 4) | Where humans intervene between stages |
| Working implementations | 10–11 | Script-to-animation (3 stages), course deck (5 stages), workspace-builder |
| U-shaped intervention pattern | 12–13 (Figure 5) | Heavy editing at stage 1 (direction) and final stage (alignment); light at middle |
| Where MWP works / does not work | 14 | Sequential reviewable workflows yes; real-time multi-agent or high-concurrency no |
| Multi-pass compilation analogy | 16 | Each stage = one compiler pass with a defined intermediate representation |
| Edit-source vs edit-output principle | 17–18 | Recurring output edits should propagate back to the stage contract or reference files |

### What the skill takes from this paper

- The **five-layer mental model** is the spine of the skill
- The **stage contract template** (`## Inputs / ## Process / ## Outputs`) is reused literally
- The **Reference vs Working separation** drives the folder layout the skill produces
- The **routing-vs-content distinction** is why the skill writes `CONTEXT.md` files (routing) separately from `references/*.md` (content)

---

## 2. Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems

**File:** [dive_into_claude_code.pdf](dive_into_claude_code.pdf)
**Authors:** Jiacheng Liu, Xiaohan Zhao, Xinyi Shang, Zhiqiang Shen (VILA Lab, MBZUAI; UCL) — April 2026
**Source:** [arXiv:2604.14228v1](https://arxiv.org/abs/2604.14228)
**Companion repo:** [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)

### One-line thesis

A source-level analysis of Claude Code v2.1.88 (~512K LOC) showing that ~98.4% of the codebase is operational harness and only ~1.6% is decision logic — the model is given broad latitude inside a dense deterministic infrastructure.

### Why it matters for this skill

This paper is **secondary context** for the skill. It is less about how to structure folders and more about why context architecture is load-bearing in the first place: it documents how a real production agent treats the context window as the binding resource and what it costs when that fails.

### Key concepts and where to find them

| Concept | Page | Notes |
|---|---|---|
| Five values + thirteen design principles | 3–4 | Human authority, safety, reliability, capability amplification, contextual adaptability |
| Where reasoning lives (model vs harness split) | 6 | Model emits `tool_use` blocks; harness validates and executes |
| Context as the binding resource | 6 | "The five-layer pipeline exists because no single compaction strategy addresses all types of context pressure" |
| **Five-layer compaction pipeline** | 11–12, 20 | Budget reduction → snip → microcompact → context collapse → auto-compact |
| **CLAUDE.md four-level hierarchy** | 19–20 | Managed → user → project → local memory; `@include` directive for modular instruction sets |
| Context window assembly (9 sources) | 18 | System prompt, environment info, CLAUDE.md, path-scoped rules, auto memory, tool metadata, history, tool results, compact summaries |
| Stage-specific context loading argument | 4 (cited from Liu et al.) | "Lost in the middle" — irrelevant context degrades model performance |
| Sub-agent isolation and summary-only return | 22–24 | Subagents get isolated contexts; only a summary returns to the parent — the same insight that justifies MWP's stage boundaries |
| OpenClaw architectural contrast | 24–27 | Same questions, different answers when deployment context changes |
| Memory as a first-class subsystem | 31, 33 | Future direction: experiential memory beyond per-session CLAUDE.md |
| Architectural decoupling (Managed Agents) | 31 | Sessions, harness, sandbox virtualized as independent interfaces |
| Empirical predictions about bounded context | 30 | Architecturally predicts higher pattern-duplication and convention-drift rates |

### What the skill takes from this paper

- **Validation that bounded context is the binding constraint** — every layer of the skill's output exists to load less but more relevant context
- **CLAUDE.md as Layer 0** — the four-level memory hierarchy (managed → user → project → local) is exactly the role MWP assigns to Layer 0
- **Subagent summary-only return** — supports the skill's recommendation to keep `output/` folders narrow (only the artifacts the next stage needs)
- **Vocabulary** — terms like *deny-first*, *graduated trust*, *append-only*, *lazy loading*, *context shapers* show up implicitly in the skill's recommendations

---

## How the two papers compose

The MWP paper says: **structure the filesystem so the model gets the right context at each stage.**
The Claude Code paper says: **bounded context is the binding resource and Claude Code already has CLAUDE.md as Layer 0.**

Together they imply a workflow that:

1. Treats existing `CLAUDE.md` (Claude Code's mechanism) as Layer 0
2. Adds `CONTEXT.md` files at workspace root (Layer 1) and per-stage (Layer 2) following MWP
3. Separates `references/` (Layer 3, stable) from `output/` (Layer 4, per-run)
4. Lets the same Claude Code agent read the right layer at the right moment without any new framework

That workflow is the `context-architect` skill.
