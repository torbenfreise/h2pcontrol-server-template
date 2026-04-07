import tomllib
from pathlib import Path
from types import SimpleNamespace


def _ns(d):
    return SimpleNamespace(**{k: _ns(v) if isinstance(v, dict) else v for k, v in d.items()})


def _project_root() -> Path:
    for parent in Path(__file__).parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError("Could not locate project root (no pyproject.toml found)")


def load() -> SimpleNamespace:
    with open(_project_root() / "config.toml", "rb") as f:
        return _ns(tomllib.load(f))
