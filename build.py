"""
모두의연구소 AI 교육 제안서 — 통합 빌드 CLI
=============================================
사용법:
    python build.py <기업명>                       # 해당 기업 전체 제안서 빌드
    python build.py <기업명>/<과정명>               # 단일 제안서 빌드
    python build.py --all                         # 전체 프로젝트 빌드

예시:
    python build.py 기웅정보통신
    python build.py 기웅정보통신/전체_교육_로드맵
    python build.py --all
"""

import glob
import json
import os
import shutil
import sys
import subprocess
import argparse

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("❌ jinja2가 설치되지 않았습니다. 아래 명령어로 설치해 주세요:")
    print("   pip install jinja2")
    sys.exit(1)

# ── 경로 설정 ──
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
PROJECTS_DIR = os.path.join(ROOT_DIR, "projects")
CSS_FILE = os.path.join(TEMPLATES_DIR, "base.css")

# ── 버전 관리 ──
sys.path.insert(0, ROOT_DIR)
try:
    from scripts.version_manager import snapshot, print_version_log
except ImportError:
    snapshot = None
    print_version_log = None

# ── Google Drive 업로드 ──
# import 실패를 조용히 넘기면 "PDF는 생겼는데 Drive엔 없다"가 무증상으로 재현되므로
# 실패 사유를 남겨 두었다가 업로드 시점에 출력한다.
try:
    from scripts.drive_upload import upload_company_files
    DRIVE_IMPORT_ERROR = None
except ImportError as e:
    upload_company_files = None
    DRIVE_IMPORT_ERROR = str(e)


def upload_to_drive(company_dir: str, author: str = "시스템", skip_drive: bool = False):
    """빌드 산출물을 Google Drive에 업로드. 실패해도 빌드는 계속 진행한다."""
    if skip_drive:
        print("\n⏭️  Drive 업로드 생략 (--no-drive-upload 또는 CI=true)")
        return
    if upload_company_files is None:
        print(f"\n⚠️  Drive 업로드 불가 — 의존성 미설치: {DRIVE_IMPORT_ERROR}")
        print("   pip install google-auth google-auth-oauthlib google-api-python-client")
        return
    try:
        result = upload_company_files(company_dir, author=author)
        if result:
            print(f"\n📂 Drive: {result['folder_link']}")
    except Exception as e:
        # DriveAuthError(token.json 없음/만료) 포함. 여기서 삼켜야 빌드가 끝까지 진행된다.
        print(f"\n⚠️  Drive 업로드 실패: {e}")


def detect_template_type(data: dict) -> str:
    """content.json의 키를 보고 템플릿 타입을 자동 감지"""
    # type 필드가 명시된 경우 우선 사용
    if data.get("type") == "bootcamp":
        return "bootcamp"
    if data.get("type") == "guide":
        return "guide"
    if data.get("type") == "workshop" or "days" in data:
        return "workshop"
    if "steps" in data:
        return "roadmap"
    elif "tracks" in data:
        return "track"
    elif "seminars" in data:
        return "khp-seminar"
    elif "modules" in data:
        return "module"
    else:
        raise ValueError("content.json 스키마를 인식할 수 없습니다. "
                         "'days', 'steps', 'tracks', 'seminars', 또는 'modules' 키가 필요합니다.")


