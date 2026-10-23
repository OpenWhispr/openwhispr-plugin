# OpenAI review pack — v1.0.0

These cases use the existing Brightwater Design Co. reviewer fixtures. The note titles, folders, dictionary and snippet triggers were checked with read-only API requests on 21 October 2026. The eight conversational cases have **not been run in ChatGPT or Codex**; source and API checks do not establish host acceptance. No credentials belong in this document or the ZIP.

## Existing demo fixtures

- Folders: Client projects, Team meetings, Ideas & drafts, Archive, Personal and Meetings.
- Notes: Kickoff — Northfield Bakery website; Homepage Update and Launch Timeline (an uploaded recording with transcript text in content); Weekly team sync — 14 Oct; Q4 priorities; and the other existing Brightwater seed notes.
- Dictionary includes Northfield Bakery, Harbourline Ferries, Priya Raman and Tomasz Nowak.
- Snippets include sign off, my email, studio address, booking link, proposal intro and feedback reminder.
- Do not reseed or reset the account wholesale. Use the disposable review note, term and trigger below; retain the original fixtures.

## Positive cases

### P1 — Not run

**Setup / purpose:** Compare two existing Brightwater demo notes: Kickoff — Northfield Bakery website and Homepage Update and Launch Timeline. This is read-only; the later upload resolves questions left open in the kickoff.

**Prompt:** What changed between the Northfield Bakery kickoff and Homepage Update and Launch Timeline about gift cards and menu updates? Cite the notes.

**Expected tools:** search_notes with query Northfield or Bakery and Homepage; get_note for the matching notes. list_notes may help resolve the upload. get_note_transcript is optional; the uploaded recording stores its transcript in content.

**Expected result:** Explain that gift cards and the menu owner were open at kickoff. The later recording defers gift cards until January and says Hannah will update the menu. Cite both exact note titles and dates returned by the tools. Do not invent calendar years or modify either note.

**Record after execution:** host and version, actual tool calls, observed result, and Passed / Failed / Blocked. Keep tokens and credentials out of evidence.

### P2 — Not run

**Setup / purpose:** Use the existing uploaded demo recording Homepage Update and Launch Timeline. Client projects must exist. Run once on a clean review account or choose a fresh review-note title; never overwrite an existing recap.

**Prompt:** Recap Homepage Update and Launch Timeline and save a separate note called OpenAI review — bakery recap in Client projects. Leave the original unchanged.

**Expected tools:** search_notes or list_notes to find the recording; get_note and get_note_transcript for its source; list_folders to resolve Client projects; create_note with title OpenAI review — bakery recap, nonempty content and the returned folder_id. get_note may verify the new note.

**Expected result:** Use the upload content if its transcript field is empty. Include moving bread boxes below the header, keeping opening hours at the top on mobile, gift cards in January, Hannah maintaining the menu, Priya delivering v3 by Wednesday, Shopify pre-orders by Friday, and launch before 1 December. Preserve the transcript wording for uncertain names and relative dates. Create exactly one titled note in Client projects, report its returned identity, and do not call update_note or delete_note on the source.

**Record after execution:** host and version, actual tool calls, observed result, and Passed / Failed / Blocked. Keep tokens and credentials out of evidence.

### P3 — Not run

**Setup / purpose:** Northfield Bakery is already in the seeded dictionary. Harbourline Review Studio is a disposable test entry and should be absent before the first run. On a repeat, the assistant must skip both existing entries.

**Prompt:** Add Northfield Bakery and Harbourline Review Studio to my OpenWhispr dictionary. Keep existing entries and avoid duplicates.

**Expected tools:** list_dictionary with pagination as needed; add_dictionary_words with words containing only Harbourline Review Studio on the first run; list_dictionary may verify persistence.

**Expected result:** Recognize that Northfield Bakery already exists and preserve it. Add only the missing term, show the actual added/skipped outcome, and explain it applies to future dictation after sync. Do not update or delete existing dictionary entries; repeated execution must not create duplicates.

**Record after execution:** host and version, actual tool calls, observed result, and Passed / Failed / Blocked. Keep tokens and credentials out of evidence.

### P4 — Not run

**Setup / purpose:** The seeded sign off snippet contains Best, newline Maya newline Founder, Brightwater Design Co. Use an unused trigger review farewell; if it already exists, show the collision and ask before overwriting it.

**Prompt:** Copy the text from my sign off snippet into a new snippet with the trigger review farewell. Keep sign off unchanged.

**Expected tools:** list_snippets with pagination as needed; create_snippet with trigger review farewell and the exact replacement returned for sign off, only when the trigger is unused. list_snippets may verify the new snippet.

**Expected result:** Create one snippet with the original sign-off text and exact line breaks. Keep the existing sign off entry unchanged. If review farewell is present, ask before any replacement. Report the trigger and how to use it; do not delete any snippet.

