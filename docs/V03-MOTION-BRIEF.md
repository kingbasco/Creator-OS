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

The Render V03 Motion Preview and V03 Gemini Voice workflows are manual. Automatic final rendering is enabled through the V03 readiness request; publishing remains separate.

Narration makes two precision edits to the source draft: failure after a demo is a possibility rather than an inevitable outcome, and security matters from the start. The environment comparison is explicitly narrated in its own scene. Both keep the original thesis and V04 teaser.

## Remaining production gates

Generate and listen to narration; check scene boundaries and pronunciation; adjust motion to measured timing; add semantic sound cues; perform phone-speaker and transition QA; master and measure loudness; upload one publish master to Renders with previews archived separately. The silent preview is not a final master.

## Final mix pipeline

`npm run sound:v03` generates deterministic 48 kHz stereo cues. The mix places quiet transition sounds and only six meaningful state cues, with narration dominant. An ambient bed fades at the opening and ending.

`npm run render:v03:final:4k` requires generated narration. `npm run master:v03` performs two-pass normalization, measures the encoded result and checks vertical 4K H.264 at 30 fps plus 48 kHz stereo AAC. Target: -14 LUFS and -1.5 dBTP, with a 1 LUFS and 0.2 dB encoded tolerance. QA reports are saved alongside the master.

The **Render V03 Final 4K** workflow generates narration using the existing GitHub Gemini secret, derives scene timing, mixes sound, renders, masters and uploads a review package. It does not publish or upload files to Drive automatically. A successful render still requires narration listening and visual review before the file becomes the publish master. On rerun it regenerates narration; preserve and reuse the review audio package when further edits only affect motion or mixing.

Verified silent preview: 84 seconds, 540×960, 30 fps. All eight scene keyframes were inspected, with no black intervals detected. The implementation passed local type-check, voice dry runs and GitHub Motion CI (36682118513). These checks do not verify generated speech or the final mix.

## Automatic render trigger

User authorized automatic rendering on September 30, 2026. A push to main changing `render-requests/v03.json` starts the final pipeline when `status` is `ready`. Update `requestId` for each intentional render request. Ordinary code changes do not trigger generation. Requests with a status other than ready skip rendering. Manual dispatch remains available. Concurrent V03 render runs are serialized rather than canceled mid-generation.

Output is a verified GitHub Actions review artifact retained for 14 days. Automatic Drive upload is not configured. Narration listening and visual review follow rendering; the workflow does not publish content.
