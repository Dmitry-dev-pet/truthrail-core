# Architecture lookup index — one-repository pilot

> **Experimental, partial, non-authoritative.** This is a navigation aid, not a replacement for the current source, `AGENTS.md`, requirements, tests, or live GitHub state. Do not use it to authorize operations or change safety policy. Do not auto-refresh or propagate this file to other repositories.

- **Inspected branch:** `main`
- **Source snapshot:** [`cff21b5f866adb99f00987e3808cb56e6d32c485`](https://github.com/Dmitry-dev-pet/truthrail-core/commit/cff21b5f866adb99f00987e3808cb56e6d32c485)
- **Scope:** selected entrypoints for seven concrete developer questions, **not** a complete C4 scan.
- **Confidence:** code locations and nearby tests manually checked against the pinned snapshot; test suite was **not executed** for this pilot.

## Critical source-layout warning

The public `truthrail_core` namespace is **mostly a compatibility/import surface**. For routing, admission, policy, instance bootstrap, CLI and generic validation, the actual implementation is in `agent_hub_core/`. See [admission alias](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/truthrail_core/admission.py#L1-L3), [reference alias](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/truthrail_core/reference.py#L1-L3) and [packaging tests](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/tests/test_packaging.py#L13-L21).

**Exceptions:** `truthrail_core/execution_binding.py` implements the v0.2 binding, and `agent_hub_core/execution_binding.py` re-exports it; `truthrail_core/llm_routing.py` also implements its own route safety checks.

## Task-to-source navigation map

| Developer question | Primary implementation and evidence | Independent check |
| --- | --- | --- |
| How is a project alias resolved and an agent-routable operation selected? | [ReferenceAdapter.resolve / hydrate / resolve_control_plane_operation](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/agent_hub_core/reference.py#L21-L98) | [Conformance test](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/tests/test_conformance.py#L6-L11) |
| Where is a control-plane operation denied before execution? | [evaluate_operation_admission](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/agent_hub_core/admission.py#L27-L65) (does not execute the action or read secret values) | [Wrong actor / operator-only checks](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/tests/test_admission.py#L46-L66) |
| How are newly expanded permissions and operations reviewed or blocked? | [diff_operation / diff_control_planes](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/agent_hub_core/capability_diff.py#L189-L235) and [evaluate_capability_policy](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/agent_hub_core/capability_policy.py#L48-L99) | [Human-gate and agent-routing checks](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/tests/test_capability_policy.py#L67-L106) |
| Where do protocol JSON validation and semantic safeguards run? | [load_schema / validate_document](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/agent_hub_core/validation.py#L54-L112) | [Schema and semantic validation tests](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/tests/test_validation.py#L18-L69) |
| What prevents a completed execution or receipt from being reused after preconditions change? | [assert_plan_current / assert_receipt_fresh](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/truthrail_core/execution_binding.py#L261-L291) | [Freshness and local Git change tests](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/tests/test_execution_binding.py#L322-L352) |
| How is an external LLM model, route and receipt verified? | [validate_llm_request_policy / verify_llm_receipt](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/truthrail_core/llm_routing.py#L21-L79) | [Access, approval and substitution tests](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/tests/test_llm_routing.py#L40-L90) |
| Where are CLI commands registered, and where is instance bootstrap implemented? | [CLI argument parser](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/agent_hub_core/cli.py#L29-L70); [init_instance](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/agent_hub_core/instance.py#L119-L136) | [Instance bootstrap checks](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/tests/test_instance_bootstrap.py#L16-L80); [Compatibility checks](https://github.com/Dmitry-dev-pet/truthrail-core/blob/cff21b5f866adb99f00987e3808cb56e6d32c485/tests/test_packaging.py#L12-L21) |

## Change detection for this pilot

The source commit pins every link above. Before using an answer operationally, check live `main` and the relevant source file/tests; a different commit does **not** automatically mean every entry is wrong.

For targeted invalidation, compare Git blob object IDs for the relevant paths at the pinned commit and current `main` (e.g. `git rev-parse cff21b5f866adb99f00987e3808cb56e6d32c485:truthrail_core/execution_binding.py` versus `git rev-parse main:truthrail_core/execution_binding.py`). If the blob differs, mark the corresponding entry **needs re-verification**, review the diff and test references, then refresh the index separately. This pilot does not install a watcher, hook, CI job or new agent.

## Value test (not yet a controlled benchmark)

In a fresh thread, compare lookup with this map against the ordinary process of reading `AGENTS.md`, relevant documentation, and searching code. For the following same three questions, record **source-read count, correctness, whether stale source was rejected, and time/token use where observable**:

1. Find the exact check rejecting a stale execution receipt after Git HEAD changes.
2. Find the implementation that rejects an AI-routable operation when permission expands.
3. Find the real `truthrail` CLI parser rather than only the compatibility wrapper.

No savings are claimed until both variants are actually run with the same questions. Reject this index if the maintenance and staleness burden outweigh the measured benefit.
