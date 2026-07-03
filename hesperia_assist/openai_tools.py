from __future__ import annotations

from typing import Any

from .contracts import ContractRegistry, load_contracts


TYPE_MAP = {"string": "string", "integer": "integer"}


def to_openai_tools(registry: ContractRegistry | None = None) -> list[dict[str, Any]]:
    registry = registry or load_contracts()
    tools: list[dict[str, Any]] = []
    for contract in registry.tools.values():
        properties: dict[str, Any] = {}
        for name, rules in contract.parameters.items():
            property_schema: dict[str, Any] = {"type": TYPE_MAP[rules["type"]]}
            for source_key, target_key in (
                ("minLength", "minLength"),
                ("maxLength", "maxLength"),
                ("pattern", "pattern"),
                ("minimum", "minimum"),
                ("maximum", "maximum"),
                ("default", "default"),
            ):
                if source_key in rules:
                    property_schema[target_key] = rules[source_key]
            properties[name] = property_schema
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": contract.name,
                    "description": contract.description,
                    "parameters": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": properties,
                        "required": list(contract.required_fields),
                    },
                    "strict": True,
                },
            }
        )
    return tools
