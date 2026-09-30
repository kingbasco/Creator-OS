# V03 — Why Your AI-Built App Breaks After the Demo

Status: motion implementation; narration pipeline connected, recording not generated yet.

Storyboard: https://www.figma.com/design/MFGOtVTkXyJVsbyWlYM0tU
Script: https://docs.google.com/document/d/1hmcp0AGiclaxVcY3BGMRTYK5FTCvfHbjxYowUVN1rTU/edit

Eight scenes cover demo success, the happy path, edge cases, access boundaries, environment configuration, observability, verification gates and the MCP teaser. Shared tokens and the existing Geist font match the series.

The silent prototype uses provisional 84-second timing. The voiced timeline uses measured per-scene narration duration plus 0.18 seconds of breathing room. Missing narration stops the voiced render rather than silently producing a misleading master. Illustrative UI contains no real user data or credentials.

## Commands

- `npm run render:v03`: silent 1080p motion preview.
- `npm run render:v03:4k`: silent native 2160×3840 preview, 30 fps.
- `npm run voice:v03 -- --dry-run`: validate the narration handoff without an API request.
- `npm run voice:v03`: generate narration using the existing Gemini secret and Sulafat voice.
- `npm run render:v03:voiced:4k`: render using measured narration timing.

The Render V03 Motion Preview and V03 Gemini Voice workflows are manual. No automatic publishing or final-master generation is enabled.

Narration makes two precision edits to the source draft: failure after a demo is a possibility rather than an inevitable outcome, and security matters from the start. The environment comparison is explicitly narrated in its own scene. Both keep the original thesis and V04 teaser.

## Remaining production gates

Generate and listen to narration; check scene boundaries and pronunciation; adjust motion to measured timing; add semantic sound cues; perform phone-speaker and transition QA; master and measure loudness; upload one publish master to Renders with previews archived separately. The silent preview is not a final master.
