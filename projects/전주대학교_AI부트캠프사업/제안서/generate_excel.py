"""
엑셀 제안서 생성 스크립트
content.json 을 읽어서 5개 탭의 엑셀 파일을 자동 생성합니다.

Usage:
    python generate_excel.py
"""
import json
import os
import re
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
CONTENT_JSON = SCRIPT_DIR / "content.json"
OUTPUT_XLSX  = SCRIPT_DIR / "모두의연구소_전주대 AI 부트캠프 교육과정 제안.xlsx"

# ── style presets ────────────────────────────────────────────────────────
NAVY   = "1B2A4A"
BLUE   = "2D5DA1"
TEAL   = "17A2B8"
GREEN  = "28A745"
ORANGE = "E67E22"
GRAY   = "6C757D"
LIGHT_BLUE  = "D6EAF8"
LIGHT_GREEN = "D5F5E3"
LIGHT_ORANGE = "FDEBD0"
WHITE  = "FFFFFF"
LIGHT_GRAY   = "F2F3F4"

FONT_TITLE   = Font(name="맑은 고딕", size=16, bold=True, color=WHITE)
FONT_SUBTITLE = Font(name="맑은 고딕", size=13, bold=True, color=WHITE)
FONT_SECTION = Font(name="맑은 고딕", size=12, bold=True, color=NAVY)
FONT_HEADER  = Font(name="맑은 고딕", size=10, bold=True, color=WHITE)
FONT_BODY    = Font(name="맑은 고딕", size=10)
FONT_BODY_BOLD = Font(name="맑은 고딕", size=10, bold=True)
FONT_SMALL   = Font(name="맑은 고딕", size=9, color=GRAY)

FILL_NAVY   = PatternFill("solid", fgColor=NAVY)
FILL_BLUE   = PatternFill("solid", fgColor=BLUE)
FILL_TEAL   = PatternFill("solid", fgColor=TEAL)
FILL_GREEN  = PatternFill("solid", fgColor=GREEN)
FILL_ORANGE = PatternFill("solid", fgColor=ORANGE)
FILL_LIGHT_BLUE   = PatternFill("solid", fgColor=LIGHT_BLUE)
FILL_LIGHT_GREEN  = PatternFill("solid", fgColor=LIGHT_GREEN)
FILL_LIGHT_ORANGE = PatternFill("solid", fgColor=LIGHT_ORANGE)
FILL_LIGHT_GRAY   = PatternFill("solid", fgColor=LIGHT_GRAY)
FILL_WHITE  = PatternFill("solid", fgColor=WHITE)

ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT   = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_TOP    = Alignment(horizontal="left", vertical="top", wrap_text=True)

THIN_BORDER = Border(
    left=Side(style="thin", color="D5D8DC"),
    right=Side(style="thin", color="D5D8DC"),
    top=Side(style="thin", color="D5D8DC"),
    bottom=Side(style="thin", color="D5D8DC"),
)

TRACK_COLORS = {
    "ND1": {"header_fill": FILL_BLUE,   "row_fill": FILL_LIGHT_BLUE},
    "ND2": {"header_fill": FILL_TEAL,   "row_fill": FILL_LIGHT_GREEN},
    "ND5": {"header_fill": FILL_ORANGE, "row_fill": FILL_LIGHT_ORANGE},
}


def strip_html(text: str) -> str:
    """Remove HTML tags from text."""
    if not text:
        return ""
    text = text.replace("\\n", "\n")
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def set_cell(ws, row, col, value, font=FONT_BODY, fill=None, alignment=ALIGN_LEFT, border=THIN_BORDER):
    cell = ws.cell(row=row, column=col, value=value)
    cell.font = font
    if fill:
        cell.fill = fill
    cell.alignment = alignment
    cell.border = border
    return cell


