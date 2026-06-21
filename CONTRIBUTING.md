# Contributing

Thanks for contributing!

## Dev setup

- Use Python 3.14+
- This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) as its project dependecy manager due its vastly greater developer-experience. After installing uv, run the following command:

```bash
uv sync
```

This will pick up all the required dependecies from the lock file attached to this project.

## Quality gates

Before opening a PR:
- Run unit tests: `python -m pytest`
- Keep functions small and documented (docstrings).
- Please format your codebase once before creating PR using project's linting tool: Ruff.

```bash
 uv run ruff format .
```
