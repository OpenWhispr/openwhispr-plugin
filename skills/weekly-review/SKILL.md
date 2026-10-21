---
name: weekly-review
description: Review a week, or any date range, of the user's OpenWhispr notes and meetings, covering what happened, the decisions made and the action items and loose ends still open, grouped by folder, and optionally save the review back to OpenWhispr as a note. Use this for "weekly review", "what did I get done this week?", "summarize my meetings since Monday", "end-of-week recap", "what's still open from last week's calls?", monthly look-backs, or a Friday review routine. It looks back over what was captured. It is not for planning the week ahead from scratch, unless the user wants last week's open items carried forward.
argument-hint: "[date range, e.g. 'last week' or '1–15 Nov']"
---

# Weekly review

Turn a stretch of the user's OpenWhispr notes and meetings into a short review they can act on: what happened, what was decided, and what is still open.

The OpenWhispr connector provides the tools used here (`list_notes`, `list_folders`, `get_note_transcript`, `create_note`, `create_folder`). If they aren't available, ask the user to connect OpenWhispr from the plugin's **Connectors** tab (claude.ai, Cowork) or with `/mcp` (Claude Code).

## 1. Settle the window

Use the user's range if they give one. Otherwise:

- **"This week":** Monday to today.
- **"Last week":** the previous Monday to Sunday.
- **No range given:** the last 7 days.

Timestamps are in UTC. Use the user's local dates if you know their timezone. State the window at the top of the review, so a wrong guess is easy to spot.

## 2. Collect the notes

1. Call `list_folders` once and map folder IDs to names.
2. Page through `list_notes` with `limit` 20, passing `cursor` from each response. Notes come back newest first by creation date. Stop when a page reaches notes created before the window starts, or when `has_more` is false. Keep the page size small, because each item carries the full note text and transcript.
3. Keep the notes created inside the window. Notes created earlier but edited this week fall outside a creation-date scan. If the user wants those too, include any note whose `updated_at` is in the window and say so.
4. Skip empty notes, ones with no content and no transcript, which are often "Untitled" leftovers. Mention how many you skipped.

For each note, read the best available text:

- `enhanced_content`, the AI notes, when present;
- otherwise `content`;
- for meetings with neither, the `transcript` already in the list item. Call `get_note_transcript` only if that's missing.

In transcripts, `source: "mic"` is the user and `source: "system"` is the other people on the call. Ignore one-word fragments and background chatter.

## 3. Write the review

Keep it scannable. One line per item, real names and dates, nothing invented. If an owner or due date wasn't stated, write "owner not stated" rather than guessing.

```markdown
# Week of 3–9 Nov 2026

## Highlights
- 3–5 bullets: the most important outcomes of the week

## Meetings
- Mon 3 Nov — *Design standup*: agreed the Q1 priorities
- …

## Decisions
- …

## Open action items
- [ ] Owner — task — due date (from *note title*)

## Loose ends
- Questions raised but not answered, and things promised without a date

## By folder
- Work (4 notes), Clients (2), Ideas (3)
```

For a big window, more than about 40 notes, summarize folder by folder and keep **Highlights** to the top five. Say if anything was left out.

## 4. Offer to save it

Show the review first, then offer to save it as a note titled like "Weekly review — 3–9 Nov 2026":

- **Where:** the folder the user names. Otherwise use a "Weekly reviews" folder if one exists, or failing that their default **Personal** folder, and mention they can ask for a dedicated "Weekly reviews" folder (create it with `create_folder` only when they say yes).
- **How:** call `create_note` with a `title`, always (the desktop app can't import a note without one, and its syncing stalls), the review as `content`, and the folder's `folder_id`. Use the default `note_type`. The app shows notes in a Markdown editor: keep to `##`/`###` headings, bullets and `- [ ]` checkboxes, with a blank line between paragraphs.
- **Once saved:** confirm the title and folder. Don't paste the API response.

Save without asking only when the user already asked for it ("…and save it to my notes"). Save once: a note created from Claude doesn't update cleanly in the desktop app yet, so if the user wants changes, finish them in the chat before saving. Never edit or delete the notes being reviewed.
