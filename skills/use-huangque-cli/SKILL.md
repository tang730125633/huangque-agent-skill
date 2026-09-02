---
name: use-huangque-cli
description: Discover and safely run all Huangque AI capabilities through the `hq` CLI. Use when a user asks an Agent to inspect Huangque capabilities or account data, collect public content such as Bilibili posts or videos, generate media, manage supported assets or projects, open a Huangque workbench, or automate a Huangque workflow while preserving login, confirmation, quote, idempotency, and revision safeguards.
---

# Use Huangque CLI

## Select one client

1. Locate `hq` from `PATH`; on Windows use `Get-Command hq`.
2. Run `hq version --json` and keep using that exact executable for the task.
3. If it is missing or incompatible, show the reviewed, version-pinned installer and ask before changing the machine.
4. Run `hq status --json` before account-bound work.
5. If authorization is absent or expired, run `hq login --json` and let the user finish device approval. Never request a password, Cookie, API key, or token.

## Discover the live contract

Run:

```sh
hq capabilities --json
hq describe <capability> --json
```

Treat those outputs as authoritative. Do not guess undocumented capability IDs, fields, URLs, providers, limits, methods, or costs. A navigation capability only returns or opens a Huangque page; it does not prove that a generation, order, payment, upload, or Bot change occurred.

## Website parity actions

CLI 0.15.0 exposes normal-user website actions as fixed, typed capabilities instead of an arbitrary URL or method proxy. Always describe the exact action before use.

- Creator Agent, invitation, notifications, friends, profile, asset management, canvas members, digital-IP reports, and short-drama project/script/character/scene/autodraft/refinement actions use their dedicated capability IDs and live schemas.
- Use `profile-avatar-upload` and `video-import` with one explicit `--file`; use `asset-batch-download` or `creator-agent-background-pdf` with one new absolute `--output` path. Never place a local path inside JSON.
- Read the latest project/workspace before a short-drama write. Preserve the exact `revision`, `project_revision`, `graph_revision`, `version_id`, `shot_key`, `plan_id`, or `request_id` required by `describe`; do not substitute similarly named IDs.
- `task-delete`, member removal, asset deletion, project mutation, and all other writes still require explicit confirmation.
- Password changes, point transfers that require a password, payment confirmation, local browser preferences, clipboard/QR rendering, and canvas JPG export remain browser handoffs. Never accept a password, payment credential, OTP, Cookie, or API key through CLI input.

If a visible website action has no direct capability, inspect the live backend contract. Do not claim parity from `website_operations` metadata or a navigation link alone.

## Template videos

For a template-video request, use this workflow only when the live capability discovery contains these template capabilities. First read the live template contract and catalog, then inspect the operation being used:

```sh
hq run matrix-template-capability --json
hq run matrix-template-templates --json
hq describe matrix-template-generate --json
# or, for a set of deliverables:
hq describe matrix-template-batch-generate --json
```

- Take `template_id`, and optional `font_family`, only from the live template results; take all other fields from the live description. Do not invent template IDs, fonts, prices, or input fields.
- Use `matrix-template-generate` for one deliverable. Use `matrix-template-batch-generate` only with its live-schema `count` set to 2-5.
- Quote the complete single or batch request once without `--confirm`, show the total, then submit that identical input once with `--confirm --quote-token <quote_token>` after explicit approval. Do not quote or confirm individual batch items separately.
- Preserve every returned `job_id` and the original `quote_token`. If a batch is partial or its result is unknown, keep accepted jobs and follow the returned structured recovery instruction; do not create a fresh batch.

## Digital-human one-click runs

Use this workflow only when live discovery reports the normal one-click actions as available. Do not substitute a Precision action or infer availability from the website UI.

1. Read `digital-human-oneclick-capability`, then describe the plan, consent, start, status, recover, and upload actions that the request needs.
2. Before either text or audio narration, create and preserve one stable client `dh-run-*` identifier. Use it as consent's `run_id` in both modes. Only audio narration also passes it to `digital-human-oneclick-audio-upload --run-id`; preserve the returned `audio_upload_id`. Upload only files the user explicitly selected, and use `digital-human-oneclick-material-upload` for customer images.
3. Follow this field routing exactly. Plan and start never accept a `run_id` field:

