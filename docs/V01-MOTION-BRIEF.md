# V01 — High-Energy Motion Direction v2

## Objective
Turn the restrained prototype into a fast, clean, visually dense motion explainer. Motion should feel editorial and interactive: UI cards fly into context, arrows connect cause and effect, focus rings identify problems, and small labels clarify what the viewer should notice.

## Global rules
- 1080×1920, 30fps.
- Average visible change every 0.8–1.6 seconds; avoid long static holds.
- Use depth through scale, layered movement and parallax, not heavy 3D.
- Flying objects must have a reason: reveal, connect, compare, focus, or transition.
- Arrows/callouts appear only when they direct attention to a specific object.
- Use screenshots/mock UI inside designed frames; crop aggressively to the relevant area.
- Keep one dominant teaching point per scene.
- No random particles, neon glow, generic AI orbs, or chaotic movement.

## Scene 01 — Hook
- App/dashboard frame sits behind headline with subtle parallax.
- Two small floating cards enter from opposite corners: PROMPT and UI.
- A callout arrow points from AI-generated UI label into the product frame.
- “WITHOUT CODING” gets a fast strike-through; “WITH AI” replaces it.
- End with a micro push-in that leads into Scene 02.

## Scene 02 — Prompt → Code → Run → Error → Prompt
- Cards should not merely stack; they travel along a visible process path.
- Add animated connector arrows and a loop-back path from ERROR to PROMPT.
- Use small secondary UI chips: request, diff, terminal, error.
- Error card briefly expands toward camera, then collapses into the correction prompt.

## Scene 03 — Your role moves up a level
- Start tight on code lines, then pull back to reveal the system layers.
- Add moving labels and arrows: UI → Logic → API → Data/Auth.
- A human-direction chip floats above the stack, visually “higher” than code.

## Scene 04 — Describe intent / AI proposes
- Instruction card flies in from left with a cursor click.
- Repo/file cards slide from right.
- Animated arrow from instruction to affected files.
- Diff lines reveal with staggered highlights.
- Include a small “2 files changed” chip flying in near the diff.

## Scene 05 — Run / Inspect / Correct
- Browser screenshot enters with a whip-softened slide.
- Cursor moves to the problem.
- Focus ring expands twice around the issue.
- Callout card “UX ISSUE” points at the error state.
- Correction prompt enters, then the browser updates in-place.

## Scene 06 — Fast ≠ Finished
- Speed meter fills rapidly.
- Small “DEMO WORKS” badge flies in and locks.
- Remaining quality gates appear around it: Correct, Secure, Ready to ship.
- Use arrows to show that speed only reaches the first gate.

## Scene 07 — AI executes / You decide
- Split-screen should feel active rather than static.
- AI-side task cards enter rapidly and flow downward.
- Human-side review cards enter slower with deliberate confirmations.
- Moving connector lines meet at a central BUILD / SHIP decision node.
- Add a small lock/security icon callout at the final gate.

## Scene 08 — Definition / Next episode
- Direction / Iteration / Judgment fly from different axes and lock into a single horizontal system.
- Small visual fragments from earlier scenes orbit briefly around the words, then disappear.
- V02 teaser card pushes forward from depth.

## Reusable motion primitives
- FloatingCard
- ArrowCallout
- FocusRing
- CursorPath
- FlowConnector
- OrbitingChip
- ScenePush
- WhipSlide
- MaskReveal
- ScreenshotCrop

## Tool responsibilities
- Tesseract: expressive motion pass when available in ChatGPT.
- Figma: polished UI frames, dashboard screenshots/mockups, diagrams and callout assets.
- Remotion: scene assembly, deterministic animation, timing, captions and final render automation.
- Google Flow: optional generated footage only when a specific scene needs it.
