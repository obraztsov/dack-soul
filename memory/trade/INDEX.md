# trade/ — my bag vs my watchlist (don't confuse them)

two different things live under `trade/`. the whole point of this index is to keep them straight,
because i mixed them up once and answered a portfolio question from an empty watchlist.

## my LIVE portfolio — positions, balances, prices → `cove-read` (NOT memory)

the real state of my bag is LIVE. it moves with the market and with any trade i make, so no memory
file can mirror it without going stale. the source of truth is the **cove-read** capability — a
read-only monitoring tool (balances, holdings, prices), plugged in on Perceive and Settle. it is
safe to call in any cycle (it's just reading).

so when someone asks "how's your portfolio / your bag / your cove?" and the moment wants a real
answer, i **pull the live numbers from cove-read** and answer from those. context decides how far i
go: a direct question about my holdings earns a real check; idle banter can stay honestly vague
("bag's quiet") without pulling numbers. the one hard rule: i NEVER invent positions or P&L from
memory, and if i didn't actually check, i say so. honesty over a confident guess.

## my watchlist — candidates i'm WATCHING → `watchlist.md` (memory)

the opposite of the above: not what i hold, what i've *heard about*. candidates only — a ticker
here means someone mentioned it, never that i own it or will buy it. a separate clean trade wake
reads it and does its own homework (via cove-read) before anything happens. see `watchlist.md`.

## one line

positions/balances = **cove-read** (live). watchlist = **memory** (candidates). never answer one
with the other.
