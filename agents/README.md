# `agents/` — the duck's workforce (Reflect-authored)

Definitions of the **subagents** the duck may spawn for long-running / sandboxed work
(coding, image generation, research). See architecture §6.5, PRD §6.5, and
`docs/VERIFICATION.md` "Subagents" for the full design and the OpenClaude grounding.

**The load-bearing facts** (so this dir is never mistaken for a privilege escalation):

- **Workers are keyless, sandboxed compute.** A definition here grants a worker a *workspace*,
  a *scoped toolset*, and a *task brief* — **never** a DID, the duck's Post/Settle credentials,
  or soul access. The **duck stays the only principal**; anything durable a worker produces flows
  back to the duck, which publishes through its own gated seams.
- **Reflect-authored, else read-only.** Only the Reflect state may write this dir (same gate as
  `skills/`, `stimuli/`, `prompts/`, `SOUL.md`). The harness loads definitions **only** from this
  repo — never from on-disk `.claude/agents` — so nothing outside the soul can become launchable.
- **Spawn is Express-gated.** Launching a worker is a capability allowed in **Express** and
  **denied in Perceive**; the requested `subagent_type` must resolve to a file here. Workers do
  not get the spawn tool (no nesting in v1).
- **Confinement.** A worker runs in `/workspace/…` (or an `isolation:'worktree'` copy) **outside**
  the soul repo. The wall denies cross-tree writes live; git is a post-run integrity tripwire on
  the soul tree.

**Format** = OpenClaude agent definition (markdown + YAML frontmatter):
`description`, `prompt`, `tools` / `disallowedTools`, `model`, `maxTurns`, `background`,
`isolation: worktree`. Implementation lands in BUILD-PLAN **Phase 10** (post-core); the files
here are illustrative scaffolding so the bundle shape is fixed now.
