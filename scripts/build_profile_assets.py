"""Generate the animated SVG artwork used by the profile README.

Every visual is produced in a dark and a light variant so the README can pick
the one that matches the reader's GitHub theme through a <picture> element.
The impact strip reads its publication counts from the README and the accepted
publication feed, so it stays in step with the weekly ORCID refresh.
"""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
README = ROOT / "README.md"
ACCEPTED_DATA = ROOT / "data" / "accepted_publications.json"

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": {
        "bg_start": "#06121D",
        "bg_mid": "#0A2638",
        "bg_end": "#0B4F5A",
        "grid": "#DDF7F4",
        "grid_opacity": "0.04",
        "title": "#FFFFFF",
        "text": "#D5E7EA",
        "muted": "#93B4BA",
        "accent": "#54D2D8",
        "accent_2": "#78E0B8",
        "gold": "#F3C969",
        "road": "#D6F5F1",
        "road_opacity": "0.10",
        "card": "#0E2B3D",
        "card_stroke": "#2C6474",
        "chip": "#E9FBF8",
        "chip_opacity": "0.08",
        "shadow": "#01070C",
    },
    "light": {
        "bg_start": "#F7FBFC",
        "bg_mid": "#EAF5F6",
        "bg_end": "#D4EEEC",
        "grid": "#0B3B4A",
        "grid_opacity": "0.05",
        "title": "#0B2233",
        "text": "#22414F",
        "muted": "#547985",
        "accent": "#0A8E97",
        "accent_2": "#1BA37A",
        "gold": "#C98A0B",
        "road": "#0B3B4A",
        "road_opacity": "0.08",
        "card": "#FFFFFF",
        "card_stroke": "#BFDDE0",
        "chip": "#0A8E97",
        "chip_opacity": "0.08",
        "shadow": "#0B3B4A",
    },
}

FOCUS_AREAS = [
    "Road Safety & Crash Severity",
    "Driver Behaviour",
    "Intelligent Transportation Systems",
    "Explainable AI",
    "LLMs for Transportation",
    "Sustainable Mobility",
]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def svg_open(width: int, height: int, title: str, desc: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
        f'  <title id="title">{esc(title)}</title>\n'
        f'  <desc id="desc">{esc(desc)}</desc>\n'
    )


def background_defs(t: dict[str, str], width: int, height: int) -> str:
    return f"""    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg_start']}"/>
      <stop offset="0.6" stop-color="{t['bg_mid']}"/>
      <stop offset="1" stop-color="{t['bg_end']}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['accent']}"/>
      <stop offset="1" stop-color="{t['accent_2']}"/>
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{t['grid']}" stroke-width="0.7" stroke-opacity="{t['grid_opacity']}"/>
    </pattern>
    <clipPath id="frame">
      <rect width="{width}" height="{height}" rx="20"/>
    </clipPath>
"""


# --------------------------------------------------------------------------- hero


