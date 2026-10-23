# coin-agent

A small command-line agent in plain Python. You type a request in everyday language,
and it picks the matching tool and runs it.

There is no AI model in it yet. That's deliberate — this is the tool-and-router part,
built by hand first, so I understand what a model is actually doing when it does the
same thing.

```
$ python coin_agent.py
Enter your tool, or quit: collect
Coin has been collected:  1
Enter your tool, or quit: remain
You've 4 to collect
Enter your tool, or quit: total
Current total:  1
```

## Run it

No dependencies. Python 3.6+.

```
git clone https://github.com/Diwakar-cl/coin-agent.git
cd coin-agent
python coin_agent.py
```

## Commands

The goal is 5 coins.

| Type something containing | Tool | What it does |
| --- | --- | --- |
| `collect` | `coin_collect` | adds 1 to the count |
| `total`, `collected` | `show_total` | prints the count |
| `remain`, `left` | `remaining_coin` | prints how many are left |
| `reset`, `clear` | `clear_record` | sets the count back to 0 |
| `quit`, `exit` | — | exits and prints the final count |

## How it works

```
input  ->  choose_tool()  ->  tools[name]  ->  function  ->  prints result
```

`tools` is a dict of functions keyed by name. `choose_tool()` looks for keywords in
what you typed and returns a key. Each function takes the current count and returns the
new one, so the count lives in exactly one place.

## The problem worth knowing about

Keyword matching collides. `"total" in text` is checked before `"collect"` is ever
touched, so typing `coin collected` shows the total instead of collecting a coin. The
order of the `if` chain *is* the routing logic, and that makes it fragile.

Functions that print are also hard to test — returning a value would make them
testable.

## Next

- [ ] Replace `choose_tool()` with a real LLM tool-calling call — same registry, smarter router
- [ ] Add tests for routing order and the goal limit
- [ ] Move `goal` and `coin` into one state object

MIT
