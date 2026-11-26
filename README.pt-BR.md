# MCP Tool Diff

[English](README.md)

Compare duas capturas completas de `tools/list` e receba um relatório com ferramentas adicionadas e removidas e os campos alterados. Capture com as mesmas permissões e reúna todas as páginas antes de comparar. O código de saída é 0 quando não há mudanças, 1 quando há mudanças e 2 para entrada inválida. O exemplo retorna 1.

Na raiz do repositório, use Python 3.9 ou posterior.

```bash
python3 -m mcp_tool_diff examples/before.json examples/after.json
```

## Resultados paginados

O [exemplo de paginação](README.md#comparing-paginated-results) usa duas páginas
fictícias. A primeira contém `nextCursor` e, sozinha, é rejeitada com código de
saída `2`. Depois de coletar todas as páginas, reúna os itens dos arrays `tools`
em um único array e não inclua `nextCursor` no arquivo final. Comparar esse
arquivo com ele mesmo retorna `0` e mostra que não há mudanças.

[Como contribuir](CONTRIBUTING.md) · [Licença MIT](LICENSE)
