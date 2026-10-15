"""Portable, no-I/O safety checks for an explicitly bound LLM route.

This module does not perform inference, look up credentials, or grant permissions.
Hosts validate envelopes against capabilities/llm-routing-v1.schema.json first.
"""

from collections.abc import Mapping
from typing import Any


class LLMRouteError(ValueError):
    """The route, result, or authorization binding is not acceptable."""


def _field(value: Mapping[str, Any], key: str) -> Any:
    if key not in value:
        raise LLMRouteError(f"missing required LLM contract field: {key}")
    return value[key]


def validate_llm_request_policy(request: Mapping[str, Any]) -> None:
    """Apply cross-field safety rules beyond the JSON Schema shape check.

    No provider, model, route, or executor is implicitly selected by this helper.
    """
    if _field(request, "schema") != "truthrail.llm.request.v1":
        raise LLMRouteError("unsupported LLM request version")
    selection = _field(request, "selection")
    policy = _field(request, "input_policy")
    transport = _field(_field(selection, "access"), "transport")
    mode = _field(policy, "mode")
    tools = _field(policy, "tool_profile")

    if mode == "evidence-only" and tools != "none":
        raise LLMRouteError("evidence-only requests must disable model tools")
    if mode == "github-read" and (
        transport != "reviewed_worker" or tools != "workspace_read_only"
    ):
        raise LLMRouteError("github-read requires a reviewed read-only worker")
    if transport == "gateway" and (mode != "evidence-only" or tools != "none"):
        raise LLMRouteError("HTTP gateways cannot acquire workspace tools")
    if _field(policy, "classification") == "restricted" and not policy.get("approval_ref"):
        raise LLMRouteError("restricted data requires an explicit approval reference")
    if _field(selection, "fallback_policy") not in {"deny", "approval_required"}:
        raise LLMRouteError("silent fallback is forbidden")


def verify_llm_receipt(request: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    """Require independent verification of the *exact* requested model and route.

    A different model/upstream/route requires a new approved request; a fallback
    setting never silently authorizes substitution. The owning control plane
    must independently check the evidence references against live execution.
    """
    validate_llm_request_policy(request)
    if _field(receipt, "schema") != "truthrail.llm.receipt.v1":
        raise LLMRouteError("unsupported LLM receipt version")
    if _field(receipt, "request_id") != _field(request, "request_id"):
        raise LLMRouteError("receipt references a different request")
    if _field(receipt, "status") != "executed":
        raise LLMRouteError("LLM request was not executed")
    if _field(receipt, "actual_selection") != _field(request, "selection"):
        raise LLMRouteError("model, provider, or route changed without a new request")

    verification = _field(receipt, "verification")
    if _field(verification, "state") != "verified":
        raise LLMRouteError("execution is not independently verified")
    if not _field(verification, "evidence_refs"):
        raise LLMRouteError("verified inference requires authoritative evidence")

    budget = request.get("budget")
    usage = receipt.get("usage") or {}
    if (
        budget is not None
        and "charged_amount_usd" in usage
        and usage["charged_amount_usd"] > budget["max_amount"]
    ):
        raise LLMRouteError("actual charge exceeds the selected request budget")
