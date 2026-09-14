"""Refresh publication venue badges from ORCID and accepted-paper metadata."""

from __future__ import annotations

import html
import json
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ACCEPTED_DATA = ROOT / "data" / "accepted_publications.json"
ORCID_ID = "0009-0006-1956-8159"
ORCID_WORKS_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
SCHOLAR_URL = "https://scholar.google.com/citations?user=PGwRExQAAAAJ&hl=en"

VENUE_START = "<!-- PUBLICATION-VENUES:START -->"
VENUE_END = "<!-- PUBLICATION-VENUES:END -->"
ACCEPTED_START = "<!-- ACCEPTED-PUBLICATIONS:START -->"
ACCEPTED_END = "<!-- ACCEPTED-PUBLICATIONS:END -->"

COLORS = {
    "transportation research": "E76F00",
    "scientific reports": "24292F",
    "results in engineering": "F26B21",
    "ieee access": "00629B",
    "archives of computational": "176B45",
    "journal of public transportation": "005A8D",
    "frontiers": "E84A5F",
    "energy conversion": "009B77",
    "energy engineering": "D35400",
    "future transportation": "2A9D8F",
    "discover": "6F42C1",
    "computers, materials": "B23A48",
    "transformative technologies": "8A4FFF",
}


def replace_block(text: str, start: str, end: str, content: str) -> str:
    """Replace content between a unique pair of README markers."""
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"Expected exactly one marker pair: {start} / {end}")
    before, remainder = text.split(start, 1)
    _, after = remainder.split(end, 1)
    return f"{before}{start}\n{content.rstrip()}\n{end}{after}"


def venue_color(name: str) -> str:
    lowered = name.casefold()
    return next((color for key, color in COLORS.items() if key in lowered), "087F8C")


def badge(label: str, venue: str, color: str, link: str) -> str:
    query = urllib.parse.urlencode(
        {"label": label, "message": venue, "color": color, "style": "flat-square"}
    )
    image = f"https://img.shields.io/static/v1?{query}"
    return f'<a href="{link}"><img src="{image}" alt="{label}: {html.escape(venue)}"></a>'


def orcid_journals() -> Counter[str]:
    request = urllib.request.Request(
        ORCID_WORKS_URL,
        headers={
            "Accept": "application/json",
            "User-Agent": "mahbubchula-github-profile/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        record = json.load(response)

    journals: list[str] = []
    for group in record.get("group", []):
        summaries = group.get("work-summary") or []
        if not summaries:
            continue
        work = summaries[0]
        if work.get("type") != "journal-article":
            continue
        raw_title = (work.get("journal-title") or {}).get("value") or ""
        title = html.unescape(raw_title).strip()
        if title:
            journals.append(title)
    if not journals:
        raise RuntimeError("No journal articles were returned by the public ORCID record")
    return Counter(journals)


def load_accepted() -> list[dict[str, object]]:
    records = json.loads(ACCEPTED_DATA.read_text())
    required = {"authors", "year", "title", "journal", "doi"}
    for index, record in enumerate(records, start=1):
        missing = required - record.keys()
        if missing:
            raise ValueError(f"Accepted record {index} is missing: {sorted(missing)}")
    return records


def render_venues(published: Counter[str], accepted: list[dict[str, object]]) -> str:
    published_badges = [
        badge("Published", venue, venue_color(venue), SCHOLAR_URL)
        for venue, _ in sorted(published.items(), key=lambda item: (-item[1], item[0].casefold()))
    ]
    accepted_venues = list(dict.fromkeys(str(item["journal"]) for item in accepted))
    accepted_badges = [
        badge("Accepted", venue, venue_color(venue), SCHOLAR_URL) for venue in accepted_venues
    ]
    return "\n".join(
        [
            '<p align="center"><b>Published in</b></p>',
            '<p align="center">',
            "\n".join(published_badges),
            "</p>",
            '<p align="center"><b>Recently accepted in</b></p>',
            '<p align="center">',
            "\n".join(accepted_badges),
            "</p>",
            (
                '<p align="center"><sub>Published venues refresh weekly from '
                f'<a href="https://orcid.org/{ORCID_ID}">ORCID</a>; accepted venues '
                "are generated from the repository's structured publication feed.</sub></p>"
            ),
        ]
    )


def render_accepted(records: list[dict[str, object]]) -> str:
    lines = []
    for index, item in enumerate(records, start=1):
        doi = str(item["doi"]).strip()
        link = f" [DOI](https://doi.org/{doi})" if doi else ""
        lines.append(
            f'{index}. {item["authors"]} ({item["year"]}). '
            f'*{item["title"]}*. **{item["journal"]}**. '
            f"Accepted for publication.{link}"
        )
    return "\n".join(lines)


def main() -> None:
    accepted = load_accepted()
    published = orcid_journals()
    text = README.read_text()
    text = replace_block(text, VENUE_START, VENUE_END, render_venues(published, accepted))
    text = replace_block(text, ACCEPTED_START, ACCEPTED_END, render_accepted(accepted))
    README.write_text(text)
    print(
        f"Updated {len(published)} published journal venues and "
        f"{len({str(item['journal']) for item in accepted})} accepted venues."
    )


if __name__ == "__main__":
    main()
