---
name: transcribe-recording
description: Transcribe audio files and recordings (interviews, voice memos, lectures, podcasts, call recordings) with OpenWhispr, then save the transcript as an OpenWhispr note, tidy it up or recap it. Use this skill first, before running any command or calling the connector's transcribe_audio tool, whenever the user asks to transcribe something or turn a recording into text or notes ("transcribe interview.m4a", "transcribe this voice memo for me", "get me a transcript of ~/Downloads/call.mp3", "turn these recordings into notes"). transcribe_audio can only carry clips of a few seconds. This skill uses the OpenWhispr command-line tool where Claude can run commands (Claude Code), and explains the desktop-app route everywhere else.
argument-hint: "<audio file> [--save to <folder>]"
---

# Transcribe a recording

Use the OpenWhispr command-line tool (`openwhispr`) to transcribe audio files, because it sends the file straight to OpenWhispr. The connector's `transcribe_audio` tool takes the audio inline in the tool call, as base64 text, and is capped at 3 MB, so every byte would have to pass through the conversation. That is only workable for a clip of a few seconds. Don't use it for real recordings.

## When commands can't run

In claude.ai chat or on mobile there is no way to run the CLI. Explain the alternative in two lines: open the file in the OpenWhispr desktop app, which transcribes it into a new note, then ask Claude about that note. The plugin's meeting recap and note search work on it from there.

## 1. Check the CLI

Run `openwhispr version`. The `transcribe` command needs version 0.3.0 or later.

If the command isn't found or is older, tell the user the install command and let them decide. Installing software on their machine is their call:

```bash
npm i -g @openwhispr/cli
```

It needs Node.js 20 or later.

## 2. Pick local or cloud

Run `openwhispr doctor`. It reports whether each backend can be reached.

| | Local (desktop app) | Cloud (`--remote`) |
|---|---|---|
| Needs | OpenWhispr desktop app open | Pro or Business plan, CLI signed in |
| Cost | Free | Counts toward 600 cloud minutes a month (beta) |
| Size | No limit | 4 MB per request. Larger files are split into 4-minute chunks, which needs `ffmpeg` installed |
| Privacy | Audio stays on the computer | Audio is uploaded to OpenWhispr. The file path is not |
| Extras | `--model <name>` picks a downloaded model | `--prompt` helps spell names |

Use local when the desktop app is reachable. Otherwise use cloud. Tell the user which one you're using and why.

If cloud isn't signed in, ask the user to run `openwhispr auth login` themselves. It asks for their OpenWhispr API key. The user creates one in the desktop app under Integrations → API keys, and it needs the `transcriptions:write` scope. Never ask the user to paste the key into the conversation.

## 3. Get names right (cloud)

For cloud runs, pass the names and jargon likely to come up in the recording with `--prompt`, for example `--prompt "Names: Sam Patel, Acme, Kubernetes"`. Take them from what the user says about the recording, or from their OpenWhispr dictionary (the connector's `list_dictionary`, or `openwhispr dictionary list`). Keep it to a few dozen of the most relevant terms. A short focused list helps more than the whole dictionary.

## 4. Transcribe

```bash
openwhispr transcribe "/path/to/recording.m4a" --format json
```

- **Quote paths** that contain spaces.
- **Formats:** wav, mp3, m4a, mp4 audio, ogg, flac and webm.
- **Video files:** if the CLI rejects one and `ffmpeg` is installed, extract the audio first with `ffmpeg -i in.mov -vn -c:a aac out.m4a`.
- **Long recordings** can take several minutes, since local runs allow up to 30. Use a long command timeout, and tell the user it's working.
- **Several files:** transcribe them one at a time and report each result.

**To save the transcript as a note** in the same step, add `--note --title "<title>" --folder "<folder name>"`:

- the folder must already exist, and `openwhispr folders list` shows the names;
- with no `--title`, the note is named after the file;
- the note lands in the account the backend uses: the desktop app's account for local, the signed-in account for cloud.

**Exit codes:**

| Code | Meaning | What to do |
|---|---|---|
| 2 | Backend unreachable | Open the desktop app, or use `--remote` |
| 3 | Not signed in, or the key lacks the scope | `openwhispr auth login` |
| 4 | Not found | Check the file path or folder name |
| 1 | Bad arguments | Read the message |

A plan error on cloud means the account isn't Pro or Business. Offer local instead.

## 5. Afterwards

Don't paste a long transcript into the chat unless the user asks. Show the first few lines, the length, and where it was saved. Then offer the useful next step:

- **Save it** as a note, if it wasn't saved already.
- **Tidy it up** into paragraphs with filler words removed, keeping the original wording available.
- **Recap it:** decisions, action items with owners and dates, and open questions. If it was saved as a note, the meeting-recap skill can write the recap back into OpenWhispr.
