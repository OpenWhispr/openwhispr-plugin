# Validation — 21 October 2026

**Status: prepared for a draft upload, not ready for final submission.** No
OpenAI portal scan, review submission, approval or publication has occurred.
Server and consent changes are draft PRs; they have not been deployed.

## Package and listing

| Check | Result |
| --- | --- |
| Manifest validation | `plugin.json` passes the published Agent Plugins 1.0 schema. The portable MCP transport/URL fields pass its MCP schema when checked separately. The complete MCP manifest includes OpenAI's documented OAuth/DCR extension, which the generic schema rejects because it disallows `extensions`; this is an unresolved documentation/schema conflict, not a full schema pass. |
| Archive | 10 allowlisted files, 764,208 bytes; safe relative paths, no duplicates, symlinks or extra wrapper directory. |
| Contents | One plugin, one existing remote Streamable HTTP MCP, six existing skills, MIT license and existing PNG. No hooks, apps, secrets, headers, dependencies or submission documents. |
| Claude compatibility | Original `.claude-plugin` manifests and `.mcp.json` remain in the source repository; plugin name/version and MCP URL match the portable package. No Claude runtime acceptance was performed on this branch. |
| Skills | All six frontmatter blocks parse; name/directory and description-length checks pass. No Claude/Cowork-specific instructions remain. Local transcription explicitly requires access to the user's computer and file. |
| Listing | Display name 10 characters; subtitle 29; long description 1,359; three distinct default prompts under 128 characters; nine capabilities; Productivity category. |
| Brand | Existing 1024 × 1024 PNG, 745,176 bytes, reused for logo and composer icon. `#1D4ED8` has 6.70:1 contrast against white. |
| Publication | All available countries (`[]`), no purchases/payments, initial v1.0.0 release notes. OpenWhispr is the provisional publisher name pending the selected verified portal identity. |
| Review metadata | Five positive and three negative cases with actual demo fixtures. No reviewer credentials in the source or ZIP. Demo URL is deliberately absent. |
| Authentication declaration | Explicit OAuth, DCR client mode, and the existing nine data scopes plus openid/email. Endpoint discovery is preserved. No static client ID, client secret, access token, headers or endpoint overrides. |

ZIP SHA-256:

```text
64378601e79e92483e93dfa1060bb488ec86d8d038f00596ce7026292a312d9b
```