def build_hero(t: dict[str, str]) -> str:
    width, height = 1200, 340
    roads = [
        "M700 380C770 300 800 215 880 150C950 92 1040 70 1110 -10",
        "M760 250C860 262 960 236 1030 170C1080 122 1130 100 1230 98",
        "M820 330C920 312 1010 290 1080 240C1120 212 1165 200 1230 204",
    ]
    vehicles = [
        (0, "7s", "0s", t["gold"]),
        (0, "7s", "3.5s", t["accent"]),
        (1, "9s", "1s", t["accent_2"]),
        (1, "9s", "5.5s", t["gold"]),
        (2, "11s", "2s", t["accent"]),
    ]
    nodes = [(880, 150, 0), (1030, 170, 0.8), (1080, 240, 1.6), (958, 98, 2.4), (1160, 100, 3.2)]

    road_paths = "\n".join(
        f'      <path id="road{i}" d="{d}" stroke="{t["road"]}" stroke-opacity="{t["road_opacity"]}" stroke-width="{38 - i * 8}"/>'
        for i, d in enumerate(roads)
    )
    lane_marks = "\n".join(
        f'      <path d="{d}" stroke="{t["gold"] if i == 0 else t["accent"]}" stroke-opacity="{0.7 if i == 0 else 0.35}" '
        f'stroke-width="1.6" stroke-dasharray="10 12">'
        f'<animate attributeName="stroke-dashoffset" from="0" to="-44" dur="{1.6 + i * 0.6:.1f}s" repeatCount="indefinite"/></path>'
        for i, d in enumerate(roads)
    )
    cars = "\n".join(
        f"""    <g>
      <rect x="-9" y="-4.5" width="18" height="9" rx="3.5" fill="{color}"/>
      <rect x="3" y="-3" width="4" height="6" rx="1.5" fill="{t['bg_start']}" fill-opacity="0.55"/>
      <animateMotion dur="{dur}" begin="{begin}" repeatCount="indefinite" rotate="auto">
        <mpath href="#road{road}"/>
      </animateMotion>
    </g>"""
        for road, dur, begin, color in vehicles
    )
    pulses = "\n".join(
        f"""    <circle cx="{x}" cy="{y}" r="4.5" fill="{t['accent']}"/>
    <circle cx="{x}" cy="{y}" r="6" fill="none" stroke="{t['accent']}" stroke-width="1.5">
      <animate attributeName="r" values="6;22" dur="3.2s" begin="{delay}s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.7;0" dur="3.2s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>"""
        for x, y, delay in nodes
    )

    # Rotating focus area: each phrase owns an equal slice of the cycle.
    cycle = 3.0 * len(FOCUS_AREAS)
    rotating = []
    for index, phrase in enumerate(FOCUS_AREAS):
        start = index / len(FOCUS_AREAS)
        end = (index + 1) / len(FOCUS_AREAS)
        fade = 0.25 / cycle
        key_times = [0, start, start + fade, end - fade, end, 1]
        values = [0, 0, 1, 1, 0, 0]
        if index == 0:
            key_times, values = [0, fade, end - fade, end, 1], [0, 1, 1, 0, 0]
        rotating.append(
            f'      <text x="0" y="0" opacity="0">{esc(phrase)}'
            f'<animate attributeName="opacity" dur="{cycle:.0f}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in key_times)}" values="{";".join(map(str, values))}"/></text>'
        )
    rotating_text = "\n".join(rotating)

    chips = []
    x = 0
    for index, label in enumerate(["M.Eng. Researcher", "IEEE Graduate Student Member", "Founder, B'Deshi Research Lab"]):
        chip_w = round(len(label) * 7.6) + 44
        chips.append(
            f"""      <g transform="translate({x} 0)">
        <rect width="{chip_w}" height="32" rx="16" fill="{t['chip']}" fill-opacity="{t['chip_opacity']}" stroke="{t['accent']}" stroke-opacity="0.45"/>
        <circle cx="17" cy="16" r="4" fill="{t['gold'] if index == 0 else t['accent']}"/>
        <text x="30" y="21" font-size="14" font-weight="600" fill="{t['text']}">{esc(label)}</text>
      </g>"""
        )
        x += chip_w + 14
    chip_svg = "\n".join(chips)

    return (
        svg_open(
            width,
            height,
            "Mahbub Hassan — Transportation Engineering Researcher",
            "Animated banner: Mahbub Hassan, transportation engineering researcher at Chulalongkorn University, "
            "working on road safety, driver behaviour, intelligent transportation systems, explainable AI, "
            "LLMs for transportation and sustainable mobility.",
        )
        + f"""  <defs>
{background_defs(t, width, height)}    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{width}" height="{height}" fill="url(#bg)"/>
    <rect width="{width}" height="{height}" fill="url(#grid)"/>
    <ellipse cx="1010" cy="170" rx="330" ry="260" fill="url(#glow)">
      <animate attributeName="rx" values="320;350;320" dur="8s" repeatCount="indefinite"/>
    </ellipse>
    <rect width="{width}" height="4" fill="url(#accent)"/>
    <g fill="none" stroke-linecap="round">
{road_paths}
{lane_marks}
    </g>
{pulses}
{cars}
    <g transform="translate(68 62)" font-family="{FONT}">
      <text x="0" y="0" font-size="14" font-weight="700" letter-spacing="3" fill="{t['accent']}">TRANSPORTATION ENGINEERING · CHULALONGKORN UNIVERSITY</text>
      <text x="-3" y="72" font-size="62" font-weight="800" letter-spacing="-1.5" fill="{t['title']}">Mahbub Hassan</text>
      <rect x="0" y="92" width="76" height="4" rx="2" fill="url(#accent)">
        <animate attributeName="width" values="0;76" dur="1.2s" fill="freeze"/>
      </rect>
      <text x="0" y="132" font-size="20" font-weight="500" fill="{t['text']}">Data-driven research for safer, smarter and greener mobility</text>
      <g transform="translate(0 172)" font-size="20" font-weight="700" fill="{t['gold']}">
        <text x="0" y="0" font-size="15" font-weight="600" letter-spacing="1.5" fill="{t['muted']}">FOCUS</text>
        <rect x="62" y="-15" width="2" height="20" fill="{t['muted']}" opacity="0.6"/>
        <g transform="translate(80 0)">
{rotating_text}
        </g>
      </g>
      <g transform="translate(0 208)">
{chip_svg}
      </g>
    </g>
    <g transform="translate(905 312)" font-family="{FONT}" font-size="11" font-weight="700" letter-spacing="2">
      <text x="0" y="0" fill="{t['muted']}">DATA</text>
      <path d="M42 -4h24M62 -7l4 3-4 3" fill="none" stroke="{t['accent']}" stroke-width="1.5"/>
      <text x="76" y="0" fill="{t['muted']}">EVIDENCE</text>
      <path d="M148 -4h24M168 -7l4 3-4 3" fill="none" stroke="{t['accent']}" stroke-width="1.5"/>
      <text x="182" y="0" fill="{t['gold']}">IMPACT</text>
    </g>
  </g>
</svg>
"""
    )


