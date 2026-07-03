# Architecture

Build a compact Python package named `hesperia_assist` that models the production function-calling boundary for Hesperia Assist:

- `tool_contracts.json` is the machine-readable source of truth for the approved tools.
- `hesperia_assist/contracts.py` loads and validates contract definitions.
- `hesperia_assist/validation.py` validates model-selected tool names and arguments before execution.
- `hesperia_assist/api_client.py` provides a secure external API client abstraction with managed-secret configuration, timeouts, retries, and deterministic mock transport for local validation.
- `hesperia_assist/router.py` routes model function-call outputs to approved tools only, parses responses, and fails closed on missing, invalid, ambiguous, or unsafe calls.
- `hesperia_assist/openai_tools.py` exports OpenAI-compatible tool definitions from the same contract file.
- `tests/` and `e2e_tests.json` cover happy paths and negative paths.

# Chosen Stack

- Python 3 standard library only for the package and tests.
- `unittest` for validation to avoid external dependency installation.
- JSON Schema-like contracts implemented with explicit local validation rules.
- No live OpenAI API call is required for local validation; the repository exposes function/tool schemas compatible with real OpenAI tool calling and keeps the runtime boundary deterministic.

# File Tree

```text
.
├── .env.example
├── .gitignore
├── BUILD_REPORT.md
├── CHECK_REPORT.md
├── FINAL_SUBMISSION.md
├── README.md
├── TASKLEARN_FINAL_REPORT.md
├── TASKLEARN_PAGE.html
├── TASKLEARN_SOURCE.json
├── PROMPT.md
├── PLAN.md
├── e2e_tests.json
├── tool_contracts.json
├── hesperia_assist/
│   ├── __init__.py
│   ├── api_client.py
│   ├── cli.py
│   ├── contracts.py
│   ├── openai_tools.py
│   ├── router.py
│   └── validation.py
├── scripts/
│   ├── run_e2e.py
│   └── secret_scan.py
└── tests/
    ├── test_contracts.py
    ├── test_openai_tools.py
    └── test_router.py
```

# Implementation Tasks

1. Define `tool_contracts.json` for exactly three approved tools: `order_lookup`, `subscription_lookup`, and `knowledge_base_search`.
2. Define `e2e_tests.json` with at least one success case for each tool plus invalid input, unsupported tool, and API failure scenarios.
3. Implement contract loading, argument validation, prompt-injection guards, route selection, secure client configuration, timeout/retry metadata, and structured response parsing.
4. Add CLI demos for local execution.
5. Add unit tests and an E2E runner that validates the JSON test cases against the router.
6. Write README, build report, final submission, and TaskLearn final report.

# Validation Commands

```bash
python3 -m compileall hesperia_assist scripts tests
python3 -m unittest discover -s tests
python3 scripts/run_e2e.py
python3 -m hesperia_assist.cli --tool order_lookup --arguments '{"order_id":"ord_1001","customer_id":"cus_100"}'
python3 scripts/secret_scan.py
```

# Deliverables

- `tool_contracts.json`
- public GitHub repository URL containing the implementation
- `e2e_tests.json`

# Risk Notes

- The integration must fail closed for unsupported or malformed tool calls.
- Secrets must come from environment variables and never from hard-coded values.
- Prompt-injection strings must not be allowed to change the approved tool set or bypass validation.
- TaskLearn may require both file uploads and a repository URL; `FINAL_SUBMISSION.md` must list all three contract items.

# GitHub Publication Policy

`publish_required: true` because TaskLearn asks for `repo_url`. Publish only after local validation passes, `.env` is ignored/untracked, and `scripts/secret_scan.py` passes.

# TaskLearn Submission Plan

1. Publish the validated project to a public `grinegor` GitHub repository.
2. Open the TaskLearn task in logged-in Chrome, click `Start Task` if visible, then attach the repository URL.
3. Upload `tool_contracts.json` and `e2e_tests.json` if the TaskLearn workspace exposes file upload fields for them.
4. Submit/evaluate, save attempt evidence, and retry at most twice from TaskLearn feedback if not accepted.
