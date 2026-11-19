---
title: Create a knowledge repository
parent: How-to guides
nav_order: 1
---

# Create a knowledge repository

Generate a repository and turn one public YouTube playlist into a collection of notes.

## Before you begin

- Install [uv](https://docs.astral.sh/uv/), Git, Make, and Python 3.12 or newer.
- Choose a public YouTube playlist with accessible transcripts.
- Install and start [Ollama](https://ollama.com/) for the default model,
  or have a working model backend ready.

## Generate the repository

Use Cruft so the generated repository records the template version for future updates:

```bash
uvx --from cruft==2.16.0 cruft create https://github.com/electrocucaracha/yt-summarizer-template
cd youtube-knowledge
git init -b main
make install
```

Replace `youtube-knowledge` and `main` if you chose a different repository name
or default branch.
If the installed tools are not on your `PATH`, run `uv tool update-shell` and
open a new shell.

To try an uncommitted local copy of the template, use
`uvx --from cookiecutter==2.6.0 cookiecutter /absolute/path/to/yt-summarizer-template`
in place of `cruft create`, then initialize the generated repository as above.
Cookiecutter does not record update metadata; see [Update a generated repository](update-template.md)
to link it later.

## Configure a playlist

Append an entry after the existing `[playlists]` table in `knowledge.toml`:

```toml
[playlists.conference]
url = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

Replace `YOUR_PLAYLIST_ID` with the `list` value from your playlist URL.
For the default Ollama model, run:

```bash
ollama pull llama3.2
```

If you use another model, see the [manifest reference](../references/knowledge-manifest.md).
Export any required provider credentials locally; do not put them in the manifest.

## Generate and review notes

From the generated repository, inspect the command and then run it:

```bash
make summarize-dry-run COLLECTION=conference
make summarize COLLECTION=conference
```

Omit `COLLECTION` to process every configured playlist.
Look under `docs/` for the directory named after the YouTube playlist title,
not the manifest key `conference`.
Review the video notes, collection index, and executive summary for accuracy
and attribution before committing.
If a video has no accessible transcript, the summarizer cannot process it.

Next, [preview or publish the portal](publish-knowledge-portal.md)
or [search your notes locally](search-notes.md).
