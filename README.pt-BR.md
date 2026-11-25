# MCP Tool Diff

[English](README.md)

Compare duas capturas completas de `tools/list` e receba um relatório com ferramentas adicionadas e removidas e os campos alterados. Capture com as mesmas permissões e reúna todas as páginas antes de comparar. O código de saída é 0 quando não há mudanças, 1 quando há mudanças e 2 para entrada inválida. O exemplo retorna 1.

Na raiz do repositório, use Python 3.9 ou posterior.

```bash
python3 -m mcp_tool_diff examples/before.json examples/after.json
```

[Como contribuir](CONTRIBUTING.md) · [Licença MIT](LICENSE)
