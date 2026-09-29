# Creator OS — Design Direction

Creator OS should feel **authored, precise, editorial and technically credible**. The visual system is designed for coding and AI-building explainers, not for generic SaaS dashboards.

The craft bar may be informed by high-quality product references, including the level of restraint and polish the user associates with Hapo, but Creator OS must remain an original system rather than copying another brand's identity, layouts, trademarks or signature assets.

## Visual thesis

- Calm base, high-energy focal moments.
- One dominant teaching point per scene.
- Prefer proximity, scale, typography and negative space over extra containers.
- UI fragments should look like believable product interfaces, not generic AI mockups.
- Use asymmetry when it improves the reading path.
- Every arrow, focus ring, crop, zoom and floating object must explain a relationship, state or cause/effect.

## Typography

- Sans: **Geist**
- Code / terminal / file data: **Geist Mono**
- Display: 36px Bold
- Title: 24px SemiBold
- Body: 16px Regular
- Metadata: 13px Medium

Keep the role count small. Do not use monospace as a generic "tech" costume outside code, commands, filenames, timestamps or measurements.

### Optical type rules

Use size-aware tracking and leading rather than one fixed value across all text.

- Display 34px+: tracking around -2.2%, line-height ~104%
- Large title 28–33px: tracking around -1.6%, line-height ~108%
- Title 22–27px: tracking around -0.9%, line-height ~114%
- Body 16–21px: near-neutral tracking, line-height ~132%
- Metadata under 16px: slightly positive tracking, line-height ~142%

## Color tokens

- Background/Canvas — #F7F8FA
- Background/Surface — #FFFFFF
- Background/Well — #F1F3F6
- Text/Primary — #101114
- Text/Muted — #6B7280
- Text/OnDark — #F7F8FA
- Text/MutedOnDark — #A7ACB7
- Border/Default — #E5E7EB
- Border/RimDark — #2A2E38
- Accent/Primary — #5B6CFF
- Accent/Soft — #EEF0FF
- Status/Success — #16A34A
- Status/Warning — #C47A1D
- Status/Danger — #DC2626
- Surface/Dark — #111318

Accent is for selection, focus and meaningful emphasis. It should not become the default decoration on every surface.

## Shape and depth

- Small radius: 10–12px
- Standard surface radius: 14px
- Major composition radius: 18px
- Pills only for compact statuses or controls.
- Use one subtle elevation recipe per surface.
- Do not combine heavy border + wide shadow + glow.
- Dark surfaces use restrained rim strokes and small inner highlights rather than glow.
- Use translucent / blurred material only for true floating functional layers, not every card.
- Bigger floating layers may use slightly deeper blur and shadow than small chips.

## Motion language

Recommended timing:
- Immediate feedback: 120ms
- Routine state transition: 240ms
- Authored focal transition: 420ms
- Exits should be faster than entrances.
- Primary easing for non-physical transitions: cubic-bezier(0.16, 1, 0.3, 1)

Motion must communicate:
1. relationship,
2. continuity,
3. focus,
4. cause and effect,
5. meaningful state change.

Prefer shared movement, cropping/masks, focus rings, connector paths, cursor paths and deliberate camera pushes. Avoid identical fade-and-rise entrances on every object.

## Physical motion rules

For motion that should feel physically direct rather than pre-scripted:

- Default to a critically damped spring: damping ratio ~1.0.
- Typical response: 0.35–0.4s.
- Do **not** add bounce by default.
- Add slight bounce only when the preceding movement carries real momentum, such as a flick or thrown card.
- When a target changes mid-motion, continue from the current on-screen value instead of restarting from the previous logical state.
- Carry velocity through re-targets whenever possible.
- Enter and exit along the same spatial path.
- Anchor popovers, callouts and floating cards to the source object that caused them.
- Motion should hint toward the final state before arrival.
- For very fast travel, prefer a subtle stretch/blur rather than a hard teleport.

For Remotion, emulate spring behavior with critically damped values unless a scene explicitly represents momentum.

## Spatial continuity

- If a panel enters from a source, it should return toward that same source.
- If a callout explains a browser element, its connector should originate from that element.
- Use shared-element movement when a concept transforms from one state to another.
- Avoid unrelated directional changes between scenes unless the direction itself communicates meaning.

## Reduced motion

Every implemented animation must have a reduced-motion version that preserves meaning while reducing spatial movement.

When reduced motion is active:
- replace large slides, parallax and spring movement with short cross-fades,
- remove overshoot,
- keep color, opacity, highlighting and state changes,
- preserve the same information hierarchy.

## Anti-patterns

Do not use:
- generic metric-card dashboard grids as the default composition,
- repeated equal-size cards when information is not equivalent,
- uppercase eyebrow labels above every heading,
- gradient text,
- decorative AI orbs or random particles,
- gratuitous glow,
- Unicode arrows or emoji as the icon system,
- pills as decoration,
- fake charts or invented trends,
- motion with no explanatory purpose,
- long static holds in short-form explainers,
- bounce where no momentum exists,
- inconsistent entry/exit directions,
- glassmorphism as a universal surface treatment.

## V01 Figma source

Creator OS — V01 Visual Assets:
https://www.figma.com/design/l1tc9Fe9SNURZf6lgG59dO

The file contains the production visuals plus the **Creator OS Visual Grammar** frame, which is the visual source of truth for subsequent motion scenes.
