# Maintain Template Updates

Cruft lets generated repositories review and adopt shared template changes
without replacing their knowledge content.
Updates are currently manual; the template does not include a scheduled action
that opens update pull requests or automatically merges changes.

## Shared Files and Repository-Owned Content

The template maintains the summarizer version, runner, Make targets, Python
quality configuration, publishing workflows, and shared guidance.
The summarizer remains responsible for transcript retrieval, prompts, summary
generation, and Open Knowledge Format (OKF) output.

Each generated repository owns:

- `knowledge.toml`, including playlists, model, endpoint, language, and workers.
- Everything under `docs/`, including generated notes, collection indexes, and
  local edits.

Cruft skips those paths during updates.
If an upstream change introduces new manifest settings, adopt them manually.
Do not remove the exclusions to force an update over existing knowledge content.

Conference-specific styling and editor settings are not included in the
template. No conference notes, personal information, or credentials are copied
from the reference repositories.

## Review and Apply Updates

Generate repositories with Cruft as described in
[Getting Started](getting-started.md).
If you originally used Cookiecutter, first link the generated repository:

```bash
cruft link https://github.com/electrocucaracha/yt-summarizer-template
```

When linking an existing repository, select the template revision that matches
its original generation and review the recorded context before updating.
For a local template, use its committed Git path instead of the remote URL.

From a clean generated repository, run:

```bash
make template-check
make template-diff
make template-update
```

Review the diff, resolve any conflicts, run `make lint`, and commit the updated
shared files and Cruft metadata.
If knowledge files changed, also run `make check` with Kiso installed.
Never force template changes over uncommitted content.

To change the upstream template rather than update a generated repository, see
[Contributing](../CONTRIBUTING.md).
Return to the [project overview](../README.md).
