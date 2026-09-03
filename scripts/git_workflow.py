#!/usr/bin/env python3
"""
모두의연구소 AI 교육 제안서 — PR 워크플로우 매니저
====================================================

Slack 명령(/setup, /review, /build, /estimate) 처리 흐름에서 호출되어
"기업별 활성 PR 1개" 모델로 Git 변경사항을 안전하게 관리.

사용 흐름:
    # 1. 작업 시작 시
    python scripts/git_workflow.py begin --company 한화오션 --command setup --author 영광

    # 2. 기존 작업 수행 (content.json 작성, 빌드, 검증, Drive 업로드 등)

    # 3. 작업 완료 시
    python scripts/git_workflow.py finish \
        --company 한화오션 --command setup --author 영광 \
        --message "초안 생성" \
        --drive-url "https://drive.google.com/..."

브랜치 명명 규칙:
    proposal/{company_key}/{YYYYMMDD-HHMM}-{command}-{author_slug}
    예) proposal/c-a1b2c3d4/20260620-1430-setup-영광

PR 라벨:
    company-{company_key}    (기업 식별용, 같은 기업 PR 찾기)
    proposal                 (유형 분류)

Git 추적 허용 범위 (finish 시 강제 적용):
    포함: content.json, *.md, *.csv, 이메일_초안.html
    제외: *.pdf, proposal_render.html, versions/

충돌 정책:
    같은 기업의 활성 PR이 이미 원격에 존재하면 rebase 후 push.
    같은 줄 충돌 시 자동 해결하지 않고 중단 (안전장치).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── 경로 설정 ──
ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT_DIR / "projects"

# ── 작업자 매핑 (version_manager.py와 동일) ──
USER_MAP = {
    "U0924H9HSK1": "영광",
    "U03RP0HEZDW": "은숙",
    "U093RP4EZMK": "은경",
}

# ── 허용/제외 파일 패턴 ──
ALLOWED_EXTENSIONS = {".json", ".md", ".csv", ".html"}
FORCE_EXCLUDE_NAMES = {"proposal_render.html", "combined_render.html"}
FORCE_EXCLUDE_PATTERNS = [
    re.compile(r"\.pdf$", re.IGNORECASE),
    re.compile(r"^versions/", re.IGNORECASE),
    re.compile(r"[~$]", re.IGNORECASE),  # 오피스 임시 파일
]
# .gitignore에 이미 제외된 항목도 명시적으로 보호
GITIGNORE_PROTECTED = {".hermes", ".omo", ".openclaw", ".claude", ".venv", "venv", "__pycache__"}

# ── PR 본문 템플릿 ──
PR_BODY_TEMPLATE = """## {command_upper} {company} — {author}

### 📝 변경 요약
{message}

### 📂 산출물
- **기업**: `{company}`
- **작업자**: {author}
- **명령**: `/{command}`
- **버전 스냅샷**: `{snapshot_name}`

### 🔗 링크
{drive_line}{slack_line}
- GitHub Branch: `tree/{branch}`

### ✅ 체크리스트
- [ ] `content.json` 스키마 검증 통과
- [ ] 도구 일관성 (tech_stack ↔ tracks[].tools ↔ modules[].items)
- [ ] PDF 빌드 정상 완료
- [ ] 검토자 1명 이상 승인

