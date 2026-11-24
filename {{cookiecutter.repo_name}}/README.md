# {{ cookiecutter.readme_title }}

<!-- markdown-link-check-disable-next-line -->
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
<!-- markdownlint-disable MD034 -->
[![Check Python](https://github.com/{{ cookiecutter.github_owner }}/{{ cookiecutter.repo_name }}/workflows/Check%20Python/badge.svg)](https://github.com/{{ cookiecutter.github_owner }}/{{ cookiecutter.repo_name }}/actions/workflows/python.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<!-- markdown-link-check-disable-next-line -->
![visitors](https://visitor-badge.laobi.icu/badge?page_id={{ cookiecutter.github_owner }}.{{ cookiecutter.repo_name }})
[![Scc Code Badge](https://sloc.xyz/github/{{ cookiecutter.github_owner }}/{{ cookiecutter.repo_name }}?category=code)](https://github.com/boyter/scc/)
[![Scc COCOMO Badge](https://sloc.xyz/github/{{ cookiecutter.github_owner }}/{{ cookiecutter.repo_name }}?category=cocomo)](https://github.com/boyter/scc/)

{{ cookiecutter.readme_title }} is a curated, searchable collection of notes from
technology conference videos.

It turns long-form talks into durable technical knowledge by capturing the
ideas, explanations, examples, and lessons that are most useful after the
video ends.
The collection brings together perspectives from conference speakers across
cloud-native computing, Kubernetes, artificial intelligence, developer
productivity, engineering leadership, and related areas.

The information is produced by
[`yt-summarizer`](https://github.com/electrocucaracha/yt-summarizer), an
application that fetches conference videos uploaded to YouTube, retrieves their
transcripts, and uses a large language model to generate summaries and extract key
points.
This project organizes that generated information into a durable knowledge base
that is easier to browse, search, and reuse.

The notes are organized as a structured, machine-readable knowledge base using
[Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).
The canonical collection lives in [`docs/`](docs/index.md), where content is
grouped into navigable conference and subject areas.
This structure supports both broad exploration by topic and focused reading of
an individual talk.
{% if cookiecutter.include_diagram %}
![Diagram](docs/assets/diagram.png)
{% endif %}

## What This Offers

- **Curated learning**: Explore concise notes from talks about Kubernetes,
  cloud-native platforms, artificial intelligence, developer productivity,
  leadership, and other areas of modern technology.
- **Efficient understanding**: Read a short summary and key takeaways before
  deciding whether a full talk is relevant to your work or interests.
- **In-page playback**: Watch talks in the portal through privacy-enhanced YouTube players, with original YouTube links available when embedding is restricted.
- **Structured knowledge**: Use consistent notes that combine descriptive
  metadata, a summary, key takeaways, the original video, and its transcript.
- **Progressive discovery**: Move from the collection index to a subject or
  conference directory, then to an individual talk without losing context.
  Previous and Next links follow the collection index order, with a direct link back to the collection.
- **Semantic search**: Find related ideas by meaning and intent, not only by
  exact keyword matches.
- **Knowledge reuse**: Return to the collection as a reference for research,
  technical discussions, writing, planning, and continued learning.
- **Machine-readable content**: Build on a consistent format that makes the
  knowledge base suitable for indexing, automation, and future integrations.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), Git, and
Python 3.12 or newer. Then run:

```bash
make install
```

The summarizer is installed from the Git revision pinned in the Makefile.
For local development against a sibling checkout, use
`make install SUMMARIZER_SOURCE=../yt-summarizer` instead.
Ensure uv's tool directory is on your `PATH` (`uv tool update-shell`).

The default model uses [Ollama](https://ollama.com/). Start Ollama and pull the
model before generating notes:

```bash
ollama pull {{ cookiecutter.model | replace('ollama/', '') }}
```

For other LiteLLM providers, configure the model and endpoint in
[knowledge.toml](knowledge.toml) and export the provider's credentials locally.
Never put credentials in the manifest or generated notes. `.env` files and logs
are ignored because they may contain credentials or sensitive runtime data.

## Generate Notes

Add named public playlists to [knowledge.toml](knowledge.toml):

```toml
[playlists.conference]
url = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

Keep the existing `[playlists]` table; append named entries below it.
Model, API base, summary language, and worker count are configured once in the
same manifest. Keep workers at 1 for a local Ollama server.

```bash
make summarize-dry-run
make summarize
make summarize COLLECTION=conference
```

The runner validates the configuration before starting, processes playlists
sequentially, and stops on the first failure. It always passes `--output-dir`
explicitly to select filesystem mode without requiring Notion credentials.
The summarizer creates title-based playlist directories, video notes,
executive summaries, and collection indexes under `docs/`. Manifest names
select playlists; they do not rename the generated directories.

Review the generated content and attribution before committing it. Notes can
contain model errors. Videos without accessible transcripts cannot be processed.
Repeat runs use the summarizer's existing-note handling; this template does not
implement a separate cache or force regeneration.

## Browse and Publish

`make check` and `make build` download the pinned
[Kiso CLI v0.2.7](https://github.com/oak-invest/kiso/releases/tag/v0.2.7) into a
local cache on first use through [scripts/run_kiso.sh](scripts/run_kiso.sh).
Native binaries exist for Linux x86_64 and macOS arm64; other platforms need
`java` to run the release JAR. Then run:

```bash
make check
make preview
```

The local preview is at <http://127.0.0.1:8099>. Override its port with `PORT=8100`.
`make build` writes the static portal to `public/`.

For GitHub Pages, push to
`{{ cookiecutter.github_owner }}/{{ cookiecutter.repo_name }}` and choose
**GitHub Actions** as the Pages source in repository settings. The included
workflow publishes on pushes to `{{ cookiecutter.default_branch }}` or manual
dispatch. Pages publishing may make your notes public; verify repository and
organization visibility settings first.

## Local Search

With [QMD](https://github.com/tobi/qmd) installed:

```bash
make qmd-setup
make qmd-update
make qmd-embed
make qmd-check
```

Run setup once per checkout. After notes change, run update and embed again.
Use `make qmd-mcp` to serve the local search index to an MCP client.
QMD defaults to CPU mode to avoid known Metal shutdown issues on macOS;
override with `QMD_FORCE_CPU=0` when appropriate.

## Python Quality Checks

```bash
make lint
make fmt
```

`make lint` checks Python scripts with Black, isort, Ruff, Pylint, mypy, and
Bandit using pinned development tool versions. `make fmt` applies compatible
Black and isort formatting. The Python CI workflow runs the same lint gates on
pushes and pull requests.

Bandit blocks medium-or-higher severity findings with medium-or-higher
confidence. Low-severity findings are informational; no individual rules are
disabled. `make check` remains the separate Kiso knowledge-bundle validation.

## Template Updates

This repository comes from
[yt-summarizer-template]({{ cookiecutter.template_url }}).
When generated through Cruft, run these commands from a clean working tree:

```bash
make template-check
make template-diff
make template-update
```

To refresh the pinned Kiso CLI version and GitHub Action revisions, run
`make update-versions`. It needs network access and Git, and it formats the
Python scripts afterward.

Review and commit the resulting changes. Cruft excludes `docs/` and
`knowledge.toml`, so your notes, indexes, playlists, and local model choices
remain repository-owned. New manifest settings must be adopted manually.
Projects rendered directly with Cookiecutter must first be linked with
`cruft link {{ cookiecutter.template_url }}`.