Rebuild with `python3 scripts/package-openai.py /absolute/path/output.zip`.
The standard-library validator checks the final archive, including exact file
inventory, manifest limits, paths, URLs, icons, contrast and review-case structure.
The schema checks were separately run against the downloaded official
[plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and
[MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json) using
`jsonschema` 4.25.1. The full MCP schema rejection is retained as a finding;
validating the transport fields alone does not establish that the complete file
passes that schema. The auth extension is checked against the field names and
values in [OpenAI's authentication packaging reference](https://developers.openai.com/plugins/build/plugins#configure-mcp-authentication).
The [submission guide](https://developers.openai.com/plugins/deploy/submission#configure-authentication-for-submission)
says advanced authentication settings are imported from the package. Portal
import, saved OAuth/DCR settings and connection must still be verified.

## Server and consent checks

| Area | Evidence and limit |
| --- | --- |
| API | 34 focused tests passed: existing OAuth parsing/flow plus 10 UserInfo tests using the PGlite database harness. Covers DCR, PKCE, verified/unverified email, scope-limited claims, existing Claude/default scopes, no privilege escalation, refresh, revoke, expired/invalid credentials, deleted/anonymous users and route metadata. Typecheck, changed-file ESLint, formatting and test-schema consistency passed locally on Node 25.8.0. The full Node 24 [CI test job](https://github.com/OpenWhispr/openwhispr-api/actions/runs/39607163959/job/119246229255) and CodeQL passed on API commit 537de832b78837174da1da7463d743059e831c0a. |
| MCP | Four tests passed using handler requests and an MCP SDK in-memory client. Checks exact configurable challenge response, absent token, HEAD/method handling, secure reconnect guidance, and all 21 tool names/annotations. ESLint and typecheck passed. The dictionary-add and snippet-create hints reflect existing upsert behaviour; no tool's implementation changed. |
| Consent | All 18 existing/new OAuth browser tests passed using installed Chrome via Playwright, including the new identity-scope labels, legacy Claude permissions, callbacks, error states, mobile layout and keyboard focus. This is a synthetic local fixture, not a real provider login. The fixture run includes a successful Next build. |
| Deployment prevention | Each hosted draft branch sets its own `git.deploymentEnabled` entry to `false`. No production configuration, environment variable or deployment was changed. |

The API provides the identity claims OpenAI documents as required for workspace
domain restrictions. It does not add ID tokens, JWKS or the optional
`id_token_hint` reauthorization optimization. `email_verified` reflects the
stored verification state; an unverified account returns `false`, never a
fabricated `true`.

## Read-only production checks

- Existing auth discovery and MCP resource metadata were reachable. The live
  auth discovery still advertises the original nine data scopes plus
  `offline_access`, without UserInfo or identity scopes.
- Live OpenID discovery and the OpenAI challenge URL returned 404, as expected
  before these draft changes are deployed. This is not an acceptance pass.
- The public help, contact, privacy and terms URLs were reachable. Their contents
  describe the connection and service; reachability is not legal approval.
- Existing reviewer demo note titles, folder names, dictionary words and snippet
  triggers were checked through read-only API requests. The uploaded recording's
  transcript is in `content`, so the cases explicitly account for that. No demo
  data was created, updated or deleted during preparation.

## Still unverified or missing

1. **Domain token and hosted challenge:** obtain the token from the draft's MCP
   connection step; configure the environment only with separately authorized
   deployment. Portal domain verification has not run.
2. **Real OAuth in OpenAI and regression in Claude:** deployed discovery, actual
   requested scopes, consent, callback, UserInfo, refresh, revoke/reconnect and
   resource checks require host testing. The reviewer account's real email
   verification and password-only login were not checked.
3. **OpenAI scans and execution:** the documented auth extension versus generic
   schema conflict, imported OAuth/DCR/scopes, skill scan, metadata, saved MCP scan,
   all 21 tools and the eight conversational cases in ChatGPT/Codex remain pending.
   ChatGPT mobile and the optional local CLI path were not exercised here.
4. **Reviewer access:** Josh must enter credentials directly in the secure portal
   fields and confirm entitlement, demo data and sign-in stay accessible to reviewers.
5. **Demo video:** no recording URL was supplied or played. The recording plan is
   in the review pack; do not submit a placeholder URL.
6. **Publisher and attestations:** organization/project permissions, verified
   identity, actual country availability, legal/policy declarations and approval
   are portal decisions. The selected verified name may differ from the draft
   OpenWhispr display name; public legal pages name Gizmo Labs Inc.

The current [guidelines](https://developers.openai.com/plugins/plugin-guidelines)
say annotation justifications are no longer required, while the
[validation-errors page](https://developers.openai.com/plugins/deploy/submission-errors)
still mentions them. The three explicit safety booleans are present. Follow the
current portal findings and provide behaviour-based explanations if requested.

## Sources and reuse

The approved Claude listing and original Brightwater demo seed were located in
the existing Claude session, then compared with the public plugin and live demo
fixtures. Copy was adapted for the new field limits and host-neutral wording;
no new service, UI widget or reviewer account was built. The public package does
not include session transcripts, seed files or account credentials.

Requirements checked: [Claude migration](https://developers.openai.com/plugins/guides/submit-claude-plugin),
[submission](https://developers.openai.com/plugins/deploy/submission),
[authentication](https://developers.openai.com/plugins/build/auth),
[review](https://developers.openai.com/plugins/deploy/app-review), and
[guidelines](https://developers.openai.com/plugins/plugin-guidelines).
