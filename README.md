# YouTube Knowledge Template

Create a repository of searchable, source-linked notes from public YouTube
playlists with [yt-summarizer](https://github.com/electrocucaracha/yt-summarizer).
You own the playlists, model settings, and notes in the repository you generate.

## What it provides

- Turn videos with accessible transcripts into Open Knowledge Format (OKF)
  notes, collection indexes, and executive summaries.
- Browse your notes locally or publish a static knowledge portal on GitHub Pages.
- Search your notes locally with QMD and adopt shared tooling updates with Cruft.

## Get started

With [uv](https://docs.astral.sh/uv/) installed, generate your repository:

```bash
uvx --from cruft==2.16.0 cruft create https://github.com/electrocucaracha/yt-summarizer-template
```

Follow [Create a knowledge repository](docs/how-to-guides/create-knowledge-repository.md)
to configure a playlist and review your first notes.

## Learn more

Browse the [documentation site](https://electrocucaracha.github.io/yt-summarizer-template/)
or read the [documentation in this repository](docs/index.md).
To improve the template itself, see [Contributing](CONTRIBUTING.md).
