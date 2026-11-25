"""Compare two saved MCP tools/list snapshots without connecting to a server."""

import json


FIELDS = ("title", "description", "inputSchema", "outputSchema", "annotations", "execution")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _reject_constant(_value):
    raise ValueError("non-finite numbers are not valid JSON")


def read_snapshot(text):
    return json.loads(text, object_pairs_hook=_unique_object, parse_constant=_reject_constant)


def inventory(document):
    if not isinstance(document, dict):
        raise ValueError("expected a tools/list result object")
    if "jsonrpc" in document or "result" in document:
        if document.get("jsonrpc") != "2.0" or "error" in document or "tools" in document:
            raise ValueError("expected a successful JSON-RPC 2.0 response")
        document = document.get("result")
    if not isinstance(document, dict) or not isinstance(document.get("tools"), list):
        raise ValueError("expected a tools array")
    if document.get("nextCursor") is not None:
        raise ValueError("snapshot is incomplete; combine all pages before comparing")

    tools = {}
    for index, tool in enumerate(document["tools"]):
        if not isinstance(tool, dict):
            raise ValueError(f"tool #{index + 1} must be an object")
        name = tool.get("name")
        if not isinstance(name, str) or not name.strip() or name in tools:
            raise ValueError(f"tool #{index + 1} has a missing or duplicate name")
        for field in ("inputSchema", "outputSchema"):
            if field == "outputSchema" and field not in tool:
                continue
            schema = tool.get(field)
            if not isinstance(schema, dict) or schema.get("type") != "object":
                raise ValueError(f"tool #{index + 1} must provide an object {field}")
        tools[name] = {
            field: json.dumps(tool[field], sort_keys=True, allow_nan=False)
            for field in FIELDS if field in tool
        }
    return tools


def compare(before, after):
    changes = []
    for name in sorted(before.keys() & after.keys()):
        previous, current = before[name], after[name]
        fields = sorted(key for key in previous.keys() | current.keys()
                        if previous.get(key) != current.get(key))
        if fields:
            changes.append({"name": name, "fields": fields})
    return {
        "added": sorted(after.keys() - before.keys()),
        "removed": sorted(before.keys() - after.keys()),
        "changed": changes,
    }
