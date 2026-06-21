# Introduction

![alt text](assets/absolute_mental_state.webp)

Ever felt like "uhhh ..." actually I don't have any narrative for today.

But it is often tiresome to manually setup pyprojects when most of it is boilerplate, so ... let's change that

## Features

* **Lightning Fast Dependency Management:** Uses [`uv`](https://docs.astral.sh/uv/) instead of pip/poetry for ridiculously fast package resolution and syncing.
* **Modern Build System:** Pre-configured with `hatchling` via `pyproject.toml`.
* **Linting & Formatting:** Uses `ruff` for blazingly fast code formatting and linting.
* **Testing Ready:** Ships with `pytest` and a dummy test file to ensure your CI/CD passes on day one.
* **Distribution Ready:** Includes `build`, `twine`, and `pyinstaller` in dev dependencies so you are ready to publish to PyPI or build standalone executables.

## Usage

You can use `pyplatez` to instantly scaffold a batteries-included Python project or also you can use this directly in GitHub as template repository.

### Installation
Install the package globally using `pip` or `uv`:

```bash
pip install pyplatez
# or use uv (Recommended)
uv tool install pyplatez
```

### To create a new project

```bash
pyplatez init pyproj
```

By default, this will create a new directory in your current folder. If you want to specify a custom path, use the `--path` flag:

```bash
pyplatez init pyproj --path ~/Projects/pyproj
```

Navigate to the folder & sync all dependencies:

```bash
cd pyproj
uv sync
```

& Start Comding!

## Directory Structure

Here is how the boilerplate is organized:

```text
pyplatez/
├── .github/
│   ├── ISSUE_TEMPLATE/       # YAML issue templates & discussions config
│   ├── workflows/            # GitHub Actions for CI/CD pipeline
│   ├── CODEOWNERS            # Repository ownership definitions
│   ├── FUNDING.yml           # Sponsorships
│   └── PULL_REQUEST_TEMPLATE.md
├── assets/                   # Images and static assets for docs
├── src/                      # Application source code
│   └── pyplatez/             # The main package directory
│       └── cli.py            # Command-line interface logic for scaffolding via `pyplatez init`
├── tests/                    # Unit tests via pytest
├── CODE_OF_CONDUCT.md        # Community guidelines
├── CONTRIBUTING.md           # Instructions for dev setup and PRs
├── hatch_build.py            # Custom build hook that dynamically bundles template files into the wheel
├── LICENSE                   # Open source license
├── main.py                   # Default application entry point
├── pyproject.toml            # The heart of the project configuration
├── README.md                
└── uv.lock                   # Exact dependency versions for reproducibility
```

## Getting Started

1. Clone the template (or click "Use this template" on GitHub).
2. install uv if you haven't already:

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

3.Sync all dependencies

```bash
uv sync
```

4.Run the tests to make sure everything works:

```bash
uv run pytest
```

5.Start coding, Drop your logic into main.py and build from there.

Even Contributing Guidelines, Code-Of-Conduct & Issue templates are filled with boilerplate with minimal editing as per your project needs.

## Future

Planning to make this customizable for different purposes for lightning fast iteration.

## License

[MIT](https://github.com/PranavU-Coder/PyPlatez?tab=MIT-1-ov-file)

## Other

Please do consider starring this template if you found it useful for your everday programming needs!

<a href="https://www.star-history.com/?repos=PranavU-Coder%2FPyPlatez&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=PranavU-Coder/PyPlatez&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=PranavU-Coder/PyPlatez&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=PranavU-Coder/PyPlatez&type=date&legend=top-left" />
 </picture>
</a>
