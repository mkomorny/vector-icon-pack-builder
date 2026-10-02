# Vector Icon Pack Builder - Setup & Usage Guide

## Prerequisites
- **Python**: 3.8+

---

## 1. Compiling an Icon Pack

Generate a standard 24x24 normalized icon pack with 2px stroke width and round caps:
```bash
python scripts/build_icon_pack.py --stroke-width 2 --cap round --join round --output ./dist/icons
```

Generate sharp technical avionics icons:
```bash
python scripts/build_icon_pack.py --stroke-width 1.5 --cap square --join miter --color "#00ff66" --output ./dist/avionics_icons
```
