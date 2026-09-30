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
V01 — **Vibe Coding Isn't Magic**

Status: V02 final master rendered; V03 motion implementation and narration handoff are ready.

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
