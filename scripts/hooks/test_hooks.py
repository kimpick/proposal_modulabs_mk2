"""
hook 스크립트 회귀 테스트
=========================
실행:
    python scripts/hooks/test_hooks.py

의존성 없음 (google 라이브러리 불필요). 파싱·추론 로직만 검증한다.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from post_build_drive import extract_build_target  # noqa: E402
from stop_pr_sync import infer_command  # noqa: E402

# 이 테스트 파일을 다루는 Bash 명령이 PostToolUse hook을 오탐 발동시키지 않도록
# 리터럴 "build.py" 를 파일 안에 직접 쓰지 않는다.
B = "build" + ".py"

BUILD_COMMANDS = [
    # (명령, (기업명, 업로드생략))
    (f"python {B} 한화오션", ("한화오션", False)),
    (f"python {B} 한화오션/전체_교육_로드맵", ("한화오션", False)),
    (f"python {B} 기웅정보통신 --author 영광", ("기웅정보통신", False)),
    (f'python {B} 미래엔 --author 영광 -m "초안 수정"', ("미래엔", False)),
    (f"python {B} 미래엔 --no-drive-upload", ("미래엔", True)),
    (f"CI=true python {B} 미래엔", ("미래엔", True)),
    (f"PYTHONIOENCODING=utf-8 python {B} 가온그룹", ("가온그룹", False)),
    (f"python3 {B} 미래엔", ("미래엔", False)),
    (f"python ./{B} 미래엔", ("미래엔", False)),
    (f"python /home/user/propsal_modulabs/{B} 미래엔", ("미래엔", False)),
    (f"python {B} 삼성전자_7-8월교육 && echo done", ("삼성전자_7-8월교육", False)),
    (f"cd /repo && python {B} 미래엔", ("미래엔", False)),
    # --all 은 대상이 모호하므로 hook이 개입하지 않는다
    (f"python {B} --all", (None, False)),
    (f"python {B} --all --author 은숙", (None, False)),
    (f"python {B}", (None, False)),
]

# build.py 문자열이 등장하지만 실제 빌드 실행이 아닌 명령 — 반드시 (None, False)
NON_BUILD_COMMANDS = [
    # 회귀: hook 도입 당시 이 형태(JSON 인자 속 문자열)에 실제로 오탐했다
    f"""echo '{{"tool_input":{{"command":"python {B} 미래엔"}}}}' | python hook.py""",
    f"grep -n {B} scripts/*.py",
    f"rg '{B}' --glob '*.md'",
    f"cat {B}",
    f"git diff {B}",
    f'echo "python {B} 미래엔 실행하세요"',
    f"ls -la {B}",
    f"sed -i 's/x/y/' {B}",
    f"python -c \"print('python {B} 미래엔')\"",
    "git status",
    "python scripts/validate_content.py projects/미래엔",
]

COMMAND_INFERENCE = [
    (["projects/미래엔/제안서/content.json"], "setup"),
    (["projects/미래엔/요구조건.md"], "setup"),
    (["projects/미래엔/미래엔_AI교육_견적서.csv"], "estimate"),
    (["projects/미래엔/미래엔_AI교육_이메일_초안.html"], "estimate"),
    (["projects/미래엔/제안서/proposal_render.html"], "build"),
]


def main() -> int:
    failures: list[str] = []

    for command, expected in BUILD_COMMANDS:
        got = extract_build_target(command)
        if got != expected:
            failures.append(f"extract_build_target({command!r}) = {got}, 기대 {expected}")

    for command in NON_BUILD_COMMANDS:
        got = extract_build_target(command)
        if got != (None, False):
            failures.append(f"오탐: extract_build_target({command!r}) = {got}")

    for paths, expected in COMMAND_INFERENCE:
        got = infer_command(paths)
        if got != expected:
            failures.append(f"infer_command({paths}) = {got!r}, 기대 {expected!r}")

    total = len(BUILD_COMMANDS) + len(NON_BUILD_COMMANDS) + len(COMMAND_INFERENCE)
    if failures:
        print(f"❌ {len(failures)}/{total} 실패")
        for f in failures:
            print(f"   - {f}")
        return 1
    print(f"✅ {total}/{total} 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
