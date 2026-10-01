# MCP presenter — motion direction prototype

15-second, 1080 × 1920, 30 fps silent prototype. This is an illustrated explanation, not a live integration or finished episode.

## Direction

Original editable vector presenter with a separate head, eyes and pointing arm. Geist type and Creator OS blue (#5B6CFF). A typed request reframes into an AI-app/server connection; a search request travels out and a document returns into a source-linked answer. The presenter is a proposed character, not a likeness of Cyril.

Timing: 0–4.4s ask; 4.4–9.8s tool exchange; 9.8–15s answer with context. This is a simplified tool-call example; MCP does not itself grant access.

## Files

- `MCP-Presenter.tsrct`: portable editable Tesseract 0.3.0 project with packaged Geist fonts, 96 native layers and 26 animation tracks.
- `.tesseract-work/build.py`: deterministic layout/animation authoring source.
- `.tesseract-work/base.json`: initial document metadata; fonts are packaged in the existing project.
- `.tesseract-work/document.json` and `animation.json`: source geometry and animation actions.
- `Geist-OFL.txt`: font license; original variable font from google/fonts/ofl/geist, instantiated at 400 and 600.

The rendered MP4 is delivered separately to avoid committing video output to the repository.

To regenerate geometry, run build.py, then `tsrct project commit` with document.json and `tsrct project apply` with animation.json, targeting the existing packaged project. To render, use Tesseract 0.3.0:

```sh
tsrct export --project MCP-Presenter.tsrct --resolution 1080p --fps 30 --encoder-backend external-ffmpeg-command --ffmpeg-path /usr/bin/ffmpeg --output MCP-Presenter.mp4
```

Linux requires a working Vulkan driver; Mesa lavapipe can render in software.

## Review

Inspected native filmstrip at 1, 3, 4.7, 5.8, 7, 8.5, 10, 12 and 14.5 seconds. Corrected text vertical alignment after first frame review. Export measured as H.264, 1080×1920, 30 fps, exactly 15 seconds; full FFmpeg decode completed without errors. No audio track, narration or lip sync in this direction test. Real-time playback and subjective audio review were not performed. The full V04 episode and its existing delivery status have not been changed. No paid generation API was used.
