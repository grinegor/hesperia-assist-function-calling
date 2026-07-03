# Hesperia Assist Function Calling

This repository implements secure function-calling access for Hesperia Assist, an AI support copilot that may call only approved external APIs for order lookup, subscription lookup, and knowledge-base search.

## Deliverables

- `tool_contracts.json`: strict machine-readable contracts for the approved Hesperia tools.
- `hesperia_assist/`: routing, validation, API client, response parsing, and OpenAI-compatible function tool export.
- `e2e_tests.json`: structured success and failure scenarios for end-to-end validation.

## Security Model

- The approved tool set is fixed to `order_lookup`, `subscription_lookup`, and `knowledge_base_search`.
- The router fails closed when a tool is missing, unsupported, malformed, ambiguous, or unsafe.
- Arguments are validated before any API client execution.
- Secrets are read from environment variables and are never hard-coded.
- Timeout and retry settings are explicit in `tool_contracts.json` and `ApiClientConfig`.
- Prompt-injection patterns in knowledge-base queries are blocked before API execution.

## Run Locally

```bash
python3 -m compileall hesperia_assist scripts tests
python3 -m unittest discover -s tests
python3 scripts/run_e2e.py
python3 -m hesperia_assist.cli --tool order_lookup --arguments '{"order_id":"ord_1001","customer_id":"cus_100"}'
python3 scripts/secret_scan.py
```

## OpenAI Tool Definitions

`hesperia_assist.openai_tools.to_openai_tools()` converts `tool_contracts.json` into strict OpenAI-compatible function tool definitions. The same local contracts remain the source of truth for model-visible function schemas and server-side validation.
