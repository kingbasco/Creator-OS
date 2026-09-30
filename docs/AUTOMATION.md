# Creator OS automation

## Active monitoring

`Creator OS daily queue check` runs daily at 08:17 Africa/Lagos (07:17 UTC), on relevant code changes, or through Run workflow. It uses the Google OAuth credentials stored in Actions secrets. One monitor runs at a time; each job is limited to five minutes. There are no third-party Python dependencies or AI calls.

It reads the Content Calendar and the Renders folder, skips completed episodes, waits if an episode is In progress, and selects the earliest publish-date Queued episode. Invalid dates and duplicated IDs stop the check. It scans all render-folder pages for existing episode MP4s, using episode metadata where available or bounded episode IDs in filenames, and reports production blockers. This is a duplicate warning/preflight, not a complete exactly-once production mechanism.

Read the result in Actions → Creator OS daily queue check → latest run → Summary. A successful monitor means the inspection worked, not that a video was produced. Expected production blockers appear in the summary without failing the read-only job. Failed API or malformed calendar checks fail the job.

No Google files or cells are modified. No video is rendered or published. No paid API is invoked. Production limits are not configured. Monitoring requires no recurring Next instruction.

## Verified access

The Google connection check passed on 30 September 2026: OAuth refresh, calendar read and edit capability, render-folder listing and upload capability. Actual writes have not been exercised by these checks.

## V04 rendering and Drive delivery

V04 now has an eight-scene script and Remotion composition. Render V04 and deliver to Drive produces a silent 1080p preview when its request changes on main, or a narrated 4K final through manual dispatch with an existing verified narration ZIP. It checks that V04 is the next queued episode. No AI generation is called by this workflow.

The 78-second preview rendered and was delivered successfully on 30 September 2026. Drive checksums, file size and folder placement were verified. Calendar Next Action changed to Review Prototype with the link in its note; status remains Queued. All eight representative scene frames were inspected for readability and clipping. This is not a completed episode.

Delivery checkpoints store reserved file IDs in Assets and bind each request to its media digest. Retries reuse those IDs; different content under an existing request ID is rejected. Preview videos go to Assets; final masters go to Renders. Final QA reports bind to the master checksum. Existing files are not deleted and sharing is not changed.

Preview: https://drive.google.com/file/d/1SUq-SXkn9MWmTWnSKZWliqL0UViMJR_g/view

Run: https://github.com/kingbasco/Creator-OS/actions/runs/36702338903

## Remaining production work

1. Generate or supply V04 narration after provider quota and cost limits are configured. The narration package must match the transcript.
2. Configure billing/quota and numeric cost limits before unattended AI calls.
3. Connect scheduled monitoring to production with durable stage claims and checkpoints for research, scripts, narration and rendering. Delivery checkpoints and upload/calendar verification are implemented; full production orchestration is still pending.
4. Exercise a complete episode run, verify the master and saved links, then enable scheduled production. Publishing requires human approval.

GitHub schedules may be delayed and public-repository schedules can be disabled after 60 days of repository inactivity. Inspect Actions if an expected daily check is absent. Disable the workflow in Actions to stop monitoring; revoke the Google connection and remove secrets to stop account access.
