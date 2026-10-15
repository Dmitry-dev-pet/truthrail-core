import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from truthrail_core.llm_routing import (
    LLMRouteError,
    validate_llm_request_policy,
    verify_llm_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "capabilities" / "llm-routing-v1.schema.json").read_text())
REQUEST = json.loads((ROOT / "examples" / "llm-request-v0.1.json").read_text())
RECEIPT = json.loads((ROOT / "examples" / "llm-receipt-v0.1.json").read_text())


class LLMRoutingTests(unittest.TestCase):
    def setUp(self):
        self.validator = Draft202012Validator(SCHEMA)

    def test_schema_and_examples(self):
        Draft202012Validator.check_schema(SCHEMA)
        self.validator.validate(REQUEST)
        self.validator.validate(RECEIPT)
        validate_llm_request_policy(REQUEST)
        verify_llm_receipt(REQUEST, RECEIPT)

    def test_model_publisher_is_separate_from_reseller(self):
        req = copy.deepcopy(REQUEST)
        req["selection"]["access"].update(
            provider="openrouter", provider_kind="reseller", route_id="reviewed-broker"
        )
        self.validator.validate(req)
        validate_llm_request_policy(req)

    def test_http_gateway_cannot_read_workspace(self):
        req = copy.deepcopy(REQUEST)
        req["selection"]["access"]["transport"] = "gateway"
        req["input_policy"]["mode"] = "github-read"
        req["input_policy"]["tool_profile"] = "workspace_read_only"
        self.validator.validate(req)
        with self.assertRaises(LLMRouteError):
            validate_llm_request_policy(req)

    def test_evidence_only_never_has_tools(self):
        req = copy.deepcopy(REQUEST)
        req["input_policy"]["tool_profile"] = "workspace_read_only"
        with self.assertRaises(LLMRouteError):
            validate_llm_request_policy(req)

    def test_restricted_data_requires_approval(self):
        req = copy.deepcopy(REQUEST)
        req["input_policy"]["classification"] = "restricted"
        with self.assertRaises(LLMRouteError):
            validate_llm_request_policy(req)
        req["input_policy"]["approval_ref"] = "approved-operation://example"
        validate_llm_request_policy(req)

    def test_schema_rejects_unknown_gateway_authority(self):
        req = copy.deepcopy(REQUEST)
        req["selection"]["access"]["arbitrary_shell"] = True
        self.assertFalse(self.validator.is_valid(req))

    def test_no_silent_model_or_reseller_substitution(self):
        for name, value in (
            ("model", {"publisher": "other", "id": "another-model"}),
            ("access", {
                "provider": "broker", "provider_kind": "reseller",
                "route_id": "other", "transport": "reviewed_worker",
            }),
        ):
            receipt = copy.deepcopy(RECEIPT)
            receipt["actual_selection"][name] = value
            self.validator.validate(receipt)
            with self.assertRaises(LLMRouteError):
                verify_llm_receipt(REQUEST, receipt)

    def test_approval_required_does_not_implicitly_allow_fallback(self):
        req = copy.deepcopy(REQUEST)
        req["selection"]["fallback_policy"] = "approval_required"
        receipt = copy.deepcopy(RECEIPT)
        receipt["actual_selection"]["fallback_policy"] = "deny"
        with self.assertRaises(LLMRouteError):
            verify_llm_receipt(req, receipt)

    def test_executed_is_not_verified(self):
        receipt = copy.deepcopy(RECEIPT)
        receipt["verification"]["state"] = "unverified"
        with self.assertRaises(LLMRouteError):
            verify_llm_receipt(REQUEST, receipt)
        receipt["verification"]["state"] = "verified"
        receipt["verification"]["evidence_refs"] = []
        with self.assertRaises(LLMRouteError):
            verify_llm_receipt(REQUEST, receipt)

    def test_budget_ceiling(self):
        req = copy.deepcopy(REQUEST)
        req["budget"] = {"currency": "USD", "max_amount": 0.05}
        receipt = copy.deepcopy(RECEIPT)
        receipt["usage"]["charged_amount_usd"] = 0.10
        with self.assertRaises(LLMRouteError):
            verify_llm_receipt(req, receipt)

    def test_no_secrets_or_resolved_endpoints_in_examples(self):
        for fixture in (REQUEST, RECEIPT):
            payload = json.dumps(fixture).lower()
            for forbidden in ("api_key", "authorization", "bearer", "secret", "https://"):
                self.assertNotIn(forbidden, payload)


if __name__ == "__main__":
    unittest.main()
