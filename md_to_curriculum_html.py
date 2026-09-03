#!/usr/bin/env python3
"""
===============================================================================
  Skill 1 Agent: 커리큘럼 MD → HTML 변환 파이프라인
===============================================================================

사용법:
    python md_to_curriculum_html.py <input.md> [-o output.html]

예시:
    # 같은 디렉토리에 HTML 생성 (입력파일명.html)
    python md_to_curriculum_html.py projects/도쿄일렉트론코리아/기초교육_RAG_커리큘럼.md

    # 출력 파일 경로 지정
    python md_to_curriculum_html.py 기초교육_RAG_커리큘럼.md -o 과정안내.html

입력 MD 파일 형식 (필수 구조):
    # [기관명] — [과정명]

    > [부제목]

    [설명 문단]

    ---

    ## 1단계: [단계명] (NH)

    | 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 및 구현 스택 |
    |------|--------|---------------|----------------------|
    | XH  | ...    | - ...<br>- ... | - ...<br>- ...       |

    ## 2단계: ...

    ---

    ## 심화 과정으로 이관되는 항목 (선택)

    | 항목 | 이관 사유 |
    |------|----------|
    | ...  | ...      |

    ---

    > * [하단 안내문]

특수 마커:
    **[Trend]**           → 초록색 Trend 뱃지
    **[Paradigm]**        → 빨간색 Paradigm 뱃지
    **[Paradigm Shift]**  → 빨간색 Paradigm Shift 뱃지
    **굵은 텍스트**        → <strong>굵은 텍스트</strong>
===============================================================================
"""

import re
import argparse
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List


# ── Data Models ──────────────────────────────────────────────────────────────

@dataclass
class Module:
    hours: str
    name: str
    content_items: List[str]
    practice_items: List[str]


@dataclass
class Stage:
    number: int
    title: str
    total_hours: str
    modules: List[Module] = field(default_factory=list)


@dataclass
class ExcludedItem:
    name: str
    reason: str


@dataclass
class Curriculum:
    company: str = ""
    title: str = ""
    subtitle: str = ""
    description: str = ""
    stages: List[Stage] = field(default_factory=list)
    excluded_items: List[ExcludedItem] = field(default_factory=list)
    footer: str = ""


# ── Parsing ──────────────────────────────────────────────────────────────────

def parse_md(filepath: str) -> Curriculum:
    """MD 파일을 파싱하여 Curriculum 객체 반환"""
    text = Path(filepath).read_text(encoding="utf-8")
    curr = Curriculum()

    # ── Title ────────────────────────────────────────────────────────────
    title_m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    if title_m:
        full = title_m.group(1).strip()
        for sep in ("\u2014", "\u2013", "-"):
            if sep in full:
                curr.company, curr.title = [s.strip() for s in full.split(sep, 1)]
                break
        else:
            curr.title = full

    # ── Subtitle ─────────────────────────────────────────────────────────
    sub_m = re.search(r"^>\s+(.+)", text, re.MULTILINE)
    if sub_m:
        curr.subtitle = sub_m.group(1).strip()

    # ── Description ──────────────────────────────────────────────────────
    desc_parts = []
    in_desc = False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("## ") or s == "---":
            break
        if s.startswith("#") or s.startswith(">") or not s:
            if in_desc:
                break
            continue
        desc_parts.append(s)
        in_desc = True
    curr.description = " ".join(desc_parts)

    # ── Stages: ## N단계 ... (XH) 별로 분리 파싱 ───────────────────────
    stage_re = re.compile(r"^##\s+(\d+)단계[:\s]+(.+?)\((\d+)H\)\s*$", re.MULTILINE)
    matches = list(stage_re.finditer(text))
    for idx, m in enumerate(matches):
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        chunk = text[start:end]
        dash = chunk.find("\n---\n")
        if dash >= 0:
            chunk = chunk[:dash]

        stage = Stage(
            number=int(m.group(1)),
            title=m.group(2).strip(),
            total_hours=m.group(3),
        )
        for row_text in _table_rows(chunk):
            cells = _split_row(row_text)
            if len(cells) >= 4:
                stage.modules.append(Module(
                    hours=cells[0],
                    name=cells[1],
                    content_items=_parse_items(cells[2]),
                    practice_items=_parse_items(cells[3]),
                ))
        curr.stages.append(stage)

    # ── Excluded items ───────────────────────────────────────────────────
    excl_m = re.search(r"^##\s+.*(?:이관|제외).*$", text, re.MULTILINE)
    if excl_m:
        chunk = text[excl_m.end():]
        dash = chunk.find("\n---\n")
        if dash >= 0:
            chunk = chunk[:dash]
        for row_text in _table_rows(chunk):
            cells = _split_row(row_text)
            if len(cells) >= 2:
                curr.excluded_items.append(ExcludedItem(name=cells[0], reason=cells[1]))

    # ── Footer ───────────────────────────────────────────────────────────
    footers = re.findall(r"^>\s*\*?\s*(.+)$", text, re.MULTILINE)
    if footers:
        curr.footer = footers[-1].strip()

    return curr


