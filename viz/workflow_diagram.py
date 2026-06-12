"""Generate a self-contained workflow diagram (SVG) for the Theme-to-Trade engine.

Renders the full pipeline — raw sources -> wiki memory -> Stage 0 ingestion ->
memory firewall -> Engines 1-4 -> PM gate -> Thesis Tracker sidecar — with the 15
method skills mapped to the phase where they fire. Output is a stand-alone SVG
(no external fonts/assets required) intended to be converted to a shareable PDF.

    python viz/workflow_diagram.py            # writes viz/workflow.svg
"""
from __future__ import annotations

from pathlib import Path

W = 1000
PAGE_PAD = 30
BOX_W = 760
BOX_X = (W - BOX_W) // 2
GAP = 46  # vertical gap between stacked boxes (room for the arrow)

# Palette: (fill, border, text) — light, print-friendly.
PAL = {
    "grey":   ("#EEF1F4", "#94A0AB", "#2B3138"),
    "blue":   ("#E7F0FB", "#3B82C4", "#15324F"),
    "amber":  ("#FFF4E0", "#E0A53A", "#5A4410"),
    "green":  ("#E8F5EC", "#3A9D5D", "#163E27"),
    "teal":   ("#E2F4F2", "#2FA39B", "#0E3F3B"),
    "purple": ("#EFE9FA", "#7C5CC4", "#2E2153"),
    "red":    ("#FBE9E9", "#C0392B", "#5A1812"),
    "slate":  ("#EAEEF2", "#5B6B7B", "#22303C"),
}

FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"

# ── pipeline definition ──────────────────────────────────────────────────────
# kind: "box" | "band". detail = pre-wrapped lines. skills = chip labels.
STAGES = [
    dict(kind="box", color="grey", title="RAW SOURCES  (immutable)",
         detail=["markdowns/ · research books · papers — never modified"], skills=[]),
    dict(kind="box", color="grey", title="WIKI MEMORY",
         detail=["method pages (how to reason)  ·  case pages (past themes/outcomes)"],
         skills=[]),
    dict(kind="box", color="blue", title="STAGE 0 — INGESTION",
         detail=["Observation (facts) · CandidateTheme (narratives) · ConsensusSignal (attention)",
                 "nominate themes RANKED BY divergence(evidence, attention) = pre-screen on (p − q)"],
         skills=["iceberg-classifier", "macro-state-parser", "macro-regime-classifier"]),
    dict(kind="band", color="amber", title="MEMORY FIREWALL",
         detail=["Phase A — fresh reasoning, METHOD pages only   ▶   FREEZE (SHA-256 snapshot)"
                 "   ▶   Phase B — CASE pages: analogue + calibration only"]),
    dict(kind="box", color="green", title="ENGINE 1 — Driver + Axis",
         detail=["Q1 theme · Q2 universe · Q3 operational axis (a named, computable series)"],
         skills=["causal-compiler", "system-mapper", "global-io-network",
                 "backdoor-identifiability-gate", "trap-detector"]),
    dict(kind="box", color="teal", title="ENGINE 2 — Scenario Pricing",
         detail=["Q4 normal FV · Q5 scenario FV = Σ pₛ Xₛ · Q6 priced-in q (max-entropy) · "
                 "Q7 edge = ⟨p − q, X⟩"],
         skills=["scenario-pricing-engine", "evidence-weighting",
                 "outcome-calibration-engine", "priced-in-estimator", "term-premium-estimator"]),
    dict(kind="box", color="purple", title="DISCOVERY OUTPUT",
         detail=["ranked strategy families + decomposed confidence",
                 "status: strategy_family_routed   ◀ DISCOVERY STOPS HERE (no legs / sizing / hedges)"],
         skills=["edge-validity", "factor-r2-router"]),
    dict(kind="band", color="grey", title="EXPRESSION MODE  (separate pass — only on request)",
         detail=["the discovery firewall does NOT produce expression_complete; the human re-enters"]),
    dict(kind="box", color="grey", title="ENGINE 3 — Expression Scoring",
         detail=["Q8 candidates · Q9 best = gated score ρ²·Ω·(1+a·cvx)·liq·e^(−g·crowd)/(1+cap)"],
         skills=[]),
    dict(kind="box", color="grey", title="ENGINE 4 — Sizer + Risk",
         detail=["Q10 size (Alaph grid) · Q11 stop (on the axis) · Q12 falsifiers (observable+threshold)"],
         skills=[]),
    dict(kind="box", color="red", title="PM GATE",
         detail=["Q13 open questions  →  STOP · hands control to the human (epistemic engine ends here)"],
         skills=[]),
]

