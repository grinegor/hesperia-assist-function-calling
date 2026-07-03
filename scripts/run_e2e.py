from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from hesperia_assist.router import ToolRouter


def main() -> int:
    cases_path = PROJECT_ROOT / "e2e_tests.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))["cases"]
    router = ToolRouter()
    failures: list[str] = []
    for case in cases:
        result = router.route(case["toolCall"])
        serialized = json.dumps(result, sort_keys=True)
        if result["status"] != case["expectedStatus"]:
            failures.append(f"{case['name']}: expected status {case['expectedStatus']}, got {result['status']}")
            continue
        missing = [fragment for fragment in case.get("expectedContains", []) if fragment not in serialized]
        if missing:
            failures.append(f"{case['name']}: missing fragments {missing}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"PASS {len(cases)} end-to-end function-calling cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