def merge_and_set(ws, row1, col1, row2, col2, value, font=FONT_BODY, fill=None, alignment=ALIGN_CENTER):
    ws.merge_cells(start_row=row1, start_column=col1, end_row=row2, end_column=col2)
    cell = ws.cell(row=row1, column=col1, value=value)
    cell.font = font
    if fill:
        cell.fill = fill
    cell.alignment = alignment
    cell.border = THIN_BORDER
    # Apply border to all merged cells
    for r in range(row1, row2 + 1):
        for c in range(col1, col2 + 1):
            ws.cell(row=r, column=c).border = THIN_BORDER
            if fill:
                ws.cell(row=r, column=c).fill = fill


# ══════════════════════════════════════════════════════════════════════════
# TAB 1: 제안 개요
# ══════════════════════════════════════════════════════════════════════════
def build_tab1_overview(wb, data):
    ws = wb.active
    ws.title = "제안 개요"
    ws.sheet_properties.tabColor = NAVY

    # Column widths
    for col, w in [(1, 22), (2, 18), (3, 18), (4, 18), (5, 18), (6, 18)]:
        ws.column_dimensions[get_column_letter(col)].width = w

    r = 1
    # Title
    merge_and_set(ws, r, 1, r, 6, data["title"], FONT_TITLE, FILL_NAVY, ALIGN_CENTER)
    r += 1
    merge_and_set(ws, r, 1, r, 6, data["subtitle"], FONT_SUBTITLE, FILL_BLUE, ALIGN_CENTER)
    ws.row_dimensions[r].height = 40

    # Overview section
    r += 1
    set_cell(ws, r, 1, "제안 개요", FONT_SECTION, FILL_LIGHT_GRAY, ALIGN_CENTER)
    merge_and_set(ws, r, 2, r, 6, strip_html(data["intro"]), FONT_BODY, FILL_WHITE, ALIGN_TOP)
    ws.row_dimensions[r].height = 120

    # Education objectives
    r += 1
    merge_and_set(ws, r, 1, r, 6, "교육 목표", FONT_SECTION, FILL_LIGHT_GRAY, ALIGN_CENTER)

    r += 1
    set_cell(ws, r, 1, "ND1 (중급)", FONT_BODY_BOLD, FILL_LIGHT_BLUE)
    merge_and_set(ws, r, 2, r, 6,
                  "피지컬 AI의 뼈대: LLM·로봇·시뮬레이션의 원리를 이해하고 오픈소스 생태계(HuggingFace, ROS2, Isaac/MuJoCo)를 활용하여 통합적으로 체득 (역량 인증 Lv3 목표)",
                  FONT_BODY, FILL_WHITE, ALIGN_LEFT)
    ws.row_dimensions[r].height = 35

    r += 1
    set_cell(ws, r, 1, "ND2 (중급)", FONT_BODY_BOLD, FILL_LIGHT_GREEN)
    merge_and_set(ws, r, 2, r, 6,
                  "합성 데이터/멀티모달: PC 시뮬레이션으로 합성 데이터를 구축하고, 경량 VLM 실습과 하이엔드 AI 사례 분석을 통해 Sim2Real 설계 역량 확보 (역량 인증 Lv3 목표)",
                  FONT_BODY, FILL_WHITE, ALIGN_LEFT)
    ws.row_dimensions[r].height = 35

    r += 1
    set_cell(ws, r, 1, "ND5 (고급)", FONT_BODY_BOLD, FILL_LIGHT_ORANGE)
    merge_and_set(ws, r, 2, r, 6,
                  "로보틱스 LLM 에이전트: Prompt → VLM → 에이전트 플래닝 → LLM-로봇 통합 순차 심화 → 기업 실무 수준 포트폴리오 완성 (역량 인증 Lv4 목표)",
                  FONT_BODY, FILL_WHITE, ALIGN_LEFT)
    ws.row_dimensions[r].height = 35

    # Competency levels
    r += 2
    merge_and_set(ws, r, 1, r, 2, "역량 레벨 정의", FONT_SECTION, FILL_LIGHT_GRAY, ALIGN_CENTER)
    set_cell(ws, r, 3, "역량 수준", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)
    r += 1
    set_cell(ws, r, 1, "레벨", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)
    set_cell(ws, r, 2, "역량 수준", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)
    set_cell(ws, r, 3, "도달 시점", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

    levels = [
        ("Lv1", "AI 관심 단계", "입문 전"),
        ("Lv2", "입문 단계 (기본 코딩·도구 활용)", "AI 기초 수강 중"),
        ("Lv3", "기초 소양 완성 (LLM 원리 이해, 로봇/시뮬레이션 맥락 파악)", "ND1/ND2 수료"),
        ("Lv4", "실무 완성 (E2E LLM-로봇 시스템 구축, 기업 채용 연계 포트폴리오)", "ND5 수료"),
    ]
    for lv, desc, timing in levels:
        r += 1
        set_cell(ws, r, 1, lv, FONT_BODY_BOLD, FILL_WHITE, ALIGN_CENTER)
        set_cell(ws, r, 2, desc, FONT_BODY, FILL_WHITE, ALIGN_LEFT)
        set_cell(ws, r, 3, timing, FONT_BODY, FILL_WHITE, ALIGN_CENTER)

    # Infrastructure
    r += 2
    merge_and_set(ws, r, 1, r, 3, "교육 인프라", FONT_SECTION, FILL_LIGHT_GRAY, ALIGN_CENTER)
    r += 1
    set_cell(ws, r, 1, "구분", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)
    merge_and_set(ws, r, 2, r, 3, "설명", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

    infra_items = [
        ("GPU 기반 AI 클라우드", "모델 추론 및 서빙 실습 환경"),
        ("LLM 서빙 플랫폼", "RAG 파이프라인 · 에이전트 런타임"),
        ("MLOps-DevOps 환경", "실험 이력 관리 · 재현성 보장"),
        ("AI LMS / 문제은행", "전 과정 학습 지원"),
        ("물리 시뮬레이션 클러스터", "MuJoCo · Isaac Sim 실습 환경"),
    ]
    for label, desc in infra_items:
        r += 1
        set_cell(ws, r, 1, label, FONT_BODY_BOLD, FILL_WHITE, ALIGN_LEFT)
        merge_and_set(ws, r, 2, r, 3, desc, FONT_BODY, FILL_WHITE, ALIGN_LEFT)


# ══════════════════════════════════════════════════════════════════════════
# TAB 2: 커리큘럼_개요
# ══════════════════════════════════════════════════════════════════════════
def build_tab2_curriculum_overview(wb, data):
    ws = wb.create_sheet("커리큘럼_개요")
    ws.sheet_properties.tabColor = BLUE

    for col, w in [(1, 8), (2, 35), (3, 8), (4, 50), (5, 35), (6, 40)]:
        ws.column_dimensions[get_column_letter(col)].width = w

    r = 1
    merge_and_set(ws, r, 1, r, 6, "커리큘럼 개요", FONT_TITLE, FILL_NAVY, ALIGN_CENTER)

    for track in data["tracks"]:
        tid = track["track_id"]
        colors = TRACK_COLORS[tid]

        r += 1
        merge_and_set(ws, r, 1, r, 6, track["track_name"], FONT_SUBTITLE, colors["header_fill"], ALIGN_CENTER)
        ws.row_dimensions[r].height = 30

        r += 1
        headers = ["No.", "과목", "시간", "이론/실습 구성", "키워드", "산출물/학습목표"]
        for ci, h in enumerate(headers, 1):
            set_cell(ws, r, ci, h, FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

        for mod in track["modules"]:
            r += 1
            # Extract module number like M1, M7, etc.
            mod_num = mod["module_name"].split(".")[0] if "." in mod["module_name"] else mod["module_name"]

            # Calculate theory/practice breakdown
            theory_hours = 0
            practice_hours = 0
            keywords = []
            for item in mod["items"]:
                h_val = int(item["hours"].replace("H", ""))
                if item["method"] == "이론/사례":
                    theory_hours += h_val
                else:
                    practice_hours += h_val

            # Build composition string
            composition_parts = []
            if theory_hours:
                composition_parts.append(f"이론/사례 {theory_hours}H")
            if practice_hours:
                composition_parts.append(f"실습/심화 {practice_hours}H")
            composition = " + ".join(composition_parts)

            # Short summary of items
            item_summaries = [it["detail"][:30] + "…" for it in mod["items"]]
            composition_detail = f"{composition}\n({', '.join(item_summaries)})"

            # Build keyword from detail text
            detail_text = " ".join([it["detail"] for it in mod["items"]])

            # Get output/objective from items or module info
            output_text = ""
            for item in mod["items"]:
                if item["method"] == "캡스톤":
                    output_text = item["detail"][:60]
                    break
            if not output_text:
                output_text = mod["items"][-1]["detail"][:60]

            set_cell(ws, r, 1, mod_num, FONT_BODY_BOLD, colors["row_fill"], ALIGN_CENTER)
            set_cell(ws, r, 2, mod["module_name"], FONT_BODY, colors["row_fill"], ALIGN_LEFT)
            set_cell(ws, r, 3, mod["duration"], FONT_BODY, colors["row_fill"], ALIGN_CENTER)
            set_cell(ws, r, 4, composition_detail, FONT_SMALL, colors["row_fill"], ALIGN_TOP)
            set_cell(ws, r, 5, detail_text[:80] + "…" if len(detail_text) > 80 else detail_text, FONT_SMALL, colors["row_fill"], ALIGN_TOP)
            set_cell(ws, r, 6, output_text, FONT_BODY, colors["row_fill"], ALIGN_TOP)
            ws.row_dimensions[r].height = 55


# ══════════════════════════════════════════════════════════════════════════
# TAB 3: 커리큘럼_상세
# ══════════════════════════════════════════════════════════════════════════
def build_tab3_curriculum_detail(wb, data):
    ws = wb.create_sheet("커리큘럼_상세")
    ws.sheet_properties.tabColor = TEAL

    for col, w in [(1, 12), (2, 8), (3, 90)]:
        ws.column_dimensions[get_column_letter(col)].width = w

    r = 1
    merge_and_set(ws, r, 1, r, 3, "커리큘럼 상세", FONT_TITLE, FILL_NAVY, ALIGN_CENTER)

    for track in data["tracks"]:
        tid = track["track_id"]
        colors = TRACK_COLORS[tid]

        r += 2
        merge_and_set(ws, r, 1, r, 3, track["track_name"], FONT_SUBTITLE, colors["header_fill"], ALIGN_CENTER)
        ws.row_dimensions[r].height = 30

        for mod in track["modules"]:
            r += 1
            merge_and_set(ws, r, 1, r, 3,
                          f"{mod['module_name']} ({mod['duration']})",
                          FONT_SECTION, FILL_LIGHT_GRAY, ALIGN_LEFT)

            # Learning objective / output row
            r += 1
            has_capstone = any(it["method"] == "캡스톤" for it in mod["items"])
            label = "산출물" if has_capstone else "학습목표"
            obj_text = ""
            for item in mod["items"]:
                if item["method"] == "캡스톤":
                    obj_text = item["detail"]
                    break
            if not obj_text:
                obj_text = mod["items"][-1]["detail"]

            merge_and_set(ws, r, 1, r, 2, label, FONT_BODY_BOLD, FILL_WHITE, ALIGN_CENTER)
            set_cell(ws, r, 3, obj_text, FONT_BODY, FILL_WHITE, ALIGN_LEFT)

            # Detail header
            r += 1
            set_cell(ws, r, 1, "구분", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)
            set_cell(ws, r, 2, "시간", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)
            set_cell(ws, r, 3, "내용", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

            # Detail items
            for item in mod["items"]:
                r += 1
                set_cell(ws, r, 1, item["method"], FONT_BODY, colors["row_fill"], ALIGN_CENTER)
                set_cell(ws, r, 2, item["hours"], FONT_BODY, colors["row_fill"], ALIGN_CENTER)
                set_cell(ws, r, 3, item["detail"], FONT_BODY, FILL_WHITE, ALIGN_TOP)
                ws.row_dimensions[r].height = 35

        # Track total
        r += 1
        total_hours = sum(
            int(item["hours"].replace("H", ""))
            for mod in track["modules"]
            for item in mod["items"]
        )
        theory_h = sum(
            int(item["hours"].replace("H", ""))
            for mod in track["modules"]
            for item in mod["items"]
            if item["method"] == "이론/사례"
        )
        practice_h = total_hours - theory_h
        merge_and_set(ws, r, 1, r, 3,
                      f"{tid} 과정 총계: 이론/사례 {theory_h}H + 실습/심화/캡스톤 {practice_h}H = {total_hours}H",
                      FONT_BODY_BOLD, FILL_LIGHT_GRAY, ALIGN_CENTER)


# ══════════════════════════════════════════════════════════════════════════
# TAB 4: 기술스택
# ══════════════════════════════════════════════════════════════════════════
def build_tab4_tech_stack(wb, data):
    ws = wb.create_sheet("기술스택")
    ws.sheet_properties.tabColor = GREEN

    for col, w in [(1, 22), (2, 35), (3, 50), (4, 15)]:
        ws.column_dimensions[get_column_letter(col)].width = w

    r = 1
    merge_and_set(ws, r, 1, r, 4, "기술 스택 및 도구", FONT_TITLE, FILL_NAVY, ALIGN_CENTER)

    r += 1
    for ci, h in enumerate(["분류", "기술/도구", "용도", "과정"], 1):
        set_cell(ws, r, ci, h, FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

    # Build tech stack from content.json data
    tech_items = [
        ("프로그래밍", "Python · PyTorch", "딥러닝 및 모델 개발", "공통"),
        ("LLM 프레임워크", "Hugging Face (Transformers)", "모델 로드/추론/파인튜닝/임베딩", "ND1, ND5"),
        ("LLM API", "OpenAI API (GPT-4o)", "LLM 호출 및 응용", "공통"),
        ("LLM 오케스트레이션", "LangChain / LlamaIndex / LangGraph", "에이전트/RAG 파이프라인", "ND5"),
        ("벡터 DB", "FAISS, ChromaDB", "RAG 문서 인덱싱/검색", "ND5"),
        ("멀티모달 AI", "Florence-2 / Qwen3-VL-3B", "경량 VLM 추론 (교육용)", "ND2"),
        ("멀티모달 AI", "LLaVA, GPT-4o", "VLM 시각 이해/VQA", "ND5"),
        ("객체 탐지", "Ultralytics (YOLO11)", "합성 데이터 기반 객체 탐지 파인튜닝", "ND2"),
        ("객체 탐지", "Grounding DINO", "자연어 기반 객체 Grounding", "ND5"),
        ("3D Pose", "FoundationPose (6D Pose) / OpenVLA", "제로샷 6D Pose 추정 (사례)", "ND2, ND5"),
        ("로보틱스", "ROS2 (Humble)", "로봇 통신/제어", "ND1, ND5"),
        ("로보틱스", "LeRobot", "사전학습 모방학습 정책 모델", "ND5"),
        ("시뮬레이션", "NVIDIA Isaac Sim 6.0", "디지털 트윈, 합성 데이터 렌더링", "ND1, ND2"),
        ("시뮬레이션", "MuJoCo", "물리 시뮬레이션 환경", "ND1, ND5"),
        ("MLOps", "MLflow / W&B", "실험 추적/에이전트 트레이싱/평가", "ND5"),
        ("LLM 서빙", "vLLM", "고속 LLM 추론 서빙 (PagedAttention)", "ND5"),
        ("개발 환경", "Jupyter, VS Code", "코딩 및 실습", "공통"),
        ("버전 관리", "Git, GitHub", "협업 및 포트폴리오", "공통"),
    ]

    for category, tool, purpose, course in tech_items:
        r += 1
        # Determine row fill color based on course
        if "ND1" in course and "ND2" not in course and "ND5" not in course and "공통" not in course:
            row_fill = FILL_LIGHT_BLUE
        elif "ND2" in course and "ND1" not in course and "ND5" not in course:
            row_fill = FILL_LIGHT_GREEN
        elif "ND5" in course and "ND1" not in course and "ND2" not in course:
            row_fill = FILL_LIGHT_ORANGE
        else:
            row_fill = FILL_WHITE

        set_cell(ws, r, 1, category, FONT_BODY, row_fill, ALIGN_LEFT)
        set_cell(ws, r, 2, tool, FONT_BODY_BOLD, row_fill, ALIGN_LEFT)
        set_cell(ws, r, 3, purpose, FONT_BODY, row_fill, ALIGN_LEFT)
        set_cell(ws, r, 4, course, FONT_BODY, row_fill, ALIGN_CENTER)


# ══════════════════════════════════════════════════════════════════════════
# TAB 5: 캡스톤_예시
# ══════════════════════════════════════════════════════════════════════════
def build_tab5_capstone(wb, data):
    ws = wb.create_sheet("캡스톤_예시")
    ws.sheet_properties.tabColor = ORANGE

    for col, w in [(1, 25), (2, 50), (3, 40), (4, 22)]:
        ws.column_dimensions[get_column_letter(col)].width = w

    r = 1
    merge_and_set(ws, r, 1, r, 4, "캡스톤 프로젝트 예시", FONT_TITLE, FILL_NAVY, ALIGN_CENTER)

    # ── ND1 Capstone ──
    r += 2
    merge_and_set(ws, r, 1, r, 4, "ND1 캡스톤 — M13. 물리 시뮬레이션 연동 캡스톤", FONT_SUBTITLE, FILL_BLUE, ALIGN_CENTER)
    r += 1
    for ci, h in enumerate(["프로젝트명", "시나리오 설명", "주요 기술 요소", "예상 산출물"], 1):
        set_cell(ws, r, ci, h, FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

    nd1_projects = [
        ("ROS2-시뮬레이터 Pick & Place",
         "ROS2 Action 통신 레이어를 연동하여 파이썬 스크립트 기반 시뮬레이션 환경 내 Pick & Place 단대단 구현",
         "ROS2 Action Server, MuJoCo/Isaac Sim, Python API, 토크 제어",
         "데모 영상 + 실행 스크립트"),
        ("커스텀 SLM 로컬 추론 시스템",
         "HuggingFace 생태계를 활용한 나만의 커스텀 파라미터 언어 모델 구축 미니 캡스톤",
         "Hugging Face, Llama-3 8B / Qwen 1.5B, 파인튜닝, GPU 추론",
         "모델 + 추론 스크립트"),
    ]
    for name, desc, tech, output in nd1_projects:
        r += 1
        set_cell(ws, r, 1, name, FONT_BODY_BOLD, FILL_LIGHT_BLUE, ALIGN_LEFT)
        set_cell(ws, r, 2, desc, FONT_BODY, FILL_WHITE, ALIGN_TOP)
        set_cell(ws, r, 3, tech, FONT_BODY, FILL_WHITE, ALIGN_TOP)
        set_cell(ws, r, 4, output, FONT_BODY, FILL_WHITE, ALIGN_CENTER)
        ws.row_dimensions[r].height = 45

    # ── ND2 Capstone ──
    r += 2
    merge_and_set(ws, r, 1, r, 4, "ND2 캡스톤 — M4. VLM 기반 합성 이미지 Grounding", FONT_SUBTITLE, FILL_TEAL, ALIGN_CENTER)
    r += 1
    for ci, h in enumerate(["프로젝트명", "시나리오 설명", "주요 기술 요소", "예상 산출물"], 1):
        set_cell(ws, r, ci, h, FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

    nd2_projects = [
        ("합성 데이터 기반 객체 탐지 시스템",
         "실 장비 테스트 데이터(소량) vs 시뮬레이션 라벨링 합성 데이터(대량) 혼합 학습 검증 및 탐지 성능 지표(mAP) 산출",
         "Isaac Sim Replicator, YOLO11 파인튜닝, 도메인 랜덤화, PGR 지표",
         "학습 로그 + mAP 리포트"),
        ("VLM 기반 합성 이미지 VQA & Grounding",
         "시뮬레이션으로 생성한 합성 이미지 내부의 다중 객체에 대하여 VLM 기반 질의응답 및 자연어 기반 객체 Grounding 종합",
         "Florence-2, Qwen-VL-3B, VQA, 객체 Grounding",
         "데모 영상 + Grounding 파이프라인"),
    ]
    for name, desc, tech, output in nd2_projects:
        r += 1
        set_cell(ws, r, 1, name, FONT_BODY_BOLD, FILL_LIGHT_GREEN, ALIGN_LEFT)
        set_cell(ws, r, 2, desc, FONT_BODY, FILL_WHITE, ALIGN_TOP)
        set_cell(ws, r, 3, tech, FONT_BODY, FILL_WHITE, ALIGN_TOP)
        set_cell(ws, r, 4, output, FONT_BODY, FILL_WHITE, ALIGN_CENTER)
        ws.row_dimensions[r].height = 45

    # ── ND5 Capstone ──
    r += 2
    merge_and_set(ws, r, 1, r, 4, "ND5 캡스톤 — M12. LLM · 로봇 시스템 E2E 통합", FONT_SUBTITLE, FILL_ORANGE, ALIGN_CENTER)
    r += 1
    for ci, h in enumerate(["프로젝트명", "시나리오 설명", "주요 기술 요소", "예상 산출물"], 1):
        set_cell(ws, r, ci, h, FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

    nd5_projects = [
        ("창고 물류 자동화 에이전트",
         "LLM이 창고 내 물품 배치 최적화 및 피킹 작업 지시를 수행하는 자율 물류 시스템",
         "VLM 객체 인식, Task Planning, ROS2 로봇 제어, LeRobot",
         "데모 영상 + Git 포트폴리오"),
        ("실험실 로봇 어시스턴트",
         "연구원의 자연어 명령을 받아 실험 기구 정리 및 시약 운반을 수행하는 연구 보조 로봇",
         "RAG(실험 매뉴얼), Grounding DINO, Safety 모니터링, Manipulation",
         "데모 영상 + Git 포트폴리오"),
        ("재활 보조 로봇 Safety 에이전트",
         "환자 재활 운동 보조 시 안전 제약을 최우선으로 하는 LLM 에이전트 시스템",
         "안전 정렬, 실시간 이상 감지, 비상 정지 시스템, Force Control",
         "데모 영상 + Git 포트폴리오"),
    ]
    for name, desc, tech, output in nd5_projects:
        r += 1
        set_cell(ws, r, 1, name, FONT_BODY_BOLD, FILL_LIGHT_ORANGE, ALIGN_LEFT)
        set_cell(ws, r, 2, desc, FONT_BODY, FILL_WHITE, ALIGN_TOP)
        set_cell(ws, r, 3, tech, FONT_BODY, FILL_WHITE, ALIGN_TOP)
        set_cell(ws, r, 4, output, FONT_BODY, FILL_WHITE, ALIGN_CENTER)
        ws.row_dimensions[r].height = 45

    # ── Evaluation criteria (shared) ──
    r += 2
    merge_and_set(ws, r, 1, r, 4, "평가 기준 (공통)", FONT_SECTION, FILL_LIGHT_GRAY, ALIGN_CENTER)
    r += 1
    for ci, h in enumerate(["평가 항목", "배점", "세부 기준"], 1):
        set_cell(ws, r, ci, h, FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

    eval_items = [
        ("기술 구현 완성도", "40%", "E2E 파이프라인 동작 여부, 코드 품질 및 모듈화"),
        ("문제 해결 창의성", "25%", "시나리오 선정의 적절성, 접근 방식의 독창성"),
        ("발표 및 문서화", "20%", "데모 영상 품질, README 완성도, 기술 문서"),
        ("팀워크 및 협업", "15%", "Git 기여도 분포, 역할 분담 및 커뮤니케이션"),
    ]
    for item, score, detail in eval_items:
        r += 1
        set_cell(ws, r, 1, item, FONT_BODY_BOLD, FILL_WHITE, ALIGN_LEFT)
        set_cell(ws, r, 2, score, FONT_BODY, FILL_WHITE, ALIGN_CENTER)
        merge_and_set(ws, r, 3, r, 4, detail, FONT_BODY, FILL_WHITE, ALIGN_LEFT)

    # Pass/Fail
    r += 2
    merge_and_set(ws, r, 1, r, 4, "평가 방식", FONT_SECTION, FILL_LIGHT_GRAY, ALIGN_CENTER)
    r += 1
    set_cell(ws, r, 1, "합격 기준", FONT_BODY_BOLD, FILL_WHITE, ALIGN_LEFT)
    merge_and_set(ws, r, 2, r, 3, "절대평가 75점 이상 (Pass/Fail)", FONT_BODY, FILL_WHITE, ALIGN_LEFT)
    r += 1
    set_cell(ws, r, 1, "역량 인증", FONT_BODY_BOLD, FILL_WHITE, ALIGN_LEFT)
    merge_and_set(ws, r, 2, r, 3, "Lv3 (ND1/ND2) / Lv4 (ND5) 기준 충족 시 인증서 발급", FONT_BODY, FILL_WHITE, ALIGN_LEFT)

    # Performance metrics
    r += 2
    merge_and_set(ws, r, 1, r, 3, "성과 지표", FONT_SECTION, FILL_LIGHT_GRAY, ALIGN_CENTER)
    r += 1
    set_cell(ws, r, 1, "지표", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)
    set_cell(ws, r, 2, "설명", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)
    set_cell(ws, r, 3, "측정 방법", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

    metrics = [
        ("성공률", "Task 완료 비율", "전체 시도 중 성공 횟수 측정"),
        ("지연 시간 (Latency)", "명령→실행 완료 소요 시간", "프로파일링 도구로 측정"),
        ("안전 위반 횟수", "금지 행동 발생 횟수", "Safety 레이어 로그 분석"),
    ]
    for m, desc, method in metrics:
        r += 1
        set_cell(ws, r, 1, m, FONT_BODY_BOLD, FILL_WHITE, ALIGN_LEFT)
        set_cell(ws, r, 2, desc, FONT_BODY, FILL_WHITE, ALIGN_LEFT)
        set_cell(ws, r, 3, method, FONT_BODY, FILL_WHITE, ALIGN_LEFT)

    # Submission requirements
    r += 2
    merge_and_set(ws, r, 1, r, 3, "제출물 요건", FONT_SECTION, FILL_LIGHT_GRAY, ALIGN_CENTER)
    r += 1
    set_cell(ws, r, 1, "항목", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)
    merge_and_set(ws, r, 2, r, 3, "상세", FONT_HEADER, FILL_NAVY, ALIGN_CENTER)

    submissions = [
        ("Git/README", "프로젝트 구조, 실행 방법, 아키텍처 설명"),
        ("실행 스크립트", "환경 설정부터 데모 실행까지 재현 가능한 스크립트"),
        ("실험 로그", "MLflow/W&B 기록 (하이퍼파라미터, 성능 지표)"),
        ("데모 영상", "전체 파이프라인 동작을 보여주는 2-5분 영상"),
    ]
    for item, detail in submissions:
        r += 1
        set_cell(ws, r, 1, item, FONT_BODY_BOLD, FILL_WHITE, ALIGN_LEFT)
        merge_and_set(ws, r, 2, r, 3, detail, FONT_BODY, FILL_WHITE, ALIGN_LEFT)


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════
def main():
    with open(CONTENT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    wb = Workbook()

    build_tab1_overview(wb, data)
    build_tab2_curriculum_overview(wb, data)
    build_tab3_curriculum_detail(wb, data)
    build_tab4_tech_stack(wb, data)
    build_tab5_capstone(wb, data)

    wb.save(str(OUTPUT_XLSX))
    print(f"✅ 엑셀 생성 완료: {OUTPUT_XLSX}")
    print(f"   - 시트 수: {len(wb.sheetnames)}")
    for name in wb.sheetnames:
        ws = wb[name]
        print(f"   - [{name}] {ws.max_row} rows × {ws.max_column} cols")


if __name__ == "__main__":
    main()
