#!/usr/bin/env python3
"""Generate a Google Fonts Article readiness report."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/article-readiness.md")
ARTICLE = Path("documentation/google-fonts/ARTICLE.en_us.html")
IMAGE_LICENSE = Path("documentation/assets/image-license.txt")
LANGUAGE_METADATA = Path("documentation/google-fonts/google-fonts-language-metadata.md")
PLACEHOLDER_URL = "https://github.com/fontgarden/virtua-grotesk"
MAX_RASTER_IMAGE_BYTES = 1_750_000
RECOMMENDED_IMAGE_WIDTH = 1000
ARABIC_RE = re.compile(r"[\u0600-\u06ff]")
ALLOWED_TAGS = {
    "a",
    "blockquote",
    "code",
    "em",
    "figcaption",
    "figure",
    "h3",
    "h4",
    "h5",
    "hr",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "span",
    "strong",
    "sub",
    "ul",
    "video",
}
FORBIDDEN_TAGS = {
    "applet",
    "base",
    "embed",
    "form",
    "frame",
    "frameset",
    "head",
    "iframe",
    "link",
    "math",
    "meta",
    "object",
    "script",
    "style",
    "svg",
    "template",
}


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.links: list[str] = []
        self.images: list[str] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        attrs_dict = {name: value for name, value in attrs}
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"] or "")
        if tag == "img" and attrs_dict.get("src"):
            self.images.append(attrs_dict["src"] or "")

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def png_dimensions(path: Path) -> tuple[int | None, int | None]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return (None, None)
    width, height = struct.unpack(">II", data[16:24])
    return (width, height)


def language_primary_script() -> str:
    path = ROOT / LANGUAGE_METADATA
    if not path.exists():
        return "unknown"
    match = re.search(r"Script id: `([^`]+)`", path.read_text(encoding="utf-8"))
    return match.group(1) if match else "unknown"


def image_statuses(images: list[str], image_license_text: str) -> list[dict[str, str | int | None]]:
    rows = []
    for src in images:
        path = ROOT / "documentation" / "assets" / Path(src).name
        width = height = None
        if path.exists() and path.suffix.lower() == ".png":
            width, height = png_dimensions(path)
        rows.append(
            {
                "src": src,
                "exists": "yes" if path.exists() else "no",
                "bytes": path.stat().st_size if path.exists() else None,
                "width": width,
                "height": height,
                "provenance": "yes" if src in image_license_text else "no",
            }
        )
    return rows


def markdown_report() -> str:
    article_text = (ROOT / ARTICLE).read_text(encoding="utf-8")
    parser = ArticleParser()
    parser.feed(article_text)
    tags = sorted(set(parser.tags))
    disallowed_tags = sorted(tag for tag in tags if tag not in ALLOWED_TAGS)
    forbidden_tags = sorted(tag for tag in tags if tag in FORBIDDEN_TAGS)
    text = " ".join(part.strip() for part in parser.text_parts if part.strip())
    words = re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text)
    image_license_path = ROOT / IMAGE_LICENSE
    image_license_text = image_license_path.read_text(encoding="utf-8") if image_license_path.exists() else ""
    primary_script = language_primary_script()
    localized_arabic_text = bool(ARABIC_RE.search(text))
    image_rows = image_statuses(parser.images, image_license_text)
    raster_images_within_limit = all(
        row["bytes"] is not None and int(row["bytes"]) <= MAX_RASTER_IMAGE_BYTES
        for row in image_rows
    )
    images_recommended_width = all(
        row["width"] is not None and int(row["width"]) >= RECOMMENDED_IMAGE_WIDTH
        for row in image_rows
    )
    provenance_count = sum(1 for row in image_rows if row["provenance"] == "yes")
    upstream_links = [link for link in parser.links if "github.com/" in link]
    placeholder_links = [link for link in parser.links if PLACEHOLDER_URL in link]

    lines = [
        "# Article Readiness",
        "",
        "This generated report checks the Google Fonts Article draft against",
        "the current Article guide requirements that can be verified locally.",
        "It does not replace copy review by Google Fonts.",
        "",
        "## Summary",
        "",
        f"- Article file: `{ARTICLE}`",
        f"- Article exists: {yes_no((ROOT / ARTICLE).exists())}",
        f"- Text length: {len(words)} words",
        f"- More than 100 text characters: {yes_no(len(text) > 100)}",
        f"- Around 500 words target met: {yes_no(400 <= len(words) <= 650)}",
        f"- Primary script target from metadata: `{primary_script}`",
        f"- Localized Arabic text present: {yes_no(localized_arabic_text)}",
        f"- Upstream repository link present: {yes_no(bool(upstream_links))}",
        f"- Placeholder upstream URL still present: {yes_no(bool(placeholder_links))}",
        f"- Images referenced: {len(parser.images)}",
        f"- Referenced images exist locally: {yes_no(all(row['exists'] == 'yes' for row in image_rows))}",
        f"- Raster images within 1.75 MB limit: {yes_no(raster_images_within_limit)}",
        f"- Images meet 1000 px recommended width: {yes_no(images_recommended_width)}",
        f"- Image license/provenance file exists: {yes_no(image_license_path.exists())}",
        f"- Article image sources covered by provenance file: {provenance_count} / {len(image_rows)}",
        f"- Disallowed HTML tags: {len(disallowed_tags)}",
        f"- Forbidden HTML tags: {len(forbidden_tags)}",
        "",
        "## HTML Tags",
        "",
        f"- Used tags: `{', '.join(tags) if tags else 'none'}`",
        f"- Disallowed tags: `{', '.join(disallowed_tags) if disallowed_tags else 'none'}`",
        f"- Forbidden tags: `{', '.join(forbidden_tags) if forbidden_tags else 'none'}`",
        "",
        "## Links",
        "",
    ]
    if parser.links:
        lines.extend(f"- `{link}`" for link in parser.links)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Images",
            "",
            "| Source | Exists locally | Size | Dimensions | Provenance documented |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in image_rows:
        size = f"{row['bytes']} bytes" if row["bytes"] is not None else "missing"
        dimensions = (
            f"{row['width']} x {row['height']}"
            if row["width"] is not None and row["height"] is not None
            else "unknown"
        )
        lines.append(f"| `{row['src']}` | {row['exists']} | {size} | {dimensions} | {row['provenance']} |")

    lines.extend(
        [
            "",
            "## Apply Before Packaging",
            "",
            "- Replace the placeholder upstream repository URL after the public URL",
            "  decision is confirmed.",
            "- Keep Article images in the downstream `article/` directory and keep",
            "  `documentation/assets/image-license.txt` current for provenance review.",
            "- Confirm whether Google Fonts wants additional Arabic/localized",
            "  Article text for the `Arab` primary script before final packaging.",
            "- If the package uses Article content, do not also ship a duplicate",
            "  legacy `DESCRIPTION.en_us.html` unless Google Fonts asks for it.",
            "- Rerun `make preflight` after Article text, image, or package",
            "  source-mapping changes.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/article.html",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_article_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
