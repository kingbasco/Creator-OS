# V01 — Visual Asset Map

Figma source: https://www.figma.com/design/l1tc9Fe9SNURZf6lgG59dO

The Figma file now contains two pages:

- **V01 Visual Assets** — earlier refined exploration, preserved for comparison.
- **V02 Redesign** — current production direction for V01 motion work.

## Current production source — V02 Redesign

Board node: **20:3**

| Figma frame | Node ID | Primary use |
|---|---:|---|
| 01 / Dashboard Overview V2 | 20:7 | Scene 01 Creator OS production pipeline, scene map and review action |
| 02 / Vibe Coding Loop V2 | 20:8 | Scene 02 prompt → code → run → error → correction mechanism |
| 03 / Instruction to Repo Diff V2 | 20:9 | Scene 04 request → affected files → focused code diff |
| 04 / Run Inspect Correct V2 | 20:10 | Scene 05 large browser problem state → corrected state |
| 05 / Fast Not Finished V2 | 20:11 | Scene 06 Works → Correct → Secure → Ship quality-gate composition |
| 06 / AI Executes Human Decides V2 | 20:12 | Scene 07 AI execution → human judgment → ship decision |
| 07 / Creator OS Visual Grammar V2 | 20:13 | Production visual grammar for type, surfaces, connectors and motion behavior |

The V2 redesign is the preferred visual source for subsequent Remotion/Tesseract-style motion implementation.

## Previous V01 exploration

| Figma frame | Node ID | Primary use |
|---|---:|---|
| 01 / Dashboard Overview | 4:16 | Earlier production-pipeline exploration |
| 02 / Prompt Code Run Error Loop | 4:61 | Earlier connected loop visual |
| 03 / Instruction to Repo Diff | 4:96 | Earlier request → repo → diff visual |
| 04 / Browser Issue and Fix | 4:118 | Earlier inspect/correct visual |
| 05 / Fast Not Finished | 4:143 | Earlier quality-gate visual |
| 06 / AI Executes Human Decides | 4:173 | Earlier AI/human responsibility split |
| 07 / Creator OS Visual Grammar | 10:83 | Earlier visual-grammar board |

## Integration rule

Prefer semantic reconstruction in Remotion for elements that need to animate independently.

Use exported Figma frames or cropped assets only when the visual is primarily static. If a screenshot is exported, preserve editable Figma as the source of truth.

## Visual system

The Figma file contains local Creator OS variables and effect styles that align with `DESIGN.md`.

### Colors

- Background/Canvas
- Background/Surface
- Background/Well
- Text/Primary
- Text/Muted
- Text/OnDark
- Text/MutedOnDark
- Border/Default
- Border/RimDark
- Accent/Primary
- Accent/Soft
- Status/Success
- Status/Warning
- Status/Danger
- Surface/Dark

### Type

- Geist — interface and explainer typography
- Geist Mono — code, commands, filenames and measurement data

### Depth

- Creator OS / Surface — ordinary elevated surfaces
- Creator OS / Float — selective floating/focal elements

### Motion baseline

- 120ms immediate feedback
- 240ms state transition
- 0.35–0.4s critically damped spring response for physical focal movement
- cubic-bezier(0.16, 1, 0.3, 1) for non-physical state transitions

Movement must explain relationship, continuity, focus or cause/effect. Avoid decorative motion that does not add meaning.
