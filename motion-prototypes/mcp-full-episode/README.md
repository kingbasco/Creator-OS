# V04 MCP — full visual draft

78 seconds, eight scenes, 1080 × 1920 at 30 fps. Silent visual draft based on the approved original presenter and Creator OS blue/Geist style. Top branding labels removed.

Editable source: V04-MCP.tsrct (Tesseract 0.3.0, packaged fonts). Authoring source: .tesseract-work/build.py and approved-presenter.json. Run build.py, then project commit using the emitted document.json and project apply using animation.json. Target the existing packaged document to retain its fonts. Geist license included.

Scene timing follows src/content/v04.json: 0–8 connection pattern; 8–18 host/client/server; 18–28 discovery; 28–38 request; 38–48 returned result; 48–58 different systems; 58–68 permissions and request metadata; 68–78 recap and next episode.

Reviewed sampled frames across all eight scenes and corrected a connector crossing opening text. Export: H.264, 1080 × 1920, 30 fps, exactly 78 seconds. This is an illustrated workflow, not a live integration. No narration, music or sound effects yet; real-time playback review was not performed. Narration timing and audio mastering remain pending. No paid generation API used. Existing automation and calendar status were not changed.

The MP4 and overview are delivered separately. Linux export requires Vulkan (software Mesa lavapipe works) and an external FFmpeg encoder. Example:

```sh
tsrct export --project V04-MCP.tsrct --resolution 1080p --fps 30 --encoder-backend external-ffmpeg-command --ffmpeg-path /usr/bin/ffmpeg --output V04-MCP-Visual-Draft.mp4
```
