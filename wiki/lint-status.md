# Lint Status

Tracks lint progress over source pages. Lint runs in **batches of 5 sources per session**.

The order is **randomised once with seed 42** to break topic clustering, then **stored
permanently** — never reshuffled between sessions. Checkboxes:

- `[ ]` not yet linted
- `[x]` linted (for a source: done; for a hub page: all contributing sources done)
- `[~]` hub page partially linted (some contributing sources still `[ ]`)

## How this list is built (run once, when source pages first exist)

Deterministic so it reproduces exactly:

```python
import random
from pathlib import Path
slugs = sorted(p.stem for p in Path("wiki/sources").glob("*.md"))  # stable input order
random.Random(42).shuffle(slugs)                                   # randomise ONCE, seed 42
# write slugs in this order as "- [ ] [[slug]]" under "## Source order (seed 42, frozen)"
```

## Source order (seed 42, frozen)

_No source pages found in `wiki/sources/` yet._

When you add source summaries under `wiki/sources/`, build the frozen randomised checklist
once (procedure above) and do not reshuffle it afterwards. Then run **"lint the wiki"** to
process the first batch of 5.

## Hub pages (entities / concepts / themes touched during lint)

_None yet._
