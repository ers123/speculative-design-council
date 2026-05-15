#!/usr/bin/env python3
"""Class-wide Constellation — 학기말 통합 시각화 도구.

박은선 교수님 vision 응답:
  학생 작품에 대한 청중 반응을 Dator's Four Futures (성장/붕괴/지속/변혁)
  4 archetype 분포로 매핑하고, 14명 학생을 격자·polar 시각화로 통합.

사용:
    # 실제 학생 audience_report 폴더로
    python class_constellation.py --dir ./student_reports/ --out class_view.html

    # 데모 (synthetic 14명 = 2025 학생 narratype 기반)
    python class_constellation.py --demo --out class_demo.html

출력:
    class_view.html — 인터랙티브 히트맵 격자 + polar constellation (브라우저에서 열기)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# ═════════════════════════════════════════════════════════════════════
# 1. audience_report.md 에서 4 archetype 분포 파싱
# ═════════════════════════════════════════════════════════════════════

ARCHETYPES = ["성장", "붕괴", "지속", "변혁"]
ARCHETYPE_EN = {
    "성장": "Growth",
    "붕괴": "Collapse",
    "지속": "Discipline",
    "변혁": "Transformation",
}
ARCHETYPE_COLOR = {
    "성장": "#2d6a4f",   # green — continued growth
    "붕괴": "#9b2c2c",   # red — collapse
    "지속": "#8b6914",   # amber — discipline
    "변혁": "#5e548e",   # purple — transformation
}


def parse_distribution(md_text: str) -> dict[str, int] | None:
    """Extract {성장: 40, 붕괴: 30, ...} from audience_report.md text.

    Looks for patterns like:
        성장 ████████░░ 40%
        붕괴 ██████░░░░ 30%
    Returns None if no valid distribution found.
    """
    dist: dict[str, int] = {}
    for arc in ARCHETYPES:
        # Multiple patterns to be robust to LLM output variations
        patterns = [
            rf"{arc}\s+[█▓▒░\s]+(\d+)\s*%",      # bar + percent
            rf"{arc}\s*[:：]\s*(\d+)\s*%",        # 성장: 40%
            rf"{arc}\s*\(\s*(\d+)\s*%\)",         # 성장 (40%)
            rf"-\s*{arc}\s*[:：]?\s*(\d+)\s*%",   # - 성장: 40%
        ]
        for pat in patterns:
            m = re.search(pat, md_text)
            if m:
                try:
                    dist[arc] = int(m.group(1))
                    break
                except ValueError:
                    continue
    if len(dist) < 4:
        return None
    return dist


def extract_student_label(filename: str, md_text: str) -> str:
    """Try to extract a student/narratype label."""
    # First try a header line like "# 청중 반응 분석 보고서 — [세계명]" or "# narratype: [name]"
    m = re.search(r"^#\s+청중\s+반응[^—\-\n]*[—\-]\s*(.+?)$", md_text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r"^#\s+(.+?)$", md_text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Fall back to filename without extension
    name = Path(filename).stem
    # Strip common prefixes
    name = re.sub(r"^(audience_report_|학생_|2026_)", "", name)
    return name


def load_directory(path: str) -> list[dict]:
    """Load all .md files in directory and parse archetype distributions."""
    students = []
    for p in sorted(Path(path).glob("*.md")):
        text = p.read_text(encoding="utf-8")
        dist = parse_distribution(text)
        if dist is None:
            print(f"  [skip] {p.name} — 4 archetype 분포 파싱 실패", file=sys.stderr)
            continue
        label = extract_student_label(p.name, text)
        students.append({
            "label": label,
            "filename": p.name,
            "distribution": dist,
        })
    return students


# ═════════════════════════════════════════════════════════════════════
# 2. 데모 데이터 (2025 학생 14명 narratype 기반 synthetic 분포)
# ═════════════════════════════════════════════════════════════════════

DEMO_STUDENTS = [
    # (narratype명, 성장%, 붕괴%, 지속%, 변혁%) — 그럴듯한 분포
    ("김민주 — Neuphoria (행복 상품화)",        25, 45, 20, 10),
    ("김수민 — GUILTAMINE (휴식 죄책감)",       15, 25, 50, 10),
    ("김예진 — D.O.L. (운명/전통)",             20, 20, 45, 15),
    ("나예진 — 집단 갈등 (소수자 혐오)",        10, 55, 25, 10),
    ("박지우 — HAPPY GATE (감정 검열)",         40, 30, 20, 10),
    ("박혜준 — SelectON (이어버드 단절)",       30, 35, 25, 10),
    ("심영석 — SPLIT (기후 불평등)",            15, 50, 25, 10),
    ("오창도 — 꼰대 vs 젊은 세대",              20, 30, 40, 10),
    ("이연호 — MORDISH (그린워싱)",             25, 40, 25, 10),
    ("이예진 — COCOO (자녀 CCTV)",              45, 25, 25,  5),
    ("이효서 — EMOTONE (감정을 입다)",          40, 20, 25, 15),
    ("조가은 — NeuroLens (수면 사라진 사회)",   50, 30, 15,  5),
    ("조우용 — 신뢰 Point (신뢰 정량화)",       55, 20, 20,  5),
    ("지연우 — GELOTTO (유전자 복권)",          35, 30, 25, 10),
]


def demo_data() -> list[dict]:
    return [
        {
            "label": label,
            "filename": f"demo_{i+1}.md",
            "distribution": {"성장": g, "붕괴": c, "지속": d, "변혁": t},
        }
        for i, (label, g, c, d, t) in enumerate(DEMO_STUDENTS)
    ]


# ═════════════════════════════════════════════════════════════════════
# 3. HTML 렌더링
# ═════════════════════════════════════════════════════════════════════

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Constellation of 2045 — Class-wide Reception Map</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600;700&family=Noto+Sans+KR:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
:root {
  --ink: #1a1a1a;
  --ink-muted: #8a8a8a;
  --paper: #faf8f5;
  --paper-warm: #f5f0e8;
  --rule: #d4cfc4;
  --accent: #2c5f7c;
  --accent-deep: #1a3d52;
  --growth: #2d6a4f;
  --collapse: #9b2c2c;
  --discipline: #8b6914;
  --transformation: #5e548e;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 2rem 1.5rem;
  background: var(--paper);
  font-family: 'Noto Sans KR', sans-serif;
  color: var(--ink);
  line-height: 1.6;
}
.container { max-width: 1200px; margin: 0 auto; }
h1 {
  font-family: 'Noto Serif KR', serif;
  font-weight: 700;
  font-size: 1.9rem;
  border-bottom: 2px solid var(--ink);
  padding-bottom: 0.4rem;
  margin-top: 0;
}
.subtitle { color: var(--ink-muted); font-style: italic; font-size: 0.9rem; margin-bottom: 1.5rem; }
h2 {
  font-family: 'Noto Serif KR', serif;
  color: var(--accent-deep);
  font-size: 1.3rem;
  border-left: 4px solid var(--accent);
  padding-left: 0.8rem;
  margin-top: 2.5rem;
}
.legend { display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0; }
.legend-item {
  display: flex; align-items: center; gap: 0.4rem;
  font-size: 0.85rem; color: var(--ink);
}
.legend-swatch { width: 14px; height: 14px; border-radius: 2px; }

/* HEATMAP */
.heatmap {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0 2rem 0;
  font-size: 0.85rem;
  background: white;
}
.heatmap th, .heatmap td {
  padding: 0.6rem 0.8rem;
  border: 1px solid var(--rule);
  text-align: center;
}
.heatmap th {
  background: var(--accent-deep);
  color: white;
  font-weight: 600;
  letter-spacing: 0.04em;
}
.heatmap td.student-label {
  text-align: left;
  font-weight: 500;
  background: var(--paper-warm);
  white-space: nowrap;
  max-width: 320px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.cell { font-family: 'IBM Plex Mono', monospace; font-weight: 600; }

/* POLAR CONSTELLATION */
.polar-wrap {
  display: flex; gap: 2rem; flex-wrap: wrap; align-items: flex-start;
  margin: 1rem 0;
}
.polar-svg { background: white; border: 1px solid var(--rule); border-radius: 4px; }
.polar-list {
  flex: 1; min-width: 300px;
  font-size: 0.85rem;
}
.polar-list .row {
  display: flex; align-items: center; gap: 0.6rem;
  padding: 0.3rem 0;
  border-bottom: 1px dashed var(--rule);
}
.polar-list .swatch { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.polar-list .name { flex: 1; }

/* CLUSTER SUMMARY */
.cluster-section { margin-top: 2rem; }
.cluster-card {
  background: white;
  border-left: 4px solid var(--accent);
  padding: 0.8rem 1.2rem;
  margin: 0.6rem 0;
  border-radius: 4px;
}
.cluster-card h3 {
  font-family: 'Noto Serif KR', serif;
  margin: 0 0 0.4rem 0;
  font-size: 1.05rem;
  color: var(--accent-deep);
}
.cluster-card .members { font-size: 0.85rem; color: var(--ink-muted); }

footer {
  margin-top: 3rem; padding-top: 1rem;
  border-top: 1px solid var(--rule);
  color: var(--ink-muted); font-size: 0.8rem;
  text-align: center;
}
</style>
</head>
<body>
<div class="container">
  <h1>Constellation of 2045 — Class-wide Reception Map</h1>
  <div class="subtitle">
    학생 작품에 대한 청중(Nemotron-Personas-Korea 페르소나) 반응을
    Dator's Four Futures (성장 · 붕괴 · 지속 · 변혁)로 분류한 통합 시각화.
  </div>

  <div class="legend">
    <div class="legend-item"><div class="legend-swatch" style="background: var(--growth)"></div>성장 (Continued Growth)</div>
    <div class="legend-item"><div class="legend-swatch" style="background: var(--collapse)"></div>붕괴 (Collapse)</div>
    <div class="legend-item"><div class="legend-swatch" style="background: var(--discipline)"></div>지속 (Discipline)</div>
    <div class="legend-item"><div class="legend-swatch" style="background: var(--transformation)"></div>변혁 (Transformation)</div>
  </div>

  <h2>1. 격자 히트맵 — 학생 × Archetype</h2>
  <p style="font-size: 0.9rem; color: var(--ink-muted);">
    각 셀의 색 농도 = 해당 archetype 반응 비율. 행이 클러스터 되면 비슷한 미래 수용 패턴.
  </p>
  __HEATMAP__

  <h2>2. Polar Constellation — 4축 분포 visualization</h2>
  <p style="font-size: 0.9rem; color: var(--ink-muted);">
    각 학생 작품 = 4개 점 (4 archetype 각 축에서 % 길이만큼 떨어진 위치). 도형이 클수록 강한 반응, 한 축에 치우치면 single-archetype 작품.
  </p>
  <div class="polar-wrap">
    __POLAR_SVG__
    <div class="polar-list">__POLAR_LIST__</div>
  </div>

  <h2>3. 클러스터 — 비슷한 수용 패턴</h2>
  __CLUSTERS__

  <h2>4. 분포 통계</h2>
  __STATS__

  <footer>
    Yonsei University Speculative Design · 2026 · Generated by Speculative Design Council
  </footer>
</div>
</body>
</html>"""


