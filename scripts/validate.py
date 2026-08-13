#!/usr/bin/env python3
"""Validate YAML syntax and JSON Schema examples without network access."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "venv", "__pycache__"}


def yaml_files() -> list[Path]:
    return sorted(
        path
        for pattern in ("*.yaml", "*.yml")
        for path in ROOT.rglob(pattern)
        if not EXCLUDED.intersection(path.parts)
    )


def main() -> int:
    failures: list[str] = []
    documents: dict[Path, object] = {}

    for path in yaml_files():
        try:
            documents[path] = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # validation entrypoint
            failures.append(f"{path.relative_to(ROOT)}: {exc}")

    for path, document in documents.items():
        if path.name.endswith(".schema.yaml") and isinstance(document, dict):
            try:
                Draft202012Validator.check_schema(document)
            except Exception as exc:  # validation entrypoint
                failures.append(f"{path.relative_to(ROOT)}: invalid JSON Schema: {exc}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print(f"Validated {len(documents)} YAML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
