---
title: Template model
parent: Explanations
nav_order: 1
---

# Template model

The template supplies a repeatable workflow without taking ownership of your notes.
It maintains the pinned summarizer version, configuration runner, Make targets,
Python checks, and publishing workflow.
[yt-summarizer](https://github.com/electrocucaracha/yt-summarizer) handles transcript
retrieval, prompts, summary generation, and Open Knowledge Format (OKF) output.

Each generated repository owns `knowledge.toml` and all files under `docs/`.
For example, if you switch models in `knowledge.toml` and correct a summary in
`docs/`, a Cruft update skips both files while it can still update the Makefile.
This also means changes to the template's starter manifest or knowledge index
do not automatically reach existing repositories.

## Two sites with different readers

The template's GitHub Pages site serves these guides from the root `docs/`.
The knowledge portal in a generated repository serves that repository's reviewed
notes from its own `docs/`. Kiso builds that portal from the committed OKF files.
Local QMD search can index the same notes without a deployment.

See how to [publish a knowledge portal](../how-to-guides/publish-knowledge-portal.md)
or [review a template update](../how-to-guides/update-template.md).
