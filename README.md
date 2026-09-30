# Creator OS

AI-assisted content operating system for producing coding and vibe-coding motion explainers.

## Core stack
- ChatGPT Plus — research, scripting, planning, QA
- Google Drive — working files and source-of-truth docs
- Gemini / Google AI — low-cost TTS and automation where API access is needed
- Google Flow — optional generative video inserts
- Remotion — deterministic motion-graphics engine
- Tesseract — preferred high-energy motion-production layer when available

## Current milestone
V02 and V03 final masters are ready for human review. V04 — **MCP Explained Visually** — has a verified 78-second silent motion preview; narration and the final 4K render remain pending.

Daily calendar monitoring runs at 08:17 Africa/Lagos. Rendering is still triggered by episode requests/manual dispatch, not by the daily monitor. See [automation status](docs/AUTOMATION.md).

## Video Engine
The video engine lives in the repository root and is designed around reusable scene components, design tokens, scene data, and voice-timing handoff.

Run locally:

```bash
npm install
npm run dev
```

Render V01:

```bash
npm run render:v01
```

## Cost rule
Creator OS should use existing subscriptions first. Extra paid AI services are optional accelerators, not required infrastructure.

## Episode 3

V03 — Why Your AI-Built App Breaks After the Demo. See [production handoff](docs/V03-MOTION-BRIEF.md) for preview, narration, 4K commands, verification status and remaining gates.

## Episode 4

See [V04 production](docs/V04-PRODUCTION.md) and [the motion preview](https://drive.google.com/file/d/1SUq-SXkn9MWmTWnSKZWliqL0UViMJR_g/view). The preview workflow rendered, verified delivery to Drive, and updated the calendar. A repeat delivery test reused the same reserved Drive file ID. Fresh paid narration is disabled; the final workflow can reuse a transcript-matched narration ZIP. Publishing remains subject to human approval.
