# V10 — One Agent or Many? How Multi-Agent Coding Actually Works

80-second explainer based on current OpenAI multi-agent guidance.

## Core visual
One central **Main Agent / Orchestrator** owns the user goal. It delegates four independent workstreams:

- Research
- Frontend
- Backend
- Tests

Each subagent receives a bounded card, keeps its own progress, and returns one concise result. The central orchestrator never disappears; it coordinates and integrates.

## Key motion sequence
1. One task arrives at the main agent.
2. Main agent decomposes it into four bounded assignments.
3. Four subagent cards fan out with generous spacing.
4. Independent progress bars run in parallel.
5. Result packets return to the main agent.
6. Integration/review node combines them into one final change.

## Important contrast
Show a second case where two subagents both try to edit the same shared file. Their paths collide and a conflict badge appears. Then collapse that work back into the main agent to show that tightly dependent/shared mutable work is better coordinated sequentially.

## Accuracy notes
Current OpenAI guidance says subagents are useful for independent tasks; each subagent keeps its own context and may work in parallel while the main agent coordinates and combines results. Short tasks and dependent steps should stay with the main agent, and agents editing the same files need coordination.

## Style
Continue the approved presenter-led Creator OS direction. No top branding header. Keep the main agent centered and the four specialists in separate quadrants; do not let progress bars or connector lines cross labels.

No narration while the current TTS quota is unavailable.
