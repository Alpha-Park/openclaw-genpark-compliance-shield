# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Compliance Shield - Agent Autonomous Policy & Differential Privacy Limiter
Standard Library only: math, random, typing, time.
Evaluates deterministic fine-grained RBAC/ABAC action policies, adds Laplace differential
privacy noise for privacy-preserving telemetry, and enforces token-bucket rate limits.
"""

import math
import random
import time
from typing import Dict, List, Any

class OpenClawGenParkComplianceShield:
    def __init__(self, default_epsilon: float = 1.0):
        self.default_epsilon = default_epsilon

    def evaluate_action_policy(self, action_payload: Dict[str, Any],
                               policy_rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates agent proposed action against fine-grained guardrail rules.
        Rules specify: rule_id, principal_role, allowed_actions, max_value_usd, forbidden_resources.
        """
        role = action_payload.get("role", "ANONYMOUS_AGENT")
        action = action_payload.get("action", "UNKNOWN")
        resource = action_payload.get("resource", "")
        value_usd = float(action_payload.get("value_usd", 0.0))

        violations = []
        matching_rules = []

        for rule in policy_rules:
            # Check principal match
            target_role = rule.get("principal_role", "*")
            if target_role != "*" and target_role != role:
                continue

            matching_rules.append(rule.get("rule_id", "rule_anon"))

            # Check action permission
            allowed = rule.get("allowed_actions", ["*"])
            if "*" not in allowed and action not in allowed:
                violations.append({
                    "rule_id": rule.get("rule_id"),
                    "type": "UNAUTHORIZED_ACTION",
                    "details": f"Action '{action}' is not in allowed list {allowed} for role '{role}'"
                })

            # Check value cap
            max_val = rule.get("max_value_usd")
            if max_val is not None and value_usd > float(max_val):
                violations.append({
                    "rule_id": rule.get("rule_id"),
                    "type": "SPENDING_LIMIT_EXCEEDED",
                    "details": f"Value ${value_usd:.2f} exceeds rule limit ${max_val:.2f}"
                })

            # Check forbidden resources
            forbidden = rule.get("forbidden_resources", [])
            for f in forbidden:
                if f.lower() in resource.lower():
                    violations.append({
                        "rule_id": rule.get("rule_id"),
                        "type": "FORBIDDEN_RESOURCE_ACCESS",
                        "details": f"Resource '{resource}' contains forbidden keyword '{f}'"
                    })

        if violations:
            has_critical = any(v["type"] in ["FORBIDDEN_RESOURCE_ACCESS", "UNAUTHORIZED_ACTION"] for v in violations)
            verdict = "DENY" if has_critical else "FLAG_FOR_OVERSIGHT"
        else:
            verdict = "ALLOW"

        return {
            "action_id": action_payload.get("action_id", "act_001"),
            "verdict": verdict,
            "is_authorized": verdict == "ALLOW",
            "matched_rules_count": len(matching_rules),
            "violations_count": len(violations),
            "violations": violations
        }

    def apply_differential_privacy_noise(self, value: float, epsilon: float = None,
                                         sensitivity: float = 1.0) -> Dict[str, Any]:
        """
        Adds pure Laplace differential privacy noise to a numeric telemetry measurement.
        Noise drawn from Laplace(0, sensitivity / epsilon) via inverse CDF sampling.
        """
        eps = epsilon if epsilon is not None else self.default_epsilon
        scale = sensitivity / max(1e-6, eps)

        # Inverse transform sampling for Laplace distribution:
        # u in (-0.5, 0.5), X = -scale * sgn(u) * ln(1 - 2|u|)
        u = random.random() - 0.5
        sgn = 1.0 if u >= 0 else -1.0
        # Guard against log(0)
        u_adj = max(-0.4999999, min(0.4999999, u))
        noise = -scale * sgn * math.log(1.0 - 2.0 * abs(u_adj))
        
        perturbed_value = value + noise
        theoretical_variance = 2.0 * (scale ** 2)

        return {
            "original_value": round(value, 4),
            "perturbed_value": round(perturbed_value, 4),
            "epsilon": eps,
            "sensitivity": sensitivity,
            "noise_added": round(noise, 4),
            "scale_parameter": round(scale, 4),
            "theoretical_noise_variance": round(theoretical_variance, 4),
            "dp_mechanism": "LAPLACE_MECHANISM"
        }

    def evaluate_rate_limit_token_bucket(self, entity_id: str, capacity: int,
                                         refill_rate_per_sec: float,
                                         current_tokens: float,
                                         tokens_requested: int = 1,
                                         elapsed_seconds: float = 1.0) -> Dict[str, Any]:
        """
        Evaluates token bucket rate limit: refills tokens based on elapsed time and grants/denies tokens.
        """
        refilled = min(float(capacity), current_tokens + refill_rate_per_sec * max(0.0, elapsed_seconds))
        if refilled >= tokens_requested:
            allowed = True
            new_tokens = refilled - tokens_requested
        else:
            allowed = False
            new_tokens = refilled

        return {
            "entity_id": entity_id,
            "capacity": capacity,
            "refill_rate_per_sec": refill_rate_per_sec,
            "tokens_requested": tokens_requested,
            "is_allowed": allowed,
            "tokens_remaining": round(new_tokens, 2),
            "tokens_deficit": round(max(0.0, tokens_requested - refilled), 2) if not allowed else 0.0
        }