def render_heatmap(students: list[dict]) -> str:
    """HTML table heatmap. Cell bg color intensity = % value."""
    rows = []
    rows.append("<table class='heatmap'>")
    rows.append("  <thead><tr><th>학생 / 작품</th>")
    for arc in ARCHETYPES:
        rows.append(f"    <th>{arc}<br><span style='font-weight:400;font-size:0.75rem;'>{ARCHETYPE_EN[arc]}</span></th>")
    rows.append("    <th>지배 archetype</th></tr></thead><tbody>")
    for s in students:
        dist = s["distribution"]
        dominant = max(dist, key=dist.get)
        rows.append(f"  <tr><td class='student-label'>{s['label']}</td>")
        for arc in ARCHETYPES:
            pct = dist[arc]
            color = ARCHETYPE_COLOR[arc]
            alpha = min(0.85, pct / 60.0)  # cap intensity
            text_color = "#fff" if alpha > 0.4 else "var(--ink)"
            rows.append(
                f"    <td class='cell' style='background: rgba({_hex_to_rgb(color)},{alpha:.2f}); color: {text_color};'>{pct}%</td>"
            )
        rows.append(f"    <td style='font-weight:600; color: {ARCHETYPE_COLOR[dominant]}'>{dominant}</td></tr>")
    rows.append("</tbody></table>")
    return "\n".join(rows)


