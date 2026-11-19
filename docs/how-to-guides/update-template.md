---
title: Update a generated repository
parent: How-to guides
nav_order: 4
---

# Update a generated repository

Use Cruft to review and apply shared template changes.
Updates are manual and leave [repository-owned files](../explanations/template-model.md)
out of the template patch.

If you generated your repository with Cookiecutter instead of
[Cruft](create-knowledge-repository.md), run `make install` first, then link it:

```bash
cruft link https://github.com/electrocucaracha/yt-summarizer-template
```

Select the template revision that matches the original generation and review
the recorded settings. Use a committed local Git path instead of the URL if
you generated from a local template.

From a clean working tree in the generated repository, run:

```bash
make template-check
make template-diff
make template-update
```

Review the resulting diff and resolve conflicts before committing the shared
changes and `.cruft.json`. Run `make lint` on the updated scripts.
If the update changes the pinned summarizer version, run `make install` again.
If you also change the knowledge bundle, run `make check` with Kiso installed.
Adopt new manifest settings manually; do not remove the exclusions to force
an update over your notes or configuration.
