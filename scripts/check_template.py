"""Validate rendered repositories, runner behavior, and Cruft content ownership."""

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path
from unittest.mock import patch

import yaml
from cookiecutter.main import cookiecutter

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "{{cookiecutter.repo_name}}"


def run(*arguments, cwd):
    """Run a fixture command and retain diagnostics when it fails."""
    return subprocess.run(
        arguments, cwd=cwd, check=True, capture_output=True, text=True
    )


def validate(project, branch):
    """Check rendered configuration and exercise the generated Python tooling."""
    project = project.resolve()
    for filename in project.rglob("*"):
        if not filename.is_file():
            continue
        content = filename.read_text(encoding="utf-8")
        assert "{{cookiecutter." not in content, filename
        assert "{{ cookiecutter." not in content, filename
        assert "{% raw %}" not in content, filename
        if filename.suffix == ".toml":
            tomllib.loads(content)
        if filename.suffix in {".yml", ".yaml"}:
            yaml.safe_load(content)
        if filename.suffix == ".py":
            compile(content, str(filename), "exec")
    workflow = yaml.safe_load((project / ".github/workflows/pages.yml").read_text())
    assert workflow[True]["push"]["branches"] == [branch]
    assert (
        workflow["jobs"]["publish"]["environment"]["url"]
        == "${{ steps.deployment.outputs.page_url }}"
    )
    run(
        "make",
        "--dry-run",
        "install",
        "build",
        "qmd-setup",
        "update-versions",
        "template-update",
        cwd=project,
    )
    for script in project.glob("**/*.sh"):
        run("bash", "-n", str(script), cwd=project)
    validate_runner(project)
    validate_site_styling(project)
    run("make", "lint", cwd=project)


def validate_runner(project):
    """Exercise command validation and dispatch without invoking external services."""
    spec = importlib.util.spec_from_file_location(
        "summarize", project / "scripts/summarize.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the generated summarizer runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    manifest = project / "knowledge.toml"
    original = manifest.read_text()
    config = tomllib.loads(original)
    try:
        module.commands(config)
    except ValueError:
        pass
    else:
        raise AssertionError("An empty playlist manifest must fail")
    configured = (
        original
        + "\n[playlists.conference]\n"
        + 'url = "https://www.youtube.com/playlist?list=fixture"\n'
    )
    manifest.write_text(configured)
    config = tomllib.loads(configured)
    expected = module.commands(config, "conference")[0]
    assert expected[expected.index("--output-dir") + 1] == str(project / "docs")
    assert expected[expected.index("--model") + 1] == config["model"]
    assert expected[expected.index("--language") + 1] == config["language"]
    assert len(module.commands(config)) == 1
    with (
        patch.object(sys, "argv", ["summarize.py"]),
        patch.object(module.subprocess, "run") as execute,
    ):
        module.main()
        execute.assert_called_once_with(expected, cwd=project, check=True)
    dry = run(sys.executable, "scripts/summarize.py", "--dry-run", cwd=project)
    assert "--playlist-url" in dry.stdout
    for change in (
        {"workers": 0},
        {"workers": True},
        {"model": ""},
        {"playlists": {"bad": {"url": "https://example.com/playlist?list=x"}}},
    ):
        try:
            module.commands(config | change)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Invalid configuration accepted: {change}")
    try:
        module.commands(config, "missing")
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown collection accepted")
    manifest.write_text(original)


def validate_site_styling(project):
    """Check that metrics are added once and the template CSS reaches the build."""
    spec = importlib.util.spec_from_file_location(
        "style_site", project / "scripts/style_site.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the generated site styler")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix="yt-site-style-") as temporary:
        root = Path(temporary)
        source = root / "docs"
        destination = root / "public"
        note = source / "conference/talk.md"
        page = destination / "conference/talk.html"
        note.parent.mkdir(parents=True)
        page.parent.mkdir(parents=True)
        (destination / "assets/css").mkdir(parents=True)
        note.write_text(
            "---\nyoutube_stats:\n"
            "  view_count: 1234\n"
            "  like_count: 5\n"
            "  channel_subscriber_count: 6000\n"
            "---\n# Talk\n",
            encoding="utf-8",
        )
        page.write_text(
            '<article class="kiso-content"><h1>Talk</h1></article>',
            encoding="utf-8",
        )
        stylesheet = destination / "assets/css/application.css"
        stylesheet.write_text("/* Kiso styles */\n", encoding="utf-8")

        module.style_site(source, destination)
        module.style_site(source, destination)

        rendered = page.read_text(encoding="utf-8")
        assert rendered.count('class="kiso-youtube-stats"') == 1
        assert "<dt>Views</dt><dd>1,234</dd>" in rendered
        assert "<dt>Likes</dt><dd>5</dd>" in rendered
        assert "<dt>Subscribers</dt><dd>6,000</dd>" in rendered
        css = stylesheet.read_text(encoding="utf-8")
        assert css.count("YouTube knowledge template stylesheet") == 1
        assert ".kiso-youtube-stats" in css


