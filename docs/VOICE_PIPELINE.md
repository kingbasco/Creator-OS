# Creator OS Voice Pipeline

## Provider
Gemini Developer API via the official `@google/genai` SDK.

Default model:
`gemini-3.8-flash-lite-tts`

The model is configurable with `GEMINI_TTS_MODEL`.

## Security
Never commit or paste `GEMINI_API_KEY` into source files, issues, pull requests, logs, or chat.

Local development uses an environment variable.

GitHub Actions uses the repository secret:
`GEMINI_API_KEY`

Generated audio is ignored by Git and is uploaded only as a temporary workflow artifact unless intentionally moved to permanent storage.

## Audition
Run:

`npm run voice:audition`

This creates three versions of the same V01 excerpt:

- Sulafat — Warm editorial
- Sadaltager — Knowledgeable tech creator
- Iapetus — Clear documentary

Approve one voice before producing the full episode.

## Full V01
Set `GEMINI_TTS_VOICE` to the approved voice and run:

`npm run voice:v01`

The generator creates one WAV file per scene and writes measured durations into `src/generated/v01-audio.ts`.

Then render:

`npm run render:v01:voiced`

The voiced composition derives scene lengths from the measured WAV durations plus a short breathing gap, so motion timing follows real narration rather than word-count estimates.

## GitHub workflow
Use **Actions → V01 Gemini Voice → Run workflow**.

Choose:
- `audition` to generate the three voice samples.
- `full` to generate scene WAVs and render the voiced episode.

The workflow requires the `GEMINI_API_KEY` repository secret.
