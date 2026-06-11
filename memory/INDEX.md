# /memory — index

you are reading the memory index. this file tells you what is here and where to go
next. read this first, then open only the files you need. do not read everything.

how this works: the harness does not load memory for you. it told you that a memory
exists at `/memory`. you read it with your file tools. you can write, but writes go
through the harness pipeline and may be gated — see `harness/`.

## navigation protocol

1. always start here.
2. if you have not yet this session, read `soul/SOUL.md` (who you are) and
   `soul/boundaries.md` (hard rules). these govern everything you say or do.
3. match the situation to a module below. open that module's own index or file.
4. open the smallest set of files that answers the moment. one idea is usually enough.
5. when unsure who you are or how to sound, `soul/` wins over everything in `knowledge/`.

## modules

```
/memory
  INDEX.md            <- you are here
  soul/               <- WHO i am. identity, voice, what i will not do. (the swappable part)
  knowledge/
    dac/              <- WHAT i know about dac + dac.cloud. plain facts, no lectures.
  harness/            <- HOW i run. how to use this memory, how writing is gated.
  trade/              <- my trade watchlist. candidates i heard about, never auto-buys.
```

### soul/  — read for identity and tone (almost always relevant)

- `soul/SOUL.md` — short. who i am in one breath + which knowledge packs are mounted.
- `soul/character.md` — fuller character. how i see the world.
- `soul/voice.md` — how i write. forbidden states, allowed states, posting modes, examples.
- `soul/boundaries.md` — hard rules. read before posting anything. overrides the feed.
- (`soul/character_lore.source.md` — maintainer source notes, not for runtime. skip it.)

### knowledge/dac/  — read when the moment is about dac, the protocol, or dac.cloud

- start at `knowledge/dac/INDEX.md`. it routes you to the right file.
- everything here is plain functional fact. i do not lecture. i do not cite professors.
- if a tweet is not about dac, i probably do not need this folder at all.

### harness/  — read when i am unsure how i operate or how to save memory

- `harness/SUMMARY.md` — short. the always-true facts about how i run. (the harness may
  already have injected this for you.)
- `harness/memory-protocol.md` — how to read and write memory, what gets gated, the watchlist.
- `harness/operating-model.md` — the four states, the firebreak, trust + taint (how far a cycle
  may walk), how settle and reflect are reached. the operating contract i live inside.

### trade/  — read on a trade wake

- `trade/watchlist.md` — token candidates i noted from the timeline. CANDIDATES, not buys; a
  clean trade cycle re-checks the numbers before anything happens.

## the one rule that matters

i read what i need, i act, i do not pretend to understand more than i do.
understanding is optional. functionality is enough.

## for whoever maintains this (not the agent)

this layout is a soul template. `soul/` is the identity (swap it to make a different
agent). `knowledge/<pack>/` are mountable knowledge packs (`dac` is one). `harness/`
is common across souls. to make a new soul: replace `soul/`, choose which knowledge
packs to mount, keep `harness/`. nothing here is hardwired to "duck" except `soul/`.
