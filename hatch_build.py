from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

EXCLUDE = {
    "src",
    "dist",
    "__pycache__",
    ".git",
    ".venv",
    "hatch_build.py",
    "uv.lock",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "PKG-INFO",
    ".hatch",
}


class BuildHook(BuildHookInterface):
    def initialize(self, _version, build_data):
        if self.target_name != "wheel":
            return
        # shit doesn't package unless you force it down
        root = Path(self.root)
        force_include = build_data.setdefault("force_include", {})

        for item in root.iterdir():
            if item.name in EXCLUDE:
                continue

            dest = f"pyplatez/templates/{item.name}"
            force_include[str(item)] = dest

        print(
            f"[pyplatez] Bundling {len(force_include)} root items into pyplatez/templates/"
        )
