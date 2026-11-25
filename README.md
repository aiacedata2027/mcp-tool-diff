# MCP Tool Diff

[Português](README.pt-BR.md)

Review what changed between two saved MCP tool inventories before shipping an agent integration. The report lists added and removed tool names and changed field names.

## Quick start

Run from the repository root with Python 3.9 or later.

```bash
python3 -m mcp_tool_diff examples/before.json examples/after.json
```

Save the complete results of two `tools/list` calls as UTF-8 JSON. A bare response result or a successful JSON-RPC 2.0 envelope works. If the server paginates, retrieve every page and combine the `tools` arrays before comparing. Use the same scopes in both captures because the server can expose different tools for different callers.

The comparison covers title, description, input and output schemas, annotations, and execution. It ignores JSON object key order and keeps array order. Status 0 means unchanged, 1 means changes, and 2 means input could not be compared. The example exits 1. Review changes before deciding whether they break an integration. The tool reads saved files, makes no connections, and invokes no tools.

## Comparing paginated results

Save every page from the same `tools/list` listing before comparing. Run the
following from the repository root to create two synthetic pages. The first
has a `nextCursor`; the last does not.

```bash
cat > page-1.json <<'JSON'
{"tools":[{"name":"list_notes","inputSchema":{"type":"object"}}],"nextCursor":"page-2"}
JSON
cat > page-2.json <<'JSON'
{"tools":[{"name":"read_note","inputSchema":{"type":"object"}}]}
JSON
```

Concatenate the `tools` arrays into a single result object. Omit `nextCursor`
from the combined snapshot only after you have collected every page.

```bash
cat > combined.json <<'JSON'
{
  "tools": [
    {"name":"list_notes","inputSchema":{"type":"object"}},
    {"name":"read_note","inputSchema":{"type":"object"}}
  ]
}
JSON
```

Comparing the first page with the complete snapshot exits `2` and prints
`snapshot is incomplete; combine all pages before comparing` to standard error:

```bash
python3 -m mcp_tool_diff page-1.json combined.json
```

As a sanity check, comparing the complete snapshot with itself exits `0` and
prints `{"added": [], "removed": [], "changed": []}` (formatted across several
lines). For a real comparison, pass the complete before and after snapshots.

```bash
python3 -m mcp_tool_diff combined.json combined.json
```

## Contributing

Choose a [beginner task](https://github.com/henrivalle/mcp-tool-diff/contribute) and use a small synthetic file to show the expected result. [Contributing guide](CONTRIBUTING.md) · [MIT license](LICENSE)

## References

[MCP Tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) · [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
