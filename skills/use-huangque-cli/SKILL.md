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
2. Upload only files the user explicitly selected. Use `digital-human-oneclick-material-upload` for customer images. For recording-driven narration, create one stable `dh-run-*` identifier and reuse it with `digital-human-oneclick-audio-upload --run-id`, plan, consent, and start.
3. Run `digital-human-oneclick-plan` and preserve its exact `plan_digest`. Record consent only for the same run, plan digest, portrait digest, voice choice, and material policy.
4. Run `digital-human-oneclick-start` without `--confirm` to obtain the server quote. After approval, repeat the identical input with the same `request_id`, `plan_digest`, and returned `quote_token` plus `--confirm`.
5. Preserve the returned `run_id` and poll `digital-human-oneclick-status`. On a recoverable terminal step, call `digital-human-oneclick-recover` with the original `run_id` and `request_id`; never recreate completed or still-running children. Use abandon only when the user explicitly wants to stop future recovery.

No quote or unconfirmed start may create a paid task. If status says `needs_attention` or `refund_pending`, do not retry; wait for the same run's billing state to settle. Accept only owner-scoped uploads, platform-authorized material, or user-approved AI-generated fictional material, and never infer consent to use another person's face or voice.

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
