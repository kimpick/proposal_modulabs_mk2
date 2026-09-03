"""Deterministic checks for proposal content.json files.

This script performs local validation only. It does not call an LLM or any
external API, so it is safe to run before a Codex multi-agent review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT_DIR / "projects"
TEMPLATES_DIR = ROOT_DIR / "templates"

SEVERITY_ORDER = {"INFO": 0, "WARN": 1, "FIX": 2}

COMMON_REQUIRED = ["title", "subtitle", "info"]
# "output"(섹션 06 예상 산출물)은 track.html에서 조건부 렌더링되므로 필수가 아닙니다.
# 생략하면 섹션 자체가 빠지고 이후 섹션 번호가 자동으로 당겨집니다.
TRACK_REQUIRED = [
    "intro",
    "objective",
    "tech_stack",
    "tracks",
    "schedule_message",
]
MODULE_REQUIRED = ["modules"]
ROADMAP_REQUIRED = ["steps"]
SEMINAR_REQUIRED = ["seminars"]

TEXT_FIELDS_WITH_HTML = ["intro", "objective", "output", "schedule_message"]


@dataclass
class Finding:
    severity: str
    location: str
    issue: str
    impact: str
    recommendation: str


class TagBalanceParser(HTMLParser):
    VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() not in self.VOID_TAGS:
            self.stack.append(tag.lower())

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if not self.stack:
            self.errors.append(f"closing tag without opener: </{tag}>")
            return
        last = self.stack.pop()
        if last != tag:
            self.errors.append(f"expected </{last}> but found </{tag}>")

    def close(self) -> None:
        super().close()
        for tag in reversed(self.stack):
            self.errors.append(f"unclosed tag: <{tag}>")


def normalize_tool(tool: str) -> str:
    return re.sub(r"\s+", " ", str(tool)).strip()


def detect_template_type(data: dict[str, Any]) -> str | None:
    if data.get("type") == "bootcamp":
        return "bootcamp"
    if data.get("type") == "guide":
        return "guide"
    if "steps" in data:
        return "roadmap"
    if "tracks" in data:
        return "track"
    if "seminars" in data:
        return "khp-seminar"
    if "modules" in data:
        return "module"
    return None


def resolve_content_paths(target: str) -> list[Path]:
    raw = Path(target)
    if raw.is_file():
        return [raw]

    normalized = target.replace("\\", "/").strip("/")
    target_path = PROJECTS_DIR / normalized
    if target_path.is_file():
        return [target_path]
    if (target_path / "content.json").is_file():
        return [target_path / "content.json"]
    if target_path.is_dir():
        return sorted(target_path.rglob("content.json"))

    fallback = ROOT_DIR / normalized
    if fallback.is_file():
        return [fallback]
    if (fallback / "content.json").is_file():
        return [fallback / "content.json"]
    if fallback.is_dir():
        return sorted(fallback.rglob("content.json"))

    raise FileNotFoundError(f"content.json target not found: {target}")


def add_required_key_findings(
    data: dict[str, Any],
    keys: list[str],
    findings: list[Finding],
    prefix: str = "",
) -> None:
    for key in keys:
        if key not in data:
            findings.append(
                Finding(
                    "FIX",
                    f"{prefix}{key}",
                    "필수 키가 없습니다.",
                    "템플릿 렌더링 중 빈 섹션이 생기거나 빌드가 실패할 수 있습니다.",
                    f"`{key}` 값을 content.json에 추가하세요.",
                )
            )


def validate_html_fragment(value: Any, location: str, findings: list[Finding]) -> None:
    if not isinstance(value, str) or "<" not in value:
        return
    parser = TagBalanceParser()
    parser.feed(value)
    parser.close()
    if parser.errors:
        findings.append(
            Finding(
                "FIX",
                location,
                "HTML 태그 균형이 맞지 않습니다.",
                "PDF 렌더링에서 해당 섹션이 깨지거나 이후 내용까지 스타일이 오염될 수 있습니다.",
                "열고 닫는 태그를 맞추고, 복잡한 HTML은 짧은 `<p>`, `<ul>`, `<li>`, `<b>` 구조로 단순화하세요.",
            )
        )


def collect_track_tools(data: dict[str, Any]) -> tuple[set[str], list[tuple[str, set[str]]]]:
    track_tool_sets = []
    all_tools: set[str] = set()
    for track_index, track in enumerate(data.get("tracks", []) or []):
        tools = {
            normalize_tool(tool)
            for tool in track.get("tools", []) or []
            if normalize_tool(tool)
        }
        all_tools.update(tools)
        track_tool_sets.append((f"tracks[{track_index}].tools", tools))
    return all_tools, track_tool_sets


def validate_track_tools(data: dict[str, Any], findings: list[Finding]) -> None:
    tech_stack = {
        normalize_tool(tool)
        for tool in data.get("tech_stack", []) or []
        if normalize_tool(tool)
    }
    all_track_tools, track_tool_sets = collect_track_tools(data)

    missing_from_tech_stack = sorted(all_track_tools - tech_stack)
    extra_in_tech_stack = sorted(tech_stack - all_track_tools)

    if missing_from_tech_stack:
        findings.append(
            Finding(
                "FIX",
                "tech_stack",
                "`tracks[].tools`에는 있지만 `tech_stack`에는 없는 도구가 있습니다: "
                + ", ".join(missing_from_tech_stack),
                "제안서의 핵심 도구 섹션과 실제 트랙 배지가 달라져 고객이 교육 범위를 오해할 수 있습니다.",
                "`tech_stack`을 모든 Track tools의 합집합으로 맞추세요.",
            )
        )

    if extra_in_tech_stack:
        findings.append(
            Finding(
                "WARN",
                "tech_stack",
                "`tech_stack`에는 있지만 어떤 Track에도 없는 도구가 있습니다: "
                + ", ".join(extra_in_tech_stack),
                "실제로 다루지 않는 도구가 핵심 도구로 보일 수 있어 교육 범위가 부풀려 보입니다.",
                "실제 수업에서 쓰지 않는 도구라면 제거하고, 선택 도구라면 별도 설명으로 분리하세요.",
            )
        )

    known_tools = sorted(tech_stack | all_track_tools, key=len, reverse=True)
    for track_index, track in enumerate(data.get("tracks", []) or []):
        track_tools = {
            normalize_tool(tool)
            for tool in track.get("tools", []) or []
            if normalize_tool(tool)
        }
        item_texts = []
        for module in track.get("modules", []) or []:
            item_texts.extend(str(item) for item in module.get("items", []) or [])
        joined_items = "\n".join(item_texts)
        mentioned = {
            tool
            for tool in known_tools
            if tool and re.search(re.escape(tool), joined_items, flags=re.IGNORECASE)
        }
        missing_from_track = sorted(mentioned - track_tools)
        if missing_from_track:
            findings.append(
                Finding(
                    "FIX",
                    f"tracks[{track_index}].tools",
                    "본문에는 등장하지만 해당 Track tools에 없는 도구가 있습니다: "
                    + ", ".join(missing_from_track),
                    "PDF의 도구 배지와 실제 학습 항목이 달라져 준비물과 실습 범위가 불명확해집니다.",
                    "실제 사용하는 도구라면 `tracks[].tools`에 추가하고, 언급만 한 도구라면 본문 표현을 조정하세요.",
                )
            )


def validate_track_readability(data: dict[str, Any], findings: list[Finding]) -> None:
    for track_index, track in enumerate(data.get("tracks", []) or []):
        for module_index, module in enumerate(track.get("modules", []) or []):
            # item과 동일하게 태그를 제거한 실제 렌더링 길이로 판단
            module_name = re.sub(r"<[^>]+>", " ", str(module.get("module_name", ""))).strip()
            if len(module_name) > 15:
                findings.append(
                    Finding(
                        "WARN",
                        f"tracks[{track_index}].modules[{module_index}].module_name",
                        "모듈명이 15자를 초과합니다.",
                        "왼쪽 모듈명 컬럼에서 줄바꿈이 생겨 PDF 박스 높이가 불안정해질 수 있습니다.",
                        "핵심 명사구 중심으로 15자 안팎까지 줄이세요.",
                    )
                )

            items = module.get("items", []) or []
            if len(items) >= 5:
                findings.append(
                    Finding(
                        "WARN",
                        f"tracks[{track_index}].modules[{module_index}].items",
                        "모듈 item이 5개 이상입니다.",
                        "PDF에서 모듈 박스가 길어져 페이지 분할이나 과밀 문제가 생길 수 있습니다.",
                        "중복 항목을 합치거나 핵심 3-4개 항목으로 압축하세요.",
                    )
                )

            for item_index, item in enumerate(items):
                text = re.sub(r"<[^>]+>", "", str(item)).strip()
                if len(text) >= 100:
                    findings.append(
                        Finding(
                            "WARN",
                            f"tracks[{track_index}].modules[{module_index}].items[{item_index}]",
                            "item 문장이 100자를 초과합니다.",
                            "PDF에서 줄바꿈이 길어지고 핵심 키워드가 묻힐 수 있습니다.",
                            "한 item에는 하나의 활동만 담고, 세부 설명은 뒤 문장보다 짧은 명사구로 압축하세요.",
                        )
                    )
                validate_html_fragment(
                    item,
                    f"tracks[{track_index}].modules[{module_index}].items[{item_index}]",
                    findings,
                )


def validate_content(path: Path) -> list[Finding]:
    data = json.loads(path.read_text(encoding="utf-8"))
    findings: list[Finding] = []

    if not isinstance(data, dict):
        return [
            Finding(
                "FIX",
                "$",
                "content.json 최상위 구조가 객체가 아닙니다.",
                "빌드 스크립트가 템플릿 타입을 감지할 수 없습니다.",
                "최상위 JSON을 `{ ... }` 객체로 작성하세요.",
            )
        ]

    add_required_key_findings(data, COMMON_REQUIRED, findings)

    template_type = detect_template_type(data)
    if template_type is None:
        findings.append(
            Finding(
                "FIX",
                "$",
                "템플릿 타입을 감지할 수 없습니다.",
                "`tracks`, `modules`, `seminars`, `steps`, `type: bootcamp` 중 하나가 없으면 빌드할 템플릿을 고를 수 없습니다.",
                "제안서 목적에 맞는 최상위 키를 추가하세요.",
            )
        )
    else:
        template_path = TEMPLATES_DIR / f"{template_type}.html"
        if not template_path.is_file():
            findings.append(
                Finding(
                    "FIX",
                    "$",
                    f"템플릿 파일이 없습니다: templates/{template_type}.html",
                    "빌드가 실패합니다.",
                    "템플릿 파일을 추가하거나 content.json 타입을 기존 템플릿에 맞추세요.",
                )
            )

    if template_type == "track":
        add_required_key_findings(data, TRACK_REQUIRED, findings)
        validate_track_tools(data, findings)
        validate_track_readability(data, findings)
    elif template_type == "module":
        add_required_key_findings(data, MODULE_REQUIRED, findings)
    elif template_type == "roadmap":
        add_required_key_findings(data, ROADMAP_REQUIRED, findings)
    elif template_type == "khp-seminar":
        add_required_key_findings(data, SEMINAR_REQUIRED, findings)

    for field in TEXT_FIELDS_WITH_HTML:
        validate_html_fragment(data.get(field), field, findings)

    return findings


def final_verdict(findings: list[Finding]) -> str:
    fix_count = sum(1 for finding in findings if finding.severity == "FIX")
    warn_count = sum(1 for finding in findings if finding.severity == "WARN")
    if fix_count:
        return "NEEDS_FIX"
    if warn_count >= 3:
        return "NEEDS_FIX"
    if warn_count:
        return "PASS_WITH_NOTES"
    return "PASS"


def format_markdown(path: Path, findings: list[Finding]) -> str:
    verdict = final_verdict(findings)
    fix_count = sum(1 for finding in findings if finding.severity == "FIX")
    warn_count = sum(1 for finding in findings if finding.severity == "WARN")
    info_count = sum(1 for finding in findings if finding.severity == "INFO")

    lines = [
        f"## Local Validation: {path}",
        "",
        f"- Verdict: {verdict}",
        f"- FIX: {fix_count}",
        f"- WARN: {warn_count}",
        f"- INFO: {info_count}",
        "",
    ]

    if not findings:
        lines.append("No deterministic issues found.")
        return "\n".join(lines)

    lines.extend(
        [
            "| # | Severity | Location | Issue | Impact | Recommendation |",
            "|---|---|---|---|---|---|",
        ]
    )
    sorted_findings = sorted(
        findings,
        key=lambda finding: (
            -SEVERITY_ORDER.get(finding.severity, 0),
            finding.location,
        ),
    )
    for index, finding in enumerate(sorted_findings, start=1):
        row = [
            str(index),
            finding.severity,
            finding.location,
            finding.issue,
            finding.impact,
            finding.recommendation,
        ]
        escaped = [cell.replace("|", "\\|").replace("\n", " ") for cell in row]
        lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate proposal content.json files without external API calls."
    )
    parser.add_argument("target", help="content.json path, project folder, or company/proposal name")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of Markdown.",
    )
    args = parser.parse_args()

    try:
        paths = resolve_content_paths(args.target)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    results = []
    exit_code = 0
    for path in paths:
        findings = validate_content(path)
        verdict = final_verdict(findings)
        if verdict == "NEEDS_FIX":
            exit_code = 1
        results.append(
            {
                "path": str(path),
                "verdict": verdict,
                "findings": [finding.__dict__ for finding in findings],
            }
        )

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(format_markdown(Path(result["path"]), [
            Finding(**finding) for finding in result["findings"]
        ]) for result in results))

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
