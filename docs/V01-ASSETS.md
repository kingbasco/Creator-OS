# V01 — Visual Asset Map

Figma source: https://www.figma.com/design/l1tc9Fe9SNURZf6lgG59dO

These frames are editable source artwork for the V01 motion explainer.

| Figma frame | Node ID | Primary use |
|---|---:|---|
| 01 / Dashboard Overview | 4:16 | Scene 01 app/dashboard background and floating UI fragments |
| 02 / Prompt Code Run Error Loop | 4:61 | Scene 02 process-loop cards and connector references |
| 03 / Instruction to Repo Diff | 4:96 | Scene 04 instruction → repo → diff visual |
| 04 / Browser Issue and Fix | 4:118 | Scene 05 inspect/correct before-and-after browser visual |
| 05 / Fast Not Finished | 4:143 | Scene 06 speed vs quality-gate visual |
| 06 / AI Executes Human Decides | 4:173 | Scene 07 AI/human responsibility split and final ship gate |

## Integration rule

Prefer semantic reconstruction in Remotion for elements that need to animate independently.

Use exported Figma frames or cropped assets only when the visual is primarily static. If a screenshot is exported, preserve editable Figma as the source of truth.

## Visual system

The Figma file contains local Creator OS color variables matching the code tokens:

- Background/Canvas
- Background/Surface
- Text/Primary
- Text/Muted
- Border/Default
- Accent/Primary
- Accent/Soft
- Status/Success
- Status/Danger
- Surface/Dark
