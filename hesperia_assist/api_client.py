from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Protocol


class ApiError(Exception):
    def __init__(self, code: str, message: str, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


class HesperiaTransport(Protocol):
    def request(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class ApiClientConfig:
    base_url: str
    token_present: bool
    timeout_ms: int = 3000
    max_attempts: int = 2

    @classmethod
    def from_env(cls) -> "ApiClientConfig":
        return cls(
            base_url=os.getenv("HESPERIA_API_BASE_URL", "https://api.hesperia.example"),
            token_present=bool(os.getenv("HESPERIA_API_TOKEN")),
            timeout_ms=int(os.getenv("HESPERIA_TIMEOUT_MS", "3000")),
            max_attempts=int(os.getenv("HESPERIA_RETRY_MAX_ATTEMPTS", "2")),
        )


class HesperiaApiClient:
    def __init__(self, config: ApiClientConfig | None = None, transport: HesperiaTransport | None = None) -> None:
        self.config = config or ApiClientConfig.from_env()
        self.transport = transport or MockHesperiaTransport()

    def execute(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        last_error: ApiError | None = None
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                response = self.transport.request(tool_name, arguments)
                return self._normalize_response(tool_name, response)
            except ApiError as exc:
                last_error = exc
                if not exc.retryable or attempt >= self.config.max_attempts:
                    break
                time.sleep(0.05 * attempt)
        assert last_error is not None
        return {
            "status": "error",
            "error": {
                "code": last_error.code,
                "message": last_error.message,
                "retryable": last_error.retryable,
            },
        }

    def _normalize_response(self, tool_name: str, response: dict[str, Any]) -> dict[str, Any]:
        if response.get("status") not in {"ok", "not_found", "error"}:
            raise ApiError("invalid_response", f"{tool_name} returned an invalid status.", retryable=False)
        response.setdefault("error", None)
        return response


class MockHesperiaTransport:
    def request(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments.get("order_id") == "ord_5000":
            raise ApiError("api_unavailable", "Order service is temporarily unavailable.", retryable=True)
        if tool_name == "order_lookup":
            return {
                "status": "ok",
                "order": {
                    "order_id": arguments["order_id"],
                    "customer_id": arguments.get("customer_id", "cus_unknown"),
                    "order_status": "shipped",
                    "tracking_number": "1Z999AA10123456784",
                    "updated_at": "2026-07-03T07:45:00Z",
                },
                "error": None,
            }
        if tool_name == "subscription_lookup":
            return {
                "status": "ok",
                "subscription": {
                    "subscription_id": arguments["subscription_id"],
                    "customer_id": arguments.get("customer_id", "cus_unknown"),
                    "plan": "Growth Annual",
                    "subscription_status": "active",
                    "next_renewal_date": "2026-10-15",
                },
                "error": None,
            }
        if tool_name == "knowledge_base_search":
            return {
                "status": "ok",
                "results": [
                    {
                        "article_id": "kb_0142",
                        "title": "Refund policy for annual subscriptions",
                        "summary": "Annual subscriptions can be refunded within 30 days unless usage exceeds the fair-use threshold.",
                        "url": "https://support.hesperia.example/kb/kb_0142",
                    }
                ][: arguments.get("limit", 3)],
                "error": None,
            }
        raise ApiError("unsupported_tool", f"{tool_name} is not supported by the API client.", retryable=False)
