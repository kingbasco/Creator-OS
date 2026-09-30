# Creator OS automation

## Active monitoring

`Creator OS daily queue check` runs daily at 08:17 Africa/Lagos (07:17 UTC), on relevant code changes, or through Run workflow. It uses the Google OAuth credentials stored in Actions secrets. One monitor runs at a time; each job is limited to five minutes. There are no third-party Python dependencies or AI calls.

It reads the Content Calendar and the Renders folder, skips completed episodes, waits if an episode is In progress, and selects the earliest publish-date Queued episode. Invalid dates and duplicated IDs stop the check. It scans all render-folder pages for existing episode MP4s, using episode metadata where available or bounded episode IDs in filenames, and reports production blockers. This is a duplicate warning/preflight, not a complete exactly-once production mechanism.

Read the result in Actions → Creator OS daily queue check → latest run → Summary. A successful monitor means the inspection worked, not that a video was produced. Expected production blockers appear in the summary without failing the read-only job. Failed API or malformed calendar checks fail the job.

No Google files or cells are modified. No video is rendered or published. No paid API is invoked. Production limits are not configured. Monitoring requires no recurring Next instruction.

## Verified access

The Google connection check passed on 30 September 2026: OAuth refresh, calendar read and edit capability, render-folder listing and upload capability. Actual writes have not been exercised by these checks.

## Remaining production work

1. Implement V04 script, narration and motion composition or a general episode template; current rendering is specific to V01–V03.
2. Configure billing/quota and numeric cost limits before unattended AI calls.
3. Implement durable episode/request state and checkpoints, persisted Drive IDs, upload verification, technical QA, and calendar updates. Reuse generated assets and allow at most two retries per failed stage.
4. Exercise a complete episode run, verify the master and saved links, then enable scheduled production. Publishing requires human approval.

GitHub schedules may be delayed and public-repository schedules can be disabled after 60 days of repository inactivity. Inspect Actions if an expected daily check is absent. Disable the workflow in Actions to stop monitoring; revoke the Google connection and remove secrets to stop account access.
