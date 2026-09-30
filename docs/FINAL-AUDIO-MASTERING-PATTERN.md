# Creator OS — Final Audio & Mastering Pattern

Use this pattern for V03 onward after narration timing and authored motion are locked.

## 1. Sound design

Generate project-owned, deterministic sound assets. Keep narration dominant.

Use:
- a very low ambient bed,
- directional transition whooshes tied to actual spatial motion,
- UI ticks only on visible interactions,
- success/error tones only on meaningful state changes,
- one distinct human-approval cue where responsibility returns to the viewer/user.

Avoid:
- decorative sound on every animation,
- stock trailer impacts,
- constant risers,
- loud music under explanation,
- effects that do not correspond to a visual or semantic event.

## 2. Mix hierarchy

1. Narration
2. Meaningful state cues
3. Transition movement
4. Ambient bed

The mix should still communicate clearly if effects are removed.

## 3. Master target

Default Creator OS social master:
- vertical 2160×3840
- 30 fps
- H.264
- stereo AAC
- target -14 LUFS integrated
- true peak ceiling -1.5 dBTP

## 4. QA gate

Before publish approval, verify:
- correct resolution and frame rate,
- audio stream exists and is stereo,
- narration remains intelligible on phone speakers,
- no transition masks expose black/empty frames,
- no SFX obscures a word,
- no clipping,
- final loudness analysis is archived with the render,
- master artifact is downloadable and unexpired.

## 5. Automation rule

Episode render workflows remain manual/approval-gated. Do not auto-publish or auto-render final masters on every repository push.
