---
name: meeting-recap
description: Recap a meeting recorded in OpenWhispr by pulling the decisions, the action items with owners and due dates, and the open questions from its transcript, then save the recap back into OpenWhispr. Use this whenever the user asks to recap, summarize or write up a meeting, call, interview, 1:1 or standup, or wants its action items, next steps, minutes or follow-ups ("recap my call with Sam and save it", "what were the action items from this morning's sync?", "write up yesterday's kickoff into my Clients folder"), including the most recent meeting when none is named.
argument-hint: "[meeting name, person or date]"
---

# Meeting recap

Turn an OpenWhispr meeting into a recap the user can act on, and save it where they'll see it: on the meeting itself, in OpenWhispr.

The OpenWhispr connector provides the tools used here (`list_notes`, `search_notes`, `get_note`, `get_note_transcript`, `list_folders`, `update_note`, `create_note`). If they aren't available, ask the user to connect OpenWhispr in their assistant's plugin or connection settings. Complete sign-in through the secure connection flow; never ask for a password, login code or API key in the conversation.

## 1. Find the meeting

Recorded meetings are often titled "Untitled Note" and keep everything in their transcript, and `search_notes` doesn't read transcripts. So:

- **The user names it** by person, company, topic or day: run `search_notes` with those words. Also call `list_notes` with `limit` 20, which returns newest first and includes each note's transcript, and look for the names or topic inside the transcripts of meeting notes.
- **They don't name one** ("recap my last meeting"): call `list_notes` with `limit` 10 and take the newest note that has a transcript.
- **More than one plausible match:** ask which one. Show each candidate's title, date and opening line, and nothing more.

## 2. Read everything about it

Call `get_note`, then `get_note_transcript`.

- **Notes:** `content` holds what the user typed during the meeting. `enhanced_content` is the meeting's **AI Summary**, which the app shows in its own tab.
- **Transcript format:** the transcript comes back as text. When it starts with `[`, it is a JSON list of segments, each with `text`, a `source` (`mic` is the user, `system` is everyone else on the call) and usually a `speaker`:
  - `you` is the user;
  - `speaker_0`, `speaker_1` and so on are other voices, shown in the app as "Speaker 1", "Speaker 2";
  - `speakerName`, when set, is a real name.
- **Times:** segment `timestamp` values aren't reliable clock times, so don't quote them.
- **Uploaded recordings** (`note_type: "upload"`) keep their transcript in `content`, sometimes as `[Speaker 1] 00:00 - 00:12` blocks.

Read it with care:

- **Names:** use a person's name only when the note or transcript establishes it, from `speakerName`, from the participants, or from people addressing each other ("Thanks, Alex"). When one speaker label covers several people, write "the client said…" or "someone on the call…" rather than guessing who spoke.
- **Noise:** skip stray fragments, such as single words, snatches of another language or background chatter. They are usually microphone noise, not part of the meeting.
- **No transcript and no content:** say so plainly and stop. Don't recap an empty note.

## 3. Write the recap

The desktop app shows saved text in a Markdown editor. Use `##` and `###` headings, bullets and `- [ ]` checkboxes, and put a blank line between paragraphs. Don't use deeper headings, images or HTML, which don't display.

Use this structure, and leave out any section with nothing in it:

```markdown
## Summary

Two or three sentences: what the meeting was for and where it landed.

## Decisions

- What was agreed, in plain words.

## Action items

- [ ] Send the revised proposal — Sam, by Friday 24 Oct
- [ ] Book the photo shoot — owner not stated

## Open questions

- What was raised but not settled.

## Key details

- Dates, numbers, names, links and deadlines mentioned, exactly as said.
```

- **Stick to what was said.** If an owner or date wasn't stated, say so rather than inventing one. Users act on these lists.
- **Dates:** keep relative ones as spoken, adding the calendar date only when the meeting date makes it certain.
- **Length:** keep it readable in a minute. Longer meetings get more items, not longer items.

## 4. Save it back

Save the recap when the user asked for that ("…and save it"). Otherwise show it and offer to save it in one line.

**Default: the meeting's own AI Summary.** Use it when both are true:

- the meeting came from the OpenWhispr app, so `get_note` shows a `client_note_id`;
- its `enhanced_content` is empty.

In that case call `update_note` with the note's `id` and the recap as `enhanced_content`. The recap then appears in the meeting's **AI Summary** tab, synced to the user's devices. Never touch `content`, which holds the user's own notes.

**The meeting already has an AI Summary:** show what's there and ask whether to replace it or save the recap as a separate note.

**A separate note:** use one when the user asks for it, when replacing was declined, or when the meeting has no `client_note_id` because it was created outside the app. Call `create_note` with:

- a `title`, always, such as "Recap: <meeting title> (<date>)". The desktop app can't import a note without a title, and its syncing stalls.
- `content`: the recap;
- `folder_id`: the meeting's folder, or the folder the user named. Find its ID with `list_folders`, and ask before creating one.

**Two rules for any save:**

- Never send an empty string for `content` or `enhanced_content`. An empty value deliberately clears that field on every device.
- Offer a better title for a meeting still called "Untitled Note", such as "Acme kickoff (21 Oct)", only if it came from the app. Rename it with `update_note` only after a yes.

**After saving:** confirm where the recap went in one sentence. Don't paste the API response.

Never delete the meeting, its transcript or any other note as part of a recap.
