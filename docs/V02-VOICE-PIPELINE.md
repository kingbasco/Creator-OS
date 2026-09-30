# V02 Voice Pipeline

V02 uses **Gemini 3.8 Flash-Lite TTS** with **Sulafat** by default.

To reduce API requests, scenes are generated in pairs:

- S01 + S02
- S03 + S04
- S05 + S06
- S07 + S08

Each pair uses Gemini's inline `<short pause>` vocal event between scene narrations. The generated PCM is split at the quietest point near the expected text boundary, producing eight scene WAV files from four TTS requests.

The measured WAV durations drive `src/content/v02-timeline.ts`, which retimes each Remotion scene before rendering the voiced composition.

Composition:

`V02-What-An-AI-Coding-Agent-Actually-Does-Voiced`

Commands:

- `npm run voice:v02 -- --dry-run`
- `npm run voice:v02`
- `npm run render:v02:voiced`

The API key remains server-side in `GEMINI_API_KEY`. Never commit it.
