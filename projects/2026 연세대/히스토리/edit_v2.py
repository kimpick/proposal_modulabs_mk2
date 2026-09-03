"""
연세AX 제안서 v2 편집 스크립트
- 사본(v2)의 "2.가. 사업 수행 목표 및 방안" 섹션 보완
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from copy import deepcopy
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement
from lxml import etree

PATH = '연세AX_제안서_모두의연구소_v2_260506.docx'

doc = Document(PATH)
body = doc.element.body


def find_para_by_text(doc, contains_text, start_idx=0):
    """contains_text를 포함한 첫 paragraph 인덱스 반환"""
    for i, p in enumerate(doc.paragraphs):
        if i < start_idx:
            continue
        if contains_text in p.text:
            return i
    return -1


def find_paras_by_text(doc, contains_text):
    """contains_text를 포함한 모든 paragraph 인덱스 반환"""
    result = []
    for i, p in enumerate(doc.paragraphs):
        if contains_text in p.text:
            result.append(i)
    return result


def replace_paragraph_text(para, new_text, bold=None):
    """기존 paragraph의 runs를 비우고 새 텍스트 1개의 run으로 교체"""
    # Get formatting from first run if available
    src_run = para.runs[0] if para.runs else None
    src_bold = bold if bold is not None else (src_run.bold if src_run else False)
    src_font = src_run.font.name if src_run and src_run.font.name else None
    src_size = src_run.font.size if src_run and src_run.font.size else None

    # Remove all runs
    for r in list(para.runs):
        r._element.getparent().remove(r._element)

    # Add new run
    new_run = para.add_run(new_text)
    if src_bold:
        new_run.bold = True
    if src_font:
        new_run.font.name = src_font
        # Korean font hint
        rpr = new_run._element.get_or_add_rPr()
        rfonts = rpr.find(qn('w:rFonts'))
        if rfonts is None:
            rfonts = OxmlElement('w:rFonts')
            rpr.append(rfonts)
        rfonts.set(qn('w:eastAsia'), src_font)
    if src_size:
        new_run.font.size = src_size


def delete_paragraph(para):
    """단락 자체를 문서에서 제거"""
    elem = para._element
    elem.getparent().remove(elem)


def insert_paragraph_after(reference_element, text, bold=False, style=None):
    """reference_element 바로 뒤에 새 paragraph 삽입. 새 paragraph 객체 반환."""
    new_p = OxmlElement('w:p')
    reference_element.addnext(new_p)
    # Build run
    r = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    if bold:
        b = OxmlElement('w:b')
        rpr.append(b)
        b2 = OxmlElement('w:bCs')
        rpr.append(b2)
    # Korean font preservation
    rfonts = OxmlElement('w:rFonts')
    rfonts.set(qn('w:eastAsia'), '맑은 고딕')
    rpr.append(rfonts)
    r.append(rpr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    r.append(t)
    new_p.append(r)
    if style:
        ppr = OxmlElement('w:pPr')
        pstyle = OxmlElement('w:pStyle')
        pstyle.set(qn('w:val'), style)
        ppr.append(pstyle)
        new_p.insert(0, ppr)
    return new_p


def set_cell_text(cell, text, bold=False):
    """셀 내용을 새 텍스트로 교체 (기존 내용 모두 비움)"""
    # Clear existing paragraphs
    for p in list(cell.paragraphs):
        cell._element.remove(p._element)
    # Add new paragraph
    p = cell.add_paragraph()
    run = p.add_run(text)
    if bold:
        run.bold = True
    # Korean font hint
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set(qn('w:eastAsia'), '맑은 고딕')


# ====================================================================
# Step 1: 위치 확인 (현재 paragraph 인덱스)
# ====================================================================
print("=== 현재 문서 구조 확인 ===")
key_paras = [
    "사업 수행 목표는 수치적으로",
    "아래 예시",
    "비전공자 특화 5-Track",
    "빈틈없는 3중 학습",
    "Tech-Native 기반",
    "세가지 즐거움은 전략인지",
    "기관별 독립 운영을 원칙으로",
    "사업 품질관리 및 업무 보고 체계에 넣어야",
    "AX 역량 로드맵",
    "학부 재학 중 이수 가능한",
    "총장 명의의 AX 역량 인증서",
    "전략 1. Joy of Depth",
    "전략 2. Joy of Expansion",
    "전략 3. Joy of Originality",
]
for kp in key_paras:
    idx = find_para_by_text(doc, kp)
    if idx >= 0:
        print(f"  [{idx}] '{kp[:40]}...' -> {doc.paragraphs[idx].text[:80]}")
    else:
        print(f"  [NOT FOUND] {kp}")

print()

# ====================================================================
# Task 1 + Task 2: 내부 코멘트 삭제 + 사업 수행 목표 4개 삽입
# ====================================================================
# 위치: "사업 수행 목표 및 추진 전략" 아래에 코멘트 2줄 + 플레이스홀더 3줄
# 전략: 코멘트 2줄과 플레이스홀더 3줄을 삭제하고, 그 자리에 새 목표 4개 삽입

# 코멘트 삭제
for txt in ["사업 수행 목표는 수치적으로", "아래 예시"]:
    idx = find_para_by_text(doc, txt)
    if idx >= 0:
        delete_paragraph(doc.paragraphs[idx])
        print(f"DELETED: '{txt}'")

# Task 2: "비전공자 특화 5-Track..." 플레이스홀더 paragraph 위치 확인
# 그 paragraph를 첫 목표로 교체하고, 나머지 placeholder는 삭제 후 새 목표 추가
idx_place1 = find_para_by_text(doc, "비전공자 특화 5-Track")
idx_place2 = find_para_by_text(doc, "빈틈없는 3중 학습")
idx_place3 = find_para_by_text(doc, "Tech-Native 기반")

# 첫 placeholder 위치 기준으로 anchor 확보 (XML element)
anchor_para = doc.paragraphs[idx_place1] if idx_place1 >= 0 else None
anchor_elem = anchor_para._element if anchor_para else None

# 기존 placeholder 3개 삭제
for txt in ["비전공자 특화 5-Track", "빈틈없는 3중 학습", "Tech-Native 기반"]:
    idx = find_para_by_text(doc, txt)
    if idx >= 0:
        delete_paragraph(doc.paragraphs[idx])
        print(f"DELETED placeholder: '{txt}'")

# anchor가 삭제됐을 수 있으니, "사업 수행 목표 및 추진 전략" 앵커를 다시 찾음
heading_idx = find_para_by_text(doc, "사업 수행 목표 / 및 추진 전략")
if heading_idx < 0:
    heading_idx = find_para_by_text(doc, "사업 수행 목표")
    while heading_idx >= 0 and "추진 전략" not in doc.paragraphs[heading_idx].text:
        heading_idx = find_para_by_text(doc, "사업 수행 목표", heading_idx + 1)

# 직접 검색
heading_idx = -1
for i, p in enumerate(doc.paragraphs):
    if "사업 수행 목표" in p.text and "추진 전략" in p.text:
        heading_idx = i
        break
print(f"Heading '사업 수행 목표 및 추진 전략' index: {heading_idx}")

if heading_idx < 0:
    print("ERROR: Heading not found!")
    sys.exit(1)

# 새 목표 본문 (heading 바로 뒤에 순서대로 삽입)
# insert_paragraph_after는 매번 reference 다음에 넣으므로,
# 마지막 삽입한 element를 다음 reference로 사용
goals = [
    ("본 사업의 수행 목표를 다음 네 가지로 설정하고, 각 목표에 대한 정량적 달성 기준을 제시합니다.", False, None),
    ("", False, None),  # 빈 줄
    ("가. 3개 기관 통합 AX 교육 체계 구축 및 전주기 교육 운영", True, None),
    ("신촌캠퍼스 도서관(연세 AX 아카데미), 국제캠퍼스 도서관(연세 AX 스타트), 신촌캠퍼스 박물관(연세 AX 뮤즈로그)을 기관별 독립 운영하되, 기초→활용→심화 단계별 연계 구조를 설계하여 체계적으로 AX 역량을 쌓을 수 있도록 합니다.", False, None),
    ("달성 기준: 총 90건 과정, 343회, 549시간 교육 운영 완료", False, None),
    ("", False, None),
    ("나. 문제정의–실습–프로젝트–성과확산 전주기 커리큘럼 설계·운영", True, None),
    ("봄학기 문제 발견(디자인씽킹) → 여름방학 기술 심화(AX 캠프) → 가을학기 프로젝트 수행 → 겨울 MVP 완성·쇼케이스로 이어지는 4계절 전주기 교육을 설계합니다.", False, None),
    ("체험 교육(5건) → 세미나(8건) → 워크숍(41건) → 멘토링(9건) → 공모전·성과 공유(7건) + 콘텐츠 개발(20건)의 단계적 교육 체계를 구성합니다.", False, None),
    ("", False, None),
    ("다. 총장 명의 AX 역량 인증서 발급 체계 구축", True, None),
    ("사회적 수요를 반영한 AX 역량을 도출하고, 학부 재학 중 이수 가능한 기초(AX Starter)→활용(AX Practitioner)→심화(AX Creator) 3단계 교육 과정을 설계합니다.", False, None),
    ("국제캠퍼스 연세 AX 스타트(신입생)에서 신촌캠퍼스 연세 AX 아카데미(심화)로 자연 연계되는 로드맵을 구성합니다.", False, None),
    ("", False, None),
    ("라. 실습 교육 콘텐츠 15종 및 실감형 콘텐츠 5종 기획·제작", True, None),
    ("AX 교육의 학습 효과 극대화를 위해 주제별·수준별 맞춤형 실습 교재 및 콘텐츠를 개발합니다.", False, None),
    ("실감형 콘텐츠는 연세 학술정보원의 VR/AR/MR 인프라를 활용하되, Physical AI 기술 요소(센서 데이터 연동, 공간 인식 AI 등)와의 접점을 탐색하여 차세대 실감 교육 콘텐츠를 기획합니다.", False, None),
]

# heading 다음에 순차 삽입 (reverse 후 한 번에 삽입하면 순서 유지)
ref = doc.paragraphs[heading_idx]._element
for text, bold, style in goals:
    new_elem = insert_paragraph_after(ref, text, bold=bold, style=style)
    ref = new_elem  # 다음 삽입 위치를 방금 삽입한 element로

print(f"INSERTED {len(goals)} goal paragraphs")

# ====================================================================
# Task 3: Trinity of Joy 전략 헤딩 정리 + 구현 프로그램 줄 추가
# ====================================================================
# "세가지 즐거움은 전략인지 목표인지?" 삭제
idx = find_para_by_text(doc, "세가지 즐거움은 전략인지")
if idx >= 0:
    delete_paragraph(doc.paragraphs[idx])
    print("DELETED: '세가지 즐거움은 전략인지...'")

# "The Trinity of Joy" 헤딩 텍스트를 "추진 전략: The Trinity of Joy..."로 교체
idx = find_para_by_text(doc, "The Trinity of Joy")
if idx >= 0:
    replace_paragraph_text(doc.paragraphs[idx], "추진 전략: The Trinity of Joy (배움의 세 가지 즐거움)", bold=True)
    print("UPDATED: Trinity of Joy heading")

# "모든 프로그램은 설계 방향 기반 아래 세 가지 즐거움을 축으로 설계됩니다." 교체
idx = find_para_by_text(doc, "모든 프로그램은 설계 방향")
if idx >= 0:
    replace_paragraph_text(doc.paragraphs[idx],
        "위 네 가지 목표를 달성하기 위해, 모든 프로그램은 아래 세 가지 즐거움을 설계 원칙으로 삼습니다.")
    print("UPDATED: Trinity of Joy intro")

# 각 전략 끝에 "구현 프로그램" 1줄 추가
# 전략 1 (Joy of Depth) — 인용문 뒤에 삽입
strategy_additions = [
    ("나는 AI가 어떻게 작동하는지 안다",
     "구현 프로그램: AX 기술 실습 워크숍(41건), 여름 AX 심화 캠프 (Vibe Coding → Agentic Coding → Harness Engineering 단계별 심화)"),
    ("나는 내 전공으로 AI를 활용할 수 있다",
     "구현 프로그램: 3개 캠퍼스 특성화 운영, AX 트렌드 세미나(8건), 박물관 인문학 역량 강화 융합 교육, 실감미디어 체험 프로그램(5건)"),
    ("나는 AI를 도구로 삼아 세상에 내 결과물",
     "구현 프로그램: 멘토링 프로젝트(9건), 공모전·경진대회·쇼케이스(7건), Wild Public Release를 통한 SNS 배포 및 사회적 확산"),
]

for anchor_text, new_line in strategy_additions:
    idx = find_para_by_text(doc, anchor_text)
    if idx >= 0:
        anchor_elem = doc.paragraphs[idx]._element
        insert_paragraph_after(anchor_elem, new_line, bold=False)
        print(f"INSERTED 구현프로그램 after: '{anchor_text[:30]}...'")

# ====================================================================
# Task 4: Table 14 (커리큘럼 90건) 채우기 + 4계절 흐름 표 삽입
# ====================================================================
# Table 14 = 5번째 인덱스 (이전 분석에서 확인)
# 다시 계산이 필요할 수 있으므로 헤더가 ['구분','과정 유형','건수','주요 내용'] 인 표 찾기

target_table = None
for i, t in enumerate(doc.tables):
    if len(t.rows) > 0:
        first_row_text = [c.text.strip() for c in t.rows[0].cells]
        if '구분' in first_row_text and ('과정 유형' in first_row_text or '건수' in first_row_text):
            # Skip the curriculum-related table after this one if it's the AI tool table
            if '주요 내용' in first_row_text:
                target_table = t
                print(f"Found curriculum table at index {i}: {first_row_text}")
                break

if target_table is None:
    print("ERROR: Curriculum Table 14 not found")
else:
    curriculum_data = [
        ("구분", "내용", "건수", "주요 내용"),
        ("체험 교육", "[신촌] 실감미디어 기반 몰입 체험 프로그램", "5",
         "도서관 미디어 인프라(VR/AR/MR)를 활용한 정규 프로그램, 특별 체험 및 전시 프로그램. Physical AI 기술 요소(공간 인식 AI, 센서 데이터 연동 등)와의 접점을 탐색하여 차세대 실감 교육 경험 설계"),
        ("세미나", "[신촌/국제] AX 트렌드 세미나", "5",
         "IT·미디어 산업 최고 전문가가 진행하는 AX 최신 트렌드 강의 및 토론. 봄/가을 학기별 운영"),
        ("", "[박물관] 인문학 역량 강화 세미나", "3",
         "AX 시대의 인문학 미래, 한글을 지킨 연세의 거인들 등 인문학·AI 접점 탐구"),
        ("워크숍", "[신촌] AX 핵심 기술 실습", "10",
         "생성형 AI, 데이터 분석, AI 에이전트 등 심화 실습. Vibe Coding → Agentic Coding → Harness Engineering 단계별 커리큘럼"),
        ("", "[국제] AI 및 프로그래밍 실습", "10",
         "신입생 대상 AI·프로그래밍 기초, Codex 활용 자연어 기반 프로토타이핑"),
        ("", "[국제] 생성형 AI 콘텐츠 제작", "10",
         "생성형 AI 활용 텍스트·이미지·영상 콘텐츠 제작 실습"),
        ("", "[국제] 디지털 미디어 S/W 활용", "10",
         "Capcut, Canva 등 미디어 제작 S/W 활용 과정"),
        ("", "[박물관] AI 활용 워크숍", "1",
         "AI 창작 워크숍(기초, 심화) — 인문학 자원 기반 AI 콘텐츠 창작"),
        ("멘토링", "[신촌] 실전 문제 해결 프로젝트", "7",
         "디자인씽킹 기반 문제 정의 → AI 프로토타입 제작 → MVP 완성. 2026 여름 AX 캠프 포함"),
        ("", "[국제] 공모전 참여 기술 멘토링", "2",
         "공모전 출품을 위한 기술 워크숍 및 개별(팀별) 멘토링"),
        ("공모전·경진대회·성과 공유", "[신촌] AI 활용 문제 해결 성과 발표", "3",
         "학기별 피드백 데이 + 최종 쇼케이스(Wild Public Release). SNS 기반 결과물 공개"),
        ("", "[국제] AX 역량 강화 공모전·경진대회", "3",
         "캠퍼스별 공모전 개최, 전문가 심사 및 피드백"),
        ("", "[박물관] 문화 유산 기반 AX 공모전", "1",
         "인문학·문화유산 주제 AX 공모전 및 성과 확산"),
        ("AX 교육 콘텐츠 개발", "[신촌] 실습 교육 콘텐츠", "15",
         "주제별·수준별 맞춤형 실습 교재 기획·제작 (프로그래밍, 데이터 분석, 미디어 등)"),
        ("", "[신촌] 실감형 콘텐츠", "5",
         "VR/AR/MR 기반 실감형 교육 콘텐츠 기획·제작. 연세 학술정보원 인프라 활용"),
        ("합계", "", "90", "총 343회, 549시간"),
    ]

    # 현재 표 행 수 확인
    current_rows = len(target_table.rows)
    needed_rows = len(curriculum_data)
    print(f"Curriculum table: current {current_rows} rows, need {needed_rows}")

    # 행 수 맞추기 (현재 8개 → 17개로 늘려야 함)
    while len(target_table.rows) < needed_rows:
        target_table.add_row()

    # 데이터 채우기
    for r_idx, row_data in enumerate(curriculum_data):
        row = target_table.rows[r_idx]
        for c_idx, cell_text in enumerate(row_data):
            if c_idx < len(row.cells):
                set_cell_text(row.cells[c_idx], cell_text, bold=(r_idx == 0))
    print(f"FILLED curriculum table with {needed_rows} rows")

# ====================================================================
# Task 5: Table 15 (AI 툴) 채우기
# ====================================================================
target_tool_table = None
for i, t in enumerate(doc.tables):
    if len(t.rows) > 0:
        first_row_text = [c.text.strip() for c in t.rows[0].cells]
        if '핵심 실습 툴' in first_row_text or '활용 목적' in first_row_text:
            target_tool_table = t
            print(f"Found AI tool table at index {i}: {first_row_text}")
            break

if target_tool_table is None:
    print("ERROR: AI Tool Table 15 not found")
else:
    tool_data = [
        ("과정", "핵심 실습 툴", "활용 목적", "대체 가능 툴"),
        ("생성형 AI 워크숍", "ChatGPT, Gemini, Perplexity",
         "프롬프트 설계·비교 분석, AI 기반 리서치·텍스트 생성", "NotebookLM"),
        ("데이터 분석 워크숍", "NotebookLM, Python(Colab)",
         "AI 기반 데이터 해석·요약, 시각화 및 인사이트 도출", "Pandas AI"),
        ("AI 에이전트 실습", "Codex",
         "자율 에이전트 설계, 자동화 워크플로우 구축, Agentic Coding 실습", "—"),
        ("코딩·프로토타이핑", "Codex",
         "Vibe Coding 기반 자연어→웹앱 프로토타입 구현, Harness Engineering 실습", "Lovable"),
        ("디지털 콘텐츠 제작", "Canva, Capcut, Gamma",
         "AI 기반 이미지·영상·프레젠테이션 콘텐츠 제작", "Figma AI"),
        ("실감미디어 체험", "발주처 보유 VR/AR/MR 인프라",
         "몰입형 체험 교육. Physical AI(공간 인식, 센서 연동) 접점 탐색", "—"),
        ("인문학 AI 융합 (박물관)", "ChatGPT, Midjourney, Suno",
         "AI 기반 텍스트·이미지·음악 창작, 문화유산 디지털 재해석", "DALL-E"),
    ]

    current_rows = len(target_tool_table.rows)
    needed_rows = len(tool_data)
    print(f"Tool table: current {current_rows} rows, need {needed_rows}")

    while len(target_tool_table.rows) < needed_rows:
        target_tool_table.add_row()

    for r_idx, row_data in enumerate(tool_data):
        row = target_tool_table.rows[r_idx]
        for c_idx, cell_text in enumerate(row_data):
            if c_idx < len(row.cells):
                set_cell_text(row.cells[c_idx], cell_text, bold=(r_idx == 0))
    print(f"FILLED tool table with {needed_rows} rows")

# ====================================================================
# Task 1 (cont.): "[  ]" placeholder 교체
# ====================================================================
idx = find_para_by_text(doc, "기관별 독립 운영을 원칙으로")
if idx >= 0:
    para = doc.paragraphs[idx]
    full_text = para.text
    # "[  ]" 부분을 "기초→활용→심화 단계별 연계" 로 교체
    new_text = full_text.replace("[  ]", "기초→활용→심화 단계별 연계").replace("[ ]", "기초→활용→심화 단계별 연계")
    if new_text != full_text:
        replace_paragraph_text(para, new_text)
        print(f"REPLACED [  ] placeholder")

# ====================================================================
# Task 1 (cont.): "사업 품질관리 및 업무 보고 체계에 넣어야 할 지 고민중" 삭제
# ====================================================================
idx = find_para_by_text(doc, "사업 품질관리 및 업무 보고 체계에 넣어야")
if idx >= 0:
    delete_paragraph(doc.paragraphs[idx])
    print("DELETED: 사업 품질관리 코멘트")

# ====================================================================
# Task 6: AX 역량 로드맵 본문 추가
# ====================================================================
# 위치: "총장 명의의 AX 역량 인증서" 라인 뒤에 추가
# 그 후 "사업 품질관리..." 코멘트가 있던 자리에 본문 추가

# 앵커: "학부 재학 중 이수 가능한 기초·활용-심화 단계별 교육 과정 설계" (이건 그대로 유지)
# 그 다음 라인 "총장 명의의 AX 역량 인증서 발급에 필요한..." 도 그대로 유지
# 그 다음에 새로운 본문 추가

# 둘 중 더 뒤에 있는 라인 찾기 (총장 명의의 AX...)
idx = find_para_by_text(doc, "총장 명의의 AX 역량 인증서")
if idx < 0:
    idx = find_para_by_text(doc, "학부 재학 중 이수 가능한")

if idx >= 0:
    anchor_elem = doc.paragraphs[idx]._element

    # 새 본문 (단락별로 삽입)
    roadmap_paras = [
        ("", False),
        ("총장 명의의 AX 역량 인증서 발급을 위해, 학부 재학 중 이수 가능한 기초–활용–심화 3단계 교육 로드맵을 구성합니다. 사회적 수요를 반영한 AX 역량을 도출하고, 국제캠퍼스(신입생)에서 신촌캠퍼스(심화)로 자연 연계되는 성장 경로를 설계합니다.", False),
        ("", False),
        ("▶ 단계 1. 기초 — AX Starter (\"AI를 이해하다\")", True),
        ("대상: 국제캠퍼스 신입생 (연세 AX 스타트)", False),
        ("핵심 역량: AI 기초 리터러시, 생성형 AI 도구 활용 능력", False),
        ("이수 요건: 체험 교육 참여 + 입문 세미나 수강 + 기초 워크숍(생성형 AI 원데이 클래스 등) 2건 이상 이수", False),
        ("Joy 매핑: Joy of Depth — AI가 무엇이고 어떻게 작동하는지 이해하는 단계", False),
        ("인증: AX Starter 수료 인증 (출결 + 기초 과제 제출)", False),
        ("", False),
        ("▶ 단계 2. 활용 — AX Practitioner (\"AI로 만들다\")", True),
        ("대상: 신촌캠퍼스 (연세 AX 아카데미) 및 AX Starter 이수자", False),
        ("핵심 역량: AI 도구 활용 실무 능력, 주제별 문제 해결 역량", False),
        ("이수 요건: 주제별 워크숍 4건 이상 이수 + 멘토링 프로젝트 1건 참여", False),
        ("Joy 매핑: Joy of Expansion — 배운 기술을 자신의 전공·관심 도메인에 적용하는 단계", False),
        ("인증: AX Practitioner 수료 인증 (워크숍 이수 + 프로젝트 결과물 제출)", False),
        ("", False),
        ("▶ 단계 3. 심화 — AX Creator (\"AI로 증명하다\")", True),
        ("대상: 전 캠퍼스 (AX Practitioner 이수자, 공모전·쇼케이스 참여자)", False),
        ("핵심 역량: AI 기반 창의적 문제 해결, 프로젝트 완수 및 사회적 확산 능력", False),
        ("이수 요건: 공모전 또는 경진대회 출품 + 최종 쇼케이스 발표 + AX 포트폴리오 제출", False),
        ("Joy 매핑: Joy of Originality — 나만의 결과물(MVP)을 만들어 세상에 공개하는 단계", False),
        ("인증: 총장 명의 AX 역량 인증서 발급", True),
        ("", False),
        ("▶ 이수 현황 관리", True),
        ("참여자 출결, 결과물 등 수료 기준 및 교육 이수 현황 체계적 관리", False),
        ("단계별 이수 조건 충족 여부 자동 추적 및 인증서 발급 대상 관리", False),
        ("학기별 이수 현황 보고를 통한 로드맵 운영 실효성 확보", False),
    ]

    ref = anchor_elem
    for text, bold in roadmap_paras:
        new_elem = insert_paragraph_after(ref, text, bold=bold)
        ref = new_elem
    print(f"INSERTED {len(roadmap_paras)} roadmap paragraphs")

# ====================================================================
# Save
# ====================================================================
doc.save(PATH)
print(f"\n✅ Saved: {PATH}")
