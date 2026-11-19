# YouTube Knowledge Template

A Cookiecutter template for turning YouTube playlists into durable, searchable
knowledge repositories with
[yt-summarizer](https://github.com/electrocucaracha/yt-summarizer).
Start with shared tooling and conventions, then keep your playlists and notes
in a repository you own.

## What This Offers

- **A ready-to-use knowledge repository.** Generate a consistent starting point
 for video notes, collection indexes, and executive summaries in
 Open Knowledge Format (OKF).
- **One place for collection settings.** Configure playlists, model, endpoint,
 language, and worker count in a single manifest.
- **Shared tooling without duplicated summarizer logic.** Reuse a pinned
 summarizer version, a validated runner, and common Make commands.
- **Publishing and search.** Build a browsable knowledge portal with Kiso,
 publish through GitHub Pages, and index notes locally with QMD.
- **Updates that preserve your knowledge.** Review and apply upstream tooling
 changes with Cruft while keeping repository-owned notes and configuration.
- **Python quality checks included.** Run Black, isort, Ruff, Pylint, mypy, and
 Bandit locally and in generated repositories' CI workflows.

The template follows the Cookiecutter and Cruft approach used by
[work-log-template](https://github.com/electrocucaracha/work-log-template), with
[yt-conferences](https://github.com/electrocucaracha/yt-conferences) as the
reference knowledge repository.
It does not copy conference notes, personal information, or credentials.

## Get Started

Follow the [getting-started guide](docs/getting-started.md) to create a repository
and generate your first notes.
For ongoing maintenance, see [template updates](docs/template-updates.md).
To improve the template itself, see [CONTRIBUTING.md](CONTRIBUTING.md).
