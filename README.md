# DataGovSecOps

Open security, compliance and assurance extensions for governed data products.

DataGovSecOps connects machine-readable data governance with security controls, supply-chain assurance, policy evidence and automated validation across the data-product lifecycle.

> Status: early-stage research and reference implementation. Controls are illustrative and do not replace organizational risk assessment, legal review or security accreditation.

## Scope

- Security metadata for data contracts and data products
- Classification, access, integrity and provenance controls
- Evidence requirements and control ownership
- CI/CD validation and policy-as-code readiness
- Data and software supply-chain assurance
- Swedish public-sector security and archival considerations

## Relationship to DataGovOps

This repository contains security-focused public profiles and reference controls. The foundational governance model lives in `frecke/datagovops`.

Detailed control assessment methods, customer mappings, implementation playbooks and commercial policy packs remain private in `frecke/datagovsecops-private`.

## Repository layout

- `schemas/` security profile schemas
- `controls/` open control definitions
- `examples/` fictional examples
- `docs/` architecture notes and decisions
- `scripts/` validation tooling
- `tests/` validation fixtures and guidance

## Licensing

Code and schemas are licensed under Apache License 2.0. Documentation is licensed under CC BY 4.0 unless a file states otherwise.

## Contributing

See `CONTRIBUTING.md`, `GOVERNANCE.md` and `SECURITY.md`.
