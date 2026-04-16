"""Smoke-test every gallery example: import and run without error."""

import importlib.util
import pathlib

import matplotlib
import pytest

matplotlib.use("Agg")

GALLERY_ROOT = pathlib.Path(__file__).resolve().parent.parent / "galleries" / "examples"


def _discover_examples():
    """Find all .py files under the gallery examples directory."""
    return sorted(
        p for p in GALLERY_ROOT.rglob("*.py")
        if p.name != "__init__.py"
    )


@pytest.mark.parametrize(
    "example",
    _discover_examples(),
    ids=lambda p: f"{p.parent.name}/{p.stem}",
)
def test_gallery_example(example):
    """Each gallery script must run without raising an exception."""
    spec = importlib.util.spec_from_file_location(example.stem, example)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
