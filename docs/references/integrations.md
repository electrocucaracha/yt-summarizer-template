---
title: Integrations and requirements
parent: References
nav_order: 1
---

# Integrations and requirements

| Tool | Role |
| --- | --- |
| [uv](https://docs.astral.sh/uv/), Python 3.12 or newer, Make, and Git | Generate a repository, install tools, and run commands. |
| [Cruft](https://github.com/cruft/cruft) | Generates repositories with `.cruft.json` for future template updates. Cookiecutter alone does not write that file. |
| [yt-summarizer](https://github.com/electrocucaracha/yt-summarizer) | Converts playlists to OKF files. The generated Makefile pins its Git revision. |
| [Ollama](https://ollama.com/) or another LiteLLM-compatible backend | Supplies the language model. Credentials, if needed, are configured outside the manifest. |
| [Kiso CLI v0.2.7](https://github.com/oak-invest/kiso/releases/tag/v0.2.7) | Validates and builds the knowledge bundle. `scripts/run_kiso.sh` downloads the pinned release on first use for `make check`, `make build`, and `make preview`; Java is required only where no native binary exists. |
| [GitHub Pages](https://docs.github.com/pages) | Optionally hosts the generated portal using the included GitHub Actions workflow. |
| [QMD](https://github.com/tobi/qmd) | Optionally indexes notes for local search and can serve the index to an MCP client. |

See the [how-to guides](../how-to-guides/index.md) for the commands that use these tools.
