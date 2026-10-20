"""
Week 2 • Day 5 (Lec 61) — Animated SVG Revealer Utility
======================================================
Inspired by Simon Willison's SVG AI benchmark ("Pelican riding a bike").
Injects CSS keyframes and staggered animation delays into raw SVG shapes and paths
so that the SVG draws itself on screen dynamically!
"""

import xml.etree.ElementTree as ET
from typing import Optional


def tag(el) -> str:
    """Strips XML namespace URI to get the base element tag name."""
    return el.tag.split("}", 1)[-1]


def clean_svg_markup(svg_text: str) -> str:
    """Extracts pure <svg>...</svg> XML if the model wrapped it in markdown or comments."""
    if not svg_text:
        return ""
    text = svg_text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    start_idx = text.find("<svg")
    end_idx = text.rfind("</svg>")
    if start_idx != -1 and end_idx != -1:
        text = text[start_idx : end_idx + 6]
    return text


def create_animated_svg(svg_raw: str, step_delay: float = 0.08) -> str:
    """
    Parses SVG XML and attaches staggered CSS animation-delay to every drawable element.
    Returns the enriched SVG markup with embedded @keyframes CSS.
    """
    svg_clean = clean_svg_markup(svg_raw)
    if not svg_clean:
        return ""

    try:
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        root = ET.fromstring(svg_clean)
        drawable = {"path", "line", "ellipse", "rect", "polygon", "polyline", "circle"}

        # Inject CSS Keyframe Animation
        style = ET.SubElement(root, "style")
        style.text = """
        @keyframes reveal {
            from { opacity: 0; stroke-dashoffset: 50; }
            to { opacity: 1; stroke-dashoffset: 0; }
        }
        .reveal {
            opacity: 0;
            animation: reveal 0.25s ease-out forwards;
        }
        """

        delay = 0.0
        for el in root.iter():
            if tag(el) in drawable:
                existing = el.get("style", "")
                el.set("style", f"{existing};animation-delay:{delay:.2f}s".strip(";"))
                el.set("class", (el.get("class", "") + " reveal").strip())
                delay += step_delay

        return ET.tostring(root, encoding="unicode")
    except Exception as e:
        print(f"⚠️ XML Parse warning in revealer: {e}. Returning raw SVG.", flush=True)
        return svg_clean
