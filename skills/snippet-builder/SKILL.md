---
name: snippet-builder
description: Create and manage OpenWhispr snippets, the spoken trigger phrases that OpenWhispr expands into saved text while the user dictates, such as email sign-offs, addresses, booking links, boilerplate replies and templates. Use this whenever the user wants a voice shortcut, text expansion, canned response or "a snippet for…", wants to list, change or delete snippets, or mentions dictating the same text over and over.
argument-hint: "[text to expand, or the snippet to change]"
---

# Snippet builder

A snippet is a trigger phrase plus replacement text. When the user says the trigger while dictating, OpenWhispr types the replacement. Good snippets save real typing and never fire by accident.

How matching works:

- OpenWhispr looks for the trigger anywhere in each finished dictation, ignoring case, as whole words, and replaces every occurrence.
- Punctuation must match exactly. If transcription writes "sign-off" where the trigger says "sign off", nothing happens.
- When triggers overlap, the longest one wins.
- Triggers are also passed to transcription as spelling hints, along with the dictionary.

The OpenWhispr connector provides the tools used here (`list_snippets`, `create_snippet`, `update_snippet`, `delete_snippet`). If they aren't available, ask the user to connect OpenWhispr from the plugin's **Connectors** tab (claude.ai, Cowork) or with `/mcp` (Claude Code).

## 1. Pin down the text

Get the exact replacement text: the link, address, sign-off or paragraph.

- **Keep it exactly as given.** Preserve line breaks and punctuation, and don't "improve" it unless asked.
- **Size limit:** replacements can be up to 5,000 characters.
- **Templates:** if the text should vary each time, keep the fixed part in the snippet and tell the user what they'll fill in after it expands.

## 2. Choose a trigger

A good trigger is:

- **Short and speakable:** two to four plain words. A single common word fires too often.
- **Distinctive:** a phrase the user wouldn't say in normal speech, because it expands wherever it appears, even mid-sentence. "my invoice footer" or "insert home address" are safer than "address".
- **Easy to transcribe the same way every time:** no punctuation, digits or symbols. Avoid words transcription may hyphenate or merge ("follow up" vs "follow-up"), and rare names or homophones it may spell differently.
- **At most 80 characters**, the desktop app's limit.

If the user gave a trigger, use theirs, and mention a problem only if it's likely to misfire. Otherwise suggest one, or two if there's a real choice.

## 3. Check the existing snippets

Page through `list_snippets` with `limit` 500, passing `cursor` while `has_more` is true. Look for:

- **The same trigger**, compared case-insensitively. `create_snippet` with a trigger that already exists doesn't fail: it silently replaces that snippet's text. So never create one without checking first.
- **A trigger that contains, or sits inside, the new one** ("invoice footer" and "my invoice footer"). These can clash, so pick a different phrase.
- **A snippet with the same purpose**, such as an older version of the same link or address. Show its current text and ask whether to update it or add a second one. Updating is usually what people want.

## 4. Confirm, then save

- **Create directly** when the user gave both the trigger and the text, or clearly asked for an update with the new text.
- **Otherwise** show the trigger and the replacement and ask before saving.

**To create one:** call `create_snippet` with `trigger` and `replacement`.

**To change one:**

- find it by trigger, compared case-insensitively;
- show the current text next to the new one;
- call `update_snippet` with its `id` and only the fields that change. Renaming to a trigger that is in use, or was deleted in the last 30 days, is refused; suggest another phrase.

**To delete one:** show it, get a yes, then call `delete_snippet`. Never delete a snippet just to recreate it. Update it instead.

## 5. Tell them how to use it

Close with one line, for example: *Say "my invoice footer" while dictating and OpenWhispr types the full footer.*

Mention that it works in new dictations once the OpenWhispr app has synced.
