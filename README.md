# `soul-template/` — the actor bundle (PRD §3.2)

This is a **template** of the duck's durable identity bundle. In production it is a
*separate* Gitlawb repo (`dack-soul`) under the duck's Soul DID, hosted off-VPS (PRD §2)
— **not** part of the harness source tree. It is checked in here only as the canonical
example of the on-repo file formats the harness reads and the agent (in Reflect) writes.

```
dack-soul/
├── SOUL.md                 identity, values, voice, world & trust model
├── prompts/                state system prompts (perceive/express/settle/reflect)
├── skills/                 AgentSkills standard: <skill>/SKILL.md (+ scripts/)
├── stimuli/                standing duties (the job description) — STIMULUS.md + scripts/
├── memory/                 the agent's own cognitive store (flat now; graph-swappable)
└── runlogs/                harness-authored, append-only (agent reads, never writes)
```

**Two lifetimes (PRD §2):** this bundle is durable and survives VPS disposal
(resurrection = fresh VPS pulls the soul from Gitlawb). The ephemeral stimulus/dedup
queue lives in SQLite on the VPS and is disposable.

**Write-gating recap (PRD §4.1), enforced by the harness — not by anything in this repo:**

| Dir / file        | Readable | Writable in        |
|-------------------|----------|--------------------|
| `SOUL.md`, `prompts/`, `skills/`, `stimuli/` | all states | **Reflect only** |
| `memory/`         | all states | Express + Reflect |
| `runlogs/`        | all states | **no state** (harness authors it) |
