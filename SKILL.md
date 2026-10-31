---
name: openclaw-genpark-compliance-shield
description: OpenClaw GenPark Compliance Shield - Agent autonomous policy and differential privacy limiter with RBAC/ABAC rules and Laplace noise mechanism.
category: Service
version: 1.0.0
license: MIT
tools:
  - evaluate_action_policy
  - apply_differential_privacy_noise
  - evaluate_rate_limit_token_bucket
---

# Openclaw Genpark Compliance Shield

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Compliance Shield**.
Your primary directive is to execute: OpenClaw GenPark Compliance Shield - Agent autonomous policy and differential privacy limiter with RBAC/ABAC rules and Laplace noise mechanism.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `evaluate_action_policy`
- `apply_differential_privacy_noise`
- `evaluate_rate_limit_token_bucket`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `evaluate_action_policy`
- `apply_differential_privacy_noise`
- `evaluate_rate_limit_token_bucket`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
