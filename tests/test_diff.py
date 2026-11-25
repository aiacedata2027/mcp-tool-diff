import unittest

from mcp_tool_diff import compare, inventory, read_snapshot


def tool(name="lookup", **fields):
    return {"name": name, "inputSchema": {"type": "object"}, **fields}


class InventoryTests(unittest.TestCase):
    def test_rpc_and_bare_results_produce_same_inventory(self):
        bare = {"tools": [tool()]}
        rpc = {"jsonrpc": "2.0", "id": 8, "result": bare}
        self.assertEqual(inventory(bare), inventory(rpc))

    def test_rejects_partial_snapshot_and_duplicate_names(self):
        for document in (
            {"tools": [], "nextCursor": "second-page"},
            {"tools": [tool(), tool()]},
            {"tools": [{"name": "lookup", "inputSchema": {"type": "string"}}]},
            {"jsonrpc": "2.0", "id": 8, "error": {"code": -32601}},
        ):
            with self.subTest(document=document), self.assertRaises(ValueError):
                inventory(document)

    def test_canonical_json_rejects_duplicate_object_keys(self):
        with self.assertRaises(ValueError):
            read_snapshot('{"tools":[],"tools":[]}')

    def test_changes_are_sorted_and_do_not_reveal_schema_values(self):
        before = inventory({"tools": [tool("gone"), tool(description="old")]})
        after = inventory({"tools": [tool("added"), tool(description="new", annotations={})]})
        self.assertEqual(compare(before, after), {
            "added": ["added"],
            "removed": ["gone"],
            "changed": [{"name": "lookup", "fields": ["annotations", "description"]}],
        })

    def test_json_boolean_and_number_are_distinct(self):
        a = tool(inputSchema={"type": "object", "properties": {"mode": {"const": True}}})
        b = tool(inputSchema={"type": "object", "properties": {"mode": {"const": 1}}})
        self.assertEqual(compare(inventory({"tools": [a]}), inventory({"tools": [b]}))["changed"],
                         [{"name": "lookup", "fields": ["inputSchema"]}])

    def test_ignores_object_order_and_unmonitored_metadata(self):
        a = tool(inputSchema={"type": "object", "required": ["query"]}, _meta={"tag": 1})
        b = tool(inputSchema={"required": ["query"], "type": "object"}, _meta={"tag": 2})
        self.assertEqual(compare(inventory({"tools": [a]}), inventory({"tools": [b]}))["changed"], [])
