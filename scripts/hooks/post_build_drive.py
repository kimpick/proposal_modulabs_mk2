"""
PostToolUse hook — 빌드 후 Google Drive 업로드 검증 및 재시도
=============================================================
Bash 도구로 build.py를 실행한 직후에 발동한다.
빌드는 됐는데 Drive에 안 올라간 경우를 잡아내는 "그물" 역할.

build.py 자체가 업로드를 수행하므로 정상 경로에서는 이 hook이 할 일이 없다.
다만 아래 경우에 실제로 재시도한다:
  - build.py 출력에 업로드 성공 흔적(📂 Drive:)이 없음
  - --no-drive-upload / CI=true 가 아님
  - 산출물(PDF/CSV/HTML)이 실제로 존재함

경고만 하는 정책이므로 재시도가 실패해도 exit 0으로 통과시키고,
결과만 Claude 컨텍스트에 주입한다.
"""

from __future__ import annotations

import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from _common import (  # noqa: E402
    PROJECTS_DIR,
    emit_context,
    hooks_disabled,
    normalize,
    read_hook_input,
    resolve_author,
    setup_io,
)

EVENT = "PostToolUse"
UPLOAD_MARKERS = ("📂 Drive:", "📂 Drive 폴더:")
SKIP_FLAGS = ("--no-drive-upload",)
ARTIFACT_EXTENSIONS = {".pdf", ".csv", ".html"}


SHELL_OPERATORS = ("&&", "||", ";", "|", "&")
INTERPRETER_RE = re.compile(r"^(?:.*[/\\])?(?:python|python3|py|python\.exe|py\.exe)$",
                            re.IGNORECASE)
BUILD_SCRIPT_RE = re.compile(r"^(?:.*[/\\])?build\.py$", re.IGNORECASE)


def _find_build_invocation(tokens: list[str]) -> int | None:
    """토큰 목록에서 실제 `python build.py` 호출 위치(build.py 토큰의 인덱스)를 찾는다.

    `build.py`를 단순 문자열 포함 검사로 찾으면 오탐이 난다. 예를 들어
        echo '{"command":"python build.py 미래엔"}'
        grep -n build.py scripts/*.py
    같은 명령에서도 걸린다 (실제로 이 hook이 자기 테스트 명령에 오탐했다).
    그래서 (1) shlex로 토큰화해 인용된 문자열 안쪽은 하나의 토큰으로 묶고,
    (2) build.py가 **독립 토큰**이면서 (3) 바로 앞이 python 인터프리터일 때만 인정한다.
    """
    for i, tok in enumerate(tokens):
        if not BUILD_SCRIPT_RE.match(tok):
            continue
        prev = tokens[i - 1] if i > 0 else ""
        if INTERPRETER_RE.match(prev):
            return i
    return None


def extract_build_target(command: str) -> tuple[str | None, bool]:
    """build.py 실행 명령에서 (기업명, 업로드 생략여부) 추출.

    Returns:
        (기업명 or None, skip_requested)
        기업명이 None이면 이 hook은 아무것도 하지 않는다 (--all, 오탐 포함).
    """
    if "build.py" not in command:
        return None, False

    try:
        tokens = shlex.split(command)
    except ValueError:
        # 인용부호가 안 맞는 명령 — 잘못 쪼개서 오탐하는 것보다 포기하는 편이 안전하다.
        return None, False

    idx = _find_build_invocation(tokens)
    if idx is None:
        return None, False

    # build.py 이후 ~ 다음 셸 연산자 전까지가 이 명령의 인자
    args: list[str] = []
    for tok in tokens[idx + 1:]:
        if tok in SHELL_OPERATORS:
            break
        args.append(tok)

    # 인터프리터 앞의 환경변수 할당(CI=true python build.py ...)도 확인 대상
    prefix = tokens[:idx]
    skip = any(flag in args for flag in SKIP_FLAGS)
    for tok in prefix + args:
        if re.fullmatch(r"CI=(1|true|yes)", tok, re.IGNORECASE):
            skip = True

    # --author 영광, -m "메시지" 같은 옵션 값이 위치 인자로 새는 것을 방지
    flags_with_value = {"--author", "--message", "-m"}
    positional: list[str] = []
    skip_next = False
    for tok in args:
        if skip_next:
            skip_next = False
            continue
        if tok in flags_with_value:
            skip_next = True
            continue
        if tok.startswith("-"):
            if tok == "--all":
                return None, skip  # 전체 빌드는 대상이 모호하므로 손대지 않는다
            continue
        positional.append(tok)

    if not positional:
        return None, skip

    target = positional[0].replace("\\", "/")
    company = normalize(target.split("/")[0])
    return (company or None), skip


