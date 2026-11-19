---
title: Search notes locally
parent: How-to guides
nav_order: 3
---

# Search notes locally

Index your notes with [QMD](https://github.com/tobi/qmd) without publishing them.

After you [generate notes](create-knowledge-repository.md), install `qmd` on your
`PATH` and run these commands from the generated repository:

```bash
make qmd-setup
make qmd-update
make qmd-embed
make qmd-check
```

Run setup once per checkout. `make qmd-check` displays the index status and
lists the files in your collection.
After notes change, run `make qmd-update` and `make qmd-embed` again.

Run `make qmd-mcp` to serve the index to a Model Context Protocol (MCP) client.
The Makefile defaults to CPU mode to avoid Metal shutdown issues on macOS.
You can override it with `QMD_FORCE_CPU=0`.

If you want others to browse your notes instead,
see [Publish a knowledge portal](publish-knowledge-portal.md).
