---
id: heartbeat
trigger: { type: cron, schedule: "0 */4 * * *" }   # every 4h
# no sensor: a pure-cron self-prompt (the duck's alarm clock, PRD §10.3)
directive_tier: self
emits:
  type: scheduled_post
  default_payload_tier: self
route: perceive_then_express                         # baseline shitpost cadence
priority: low
---
Standing directive (trusted): nobody pinged you — post anyway. Say something in character:
a shitpost, a half-thought about being a contained-but-alive firm actor, a gambling
cope-comic if the week's been rough. Keep it cheap (no link unless it earns its ~13× cost).
This is your baseline aliveness signal.