| Mode | Client run identity | Plan | Consent | Start |
| --- | --- | --- | --- | --- |
| `text` | create `dh-run-*`; no audio upload | `narration_mode=text`, `script`; no `run_id` | same `run_id`, `plan_digest`, `narration_mode=text`, `script` | stable `request_id`, `consent_token`, `plan_digest`, `narration_mode=text`, `script`; no `run_id` |
| `audio` | create `dh-run-*`; audio upload `--run-id` | `narration_mode=audio`, `audio_upload_id`; no `run_id` | same `run_id`, `plan_digest`, `narration_mode=audio`, `audio_upload_id` | stable `request_id`, `consent_token`, `plan_digest`, `narration_mode=audio`, `audio_upload_id`; no `run_id` |

4. Run `digital-human-oneclick-plan` and preserve its exact `plan_digest`. Record consent only for the same client run identifier, plan digest, portrait digest, voice choice, narration inputs, and material policy.
5. Create and preserve one stable `request_id`. Run `digital-human-oneclick-start` without `--confirm` to obtain the server quote. After approval, repeat the identical input with the same `request_id`, `plan_digest`, and returned `quote_token` plus `--confirm`.
6. Preserve both the server-returned `run_id` and the original `request_id`, then poll `digital-human-oneclick-status`. On a recoverable terminal step, call `digital-human-oneclick-recover` with that pair; never recreate completed or still-running children. Use abandon only when the user explicitly wants to stop future recovery.

No quote or unconfirmed start may create a paid task. If status says `needs_attention` or `refund_pending`, do not retry; wait for the same run's billing state to settle. Accept only owner-scoped uploads, platform-authorized material, or user-approved AI-generated fictional material, and never infer consent to use another person's face or voice.

## Director workflows

Use direct Director actions only when live discovery lists them as `available`:

```sh
hq run director-capability --json
hq describe director-script-generate --json
hq describe director-breakdown --json
hq describe director-breakdown-upload --json
hq describe director-scene-image-generate --json
hq describe director-scene-video-generate --json
hq describe director-scene-talking-generate --json
```

- Use `director-script-generate` for the main-site AI script workflow. Supply the topic or factual brief as `prompt`; use only the advertised style, duration, and platform enums.
- Use `director-breakdown` for one public Douyin or Xiaohongshu link, or a `urls` batch of at most five links. `reverse_prompt` accepts one link only.
- Use `director-breakdown-upload` for exactly one local image or video selected by the user. Inspect its live MIME and size constraints. First obtain a file-bound quote; this hashes the file locally without uploading it:

```sh
hq run director-breakdown-upload --file <absolute-path> --json
```

- Show the returned `cost` and wait for explicit approval. Then reuse the same file and `quote_token`, and pass the approved cost explicitly:

```sh
hq run director-breakdown-upload --file <absolute-path> --confirm \
  --quote-token <quote_token> --expected-cost <cost> --json
```

