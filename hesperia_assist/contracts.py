from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT_PATH = PROJECT_ROOT / "tool_contracts.json"


@dataclass(frozen=True)
class ToolContract:
    name: str
    description: str
    method: str
    path: str
    required_fields: tuple[str, ...]
    optional_fields: tuple[str, ...]
    parameters: dict[str, dict[str, Any]]
    response_shape: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ToolContract":
        return cls(
            name=data["name"],
            description=data["description"],
            method=data["method"],
            path=data["path"],
            required_fields=tuple(data.get("requiredFields", [])),
            optional_fields=tuple(data.get("optionalFields", [])),
            parameters=data.get("parameters", {}),
            response_shape=data.get("responseShape", {}),
        )


class ContractRegistry:
    def __init__(self, raw_contracts: dict[str, Any]) -> None:
        self.raw_contracts = raw_contracts
        self.policy = raw_contracts.get("policy", {})
        self.tools = {
            tool.name: tool
            for tool in (ToolContract.from_dict(item) for item in raw_contracts.get("tools", []))
        }
        self._validate_registry()

    def _validate_registry(self) -> None:
        required_names = {"order_lookup", "subscription_lookup", "knowledge_base_search"}
        actual_names = set(self.tools)
        if actual_names != required_names:
            raise ValueError(f"Approved tool set mismatch: expected {required_names}, got {actual_names}")
        if not self.policy.get("approvedOnly") or not self.policy.get("failClosed"):
            raise ValueError("Tool policy must be approved-only and fail-closed.")
        for tool in self.tools.values():
            missing = [field for field in tool.required_fields if field not in tool.parameters]
            if missing:
                raise ValueError(f"{tool.name} references missing required parameters: {missing}")

    def get(self, name: str) -> ToolContract | None:
        return self.tools.get(name)

    def require(self, name: str) -> ToolContract:
        contract = self.get(name)
        if contract is None:
            raise KeyError(name)
        return contract

    @property
    def approved_tool_names(self) -> tuple[str, ...]:
        return tuple(sorted(self.tools))


def load_contracts(path: str | Path = DEFAULT_CONTRACT_PATH) -> ContractRegistry:
    with Path(path).open("r", encoding="utf-8") as handle:
        return ContractRegistry(json.load(handle))
