---
title: Knowledge manifest
parent: References
nav_order: 2
---

# Knowledge manifest

`knowledge.toml` configures the runner in a generated repository.
The runner shares the top-level settings across all selected playlists.

| Setting | Default | Accepted value |
| --- | --- | --- |
| `model` | `ollama/llama3.2` | Non-empty model identifier accepted by yt-summarizer's model backend. |
| `api_base` | `http://localhost:11434` | Non-empty model API base URL. |
| `language` | `en` | Non-empty summary language code. |
| `workers` | `1` | Positive integer for the summarizer's worker count. |
| `playlists.<name>.url` | No entries | HTTPS URL on `youtube.com`, `www.youtube.com`, or `m.youtube.com` with path `/playlist` and a non-empty `list` query parameter. |

The runner requires at least one named playlist.
`COLLECTION` selects a manifest key, not an output directory.
The summarizer names output directories after playlist titles.
The runner validates the selected playlists before starting, processes them
sequentially, and stops on the first failure.

For an example manifest entry and commands, see
[Create a knowledge repository](../how-to-guides/create-knowledge-repository.md).
