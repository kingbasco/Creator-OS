# V04 — MCP explained visually

78-second motion preview; eight scenes. Narrated timing is measured from generated audio rather than fixed preview timing. Existing Creator OS colors, Geist typography, vertical format, animated tool requests and returned results.

## Sources checked 30 September 2026
- https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture — host/client/server, tools/list, tools/call, resources, stateless metadata.
- https://blog.modelcontextprotocol.io/posts/2026-07-28/ — current specification.
Examples are illustrative, not screenshots of real customer data. MCP does not grant blanket permissions.

## Production
The preview contains no narration. It must not be marked Ready for review as a completed episode. Fresh Gemini narration is disabled unless CREATOR_OS_ALLOW_FRESH_TTS=true; do not enable until quotas and cost limits are configured. No automatic fallback model. The manual final workflow can reuse the saved narration package.

Subjective pronunciation and complete listening checks require human review; technical checks alone do not establish content approval.

## Drive delivery
The preview workflow runs when render-requests/v04.json changes on main. It verifies that V04 is the next queued episode before rendering. Preview files go to Assets, not Renders. A small delivery-state JSON in Assets stores a reserved Drive file ID and binds it to the request ID and media checksum. Retries use the same reserved ID. If content differs under the same request ID, delivery stops instead of creating another master; use a new revision request ID for deliberate replacements. No existing files are deleted or sharing permissions changed.

Drive delivery verifies file size, MD5 checksum, MIME type and destination after upload. Only then does it update the V04 Next Action cell to Review Prototype and save the link in that cell’s note. Preview status remains Queued. Final delivery uses Ready / Ready for review after narrated 4K media and loudness QA; human publishing approval remains required. Calendar content updates retain formatting and dropdowns. Concurrent human sheet edits are not transactional with Drive delivery; a failed calendar update can be recovered by rerunning delivery with the same media and request ID.

For reused narration, ZIP manifest.json and S01–S08.wav at the ZIP root. The manifest must include scriptSha256 for the exact src/content/v04.json bytes. Hydration remeasures mono 24 kHz, 16-bit WAV durations and rejects a transcript mismatch. Supply the private ZIP’s Drive file ID to the manual workflow in final mode. The workflow never invokes fresh Gemini TTS.
