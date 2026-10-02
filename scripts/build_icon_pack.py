#!/usr/bin/env python3
"""
Design Kit Icon Pack Builder
Generates mathematically normalized, theme-styled SVG icon packs matching any design kit.
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Built-in high-precision 24x24 geometric icon vector paths
# Formatted as clean path d-strings or element templates designed for viewBox="0 0 24 24"
ICONS_REGISTRY = {
    # --- Navigation & Standard UI ---
    "home": [
        '<path d="M3 10.5L12 3l9 7.5v9a1.5 1.5 0 01-1.5 1.5h-4.5v-6h-6v6H4.5A1.5 1.5 0 013 19.5v-9z" />'
    ],
    "search": [
        '<circle cx="11" cy="11" r="7" />',
        '<line x1="16.5" y1="16.5" x2="21" y2="21" />'
    ],
    "settings": [
        '<circle cx="12" cy="12" r="3" />',
        '<path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 01-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z" />'
    ],
    "bell": [
        '<path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />',
        '<path d="M13.73 21a2 2 0 01-3.46 0" />'
    ],
    "user": [
        '<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />',
        '<circle cx="12" cy="7" r="4" />'
    ],
    "trash": [
        '<path d="M3 6h18" />',
        '<path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6" />',
        '<path d="M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2" />',
        '<line x1="10" y1="11" x2="10" y2="17" />',
        '<line x1="14" y1="11" x2="14" y2="17" />'
    ],
    "edit": [
        '<path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />',
        '<path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />'
    ],
    "copy": [
        '<rect x="9" y="9" width="13" height="13" rx="2" ry="2" />',
        '<path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />'
    ],
    "check": [
        '<polyline points="20 6 9 17 4 12" />'
    ],
    "close": [
        '<line x1="18" y1="6" x2="6" y2="18" />',
        '<line x1="6" y1="6" x2="18" y2="18" />'
    ],
    "plus": [
        '<line x1="12" y1="5" x2="12" y2="19" />',
        '<line x1="5" y1="12" x2="19" y2="12" />'
    ],
    "minus": [
        '<line x1="5" y1="12" x2="19" y2="12" />'
    ],
    "chevron-down": [
        '<polyline points="6 9 12 15 18 9" />'
    ],
    "chevron-right": [
        '<polyline points="9 18 15 12 9 6" />'
    ],
    "arrow-left": [
        '<line x1="19" y1="12" x2="5" y2="12" />',
        '<polyline points="12 19 5 12 12 5" />'
    ],
    "arrow-right": [
        '<line x1="5" y1="12" x2="19" y2="12" />',
        '<polyline points="12 5 19 12 12 19" />'
    ],
    "folder": [
        '<path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z" />'
    ],
    "file": [
        '<path d="M13 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V9z" />',
        '<polyline points="13 2 13 9 20 9" />'
    ],
    "download": [
        '<path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />',
        '<polyline points="7 10 12 15 17 10" />',
        '<line x1="12" y1="15" x2="12" y2="3" />'
    ],
    "upload": [
        '<path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />',
        '<polyline points="17 8 12 3 7 8" />',
        '<line x1="12" y1="3" x2="12" y2="15" />'
    ],
    "grid": [
        '<rect x="3" y="3" width="7" height="7" />',
        '<rect x="14" y="3" width="7" height="7" />',
        '<rect x="14" y="14" width="7" height="7" />',
        '<rect x="3" y="14" width="7" height="7" />'
    ],
    "eye": [
        '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />',
        '<circle cx="12" cy="12" r="3" />'
    ],
    "lock": [
        '<rect x="3" y="11" width="18" height="11" rx="2" ry="2" />',
        '<path d="M7 11V7a5 5 0 0110 0v4" />'
    ],

    # --- Audio, Music Production & DAW Controls ---
    "play": [
        '<polygon points="5 3 19 12 5 21 5 3" />'
    ],
    "pause": [
        '<line x1="6" y1="4" x2="6" y2="20" />',
        '<line x1="18" y1="4" x2="18" y2="20" />'
    ],
    "stop": [
        '<rect x="4" y="4" width="16" height="16" />'
    ],
    "record": [
        '<circle cx="12" cy="12" r="8" fill="var(--accent, #e63946)" />'
    ],
    "loop": [
        '<path d="M17 2l4 4-4 4" />',
        '<path d="M3 11v-1a4 4 0 014-4h14" />',
        '<path d="M7 22l-4-4 4-4" />',
        '<path d="M21 13v1a4 4 0 01-4 4H3" />'
    ],
    "waveform": [
        '<line x1="3" y1="12" x2="3" y2="12.01" />',
        '<line x1="6" y1="8" x2="6" y2="16" />',
        '<line x1="9" y1="5" x2="9" y2="19" />',
        '<line x1="12" y1="3" x2="12" y2="21" />',
        '<line x1="15" y1="7" x2="15" y2="17" />',
        '<line x1="18" y1="10" x2="18" y2="14" />',
        '<line x1="21" y1="12" x2="21" y2="12.01" />'
    ],
    "sliders": [
        '<line x1="4" y1="21" x2="4" y2="14" />',
        '<line x1="4" y1="10" x2="4" y2="3" />',
        '<line x1="12" y1="21" x2="12" y2="12" />',
        '<line x1="12" y1="8" x2="12" y2="3" />',
        '<line x1="20" y1="21" x2="20" y2="16" />',
        '<line x1="20" y1="12" x2="20" y2="3" />',
        '<circle cx="4" cy="12" r="2" />',
        '<circle cx="12" cy="10" r="2" />',
        '<circle cx="20" cy="14" r="2" />'
    ],
    "dial-knob": [
        '<circle cx="12" cy="12" r="9" />',
        '<line x1="12" y1="12" x2="12" y2="5" />',
        '<circle cx="12" cy="12" r="2" />'
    ],
    "drum-pad": [
        '<rect x="2" y="2" width="20" height="20" rx="3" ry="3" />',
        '<line x1="2" y1="12" x2="22" y2="12" />',
        '<line x1="12" y1="2" x2="12" y2="22" />'
    ],
    "piano-keys": [
        '<rect x="2" y="3" width="20" height="18" rx="2" ry="2" />',
        '<line x1="7" y1="3" x2="7" y2="13" />',
        '<line x1="12" y1="3" x2="12" y2="13" />',
        '<line x1="17" y1="3" x2="17" y2="13" />',
        '<line x1="7" y1="21" x2="7" y2="13" />',
        '<line x1="12" y1="21" x2="12" y2="13" />',
        '<line x1="17" y1="21" x2="17" y2="13" />'
    ],
    "metronome": [
        '<path d="M5 20h14L15 4H9L5 20z" />',
        '<line x1="12" y1="10" x2="17" y2="6" />',
        '<circle cx="17" cy="6" r="1.5" />'
    ],
    "volume-high": [
        '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />',
        '<path d="M19.07 4.93a10 10 0 010 14.14M15.54 8.46a5 5 0 010 7.07" />'
    ],
    "volume-mute": [
        '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />',
        '<line x1="23" y1="9" x2="17" y2="15" />',
        '<line x1="17" y1="9" x2="23" y2="15" />'
    ],
    "microphone": [
        '<path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" />',
        '<path d="M19 10v2a7 7 0 01-14 0v-2" />',
        '<line x1="12" y1="19" x2="12" y2="23" />',
        '<line x1="8" y1="23" x2="16" y2="23" />'
    ],
    "headphones": [
        '<path d="M3 18v-6a9 9 0 0118 0v6" />',
        '<path d="M21 19a2 2 0 01-2 2h-1a2 2 0 01-2-2v-3a2 2 0 012-2h3zM3 19a2 2 0 002 2h1a2 2 0 002-2v-3a2 2 0 00-2-2H3z" />'
    ],
    "layers": [
        '<polygon points="12 2 2 7 12 12 22 7 12 2" />',
        '<polyline points="2 17 12 22 22 17" />',
        '<polyline points="2 12 12 17 22 12" />'
    ],
    "plug": [
        '<path d="M12 22v-5" />',
        '<path d="M9 8V2" />',
        '<path d="M15 8V2" />',
        '<path d="M18 8v5a6 6 0 01-12 0V8z" />'
    ]
}

# Kit Aesthetic Presets for automatic styling when kit is named
KIT_AESTHETICS = {
    # 808 / Industrial / Sampler
    "classic-808-programmer": {
        "stroke_width": 2.25,
        "linecap": "square",
        "linejoin": "miter",
        "bg": "#1a1918",
        "fg": "#f4f1de",
        "accent": "#e63946",
        "border": "#3d3b38"
    },
    # Avionics / HUD / Radar
    "avionics-flight-hud": {
        "stroke_width": 1.0,
        "linecap": "square",
        "linejoin": "miter",
        "bg": "#030806",
        "fg": "#00ff66",
        "accent": "#00ffcc",
        "border": "#0a2916"
    },
    # Braun / Dieter Rams Functionalist
    "braun-dieter-rams": {
        "stroke_width": 1.5,
        "linecap": "round",
        "linejoin": "round",
        "bg": "#e8e8e6",
        "fg": "#1a1a1a",
        "accent": "#ff5500",
        "border": "#d0d0ce"
    },
    # Bubble Chamber / Science
    "bubble-chamber-event": {
        "stroke_width": 1.25,
        "linecap": "round",
        "linejoin": "round",
        "bg": "#07090c",
        "fg": "#e2f1f8",
        "accent": "#3fd0e0",
        "border": "#1a242f"
    },
    # Cyberdeck / Netrunner
    "netrunner-cyberdeck": {
        "stroke_width": 1.75,
        "linecap": "square",
        "linejoin": "miter",
        "bg": "#090a0f",
        "fg": "#39ff14",
        "accent": "#ff007f",
        "border": "#1a1c24"
    },
    # Minimal Modern (Default fallback)
    "default": {
        "stroke_width": 1.5,
        "linecap": "round",
        "linejoin": "round",
        "bg": "#0f172a",
        "fg": "#f8fafc",
        "accent": "#38bdf8",
        "border": "#334155"
    }
}

def generate_svg(icon_name, elements, style):
    sw = style["stroke_width"]
    lc = style["linecap"]
    lj = style["linejoin"]
    inner = "\n  ".join(elements)
    
    # Replace default stroke/fill tags with styled attributes
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="{lc}" stroke-linejoin="{lj}">
  {inner}
</svg>"""
    return svg