# --------------------------------------------------------------------- impact strip


def publication_counts() -> tuple[int, int]:
    """Return (published venues, accepted articles) from the generated profile data."""
    readme = README.read_text()
    published = readme.count("label=Published&")
    accepted = len(json.loads(ACCEPTED_DATA.read_text()))
    return published, accepted


def build_impact(t: dict[str, str]) -> str:
    published, accepted = publication_counts()
    metrics = [
        ("190,910", "road crashes analysed", "South Australia, 2012–2024"),
        (str(published), "journal venues", "peer-reviewed publications"),
        (str(accepted), "articles accepted", "forthcoming publications"),
        ("31", "manuscripts reviewed", "for 21 journals"),
        ("20+", "researchers mentored", "B'Deshi Research Lab"),
        ("100K+", "YouTube views", "open research education"),
    ]
    width, height = 1200, 150
    card_w, gap = 186, 14
    offset = (width - (card_w * len(metrics) + gap * (len(metrics) - 1))) / 2
    cards = []
    for index, (value, label, note) in enumerate(metrics):
        x = offset + index * (card_w + gap)
        begin = f"{index * 0.15:.2f}s"
        accent = t["gold"] if index == 0 else t["accent"]
        cards.append(
            f"""  <g transform="translate({x:.0f} 14)" opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="{begin}" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="{x:.0f} 30" to="{x:.0f} 14" dur="0.6s" begin="{begin}" fill="freeze"/>
    <rect width="{card_w}" height="122" rx="16" fill="{t['card']}" stroke="{t['card_stroke']}"/>
    <rect x="20" y="0" width="40" height="3" rx="1.5" fill="{accent}"/>
    <text x="20" y="54" font-size="34" font-weight="800" letter-spacing="-0.5" fill="{t['title']}">{esc(value)}</text>
    <text x="20" y="80" font-size="14" font-weight="700" fill="{accent}">{esc(label)}</text>
    <text x="20" y="102" font-size="12" font-weight="500" fill="{t['muted']}">{esc(note)}</text>
  </g>"""
        )
    return (
        svg_open(
            width,
            height,
            "Research impact at a glance",
            "; ".join(f"{v} {l} ({n})" for v, l, n in metrics),
        )
        + f'<g font-family="{FONT}">\n'
        + "\n".join(cards)
        + "\n</g>\n</svg>\n"
    )


# ------------------------------------------------------------------- research map


