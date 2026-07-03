from __future__ import annotations

import argparse
import json

from .router import ToolRouter


def main() -> None:
    parser = argparse.ArgumentParser(description="Route an approved Hesperia Assist function call.")
    parser.add_argument("--tool", required=True, help="Approved tool name.")
    parser.add_argument("--arguments", required=True, help="JSON object of tool arguments.")
    args = parser.parse_args()

    router = ToolRouter()
    result = router.route({"name": args.tool, "arguments": json.loads(args.arguments)})
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