def _table_rows(text: str) -> List[str]:
    """표에서 헤더/구분선을 제외한 데이터 행만 반환"""
    rows = []
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]
        if not cells:
            continue
        # skip separator (---) or header rows
        if re.match(r"^[\s:\-]+$", cells[0]):
            continue
        if cells[0] in ("시간", "항목"):
            continue
        rows.append(line)
    return rows


def _split_row(line: str) -> List[str]:
    """| 로 분리하여 셀 텍스트 배열 반환"""
    return [c.strip() for c in line.split("|") if c.strip()]


def _parse_items(cell: str) -> List[str]:
    """셀 내용을 `- ...<br>- ...` 형식에서 항목 리스트로 분리"""
    parts = re.split(r"<br\s*/?>\s*", cell)
    items = []
    for p in parts:
        p = p.strip()
        if p.startswith("- "):
            p = p[2:]
        if p:
            items.append(p)
    return items


# ── HTML Formatting Helpers ──────────────────────────────────────────────────

def _badge(text: str) -> str:
    """MD 마커 → HTML 뱃지/볼드 변환"""
    text = re.sub(
        r"\*\*\[Trend\]\*\*\s*",
        '<span class="inline-block px-2 py-0.5 text-xs font-semibold text-white trend-badge rounded shadow-sm mr-1">Trend</span>',
        text,
    )
    text = re.sub(
        r"\*\*\[Paradigm Shift\]\*\*\s*",
        '<span class="inline-block px-2 py-0.5 text-xs font-semibold text-white paradigm-badge rounded shadow-sm mr-1">Paradigm Shift</span>',
        text,
    )
    text = re.sub(
        r"\*\*\[Paradigm\]\*\*\s*",
        '<span class="inline-block px-2 py-0.5 text-xs font-semibold text-white paradigm-badge rounded shadow-sm mr-1">Paradigm</span>',
        text,
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def _items_html(items: List[str]) -> str:
    """항목 리스트 → HTML <ul>/<li> 또는 단일 텍스트"""
    if not items:
        return ""
    if len(items) == 1:
        return _badge(items[0])
    parts = [f"<li>{_badge(it)}</li>" for it in items]
    return '<ul class="list-disc list-outside ml-4 space-y-1 text-gray-600">' + "".join(parts) + "</ul>"


# ── HTML Generation ──────────────────────────────────────────────────────────

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company} — {title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700&display=swap"
        rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Pretendard', 'sans-serif'],
                    }},
                    colors: {{
                        modu: {{
                            navy: '#1A233A',
                            blue: '#2B4162',
                            teal: '#00B4A6',
                            coral: '#FF6B6B',
                            light: '#F8FAFC',
                            border: '#E2E8F0'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            background-color: #F3F4F6;
            -webkit-font-smoothing: antialiased;
        }}
        .table-shadow {{
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        }}
        .trend-badge {{
            background: linear-gradient(135deg, #00B4A6 0%, #008F84 100%);
        }}
        .paradigm-badge {{
            background: linear-gradient(135deg, #FF6B6B 0%, #E03E3E 100%);
        }}
    </style>
</head>

<body class="p-4 md:p-8">
    <div class="max-w-7xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden table-shadow">
        <!-- Header -->
        <div class="bg-modu-navy p-8 md:p-10 text-white relative overflow-hidden">
            <div class="absolute top-0 right-0 w-64 h-64 bg-modu-teal rounded-full mix-blend-multiply filter blur-3xl opacity-20 transform translate-x-1/2 -translate-y-1/2"></div>
            <div class="absolute bottom-0 left-0 w-48 h-48 bg-modu-coral rounded-full mix-blend-multiply filter blur-3xl opacity-10 transform -translate-x-1/2 translate-y-1/2"></div>
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-modu-teal rounded-lg flex items-center justify-center font-bold text-xl tracking-tighter shadow-md">M</div>
                    <span class="text-xl font-semibold tracking-wide text-gray-100">{company}</span>
                </div>
                <div class="text-sm text-gray-300 font-medium px-3 py-1 bg-white/10 rounded-full backdrop-blur-sm border border-white/20">
                    B2B Enterprise Training
                </div>
            </div>
            <h1 class="text-3xl md:text-4xl font-bold mb-2 leading-tight">{title}</h1>
            <p class="text-modu-teal text-sm font-medium mb-4">{subtitle}</p>
            <p class="text-gray-300 text-lg max-w-3xl leading-relaxed">{description}</p>
        </div>

        <!-- Content -->
        <div class="p-8">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-modu-light text-modu-navy border-b-2 border-modu-border uppercase text-sm font-semibold tracking-wider">
                            <th class="p-4 rounded-tl-lg w-24 text-center">단계</th>
                            <th class="p-4 w-20 text-center">시간</th>
                            <th class="p-4 w-56">모듈명</th>
                            <th class="p-4">핵심 학습 내용</th>
                            <th class="p-4 rounded-tr-lg w-64">주요 실습 및 구현 스택</th>
                        </tr>
                    </thead>
                    <tbody class="text-gray-700 text-sm md:text-base">
{tbody}
                    </tbody>
                </table>
            </div>
{excluded_section}
            <!-- Footer -->
            <div class="mt-8 pt-6 border-t border-gray-100 flex flex-col md:flex-row items-center justify-between">
                <p class="text-sm text-gray-500 mb-4 md:mb-0">* {footer}</p>
                <button onclick="window.print()"
                    class="bg-modu-navy hover:bg-modu-blue text-white px-6 py-2 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2 shadow-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                    </svg>
                    <span>로드맵 PDF 인쇄</span>
                </button>
            </div>
        </div>
    </div>
</body>

</html>"""


def generate_html(curr: Curriculum) -> str:
    """Curriculum → 최종 HTML 문자열"""

    # ── Main table rows ──────────────────────────────────────────────────
    tbody_parts = []
    for si, stage in enumerate(curr.stages):
        n = len(stage.modules)
        for mi, mod in enumerate(stage.modules):
            # border class per row
            if mi < n - 1:
                bc = "border-b border-modu-border"
            elif si < len(curr.stages) - 1:
                bc = "border-b-2 border-modu-border"
            else:
                bc = ""

            parts = [f'<tr class="{bc} hover:bg-gray-50 transition-colors">']

            # Stage cell — first module only (rowspan)
            if mi == 0:
                bl = " rounded-bl-lg" if si == len(curr.stages) - 1 else ""
                parts.append(
                    f'<td rowspan="{n}" class="p-4 border-r border-modu-border text-center align-middle bg-gray-50{bl}">'
                    f'<div class="font-bold text-modu-blue text-lg mb-1">{stage.number}단계</div>'
                    f'<div class="text-xs text-gray-500 font-medium">{stage.title}<br>({stage.total_hours}H)</div>'
                    f"</td>"
                )

            parts.append(f'<td class="p-4 text-center font-semibold text-gray-600">{mod.hours}</td>')
            parts.append(f'<td class="p-4 font-bold text-modu-navy">{mod.name}</td>')
            parts.append(f'<td class="p-4 leading-relaxed">{_items_html(mod.content_items)}</td>')

            br = " rounded-br-lg" if (si == len(curr.stages) - 1 and mi == n - 1) else ""
            parts.append(f'<td class="p-4 leading-relaxed text-gray-600 bg-gray-50/50{br}">{_items_html(mod.practice_items)}</td>')

            parts.append("</tr>")
            tbody_parts.append("".join(parts))

    tbody = "\n".join(tbody_parts)

    # ── Excluded items section ───────────────────────────────────────────
    excluded_html = ""
    if curr.excluded_items:
        rows = ""
        for it in curr.excluded_items:
            rows += (
                '<tr class="border-b border-gray-100 hover:bg-gray-50">'
                f'<td class="p-3 text-gray-700">{it.name}</td>'
                f'<td class="p-3 text-gray-500 text-sm">{it.reason}</td>'
                "</tr>\n"
            )
        excluded_html = f"""\
            <div class="mt-8">
                <h3 class="text-lg font-semibold text-gray-700 mb-3">심화 과정으로 이관되는 항목</h3>
                <table class="w-full text-left border-collapse border border-gray-200 rounded-lg overflow-hidden">
                    <thead>
                        <tr class="bg-gray-50 text-sm font-semibold text-gray-600">
                            <th class="p-3 w-64">항목</th>
                            <th class="p-3">이관 사유</th>
                        </tr>
                    </thead>
                    <tbody>
{rows}
                    </tbody>
                </table>
            </div>"""

    return HTML_TEMPLATE.format(
        company=curr.company or "모두의연구소",
        title=_badge(curr.title),
        subtitle=curr.subtitle,
        description=_badge(curr.description),
        tbody=tbody,
        excluded_section=excluded_html,
        footer=curr.footer or "위 과정은 오픈소스 프레임워크(LangChain 등)를 기반으로 하여 Databricks, AWS 등 어떠한 인프라에서도 구현 가능합니다.",
    )


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="커리큘럼 MD → Modulabs 스타일 HTML 변환 (Skill 1 Agent)",
    )
    parser.add_argument("input", help="입력 MD 파일 경로")
    parser.add_argument("-o", "--output", help="출력 HTML 파일 경로 (기본: 입력파일명.html)")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"[ERROR] 파일 없음: {src}")
        sys.exit(1)

    dst = Path(args.output) if args.output else src.with_suffix(".html")

    curr = parse_md(str(src))
    html = generate_html(curr)
    dst.write_text(html, encoding="utf-8")

    n_modules = sum(len(s.modules) for s in curr.stages)
    print(f"[OK] HTML 생성 완료: {dst}")
    print(f"     {len(curr.stages)}단계 / {n_modules}모듈", end="")
    if curr.excluded_items:
        print(f" / 심화이관 {len(curr.excluded_items)}건", end="")
    print()


if __name__ == "__main__":
    main()