---
*이 PR은 `scripts/git_workflow.py finish`에 의해 자동 생성/업데이트되었습니다.*
*충돌 발생 시 자동 해결하지 않습니다. 리뷰어가 수동으로 조율해 주세요.*
"""


# ──────────────────────────────────────────────────────────────
# 보조 함수
# ──────────────────────────────────────────────────────────────

def normalize_company(name: str) -> str:
    """기업명을 NFC 정규화 (macOS NFD 이슈 방지)."""
    return unicodedata.normalize("NFC", name).strip()


def company_key(name: str) -> str:
    """기업명의 SHA-1 앞 8자리 (ASCII 브랜치명용)."""
    normalized = normalize_company(name)
    return "c-" + hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:8]


def resolve_author(author_input: str) -> str:
    """Slack User ID → 표시 이름 변환."""
    return USER_MAP.get(author_input, author_input)


def author_slug(author_input: str) -> str:
    """브랜치명용 ASCII 슬러그 (한글 그대로 유지해도 되지만 안전하게)."""
    name = resolve_author(author_input)
    # 한글/알파벳/숫자만 유지, 나머지는 -
    slug = re.sub(r"[^\w가-힣ㄱ-ㅎㅏ-ㅣ-]", "-", name, flags=re.UNICODE)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "unknown"


def timestamp() -> str:
    """YYYYMMDD-HHMM 형식."""
    return datetime.now().strftime("%Y%m%d-%H%M")


def run(cmd: list[str], *, check: bool = True, capture: bool = True,
        cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    """subprocess를 list 인자로 안전하게 실행 (shell=True 금지)."""
    return subprocess.run(
        cmd,
        check=check,
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(cwd) if cwd else None,
    )


def run_git(*args: str, **kwargs) -> str:
    """git 명령 래퍼. stdout 반환."""
    result = run(["git", *args], **kwargs)
    return (result.stdout or "").strip()


def run_gh(*args: str, **kwargs) -> str:
    """gh CLI 명령 래퍼. stdout 반환."""
    result = run(["gh", *args], **kwargs)
    return (result.stdout or "").strip()


def is_git_clean() -> bool:
    """working tree가 clean인지 (untracked 제외)."""
    out = run_git("status", "--porcelain", check=False)
    # untracked(??)는 무시, 추적 파일 변경만 검사
    for line in out.splitlines():
        if line and not line.startswith("??"):
            return False
    return True


def should_include_file(rel_path: str) -> bool:
    """PR에 포함할 경로인지 판별.

    Args:
        rel_path: repo root 기준 상대경로 (POSIX separator)
    """
    # 강제 제외 패턴
    for pat in FORCE_EXCLUDE_PATTERNS:
        if pat.search(rel_path):
            return False
    # 강제 제외 파일명
    name = os.path.basename(rel_path)
    if name in FORCE_EXCLUDE_NAMES:
        return False
    # .gitignore 보호 항목
    parts = rel_path.split("/")
    for p in parts:
        if p in GITIGNORE_PROTECTED:
            return False
    # 확장자 허용 목록
    ext = os.path.splitext(name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    return True


def collect_changes(company: str) -> tuple[list[str], list[str]]:
    """해당 기업 폴더 내의 변경/신규 파일 중 PR 포함 대상만 분류.

    Returns:
        (staged_files, skipped_files)  — POSIX 경로
    """
    company_nfc = normalize_company(company)
    company_prefix = f"projects/{company_nfc}/"

    # git status (NUL 구분, macOS NFC/NFD 안전)
    out = run_git("status", "--porcelain=v1", "-z", check=False)

    staged: list[str] = []
    skipped: list[str] = []

    # -z 옵션: NUL로 항목 구분, 각 항목은 "XY path"
    for entry in out.split("\0"):
        if not entry:
            continue
        # 앞 2자리 status code, 그 다음 공백, 그 다음 경로
        if len(entry) < 4:
            continue
        path = entry[3:]
        # rename 형식 "R  old -> new" 처리
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        # 따옴표 제거 (git이 특수문자 경로를 quoted할 수 있음)
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
            # C-escape 풀기 (간단버전)
            path = path.encode("utf-8").decode("unicode_escape", errors="replace")

        # 회사 폴더 밖이면 무시
        if not path.startswith(company_prefix):
            continue

        if should_include_file(path):
            staged.append(path)
        else:
            skipped.append(path)

    return staged, skipped


# ──────────────────────────────────────────────────────────────
# PR 조회
# ──────────────────────────────────────────────────────────────

def find_open_pr(c_key: str) -> Optional[dict]:
    """company_key 라벨이 붙은 열린 PR 찾기.

    Returns:
        {number, branch, url} 또는 None
    """
    if not shutil.which("gh"):
        return None
    label = f"company-{c_key}"
    out = run_gh(
        "pr", "list",
        "--state", "open",
        "--label", label,
        "--limit", "1",
        "--json", "number,headRefName,url",
        check=False,
    )
    if not out:
        return None
    try:
        data = json.loads(out)
        if data and isinstance(data, list) and len(data) > 0:
            pr = data[0]
            return {
                "number": pr.get("number"),
                "branch": pr.get("headRefName"),
                "url": pr.get("url"),
            }
    except (json.JSONDecodeError, KeyError):
        pass
    return None


# ──────────────────────────────────────────────────────────────
# begin: 작업 시작
# ──────────────────────────────────────────────────────────────

def cmd_begin(args: argparse.Namespace) -> int:
    company = normalize_company(args.company)
    c_key = company_key(company)
    author = resolve_author(args.author)
    branch_name = f"proposal/{c_key}/{timestamp()}-{args.command}-{author_slug(args.author)}"

    print(f"🚀 BEGIN: /{args.command} {company} — {author}")
    print(f"   company_key: {c_key}")
    print(f"   proposed branch: {branch_name}")
    print()

    # 기존 열린 PR 확인
    existing_pr = find_open_pr(c_key)
    if existing_pr:
        print(f"📌 기존 열린 PR 발견: #{existing_pr['number']}")
        print(f"   branch: {existing_pr['branch']}")
        print(f"   url:    {existing_pr['url']}")
        print()
        if args.dry_run:
            print("   [dry-run] 기존 브랜치 checkout + origin/main rebase 실행 예정")
            return 0

        # 기존 브랜치 checkout
        print("   기존 브랜치 checkout 중...")
        run_git("fetch", "origin", "--prune")
        run_git("checkout", existing_pr["branch"])
        # origin/main과 rebase (기존 PR이 main 뒤처졌을 수 있음)
        print("   origin/main 기준 rebase 중...")
        result = run(["git", "rebase", "origin/main"], check=False)
        if result.returncode != 0:
            # 충돌 발생 → 안전하게 중단
            print("⚠️  rebase 충돌 발생. 안전하게 abort 합니다.")
            run_git("rebase", "--abort", check=False)
            print(f"   기존 PR을 먼저 머지/수정한 후 재시도하세요: {existing_pr['url']}")
            return 2
        print(f"✅ 기존 PR 브랜치에서 작업 재개: {existing_pr['branch']}")
        print(f"   PR: {existing_pr['url']}")
        return 0

    # 새 브랜치 생성
    print("🆕 새 PR 브랜치 생성")
    if args.dry_run:
        print(f"   [dry-run] 실행 예정:")
        print(f"   - git fetch origin --prune")
        print(f"   - git checkout -b {branch_name} origin/main")
        return 0

    run_git("fetch", "origin", "--prune")
    run_git("checkout", "-b", branch_name, "origin/main")
    print(f"✅ 새 브랜치 생성 완료: {branch_name}")
    print()
    print("다음 단계:")
    print("  1. /setup, /review, /build, /estimate 등 기존 작업 수행")
    print("  2. 작업 완료 후:")
    print(f"     python scripts/git_workflow.py finish --company {args.company} \\")
    print(f"       --command {args.command} --author {args.author} \\")
    print(f"       --message '<변경 요약>' --drive-url '<Drive 링크>'")
    return 0


# ──────────────────────────────────────────────────────────────
# finish: 작업 완료 (commit + push + PR)
# ──────────────────────────────────────────────────────────────

def cmd_finish(args: argparse.Namespace) -> int:
    company = normalize_company(args.company)
    c_key = company_key(company)
    author = resolve_author(args.author)

    print(f"🏁 FINISH: /{args.command} {company} — {author}")
    print(f"   company_key: {c_key}")
    print()

    # 1. 변경 파일 수집
    staged_files, skipped_files = collect_changes(company)
    print(f"📦 변경 파일 분석")
    print(f"   포함: {len(staged_files)}개")
    for f in staged_files[:20]:
        print(f"     + {f}")
    if len(staged_files) > 20:
        print(f"     ... 외 {len(staged_files) - 20}개")
    print(f"   제외: {len(skipped_files)}개 (PDF/HTML 렌더/versions/ 등)")
    for f in skipped_files[:10]:
        print(f"     - {f}")
    if len(skipped_files) > 10:
        print(f"     ... 외 {len(skipped_files) - 10}개")
    print()

    if not staged_files:
        print("ℹ️  포함할 변경 파일이 없습니다.")
        print("   Git 추적 대상이 아니거나 이미 커밋된 상태일 수 있습니다.")
        if not args.dry_run:
            return 0

    # 2. 현재 브랜치 확인
    current_branch = run_git("rev-parse", "--abbrev-ref", "HEAD", check=False)
    is_new_branch = current_branch.startswith(f"proposal/{c_key}/")

    if not is_new_branch:
        print(f"⚠️  현재 브랜치가 이 기업 PR 브랜치가 아닙니다: {current_branch}")
        print(f"   먼저 begin 명령을 실행하세요:")
        print(f"   python scripts/git_workflow.py begin --company {args.company} \\")
        print(f"     --command {args.command} --author {args.author}")
        return 1

    if args.dry_run:
        print("[dry-run] 이하 단계는 실행하지 않음:")
        print(f"  - git add <{len(staged_files)} files>")
        commit_msg = f"{args.command} {company} — {author} ({args.message})"
        print(f"  - git commit -m {commit_msg!r}")
        print(f"  - git push -u origin {current_branch}")
        print(f"  - gh pr create --label company-{c_key} --label proposal")
        return 0

    # 3. 파일 스테이징
    if staged_files:
        run_git("add", "--", *staged_files)

    # 4. 커밋 (이미 스테이지된 게 있을 때만)
    staged_after = run_git("diff", "--cached", "--name-only", check=False)
    if not staged_after:
        print("ℹ️  신규 커밋할 변경사항 없음 (이미 커밋된 상태일 수 있음)")
    else:
        commit_msg = f"{args.command} {company} — {author}"
        if args.message:
            commit_msg += f" ({args.message})"
        run_git("commit", "-m", commit_msg)
        print(f"✅ 커밋 완료: {commit_msg}")

    # 5. rebase origin/main (다른 작업자가 main에 머지했을 수 있음)
    print("🔄 origin/main 기준 rebase...")
    run_git("fetch", "origin", "--prune")
    result = run(["git", "rebase", "origin/main"], check=False)
    if result.returncode != 0:
        print("⚠️  rebase 충돌 발생. 안전하게 abort 합니다.")
        run_git("rebase", "--abort", check=False)
        print()
        print("원인:")
        print("  - 다른 작업자가 같은 기업의 변경사항을 main에 머지했을 가능성")
        print("  - 같은 파일의 같은 줄을 수정했을 가능성")
        print()
        print("해결:")
        print("  1. origin/main의 최신 변경사항을 수동으로 검토")
        print("  2. 충돌 해결 후 커밋 → push")
        print("  3. 또는 로컬 변경사항을 백업 후 reset --hard origin/main 후 재작업")
        return 3

    # 6. push
    print(f"📤 push: {current_branch}")
    push_result = run(
        ["git", "push", "-u", "origin", current_branch],
        check=False,
    )
    if push_result.returncode != 0:
        print(f"❌ push 실패:")
        print(push_result.stderr)
        print()
        print("원격이 앞서 있을 수 있습니다. 수동으로 해결하세요.")
        return 4

    # 7. PR 생성 또는 업데이트
    existing_pr = find_open_pr(c_key)
    drive_line = f"- Google Drive: {args.drive_url}\n" if args.drive_url else ""
    slack_line = f"- Slack thread: {args.slack_thread}\n" if args.slack_thread else ""

    pr_body = PR_BODY_TEMPLATE.format(
        command_upper=args.command.upper(),
        company=company,
        author=author,
        message=args.message or "(설명 없음)",
        snapshot_name=args.snapshot or "(로컬 스냅샷)",
        drive_line=drive_line,
        slack_line=slack_line,
        branch=current_branch,
    )
    pr_title = f"[/{args.command}] {company} AI 교육 제안서 — {author}"

    if existing_pr:
        print(f"📌 기존 PR 업데이트: #{existing_pr['number']}")
        # PR 본문 업데이트
        run_gh(
            "pr", "edit", str(existing_pr["number"]),
            "--title", pr_title,
            "--body", pr_body,
            check=False,
        )
        # 코멘트로 새 커밋 요약 추가
        comment_body = f"### 💬 {args.command.upper()} 업데이트\n\n{args.message or '(설명 없음)'}\n"
        if args.drive_url:
            comment_body += f"\n📂 Drive: {args.drive_url}\n"
        run_gh(
            "pr", "comment", str(existing_pr["number"]),
            "--body", comment_body,
            check=False,
        )
        print(f"✅ PR 업데이트 완료: {existing_pr['url']}")
        print()
        print("Slack 회신에 포함할 링크:")
        print(f"  🔀 PR: {existing_pr['url']}")
        if args.drive_url:
            print(f"  📂 Drive: {args.drive_url}")
        branch_files_url = f"https://github.com/{get_repo_slug()}/tree/{current_branch}/projects/{company}"
        print(f"  📁 Branch Files: {branch_files_url}")
        return 0

    # 새 PR 생성
    print("🆕 새 PR 생성")
    repo_slug = get_repo_slug()
    pr_create_args = [
        "pr", "create",
        "--title", pr_title,
        "--body", pr_body,
        "--base", "main",
        "--head", current_branch,
        "--label", f"company-{c_key}",
        "--label", "proposal",
    ]
    gh_out = run_gh(*pr_create_args, check=False)
    if not gh_out or "https://" not in gh_out:
        print(f"⚠️  PR 생성 실패. gh CLI 출력:")
        print(gh_out or "(빈 응답)")
        print()
        print(f"브랜치는 push 되었습니다: {current_branch}")
        print("수동으로 PR을 생성하세요:")
        print(f"  https://github.com/{repo_slug}/pull/new/{current_branch}")
        return 5

    print(f"✅ PR 생성 완료: {gh_out}")
    print()
    print("Slack 회신에 포함할 링크:")
    print(f"  🔀 PR: {gh_out}")
    if args.drive_url:
        print(f"  📂 Drive: {args.drive_url}")
    branch_files_url = f"https://github.com/{repo_slug}/tree/{current_branch}/projects/{company}"
    print(f"  📁 Branch Files: {branch_files_url}")
    return 0


def get_repo_slug() -> str:
    """현재 원격의 'owner/repo' 슬러그."""
    out = run_git("config", "--get", "remote.origin.url", check=False)
    # https://github.com/owner/repo(.git) 형태 파싱
    m = re.search(r"github\.com[:/]([^/]+)/([^/.\s]+)", out)
    if m:
        return f"{m.group(1)}/{m.group(2)}"
    return "kisdevan/propsal_modulabs"


# ──────────────────────────────────────────────────────────────
# status: 현재 PR 상태 조회
# ──────────────────────────────────────────────────────────────

def cmd_status(args: argparse.Namespace) -> int:
    company = normalize_company(args.company)
    c_key = company_key(company)
    print(f"🔍 STATUS: {company}")
    print(f"   company_key: {c_key}")
    print()

    existing_pr = find_open_pr(c_key)
    if existing_pr:
        print(f"📌 열린 PR: #{existing_pr['number']}")
        print(f"   branch: {existing_pr['branch']}")
        print(f"   url:    {existing_pr['url']}")
        return 0

    print("ℹ️  열린 PR 없음")
    return 0


# ──────────────────────────────────────────────────────────────
# CLI 진입점
# ──────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="PR 워크플로우 매니저 — 기업별 활성 PR 1개 모델",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
흐름:
  begin    작업 시작. 열린 PR 있으면 rebase 후 재개, 없으면 새 브랜치 생성
  finish   작업 완료. 허용 파일만 stage → commit → push → PR 생성/업데이트
  status   현재 기업의 열린 PR 조회

예시:
  python scripts/git_workflow.py begin --company 한화오션 --command setup --author 영광
  python scripts/git_workflow.py finish --company 한화오션 --command setup --author 영광 \\
    --message "초안 생성" --drive-url "https://drive.google.com/..."
        """,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_begin = sub.add_parser("begin", help="작업 시작 (브랜치 체크아웃/생성)")
    p_begin.add_argument("--company", required=True, help="기업명")
    p_begin.add_argument("--command", required=True,
                         choices=["setup", "research", "review", "build", "estimate"],
                         help="Slack 명령어")
    p_begin.add_argument("--author", required=True, help="작업자 이름 또는 Slack User ID")
    p_begin.add_argument("--dry-run", action="store_true", help="실행하지 않고 계획만 출력")

    p_finish = sub.add_parser("finish", help="작업 완료 (commit + push + PR)")
    p_finish.add_argument("--company", required=True, help="기업명")
    p_finish.add_argument("--command", required=True,
                          choices=["setup", "research", "review", "build", "estimate"],
                          help="Slack 명령어")
    p_finish.add_argument("--author", required=True, help="작업자 이름 또는 Slack User ID")
    p_finish.add_argument("--message", "-m", default="", help="변경 요약 (커밋 메시지)")
    p_finish.add_argument("--drive-url", default="", help="Google Drive 폴더/파일 링크")
    p_finish.add_argument("--slack-thread", default="", help="Slack 스레드 링크")
    p_finish.add_argument("--snapshot", default="", help="version_manager 스냅샷 이름")
    p_finish.add_argument("--dry-run", action="store_true", help="실행하지 않고 계획만 출력")

    p_status = sub.add_parser("status", help="현재 기업의 열린 PR 조회")
    p_status.add_argument("--company", required=True, help="기업명")

    args = parser.parse_args()

    if args.cmd == "begin":
        return cmd_begin(args)
    elif args.cmd == "finish":
        return cmd_finish(args)
    elif args.cmd == "status":
        return cmd_status(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