def _hex_to_rgb(hexcolor: str) -> str:
    h = hexcolor.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r},{g},{b}"


def render_polar(students: list[dict]) -> tuple[str, str]:
    """SVG polar constellation: 4 axes, each student = a quadrilateral.

    Returns (svg_str, list_html_str).
    """
    # Canvas
    SIZE = 460
    CX = CY = SIZE // 2
    R = 160  # max radius for 100%

    svg = [f"<svg class='polar-svg' viewBox='0 0 {SIZE} {SIZE}' width='460' height='460'>"]
    # Background rings (25/50/75/100%)
    for r_pct in [25, 50, 75, 100]:
        r_val = R * (r_pct / 100)
        svg.append(f"  <circle cx='{CX}' cy='{CY}' r='{r_val}' fill='none' stroke='#e8e4db' stroke-dasharray='2,2'/>")
    # Axes (4 directions: 위=성장, 오=붕괴, 아래=지속, 왼=변혁)
    axis_dirs = {
        "성장": (0, -1),
        "붕괴": (1, 0),
        "지속": (0, 1),
        "변혁": (-1, 0),
    }
    for arc, (dx, dy) in axis_dirs.items():
        x2 = CX + dx * R
        y2 = CY + dy * R
        svg.append(f"  <line x1='{CX}' y1='{CY}' x2='{x2}' y2='{y2}' stroke='{ARCHETYPE_COLOR[arc]}' stroke-width='1.5'/>")
        # axis label
        lx = CX + dx * (R + 22)
        ly = CY + dy * (R + 22) + 4
        anchor = "middle"
        svg.append(f"  <text x='{lx}' y='{ly}' fill='{ARCHETYPE_COLOR[arc]}' font-size='13' font-weight='600' text-anchor='{anchor}' font-family='Noto Sans KR, sans-serif'>{arc}</text>")

    # Each student → 4 points → polygon
    list_rows = []
    for i, s in enumerate(students):
        dist = s["distribution"]
        # Color cycle for student lines
        student_color = f"hsl({(i * 360 // max(1, len(students)))}, 50%, 45%)"
        pts = []
        for arc, (dx, dy) in axis_dirs.items():
            r_val = R * (dist[arc] / 100)
            x = CX + dx * r_val
            y = CY + dy * r_val
            pts.append(f"{x:.1f},{y:.1f}")
        svg.append(
            f"  <polygon points='{' '.join(pts)}' fill='{student_color}' fill-opacity='0.08' stroke='{student_color}' stroke-width='1.5' stroke-opacity='0.7'>"
            f"<title>{s['label']}</title></polygon>"
        )
        # Small label dot at centroid (위쪽 약간)
        cx_off = CX
        cy_off = CY - 6 - i * 0  # could position labels but skip for clarity
        list_rows.append(
            f"<div class='row'><div class='swatch' style='background: {student_color}'></div>"
            f"<div class='name'>{s['label']}</div></div>"
        )

    svg.append("  <circle cx='{}' cy='{}' r='3' fill='#1a1a1a'/>".format(CX, CY))
    svg.append("</svg>")

    return "\n".join(svg), "\n".join(list_rows)