def render_html(content_json_path: str) -> str:
    """content.json → HTML 렌더링 후 HTML 파일 경로 반환"""
    with open(content_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 글로벌 base.css 로드
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    # 가로(landscape) 오버라이드 — content.json에 "orientation": "landscape" 지정 시
    if data.get("orientation") == "landscape":
        landscape_css_path = os.path.join(TEMPLATES_DIR, "base-landscape.css")
        with open(landscape_css_path, "r", encoding="utf-8") as f:
            css += "\n\n/* ── 가로(A4 Landscape) 오버라이드 ── */\n" + f.read()

    # 프로젝트 단위 base.css 오버라이드 (content.json과 같은 폴더에 있으면追加)
    project_css = os.path.join(os.path.dirname(content_json_path), "base.css")
    if os.path.exists(project_css):
        with open(project_css, "r", encoding="utf-8") as f:
            css += "\n\n/* ── 프로젝트 맞춤 CSS ── */\n" + f.read()

    template_type = detect_template_type(data)
    template_file = f"{template_type}.html"

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=False,  # HTML을 그대로 출력해야 함
    )
    template = env.get_template(template_file)

    # 타입별 추가 CSS 로드 (없으면 빈 문자열)
    extra_css_path = os.path.join(TEMPLATES_DIR, f"{template_type}.css")
    extra_css = ""
    if os.path.exists(extra_css_path):
        with open(extra_css_path, "r", encoding="utf-8") as f:
            extra_css = f.read()

    html = template.render(data=data, css=css, workshop_css=extra_css)

    output_dir = os.path.dirname(content_json_path)
    html_path = os.path.join(output_dir, "proposal_render.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return html_path


def html_to_pdf(html_path: str, pdf_name: str, suffix: str = "_제안서",
                landscape: bool = False) -> str:
    """Chrome/Edge Headless 모드로 HTML → PDF 변환 (Chrome 우선, Edge fallback)"""
    pdf_path = os.path.join(os.path.dirname(html_path), f"{pdf_name}{suffix}.pdf")

    chrome_candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "google-chrome",
        "chromium",
        "chromium-browser",
    ]
    # 컨테이너/CI 환경엔 브라우저가 PATH 대신 Playwright 캐시에만 있는 경우가 많다.
    if os.environ.get("PROPOSAL_CHROME"):
        chrome_candidates.insert(0, os.environ["PROPOSAL_CHROME"])
    pw_root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    chrome_candidates += sorted(
        glob.glob(os.path.join(pw_root, "chromium-*", "chrome-linux", "chrome")), reverse=True
    )
    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "msedge",
    ]

    cmd_browser = None
    for candidate in chrome_candidates + edge_candidates:
        # 실행 파일명만 준 경우엔 PATH에 실제로 있는지 확인한다.
        # (예전엔 존재한다고 가정해서, chromium만 깔린 환경에서 google-chrome을 골라 실행에 실패했다)
        if os.sep in candidate or (os.altsep and os.altsep in candidate):
            found = candidate if os.path.exists(candidate) else None
        else:
            found = shutil.which(candidate)
        if found:
            cmd_browser = found
            break

    if cmd_browser is None:
        print("❌ Chrome 또는 Microsoft Edge를 찾을 수 없습니다.")
        return ""

    # Edge Headless는 @page(size: landscape)를 무시하므로 가로 출력은 Chrome 필수
    if landscape and any(e in cmd_browser.lower() for e in ("edge", "msedge")):
        print("   ⚠️  가로(landscape) 제안서는 Edge에서 @page 설정이 무시되어 세로로 출력됩니다. Chrome 설치를 권장합니다.")

    cmd = [
        cmd_browser,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
    ]
    # 컨테이너에서 root로 돌면 Chrome이 샌드박스를 거부한다. 로컬 사용자 환경은 그대로 둔다.
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        cmd += ["--no-sandbox"]
    cmd += [
        f"--print-to-pdf={os.path.abspath(pdf_path)}",
        f"file://{os.path.abspath(html_path)}",
    ]
    subprocess.run(cmd, check=True)
    return pdf_path