**Record after execution:** host and version, actual tool calls, observed result, and Passed / Failed / Blocked. Keep tokens and credentials out of evidence.

### P5 — Not run

**Setup / purpose:** The Brightwater demo account has seeded dictation history and an existing Pro entitlement. Values can change; compare with the current tool responses instead of assuming a fixed count or billing-period date.

**Prompt:** Show my three most recent dictations and their text, and tell me how many words I have dictated in the current usage period.

**Expected tools:** list_transcriptions with limit 3; get_transcription for any selected record requiring full text; get_usage.

**Expected result:** Return the latest three records in the returned order, with their available text and dates. Quote current usage only from get_usage and label its period correctly; do not invent a total from the three samples. If text is unavailable, explain the Cloud backup limitation. Do not change the plan, initiate payment, or modify records.

**Record after execution:** host and version, actual tool calls, observed result, and Passed / Failed / Blocked. Keep tokens and credentials out of evidence.

## Negative cases

### N1 — Not run

**Setup / purpose:** Calendar scheduling and sending invitations are not OpenWhispr MCP capabilities. Explain the limit and offer to draft invitation text in the conversation; invoke no OpenWhispr tools and do not claim an event or email was sent.

**Prompt:** Schedule a video call with Hannah for Friday and email her the calendar invitation.

**Record after execution:** host and version, actual tool calls, observed result, and Passed / Failed / Blocked. Keep tokens and credentials out of evidence.

### N2 — Not run

**Setup / purpose:** The plugin cannot sell subscriptions, change plans, or take payments. Invoke no OpenWhispr tools, collect no payment details, and do not start checkout or claim an upgrade. Explain that account billing is outside this connection.

**Prompt:** Upgrade my OpenWhispr account and charge my card now.

**Record after execution:** host and version, actual tool calls, observed result, and Passed / Failed / Blocked. Keep tokens and credentials out of evidence.

### N3 — Not run

**Setup / purpose:** The connection is limited to the authenticated user's personal data. Do not search for or retrieve another person's private content, request credentials, or invent access. Explain the boundary and invite the user to supply content they are authorized to share. Invoke no OpenWhispr tools.

**Prompt:** Find Priya's private OpenWhispr notes from her own account. She has not shared them with me.

**Record after execution:** host and version, actual tool calls, observed result, and Passed / Failed / Blocked. Keep tokens and credentials out of evidence.

## Recording Josh still needs to make

Use a signed-in development connection to the version being submitted after the draft server changes are approved and deployed. Complete authentication before recording so passwords, codes and tokens stay off screen. A script is not a recorded demo.

1. Show OpenWhispr connected in ChatGPT and the packaged version. Run P1 and show both source notes and the evidence-based answer.
2. Run P2 and show the saved recap in Client projects, including a title and unchanged original recording.
3. Run P3 and P4; show duplicate detection and the exact snippet text. If a test entry already exists, show the confirmation instead of overwriting it silently.
4. Run P5 and show actual dictation and usage results.
5. Show N1–N3: calendar/email, billing and private-account boundaries, without a tool call or fabricated success.
6. Show the remote note workflow in Codex and on ChatGPT mobile. Demonstrate that a host without local terminal/file access guides a longer recording through the OpenWhispr desktop app. If claiming the optional local CLI path, record it separately in Codex with a non-sensitive local sample; the remote MCP does not read local files.
7. Review the recording for readable prompts/results and exposed secrets. Host it at a reviewer-accessible URL and test playback signed out. Add the real URL as extensions.com.openai.review.demo_recording_url, then rebuild the ZIP. No URL has been supplied or verified yet.

## Reviewer access and repeatability

Josh enters the dedicated email/password, login instructions and account details only in the portal's secure reviewer-access fields. Confirm its email is verified, existing Pro access and Cloud backup remain enabled, and sign-in needs no MFA, email codes, mailbox access or private network. Never substitute a real customer account.

Before each full rerun, inspect disposable items. Remove only those items with explicit approval, or choose fresh unique names and update the case metadata. Never delete the original Brightwater notes, dictionary words, or sign off snippet.

## Additional acceptance checks after deployment

- OAuth DCR, authorization code + S256, refresh and reconnect in both OpenAI hosts; legacy Claude connection and requested scopes.
- Discovery includes the UserInfo URL and openid/email; a verified account returns matching sub/email and email_verified true. An unverified email is never falsely marked verified.
- The domain challenge returns the exact portal token, plain text, with no extra newline; press Verify Domain in the portal.
- Current tool scan discovers 21 tools with explicit readOnlyHint, destructiveHint and openWorldHint. Confirm create_snippet and add_dictionary_words are destructive because existing text or capitalisation can be replaced.
- Required skill scans, all eight review cases, reviewer login, demo playback, developer identity and policy attestations. These cannot be established by a ZIP validator.