def cluster_by_dominant(students: list[dict]) -> str:
    """Group students by their dominant archetype."""
    clusters: dict[str, list[str]] = {a: [] for a in ARCHETYPES}
    for s in students:
        dominant = max(s["distribution"], key=s["distribution"].get)
        clusters[dominant].append(s["label"])
    parts = []
    descriptions = {
        "성장": "현재 트렌드를 더 강하게 — 미래가 지금의 확장으로 받아들여짐",
        "붕괴": "시스템 실패·위기 — 미래가 지금의 무너짐으로 받아들여짐",
        "지속": "규제·자제 — 미래가 지금의 통제 모드로 받아들여짐",
        "변혁": "도약·post-human — 미래가 지금을 넘어선 차원으로 받아들여짐",
    }
    for arc in ARCHETYPES:
        members = clusters[arc]
        if not members:
            members_html = "<em style='color: var(--ink-muted);'>해당 클러스터 없음</em>"
        else:
            members_html = " · ".join(members)
        parts.append(
            f"<div class='cluster-card' style='border-left-color: {ARCHETYPE_COLOR[arc]}'>"
            f"<h3>{arc} 클러스터 ({len(members)}명)</h3>"
            f"<div style='font-size: 0.85rem; color: var(--ink-muted); margin-bottom: 0.4rem;'>{descriptions[arc]}</div>"
            f"<div class='members'>{members_html}</div></div>"
        )
    return "\n".join(parts)


