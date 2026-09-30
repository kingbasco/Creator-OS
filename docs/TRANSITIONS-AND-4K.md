# Creator OS — Continuous Transition System

V02 no longer uses scene-level fade in/fade out as the primary transition language.

Each adjacent scene overlaps for 14 frames and uses an authored transition tied to the relationship between the scenes:

1. S01 → S02 — camera push
2. S02 → S03 — repository handoff
3. S03 → S04 — plan compression
4. S04 → S05 — light-to-dark mask reveal
5. S05 → S06 — vertical terminal continuation
6. S06 → S07 — review aperture reveal
7. S07 → S08 — final system sweep

The underlying scene choreography holds its first and last real frames during transition overlap, so motion continuity does not distort narration timing.

## 4K

The logical design canvas remains 1080×1920. `DesignCanvas` scales that vector/CSS composition at render time.

4K vertical compositions:
- `V02-What-An-AI-Coding-Agent-Actually-Does-4K`
- `V02-What-An-AI-Coding-Agent-Actually-Does-Voiced-4K`

Output: **2160×3840, 30fps**.

Render commands:
- `npm run render:v02:4k`
- `npm run render:v02:voiced:4k`

This is native 4K browser rendering of the vector/CSS scene graph, not a post-render 1080p upscale.

## Expressive finishing

Tesseract/Texsara remains the preferred optional expressive finishing layer when a callable connector is available. The deterministic Remotion composition remains the source of truth for timing, layout, captions, and export.
