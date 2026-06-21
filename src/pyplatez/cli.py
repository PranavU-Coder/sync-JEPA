import argparse
import shutil
import sys
from importlib import resources
from pathlib import Path


def scaffold(project_name: str, package_name: str, target: Path) -> None:
    with resources.as_file(
        resources.files("pyplatez").joinpath("templates")
    ) as tmpl_dir:
        shutil.copytree(tmpl_dir, target, dirs_exist_ok=True)

    old_pkg = target / "src" / "pyplatez"
    new_pkg = target / "src" / package_name
    if old_pkg.exists():
        old_pkg.rename(new_pkg)

    pyproject = target / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text()
        text = text.replace('name = "pyplatez"', f'name = "{project_name}"')
        text = text.replace(
            'description = "minimalist python template for professional/hobbyist works"',
            'description = "Add your description here"',
        )
        pyproject.write_text(text)

    print(f" '{project_name}' ready at ./{target.name}")
    print(f"   cd {target.name} && uv sync")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pyplatez",
        description="A batteries-included Python-starter project-template",
    )
    sub = parser.add_subparsers(dest="command")

    init = sub.add_parser("init", help="Create a new project")
    init.add_argument("name", help="Project name")
    init.add_argument(
        "--path", default=None, help="Where to create it (default: ./<name>)"
    )

    args = parser.parse_args()

    if args.command == "init":
        package_name = args.name.replace("-", "_")
        if not package_name.isidentifier():
            print(
                f" Error: '{args.name}' cannot be normalized to a valid Python package name.",
                file=sys.stderr,
            )
            sys.exit(1)

        target = Path(args.path) if args.path else Path.cwd() / args.name

        if target.exists():
            if not target.is_dir():
                print(
                    f" Error: '{target}' already exists and is a file, not a directory.",
                    file=sys.stderr,
                )
                sys.exit(1)
            if any(target.iterdir()):
                print(
                    f" Error: '{target}' already exists and is not empty.",
                    file=sys.stderr,
                )
                sys.exit(1)

        target.mkdir(parents=True, exist_ok=True)
        scaffold(args.name, package_name, target)
    else:
        parser.print_help()