SIDECAR = dict(color="slate", title="THESIS TRACKER  (SQLite sidecar — standalone)",
               detail=["one row per ticker · computes probability-weighted price + upside · audit log",
                       "seeded by create_thesis_stub_from_theme() — copies thesis/links/kill-criteria,",
                       "invents NO prices, probabilities, weights, or recommendations"],
               skills=[])

# ── tiny text-metric helpers (approximate; good enough for chip wrapping) ─────
def _chip_w(label: str, fs: float = 10.0) -> float:
    return len(label) * fs * 0.60 + 18


def _wrap_chips(skills, max_w):
    rows, cur, cur_w = [], [], 0.0
    for s in skills:
        w = _chip_w(s)
        if cur and cur_w + w + 8 > max_w:
            rows.append(cur)
            cur, cur_w = [], 0.0
        cur.append((s, w))
        cur_w += w + 8
    if cur:
        rows.append(cur)
    return rows


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── layout + render ──────────────────────────────────────────────────────────
def build_svg() -> str:
    parts: list[str] = []
    y = PAGE_PAD + 78  # below the title block

    def box_height(st) -> float:
        h = 30 + 18 * len(st["detail"])
        if st.get("skills"):
            h += 8 + 24 * len(_wrap_chips(st["skills"], BOX_W - 36))
        return h + 12

    centers: list[tuple] = []  # (y_top, y_bottom) of each box for arrows

    for st in STAGES:
        fill, border, text = PAL[st["color"]]
        if st["kind"] == "band":
            h = 26 + 18 * len(st["detail"])
            parts.append(
                f'<rect x="{BOX_X}" y="{y}" width="{BOX_W}" height="{h}" rx="8" '
                f'fill="{fill}" stroke="{border}" stroke-width="1.5" stroke-dasharray="7 4"/>'
            )
            parts.append(
                f'<text x="{W/2}" y="{y+18}" text-anchor="middle" font-family="{FONT}" '
                f'font-size="12.5" font-weight="700" fill="{text}">{_esc(st["title"])}</text>'
            )
            for i, line in enumerate(st["detail"]):
                parts.append(
                    f'<text x="{W/2}" y="{y+36+i*16}" text-anchor="middle" font-family="{FONT}" '
                    f'font-size="10.5" fill="{text}">{_esc(line)}</text>'
                )
            centers.append((y, y + h))
            y += h + GAP
            continue

        h = box_height(st)
        parts.append(
            f'<rect x="{BOX_X}" y="{y}" width="{BOX_W}" height="{h}" rx="10" '
            f'fill="{fill}" stroke="{border}" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{BOX_X+18}" y="{y+24}" font-family="{FONT}" font-size="15" '
            f'font-weight="700" fill="{text}">{_esc(st["title"])}</text>'
        )
        for i, line in enumerate(st["detail"]):
            parts.append(
                f'<text x="{BOX_X+18}" y="{y+44+i*18}" font-family="{FONT}" font-size="11" '
                f'fill="#3A424B">{_esc(line)}</text>'
            )
        # chips
        if st.get("skills"):
            cy = y + 44 + 18 * len(st["detail"]) + 6
            for row in _wrap_chips(st["skills"], BOX_W - 36):
                cx = BOX_X + 18
                for label, w in row:
                    parts.append(
                        f'<rect x="{cx}" y="{cy}" width="{w:.0f}" height="17" rx="8.5" '
                        f'fill="#FFFFFF" stroke="{border}" stroke-width="1"/>'
                    )
                    parts.append(
                        f'<text x="{cx+w/2:.0f}" y="{cy+12}" text-anchor="middle" '
                        f'font-family="{FONT}" font-size="9.5" fill="{text}">{_esc(label)}</text>'
                    )
                    cx += w + 8
                cy += 24
        centers.append((y, y + h))
        y += h + GAP

    # vertical arrows between consecutive stages
    arrows = []
    for (t1, b1), (t2, _b2) in zip(centers, centers[1:]):
        arrows.append(_arrow(W / 2, b1, W / 2, t2))

    # sidecar box (below PM gate), connected by a dashed arrow
    fill, border, text = PAL[SIDECAR["color"]]
    sc_y = y + 8
    sc_h = 30 + 18 * len(SIDECAR["detail"]) + 12
    arrows.append(_arrow(W / 2, centers[-1][1], W / 2, sc_y, dashed=True,
                         label="thesis stub"))
    parts.append(
        f'<rect x="{BOX_X}" y="{sc_y}" width="{BOX_W}" height="{sc_h}" rx="10" '
        f'fill="{fill}" stroke="{border}" stroke-width="2"/>'
    )
    parts.append(
        f'<text x="{BOX_X+18}" y="{sc_y+24}" font-family="{FONT}" font-size="15" '
        f'font-weight="700" fill="{text}">{_esc(SIDECAR["title"])}</text>'
    )
    for i, line in enumerate(SIDECAR["detail"]):
        parts.append(
            f'<text x="{BOX_X+18}" y="{sc_y+44+i*18}" font-family="{FONT}" font-size="11" '
            f'fill="#3A424B">{_esc(line)}</text>'
        )
    total_h = sc_y + sc_h + PAGE_PAD + 40  # +legend

    # title block
    head = [
        f'<rect x="0" y="0" width="{W}" height="{total_h}" fill="#FFFFFF"/>',
        f'<text x="{W/2}" y="{PAGE_PAD+18}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="24" font-weight="800" fill="#11181F">Theme-to-Trade Engine — Workflow</text>',
        f'<text x="{W/2}" y="{PAGE_PAD+44}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12.5" fill="#5A636C">A disciplined, falsifiable pipeline: research → causal '
        f'theme → priced-in edge → ranked strategy families → PM decision. '
        f'Chips = method skills (firewall-safe).</text>',
    ]

    # legend (bottom)
    ly = sc_y + sc_h + 22
    legend = [
        f'<text x="{BOX_X}" y="{ly}" font-family="{FONT}" font-size="10.5" fill="#5A636C">'
        f'Solid arrow = data/control flow   ·   Dashed = optional / sidecar   ·   '
        f'Dashed band = cross-cutting (firewall / mode switch)   ·   '
        f'15 method skills shown as chips at the phase they fire</text>',
    ]

    body = "\n".join(head + parts + arrows + legend)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h:.0f}" '
        f'viewBox="0 0 {W} {total_h:.0f}">\n{body}\n</svg>\n'
    )


def _arrow(x1, y1, x2, y2, dashed=False, label=None):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    line = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2-9}" stroke="#6B7280" '
            f'stroke-width="2"{dash}/>')
    tri = (f'<polygon points="{x2-6},{y2-9} {x2+6},{y2-9} {x2},{y2}" fill="#6B7280"/>')
    lab = ""
    if label:
        lab = (f'<text x="{x1+10}" y="{(y1+y2)/2+3}" font-family="{FONT}" font-size="9.5" '
               f'fill="#6B7280">{_esc(label)}</text>')
    return line + tri + lab


def main() -> None:
    out = Path(__file__).resolve().parent / "workflow.svg"
    out.write_text(build_svg())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
