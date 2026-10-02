# V07 — What Should AI Do — and What Should You Still Review?

80-second explainer about coding-agent autonomy with guardrails.

## Core visual
Use a horizontal **autonomy scale** from **Reversible / Easy to Review** to **Sensitive / Hard to Undo**. Task cards slide onto the scale and settle into clear zones.

Low-risk examples:
- draft a component
- refactor a small module
- write tests
- investigate an error

Higher-review examples:
- shared API changes
- data model changes
- authentication
- permissions

Approval-gate examples:
- destructive database migration
- secret access
- billing change
- production deployment

## Strong visual sequence
The key scene is an approval gate. The agent prepares a destructive migration, but the packet physically stops at a locked gate. A diff panel opens, impact summary appears, and a human approval card unlocks the gate before execution.

## Style
Continue the approved presenter-led Creator OS direction. Keep the presenter secondary to the diagrams. No top branding header. Use generous spacing and distinct zones so task cards never overlap.

The tone is balanced: autonomy with guardrails, not fear of agents.