def build_research_map(t: dict[str, str]) -> str:
    width, height = 1200, 430
    columns = [
        (
            "QUESTIONS",
            70,
            [
                "Road safety & crash severity",
                "Driver behaviour & psychology",
                "Travel behaviour & MaaS",
                "Intelligent transportation",
                "Sustainable mobility",
            ],
        ),
        (
            "METHODS",
            470,
            [
                "Explainable ML (SHAP, LIME)",
                "Statistics & PLS-SEM",
                "Traffic simulation (SUMO)",
                "Edge AI & TinyML",
                "LLMs & bibliometrics",
            ],
        ),
        (
            "OUTCOMES",
            870,
            [
                "Policy-relevant evidence",
                "Open research software",
                "Open education",
            ],
        ),
    ]
    links = [
        # (from column, from row, to column, to row)
        (0, 0, 1, 0), (0, 0, 1, 1), (0, 1, 1, 1), (0, 2, 1, 0), (0, 2, 1, 1),
        (0, 3, 1, 2), (0, 3, 1, 3), (0, 3, 1, 4), (0, 4, 1, 2), (0, 4, 1, 4),
        (1, 0, 2, 0), (1, 1, 2, 0), (1, 2, 2, 1), (1, 3, 2, 1), (1, 4, 2, 2),
        (1, 0, 2, 2), (1, 4, 2, 0),
    ]
    node_w, node_h, top = 260, 48, 84

    def row_y(column: int, row: int) -> float:
        count = len(columns[column][2])
        span = 5 * node_h + 4 * 20
        step = (span - node_h) / max(count - 1, 1)
        return top + row * step

    paths = []
    for index, (c1, r1, c2, r2) in enumerate(links):
        x1 = columns[c1][1] + node_w
        y1 = row_y(c1, r1) + node_h / 2
        x2 = columns[c2][1]
        y2 = row_y(c2, r2) + node_h / 2
        mid = (x1 + x2) / 2
        paths.append(
            f'  <path d="M{x1} {y1:.0f}C{mid} {y1:.0f} {mid} {y2:.0f} {x2} {y2:.0f}" fill="none" '
            f'stroke="{t["accent"]}" stroke-opacity="0.45" stroke-width="1.4" stroke-dasharray="4 6">'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-40" dur="{2 + (index % 4) * 0.4:.1f}s" '
            f'repeatCount="indefinite"/></path>'
        )

    nodes = []
    for col_index, (heading, x, items) in enumerate(columns):
        accent = [t["accent"], t["accent_2"], t["gold"]][col_index]
        nodes.append(
            f'  <text x="{x}" y="58" font-size="13" font-weight="800" letter-spacing="2.5" fill="{accent}">{heading}</text>'
        )
        for row, label in enumerate(items):
            y = row_y(col_index, row)
            begin = f"{col_index * 0.35 + row * 0.08:.2f}s"
            nodes.append(
                f"""  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{begin}" fill="freeze"/>
    <rect x="{x}" y="{y:.0f}" width="{node_w}" height="{node_h}" rx="12" fill="{t['card']}" stroke="{t['card_stroke']}"/>
    <rect x="{x}" y="{y + 12:.0f}" width="4" height="{node_h - 24}" rx="2" fill="{accent}"/>
    <text x="{x + 20}" y="{y + 30:.0f}" font-size="15" font-weight="600" fill="{t['title']}">{esc(label)}</text>
    <circle cx="{x + node_w}" cy="{y + node_h / 2:.0f}" r="3.5" fill="{accent}" opacity="{0 if col_index == 2 else 1}"/>
    <circle cx="{x}" cy="{y + node_h / 2:.0f}" r="3.5" fill="{accent}" opacity="{0 if col_index == 0 else 1}"/>
  </g>"""
            )

    return (
        svg_open(
            width,
            height,
            "Research map",
            "How research questions in road safety, driver behaviour, travel behaviour, intelligent "
            "transportation and sustainable mobility connect to methods (explainable ML, statistics and "
            "PLS-SEM, traffic simulation, edge AI, LLMs) and to outcomes (policy evidence, open software, "
            "open education).",
        )
        + f"""  <defs>
{background_defs(t, width, height)}  </defs>
  <g clip-path="url(#frame)" font-family="{FONT}">
    <rect width="{width}" height="{height}" fill="url(#bg)"/>
    <rect width="{width}" height="{height}" fill="url(#grid)"/>
    <rect width="{width}" height="4" fill="url(#accent)"/>
{chr(10).join(paths)}
{chr(10).join(nodes)}
  </g>
</svg>
"""
    )


# ------------------------------------------------------------------------- footer


def build_footer(t: dict[str, str]) -> str:
    width, height = 1200, 90
    return (
        svg_open(
            width,
            height,
            "Thanks for visiting",
            "Animated road with vehicles travelling across, closing the profile.",
        )
        + f"""  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['road']}" stop-opacity="0"/>
      <stop offset="0.15" stop-color="{t['road']}" stop-opacity="{t['road_opacity']}"/>
      <stop offset="0.85" stop-color="{t['road']}" stop-opacity="{t['road_opacity']}"/>
      <stop offset="1" stop-color="{t['road']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="34" width="{width}" height="34" fill="url(#fade)"/>
  <path d="M60 51H1140" stroke="{t['gold']}" stroke-opacity="0.7" stroke-width="2" stroke-dasharray="14 14">
    <animate attributeName="stroke-dashoffset" from="0" to="-56" dur="1.4s" repeatCount="indefinite"/>
  </path>
  <g>
    <rect x="-14" y="38" width="28" height="10" rx="4" fill="{t['accent']}"/>
    <animateMotion path="M-40 0H1240" dur="8s" repeatCount="indefinite"/>
  </g>
  <g>
    <rect x="-14" y="55" width="28" height="10" rx="4" fill="{t['gold']}"/>
    <animateMotion path="M1240 0H-40" dur="10s" repeatCount="indefinite"/>
  </g>
  <text x="600" y="22" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" letter-spacing="3" fill="{t['muted']}">SAFER ROADS · SMARTER MOBILITY · OPEN SCIENCE</text>
</svg>
"""
    )


BUILDERS = {
    "hero": build_hero,
    "impact": build_impact,
    "research-map": build_research_map,
    "footer": build_footer,
}


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for name, builder in BUILDERS.items():
        for theme_name, theme in THEMES.items():
            path = ASSETS / f"{name}-{theme_name}.svg"
            path.write_text(builder(theme))
    print(f"Generated {len(BUILDERS) * len(THEMES)} SVG assets in {ASSETS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