def commit(repository):
    """Commit an isolated fixture without depending on the user's Git identity."""
    run("git", "add", "--all", cwd=repository)
    run(
        "git",
        "-c",
        "user.name=Template Check",
        "-c",
        "user.email=check@example.invalid",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-qm",
        "Template fixture",
        cwd=repository,
    )


def main():
    """Render representative projects and verify upstream updates preserve content."""
    with tempfile.TemporaryDirectory(prefix="yt-template-") as temporary:
        workspace = Path(temporary)
        for context in (
            {},
            {
                "repo_name": "research-notes",
                "project_name": 'Research "Notes"',
                "default_branch": "knowledge",
                "model": "ollama/qwen3",
                "language": "es",
            },
        ):
            output = Path(
                cookiecutter(
                    str(ROOT),
                    no_input=True,
                    output_dir=str(workspace),
                    extra_context=context,
                )
            )
            validate(output, context.get("default_branch", "main"))
        source = workspace / "template"
        source.mkdir()
        shutil.copy(ROOT / "cookiecutter.json", source)
        shutil.copytree(ROOT / PROJECT, source / PROJECT)
        run("git", "init", "-q", "-b", "main", cwd=source)
        commit(source)
        generated = workspace / "cruft-output"
        generated.mkdir()
        run(
            "cruft",
            "create",
            str(source),
            "--no-input",
            "--output-dir",
            str(generated),
            cwd=workspace,
        )
        project = generated / "youtube-knowledge"
        manifest = project / "knowledge.toml"
        manifest.write_text(
            manifest.read_text() + "\n# Repository-owned playlist choices\n"
        )
        note = project / "docs/personal-note.md"
        note.write_text("Repository-owned knowledge\n")
        index = project / "docs/index.md"
        index.write_text(index.read_text() + "\nLocal index edits\n")
        owned = {path: path.read_bytes() for path in (manifest, note, index)}
        shared = source / PROJECT / "Makefile"
        shared.write_text(shared.read_text() + "\n# Shared template update\n")
        for relative in ("knowledge.toml", "docs/index.md"):
            filename = source / PROJECT / relative
            filename.write_text(filename.read_text() + "\nUpstream change\n")
        commit(source)
        run("cruft", "update", "--skip-apply-ask", cwd=project)
        assert "Shared template update" in (project / "Makefile").read_text()
        assert all(path.read_bytes() == value for path, value in owned.items())
        assert not list(project.rglob("*.rej"))
        metadata = json.loads((project / ".cruft.json").read_text())
        assert (
            metadata["commit"]
            == run("git", "rev-parse", "HEAD", cwd=source).stdout.strip()
        )
    print(
        "Template rendering, runner validation, and Cruft content preservation passed."
    )


if __name__ == "__main__":
    main()
