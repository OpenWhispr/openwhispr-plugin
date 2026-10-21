---
name: ask-my-notes
description: Answer questions from the user's OpenWhispr notes, meeting transcripts and dictation history, saying which note it came from and when. Use this whenever the user asks what was said, decided, promised or discussed ("what did we decide about the launch date?", "when is the next draft due?", "find the note where I dictated the pricing ideas", "what did Sam think of the proposal?"), wants a brief before a meeting with someone ("prep me for my call with Acme"), or wants to look anything up in OpenWhispr, even if they don't name OpenWhispr.
argument-hint: "[question]"
---

# Ask my notes

Answer the user's question from what they captured in OpenWhispr, and show where each answer came from so they can trust it and find the original.

The OpenWhispr connector provides the tools used here (`search_notes`, `get_note`, `get_note_transcript`, `list_notes`, `list_transcriptions`, `list_folders`). If none of them is available, tell the user to connect OpenWhispr first: on claude.ai or in Cowork from the plugin's **Connectors** tab, or in Claude Code with `/mcp`, then sign in with their OpenWhispr account.

This skill only reads. Don't create, edit or delete anything while answering. If a brief or answer is worth keeping, offer to save it as a note and wait for a yes. When saving, always give `create_note` a `title`, because the desktop app can't import a note without one.

## 1. Search more than once

`search_notes` combines meaning-based and keyword search over the user's notes, including meeting notes. One phrasing often misses, so run two or three searches, limit 10 each:

- the distinctive nouns: names, companies, products, places ("Acme pricing page");
- the likely wording in the note itself ("go live", "sign-off");
- a broader topic, if the first two come back thin ("website timeline").

Merge the results. The `score` values only rank results against each other, so a low number doesn't mean a poor match. Read the candidates to decide which ones answer the question.

**Search doesn't read meeting transcripts.** It covers titles, the user's typed notes and the AI summaries. Recorded meetings often keep everything in the transcript under a title like "Untitled Note". So for anything said in a meeting, also page through `list_notes`, which returns newest first and includes each note's `transcript`, and look for the names or terms in the transcripts. Keep `limit` around 20 and stop after the period the question covers, or about 60 notes.

For time-based questions ("last week", "yesterday's call", "in September"), use each note's `created_at`. `list_notes` pages newest first. Keep `limit` around 20, because every item carries the full note text and transcript.

## 2. Read the source before answering

Search results can hold a lot of text, but the answer has to rest on what the note actually says:

- **Typed or dictated notes:** `content` is the user's own text. `enhanced_content`, when present, is an AI-cleaned version.
- **Meeting notes** (`note_type: "meeting"`): `get_note_transcript` gives the exact words. When the transcript starts with `[` it is a JSON list of segments:
  - `source: "mic"`, speaker `you`, is the user;
  - `source: "system"` is the other people on the call, labelled `speaker_0`, `speaker_1` and so on (shown in the app as "Speaker 1", "Speaker 2"), or by name when `speakerName` is set;
  - segment `timestamp` values aren't reliable clock times, so don't quote them.

  Use a person's name only when the note or transcript establishes it, for example when someone is addressed by name. If one speaker label covers several people, say "someone on the call" rather than guessing.
- **Uploaded recordings** (`note_type: "upload"`): the transcript is in `content`.

Skip stray fragments in transcripts, such as single words, snatches of another language or background chatter. They're usually microphone noise.

Quote short exact phrases when the wording matters, for example "we can't ship until legal signs off".

## 3. Dictation history

`list_transcriptions` returns past dictations, newest first. It has no search, so scan pages of 100 for the terms, up to about the 300 most recent, and say how far back you looked.

Each dictation's `text` is empty unless the user turned on **Cloud backup** in the OpenWhispr desktop app. Without backup the cloud keeps only word counts and timing. If every `text` comes back empty, tell the user their dictations can't be searched from Claude until Cloud backup is on (in the desktop app: **Settings → Privacy & Data → Cloud backup**). Then answer from their notes.

## 4. Answer

Lead with the answer, then the source for each claim, by title and date, never by ID:

> The pricing page goes live on 4 November, once legal signs off the new terms. Sam owns the copy changes.
> — from *Pricing sync with Acme* (meeting, 2 Oct 2026)

- **Notes disagree:** show both with their dates and say which is newer. The newer one usually reflects the latest decision.
- **Nothing found:** say what you searched for, then suggest why. The note may use other words, live in a team space (search covers personal notes only), or have been kept only on the device and never backed up.
- **Never fill gaps from general knowledge** as if it came from their notes.

## Meeting prep

When the user wants a brief before talking to someone ("prep me for my call with Acme"), search for the person and the company, then read the most recent two or three notes about them. Brief in this order:

1. **Last time:** the date and what the conversation was about.
2. **Decided:** what was agreed.
3. **Open:** action items still outstanding, and who owes them.
4. **Unanswered:** questions that are still open.
5. **To raise:** what's worth bringing up this time.

Keep it to what the notes support, and offer to save the brief as a note in the relevant folder.
