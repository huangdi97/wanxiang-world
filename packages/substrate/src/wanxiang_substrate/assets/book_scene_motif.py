"""Generic zero-cost scene morphology for deterministic T0 visuals."""

# pyright: reportUnusedFunction=false

from __future__ import annotations


_MOTIF_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("bridge", ("桥", "bridge", "crossing", "viaduct")),
    ("harbor", ("港", "码头", "渡口", "harbor", "port", "dock", "pier", "wharf")),
    ("garden", ("园", "庭", "苑", "garden", "park", "courtyard")),
    ("mountain", ("山", "谷", "岭", "峰", "崖", "mountain", "valley", "cliff", "canyon")),
    ("interior", ("书房", "室", "厅", "堂", "library", "study", "room", "hall")),
    ("pavilion", ("亭", "阁", "塔", "pavilion", "pagoda", "tower")),
    ("city", ("城", "门", "关", "堡", "寨", "city", "gate", "fortress", "castle")),
    ("water", ("河", "湖", "溪", "海", "湾", "river", "lake", "stream", "sea", "bay")),
)


def _scene_motif(place_name: str) -> str:
    normalized = place_name.casefold()
    for motif, keywords in _MOTIF_KEYWORDS:
        if any(keyword.casefold() in normalized for keyword in keywords):
            return motif
    return "settlement"


def _motif_uses_water(motif: str) -> bool:
    return motif in {"bridge", "harbor", "water"}


def _motif_svg(motif: str, *, accent_hue: int, ground_hue: int, anchor_x: int) -> str:
    """Return an illustrative foreground; motif is projection, never world truth."""
    dark = f"hsl({accent_hue + 18} 21% 28%)"
    pale = f"hsl({accent_hue} 28% 78%)"
    ground = f"hsl({ground_hue + 6} 28% 31%)"

    if motif == "bridge":
        return (
            f'<g data-motif="bridge" fill="none" stroke="{dark}">'
            '<path d="M145 640 Q600 335 1055 640" stroke-width="34"/>'
            '<path d="M145 642 H1055" stroke-width="12"/>'
            '<path d="M235 588 V696 M430 458 V686 M770 458 V686 M965 588 V696" '
            'stroke-width="12"/></g>'
        )
    if motif == "harbor":
        return (
            f'<g data-motif="harbor" fill="{pale}" stroke="{dark}" stroke-width="9">'
            '<path d="M120 640 H790 L850 700 H80Z"/>'
            '<path d="M840 690 l120 -32 105 45 -133 28Z"/>'
            '<path d="M915 655 V430 M1005 683 V500" fill="none"/>'
            '<path d="M915 445 L1010 560 H915Z" opacity=".72"/></g>'
        )
    if motif == "garden":
        return (
            f'<g data-motif="garden"><ellipse cx="620" cy="690" rx="255" ry="78" '
            'fill="hsl(194 38% 46%)" opacity=".72"/>'
            f'<g fill="{ground}"><circle cx="230" cy="560" r="86"/>'
            '<circle cx="330" cy="525" r="64"/><circle cx="920" cy="545" r="82"/>'
            '<circle cx="1010" cy="575" r="58"/></g>'
            f'<path d="M120 760 Q430 600 1080 735" fill="none" stroke="{pale}" '
            'stroke-width="32"/></g>'
        )
    if motif == "mountain":
        return (
            f'<g data-motif="mountain" fill="{ground}" stroke="{dark}" stroke-width="7">'
            '<path d="M40 720 L310 330 L515 720Z"/>'
            '<path d="M330 720 L700 245 L1010 720Z"/>'
            '<path d="M760 720 L1010 410 L1190 720Z"/></g>'
            f'<path d="M90 790 Q420 630 650 720 T1120 625" fill="none" '
            f'stroke="{pale}" stroke-width="25"/>'
        )
    if motif == "interior":
        return (
            f'<g data-motif="interior" stroke="{dark}" stroke-width="8">'
            f'<path d="M150 250 H1050 V735 H150Z" fill="{pale}" opacity=".74"/>'
            '<path d="M150 250 L355 390 H845 L1050 250 M355 390 V735 M845 390 V735" '
            'fill="none"/>'
            '<path d="M205 475 H330 M205 535 H330 M870 475 H995 M870 535 H995" '
            'fill="none" stroke-width="16"/></g>'
        )
    if motif == "pavilion":
        return (
            f'<g data-motif="pavilion" fill="{pale}" stroke="{dark}" stroke-width="9">'
            '<path d="M350 475 H850 V700 H350Z"/>'
            '<path d="M275 480 L600 300 L925 480 L820 505 H380Z" fill="none" '
            'stroke-width="28"/>'
            '<path d="M420 490 V700 M560 490 V700 M700 490 V700 M800 490 V700" '
            'fill="none"/></g>'
        )
    if motif == "city":
        return (
            f'<g data-motif="city" fill="{pale}" stroke="{dark}" stroke-width="9">'
            '<path d="M125 475 H1075 V720 H125Z"/>'
            '<rect x="185" y="385" width="155" height="335"/>'
            '<rect x="860" y="385" width="155" height="335"/>'
            '<path d="M500 720 V575 Q600 480 700 575 V720Z" fill="#102b35"/></g>'
        )
    if motif == "water":
        return (
            '<g data-motif="water">'
            '<path d="M0 620 C280 550 520 720 1200 590 V900 H0Z" '
            'fill="hsl(194 42% 37%)" opacity=".82"/>'
            f'<path d="M380 660 Q600 590 820 660 Q600 735 380 660Z" fill="{pale}" '
            f'stroke="{dark}" stroke-width="8"/></g>'
        )
    return (
        f'<g data-motif="settlement" fill="{pale}" stroke="{dark}" stroke-width="8">'
        f'<rect x="{anchor_x}" y="450" width="210" height="190" rx="5"/>'
        f'<rect x="{anchor_x + 300}" y="515" width="155" height="125" rx="5"/>'
        f'<rect x="{max(55, anchor_x - 245)}" y="530" width="145" height="110" rx="5"/>'
        f'<path d="M{anchor_x - 20} 455 L{anchor_x + 105} 375 '
        f'L{anchor_x + 230} 455Z" fill="{dark}"/></g>'
    )
