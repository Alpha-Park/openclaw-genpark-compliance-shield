# -*- coding: utf-8 -*-
from client import OpenClawGenParkComplianceShield

shield = OpenClawGenParkComplianceShield()

# 1. Action Policy Evaluation
rules = [
    {
        "rule_id": "rule_procure_limit",
        "principal_role": "PROCUREMENT_AGENT",
        "allowed_actions": ["PURCHASE_COMPUTE", "RESERVE_INSTANCE"],
        "max_value_usd": 5000.0,
        "forbidden_resources": ["production-db-master", "admin-keys"]
    }
]

action = {
    "action_id": "act_tx_992",
    "role": "PROCUREMENT_AGENT",
    "action": "PURCHASE_COMPUTE",
    "resource": "gpu-cluster-spot-h100",
    "value_usd": 3200.0
}

eval_res = shield.evaluate_action_policy(action, rules)
print(f"Policy Evaluation: {eval_res['verdict']} (Authorized: {eval_res['is_authorized']})")

# 2. Differential Privacy Telemetry
dp = shield.apply_differential_privacy_noise(value=142.50, epsilon=0.8, sensitivity=2.0)
print(f"\nDP Perturbation: Original={dp['original_value']} -> Perturbed={dp['perturbed_value']} (Noise: {dp['noise_added']})")

# 3. Rate Limit Token Bucket
rl = shield.evaluate_rate_limit_token_bucket("agent_01", capacity=10, refill_rate_per_sec=2.0, current_tokens=3.0, tokens_requested=2, elapsed_seconds=0.5)
print(f"\nRate Limit Check: Allowed={rl['is_allowed']}, Remaining Tokens={rl['tokens_remaining']}")
