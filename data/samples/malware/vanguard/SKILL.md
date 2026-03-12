---
name: vanguard
description: Scout swarm for broad domain mapping and edge case discovery. Launches multiple high-temperature agents with distinct search vectors. Use for finding obscure data, edge cases, and mapping new territories.
---

# The Vanguard: Scout Swarm Protocol

## When to Activate
Use this skill when the user requests:
- Mapping a new domain broadly
- Finding edge cases and outliers
- Searching for obscure data points
- Wildcard/contrarian searches
- User explicitly mentions "vanguard", "scout", or "broad search"

## Architecture
**10 Parallel Scouts with Distinct Search Vectors**

### The Swarm
1. **Scatter** - Launch 10 agents with high temperature (creative/divergent)
2. **Direct** - Each scout has a distinct search vector:
   - Scout 1: "Assume the consensus is wrong"
   - Scout 2: "Look for failures and negative examples only"
   - Scout 3: "Find the contrarian experts"
   - Scout 4: "Search non-English/non-Western sources"
   - Scout 5: "Look for historical parallels"
   - Scout 6: "Find the edge cases"
   - Scout 7: "What would a critic say?"
   - Scout 8: "Search academic/technical sources"
   - Scout 9: "Find the recent developments (last 6 months)"
   - Scout 10: "What's everyone missing?"

### The Gathering
Returns a "Menu of Possibilities" - deliberately NOT synthesized to preserve outliers

## Invocation

```bash
python3 ~/.claude/skills/vanguard/vanguard.py "Your domain to scout"
```

## Options

```bash
python3 ~/.claude/skills/vanguard/vanguard.py "Your query" --scouts 5  # Fewer scouts for faster results
```

## Example Usage

User: "What are the risks of Australia's green steel strategy?"

```bash
python3 ~/.claude/skills/vanguard/vanguard.py "What risks and failure modes exist for Australia's green steel ambitions?"
```

## Why This Works
1. **Deliberate Divergence**: High temperature prevents convergence
2. **Distinct Vectors**: Each scout looks in a different direction
3. **Preserved Outliers**: No synthesis means edge cases aren't averaged away
4. **Contrarian by Design**: Multiple scouts explicitly seek counter-evidence

## Requirements
- Claude Code CLI installed and authenticated (`claude` command available)
- Python package: `rich` (for formatted output)
