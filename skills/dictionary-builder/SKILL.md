---
name: dictionary-builder
description: Add names, jargon, acronyms and product terms to the user's OpenWhispr dictionary so dictation and transcription spell them right, and fix or remove dictionary words. Use this whenever the user wants OpenWhispr to recognise or spell words correctly ("add our client names to my dictionary", "it keeps writing 'cooper netties' instead of Kubernetes", "teach OpenWhispr the terms in this brief", "add the names from this repo"), asks to review, tidy, fix or delete dictionary entries, or complains that names come out wrong in their dictations or meeting transcripts.
argument-hint: "[words, or where to find them]"
---

# Dictionary builder

OpenWhispr's custom dictionary is the list of words it should spell exactly: people, companies, products, places, acronyms and jargon. OpenWhispr passes the list to the transcription engine as spelling hints.

**A short list beats a long one.** Some engines read only part of a long list. On-device transcription, for example, reads roughly the last couple of hundred words' worth. The desktop app warns once the list passes about 550 characters. So add genuinely unusual words only, and leave everyday words out: they crowd out the words that matter without helping.

The OpenWhispr connector provides the tools used here (`list_dictionary`, `add_dictionary_words`, `update_dictionary_word`, `delete_dictionary_word`, and `search_notes` / `get_note_transcript` for mining meetings). If they aren't available, ask the user to connect OpenWhispr from the plugin's **Connectors** tab (claude.ai, Cowork) or with `/mcp` (Claude Code).

## 1. Gather candidate words

Work from whatever the user points at:

- **A list they typed:** take it as given. Step 2 still applies.
- **A document, email, brief or pasted text:** pull out names of people, companies, products and places that aren't household words, plus acronyms and domain terms with unusual spellings, such as "Kubernetes", "Ngozi Eze" or "Ballymaloe House".
- **A codebase or project folder** (when Claude can read files): product, company, service and library names the user would say out loud, and internal acronyms. Skip code identifiers such as `getUserId`, because people don't dictate those as written.
- **Their meetings or notes:** compare the names in note titles, participants and the existing dictionary with how the transcripts spell them. Propose the correct form for each mismatch, for example "Naka Mura" → "Nakamura".

Leave out ordinary words such as "invoice", "workshop" or "roadmap", generic terms and whole sentences. Keep the user's preferred spelling and capitalisation ("iOS", "McKinsey"). Add people by full name as one entry ("Ngozi Eze"), and add a first name on its own only if it's unusual and used alone.

## 2. Check what's already there

Page through `list_dictionary` with `limit` 500, passing `cursor` while `has_more` is true. Compare case-insensitively.

Leave words that already exist alone and list them as "already in your dictionary". Adding a word that differs only in capitalisation overwrites the existing entry's capitalisation, so never re-add one unless the user wants the casing changed.

## 3. Confirm, then add

- **The user typed an explicit list** and asked you to add it: add it without a confirmation round. It's exactly what they asked for.
- **You chose the words**, from a document, codebase or transcripts: show the list grouped as *People*, *Companies & products* and *Terms*, with anything you skipped and why, then ask before adding. The user should decide, since every word nudges future transcriptions.

Add everything in one `add_dictionary_words` call.

- **Per call:** up to 200 words.
- **Per word:** 1–100 characters, with no line breaks and no `<` or `>`.
- **Per account:** up to 5,000 entries.

Split bigger lists across calls. If the list is already long, suggest pruning stale entries alongside the new ones.

If the call is refused because the organisation's policy turns off cloud backup, say the dictionary can only be changed in the desktop app on that account.

Then report briefly, for example: "Added 9 words: Ngozi Eze, Ballymaloe House, … Already there: Kubernetes."

## 4. Fix or remove words

- **Fix a spelling:** call `update_dictionary_word` with the entry's `id` and the corrected word. If it's refused because the word is already used, the corrected spelling was probably deleted earlier, and OpenWhispr keeps deleted words reserved. In that case add the corrected word with `add_dictionary_words`, which restores it, then delete the misspelled entry.
- **Remove words:** show the exact entries first, get a yes, then call `delete_dictionary_word` for each.
- **Tidy-ups** ("clean up my dictionary"): suggest removing everyday words, near-duplicates ("Siobhan Kelly" next to "Shivon Kelly") and misspellings. Explain each suggestion and delete nothing without a yes.

## 5. Say when it takes effect

Tell the user the words are saved to their OpenWhispr account and apply to new dictations and transcriptions once the OpenWhispr app has synced. Recordings already transcribed don't change.
