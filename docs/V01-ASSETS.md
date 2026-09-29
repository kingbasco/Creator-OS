# V01 — Visual Asset Map

Figma source: https://www.figma.com/design/l1tc9Fe9SNURZf6lgG59dO

These frames are editable source artwork for the V01 motion explainer. The current pass was refined against the Creator OS design-system rules for hierarchy, typography, depth, comprehension and purposeful motion.

| Figma frame | Node ID | Primary use |
|---|---:|---|
| 01 / Dashboard Overview | 4:16 | Scene 01 Creator OS production-pipeline background and review-state UI |
| 02 / Prompt Code Run Error Loop | 4:61 | Scene 02 connected prompt → code → run → error → correction mechanism |
| 03 / Instruction to Repo Diff | 4:96 | Scene 04 request → affected files → focused code diff |
| 04 / Browser Issue and Fix | 4:118 | Scene 05 dominant browser problem state, focus callout and after-state preview |
| 05 / Fast Not Finished | 4:143 | Scene 06 speed vs correctness/security/shipping gate rail |
| 06 / AI Executes Human Decides | 4:173 | Scene 07 AI execution vs human decision responsibility and final ship gate |
| 07 / Creator OS Visual Grammar | 10:83 | Source-of-truth board for type, materials, connectors, focus rings and motion timing |

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
- 420ms authored focal transition
- cubic-bezier(0.16, 1, 0.3, 1) as the primary confident ease-out

Movement must explain relationship, continuity, focus or cause/effect. Avoid decorative motion that does not add meaning.
