#!/usr/bin/env python3
"""Validate a candidate Google Fonts designer profile bio.html snippet."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlparse


MIN_CHARS = 200
MAX_CHARS = 1000
MIN_LINKS = 1
MAX_LINKS = 2
FIRST_PERSON_PRONOUN_RE = re.compile(
    r"\b(?:I|me|my|mine|myself|we|us|our|ours|ourselves)\b",
    flags=re.IGNORECASE,
)
SOCIAL_LINK_LABELS = {
    "github.com": {"GitHub"},
    "instagram.com": {"Instagram"},
    "linkedin.com": {"LinkedIn"},
    "twitter.com": {"Twitter", "X"},
    "x.com": {"X", "Twitter"},
}
PLACEHOLDER_MARKERS = ("example.com", "REPLACE-WITH", "TODO", "TBD")


class BioParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.paragraph_count = 0
        self.link_count = 0
        self.links: list[dict[str, str]] = []
        self._current_link: dict[str, str] | None = None
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag.lower())
        if tag.lower() == "p":
            self.paragraph_count += 1
        if tag.lower() == "a":
            self.link_count += 1
            attr_map = {name.lower(): value or "" for name, value in attrs}
            self._current_link = {
                "href": attr_map.get("href", ""),
                "target": attr_map.get("target", ""),
                "text": "",
            }
            self.links.append(self._current_link)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a":
            self._current_link = None

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.text_chunks.append(data)
            if self._current_link is not None:
                self._current_link["text"] = " ".join(
                    [self._current_link["text"], data.strip()]
                ).strip()


def plain_text(html: str) -> str:
    parser = BioParser()
    parser.feed(html)
    return " ".join(" ".join(parser.text_chunks).split())


def normalized_hostname(href: str) -> str:
    hostname = urlparse(href).hostname or ""
    return hostname.removeprefix("www.").lower()


def social_labels_for_href(href: str) -> set[str]:
    hostname = normalized_hostname(href)
    for domain, labels in SOCIAL_LINK_LABELS.items():
        if hostname == domain or hostname.endswith(f".{domain}"):
            return labels
    return set()


def validation_errors(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"bio file does not exist: {path}"]
    if not path.is_file():
        return [f"bio path is not a file: {path}"]
    if path.name != "bio.html":
        errors.append("designer profile biography should be named bio.html")

    html = path.read_text(encoding="utf-8")
    parser = BioParser()
    parser.feed(html)
    text = plain_text(html)
    character_count = len(text)
    word_count = len(re.findall(r"\b[\w'-]+\b", text))
    full_document_tags = {"html", "head", "body", "doctype"}

    if parser.paragraph_count == 0:
        errors.append("bio.html should use paragraph tags")
    if any(tag in full_document_tags for tag in parser.tags) or "<!doctype" in html.lower():
        errors.append("bio.html should be an HTML snippet, not a complete HTML document")
    if FIRST_PERSON_PRONOUN_RE.search(text):
        errors.append("bio text should be written in third person, not first person")
    if not (MIN_CHARS < character_count < MAX_CHARS):
        errors.append(
            f"bio text should be more than {MIN_CHARS} and less than {MAX_CHARS} characters, got {character_count}"
        )
    if not (MIN_LINKS <= parser.link_count <= MAX_LINKS):
        errors.append(f"bio should include one or two links, got {parser.link_count}")
    for index, link in enumerate(parser.links, start=1):
        href = link["href"].strip()
        target = link["target"].strip().lower()
        label = " ".join(link["text"].split())
        if not re.fullmatch(r"https?://[^\s\"<>]+", href):
            errors.append(f"bio link {index} should have an http(s) href")
        if any(marker.lower() in href.lower() for marker in PLACEHOLDER_MARKERS):
            errors.append(f"bio link {index} should not use a placeholder URL")
        if target != "_blank":
            errors.append(f"bio link {index} should use target=\"_blank\"")
        if not label:
            errors.append(f"bio link {index} should have visible link text")
        elif any(marker.lower() in label.lower() for marker in PLACEHOLDER_MARKERS):
            errors.append(f"bio link {index} should not use placeholder link text")
        elif label.lower().startswith(("http://", "https://")):
            errors.append(f"bio link {index} label should omit the URL protocol")
        social_labels = social_labels_for_href(href)
        if social_labels and label not in social_labels:
            expected = " or ".join(sorted(social_labels))
            errors.append(f"bio link {index} social link label should be {expected}")
    if word_count < 50 or word_count > 160:
        errors.append(f"bio should be around 100 words, got {word_count}")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_designer_profile_bio.py path/to/bio.html")
        return 2
    path = Path(argv[1])
    errors = validation_errors(path)
    print("# Designer Profile Bio Check")
    print()
    print(f"Bio: {path}")
    print(f"Ready: {'no' if errors else 'yes'}")
    if errors:
        print()
        print("Blocking findings:")
        for error in errors:
            print(f"- {error}")
        return 2

    text = plain_text(path.read_text(encoding="utf-8"))
    word_count = len(re.findall(r"\b[\w'-]+\b", text))
    parser = BioParser()
    parser.feed(path.read_text(encoding="utf-8"))
    print(f"Characters: {len(text)}")
    print(f"Words: {word_count}")
    print(f"Links: {parser.link_count}")
    print(f"Paragraphs: {parser.paragraph_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
