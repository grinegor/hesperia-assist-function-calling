# Build Report

Project folder: `/Users/egorgrin/Desktop/tasklearn-tasks/2026-07-03-give-an-llm-access-to-external-apis-function-calling`

Task: Give an LLM Access to External APIs (Function Calling)

## What Was Built

- `tool_contracts.json` defines the exact approved Hesperia tools: `order_lookup`, `subscription_lookup`, and `knowledge_base_search`.
- `hesperia_assist/contracts.py` loads and verifies the machine-readable contracts.
- `hesperia_assist/validation.py` enforces required fields, strict formats, bounds, and prompt-injection guardrails.
- `hesperia_assist/router.py` routes model-selected tool calls only after contract validation and fails closed for missing, invalid, unsupported, or unsafe calls.
- `hesperia_assist/api_client.py` models managed-secret configuration, timeout/retry settings, response normalization, and controlled API failure handling.
- `hesperia_assist/openai_tools.py` exports strict OpenAI-compatible function tool definitions from `tool_contracts.json`.
- `e2e_tests.json` covers successful tool calls, invalid inputs, unsupported requests, prompt injection, and API failure.

## TaskLearn Requirements Coverage

- Define Tool Contracts: complete in `tool_contracts.json` and `hesperia_assist/contracts.py`.
- Implement Call Routing: complete in `hesperia_assist/router.py`.
- Secure API Access: complete in `hesperia_assist/api_client.py`, `.env.example`, `.gitignore`, and validation guardrails.
- Validate End-To-End: complete in `e2e_tests.json`, `scripts/run_e2e.py`, and `tests/`.

## Validation Summary

All planned local validation commands passed before publication:

- `python3 -m compileall hesperia_assist scripts tests`
- `python3 -m unittest discover -s tests`
- `python3 scripts/run_e2e.py`
- `python3 -m hesperia_assist.cli --tool order_lookup --arguments '{"order_id":"ord_1001","customer_id":"cus_100"}'`
- `python3 scripts/secret_scan.py`

## Publication

Publication is required because TaskLearn asks for `repo_url`.

Repository URL: `https://github.com/grinegor/hesperia-assist-function-calling`
