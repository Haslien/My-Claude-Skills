---
name: business-model-canvas
description: Guide users through creating and analyzing a Business Model Canvas (BMC) based on the Osterwalder framework. Use when the user wants to build, map, fill in, analyze, or discuss a business model canvas, business model generation, BMC, value proposition, customer segments, revenue streams, or any of the 9 building blocks.
---

# Business Model Canvas

Based on Alexander Osterwalder & Yves Pigneur, *Business Model Generation* (2010).

A **Business Model Canvas** describes the rationale of how an organization creates, delivers, and captures value — through nine building blocks covering four core areas: customers, offer, infrastructure, and financial viability.

## Canvas layout

```
┌─────────────┬──────────────┬──────────────┬──────────────┬─────────────┐
│  KP         │  KA          │  VP          │  CR          │  CS         │
│  Key        │  Key         │  Value       │  Customer    │  Customer   │
│  Partners   │  Activities  │  Propositions│  Relation-   │  Segments   │
│             ├──────────────┤              │  ships       │             │
│             │  KR          │              ├──────────────┤             │
│             │  Key         │              │  CH          │             │
│             │  Resources   │              │  Channels    │             │
├─────────────┴──────────────┴──────────────┴──────────────┴─────────────┤
│  C$  Cost Structure                │  R$  Revenue Streams               │
└────────────────────────────────────┴────────────────────────────────────┘
```

## The 9 building blocks

| # | Code | Name | Key question |
|---|------|------|--------------|
| 1 | CS | Customer Segments | Who are we creating value for? |
| 2 | VP | Value Propositions | What value do we deliver? |
| 3 | CH | Channels | How do we reach our customers? |
| 4 | CR | Customer Relationships | What relationship do we have with customers? |
| 5 | R$ | Revenue Streams | What are customers paying for? |
| 6 | KR | Key Resources | What assets do we need? |
| 7 | KA | Key Activities | What must we do? |
| 8 | KP | Key Partnerships | Who are our most important partners? |
| 9 | C$ | Cost Structure | What are the most important costs? |

## Instructions for Claude

### Approach

1. **Understand context first** — ask about the business/idea if it isn't clear what we're working on
2. **Work through the canvas systematically** — recommended order: CS → VP → CH → CR → R$ → KR → KA → KP → C$
3. **Push below the surface** — don't accept vague answers; ask follow-up questions
4. **Highlight connections** — the building blocks are tightly linked; flag contradictions and gaps
5. **Present visually** — always summarize with a complete canvas table at the end

### Recommended workflow

```
Start → Choose focus → Fill in one block at a time → Validate connections → Summarize
```

**Step 1 — Context clarification**
- What is the business/idea?
- Is this a new model (greenfield) or an analysis of an existing one?
- Are we going through the full canvas or focusing on specific blocks?

**Step 2 — Fill in the building blocks**
For each block, read the detail file and use the questions there:
- [Customer Segments](building-blocks/customer-segments.md)
- [Value Propositions](building-blocks/value-propositions.md)
- [Channels](building-blocks/channels.md)
- [Customer Relationships](building-blocks/customer-relationships.md)
- [Revenue Streams](building-blocks/revenue-streams.md)
- [Key Resources](building-blocks/key-resources.md)
- [Key Activities](building-blocks/key-activities.md)
- [Key Partnerships](building-blocks/key-partnerships.md)
- [Cost Structure](building-blocks/cost-structure.md)

**Step 3 — Validate connections**
Check that these links are consistent:
- VP ↔ CS: Does the value proposition solve a real problem for the customer segment?
- CH ↔ CS: Do the channels actually reach the customers?
- R$ ↔ VP: Are revenue streams tied to value customers actually pay for?
- KA + KR ↔ VP: Do we have the activities and resources needed to deliver the VP?
- C$ ↔ KA + KR: Does the cost structure reflect the most important activities and resources?

**Step 4 — Present the complete canvas**
Always summarize with a fully filled-in canvas table:

```
| Building Block      | Content                                      |
|---------------------|----------------------------------------------|
| Customer Segments   | ...                                          |
| Value Propositions  | ...                                          |
| Channels            | ...                                          |
| Customer Relat.     | ...                                          |
| Revenue Streams     | ...                                          |
| Key Resources       | ...                                          |
| Key Activities      | ...                                          |
| Key Partnerships    | ...                                          |
| Cost Structure      | ...                                          |
```

### Common pitfalls to avoid

- **CS too broad**: "Everyone" is not a segment — push for differentiation
- **VP without pain**: A value proposition must solve a concrete problem or fulfill a concrete need
- **Forgotten revenue streams**: Distinguish between one-time and recurring revenue
- **Missing cost picture**: KA and KR without a corresponding C$ is incomplete
- **Unbalanced model**: All nine blocks must fit together — one weak block can undermine the whole model

## Source material

Based on: *Business Model Generation*, Alexander Osterwalder & Yves Pigneur, Wiley 2010.
Full book available at `.claude/skills/business-model-canvas/Business-Model-Generation_By_Alexander-Osterwalder.pdf` — use the Read tool with `pages:` parameter to look up specific sections.

The 9 building blocks are described on pages 20–41 of the book.
