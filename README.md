# OpenWhispr for Claude

Work with everything you capture in [OpenWhispr](https://openwhispr.com) without leaving Claude. That covers meetings, notes, dictation history, your custom dictionary and snippets. This plugin pairs the OpenWhispr connector with six skills that show Claude how to use it well. Claude recaps a meeting and saves the recap back to OpenWhispr, finds what was said and where, teaches OpenWhispr new words, builds voice shortcuts, reviews your week, and transcribes recordings.

## What you can ask

| Skill | Try saying | What Claude does |
|---|---|---|
| **Meeting recap** | "Recap my call with Sam and save it." | Reads the meeting's transcript, writes up decisions, action items (who and by when) and open questions, then saves the recap to OpenWhispr. |
| **Ask my notes** | "What did we decide about the launch date?" | Searches your notes and meeting transcripts several ways and answers with the note's name and date. It also preps you before a meeting. |
| **Dictionary builder** | "Add the names in this doc to my dictionary." | Picks out names and jargon, skips words you already have, shows you the list, and adds them so dictation spells them right. |
| **Snippet builder** | "Make a snippet for my email sign-off." | Suggests a short trigger phrase that's easy to say and won't fire by accident, checks it doesn't clash, and creates it. |
| **Weekly review** | "What happened this week?" | Goes through the week's notes and meetings folder by folder, pulls out decisions and loose ends, and can save the review as a note. |
| **Transcribe a recording** | "Transcribe ~/Downloads/interview.m4a into my Clients folder." | Runs the OpenWhispr command-line tool on the file, saves the transcript as a note and offers a recap. Works only where Claude can run commands, such as Claude Code. |

In Claude Code each skill can also be started by name, for example `/openwhispr:meeting-recap` or `/openwhispr:weekly-review`.

## Set up

1. Add the plugin.
   - On claude.ai and in Cowork: **Customize → Plugins**.
   - In Claude Code: `/plugin install openwhispr --marketplace OpenWhispr/openwhispr-plugin`.
2. Connect OpenWhispr.
   - On claude.ai and in Cowork: from the plugin's **Connectors** tab.
   - In Claude Code: with `/mcp`.

   Then sign in with your OpenWhispr account. If you already added the OpenWhispr connector, the plugin uses the same one.
3. Optional, for **Transcribe a recording**: install the OpenWhispr command-line tool (`npm i -g @openwhispr/cli`, version 0.3.0 or later). The skill asks before installing anything. Transcription is free and runs on your computer while the OpenWhispr desktop app is open. Cloud transcription needs a Pro or Business plan.

Claude sees what is saved to your OpenWhispr account. Turn on **Cloud backup** in the desktop app (**Settings → Privacy & Data → Cloud backup**, on paid plans) so your notes, meetings and dictation history are included. Anything kept only on your device stays there. Search covers your personal notes, not team spaces.

## Data and privacy

- **What the plugin is:** written instructions (skills) plus a link to the OpenWhispr connector. It stores nothing, runs no code of its own, and sends nothing anywhere by itself.
- **The connector:** Claude reads and changes your OpenWhispr data only through it, at `https://mcp.openwhispr.com/mcp`, signed in with your own account. Claude changes or deletes notes, dictionary words or snippets only when you ask, and asks before replacing or deleting anything.
- **The command-line tool:** **Transcribe a recording** runs it on your computer. In local mode the audio stays on your computer and is transcribed by the OpenWhispr desktop app. In cloud mode the audio, but not the file's path, is uploaded to OpenWhispr's API (`api.openwhispr.com`) for transcription. A transcript you choose to save becomes a note in your account.
- **More detail:** see OpenWhispr's [privacy policy](https://openwhispr.com/privacy) and the guide to [connecting OpenWhispr to Claude](https://docs.openwhispr.com/help/ai-tools/connect-ai-tools).

## Support

Email [support@openwhispr.com](mailto:support@openwhispr.com) or open an issue in this repository.

## License

MIT. See [LICENSE](LICENSE).
