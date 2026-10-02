# Vector Icon Pack Builder

[![Automated Release](https://img.shields.io/badge/release-automated_batch_pipeline-blue.svg)](https://github.com/mkomorny)
[![Pipeline Execution](https://img.shields.io/badge/dispatched_by-background_script-informational.svg)](https://github.com/mkomorny)

> [!NOTE]
> **Automated Distribution**: This repository was automatically sanitized, packaged, and published via a scheduled background batch staging pipeline. All file bundling, licensing, and repository synchronization were dispatched automatically by an automated release runner.

An algorithmic SVG vector normalizer and icon set builder. Generates cohesive, mathematically consistent SVG icon packs (standalone SVGs, symbol sprite sheets, and HTML galleries) matching specific design token geometries (stroke weight, stroke caps, corner radii, and color palettes).

## Normalization Engine

- **Geometric Alignment**: Normalizes vector coordinate bounds across standard 24x24 viewBox frames.
- **Stroke & Corner Conformance**: Programmatically transforms vector path attributes (`stroke-width`, `stroke-linecap`, `stroke-linejoin`) to adhere strictly to target design system rules.
- **Icon Registry**: Ships with built-in geometric vector paths for core UI actions, navigation, audio controls, editing, and system status indicators.

## Dependencies

- **Python**: Version 3.8+ (Standard Library: `os`, `sys`, `json`, `argparse`, `pathlib`). Zero external dependencies.

## Instructions

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for CLI commands and normalization parameters.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the [LICENSE](./LICENSE) file for details.
