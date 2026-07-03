from __future__ import annotations

from typing import Any

from .api_client import HesperiaApiClient
from .contracts import ContractRegistry, load_contracts
from .validation import ValidationError, validate_tool_call


class ToolRouter:
    def __init__(self, registry: ContractRegistry | None = None, api_client: HesperiaApiClient | None = None) -> None:
        self.registry = registry or load_contracts()
        self.api_client = api_client or HesperiaApiClient()

    def route(self, tool_call: dict[str, Any] | None) -> dict[str, Any]:
        if not tool_call:
            return self._rejected("missing_tool", "No approved function call was supplied.")

        tool_name = tool_call.get("name") or tool_call.get("toolName")
        raw_arguments = tool_call.get("arguments")
        contract = self.registry.get(tool_name) if isinstance(tool_name, str) else None
        try:
            validated = validate_tool_call(tool_name, raw_arguments, contract)
        except ValidationError as exc:
            return self._rejected(exc.code, exc.message)

        api_response = self.api_client.execute(validated.name, validated.arguments)
        if api_response.get("status") == "error":
            return {
                "status": "error",
                "tool": validated.name,
                "arguments": validated.arguments,
                "error": api_response["error"],
                "supportReady": False,
            }
        return {
            "status": api_response["status"],
            "tool": validated.name,
            "arguments": validated.arguments,
            "data": {key: value for key, value in api_response.items() if key not in {"status", "error"}},
            "error": api_response.get("error"),
            "supportReady": api_response["status"] == "ok",
        }

    @staticmethod
    def _rejected(code: str, message: str) -> dict[str, Any]:
        return {
            "status": "rejected",
            "error": {"code": code, "message": message, "retryable": False},
            "supportReady": False,
        }
