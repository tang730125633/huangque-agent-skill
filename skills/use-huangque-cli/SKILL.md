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

## Director workflows

Use direct Director actions only when live discovery lists them as `available`:

```sh
hq run director-capability --json
hq describe director-script-generate --json
hq describe director-breakdown --json
hq describe director-breakdown-upload --json
hq describe director-scene-image-generate --json
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
- Script, link breakdown, and scene-image generation are quoted paid actions. Quote the complete input first, show the returned point cost, and submit the identical input once with `--confirm --quote-token <quote_token>` only after explicit approval.
- Local breakdown upload is also quote-then-confirm. The CLI derives a stable `Idempotency-Key` from the quote token. If the confirmed upload response is uncertain, retry only with the same file, quote token, and expected cost; do not obtain a new quote.
- Keep the returned `job_id` and poll `task`; do not create a new job merely because the task is slow.
- A local image or video is not a URL. Never put a local path into `director-breakdown`; use the dedicated upload command only.
- `director-scene-video-generate` and `director-scene-talking-generate` are intentionally excluded. Do not describe them as available, do not substitute another video capability, and do not attempt the Director buttons “一键生成视频” or “一键生成口播”.

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
