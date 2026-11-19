# Contributing

Use this guide to change and validate the template itself.
To create a knowledge repository instead, follow
[Create a knowledge repository](docs/how-to-guides/create-knowledge-repository.md).

## Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), Git, and Make.
Run the commands below from the template repository root.
The Make targets use uv to provide Python 3.12 and the pinned development tools.

## Make Changes

- Edit `cookiecutter.json` to change template prompts and defaults.
- Edit files under `{{cookiecutter.repo_name}}/` to change generated repositories.
- Keep transcript retrieval, prompts, summary generation, and OKF writing in
  [yt-summarizer](https://github.com/electrocucaracha/yt-summarizer), rather than
  duplicating that logic here.
- Keep sample content generic. Do not include personal notes or credentials.
- Preserve the [repository ownership rules](docs/explanations/template-model.md) when
  changing how shared files are updated.
- Update the relevant guide when changing setup, commands, or update behavior.

Edit the template's [documentation site](docs/index.md) under the root `docs/`.
GitHub Pages publishes that directory from `main`.
The generated project's `docs/` is a separate knowledge bundle built with Kiso;
do not put template documentation there.

The generated project contains the shared development requirements and Python
tool configuration. Keep Black and isort settings compatible when updating them.

## Format and Lint Python

```bash
make fmt
make lint
```

`make fmt` applies isort and Black formatting.
`make lint` runs Black, isort, Ruff, Pylint, mypy, and Bandit against both the
template checker and generated-repository scripts.
Tool versions are pinned in the template's development requirements.

Bandit blocks medium-or-higher severity findings with medium-or-higher
confidence. Low-severity findings remain informational.
No individual Bandit rules are disabled.

## Validate the Template

```bash
make check
```

This runs the Python quality gates, then:

- Renders default and customized repositories.
- Parses generated configuration and checks for unrendered placeholders.
- Verifies command forwarding without contacting YouTube or an LLM.
- Runs the generated project's Python lint gates for both renderings.
- Exercises a real Cruft update in a temporary Git repository to verify that
  repository-owned content is preserved.

CI runs the same command.
The check does not install or run the summarizer, Kiso, or QMD, so changes to
those integrations also need a focused manual check with the affected tool.

## Submit Changes

Keep changes focused, run `make check`, and describe the behavior changed and
validation performed in your pull request.
Call out changes that require generated repositories to adjust their manifests
or resolve template-update conflicts.

Return to the [project overview](README.md).