- Use `director-scene-image-generate` to render one to eight Director scene descriptions. Preserve the requested `scene`, `line`, `dur`, `ratio`, and `quality` fields exactly as advertised by the live schema.
- Scene video reuses the live video channel rules; scene talking reuses the live text-video template, style, voice, and material rules. Script, breakdown, scene image, scene video, and scene talking are quoted paid actions. Quote the complete input first, show the returned point cost, and submit the identical input once with `--confirm --quote-token <quote_token>` only after explicit approval.
- Local breakdown upload is also quote-then-confirm. The CLI derives a stable `Idempotency-Key` from the quote token. If the confirmed upload response is uncertain, retry only with the same file, quote token, and expected cost; do not obtain a new quote.
- Keep the returned `job_id` and poll `task`; do not create a new job merely because the task is slow.
- A local image or video is not a URL. Never put a local path into `director-breakdown`; use the dedicated upload command only.
- Use `director-chat` only after explicit confirmation because it calls external AI and creates a zero-point job. Poll that job; if its result contains a `production_offer`, show the frozen cost and confirm only that exact offer through `director-produce`.
- Create a durable workflow from an owned completed script/breakdown job or explicit storyboard with `director-workflow-create`. Preserve `workflow_id` and the latest `revision`; update with `director-storyboard-update`, and use `director-storyboard-export` for Markdown.
- Production and remake are server-owned runs: call the matching `*-plan` with confirmation, preserve `plan_digest`, then call `*-start` once without confirmation to obtain the server quote. After approval, repeat the identical start input with `--confirm --quote-token`. Poll `*-status`; call `*-recover` only for the same result-unknown run and the same `request_id`.

## Short-drama production

Use the staged actions only when the project and current revision come from live reads.

1. Use `short-drama-advisor` with `--confirm` for a platform-funded external-AI planning turn; preserve its `request_id` for an identical retry.
2. `short-drama-character-reference-generate` is paid: quote first, then confirm the identical project/revision/character input. Poll the returned job and lock only the completed `reference_version` with `short-drama-character-reference-confirm`.
3. Generate and confirm the production plan with `short-drama-preflight-plan` and `short-drama-preflight-confirm`; both are writes and require `--confirm`.
4. For each shot, call `short-drama-autodraft-preflight` with confirmation, then `short-drama-autodraft-quote`. Put that native quote token in `short-drama-autodraft-start` input and pass `--confirm`; preserve its `request_id` and poll only `short-drama-autodraft-status`.
5. Use `short-drama-delivery-quote`, then put that native quote token in `short-drama-delivery-start` and pass `--confirm`. Poll only `short-drama-delivery-status`.
6. Read `short-drama-completion-readiness`. Only the owner may pass its exact revision, final version, asset, and delivery hash to `short-drama-completion-confirm`; this is irreversible and requires explicit confirmation.

Never substitute a fresh quote, request ID, project revision, plan, shot, or delivery version when recovering an existing paid operation.

## No-watermark download

Use `dl` only with a media URL already returned by Huangque and one explicit absolute `--output` path. The client refuses redirects, symlinked parent directories, files over 2 GiB, and any existing destination. It sends a Channels decode key in a header rather than the URL. Downloading is free and never creates a generation job.

## Apply the confirmation gate

- Run navigation and reads after identifying the requested target.
- For external AI, uploads, and ordinary writes, require explicit user approval before passing `--confirm`.
- For paid actions, first run without `--confirm`, show the returned cost and points, and wait for explicit approval. Then repeat the identical input exactly once with `--confirm --quote-token <quote_token>`.
- Preserve the same `request_id` after an uncertain response. Use a new ID only for a genuinely new operation.
- Read the latest object before a concurrent write and preserve its `revision` or `base_version` when required.

Never turn a read request into a write, paid task, upload, public message, deletion, or retry of an uncertain create.

## Prepare exact input

Pass one UTF-8 JSON object through stdin or `--input @file`, within the schema from `hq describe`.

- For uploads, pass one explicit supported file with `--file`. Never scan directories, follow symbolic links, or expose local paths as generation input.
- For collection, pass exactly one supported public content URL. Reject copied share commands, prose containing a URL, credentials, local paths, unsupported hosts, and unusual ports.
- Follow the returned provider and channel constraints instead of relying on remembered model parameters.

## Verify delivery

- Check the exit code, JSON `schema`, capability ID, and returned task or resource ID.
- For asynchronous work, poll only the supported task capability until terminal. Do not resubmit merely because it is still running.
- For media, confirm that the requested artifact exists and is usable; a provider `completed` state alone is insufficient.
- Reconcile quote, debit, refund, and final status for paid work.
- Report the capability, confirmation used, task or resource ID, final status, delivered artifact, and remaining user action. Never print credentials.
