# Coin Agent

A tiny tool-dispatching agent in **190 lines of dependency-free Python**.

It has the same architecture as a real LLM agent — a state object, a registry of
tools, and a router that decides which tool a request should call — with one thing
deliberately missing: the language model doing the routing. That's the point. This is
where I'm starting, and the router is the next thing to replace.

```text
$ python coin_agent.py
Coin Agent — collect 5 coins. Type 'help' or 'quit'.

> collect
Coin collected. Total: 1/5
> what is left
You have 4 coin(s) left to collect.
> total coin collected
Current total: 1 of 5
> reset
Reset. Count was 1, now 0.
> quit
Final total: 0 of 5
```

---

## Run it

No dependencies. Python 3.10+ (uses `X | None` type syntax).

```bash
git clone https://github.com/Diwakar-cl/coin-agent.git
cd coin-agent
python coin_agent.py
```

**Commands:** `collect` · `total` · `remaining` · `reset` · `history` · `help` · `quit`

Aliases work too: `add`, `grab`, `score`, `count`, `left`, `clear`, `log`.

## Run the tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

```text
..............                                                           [100%]
14 passed in 0.02s
```

---

## Architecture

```
input ──> choose_tool() ──> Tool.fn(State) ──> State ──> printed result
              │
              └── TOOLS registry: name, aliases, keywords, help text
```

| Piece | Purpose |
|---|---|
| `State` (dataclass) | Single source of truth: `goal`, `coins`, `history` |
| `Tool` (frozen dataclass) | A callable plus its routing metadata |
| `TOOLS` (tuple) | Ordered registry — **order is routing priority** |
| `choose_tool()` | Exact match → alias → keyword → `None` |
| `run()` | The agent loop: read, route, execute, repeat |

---

## Why it's built this way

**Routing is order-sensitive.** `"total coin collected"` contains both `total` and
`collect`. The tool that should win is declared first, and the router checks the whole
registry in order, so the specific intent beats the generic one.

This was a real bug. My first version used `elif "total" in text or "collected" in text`
*before* the `collect` branch, which meant typing `coin collected` — the tool named
after the action — returned the total instead of collecting a coin. It works if you
type `total coin collected`, and silently does the wrong thing if you type `coin collected`.
The bug was invisible until I typed the tool's own name.

There's now a regression test that locks it shut:
`test_choose_tool[total coin collected → total]`.

**Tools don't print, they return.** Printing inside a tool makes it untestable — you'd
have to capture stdout to check behaviour. Returning a string means a test is just
`assert collect(state) == "Coin collected. Total: 1/5"`.

**State is one object, not a variable.** My first version passed `current_coin` around
as a bare int and read `goal` from a module-level global. Wrapping both in a dataclass
means adding a level, a timer, or save/load later doesn't touch every function
signature — and it makes the code testable at all.

**Goal-reached is a guarded state, not an afterthought.** Collecting past the goal
returns a clear message instead of silently doing nothing, and `remaining` can never go
negative.

---

## Design decisions

| Decision | Alternative | Why I chose this |
|---|---|---|
| Three-pass router (exact → alias → keyword) | Single `if/elif` chain | No collision when new keywords are added |
| Ordered tuple registry | Dict keyed by name | Order encodes intent priority |
| Tools return strings | Tools print | Testable without capturing stdout |
| `@dataclass State` | Module-level globals | Explicit state, testable, extensible |
| Zero dependencies | Click / Typer | Forces me to understand the loop |

---

## What I'd add next

- [ ] **Replace `choose_tool()` with a real LLM tool-calling call** — same registry, same tools, smarter router. That's the definition of an LLM agent, and this repo is one step away from it.
- [ ] **Eval set** — 50 phrasings of the 5 intents (`"gimme one"`, `"how many more?"`, `"start over"`) scored against expected tool names, so router accuracy becomes a number instead of a feeling.
- [ ] Persist state to JSON so the count survives a restart
- [ ] Emit a structured tool-call log for debugging
- [ ] Multi-agent version: a planner that decides *which* sub-agent handles a request

## Background

I'm working through a self-directed roadmap toward AI engineering — Python fundamentals
→ software engineering → LLM APIs → RAG → agents → evals. This is a Phase 1 project:
built to practise the loop, the registry, and the router before the model shows up.

Building in public, one repo at a time.

---

## License

MIT — do whatever you like with it.