def has_artifacts(company_dir: Path) -> bool:
    for path in company_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in ARTIFACT_EXTENSIONS:
            return True
    return False


def main() -> int:
    setup_io()
    if hooks_disabled():
        return 0

    payload = read_hook_input()
    if payload.get("tool_name") != "Bash":
        return 0

    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command") or ""
    company, skip_requested = extract_build_target(command)
    if not company:
        return 0

    # build.py 출력에서 업로드 성공 여부 확인
    response = payload.get("tool_response")
    if isinstance(response, dict):
        output = f"{response.get('stdout', '')}\n{response.get('stderr', '')}"
    else:
        output = str(response or "")

    if any(marker in output for marker in UPLOAD_MARKERS):
        return 0  # 정상 업로드됨 — 할 일 없음

    if skip_requested:
        emit_context(
            EVENT,
            f"ℹ️ [{company}] 빌드 시 Drive 업로드를 명시적으로 생략했습니다 "
            "(--no-drive-upload 또는 CI=true). 최종 산출물이라면 나중에 "
            f"`python scripts/drive_upload.py projects/{company}` 로 올려야 합니다.",
        )
        return 0

    company_dir = PROJECTS_DIR / company
    if not company_dir.is_dir():
        return 0
    if not has_artifacts(company_dir):
        return 0  # 빌드 자체가 실패한 것 — 업로드할 게 없다

    # 재시도
    try:
        from scripts.drive_upload import DriveAuthError, upload_company_files
    except ImportError as e:
        emit_context(
            EVENT,
            f"⚠️ [{company}] 빌드 산출물이 Drive에 업로드되지 않았습니다.\n"
            f"원인: Google Drive 의존성 미설치 ({e})\n"
            "→ pip install google-auth google-auth-oauthlib google-api-python-client\n"
            "사용자에게 이 사실을 알리세요 — PDF는 로컬에만 있습니다.",
        )
        return 0

    try:
        result = upload_company_files(str(company_dir), author=resolve_author())
    except DriveAuthError as e:
        emit_context(
            EVENT,
            f"⚠️ [{company}] Drive 업로드 실패 — 인증 문제: {e}\n"
            "PDF는 로컬에 정상 생성되었습니다. 사용자에게 인증 복구가 필요함을 알리세요.",
        )
        return 0
    except Exception as e:
        emit_context(
            EVENT,
            f"⚠️ [{company}] Drive 재업로드 실패 ({type(e).__name__}: {e})\n"
            "PDF는 로컬에 정상 생성되었습니다. 사용자에게 알리세요.",
        )
        return 0

    if result:
        emit_context(
            EVENT,
            f"✅ [{company}] 빌드 출력에 업로드 기록이 없어 hook이 Drive 업로드를 "
            f"보완 실행했습니다.\n📂 {result['folder_link']}\n"
            "사용자 회신에 이 링크를 포함하세요.",
        )
    else:
        emit_context(
            EVENT,
            f"ℹ️ [{company}] 업로드 대상 파일을 찾지 못했습니다 "
            f"(projects/{company}/ 아래 PDF/CSV/HTML 확인 필요).",
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
