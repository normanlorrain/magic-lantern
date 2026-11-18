# Development

Build, test, and run magic-lantern with [uv](https://docs.astral.sh/uv/). uv reads `pyproject.toml`, writes `uv.lock`, and keeps the project environment in `.venv`.

Requires Python 3.11 or newer. `.python-version` pins local development to 3.12, because pygame and a PyMuPDF dependency have no installable wheels for Python 3.15.

## Setup

From the repository root:

```bash
uv sync
```

This creates `.venv`, installs the application and its dependencies, and installs the `dev` group (`pytest`).

Commit `uv.lock` when dependencies change. `.venv` stays untracked.

## Run

```bash
uv run magic-lantern --help
```

Dry run: print slide names and exit. This does not open a window.

```bash
uv run magic-lantern -d 3 tests/images/numbers
```

A config file works the same way:

```bash
uv run magic-lantern -d 3 -c "tests/example 1.toml"
```

A real slideshow opens a pygame window and needs a display:

```bash
uv run magic-lantern tests/images/numbers
```

Quit with `q`.

`tests/magic-lantern.sh` activates `.venv` and runs `magic-lantern`. Run `uv sync` once before using that script.

## Test

```bash
uv run pytest
```

## Build and publish

```bash
uv build
```

Artifacts are written to `dist/`.

Upload to PyPI (requires a token configured for uv):

```bash
uv publish
```

To try a built wheel outside this project environment, pass the same Python version. The wheel filename includes the version from `pyproject.toml`.

```bash
uvx --python 3.12 --from dist/magic_lantern-0.0.20-py3-none-any.whl magic-lantern --help
```
