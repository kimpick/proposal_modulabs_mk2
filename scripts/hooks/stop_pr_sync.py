"""
Stop hook — 커밋 안 된 제안서 산출물을 감지해 PR까지 자동 처리
==============================================================
응답이 끝나는 시점에 projects/{기업명}/ 변경이 남아 있으면
scripts/git_workflow.py 의 begin/finish 를 자동 실행해서
커밋 → push → PR 생성/업데이트까지 마친다.

"Claude가 기억해서 git_workflow.py를 호출해야만 PR이 열리는" 비결정성을 없애는 것이 목적.

안전장치 (하나라도 걸리면 자동 실행하지 않고 경고만 출력):
  1. stop_hook_active — hook이 촉발한 재실행에서는 무한루프 방지를 위해 즉시 종료
  2. 변경된 기업이 2곳 이상 — 어느 기업의 PR인지 모호하므로 사람이 판단
  3. 현재 브랜치가 main 도 proposal/* 도 아님 — 다른 작업 중일 수 있으므로 건드리지 않음
     (PROPOSAL_HOOK_ANY_BRANCH=1 로 해제 가능)
  4. 직전에 같은 상태로 이미 실패했음 — 같은 실패를 매 턴 반복하지 않는다
  5. PROPOSAL_HOOKS_DISABLE=1 — 전체 킬 스위치

gh CLI가 없으면 push까지는 되고 PR 생성만 실패한다 (git_workflow.py가 수동 링크를 안내).
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    ROOT_DIR,
    SCRIPTS_DIR,
    changed_companies,
    current_branch,
    git,
    hooks_disabled,
    read_hook_input,
    resolve_author,
    run,
    setup_io,
)

WORKFLOW = SCRIPTS_DIR / "git_workflow.py"
FAIL_MARKER = ROOT_DIR / ".git" / "proposal-pr-hook-failed"

# 변경 파일 패턴 → /명령 추론 (git_workflow.py의 --command choices와 일치해야 함)
COMMAND_HINTS = [
    ("견적서", "estimate"),
    ("이메일_초안", "estimate"),
    ("요구조건", "setup"),
]


def infer_command(paths: list[str]) -> str:
    """변경 파일로부터 어떤 단계였는지 추론. 확정 불가하면 build."""
    override = os.environ.get("PROPOSAL_HOOK_COMMAND", "").strip()
    if override in ("setup", "research", "review", "build", "estimate"):
        return override
    joined = "\n".join(paths)
    for needle, command in COMMAND_HINTS:
        if needle in joined:
            return command
    if any(p.endswith("content.json") for p in paths):
        return "setup"
    return "build"


def state_fingerprint(company: str, paths: list[str]) -> str:
    """현재 시도 상태의 지문 — 같은 상태로 반복 실패하는 것을 막기 위해 사용."""
    head = git("rev-parse", "HEAD")
    material = "|".join([company, head, *sorted(paths)])
    return hashlib.sha1(material.encode("utf-8")).hexdigest()


def already_failed(fingerprint: str) -> bool:
    try:
        return FAIL_MARKER.read_text(encoding="utf-8").strip() == fingerprint
    except OSError:
        return False


def mark_failed(fingerprint: str) -> None:
    try:
        FAIL_MARKER.parent.mkdir(parents=True, exist_ok=True)
        FAIL_MARKER.write_text(fingerprint, encoding="utf-8")
    except OSError:
        pass


def clear_failed() -> None:
    try:
        FAIL_MARKER.unlink()
    except OSError:
        pass


def workflow(subcommand: str, company: str, command: str, author: str,
             extra: list[str] | None = None) -> tuple[int, str]:
    cmd = [
        sys.executable, str(WORKFLOW), subcommand,
        "--company", company,
        "--command", command,
        "--author", author,
    ]
    cmd.extend(extra or [])
    proc = run(cmd, timeout=300)
    return proc.returncode, f"{proc.stdout or ''}{proc.stderr or ''}".strip()


def main() -> int:
    setup_io()
    if hooks_disabled():
        return 0

    payload = read_hook_input()
    # hook이 유발한 재실행에서 다시 돌면 무한루프가 된다.
    if payload.get("stop_hook_active"):
        return 0

    if not WORKFLOW.exists():
        return 0

    changed = changed_companies()
    if not changed:
        clear_failed()
        return 0

    if len(changed) > 1:
        names = ", ".join(sorted(changed))
        print(
            f"⚠️ 커밋되지 않은 제안서 변경이 여러 기업에 걸쳐 있습니다: {names}\n"
            "   기업별 활성 PR 1개 모델이라 자동 처리하지 않았습니다. 기업별로 나눠 실행하세요:\n"
            "   python scripts/git_workflow.py begin  --company <기업명> --command build --author <이름>\n"
            "   python scripts/git_workflow.py finish --company <기업명> --command build --author <이름> -m '<요약>'"
        )
        return 0

    company, paths = next(iter(changed.items()))
    command = infer_command(paths)
    author = resolve_author()
    branch = current_branch()

    fingerprint = state_fingerprint(company, paths)
    if already_failed(fingerprint):
        print(
            f"ℹ️ [{company}] PR 자동 처리를 직전에 같은 상태로 시도했다가 실패했습니다. "
            "같은 실패를 반복하지 않기 위해 건너뜁니다.\n"
            "   해결 후 수동 실행: "
            f"python scripts/git_workflow.py finish --company {company} "
            f"--command {command} --author {author} -m '<요약>'"
        )
        return 0

    on_proposal_branch = branch.startswith("proposal/")
    allow_any = os.environ.get("PROPOSAL_HOOK_ANY_BRANCH", "").lower() in ("1", "true", "yes")
    if not on_proposal_branch and branch not in ("main", "master") and not allow_any:
        print(
            f"ℹ️ [{company}] 커밋되지 않은 변경이 있지만 현재 브랜치가 "
            f"'{branch}' 라서 PR 자동 처리를 건너뜁니다.\n"
            "   (main 또는 proposal/* 브랜치에서만 자동 실행합니다. "
            "강제하려면 PROPOSAL_HOOK_ANY_BRANCH=1)"
        )
        return 0

    print(f"🔀 [{company}] 커밋되지 않은 산출물 {len(paths)}건 감지 — PR 자동 처리 시작 (/{command}, {author})")

    # 1. proposal 브랜치가 아니면 begin으로 브랜치 확보
    if not on_proposal_branch:
        code, out = workflow("begin", company, command, author)
        print(out)
        if code != 0:
            mark_failed(fingerprint)
            print(f"❌ [{company}] begin 실패 (exit {code}) — PR 자동 처리를 중단했습니다.")
            return 0

    # 2. finish로 commit + push + PR
    code, out = workflow(
        "finish", company, command, author,
        extra=["--message", f"/{command} 산출물 자동 동기화"],
    )
    print(out)
    if code != 0:
        mark_failed(fingerprint)
        print(
            f"❌ [{company}] finish 실패 (exit {code}).\n"
            "   exit 3=rebase 충돌 / 4=push 실패 / 5=PR 생성 실패(gh CLI 확인).\n"
            "   위 출력의 안내에 따라 수동 처리하세요."
        )
        return 0

    clear_failed()
    print(f"✅ [{company}] PR 동기화 완료")
    return 0


if __name__ == "__main__":
    sys.exit(main())
