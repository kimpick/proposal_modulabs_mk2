"""
Claude Code hook 공통 헬퍼
==========================
모든 hook 스크립트가 공유하는 유틸리티.

설계 원칙:
  1. hook은 절대 세션을 죽이지 않는다 — 예상치 못한 예외는 전부 삼키고 exit 0.
  2. cwd에 의존하지 않는다 — ROOT_DIR을 __file__ 기준으로 계산.
  3. Windows(Git Bash) / Linux 양쪽에서 동작 — shell 파이프라인 없이 python만 사용.
  4. PROPOSAL_HOOKS_DISABLE=1 이면 모든 hook이 즉시 no-op (킬 스위치).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PROJECTS_DIR = ROOT_DIR / "projects"
SCRIPTS_DIR = ROOT_DIR / "scripts"
TOKEN_PATH = ROOT_DIR / "token.json"


def setup_io() -> None:
    """Windows cp949 콘솔에서 한글/이모지 출력이 깨지지 않도록 강제 UTF-8."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def hooks_disabled() -> bool:
    return os.environ.get("PROPOSAL_HOOKS_DISABLE", "").lower() in ("1", "true", "yes")


def read_hook_input() -> dict:
    """stdin의 hook JSON 페이로드를 읽는다. 없거나 깨져 있으면 빈 dict."""
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}
    if not raw or not raw.strip():
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def emit_context(event_name: str, message: str) -> None:
    """Claude의 컨텍스트에 텍스트를 주입한다 (사람에게도 transcript에 보임)."""
    payload = {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": message,
        }
    }
    print(json.dumps(payload, ensure_ascii=False))


def run(cmd: list[str], cwd: Optional[Path] = None,
        timeout: int = 120) -> subprocess.CompletedProcess:
    """subprocess 안전 실행 (shell=True 금지)."""
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    return subprocess.run(
        cmd,
        cwd=str(cwd or ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
        env=env,
    )


def git(*args: str, timeout: int = 60) -> str:
    """git 명령 실행 후 stdout 반환. 실패해도 예외를 던지지 않는다."""
    try:
        return (run(["git", *args], timeout=timeout).stdout or "").strip()
    except Exception:
        return ""


def normalize(name: str) -> str:
    """macOS NFD ↔ Windows/Linux NFC 불일치 방지."""
    return unicodedata.normalize("NFC", name).strip()


def changed_companies() -> dict[str, list[str]]:
    """working tree에서 변경된 projects/{기업명}/ 을 기업별로 모은다.

    Returns:
        {기업명: [상대경로, ...]}  — untracked 포함, git_workflow.py가 걸러낼 것들도 포함
    """
    out = git("status", "--porcelain=v1", "-z")
    result: dict[str, list[str]] = {}
    for entry in out.split("\0"):
        if not entry or len(entry) < 4:
            continue
        path = entry[3:]
        if " -> " in path:  # rename
            path = path.split(" -> ", 1)[1]
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        path = normalize(path)
        if not path.startswith("projects/"):
            continue
        parts = path.split("/")
        if len(parts) < 2 or not parts[1]:
            continue
        result.setdefault(parts[1], []).append(path)
    return result


def current_branch() -> str:
    return git("rev-parse", "--abbrev-ref", "HEAD")


def resolve_author() -> str:
    """작업자명: PROPOSAL_AUTHOR 환경변수 > git config user.name > '시스템'."""
    author = os.environ.get("PROPOSAL_AUTHOR", "").strip()
    if author:
        return author
    name = git("config", "--get", "user.name")
    return name or "시스템"


def company_dir(company: str) -> Path:
    return PROJECTS_DIR / company
