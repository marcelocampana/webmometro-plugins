#!/usr/bin/env python3
"""Extract readable slide text from a PPTX guide into Markdown."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    if not match:
        raise ValueError(f"Not a slide XML path: {name}")
    return int(match.group(1))


def extract_text(pptx_path: Path) -> str:
    lines = [f"# Extracted PPTX Guide: {pptx_path.name}", ""]
    with ZipFile(pptx_path) as archive:
        slides = sorted(
            [
                name
                for name in archive.namelist()
                if re.search(r"ppt/slides/slide\d+\.xml$", name)
            ],
            key=slide_number,
        )
        lines.append(f"Slides: {len(slides)}")
        lines.append("")

        for index, slide in enumerate(slides, start=1):
            root = ET.fromstring(archive.read(slide))
            texts = [
                node.text.strip()
                for node in root.findall(".//a:t", NS)
                if node.text and node.text.strip()
            ]
            lines.append(f"## Slide {index}")
            if texts:
                lines.extend(f"- {text}" for text in texts)
            else:
                lines.append("- [No readable text extracted]")
            lines.append("")

    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: extract_pptx_guide.py input.pptx [output.md]", file=sys.stderr)
        return 2

    pptx_path = Path(sys.argv[1]).expanduser().resolve()
    if not pptx_path.exists():
        print(f"Missing file: {pptx_path}", file=sys.stderr)
        return 1

    markdown = extract_text(pptx_path)
    if len(sys.argv) == 3:
        output_path = Path(sys.argv[2]).expanduser().resolve()
        output_path.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
