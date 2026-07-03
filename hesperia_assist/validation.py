from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .contracts import ToolContract


class ValidationError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class ValidatedToolCall:
    name: str
    arguments: dict[str, Any]


def validate_tool_call(
    tool_name: str | None,
    arguments: dict[str, Any] | None,
    contract: ToolContract | None,
) -> ValidatedToolCall:
    if not tool_name:
        raise ValidationError("missing_tool", "No function call was provided by the model.")
    if contract is None:
        raise ValidationError("unsupported_tool", f"Tool '{tool_name}' is not approved for Hesperia Assist.")
    if not isinstance(arguments, dict):
        raise ValidationError("validation_error", "Tool arguments must be a JSON object.")

    allowed_fields = set(contract.required_fields) | set(contract.optional_fields)
    extra_fields = sorted(set(arguments) - allowed_fields)
    if extra_fields:
        raise ValidationError("validation_error", f"Unexpected argument fields: {extra_fields}")

    missing_fields = [field for field in contract.required_fields if field not in arguments]
    if missing_fields:
        raise ValidationError("validation_error", f"Missing required argument fields: {missing_fields}")

    validated: dict[str, Any] = {}
    for field_name, rules in contract.parameters.items():
        if field_name not in arguments:
            if "default" in rules:
                validated[field_name] = rules["default"]
            continue
        validated[field_name] = _validate_value(field_name, arguments[field_name], rules)
    return ValidatedToolCall(name=tool_name, arguments=validated)


def _validate_value(field_name: str, value: Any, rules: dict[str, Any]) -> Any:
    expected_type = rules.get("type")
    if expected_type == "string":
        if not isinstance(value, str):
            raise ValidationError("validation_error", f"{field_name} must be a string.")
        return _validate_string(field_name, value, rules)
    if expected_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValidationError("validation_error", f"{field_name} must be an integer.")
        minimum = rules.get("minimum")
        maximum = rules.get("maximum")
        if minimum is not None and value < minimum:
            raise ValidationError("validation_error", f"{field_name} must be at least {minimum}.")
        if maximum is not None and value > maximum:
            raise ValidationError("validation_error", f"{field_name} must be at most {maximum}.")
        return value
    raise ValidationError("validation_error", f"{field_name} has unsupported parameter type '{expected_type}'.")


def _validate_string(field_name: str, value: str, rules: dict[str, Any]) -> str:
    min_length = rules.get("minLength")
    max_length = rules.get("maxLength")
    if min_length is not None and len(value) < min_length:
        raise ValidationError("validation_error", f"{field_name} is shorter than {min_length} characters.")
    if max_length is not None and len(value) > max_length:
        raise ValidationError("validation_error", f"{field_name} is longer than {max_length} characters.")
    pattern = rules.get("pattern")
    if pattern and not re.fullmatch(pattern, value):
        raise ValidationError("validation_error", f"{field_name} does not match the approved format.")
    lowered = value.lower()
    for blocked in rules.get("blockedPatterns", []):
        if blocked.lower() in lowered:
            raise ValidationError("guardrail_violation", f"{field_name} contains a blocked prompt-injection pattern.")
    if "://" in value:
        raise ValidationError("guardrail_violation", f"{field_name} must not contain arbitrary URLs.")
    return value.strip()
