# Create a Knowledge Repository

Generate a repository, configure its playlists, and use the summarizer to write
your first collection of notes.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), Git, Make,
and Python 3.12 or newer.
You also need a public YouTube playlist with accessible transcripts and a
working model backend, such as [Ollama](https://ollama.com/).

## Generate the Repository

Use Cruft to retain the metadata needed to review and apply future template
updates:

```bash
uvx --from cruft==2.16.0 cruft create https://github.com/electrocucaracha/yt-summarizer-template
cd youtube-knowledge
git init
make install
```

The example uses the default repository name. If you choose a different name,
change into that directory instead.
Ensure uv's tool directory is on your `PATH`; run `uv tool update-shell` if needed.

Before this template is published, commit it to a local Git repository and
replace the URL with its absolute path. Cruft needs a committed Git template.

To render a local template immediately without Git history, use Cookiecutter:

```bash
uvx --from cookiecutter==2.6.0 cookiecutter /absolute/path/to/yt-summarizer-template
```

Then enter the generated directory, initialize Git, and run `make install`.
Cookiecutter does not create Cruft update metadata; see
[Template Updates](template-updates.md) to link the repository later.

## Configure a Playlist

In the generated repository, edit `knowledge.toml` and append a named playlist
below the existing `[playlists]` table:

```toml
[playlists.conference]
url = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

Replace `YOUR_PLAYLIST_ID` with your playlist's identifier.
The manifest also holds the model, API endpoint, summary language, and worker
count shared by all playlists.
Keep credentials out of the manifest; export provider credentials locally.

For the default backend, start Ollama and pull the default model:

```bash
ollama pull llama3.2
```

If you selected a different model during generation, use that model instead.

## Generate Notes

Review the command before running it:

```bash
make summarize-dry-run
make summarize
```

To process only the named playlist above:

```bash
make summarize COLLECTION=conference
```

The summarizer writes notes, executive summaries, and collection indexes under
`docs/`, using playlist titles for directory names.
Review generated summaries and source attribution before committing them;
model output can contain errors.

The generated repository's README includes instructions for Kiso publishing,
GitHub Pages, and local QMD search.
For maintenance, continue to [Template Updates](template-updates.md).

Return to the [project overview](../README.md).