def build_proposal(project_path: str):
    """단일 제안서(content.json이 있는 폴더) 빌드"""
    content_json = os.path.join(project_path, "content.json")
    if not os.path.exists(content_json):
        print(f"⚠️  건너뜀 (content.json 없음): {project_path}")
        return

    folder_name = os.path.basename(project_path)
    print(f"📄 빌드 시작: {folder_name}")

    html_path = render_html(content_json)
    print(f"   ✅ HTML: {html_path}")

    with open(content_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    is_landscape = data.get("orientation") == "landscape"
    try:
        if data.get("pdf_filename"):
            pdf_path = html_to_pdf(html_path, data["pdf_filename"], suffix="",
                                   landscape=is_landscape)
        else:
            suffix = "_교육안내서" if data.get("type") == "guide" else "_제안서"
            pdf_path = html_to_pdf(html_path, folder_name, suffix=suffix,
                                   landscape=is_landscape)
        if pdf_path:
            print(f"   ✅ PDF:  {pdf_path}")
    except Exception as e:
        print(f"   ❌ PDF 생성 실패: {e}")


def build_company(company_name: str, author: str = "시스템", message: str = "",
                  skip_snapshot: bool = False, skip_drive: bool = False):
    """특정 기업의 모든 제안서 빌드.

    Args:
        skip_snapshot: version_manager 로컬 스냅샷 생략 (CI용)
        skip_drive:    Google Drive 업로드 생략 (CI용)
    """
    company_dir = os.path.join(PROJECTS_DIR, company_name)
    if not os.path.isdir(company_dir):
        print(f"❌ 프로젝트를 찾을 수 없습니다: {company_dir}")
        sys.exit(1)

    # 빌드 전 버전 스냅샷
    if snapshot and not skip_snapshot:
        snap = snapshot(company_dir, author=author, description=message or f"/build {company_name}")
        if snap:
            print(f"📦 버전 스냅샷 저장: {os.path.basename(snap)}")

    print(f"\n🏢 [{company_name}] 전체 빌드")
    print("=" * 50)

    for entry in sorted(os.listdir(company_dir)):
        entry_path = os.path.join(company_dir, entry)
        if os.path.isdir(entry_path):
            build_proposal(entry_path)

    print("=" * 50)
    print(f"🎉 [{company_name}] 빌드 완료!")

    # 버전 히스토리 출력
    if print_version_log:
        print_version_log(company_dir)

    # Google Drive 업로드
    upload_to_drive(company_dir, author=author, skip_drive=skip_drive)
    print()


def build_all(author="시스템", message="", skip_snapshot=False, skip_drive=False):
    """전체 프로젝트(모든 기업) 빌드"""
    if not os.path.isdir(PROJECTS_DIR):
        print(f"❌ projects 폴더가 없습니다: {PROJECTS_DIR}")
        sys.exit(1)

    for company in sorted(os.listdir(PROJECTS_DIR)):
        company_path = os.path.join(PROJECTS_DIR, company)
        if os.path.isdir(company_path):
            build_company(company, author=author, message=message,
                          skip_snapshot=skip_snapshot, skip_drive=skip_drive)


def main():
    parser = argparse.ArgumentParser(
        description="모두의연구소 AI 교육 제안서 빌드 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python build.py 기웅정보통신                    기웅정보통신 전체 빌드
  python build.py 기웅정보통신/전체_교육_로드맵     단일 제안서 빌드
  python build.py --all                          모든 프로젝트 빌드
  python build.py 기웅정보통신 --author 영광       작업자 지정
  python build.py 기웅정보통신 --author U0924H9HSK1 -m "2차 수정"
        """,
    )
    parser.add_argument("target", nargs="?", help="<기업명> 또는 <기업명>/<과정명>")
    parser.add_argument("--all", action="store_true", help="전체 프로젝트 빌드")
    parser.add_argument("--author", default="시스템", help="작업자 이름 또는 Slack User ID")
    parser.add_argument("--message", "-m", default="", help="버전 설명")
    parser.add_argument("--no-drive-upload", action="store_true",
                        help="Google Drive 업로드 생략 (CI/로컬 테스트용)")
    parser.add_argument("--no-version-snapshot", action="store_true",
                        help="version_manager 로컬 스냅샷 생략 (CI/로컬 테스트용)")

    args = parser.parse_args()

    # CI=true 환경에서는 부작용(Drive 업로드, 로컬 스냅샷) 자동 억제 — Oracle 아키텍처 권고
    is_ci = os.environ.get("CI", "").lower() in ("1", "true", "yes")
    skip_snapshot = args.no_version_snapshot or is_ci
    skip_drive = args.no_drive_upload or is_ci

    if args.all:
        build_all(author=args.author, message=args.message,
                  skip_snapshot=skip_snapshot, skip_drive=skip_drive)
    elif args.target:
        # "기업명/과정명" 형태인지 체크
        parts = args.target.replace("\\", "/").split("/")
        if len(parts) == 2:
            proposal_path = os.path.join(PROJECTS_DIR, parts[0], parts[1])
            build_proposal(proposal_path)
            # 단일 제안서 빌드도 Drive 업로드까지 마쳐야 한다.
            # (이전에는 이 분기가 업로드를 건너뛰어서 "어떤 땐 올라가고 어떤 땐 안 올라가는"
            #  증상의 주 원인이었다 — build_company 경로에만 업로드가 붙어 있었음)
            upload_to_drive(os.path.join(PROJECTS_DIR, parts[0]),
                            author=args.author, skip_drive=skip_drive)
        elif len(parts) == 1:
            build_company(parts[0], author=args.author, message=args.message,
                          skip_snapshot=skip_snapshot, skip_drive=skip_drive)
        else:
            print("❌ 형식 오류. 사용법: python build.py <기업명> 또는 <기업명>/<과정명>")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
