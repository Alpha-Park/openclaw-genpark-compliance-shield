# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkComplianceShield

client = OpenClawGenParkComplianceShield()

TOOLS = [
    {
        "name": "evaluate_action_policy",
        "description": "Evaluates agent proposed action against fine-grained guardrail rules (RBAC/ABAC).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action_payload": {"type": "object"},
                "policy_rules": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["action_payload", "policy_rules"]
        }
    },
    {
        "name": "apply_differential_privacy_noise",
        "description": "Adds Laplace differential privacy noise to numeric telemetry values.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "value": {"type": "number"},
                "epsilon": {"type": "number"},
                "sensitivity": {"type": "number"}
            },
            "required": ["value"]
        }
    },
    {
        "name": "evaluate_rate_limit_token_bucket",
        "description": "Evaluates token bucket rate limiter for agent requests.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "entity_id": {"type": "string"},
                "capacity": {"type": "integer"},
                "refill_rate_per_sec": {"type": "number"},
                "current_tokens": {"type": "number"},
                "tokens_requested": {"type": "integer"},
                "elapsed_seconds": {"type": "number"}
            },
            "required": ["entity_id", "capacity", "refill_rate_per_sec", "current_tokens"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "evaluate_action_policy":
            res = client.evaluate_action_policy(args["action_payload"], args["policy_rules"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "apply_differential_privacy_noise":
            res = client.apply_differential_privacy_noise(args["value"], args.get("epsilon"), args.get("sensitivity", 1.0))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "evaluate_rate_limit_token_bucket":
            res = client.evaluate_rate_limit_token_bucket(args["entity_id"], args["capacity"], args["refill_rate_per_sec"], args["current_tokens"], args.get("tokens_requested", 1), args.get("elapsed_seconds", 1.0))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