def render_stats(students: list[dict]) -> str:
    """Class-wide statistics."""
    if not students:
        return "<p>학생 데이터 없음.</p>"
    avg = {a: 0 for a in ARCHETYPES}
    for s in students:
        for a in ARCHETYPES:
            avg[a] += s["distribution"][a]
    for a in ARCHETYPES:
        avg[a] = round(avg[a] / len(students), 1)
    # Variability — std-dev as simple measure
    def std(arc):
        m = avg[arc]
        v = sum((s["distribution"][arc] - m) ** 2 for s in students) / len(students)
        return round(v ** 0.5, 1)

    rows = ["<table class='heatmap' style='max-width: 700px;'><thead>",
            "<tr><th>지표</th>" + "".join(f"<th>{a}</th>" for a in ARCHETYPES) + "</tr></thead><tbody>"]
    rows.append("<tr><td class='student-label'>클래스 평균 (%)</td>")
    for a in ARCHETYPES:
        rows.append(f"<td class='cell'>{avg[a]}</td>")
    rows.append("</tr><tr><td class='student-label'>편차 (σ)</td>")
    for a in ARCHETYPES:
        rows.append(f"<td class='cell'>{std(a)}</td>")
    rows.append("</tr></tbody></table>")
    rows.append(f"<p style='margin-top: 0.8rem; font-size: 0.9rem;'>"
                f"<b>해석</b>: 평균이 높은 archetype = 클래스가 공통으로 본 미래 패턴. "
                f"편차가 큰 archetype = 학생간 의견이 갈리는 지점 — 비판적 토론의 좋은 출발점.</p>")
    return "\n".join(rows)


def render_html(students: list[dict]) -> str:
    heatmap = render_heatmap(students)
    polar_svg, polar_list = render_polar(students)
    clusters = cluster_by_dominant(students)
    stats = render_stats(students)
    html = (HTML_TEMPLATE
            .replace("__HEATMAP__", heatmap)
            .replace("__POLAR_SVG__", polar_svg)
            .replace("__POLAR_LIST__", polar_list)
            .replace("__CLUSTERS__", clusters)
            .replace("__STATS__", stats))
    return html


# ═════════════════════════════════════════════════════════════════════
# CLI
# ═════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Class-wide Constellation 시각화 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dir", help="학생 audience_report .md 파일들이 있는 폴더")
    parser.add_argument("--demo", action="store_true",
                        help="2025 학생 14명 narratype 기반 synthetic 데모 데이터")
    parser.add_argument("--out", default="class_constellation.html",
                        help="출력 HTML 파일 (기본: class_constellation.html)")
    args = parser.parse_args()

    if args.demo:
        students = demo_data()
        print(f"[demo] {len(students)}명 synthetic 데이터 사용")
    elif args.dir:
        students = load_directory(args.dir)
        print(f"[load] {args.dir} 에서 {len(students)}명 파싱")
    else:
        parser.error("--dir 또는 --demo 중 하나 필요")

    if not students:
        print("학생 데이터 없음. 종료.", file=sys.stderr)
        sys.exit(1)

    html = render_html(students)
    Path(args.out).write_text(html, encoding="utf-8")
    print(f"[done] {args.out} ({len(html)} bytes)")
    print(f"브라우저에서 열기: open {args.out}")


if __name__ == "__main__":
    main()