def build_pack(kit_name, out_dir, selected_icons=None):
    style = KIT_AESTHETICS.get(kit_name, KIT_AESTHETICS["default"])
    out_path = Path(out_dir)
    svgs_path = out_path / "svg"
    svgs_path.mkdir(parents=True, exist_ok=True)
    
    icons_to_build = ICONS_REGISTRY.keys() if not selected_icons else [i.strip() for i in selected_icons.split(",") if i.strip() in ICONS_REGISTRY]
    
    rendered_icons = {}
    sprite_symbols = []
    
    for name in icons_to_build:
        elements = ICONS_REGISTRY[name]
        svg_content = generate_svg(name, elements, style)
        rendered_icons[name] = svg_content
        
        # Write individual SVG file
        with open(svgs_path / f"{name}.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        # Prepare symbol for SVG sprite sheet
        inner_content = "\n    ".join(elements)
        sprite_symbols.append(f"""  <symbol id="icon-{name}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{style['stroke_width']}" stroke-linecap="{style['linecap']}" stroke-linejoin="{style['linejoin']}">
    {inner_content}
  </symbol>""")

    # Write SVG sprite sheet
    sprite_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">\n{"\n".join(sprite_symbols)}\n</svg>"""
    with open(out_path / "icons-sprite.svg", "w", encoding="utf-8") as f:
        f.write(sprite_svg)

    # Write React / JavaScript icon component file
    react_components = []
    react_components.append("import React from 'react';\n")
    for name, svg_str in rendered_icons.items():
        comp_name = "".join(part.capitalize() for part in name.split("-")) + "Icon"
        clean_jsx = svg_str.replace('xmlns="http://www.w3.org/2000/svg"', '{...props}')
        clean_jsx = clean_jsx.replace('stroke-width=', 'strokeWidth=')
        clean_jsx = clean_jsx.replace('stroke-linecap=', 'strokeLinecap=')
        clean_jsx = clean_jsx.replace('stroke-linejoin=', 'strokeLinejoin=')
        clean_jsx = clean_jsx.replace('viewBox=', 'viewBox=')
        react_components.append(f"export const {comp_name} = (props) => (\n  {clean_jsx}\n);")
    
    with open(out_path / "Icons.jsx", "w", encoding="utf-8") as f:
        f.write("\n\n".join(react_components))

    # Write HTML Interactive Showcase & Preview
    preview_cards = []
    for name, svg_str in rendered_icons.items():
        preview_cards.append(f"""
      <div class="icon-card" onclick="copySvg('{name}')" title="Click to copy SVG">
        <div class="icon-frame">{svg_str}</div>
        <span class="icon-name">{name}</span>
      </div>""")

    html_preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{kit_name} · Icon Pack Preview</title>
  <style>
    :root {{
      --bg: {style['bg']};
      --fg: {style['fg']};
      --accent: {style['accent']};
      --border: {style['border']};
      --stroke-w: {style['stroke_width']}px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--fg);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
      padding: 3rem 2rem;
      min-height: 100vh;
    }}
    header {{
      max-width: 1100px;
      margin: 0 auto 2.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }}
    h1 {{ font-size: 1.8rem; font-weight: 700; letter-spacing: -0.02em; }}
    .badge {{
      display: inline-block;
      padding: 0.3rem 0.6rem;
      background: var(--border);
      border-radius: 4px;
      font-size: 0.8rem;
      color: var(--accent);
      font-family: monospace;
    }}
    .grid {{
      max-width: 1100px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
      gap: 1.25rem;
    }}
    .icon-card {{
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.25rem 0.75rem 0.75rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .icon-card:hover {{
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}
    .icon-frame {{
      width: 36px;
      height: 36px;
      margin-bottom: 0.8rem;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--fg);
    }}
    .icon-card:hover .icon-frame {{
      color: var(--accent);
    }}
    .icon-name {{
      font-size: 0.75rem;
      font-family: monospace;
      color: rgba(255, 255, 255, 0.6);
      text-align: center;
      word-break: break-all;
    }}
    #toast {{
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      background: var(--accent);
      color: #000;
      padding: 0.6rem 1.2rem;
      font-weight: 600;
      font-size: 0.85rem;
      border-radius: 4px;
      opacity: 0;
      transition: opacity 0.2s;
      pointer-events: none;
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>Icon Pack: {kit_name}</h1>
      <p style="opacity: 0.7; margin-top: 0.4rem; font-size: 0.9rem;">
        {len(rendered_icons)} icons · Normalized to 24x24 grid · Stroke: {style['stroke_width']}px · Caps: {style['linecap']}
      </p>
    </div>
    <span class="badge">Click any icon to copy SVG</span>
  </header>

  <div class="grid">
    {''.join(preview_cards)}
  </div>

  <div id="toast">Copied SVG to clipboard!</div>

  <script>
    const svgs = {json.dumps(rendered_icons)};
    function copySvg(name) {{
      const code = svgs[name];
      navigator.clipboard.writeText(code).then(() => {{
        const toast = document.getElementById('toast');
        toast.innerText = 'Copied ' + name + '.svg!';
        toast.style.opacity = '1';
        setTimeout(() => {{ toast.style.opacity = '0'; }}, 1500);
      }});
    }}
  </script>
</body>
</html>"""

    with open(out_path / "preview.html", "w", encoding="utf-8") as f:
        f.write(html_preview)

    print(f"Successfully generated {len(rendered_icons)} icons in: {out_path}")
    print(f"  - Standalone SVGs: {svgs_path}")
    print(f"  - SVG Sprite: {out_path / 'icons-sprite.svg'}")
    print(f"  - React Components: {out_path / 'Icons.jsx'}")
    print(f"  - Visual Preview: {out_path / 'preview.html'}")

def main():
    parser = argparse.ArgumentParser(description="Build design-kit-aligned SVG icon packs.")
    parser.add_argument("--kit", default="classic-808-programmer", help="Target design kit name (e.g. classic-808-programmer, avionics-flight-hud, braun-dieter-rams)")
    parser.add_argument("--out", default="./generated-icon-pack", help="Destination output folder")
    parser.add_argument("--icons", default=None, help="Comma-separated icon names or None for all")
    args = parser.parse_args()
    
    build_pack(args.kit, args.out, args.icons)

if __name__ == "__main__":
    main()
