"""
Google Drive 업로드 스크립트
============================
빌드 완료 후 최종 산출물(PDF, HTML, 견적서 등)을 공유 드라이브에 업로드.

타겟 경로: Biz > 06. 교육 커리큘럼 & 콘텐츠 > 03. 제안서 > {기업명}/

사용법:
    python scripts/drive_upload.py projects/{기업명} --author 영광
    python scripts/drive_upload.py projects/{기업명} --dry-run  # 업로드 없이 경로만 확인
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ── 상수 ──
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(ROOT_DIR, "token.json")

# 공유 드라이브 폴더 ID
BIZ_DRIVE_ID = "0AKys-Jdims1pUk9PVA"
PROPOSAL_FOLDER_ID = "1up5Phh63CbwF2cd0UHD5YGpgTYWi8zCa"  # 03. 제안서

# 업로드할 파일 확장자
UPLOAD_EXTENSIONS = {".pdf", ".html", ".csv"}
UPLOAD_EXTENSIONS_MD = {".md"}  # 견적서 .md 등


class DriveAuthError(RuntimeError):
    """Google Drive 인증 실패. 호출자가 잡아서 처리할 수 있도록 Exception으로 발생시킨다.

    (이전에는 sys.exit(1)을 호출했는데, SystemExit는 Exception을 상속하지 않아
     build.py의 `except Exception` 에 잡히지 않고 빌드 프로세스 전체를 종료시켰다.)
    """


def get_credentials():
    """token.json에서 OAuth credentials 로드 (자동 갱신 포함)"""
    if not os.path.exists(TOKEN_PATH):
        raise DriveAuthError(
            "token.json이 없습니다. Google Drive 인증이 필요합니다. "
            "(python scripts/hooks/check_drive_auth.py --verify 로 상태 확인)"
        )

    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes"),
        # expiry를 넘기지 않으면 creds.expired가 항상 False가 되어(google-auth 구현상
        # expiry is None -> expired False -> valid True) 갱신이 한 번도 일어나지 않는다.
        # access token 수명은 1시간이라, 인증 직후 1시간 안에 빌드하면 성공하고
        # 그 뒤에는 401로 실패하는 산발적 증상의 원인이 된다.
        expiry=_parse_expiry(token_data.get("expiry")),
    )

    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
        _save_credentials(creds, token_data)

    return creds


def _parse_expiry(value):
    """token.json의 expiry 문자열을 naive UTC datetime으로 변환.

    google-auth는 expiry를 tz-naive UTC로 다루므로 tzinfo를 제거해서 넘긴다.
    """
    if not value:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    text = str(value).strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def _save_credentials(creds, token_data: dict) -> None:
    """갱신된 access token을 token.json에 다시 기록 (다음 실행에서 재사용)."""
    token_data["token"] = creds.token
    if creds.expiry:
        token_data["expiry"] = creds.expiry.isoformat() + "Z"
    try:
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            json.dump(token_data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"⚠️  갱신된 토큰 저장 실패(동작에는 영향 없음): {e}")


def get_or_create_folder(service, folder_name, parent_id):
    """부모 폴더 내에 하위 폴더 찾기 또는 생성"""
    # 기존 폴더 검색
    query = (
        f"'{parent_id}' in parents and "
        f"name = '{folder_name}' and "
        f"mimeType = 'application/vnd.google-apps.folder' and "
        f"trashed = false"
    )
    results = service.files().list(
        q=query,
        fields="files(id, name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
        corpora="drive",
        driveId=BIZ_DRIVE_ID,
    ).execute()

    folders = results.get("files", [])
    if folders:
        return folders[0]["id"], False  # existing

    # 폴더 생성
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = service.files().create(
        body=file_metadata,
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return folder["id"], True  # created


def upload_file(service, file_path, folder_id, overwrite=True):
    """파일을 Google Drive에 업로드"""
    filename = os.path.basename(file_path)

    # 기존 파일 확인 (덮어쓰기)
    existing_id = None
    if overwrite:
        query = (
            f"'{folder_id}' in parents and "
            f"name = '{filename}' and "
            f"trashed = false"
        )
        results = service.files().list(
            q=query,
            fields="files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            corpora="drive",
            driveId=BIZ_DRIVE_ID,
        ).execute()
        existing = results.get("files", [])
        if existing:
            existing_id = existing[0]["id"]

    media = MediaFileUpload(file_path, resumable=True)

    if existing_id:
        # 기존 파일 업데이트 (새 버전)
        file = service.files().update(
            fileId=existing_id,
            media_body=media,
            fields="id, name, webViewLink",
            supportsAllDrives=True,
        ).execute()
        action = "업데이트"
    else:
        # 새 파일 업로드
        file_metadata = {
            "name": filename,
            "parents": [folder_id],
        }
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name, webViewLink",
            supportsAllDrives=True,
        ).execute()
        action = "업로드"

    return file, action


def collect_upload_files(company_dir):
    """업로드할 파일 목록 수집"""
    files = []
    company_name = os.path.basename(company_dir)

    for root, dirs, filenames in os.walk(company_dir):
        # versions/ 폴더 건너뛰기
        rel_root = os.path.relpath(root, company_dir)
        if rel_root.startswith("versions") or rel_root == "versions":
            continue
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            # PDF, HTML, CSV는 항상 업로드
            if ext in UPLOAD_EXTENSIONS:
                files.append(os.path.join(root, fn))
            # 루트 레벨 .md 중 견적서, 요구조건만
            elif ext in UPLOAD_EXTENSIONS_MD and rel_root == ".":
                if any(kw in fn for kw in ["견적서", "이메일", "요구조건"]):
                    files.append(os.path.join(root, fn))

    return files


def upload_company_files(company_dir, author="시스템", dry_run=False):
    """기업 산출물을 Google Drive에 업로드"""
    company_name = os.path.basename(company_dir)
    if not os.path.isdir(company_dir):
        print(f"❌ 디렉토리 없음: {company_dir}")
        return None

    # 업로드 대상 파일 수집
    upload_files = collect_upload_files(company_dir)
    if not upload_files:
        print(f"⚠️  업로드할 파일 없음: {company_name}")
        return None

    print(f"📤 Google Drive 업로드: {company_name}")
    print(f"   타겟: Biz > 06. 교육 커리큘럼 & 콘텐츠 > 03. 제안서 > {company_name}/")
    print(f"   파일 {len(upload_files)}개:")

    for f in upload_files:
        rel = os.path.relpath(f, company_dir)
        print(f"     - {rel}")

    if dry_run:
        print("   (dry-run: 실제 업로드 없음)")
        return None

    # Google Drive 인증
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    # 기업명 폴더 생성/확인
    folder_id, created = get_or_create_folder(service, company_name, PROPOSAL_FOLDER_ID)
    if created:
        print(f"   📁 폴더 생성: {company_name}/")
    else:
        print(f"   📁 기존 폴더 사용: {company_name}/")

    # 파일 업로드
    folder_link = f"https://drive.google.com/drive/folders/{folder_id}"
    uploaded = []
    for file_path in upload_files:
        rel = os.path.relpath(file_path, company_dir)
        try:
            # 하위 폴더 구조 유지 (예: 제안서/*.pdf)
            parts = Path(rel).parts
            if len(parts) > 1:
                # 하위 폴더 생성
                current_parent = folder_id
                for part in parts[:-1]:
                    current_parent, _ = get_or_create_folder(service, part, current_parent)
                target_folder = current_parent
            else:
                target_folder = folder_id

            result, action = upload_file(service, file_path, target_folder)
            link = result.get("webViewLink", "")
            print(f"   ✅ {action}: {os.path.basename(file_path)}")
            uploaded.append({"name": os.path.basename(file_path), "action": action, "link": link})
        except Exception as e:
            print(f"   ❌ 실패: {os.path.basename(file_path)} — {e}")

    print(f"\n   📂 Drive 폴더: {folder_link}")
    return {"folder_link": folder_link, "folder_id": folder_id, "uploaded": uploaded}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Drive 산출물 업로드")
    parser.add_argument("company_dir", help="기업 프로젝트 디렉토리 경로")
    parser.add_argument("--author", default="시스템", help="작업자명")
    parser.add_argument("--dry-run", action="store_true", help="실제 업로드 없이 경로만 확인")

    args = parser.parse_args()
    try:
        result = upload_company_files(args.company_dir, author=args.author, dry_run=args.dry_run)
    except DriveAuthError as e:
        print(f"❌ {e}")
        sys.exit(1)
    if result:
        print(f"\n🔗 공유 링크: {result['folder_link']}")
