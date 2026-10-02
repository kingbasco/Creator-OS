# V09 — Row Level Security: The Setting That Protects Your Users’ Data

80-second conceptual explainer.

## Core visual
Use two user cards — Alice and Bob — pointing to one profiles table.

First state:
- both users are authenticated;
- the table contains Alice and Bob rows;
- without an effective row policy, both rows visually travel back to either user.

Then add an **RLS policy shield** directly in front of the table. The same requests now pass through the shield:
- Alice receives only Alice's row;
- Bob receives only Bob's row.

## Strong visual contrast
Make **Auth ≠ Authorization** unmistakable.

Authentication card:
- “Who are you?”
- identity/session

Authorization/RLS card:
- “Which rows may you access?”
- database policy

## Style
Continue the approved presenter-led Creator OS direction. No top branding header. Keep users, policy shield, and table in separate zones so nothing overlaps. The policy should look like a database gate, not a generic security warning.

This is a conceptual explanation, not a live security audit.
