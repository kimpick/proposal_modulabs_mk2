"""
SessionStart hook — Google Drive 인증 사전 확인
===============================================
세션이 시작될 때 Drive 업로드가 실제로 가능한 상태인지 미리 확인해서,
빌드를 다 끝낸 뒤에야 "업로드 실패"를 발견하는 상황을 막는다.

동작 (경고만 — 빌드를 차단하지 않는다):
  1. google-api-python-client / google-auth 설치 여부
  2. token.json 존재 여부
  3. access token 만료 시 refresh_token으로 갱신 시도 후 token.json에 재저장
  4. 문제가 있으면 Claude 컨텍스트에 경고 + 복구 방법 주입

수동 실행:
    python scripts/hooks/check_drive_auth.py --verify
    → Drive API를 실제로 한 번 호출해서 권한까지 확인 (--verify 없으면 토큰 갱신까지만)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from _common import (  # noqa: E402
    ROOT_DIR,
    TOKEN_PATH,
    emit_context,
    hooks_disabled,
    read_hook_input,
    setup_io,
)

EVENT = "SessionStart"

INSTALL_HINT = (
    "pip install google-auth google-auth-oauthlib google-api-python-client"
)
REAUTH_HINT = (
    "재인증 방법: Google Cloud OAuth 클라이언트로 token.json을 재발급한 뒤 "
    "저장소 루트에 두세요 (token.json은 .gitignore 대상 — 커밋되지 않습니다)."
)


def check(verify: bool = False) -> tuple[bool, str]:
    """(정상여부, 메시지) 반환."""
    # 1. 의존성
    try:
        from scripts.drive_upload import (  # noqa: F401
            BIZ_DRIVE_ID,
            DriveAuthError,
            get_credentials,
        )
    except ImportError as e:
        return False, (
            f"Google Drive 의존성이 없어 업로드가 조용히 건너뛰어집니다: {e}\n"
            f"→ {INSTALL_HINT}"
        )

    # 2. token.json
    if not TOKEN_PATH.exists():
        return False, (
            f"token.json이 없습니다 ({TOKEN_PATH}). Drive 업로드는 실패합니다.\n"
            f"→ {REAUTH_HINT}"
        )

    # 3. 토큰 로드 + 만료 시 갱신
    try:
        creds = get_credentials()
    except DriveAuthError as e:
        return False, f"Drive 인증 실패: {e}\n→ {REAUTH_HINT}"
    except Exception as e:
        return False, (
            f"Drive 토큰 갱신 실패 ({type(e).__name__}: {e}).\n"
            f"refresh_token이 만료·철회되었을 수 있습니다.\n→ {REAUTH_HINT}"
        )

    if not creds.valid:
        return False, (
            "Drive 토큰이 유효하지 않습니다 (갱신 시도 후에도 invalid).\n"
            f"→ {REAUTH_HINT}"
        )

    if not verify:
        expiry = creds.expiry.isoformat() + "Z" if creds.expiry else "미기록"
        return True, f"Drive 인증 정상 (access token 만료: {expiry})"

    # 4. --verify: 실제 API 호출로 권한까지 확인
    try:
        from googleapiclient.discovery import build as build_service

        service = build_service("drive", "v3", credentials=creds)
        drive = service.drives().get(driveId=BIZ_DRIVE_ID, fields="id,name").execute()
    except Exception as e:
        return False, (
            f"Drive API 호출 실패 ({type(e).__name__}: {e}).\n"
            "토큰은 유효하지만 공유 드라이브 접근 권한이 없을 수 있습니다."
        )
    return True, f"Drive 인증·권한 정상 — 공유 드라이브: {drive.get('name')}"


def main() -> int:
    setup_io()
    verify = "--verify" in sys.argv
    manual = verify or "--manual" in sys.argv

    if hooks_disabled():
        if manual:
            print("PROPOSAL_HOOKS_DISABLE=1 — hook 비활성 상태")
        return 0

    if not manual:
        read_hook_input()  # stdin을 비워 준다 (페이로드는 사용하지 않음)

    try:
        ok, message = check(verify=verify)
    except Exception as e:
        # hook이 세션을 죽이면 안 된다.
        if manual:
            print(f"확인 중 예기치 않은 오류: {type(e).__name__}: {e}")
        return 0

    if manual:
        print(("✅ " if ok else "❌ ") + message)
        return 0 if ok else 1

    # hook 모드: 문제가 있을 때만 컨텍스트에 주입 (정상이면 조용히 통과)
    if not ok:
        emit_context(
            EVENT,
            "⚠️ Google Drive 업로드 사전 점검 실패\n"
            f"{message}\n\n"
            "이 상태에서 build.py를 실행하면 PDF는 생성되지만 Drive 업로드는 "
            "건너뛰어집니다. 사용자에게 위 내용을 알리고, 업로드가 필요하면 "
            "인증을 먼저 복구하도록 안내하세요.",
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
