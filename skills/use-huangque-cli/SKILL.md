---
name: use-huangque-cli
description: Discover and safely run all Huangque AI capabilities through the `hq` CLI. Use when a user asks an Agent to inspect Huangque capabilities or account data, collect public content such as Bilibili posts or videos, generate media, manage supported assets or projects, open a Huangque workbench, or automate a Huangque workflow while preserving login, confirmation, quote, idempotency, and revision safeguards.
---

# Use Huangque CLI

## Select one client

1. Locate `hq` from `PATH`; on Windows use `Get-Command hq`.
2. Run `hq version --json` and keep using that exact executable for the task.
3. If it is missing or incompatible, show the reviewed, version-pinned installer and ask before changing the machine.
4. Run `hq doctor --json` before account-bound work.
5. If authorization is absent or expired, run `hq login --json` and let the user finish device approval. Never request a password, Cookie, API key, or token.

## Discover the live contract

Run:

```sh
hq capabilities --json
hq describe <capability> --json
```

Treat those outputs as authoritative. Do not guess undocumented capability IDs, fields, URLs, providers, limits, methods, or costs. A navigation capability only returns or opens a Huangque page; it does not prove that a generation, order, payment, upload, or Bot change occurred.

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
