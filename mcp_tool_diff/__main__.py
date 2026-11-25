import argparse
import json
from pathlib import Path
import sys

from . import compare, inventory, read_snapshot


def main():
    parser = argparse.ArgumentParser(description="Compare two local MCP tools/list snapshots.")
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    args = parser.parse_args()
    try:
        before = inventory(read_snapshot(args.before.read_text(encoding="utf-8-sig")))
        after = inventory(read_snapshot(args.after.read_text(encoding="utf-8-sig")))
    except (OSError, UnicodeError, RecursionError):
        print("Could not read a UTF-8 JSON snapshot.", file=sys.stderr)
        return 2
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    result = compare(before, after)
    print(json.dumps(result, indent=2))
    return int(any(result.values()))


if __name__ == "__main__":
    raise SystemExit(main())
