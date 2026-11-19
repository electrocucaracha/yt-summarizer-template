---
title: Publish a knowledge portal
parent: How-to guides
nav_order: 2
---

# Publish a knowledge portal

Build a static site from the notes in your generated repository.
The deployment workflow publishes committed files; it does not fetch transcripts
or run the summarizer.

## Preview locally

After you [generate notes](create-knowledge-repository.md), run the following
from the generated repository. The first run downloads the pinned Kiso CLI
into a local cache:

```bash
make check
make preview
```

Open <http://127.0.0.1:8099> and check that you can browse from the home page
to a collection and its notes.
Use `make preview PORT=8100` if port 8099 is already in use.
To build without serving, run `make build`; the static site goes to `public/`.

## Publish on GitHub Pages

Pages may make your notes public, even if the repository itself is private.
Verify site visibility and check the notes for sensitive or unreviewed content
before deployment. For private use, stop at the local preview or
[index the notes locally](search-notes.md).

1. Commit the reviewed notes and push the generated repository to GitHub.
2. In that repository, open **Settings** > **Pages** and set **Source** to
   **GitHub Actions**. This differs from the template documentation site,
   which publishes directly from the template repository's `main` branch.
3. In **Actions**, select **Publish Knowledge Base** and run it manually for the
   generated default branch, or push a change to that branch.
4. Open the deployment URL from the successful workflow run and verify that
   it shows your notes.

If a later deployment omits new notes, check that you committed them and pushed
them to the branch configured in the generated workflow.
