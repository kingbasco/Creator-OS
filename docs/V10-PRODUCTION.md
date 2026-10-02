# V10 — One Agent or Many? How Multi-Agent Coding Actually Works

80-second conceptual explainer.

## Core visual
Start with one central **Orchestrator** card holding the full goal. It branches into four focused subagents:

- Research
- Frontend
- Backend
- Tests

Each subagent receives a compact task card and runs a visible progress bar. When independent, the progress bars advance in parallel.

## Strong sequence
After parallel progress, introduce a coordination problem:
- Frontend and Backend both touch the same API contract.
- A conflict marker appears.
- Their outputs stop before the final node.
- The orchestrator opens both diffs, resolves the mismatch, and then merges all four outputs into one **Integration / Review** node.

## Message
Do not frame multi-agent systems as “AI teams replacing humans.” The focus is work decomposition, context management, parallelism, coordination and final review.

## Style
Reuse the approved Creator OS presenter. No top branding header. Keep branch lines behind cards, use wide spacing, and never stack task cards on top of progress labels.
