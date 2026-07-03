# Scenario

Hesperia is a SaaS company that sells Hesperia Assist, an AI support copilot used by mid-market customer service teams. The product team wants the copilot to fetch order status, subscription details, and knowledge-base answers from approved external APIs so agents can resolve tickets faster for e-commerce and subscription customers. Your job is to implement the function-calling layer that safely connects the LLM to these APIs while keeping the experience reliable for support agents handling live customer requests.

# Your Role

You are a senior AI engineer implementing secure function-calling access so an LLM can invoke approved external APIs for Hesperia's customer support workflow. The integration must support controlled tool selection, validated inputs, and reliable responses for production use.

# Task Steps

## 1. Define Tool Contracts

Goal: Specify the external API functions the Hesperia Assist LLM is allowed to call.

Checklist:

- Define only the approved Hesperia support tools and exclude any unapproved actions.
- Specify strict input parameters, required fields, and expected output structure for each tool.
- Include validation rules that prevent malformed or unsafe requests from reaching Hesperia APIs.

Deliverables:

- Tool schema definitions in JSON or equivalent machine-readable format
- Function signatures for each approved Hesperia API tool
- Input validation rules for all tool parameters

Approved tools:

- order lookup
- subscription lookup
- knowledge-base search

## 2. Implement Call Routing

Goal: Wire the LLM to select and execute the correct Hesperia API function.

Checklist:

- Route only to the approved Hesperia tool set and reject any unsupported function request.
- Parse model-generated arguments and pass only validated values to the external API layer.
- Define fallback behavior for missing, invalid, or ambiguous function-call outputs.

Deliverables:

- Function-calling router implementation
- Tool invocation and response parsing logic
- Fallback handling for invalid or missing tool calls

## 3. Secure API Access

Goal: Protect Hesperia's external API integrations with production-grade controls.

Checklist:

- Use secure credential handling for all Hesperia API access and avoid hard-coded secrets.
- Apply request timeout and retry rules appropriate for live support usage.
- Add guardrails that block unsafe tool use and reduce prompt-injection risk.

Deliverables:

- Secure API client configuration
- Timeout and retry settings for external calls
- Tool-use guardrail implementation

## 4. Validate End-To-End

Goal: Verify that Hesperia Assist can reliably call external APIs through function calling.

Checklist:

- Test at least one successful case for each approved Hesperia tool.
- Test invalid input, API failure, and unsupported-request scenarios.
- Verify that returned data is structured and safe for support-agent consumption.

Deliverables:

- End-to-end test cases or test suite
- Sample request and response payloads for each supported tool
- Validation results for success and failure scenarios

# Submission Contract

publish_required: true

submission_type: github_url plus required file uploads when TaskLearn exposes file fields

final_delivery_contract:

- `tool_contracts.json`: Machine-readable definitions for the approved Hesperia function-calling tools, including schemas, required fields, response expectations, and validation rules.
- `repo_url`: A single Git repository containing the routing logic, tool invocation flow, validation layer, and security guardrails for approved API access.
- `e2e_tests.json`: Structured test cases covering successful tool calls, invalid inputs, unsupported requests, and API failure scenarios.

# What To Do Now

Build the Hesperia Assist function-calling layer, validate it locally, publish the repository only after secret checks pass, then submit the repository URL and the required JSON artifacts to TaskLearn.
