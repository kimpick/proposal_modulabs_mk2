#!/usr/bin/env python3
"""도구(scripts/·templates/·schemas/·build.py) 변경에 대한 회귀 스모크 테스트.

validate-pr.yml 의 기업별 검증은 PR 에 `projects/**` 변경이 있을 때만 돌아간다.
그래서 `scripts/validate_content.py` 처럼 전체 콘텐츠에 영향을 주는 변경이
정작 무검증으로 통과하는 구멍이 있었다. 이 스크립트가 그 구멍을 메운다.

검사하는 것은 **도구가 동작하는지**다. 콘텐츠 품질은 보지 않는다.
기존 content.json 상당수가 이미 NEEDS_FIX 이므로(강사 실명 미마스킹 등)
전수 PASS 를 게이트로 걸면 CI 가 영구 red 가 된다. 따라서:

- validate_content.py: --json 출력이 정상 파싱되면 통과. NEEDS_FIX 판정은
  콘텐츠 사정이므로 실패로 보지 않는다. 크래시·빈 결과·JSON 깨짐은 실패.
- build.render_html: 전건 렌더해서 예외가 없으면 통과. PDF 는 CI 에 Chrome 이
  없어 대상에서 제외한다(원래 워크플로우와 동일).

사용:
    python scripts/ci_smoke.py              # projects/ 전체
    python scripts/ci_smoke.py --limit 20   # 앞 20건만 (빠른 로컬 확인)
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def find_content_files(projects_dir: Path, limit: int | None) -> list[Path]:
    paths = sorted(projects_dir.rglob("content.json"))
    return paths[:limit] if limit else paths


def tracked_render_outputs() -> dict[Path, bytes]:
    """추적 중인 proposal_render.html 을 백업한다.

    렌더는 content.json 옆에 proposal_render.html 을 덮어쓴다. 대부분 gitignore
    대상이지만 화이트리스트로 추적되는 파일이 있어, 로컬 실행이 작업 트리를
    더럽히지 않도록 내용을 보관해 두고 나중에 복원한다.
    """
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "*proposal_render.html"],
            cwd=REPO_ROOT, capture_output=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    saved = {}
    for name in out.split(b"\0"):
        if not name:
            continue
        path = REPO_ROOT / os.fsdecode(name)
        if path.is_file():
            saved[path] = path.read_bytes()
    return saved


def check_validate(paths: list[Path], expect_all: bool) -> bool:
    """validate_content.py 를 CLI 로 돌려 크래시 없이 JSON 을 내는지 본다.

    expect_all 이면 결과 건수가 실제 content.json 수와 일치해야 한다.
    resolve_content_paths() 가 파일을 조용히 빠뜨리는 회귀를 잡기 위한 것이다.
    """
    print("━━━ 1/2 validate_content.py ━━━")
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [sys.executable, "scripts/validate_content.py", "projects", "--json"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", env=env,
    )
    # exit 1 은 NEEDS_FIX 판정이라 정상. exit 2 이상은 도구 오류.
    if proc.returncode >= 2:
        print(f"❌ 종료 코드 {proc.returncode} (도구 오류)")
        print(proc.stderr[-2000:])
        return False
    try:
        results = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        print(f"❌ --json 출력을 파싱할 수 없습니다: {exc}")
        print("stdout 앞부분:", proc.stdout[:500])
        print("stderr 끝부분:", proc.stderr[-1000:])
        return False
    if not results:
        print("❌ 결과가 비어 있습니다. content.json 을 하나도 찾지 못했습니다.")
        return False
    counts = collections.Counter(r["verdict"] for r in results)
    print(f"✅ {len(results)}건 검증 실행 (크래시 없음)")
    for verdict, n in sorted(counts.items()):
        print(f"     {verdict}: {n}")
    missing = [r["path"] for r in results if "verdict" not in r]
    if missing:
        print(f"❌ verdict 누락: {missing[:5]}")
        return False
    if expect_all and len(results) != len(paths):
        print(
            f"❌ 대상 {len(paths)}건 중 {len(results)}건만 검증됐습니다. "
            "resolve_content_paths() 가 파일을 빠뜨리고 있습니다."
        )
        return False
    return True


def check_render(paths: list[Path]) -> bool:
    """build.render_html 이 전건에서 예외 없이 도는지 본다."""
    print("━━━ 2/2 build.render_html ━━━")
    sys.path.insert(0, str(REPO_ROOT))
    try:
        from build import render_html
    except Exception as exc:
        print(f"❌ build.py 를 import 할 수 없습니다: {type(exc).__name__}: {exc}")
        return False

    saved = tracked_render_outputs()
    failures: list[str] = []
    try:
        for path in paths:
            try:
                render_html(str(path))
            except Exception as exc:
                rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
                failures.append(f"{rel}: {type(exc).__name__}: {exc}")
    finally:
        for path, blob in saved.items():
            path.write_bytes(blob)

    if failures:
        print(f"❌ {len(paths)}건 중 {len(failures)}건 렌더 실패")
        for line in failures[:20]:
            print(f"     {line}")
        if len(failures) > 20:
            print(f"     ... 외 {len(failures) - 20}건")
        return False
    print(f"✅ {len(paths)}건 렌더 성공")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--limit", type=int, default=None,
        help="렌더 검사를 앞 N건으로 제한 (로컬에서 빠르게 확인할 때). "
             "validate 검사는 CLI 가 대상을 스스로 해석하므로 항상 전건이다.",
    )
    args = parser.parse_args()

    projects_dir = REPO_ROOT / "projects"
    if not projects_dir.is_dir():
        print(f"projects/ 가 없어 스모크 테스트를 건너뜁니다: {projects_dir}")
        return 0

    paths = find_content_files(projects_dir, args.limit)
    if not paths:
        print("content.json 을 찾지 못해 스모크 테스트를 건너뜁니다.")
        return 0

    print(f"대상 content.json: {len(paths)}건\n")
    ok = check_validate(paths, expect_all=args.limit is None)
    print()
    ok = check_render(paths) and ok

    print()
    if ok:
        print("스모크 테스트 통과 — 도구 회귀 없음")
        return 0
    print("스모크 테스트 실패 — 도구가 깨졌습니다")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
