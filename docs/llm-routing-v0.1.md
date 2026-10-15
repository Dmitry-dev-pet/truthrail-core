# Vendor-neutral LLM routing contract v0.1

Truthrail is a router, not a second agent or a universal inference daemon.
LLM is a logical capability. Model publishers, access/billing providers,
transports, and model-tool authority are deliberately separate.

Portable documents:
- `capabilities/llm-routing-v1.schema.json`: request/receipt shape.
- `truthrail_core.llm_routing`: pure safety checks and exact receipt binding.
- `examples/llm-request-v0.1.json` and `examples/llm-receipt-v0.1.json`: synthetic fixtures.

## How selection works

A caller declares three independent choices:

1. **Model**: `selection.model.publisher` (Google, Anthropic, OpenAI, etc.)
   and concrete `selection.model.id`. Marketing model names are not verified IDs.
2. **Access provider**: `selection.access.provider` is the entity/account
   delivering or billing access. `provider_kind` distinguishes `direct`,
   `reseller`, and `subscription_adapter`.
3. **Execution route**: `selection.access.route_id` points to a separately reviewed,
   instance-owned allowlisted route. Transport separates `gateway` and
   `reviewed_worker`.

`fallback_policy: deny` rejects substitutions. `approval_required` does **not**
authorize an automatic fallback: the caller must create a new explicitly
bound request with approved selection. Any resulting different model,
provider, route, or fallback policy fails exact receipt matching.

The same model publisher reached through a direct API, reseller, and CLI
subscription adapter represents three different trust/billing choices.

## Data, tools, and secret boundary

`evidence-only` supplies bounded evidence and forbids tools. In v1,
HTTP gateways cannot receive repository workspaces, even if their upstream
provider supports tool APIs. `github-read` requires a reviewed worker
operating on an immutable, approved, read-only workspace snapshot.

Restricted input requires an approval reference. Private data additionally
requires the owning executor to verify the upstream recipient and declared
data-sharing scope before forwarding it. A route ID never grants filesystem,
network, shell, GitHub, or credential authority.

Request envelopes contain no credentials or raw arbitrary endpoint URLs.
The private instance owns route allowlists and credential metadata, while
each executor/provider stores its own secret values.

## Independent verification

An owning executor validates current entitlement, model availability,
spend limits, authorization, and route health. `status: executed` is not
verified. `verify_llm_receipt()` checks binding and declared evidence, but
the verifier must independently inspect that live source; arbitrary
evidence references are not proof of successful inference.

Budget metadata is a maximum allowed charge, not spending authorization.
Real charges are enforced at the upstream provider/control plane.

## Compatibility and activation

Model-specific workers can remain implementation adapters under LLM without
changing existing workflow triggers or relocating OAuth credentials.
Registering the logical LLM capability creates no new agent-routable
operation and does not enable an unauthenticated proxy or a new reseller.
Any new external route requires its own reviewed activation and real
authenticated inference smoke test before it can be used.
