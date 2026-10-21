# OpenAI directory submission — draft

This reuses the existing OpenWhispr plugin and `https://mcp.openwhispr.com/mcp`.
It is preparation for the shared ChatGPT/Codex directory, not a submitted,
approved, or published OpenAI listing.

## Materials

- [Listing](listing.md): copy, capabilities, three prompts, URLs and branding.
- [Review pack](review-pack.md): five positive and three negative cases tied to
  the existing Brightwater demo data, plus the recording plan.
- [Release notes](release-notes-v1.0.0.md).
- [Validation](validation.md): checks and limits of the available evidence.

`plugin.json` holds the listing, review cases, no-commerce declaration, all-country
availability and release notes. The demo URL is deliberately absent until Josh
records and verifies a real walkthrough. The selected verified publisher name
must be confirmed in the portal; OpenWhispr is the draft name requested by Josh.

## Build the upload

From this repository:

```sh
python3 scripts/package-openai.py /absolute/output/openwhispr-1.0.0-openai-draft.zip
```

The archive contains only the portable `plugin.json`, `mcp.json`, the existing
icon, MIT license and six skills. It excludes `.claude-plugin`, `.mcp.json`,
submission notes, scripts, credentials, dependency folders and Git files.
Claude continues to use its original manifests in this same repository.
The shared skill wording is provider-neutral. There are no hooks or app references.

The MCP declaration explicitly selects OAuth with DCR through OpenAI's documented
server extension. Its base scopes include the existing nine data permissions
and `openid`/`email`; endpoints still come from the existing server's discovery.
No fixed credentials, header overrides or new MCP server are needed. Deploy the
draft identity support before connecting, then verify the portal's saved OAuth
method, DCR mode and requested scopes. Advanced auth settings come from the
package; the portal does not provide an advanced OAuth editor.

The generic Agent Plugins 1.0 MCP schema currently rejects the `extensions`
field shown in OpenAI's authentication examples. The package follows the OpenAI
submission documentation and records this schema conflict in the validation
report. Actual portal import and connection remain unverified.

## Required server work

- API: UserInfo and identity-scope discovery, preserving existing MCP scope
  defaults, PKCE, refresh and revocation. An unverified email must never be
  marked verified just to pass the portal check.
- MCP: configurable `OPENAI_APPS_CHALLENGE` at
  `/.well-known/openai-apps-challenge`, explicit safety flags on 21 tools,
  dictionary/snippet overwrite disclosure, and secure reconnect guidance on expired auth.
- Consent UI: explain identity and email scopes only when requested.

These are separate draft PRs. Their branches disable automatic Vercel deployments.
No branch is merged or deployed as part of submission preparation.

## Josh's portal checklist

Before a final review submission, separately review and authorize the server
and consent changes for deployment, then verify both OpenAI and Claude OAuth.
The package can be uploaded as a draft to obtain the challenge token first.

- [ ] Open https://platform.openai.com/plugins in the intended organization and
  project. Confirm owner access or Apps Management Write, and select/complete
  the verified business identity associated with OpenWhispr. The public legal
  pages identify Gizmo Labs Inc.; confirm which verified name the portal offers.
- [ ] Upload this ZIP as one plugin with its remote MCP included. If the portal
  offers a choice, use **With MCP**, not Skills only. Do not create another server
  or a duplicate plugin.
- [ ] Inspect imported name, descriptions, Productivity category, all countries,
  no commerce, icon, prompts, release notes and five positive/three negative cases.
- [ ] Under **MCPs → Connect**, obtain the domain-verification token. Configure it
  as `OPENAI_APPS_CHALLENGE` for the authorized MCP deployment, serve it exactly
  at `https://mcp.openwhispr.com/.well-known/openai-apps-challenge`, then choose
  **Verify Domain**. The token is not hard-coded or included in the ZIP.
- [ ] Confirm the imported authentication is OAuth, client mode is DCR, and all
  nine data scopes plus openid/email are present. Connect using the existing DCR
  flow. Complete the secure sign-in;
  check `openid`/`email` and the existing requested data permissions. Verify
  UserInfo returns the review account's real verified email. Confirm the current
  scan discovers all 21 tools and inspect the safety flags.
- [ ] In **Review information → Review details**, enter the dedicated reviewer
  email/password and sign-in instructions yourself. Confirm no MFA, email code,
  private network or other inaccessible step is required. Keep credentials out
  of chat, code, the ZIP and the recording.
- [ ] Run and record the eight cases, including the remote workflow on ChatGPT
  desktop/mobile and Codex. Keep demo data and the existing entitlement usable.
- [ ] Record and host the walkthrough described in the review pack. Verify that
  reviewers can play it without requesting access. Add its real URL to
  `review.demo_recording_url`, rebuild and upload the updated ZIP to the same draft.
- [ ] Resolve required metadata, skill and MCP scan findings. Review the selected
  version and complete the policy/legal attestations yourself, then **Submit for review**.
- [ ] Track review feedback. After approval, **Publish plugin** is a separate
  action; approval alone does not make it public.

## References checked on 21 October 2026

- [Bring an existing Claude plugin](https://developers.openai.com/plugins/guides/submit-claude-plugin)
- [Submission and metadata](https://developers.openai.com/plugins/deploy/submission)
- [Authentication and verified email](https://developers.openai.com/plugins/build/auth)
- [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)
- [Validation errors](https://developers.openai.com/plugins/deploy/submission-errors)

The current guidelines say annotation justifications are no longer required,
while the validation-errors page still mentions them. All three boolean safety
flags are required either way. Treat the actual portal findings as authoritative
for this draft; explain each tool's existing behavior if a justification is requested.
