# Changelog

## 0.5.0 — 2026-10-15

- consolidate Python modules, JSON Schemas and the CLI under the Truthrail namespace; remove the transitional implementation and package aliases;
- use a single canonical instance configuration and directory, and move example and demo identifiers to Truthrail;
- audit all portable skills, their contract references, bundle declarations and security boundaries;
- align installation, tests, CI and documentation; this is a breaking name/identifier migration for integrations pinned to older releases.

## 0.4.1 — 2026-10-09

- use the canonical Truthrail name in portable skill descriptions and headings while preserving legacy technical identifiers, imports and GitHub routes;
- add a regression check preventing the deprecated product label from resurfacing in portable skill instructions.

## 0.4.0 — 2026-10-08

- enforce v0.2 task, project, acceptance-proof, execution-ceiling, approval, capability and handoff-scope consistency across a complete run snapshot;
- bind plans to the WorkPacket and authoritative preconditions, receipts to exact plans, verification to exact receipts, and terminal verified transitions to passing verification;
- require evidence for every verified acceptance check and reject incomplete or duplicated run documents;
- add explicit freshness checks that require current provider inputs, without confusing an authorized operation's post-state with stale preconditions;
- add negative protocol tests and a local Git HEAD-change test; these do not claim full AI-host or distributed exactly-once coverage;
- preserve v0.1 schemas and behavior; document the intentionally stricter v0.2 migration in `docs/execution-binding-v0.2.md`.

- add portable opt-in operator skills for actionable attention triage, bounded daily briefs, and authoritative quota/capacity warnings;
- add CI coverage that every declared assistant skill resolves to a matching portable `SKILL.md` contract.

## 0.3.0 — 2026-10-07

- define explicit assistant / private-instance / Core / capability boundaries;
- introduced the canonical Python namespace `truthrail_core` with transitional aliases at the time;
- introduced the preferred `truthrail` CLI alongside a temporary compatibility command;
- limited historical technical identifiers to compatibility surfaces during migration;
- keep protocol schema 0.2 and the `executed -> verifying -> verified` lifecycle unchanged.

## 0.2.0 — 2026-10-06

- release the public package as Truthrail Core 0.2.0;
- make the execution/verification boundary explicit: `executed` is not success, and a run reaches lifecycle `verified` only after verification evidence passes;
- document the portable GitHub run-ledger pattern with compact bounded resume checkpoints;
- document optional Truthrail Watch lifecycle advisories as review-only signals that never authorize writes or automatic status changes;
- clarify public developer-preview positioning: AI chat as interface, disposable sessions, durable external state, and no required always-on local computer;
- add a reproducible two-chat fresh-session continuity demo and refresh public Truthrail naming/CLI examples;

- add additive work continuity v0.2 schemas with stable `run_id` across WorkPacket, plan, receipt, verification, handoff, and lifecycle documents;
- add source-channel and approval-policy metadata plus waiting/rejected/failed/cancelled lifecycle outcomes;
- add mixed-run bundle validation and explicit CLI schema-version selection while preserving v0.1 defaults;

- add runtime operation admission v1 with ADMIT / REQUIRE_HUMAN / DENY decisions;
- add explicit per-operation admission mode/requester metadata and fail-closed semantics;
- add machine-readable `capabilities/admission-v1.yaml`, decision schema, CLI and tests;

- add deterministic capability policy v1 with PASS / REVIEW / BLOCK decisions;
- publish machine-readable `capabilities/policy-v1.yaml`;
- add `truthrail capability-policy` with optional CI enforcement thresholds;

- add deterministic reviewed-control-plane capability diffs with Markdown/JSON output;
- add explicit operation metadata for GitHub permissions, network destinations, external side effects, cost ceilings, human gates, runtime auth and execution venues;
- add optional `--fail-on-expansion` CI policy without making blocking the protocol default;

- adopt **Truthrail** as the product name with the tagline `One source of truth. Any AI.`;
- introduced the preferred `truthrail` CLI with a transitional compatibility alias;
- keep legacy Python package, on-disk paths, and schema identifiers stable during the rename;

- add progressive capability readiness states: ready / degraded / dormant / blocked;
- add machine-readable `capabilities/contract.yaml`;
- add executable `capability_readiness` and `capability_activation_receipt` schemas;
- separate optional capability activation from core Core onboarding;
- add portable activation skill, examples, semantic validation and tests;
- add brownfield-first onboarding protocol with DISCOVER → CLASSIFY → BUILD → VALIDATE → WATCH → RECEIPT phases;
- add machine-readable `onboarding/contract.yaml` and portable bootstrap skill;
- add executable `onboarding_receipt` schema with verified / partial / blocked semantics;
- require complete discovered-repository coverage and successful fresh-session recovery for verified/partial receipts;
- add onboarding examples and acceptance tests.

## 0.1.1 — 2026-09-30

- add zero-custom-secret instance bootstrap;
- add `validate-instance` and `doctor`;
- default to public GitHub reads, optional ambient GitHub auth, and provider-managed
  GitHub Actions credentials;
- reject secret-value fields from instance credential metadata;
- add deterministic second-instance bootstrap acceptance to CI.

## 0.1.0 — 2026-09-30

Initial public core:

- executable v0.1 JSON Schemas;
- semantic protocol validator;
- L0-L5 reference routing adapter;
- reviewed control-plane contract schema;
- deterministic end-to-end conformance scenario;
- CLI;
- generic installation examples and agent skills;
- public-tree hygiene audit.
