"""
버전 관리 매니저
================
빌드/수정 전 현재 산출물을 버전 디렉토리에 스냅샷으로 저장.

버전 형식: v{NNN}_{작업자}_{YYYYMMDD}_{HHMM}
예: v001_영광_20260609_1430

사용법:
    from scripts.version_manager import snapshot, list_versions
    snapshot("projects/삼성전자", author="영광", description="/build 실행")
    versions = list_versions("projects/삼성전자")
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

# Slack User ID → 이름 매핑
USER_MAP = {
    "U0924H9HSK1": "영광",
    "U03RP0HEZDW": "은숙",
    "U093RP4EZMK": "은경",
}

# 버전에 포함할 파일 패턴 (산출물만)
VERSION_INCLUDE_PATTERNS = [
    "제안서",                            # 제안서/ 폴더 전체
]
VERSION_INCLUDE_EXTENSIONS = [
    ".md", ".csv", ".html",              # 견적서 등 루트 산출물
]
# 제외할 파일명
VERSION_EXCLUDE_NAMES = {
    "요구조건.md",
}
VERSION_EXCLUDE_PREFIXES = [
    "리서치_",
]


def resolve_author(author_input: str) -> str:
    """Slack User ID 또는 이름을 표시 이름으로 변환"""
    return USER_MAP.get(author_input, author_input)


def _get_next_version_number(versions_dir: str) -> int:
    """다음 버전 번호 반환 (v001 → 1, v002 → 2...)"""
    if not os.path.exists(versions_dir):
        return 1
    existing = []
    for d in os.listdir(versions_dir):
        m = re.match(r"v(\d+)_", d)
        if m:
            existing.append(int(m.group(1)))
    return max(existing, default=0) + 1


def _should_include_file(filename: str, relpath: str, company_dir: str) -> bool:
    """버전에 포함할 파일인지 판단"""
    # 제외 파일명
    if filename in VERSION_EXCLUDE_NAMES:
        return False
    # 제외 접두사
    for prefix in VERSION_EXCLUDE_PREFIXES:
        if filename.startswith(prefix):
            return False
    # 숨김/임시 파일 제외
    if filename.startswith(".") or filename.startswith("~"):
        return False

    parts = Path(relpath).parts

    # content.json이 있는 서브폴더 = 제안서 폴더 → 전체 포함
    if len(parts) >= 2:
        subfolder = os.path.join(company_dir, parts[0])
        if os.path.isdir(subfolder) and os.path.exists(os.path.join(subfolder, "content.json")):
            return True

    # "제안서"라는 이름의 폴더 안의 파일도 포함
    if "제안서" in parts:
        return True

    # 루트 레벨 산출물 (확장자 기준)
    if len(parts) == 1:
        ext = os.path.splitext(filename)[1]
        if ext in VERSION_INCLUDE_EXTENSIONS:
            return True
    return False


def snapshot(company_dir: str, author: str = "시스템",
             description: Optional[str] = None) -> Optional[str]:
    """
    현재 산출물을 버전 디렉토리에 스냅샷 저장.

    Args:
        company_dir: 기업 프로젝트 디렉토리 경로
        author: 작업자 이름 또는 Slack User ID
        description: 버전 설명 (선택)

    Returns:
        생성된 버전 디렉토리 경로, 또는 스냅샷할 파일이 없으면 None
    """
    author = resolve_author(author)
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M")

    # 수집할 파일 목록
    files_to_snapshot = []
    for root, dirs, files in os.walk(company_dir):
        # versions/ 폴더는 건너뜀
        rel_root = os.path.relpath(root, company_dir)
        if rel_root.startswith("versions") or rel_root == "versions":
            continue
        # .claude, .git 등 숨김 폴더 건너뜀
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for f in files:
            relpath = os.path.join(rel_root, f) if rel_root != "." else f
            if _should_include_file(f, relpath, company_dir):
                full_path = os.path.join(root, f)
                files_to_snapshot.append((full_path, relpath))

    # 스냅샷할 파일이 없으면 스킵
    if not files_to_snapshot:
        return None

    # 버전 디렉토리 생성
    versions_dir = os.path.join(company_dir, "versions")
    os.makedirs(versions_dir, exist_ok=True)

    ver_num = _get_next_version_number(versions_dir)
    ver_name = f"v{ver_num:03d}_{author}_{date_str}_{time_str}"
    ver_dir = os.path.join(versions_dir, ver_name)
    os.makedirs(ver_dir, exist_ok=True)

    # 파일 복사
    copied_files = []
    for full_path, relpath in files_to_snapshot:
        dest = os.path.join(ver_dir, relpath)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(full_path, dest)
        copied_files.append(relpath)

    # 메타데이터 저장
    meta = {
        "version": ver_name,
        "number": ver_num,
        "author": author,
        "timestamp": now.isoformat(),
        "description": description or "",
        "files": sorted(copied_files),
    }
    meta_path = os.path.join(ver_dir, "meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return ver_dir


def list_versions(company_dir: str) -> list:
    """
    버전 목록 반환 (최신순).

    Returns:
        list of dict: [{version, number, author, timestamp, description, files}, ...]
    """
    versions_dir = os.path.join(company_dir, "versions")
    if not os.path.exists(versions_dir):
        return []

    versions = []
    for d in sorted(os.listdir(versions_dir)):
        meta_path = os.path.join(versions_dir, d, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            versions.append(meta)

    return sorted(versions, key=lambda x: x.get("number", 0), reverse=True)


def get_latest_version(company_dir: str) -> Optional[dict]:
    """최신 버전 정보 반환"""
    versions = list_versions(company_dir)
    return versions[0] if versions else None


def print_version_log(company_dir: str):
    """버전 히스토리 출력"""
    versions = list_versions(company_dir)
    if not versions:
        print("   📋 버전 히스토리 없음")
        return
    print(f"   📋 버전 히스토리 ({len(versions)}개)")
    for v in versions:
        ts = v.get("timestamp", "")[:16].replace("T", " ")
        desc = f" — {v['description']}" if v.get("description") else ""
        print(f"      {v['version']}  ({len(v.get('files', []))}개 파일){desc}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python version_manager.py <command> <company_dir> [author] [description]")
        print("Commands: snapshot, list, latest")
        sys.exit(1)

    cmd = sys.argv[1]
    target = sys.argv[2]

    if cmd == "snapshot":
        author = sys.argv[3] if len(sys.argv) > 3 else "시스템"
        desc = sys.argv[4] if len(sys.argv) > 4 else None
        result = snapshot(target, author=author, description=desc)
        if result:
            print(f"✅ 스냅샷 생성: {os.path.basename(result)}")
        else:
            print("⏭️  스냅샷 스킵 (기존 산출물 없음)")
    elif cmd == "list":
        for v in list_versions(target):
            ts = v.get("timestamp", "")[:16].replace("T", " ")
            print(f"  {v['version']}  {ts}  ({len(v.get('files', []))}개 파일)")
    elif cmd == "latest":
        v = get_latest_version(target)
        if v:
            print(json.dumps(v, ensure_ascii=False, indent=2))
        else:
            print("버전 없음")
