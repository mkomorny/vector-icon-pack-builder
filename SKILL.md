---
name: design-kit-icon-pack-builder
description: Automatically generates cohesive, mathematically normalized SVG icon packs (standalone SVGs, sprite sheets, React components, and HTML visual galleries) styled to match the exact visual tokens (stroke weight, caps, corners, and colors) of any design kit or template (808 Programmer, Braun Functionalist, Avionics HUD, Cyberdeck, Bubble Chamber, etc.).
---

# Design Kit Icon Pack Builder

Generates tailored, visually harmonious 24x24 SVG icon packs that inherit the aesthetic DNA of any design kit or app theme.

Whenever the user asks to create an icon set, add icons to an app, or style navigation/audio controls for a specific design template (e.g. `classic-808-programmer`, `avionics-flight-hud`, `braun-dieter-rams`), use this skill to produce consistent, ready-to-use vector assets.

---

## What It Produces

For any target kit or style, the builder outputs a complete package in your destination folder:

1. **`svg/*.svg`** — 40+ clean individual vector files normalized to `viewBox="0 0 24 24"`.
2. **`icons-sprite.svg`** — Production-ready `<symbol>` sprite sheet for zero-dependency web apps.
3. **`Icons.jsx`** — Modern React/JSX icon components with `{...props}` support.
4. **`preview.html`** — Interactive visual showcase rendered in the design kit's exact colors, with 1-click SVG copy-to-clipboard.

---

## Included Icon Catalog (40+ Vectors)

* **Navigation & UI:** `home`, `search`, `settings`, `bell`, `user`, `trash`, `edit`, `copy`, `check`, `close`, `plus`, `minus`, `chevron-down`, `chevron-right`, `arrow-left`, `arrow-right`, `folder`, `file`, `download`, `upload`, `grid`, `eye`, `lock`
* **Audio & Music Production:** `play`, `pause`, `stop`, `record`, `loop`, `waveform`, `sliders`, `dial-knob`, `drum-pad`, `piano-keys`, `metronome`, `volume-high`, `volume-mute`, `microphone`, `headphones`, `layers`, `plug`

---

## Quick Usage / CLI Execution

Run the builder script directly from the skill folder:

```bash
# Build complete icon pack styled for the 808 Drum Machine theme
python "<skill_dir>/scripts/build_icon_pack.py" --kit "classic-808-programmer" --out "./icons-808"

# Build for Avionics HUD (hairline 1px, square caps, phosphor green)
python "<skill_dir>/scripts/build_icon_pack.py" --kit "avionics-flight-hud" --out "./icons-hud"

# Build for Braun Functionalist (clean 1.5px, round caps, Dieter Rams orange)
python "<skill_dir>/scripts/build_icon_pack.py" --kit "braun-dieter-rams" --out "./icons-braun"

# Build only specific icons
python "<skill_dir>/scripts/build_icon_pack.py" --kit "classic-808-programmer" --icons "play,pause,record,waveform,sliders" --out "./audio-controls"
```

---

## Aesthetic Styles & Kit Profiles

| Kit Profile | Stroke Weight | Line Caps & Joins | Default Accent | Best For |
| :--- | :--- | :--- | :--- | :--- |
| `classic-808-programmer` | `2.25px` | `square` / `miter` | `#e63946` (808 Red) | Drum machines, audio hardware, industrial |
| `avionics-flight-hud` | `1.0px` | `square` / `miter` | `#00ffcc` (Cyan) | HUDs, telemetry, radar, technical monitors |
| `braun-dieter-rams` | `1.5px` | `round` / `round` | `#ff5500` (Signal Orange) | Minimalist, mid-century hardware, tools |
| `bubble-chamber-event` | `1.25px` | `round` / `round` | `#3fd0e0` (Track Cyan) | Scientific visualizations, clean laboratory UI |
| `netrunner-cyberdeck` | `1.75px` | `square` / `miter` | `#ff007f` (Hot Pink) | Cyberpunk, terminal dashboards, neon |
| `default` | `1.5px` | `round` / `round` | `#38bdf8` (Sky Blue) | Clean, versatile modern web apps |

---

## Database Sourcing for Custom Glyphs

When a user requests an unusual or non-standard icon outside the 40+ core vectors (e.g. specialized scientific instruments, obscure transit glyphs, or circuit symbols):
* Query the local vector icon database in `/data/output`.
* Extract the matching path coordinates and normalize them into the 24x24 grid using the same stroke and cap rules.
