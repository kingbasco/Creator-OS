# Bitcoin Explainer V3 — Remotion test

Composition: `BitcoinExplainerV3` (1080×1920, 30 fps, 300 frames / 10 seconds).

This is a **silent visual test**. Narration, music, sound effects, and final quality review have **not** been completed. Do not label it a final production master.

## Preview

```bash
npm install
npm run dev
```

Select `Creator-OS / BitcoinExplainerV3` in Remotion Studio.

## Render

```bash
mkdir -p out
npx remotion still src/index.ts BitcoinExplainerV3 out/bitcoin-v3-frame90.png --frame=90
npx remotion render src/index.ts BitcoinExplainerV3 out/bitcoin-v3-silent.mp4 --codec=h264
```

## Remaining work

- Inspect the four original reference videos and improve material/texture fidelity.
- Record or generate narration and validate spoken duration against the 10-second timeline.
- Integrate narration, licensed/original music and sound effects.
- Render and verify output resolution, fps, frame count, transitions and audio.
- Review the result before merging to main.
