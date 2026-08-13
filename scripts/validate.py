#!/usr/bin/env python3
"""Validate YAML syntax, style, schemas and known examples without network access."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

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

    lint = subprocess.run(
        ["yamllint", "-c", str(ROOT / ".yamllint.yml"), str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    if lint.returncode:
        failures.append(lint.stdout or lint.stderr)

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

    pairs = [
        (
            ROOT / "schemas/datagovops-public-sector-profile.schema.yaml",
            ROOT / "examples/minimal-data-product.yaml",
        ),
        (
            ROOT / "schemas/datagovsecops-profile.schema.yaml",
            ROOT / "examples/minimal-security-profile.yaml",
        ),
    ]
    for schema_path, example_path in pairs:
        if schema_path in documents and example_path in documents:
            validator = Draft202012Validator(
                documents[schema_path],
                format_checker=FormatChecker(),
            )
            for error in validator.iter_errors(documents[example_path]):
                location = ".".join(str(part) for part in error.absolute_path)
                failures.append(
                    f"{example_path.relative_to(ROOT)}:{location}: {error.message}"
                )

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print(f"Validated {len(documents)} YAML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
