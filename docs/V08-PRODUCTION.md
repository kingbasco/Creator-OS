# V08 — Supabase for Vibe Coders: Database, Auth, Storage in One Flow

82-second conceptual backend explainer.

## Core visual
Center one browser/app card. Fan clean connections out to five backend blocks:

1. Auth
2. Postgres
3. Storage
4. Functions / API
5. Realtime

Each block should perform one visible job rather than sitting as a static label.

## Strong sequence
The final sequence is one continuous signup flow:

- user submits signup form;
- Auth creates the identity;
- profile image travels into Storage;
- profile fields become a Postgres row;
- backend function/API coordinates protected work;
- Realtime sends the updated profile state back to the app.

Use moving packets and changing UI states so the diagram explains itself.

## Style rules
Continue the approved presenter-led Creator OS style. No top branding header. Keep the central app smaller than the architecture so the five backend blocks have enough breathing room. Do not stack labels on top of the app card. Use the corrected spacing discipline from V05 onward.

This is a conceptual explainer, not a live Supabase integration.
