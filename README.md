# Coin Agent

A small command-line agent in plain Python. You type a request in everyday language,
and it picks the matching tool and runs it.

There is no AI model in it yet. That's deliberate — this is the tool-and-router part
built by hand first, so I understand what a model is actually doing when it does the
same thing.

```text
$ python coin_agent.py
Enter your tool, or quit: collect
Coin has been collected:  1
Enter your tool, or quit: remain
You've 4 to collect
Enter your tool, or quit: total
Current total:  1
Enter your tool, or quit: reset
Resetting the current count 1
Enter your tool, or quit: quit
Current coin collected: 0
```

## Run it

No dependencies. Python 3.6+.

```bash
git clone https://github.com/Diwakar-cl/coin-agent.git
cd coin-agent
python coin_agent.py
```

## Commands

The goal is 5 coins.

| Type something containing | Tool that runs | What it does |
|---|---|---|
| `collect` | collect a coin | adds 1 to the count |
| `total` or `collected` | show total | prints the current count |
| `remain` or `left` | remaining | prints how many coins are left |
| `reset` or `clear` | clear count | sets the count back to 0 |
| `quit` or `exit` | — | exits and prints the final count |

## How it works

```text
input  ->  choose_tool()  ->  tools[name]  ->  function  ->  prints result
                                    |
                             tools = {
                               "coin collected": coin_collected,
                               "total coin collected": show_total,
                               "remaining coin": remaining_coin,
                               "clear count": clear_record,
                             }
```

- `tools` is a dictionary of functions keyed by name — a small registry.
- `choose_tool()` looks for keywords in what you typed and returns a key.
- The loop calls the matching function and stores the returned count.

Each function takes the current count and returns the new one, so the count lives in
exactly one place: the `coin` variable in the loop.

## What I learned building it

- **A tool registry is just a dict of functions.** That's the same shape real agent
  frameworks use — a set of named tools, plus something that decides which one to call.
- **Keyword matching collides.** `"total" in text` fires before `"collect"` is ever
  checked, so typing `coin collected` shows the total instead of collecting a coin.
  Order of the `if` chain *is* the routing logic, and that's fragile.
- **Functions that print are hard to test.** Returning a value would make them
  testable; printing means you'd have to capture the screen output.

## Known limitations

- Keyword matching is order-dependent and will misfire as more words are added.
- `goal` is a module-level global rather than being passed in.
- No tests yet.

## Next

- [ ] Replace `choose_tool()` with a real LLM tool-calling call — same registry, smarter router
- [ ] Add tests for the routing order and the goal limit
- [ ] Move `goal` and `coin` into one state object

## License

MIT
