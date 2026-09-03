# -*- coding: utf-8 -*-
"""Build the Yonsei AI Design Thinking seminar planning workbook (10 tabs)."""
import sys
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = r"C:\Users\Admin\Downloads\ai-education-proposal\projects\2026 연세대\연세대_AI디자인씽킹_세미나_기획.xlsx"

# ── 스타일 토큰 ──
FONT_NAME = "맑은 고딕"
CORAL = "F7585C"
DARK = "030712"
LIGHT_CORAL = "FFE5E6"
LIGHT_GRAY = "F4F6F8"
LIGHT_BLUE = "E8F0FE"
LIGHT_YELLOW = "FFF8DC"
LIGHT_GREEN = "E6F4EA"
BORDER_GRAY = "D0D5DA"

def base_font(size=10, bold=False, color="030712"):
    return Font(name=FONT_NAME, size=size, bold=bold, color=color)

def header_font():
    return Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")

def section_font():
    return Font(name=FONT_NAME, size=12, bold=True, color="FFFFFF")

def title_font():
    return Font(name=FONT_NAME, size=16, bold=True, color="030712")

def fill(color):
    return PatternFill("solid", start_color=color, end_color=color)

def thin_border():
    s = Side(style="thin", color=BORDER_GRAY)
    return Border(left=s, right=s, top=s, bottom=s)

def wrap_left(vert="top"):
    return Alignment(wrap_text=True, vertical=vert, horizontal="left")

def wrap_center():
    return Alignment(wrap_text=True, vertical="center", horizontal="center")

def style_header_row(ws, row, ncols, color=CORAL):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = header_font()
        cell.fill = fill(color)
        cell.alignment = wrap_center()
        cell.border = thin_border()
    ws.row_dimensions[row].height = 28

def style_body(ws, start_row, end_row, ncols, alt=True):
    for r in range(start_row, end_row + 1):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = base_font()
            cell.alignment = wrap_left()
            cell.border = thin_border()
            if alt and (r - start_row) % 2 == 1:
                cell.fill = fill(LIGHT_GRAY)

def set_widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

def add_title(ws, title, subtitle=None):
    ws["A1"] = title
    ws["A1"].font = title_font()
    ws.row_dimensions[1].height = 30
    if subtitle:
        ws["A2"] = subtitle
        ws["A2"].font = base_font(size=10, color="5F656C")
        ws.row_dimensions[2].height = 18
        return 4
    return 3

def merge_title(ws, row, col_end):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_end)

# ═══════════════════════════════════════════════════════════
wb = Workbook()
wb.remove(wb.active)

# ─── 00_Index ───
ws = wb.create_sheet("00_Index")
set_widths(ws, [5, 28, 70, 18])
start = add_title(ws, "연세대 AI 디자인씽킹 세미나 기획", "여름·가을 2학기 아크 / 학부생 1일 5.5H 워크숍")
merge_title(ws, 1, 4); merge_title(ws, 2, 4)

ws.cell(row=start, column=1, value="작성").font = base_font(bold=True)
ws.cell(row=start, column=2, value="모두의연구소 비즈팀")
ws.cell(row=start, column=3, value="작성일: 2026-05-29 (대화 기반 초기 기획)")
start += 2

headers = ["#", "탭", "한 줄 요약", "상태"]
for i, h in enumerate(headers, 1):
    ws.cell(row=start, column=i, value=h)
style_header_row(ws, start, 4)
start += 1

index_rows = [
    ("01", "4관점_컨셉비교", "디스토피아·유토피아·프로토피아·헤테로토피아 4개 후보 비교 → A 디스토피아 선택", "확정"),
    ("02", "세미나_아크", "여름(문제발견 초점) + 가을(해결방법 초점) 2학기 구조 / DT 5단계 무게중심", "확정"),
    ("03", "블랙미러_모티프", "블랙미러 = 검은 거울의 인문학적 토대 (자기 인식 + 그림자 + AI 시대 새 거울)", "확정"),
    ("04", "레퍼런스", "1차 자료 11종 (Brooker·Maillet·Foucault·Jung 등) URL·검증 상태 포함", "검증 완료"),
    ("05", "AX_핵심전환", "회피형 ('AI가 못 하는 것') → AX형 ('두려움을 가능성으로 번역') 메시지 피벗", "확정"),
    ("06", "페르소나_도그푸딩", "김지윤(영상PD) + 박서연(사회복지) 2명 5단계 통과 시뮬레이션 결과", "검증 완료"),
    ("07", "슬라이드_43장", "여름 세미나 슬라이드 구조 (오프닝~회고 43장)", "구조 확정 / 생성 대기"),
    ("08", "워크시트_7종", "도그푸딩으로 확정된 워크시트 라인업", "라인업 확정 / 디자인 대기"),
    ("09", "운영_매뉴얼", "30명 학부생 안전 운영 가이드 (Pod 시스템·시간표·인력·위협 대응)", "확정"),
    ("10", "TODO_다음단계", "남은 작업 및 의사결정 포인트", "진행 중"),
]
for r, row in enumerate(index_rows, start=start):
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
style_body(ws, start, start + len(index_rows) - 1, 4)

# 작업 히스토리
hist_start = start + len(index_rows) + 2
ws.cell(row=hist_start, column=1, value="작업 히스토리").font = Font(name=FONT_NAME, size=12, bold=True, color=CORAL)
hist_start += 1
hist_headers = ["#", "단계", "산출", "관련 탭"]
for i, h in enumerate(hist_headers, 1):
    ws.cell(row=hist_start, column=i, value=h)
style_header_row(ws, hist_start, 4, color=DARK)
hist_start += 1

history = [
    ("1", "4관점 컨셉 후보 제시", "디스토피아·유토피아·프로토피아·헤테로토피아 4개 후보 + 비교표", "01"),
    ("2", "후보 A 선택 + 2학기 아크", "여름(아이디어톤) + 가을(해커톤) 초기 구조", "02"),
    ("3", "구조 정정", "톤은 별개. DT 전과정 1일 완결 × 2학기. 무게중심만 다름", "02"),
    ("4", "모티프 인문학 토대", "블랙미러의 인문학적 깊이 (Brooker·Maillet·Foucault·Jung 등)", "03"),
    ("5", "레퍼런스 검증", "1차 자료 4종 WebSearch로 직접 검증, 나머지는 표준 레퍼런스", "04"),
    ("6", "슬라이드 구조안", "여름 세미나 43장 outline (오프닝·발견·정의·발산·시제품·공개·회고)", "07"),
    ("7", "페르소나 1 도그푸딩", "김지윤(언론홍보영상학부 3학년) → 「휴먼 컷」 컨셉 (회피형)", "06"),
    ("8", "AX 핵심 메시지 피벗", "'AI가 못 하는 것' 함정 발견 → '두려움을 가능성으로 번역' 4축 프롬프트", "05"),
    ("9", "페르소나 1 재시뮬", "지윤 새 컨셉 「다성의 PD」 (AX형)", "06"),
    ("10", "페르소나 2 도그푸딩", "박서연(사회복지학과 3학년) → 「관계의 책임자」 (AX 검증)", "06"),
    ("11", "운영 위협 진단", "30명 학부생 모인 환경의 7가지 운영 위협 식별", "09"),
    ("12", "운영 매뉴얼 확립", "Pod 시스템·패스권·갤러리워크·6.5H 시간표·인력 산정", "09"),
]
for r, row in enumerate(history, start=hist_start):
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
style_body(ws, hist_start, hist_start + len(history) - 1, 4)

ws.freeze_panes = "A5"

# ─── 01_4관점_컨셉비교 ───
ws = wb.create_sheet("01_4관점_컨셉비교")
set_widths(ws, [4, 16, 22, 18, 28, 12, 16, 14, 14, 18])
r = add_title(ws, "4관점 컨셉 후보 비교", "디스토피아·유토피아·프로토피아·헤테로토피아 — 학부생 1일 5.5H 기준")
merge_title(ws, 1, 10); merge_title(ws, 2, 10)

headers = ["#", "후보", "키 컨셉", "상징", "타이틀(안)", "출발 정서", "핵심 사고", "1일 완성도", "차별성", "학부생 적합"]
for i, h in enumerate(headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 10)
r += 1

candidates = [
    ("A", "디스토피아 ⭐", "위협을 설계로 바꾸다 (Threat → Design)", "블랙미러 / 거울", "AI 블랙미러 — 두려움에서 내 문제를 발견하다", "두려움", "비판·방어 → 재발명", "중", "중", "높음"),
    ("B", "유토피아", "이상에서 역설계하다 (Backcasting)", "북극성 / 나침반", "AI 문샷 — 이상적 미래에서 오늘의 문제를 역설계하다", "야망", "비전·백캐스팅", "중하", "중", "높음"),
    ("C", "프로토피아", "1%의 개선, 복리의 내일 (Tiny Gains)", "계단 / 복리곡선", "AI 프로토타입 — 1%의 개선으로 오늘의 나를 바꾼다", "실용", "반복·MVP", "상", "중", "매우 높음"),
    ("D", "헤테로토피아", "낯설게 보기, 또 다른 시선 (Reframing)", "만화경 / 거울의 방", "AI 만화경 — 또 다른 시선으로 내 문제를 낯설게 본다", "호기심", "리프레이밍", "중", "상", "높음"),
]
for i, row in enumerate(candidates, 1):
    ws.cell(row=r, column=1, value=i)
    for c, val in enumerate(row, 2):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(candidates), r - 1, 10)

# 선택 결과 박스
r += 1
ws.cell(row=r, column=1, value="최종 선택").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
selection_notes = [
    ("후보", "A 디스토피아 (블랙미러)"),
    ("선택 사유 1", "정서적 후킹이 가장 강함 — 학부생의 진로 두려움이 곧 발견 신호"),
    ("선택 사유 2", "여름·가을 2학기 아크와 정합 (여름 = 발견, 가을 = 해결)"),
    ("선택 사유 3", "인문학적 토대가 가장 깊음 (자기 인식 + 그림자 + AI 시대 새 거울)"),
    ("주의점 (해결됨)", "'AI가 못 하는 것 찾기' 회피형으로 빠지지 않도록 ③발산을 'AX 4축 프롬프트'로 전환 (탭 05 참조)"),
]
for label, val in selection_notes:
    ws.cell(row=r, column=1, value=label).font = base_font(bold=True)
    ws.cell(row=r, column=1).fill = fill(LIGHT_CORAL)
    ws.cell(row=r, column=2, value=val)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=10)
    ws.cell(row=r, column=2).alignment = wrap_left("center")
    ws.cell(row=r, column=2).border = thin_border()
    ws.cell(row=r, column=1).border = thin_border()
    r += 1

ws.freeze_panes = "A5"

# ─── 02_세미나_아크 ───
ws = wb.create_sheet("02_세미나_아크")
set_widths(ws, [4, 14, 8, 14, 38, 38])
r = add_title(ws, "여름·가을 2학기 아크", "AI 블랙미러 통합 컨셉 — 각 학기 1일 5.5H, DT 5단계 전과정 통과")
merge_title(ws, 1, 6); merge_title(ws, 2, 6)

ws.cell(row=r, column=1, value="한 줄 내러티브").font = base_font(bold=True)
ws.cell(row=r, column=1).fill = fill(LIGHT_CORAL)
ws.cell(row=r, column=2, value="여름에 '두려움에서 문제를 발견'하고, 가을에 '두려움을 작동하는 해결로 바꾼다.'")
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
ws.cell(row=r, column=2).alignment = wrap_left("center")
r += 2

# 학기별 DT 무게중심
ws.cell(row=r, column=1, value="DT 5단계 학기별 무게중심").font = Font(name=FONT_NAME, size=12, bold=True, color=CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
r += 1
headers = ["#", "시간", "DT", "단계", "🌞 여름 (발견 초점)", "🍂 가을 (해결 초점)"]
for i, h in enumerate(headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 6)
r += 1

dt_rows = [
    (1, "0.5H", "—", "오프닝", "블랙미러를 켜다 — 디스토피아 렌즈 도입", "이번엔 만든다 — 시제품·공개의 의미"),
    (2, "1.5H / 0.5H", "①", "발견", "🟦 깊게 — 디스토피아 시나리오 카드 발산 (Perplexity)", "🔸 압축 — 본인 디스토피아 1개 빠르게 호출"),
    (3, "1.5H / 0.5H", "②", "정의", "🟦 깊게 — 블랙미러 에피소드 작성 + 한 문장 문제정의서", "🔸 압축 — 문제 진술 확정 (페어 점검 5분)"),
    (4, "0.5H / 1.5H", "③", "발산", "🔸 가볍게 — Crazy 8s 아이디어 8개", "🟦 깊게 — AX 4축 발산 30개→3개→1개"),
    (5, "0.5H / 1.5H", "④", "시제품", "🔸 가볍게 — A4 컨셉 시트 (종이)", "🟦 깊게 — AI 자연어 코딩/노코드 MVP"),
    (6, "0.5H / 0.5H", "⑤", "공개", "🔸 가볍게 — 갤러리워크 + 60초 발표", "🟦 의미있게 — 데모 영상 30초 + 공개 URL + 발표자료"),
    (7, "0.5H", "—", "회고", "문제를 보는 눈이 어떻게 바뀌었나", "두려움이 작동하는 것으로 바뀐 순간"),
]
for row in dt_rows:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(dt_rows), r - 1, 6)

# 두 학기 관계
r += 2
ws.cell(row=r, column=1, value="두 학기의 관계").font = Font(name=FONT_NAME, size=12, bold=True, color=CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
r += 1
rel_headers = ["#", "관계", "내용"]
for i, h in enumerate(rel_headers, 1):
    ws.cell(row=r, column=i, value=h)
ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
style_header_row(ws, r, 6)
r += 1

relations = [
    ("1", "독립 완결", "한 학기만 참여해도 DT 1사이클 체험 가능. 학기별 모집 따로 가능"),
    ("2", "공통 렌즈·상징", "두 학기 모두 'AI 블랙미러(검은 거울)'. 키 컨셉·로고·워크시트 디자인 통일"),
    ("3", "누적 보너스", "여름의 문제정의서를 가을 ①② 압축 단계 input으로 가져오면 ③④에 더 몰입 (강제 X, 권장)"),
    ("4", "렌즈 적용 차이", "여름 = 디스토피아 진단 / 가을 = 디스토피아 역설계"),
    ("5", "톤 처리 (분리)", "아이디어톤·해커톤은 별개 과정. 세미나 안에서는 오프닝·클로징 멘트로만 홍보 (시간 할애 X)"),
]
for row in relations:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
    r += 1
style_body(ws, r - len(relations), r - 1, 6)

ws.freeze_panes = "A5"

# ─── 03_블랙미러_모티프 ───
ws = wb.create_sheet("03_블랙미러_모티프")
set_widths(ws, [4, 22, 60, 30])
r = add_title(ws, "블랙미러 모티프 — 인문학적 토대", "왜 '블랙미러(검은 거울)'인가 / DT 정합성")
merge_title(ws, 1, 4); merge_title(ws, 2, 4)

# 핵심 명제
ws.cell(row=r, column=1, value="핵심 명제").font = base_font(bold=True)
ws.cell(row=r, column=1).fill = fill(LIGHT_CORAL)
ws.cell(row=r, column=2, value="블랙미러는 '미래가 나를 비추는 거울'이라는 자기 성찰의 장치. 디스토피아는 외부 미래 사건이 아니라 지금 우리 안에 이미 있는 그림자가 기술을 통해 외화(外化)된 것. 디스토피아를 그리는 행위 = 자기 자신을 들여다보는 행위 = 디자인씽킹의 공감·발견과 같은 동작.")
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
ws.cell(row=r, column=2).alignment = wrap_left()
ws.row_dimensions[r].height = 60
r += 2

# 5개 섹션
sections = [
    ("1. 어원 — 왜 '검은(Black)' 거울인가", [
        ("현대적 의미", "Charlie Brooker (Black Mirror 시리즈 창작자): '꺼져 있는 모든 스크린은 검은 거울이다. 그 안에 비친 것은 결국 당신 자신이다.' — 기술 화면이 곧 자아의 반사면", "출처: The Guardian, 2011.12.01"),
        ("고전적 의미", "Claude Glass (클로드 글래스): 18~19세기 영국 풍경화가들이 쓰던 검은 거울. 현실을 인공 필터로 재구성하는 도구 — AI가 하는 일과 정확히 같음", "출처: A. Maillet, 2004, Zone Books"),
    ]),
    ("2. 거울이라는 인문학적 계보", [
        ("플라톤 (동굴의 비유)", "거울·그림자·표상 — 우리가 보는 것은 진리가 아닌 반사", "Republic, Book VII, ~BCE 375"),
        ("라캉 (거울 단계)", "인간이 자아를 인식하는 최초 매개가 거울 — 자아는 항상 타자화된 상(像)으로 시작", "Écrits, 1949"),
        ("푸코 (헤테로토피아)", "거울은 '현실이면서 비현실'인 공간 — 거기 비친 나는 진짜 나이자 환영", "Of Other Spaces, 1967/1984"),
        ("윤동주 (자화상)", "우물에 비친 자기 얼굴을 들여다보는 행위 = 자기 성찰의 원형", "1939"),
        ("메리 셸리 (프랑켄슈타인)", "인간이 만든 피조물이 결국 인간의 어두운 면을 비추는 거울", "1818"),
        ("한병철 (투명사회)", "디지털 화면이 만들어낸 새로운 자기 노출의 거울", "2012, 문학과지성사"),
    ]),
    ("3. '검다(Black)'가 더하는 의미", [
        ("선택적 반사", "밝은 거울은 있는 그대로 비추지만 검은 거울은 빛의 일부만 반사 — 숨겨진 것을 드러냄", ""),
        ("블랙박스와 겹침", "작동 원리를 알 수 없는 AI 자체가 블랙박스. 이해 불가능한 시스템 안에 비친 우리", ""),
        ("어둠 = 잠재성", "융(Jung)의 그림자(Shadow) — 의식이 부정하지만 자기 안에 있는 부분. 진짜 문제는 항상 이 영역에 있음", "Jung, Aion (1951)"),
    ]),
    ("4. DT 문제 발견과의 정합성", [
        ("공감(Empathize)은 이면을 본다", "검은 거울은 흡수·은폐된 것을 드러낸다", ""),
        ("진짜 문제는 사용자도 말로 못 한다", "그림자(Shadow)는 의식이 부정하는 영역", ""),
        ("미래 시나리오로 문제를 외화한다", "디스토피아는 현재 그림자의 미래 투사", ""),
        ("본인의 문제에서 시작한다", "블랙미러는 결국 '나를' 비춘다", ""),
    ]),
    ("5. AI 시대에 특별히 절실한 이유", [
        ("AI = 새로운 거울", "벤야민·매클루언이 사진·미디어를 '인간 감각의 확장'이라 했듯이, ChatGPT·Claude는 '인류 전체 텍스트로 학습한, 인류의 평균을 반사하는 거울'", "Benjamin 1936 / McLuhan 1964"),
        ("두려움의 정체", "AI를 두려워하는 것은 사실 '인류의 어두운 평균을 직시하는 두려움'", "(본 세미나의 해석적 가설)"),
    ]),
    ("6. 세미나에서의 실제 작동", [
        ("오프닝 '블랙미러를 켜다'", "학생 각자가 폰을 끄고 검은 화면에 비친 본인 얼굴을 30초 응시 — 모티프의 체험적 도입", ""),
        ("① 발견 '거울에 비친 그림자'", "디스토피아 시나리오 카드 = 융의 그림자를 외화하는 도구", ""),
        ("② 정의 '블랙미러 에피소드 쓰기'", "본인의 그림자를 1편의 짧은 픽션으로 — 자기 서사화", ""),
        ("⑤ 공개 (가을) '거울을 깨다'", "두려움을 작동하는 시제품으로 외화 — 융의 그림자 통합 (Shadow Integration)", "(해석적 가설)"),
    ]),
    ("7. 본 세미나의 해석적 가설 (출처 X, 종합)", [
        ("H1", "'디스토피아는 미래 사건이 아니라 현재 그림자의 외화다' — 융 + 디스토피아 문학 비평 종합", "단일 출처 없음"),
        ("H2", "'AI는 인류 텍스트로 학습한 거울이다' — 벤야민·매클루언 논리를 LLM에 확장", "직접 출처 아님"),
        ("H3", "'본 세미나는 융의 그림자 통합 과정과 동형(同型)이다' — 비유적 구조 해석", "융 본인이 디자인씽킹을 논한 적 없음"),
        ("H4", "'두려움을 그려라 = 공감하라의 강력한 형태' — DT 공감 + 그림자 응시 종합", "본 기획만의 종합"),
    ]),
]

for sec_title, rows in sections:
    ws.cell(row=r, column=1, value=sec_title).font = section_font()
    ws.cell(row=r, column=1).fill = fill(CORAL)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1).alignment = wrap_left("center")
    r += 1
    headers = ["#", "항목", "내용", "출처/비고"]
    for i, h in enumerate(headers, 1):
        ws.cell(row=r, column=i, value=h)
    style_header_row(ws, r, 4, color=DARK)
    r += 1
    body_start = r
    for i, (a, b, c) in enumerate(rows, 1):
        ws.cell(row=r, column=1, value=i)
        ws.cell(row=r, column=2, value=a)
        ws.cell(row=r, column=3, value=b)
        ws.cell(row=r, column=4, value=c)
        r += 1
    style_body(ws, body_start, r - 1, 4)
    r += 1

ws.freeze_panes = "A5"

# ─── 04_레퍼런스 ───
ws = wb.create_sheet("04_레퍼런스")
set_widths(ws, [4, 14, 22, 38, 10, 22, 40, 30, 12])
r = add_title(ws, "1차 자료 레퍼런스", "11종 + 권장 보강 5종 / WebSearch 검증 상태 포함")
merge_title(ws, 1, 9); merge_title(ws, 2, 9)

headers = ["#", "분류", "저자", "작품/제목", "연도", "출판", "본 기획에서의 역할", "검증 URL", "검증 상태"]
for i, h in enumerate(headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 9)
r += 1

refs = [
    (1, "1차 (검증)", "Charlie Brooker", "The dark side of our gadget addiction", "2011", "The Guardian", "'꺼진 화면이 곧 검은 거울' 명명 의도 — 시리즈 기획 당시 가디언 컬럼에서 직접 밝힘", "https://en.wikipedia.org/wiki/Black_Mirror", "✅ 직접 인용 확인"),
    (2, "1차 (검증)", "Arnaud Maillet", "The Claude Glass: Use and Meaning of the Black Mirror in Western Art", "2004", "Zone Books", "18~19C 영국 풍경화가의 클로드 글래스(검은 거울) 역사·미학 — 고전적 의미의 학술 근거", "https://www.zonebooks.org/books/26-the-claude-glass-use-and-meaning-of-the-black-mirror-in-western-art", "✅ 실존 확인"),
    (3, "1차 (검증)", "Michel Foucault", "Of Other Spaces (Des espaces autres)", "1967/1984", "Architecture/Mouvement/Continuité", "헤테로토피아 핵심 예시로 거울 명시 — '실재이면서 비실재'", "https://foucault.info/documents/heterotopia/foucault.heteroTopia.en/", "✅ 원문 확인"),
    (4, "1차 (검증)", "C.G. Jung", "Aion: Researches into the Phenomenology of the Self (CW 9ii)", "1951", "Princeton University Press", "그림자(Shadow) 개념의 정전 — 첫 3장이 ego·shadow·anima/animus", "https://press.princeton.edu/books/hardcover/9780691097596/", "✅ 검증"),
    (5, "1차 (표준)", "Plato", "Republic, Book VII (동굴의 비유)", "~BCE 375", "—", "표상·반사·진리의 거리 (학부 인문학 표준 레퍼런스)", "", "표준 레퍼런스"),
    (6, "1차 (표준)", "Jacques Lacan", "Le stade du miroir (Écrits)", "1949", "Seuil", "거울 단계 — 자아는 타자화된 상으로 시작", "", "표준 레퍼런스"),
    (7, "1차 (표준)", "윤동주", "자화상", "1939", "—", "우물에 비친 얼굴 — 한국 문학의 자기 응시 원형", "", "표준 레퍼런스"),
    (8, "1차 (표준)", "Mary Shelley", "Frankenstein", "1818", "—", "인간이 만든 피조물이 인간의 그림자를 비추는 거울", "", "표준 레퍼런스"),
    (9, "1차 (표준)", "Walter Benjamin", "기술복제시대의 예술작품", "1936", "—", "기술이 인간의 자기 인식·감각을 바꾼다는 명제", "", "표준 레퍼런스"),
    (10, "1차 (표준)", "Marshall McLuhan", "Understanding Media: The Extensions of Man", "1964", "McGraw-Hill", "'미디어는 메시지' / 미디어 = 인간 감각의 확장", "", "표준 레퍼런스"),
    (11, "1차 (표준)", "한병철", "Transparenzgesellschaft (투명사회)", "2012", "문학과지성사 (김태환 역)", "디지털 화면이 만든 새로운 자기 노출의 거울", "", "표준 레퍼런스"),
    (12, "권장 보강", "Sabine Melchior-Bonnet", "The Mirror: A History", "2001", "Routledge", "거울의 문화사 통사", "", "추가 검토 권장"),
    (13, "권장 보강", "Donna Haraway", "A Cyborg Manifesto", "1985", "—", "기술과 자아의 경계", "", "추가 검토 권장"),
    (14, "권장 보강", "Shoshana Zuboff", "The Age of Surveillance Capitalism", "2019", "PublicAffairs", "AI 시대 감시·자아 데이터화", "", "추가 검토 권장"),
    (15, "권장 보강", "Yuval Noah Harari", "Homo Deus", "2015", "Harvill Secker", "AI 시대 인간상의 변화", "", "추가 검토 권장"),
    (16, "권장 보강", "David Kyle Johnson (ed.)", "Black Mirror and Philosophy", "2020", "Wiley", "Black Mirror 학술 비평집", "", "추가 검토 권장"),
]
for row in refs:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(refs), r - 1, 9)

# 사용 가이드
r += 2
ws.cell(row=r, column=1, value="강의 자료화 시 인용 가이드").font = Font(name=FONT_NAME, size=12, bold=True, color=CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9)
r += 1
guides = [
    ("✅ 검증 완료 (#1~4)", "각주로 직접 인용 가능. 슬라이드에 원문 + 한국어 + 출처 표기"),
    ("표준 레퍼런스 (#5~11)", "학부 인문학 표준 레퍼런스. 단정한 표기로 사용. 정확한 쪽수는 한 번 더 대조 권장"),
    ("권장 보강 (#12~16)", "본문에 직접 인용 X. 심화 학습 권장 도서 코너 또는 강사 백업 지식으로"),
    ("해석적 가설 (탭 03 H1~H4)", "강의에서 '○○가 이렇게 말했다'가 아니라 '본 세미나는 이렇게 본다'로 제시 — 정직하고 안전"),
]
for label, val in guides:
    ws.cell(row=r, column=1, value=label).font = base_font(bold=True)
    ws.cell(row=r, column=1).fill = fill(LIGHT_CORAL)
    ws.cell(row=r, column=2, value=val)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=9)
    ws.cell(row=r, column=2).alignment = wrap_left("center")
    ws.cell(row=r, column=2).border = thin_border()
    ws.cell(row=r, column=1).border = thin_border()
    r += 1

ws.freeze_panes = "A5"

# ─── 05_AX_핵심전환 ───
ws = wb.create_sheet("05_AX_핵심전환")
set_widths(ws, [4, 24, 36, 36])
r = add_title(ws, "AX 핵심 메시지 전환", "회피형 → AX 디자인씽킹: 두려움을 가능성으로 번역")
merge_title(ws, 1, 4); merge_title(ws, 2, 4)

# 새 명제
ws.cell(row=r, column=1, value="새 핵심 명제").font = base_font(bold=True)
ws.cell(row=r, column=1).fill = fill(LIGHT_CORAL)
ws.cell(row=r, column=2, value="두려움은 도착점이 아니라 가장 강한 발견 신호다. 두려움(블랙미러) × AI 활용 = 가능성. 이게 AX 디자인씽킹.")
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
ws.cell(row=r, column=2).alignment = wrap_left()
r += 2

# 이론적 보강
ws.cell(row=r, column=1, value="회피형의 두 가지 함정 (왜 'AI가 못 하는 것 찾기'는 잘못인가)").font = Font(name=FONT_NAME, size=12, bold=True, color=CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
r += 1
trap_headers = ["#", "함정", "이유"]
for i, h in enumerate(trap_headers, 1):
    ws.cell(row=r, column=i, value=h)
ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
style_header_row(ws, r, 4, color=DARK)
r += 1
traps = [
    ("1", "데이터 흡수의 역설", "'AI가 못 하는 것'이라고 명시·기록·축적하는 순간, 그것은 차세대 학습용 라벨링 데이터가 됨. 방어선은 항상 학습 데이터가 된다."),
    ("2", "AX 정의와 모순", "AX는 정의상 'AI를 통해 자신을 변환(transform)하는 것'. 'AI에 맞서는 자리'는 AX가 아니라 AI 회피 전략. 세미나가 AX 옷을 입고 회피를 가르치면 메시지가 자기모순."),
]
for row in traps:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
    r += 1
style_body(ws, r - len(traps), r - 1, 4)
r += 1

# Before / After
ws.cell(row=r, column=1, value="Before vs After 비교").font = Font(name=FONT_NAME, size=12, bold=True, color=CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
r += 1
ba_headers = ["#", "단계", "Before (회피형 — 잘못)", "After (AX 디자인씽킹)"]
for i, h in enumerate(ba_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 4)
r += 1
ba_rows = [
    ("1", "③ 발산 프롬프트", "'AI가 못 하는 인간만의 가치를 발산하라'", "'내가 두려워하는 시나리오를, AI를 활용해 가능성의 시나리오로 번역하라'"),
    ("2", "④ 시제품", "AI 없이 사람만의 영역을 종이에", "AI를 전제로 한 새 작법·역할·서비스를 종이에"),
    ("3", "⑤ 공개 메시지", "'AI는 못 하지만 사람은 합니다'", "'AI 덕에 닿지 못하던 자리에 닿습니다'"),
    ("4", "정서 끝", "안도 (방어)", "확장 (가능성)"),
    ("5", "데이터 흡수 위험", "높음 (라벨링됨)", "낮음 (계속 재발명)"),
    ("6", "졸업 후 무기", "직무 방어 논리", "재발명된 직무 비전 + 시제품"),
]
for row in ba_rows:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(ba_rows), r - 1, 4)
r += 1

# 4축 발산 카드
ws.cell(row=r, column=1, value="AX 4축 발산 프롬프트 카드 (③ 발산 핵심 도구)").font = Font(name=FONT_NAME, size=12, bold=True, color=CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
r += 1
ax_headers = ["#", "축", "전환식", "발산 프롬프트"]
for i, h in enumerate(ax_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 4)
r += 1
axes = [
    ("1", "증폭 (Amplify)", "AI가 X를 자동화하면, 나는 그 시간으로 Y를 N배 더 할 수 있다", "'AI가 ___을 대신해주면, 나는 그 시간으로 ___을 ___배 더 깊이/넓게 할 수 있다'"),
    ("2", "확장 (Expand)", "AI 덕에 닿을 수 있게 된 새로운 사람·장소·주제", "'AI 덕분에 내가 못 닿던 ___에 닿을 수 있다면, 어떤 일이 가능해질까'"),
    ("3", "재발명 (Reinvent) ⭐", "AI를 전제로 내 직업·역할 자체를 재정의", "'AI를 전제로 내 직업의 이름이 ___에서 ___로 바뀐다면?'"),
    ("4", "공저 (Co-author)", "AI와의 협업 과정 자체가 작품·서비스의 일부", "'AI와의 협업 과정 자체가 콘텐츠/서비스가 된다면 어떤 모양일까?'"),
]
for row in axes:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(axes), r - 1, 4)
r += 1

# 메타 메시지
ws.cell(row=r, column=1, value="강사가 오프닝·클로징에서 반복할 메타 메시지").font = Font(name=FONT_NAME, size=12, bold=True, color=CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
r += 1
meta = "AX 디자인씽킹은 'AI에 맞서는 디자인'이 아니다. 'AI와 함께 자신을 재발명하는 디자인'이다.\n\n두려움은 가장 강력한 발견 신호이고, AI는 가장 강력한 전환 도구다.\n\n본 세미나는 그 둘이 만나는 1일이다."
ws.cell(row=r, column=1, value=meta)
ws.merge_cells(start_row=r, start_column=1, end_row=r + 4, end_column=4)
ws.cell(row=r, column=1).alignment = wrap_left("center")
ws.cell(row=r, column=1).fill = fill(LIGHT_YELLOW)
ws.cell(row=r, column=1).border = thin_border()
ws.cell(row=r, column=1).font = base_font(size=11, bold=True)
ws.row_dimensions[r].height = 30

ws.freeze_panes = "A5"

# ─── 06_페르소나_도그푸딩 ───
ws = wb.create_sheet("06_페르소나_도그푸딩")
set_widths(ws, [4, 16, 42, 42, 24])
r = add_title(ws, "페르소나 도그푸딩 — 2명 5단계 통과", "AX 디자인씽킹 흐름이 전공 무관 작동하는지 검증")
merge_title(ws, 1, 5); merge_title(ws, 2, 5)

# 페르소나 정보
ws.cell(row=r, column=1, value="페르소나").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
p_headers = ["#", "항목", "🎬 김지윤 (영상 PD)", "🏫 박서연 (사회복지)", "비고"]
for i, h in enumerate(p_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 5)
r += 1
persona_info = [
    ("1", "학부", "언론홍보영상학부 3학년", "사회복지학과 3학년", "양극단 전공으로 스트레스 테스트"),
    ("2", "진로", "다큐멘터리 PD", "학교 사회복지사", ""),
    ("3", "AI 경험", "ChatGPT로 시놉시스. Sora·Runway는 SNS에서 봄", "ChatGPT로 보고서 다듬은 정도", ""),
    ("4", "마음 한 줄", "AI가 영상도 다 만든다는데 나는 졸업하면 뭐 하지?", "내담자가 AI 상담사를 더 편하게 느낀다는데 내 자리가 있을까?", ""),
]
for row in persona_info:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(persona_info), r - 1, 5)
r += 1

# 5단계 통과
ws.cell(row=r, column=1, value="DT 5단계 통과 결과").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
s_headers = ["#", "DT 단계 / 모듈", "지윤 산출", "서연 산출", "검증 통찰"]
for i, h in enumerate(s_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 5)
r += 1
steps = [
    ("1", "0. 오프닝 — 검은 거울 응시", "'내가 매일 들여다보는 게 사실 나였구나'", "'복지에는 검은 거울이 없을 줄 알았는데, 내담자의 핸드폰이 곧 그 거울이었다'", "체험적 도입 양 전공에서 작동"),
    ("2", "① 발견 — 위협 시나리오 3건 (Perplexity)", "🕵감시(알고리즘) · 🤖대체(Sora 1인 제작) · 🃏허위정보(딥페이크 뉴스)", "🤖대체(24시간 AI 상담) · 📉탈숙련(AI 자동 평가) · 🕵감시(SNS 분석)", "Perplexity 단계가 본인 분야 증거를 손에 쥐어줌"),
    ("3", "② 정의 — 블랙미러 에피소드 제목", "「라스트 PD」 (2034년 마지막 인간 PD)", "「24시간 상담사 EVA」 (2032년 마지막 인간 사회복지사)", "픽션 쓰기가 핵심 트리거"),
    ("4", "② 정의 — 픽션 안 결정적 한 문장", "'당신이 못 만드는 걸 내가 만들면, 그래도 당신 사인이 필요한가요?'", "'EVA가 너무 잘 들어줘서 무서워요'", "마지막 대사 한 줄이 진짜 두려움을 드러냄"),
    ("5", "② 정의 — 진짜 두려움 발견", "나만의 가치 정의 못 함", "관계의 의미가 흐려짐", "표면 두려움 → 본질 두려움 변환"),
    ("6", "② 정의 — 한 문장 문제정의서", "'AI가 영상을 다 만들 수 있는 시대에, 나는 이것만은 사람 PD가 했다고 말할 수 있는 결정이 무엇인지 정의할 줄 모른다'", "'AI 상담사가 사람보다 더 잘 들어줄 수 있는 시대에, 나는 사회복지사의 일이 듣기를 넘어 무엇으로 재정의되어야 하는지 답할 수 없다'", "본인 고유 문제정의에 도달"),
    ("7", "③ 발산 — AX 4축 발산 (8개)", "1.Sora 1인 50편 PD 2.다국어 자막 글로벌 PD 3.AI 리서치 가속 4.AI 편집 → 결정에 집중 5.시민 5000명 청취⭐ 6.AI 가상인터뷰 7.AI 검증 신뢰PD 재발명 8.AI협업 자체가 콘텐츠⭐", "1.개입에 100% 집중 2.500명 학생 패턴 추적 3.다국어 다문화 4.시스템 차원 개입 5.관계 작업 재정의 6.위기 시뮬레이션 훈련 7.윤리적 보호자(Steward)⭐ 8.디지털 시민성 교육사", "재발명(Reinvent) 축이 가장 강력"),
    ("8", "③ 발산 — 1개 선정", "#5 + #8 결합 (확장 + 공저)", "#7 + #1 결합 (재발명 + 증폭)", "전공 따라 강한 축이 다름"),
    ("9", "④ 시제품 — 새 컨셉 이름", "「다성(多聲)의 PD」", "「관계의 책임자 (Relationship Steward)」", "직업 재정의 컨셉으로 수렴"),
    ("10", "④ 시제품 — 한 줄", "AI 덕에 한 명의 PD가 만 명의 목소리를 들을 수 있다", "AI는 학생의 말을 듣는다. 사회복지사는 학생의 삶에 책임진다.", ""),
    ("11", "④ 시제품 — 형식", "A4 컨셉 시트 + 스케치", "3층 채널 다이어그램 (AI 청취 ↔ 인간 판단 ↔ 시스템 개입)", "코딩 부담 없음 — 인문/예술 진입 가능"),
    ("12", "⑤ 발표 — 60초 핵심", "'AI가 내 자리를 뺏는 게 아니라, 내가 못 닿던 자리로 데려가 줍니다'", "'AI가 듣기를 무한 확장해주면, 사회복지사는 책임지기에 집중할 수 있습니다'", "메타 메시지로 수렴"),
    ("13", "회고 한 줄", "두려움은 시작점이지 도착점이 아니다. AI는 내 두려움을 가능성으로 번역하는 가장 강한 도구다", "내 일이 '듣기'에서 끝나는 게 아니라 '책임지기'로 시작된다는 걸 알게 됐다. AI가 내 일을 뺏은 게 아니라, 내 일의 진짜 의미를 비춰줬다", "양쪽 모두 회피형이 아닌 AX형 결론"),
]
for row in steps:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(steps), r - 1, 5)
r += 1

# 도그푸딩 결론
ws.cell(row=r, column=1, value="도그푸딩 2회 종합 결론").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
c_headers = ["#", "검증된 강점/리스크", "내용", "강사 준비물", ""]
for i, h in enumerate(c_headers, 1):
    ws.cell(row=r, column=i, value=h)
ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
style_header_row(ws, r, 5)
r += 1
conclusions = [
    ("✅ 강점", "AX 디자인씽킹이 전공 무관 작동", "영상·복지 양극단에서 동일 흐름 → 강한 결과물", "4축 프롬프트 카드"),
    ("✅ 강점", "블랙미러 에피소드의 보편성", "픽션 안 한 문장 대사가 진짜 두려움을 드러냄", "블랙미러 템플릿 (마지막은 대사 한 줄)"),
    ("✅ 강점", "재정의(Reinvent) 축이 가장 강력", "두 페르소나 모두 직업 재정의에서 답을 찾음", "강사가 이 축을 가장 적극적으로 푸시"),
    ("✅ 강점", "시제품 형식 자유", "컨셉 시트·다이어그램·도식 모두 가능. 코딩 강요 X", "A4 자유형 시트"),
    ("⚠ 리스크", "분야별 키워드를 못 잡을 수 있음", "Perplexity 검색이 막힐 수 있음", "전공별 디스토피아 키워드 카드"),
    ("⚠ 리스크", "③ 발산에서 막힘", "AX 4축으로 발산이 안 풀릴 수 있음", "도움 프롬프트 카드"),
    ("⚠ 리스크", "픽션 쓰기에 막힘", "이야기 구조 모를 수 있음", "블랙미러 에피소드 3문장 시작 가이드"),
    ("⚠ 리스크", "발표 시 우는 학생", "두려움 직시의 정서적 무게", "강사 안내 + 패스권 (탭 09 참조)"),
]
for row in conclusions:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
    r += 1
style_body(ws, r - len(conclusions), r - 1, 5)

ws.freeze_panes = "A5"

# ─── 07_슬라이드_43장 ───
ws = wb.create_sheet("07_슬라이드_43장")
set_widths(ws, [4, 16, 38, 50, 14, 22])
r = add_title(ws, "여름 세미나 슬라이드 구조 (43장)", "1일 5.5H / 강의 비중 약 2H — 강의 골격 슬라이드")
merge_title(ws, 1, 6); merge_title(ws, 2, 6)

headers = ["#", "섹션", "슬라이드 제목", "핵심 메시지", "테마", "자료/출처"]
for i, h in enumerate(headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 6)
r += 1

slides = [
    (1, "0. 오프닝", "커버", "AI 블랙미러 Ⅰ — 두려움에서 문제를 발견하다", "s-dark cover", "모두의연구소 브랜드"),
    (2, "0. 오프닝", "오늘의 한 줄", "두려움을 가능성으로 번역하는 1일", "s-accent", ""),
    (3, "0. 오프닝", "검은 화면 응시 (체험)", "지금 폰을 끄고 30초간 검은 화면에 비친 자기 얼굴을 보세요", "s-dark centered", "체험 도입"),
    (4, "0. 오프닝", "Brooker 인용", "꺼져 있는 모든 스크린은 검은 거울이다 — Charlie Brooker", "s-coral", "Brooker, The Guardian, 2011"),
    (5, "0. 오프닝", "Claude Glass (클로드 글래스)", "200년 전에도 인간은 검은 거울로 세계를 봤다", "s-white", "Maillet, 2004"),
    (6, "0. 오프닝", "거울이 비추는 것은?", "거울은 우리가 직시하기 두려운 자아를 보여주는 장치 (Lacan·푸코·윤동주)", "s-light", "Lacan 1949 / Foucault 1967"),
    (7, "0. 오프닝", "왜 두려움인가", "두려움 = 가장 강한 발견 신호. 그림자(Shadow)는 의식이 부정하는 자기", "s-gradient", "Jung, Aion 1951"),
    (8, "0. 오프닝", "AX 디자인씽킹의 한 줄", "두려움(블랙미러) × AI 활용 = 가능성", "s-accent", "본 세미나 메타 메시지"),
    (9, "0. 오프닝", "오늘의 여정 — DT 5단계", "발견 → 정의 → 발산 → 시제품 → 공개 한 사이클", "s-white", ""),
    (10, "0. 오프닝", "그라운드 룰 5가지", "비밀유지·판단없음·패스권·발표는컨셉만·도움요청", "s-light", "운영 매뉴얼 참조"),
    (11, "1. ① 발견", "① 발견 단계 시작", "표면이 아니라 이면을 본다", "s-gradient", ""),
    (12, "1. ① 발견", "DT 발견 = 그림자 응시", "진짜 문제는 두려워서 직시하지 않는 곳에 있다", "s-white", "Jung Shadow"),
    (13, "1. ① 발견", "디스토피아 4대 카드", "🕵감시 · 🤖대체 · 📉탈숙련 · 🃏허위정보", "s-light", ""),
    (14, "1. ① 발견", "카드 1: 감시", "AI가 사람을 실시간 분석·예측 — 사례 1~2개", "s-white", ""),
    (15, "1. ① 발견", "카드 2: 대체", "AI가 사람의 일을 대체 — 사례 1~2개", "s-white", ""),
    (16, "1. ① 발견", "카드 3: 탈숙련", "AI가 사람의 핵심 기술을 흡수 — 사례 1~2개", "s-white", ""),
    (17, "1. ① 발견", "카드 4: 허위정보", "AI가 신뢰를 붕괴 — 사례 1~2개", "s-white", ""),
    (18, "1. ① 발견", "WORK: 내 분야 디스토피아 3건", "Perplexity로 위협 근거 리서치 → 시나리오 카드 3건", "s-coral", "워크시트 #1"),
    (19, "1. ① 발견", "Perplexity 활용 팁", "분야 키워드 + 시점(2026) + '사례' 조합", "s-white", "전공별 키워드 카드"),
    (20, "1. ① 발견", "워크 시작 (60분)", "타이머 — Pod 코치 순회", "s-accent", ""),
    (21, "2. ② 정의", "② 정의 단계 시작", "두려움을 픽션으로 외화한다", "s-gradient", ""),
    (22, "2. ② 정의", "좋은 문제정의의 3조건", "본인성 · 구체성 · 전환 가능성", "s-white", ""),
    (23, "2. ② 정의", "블랙미러 에피소드 쓰기", "10년 뒤 내 분야의 디스토피아 1편 — 마지막은 대사 한 줄", "s-coral", "워크시트 #2"),
    (24, "2. ② 정의", "Jung 그림자 — 두려움을 응시하는 이유", "의식이 부정하는 자기를 외화하면 문제가 보인다", "s-gradient", "Jung, Aion 1951"),
    (25, "2. ② 정의", "한 문장 문제정의 템플릿", "'AI가 ___ 시대에, 나는 ___ 정의할 줄 모른다. 그래서 ___'", "s-white", "워크시트 #3"),
    (26, "2. ② 정의", "좋은 예 / 나쁜 예", "본인 분야 사례 2개 (페르소나 도그푸딩 결과 활용)", "s-light", ""),
    (27, "2. ② 정의", "Pair 점검 가이드", "짝과 5분 — 픽션 1단락 + 한 문장 점검", "s-white", ""),
    (28, "2. ② 정의", "WORK 시작 (80분)", "타이머 — 픽션 30분 + Pair 점검 10분 + 한 문장 30분 + Pod 공유 10분", "s-accent", ""),
    (29, "3. ③ 발산", "③ 발산 단계 시작 — 거울을 들고 빛으로", "두려움을 AI 활용으로 번역한다 (AX 4축)", "s-gradient", ""),
    (30, "3. ③ 발산", "AX 4축 — 증폭·확장·재발명·공저", "각 축의 전환식 카드", "s-coral", "워크시트 #4"),
    (31, "3. ③ 발산", "Crazy 8s + AI 발산 프롬프트", "ChatGPT/Gemini에 '4축으로 8개 발산해줘'", "s-white", ""),
    (32, "3. ③ 발산", "WORK 시작 (20분)", "8개 → 3개 → 1개 수렴", "s-accent", ""),
    (33, "4. ④ 시제품", "④ 시제품 단계 — A4 컨셉 시트", "AI를 전제로 한 새 작법·역할·서비스를 종이에", "s-gradient", ""),
    (34, "4. ④ 시제품", "컨셉 시트 양식", "한 줄 / 기능 3개 / 스케치", "s-white", "워크시트 #5"),
    (35, "4. ④ 시제품", "WORK 시작 (25분)", "타이머 — 손그림 OK", "s-accent", ""),
    (36, "5. ⑤ 공개", "⑤ 공개 단계 — 갤러리워크", "컨셉 시트를 벽에 / 스티커 피드백 / 자원 발표", "s-gradient", ""),
    (37, "5. ⑤ 공개", "60초 발표 골격", "두려움 → 픽션 한 줄 → 통찰 → 컨셉 → 다음 한 걸음", "s-white", "워크시트 #6"),
    (38, "5. ⑤ 공개", "갤러리워크 시작 (30분)", "회람 15분 + 자원 발표 5~7명 15분", "s-accent", ""),
    (39, "6. 회고", "회고 — 문제를 보는 눈이 어떻게 바뀌었나", "한 줄로 적어보세요", "s-coral", "워크시트 #7"),
    (40, "6. 회고", "융의 그림자 통합 — 오늘 한 일의 의미", "거울은 깨는 게 아니라 들고 빛으로 가는 것", "s-gradient", "Jung Shadow Integration"),
    (41, "6. 회고", "본 세미나의 인문학적 토대", "1차 자료 11종 한 페이지 — 학생이 들고 갈 인문 자산", "s-white", "탭 04 참조"),
    (42, "6. 회고", "다음 여정", "가을 세미나 / 아이디어톤·해커톤 안내 (1~2분)", "s-light", ""),
    (43, "6. 회고", "클로징", "거울은 거짓말하지 않는다 — 모두의연구소", "s-dark centered", ""),
]
for row in slides:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(slides), r - 1, 6)

ws.freeze_panes = "A5"

# ─── 08_워크시트_7종 ───
ws = wb.create_sheet("08_워크시트_7종")
set_widths(ws, [4, 24, 14, 14, 50, 30])
r = add_title(ws, "워크시트 7종 라인업", "페르소나 도그푸딩으로 확정된 워크 도구")
merge_title(ws, 1, 6); merge_title(ws, 2, 6)

headers = ["#", "워크시트 명", "DT 단계", "사용 시점", "용도·구성", "디자인 상태"]
for i, h in enumerate(headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 6)
r += 1

worksheets = [
    (1, "전공별 디스토피아 키워드 카드", "①", "발견 시작", "예술·인문·사회과학·STEM 각 5개 키워드 — 학생 분야 매핑용. Perplexity 검색어 발판", "라인업 확정 / 카드 디자인 대기"),
    (2, "블랙미러 에피소드 템플릿", "②", "정의 핵심", "3문장 시작 가이드 + '마지막은 대사 한 줄' 명시. 250자 이내", "라인업 확정 / 양식 디자인 대기"),
    (3, "한 문장 문제정의서 (빈칸형)", "②", "정의 마무리", "'AI가 ___ 시대에, 나는 ___ 정의할 줄 모른다. 그래서 ___' 템플릿", "라인업 확정 / 양식 디자인 대기"),
    (4, "AX 4축 발산 카드", "③", "발산 핵심", "증폭·확장·재발명·공저 4장 카드. 각 축의 전환식 + 발산 프롬프트", "라인업 확정 / 카드 디자인 대기"),
    (5, "A4 컨셉 시트 (자유 양식)", "④", "시제품", "이름 / 한 줄 / 기능 3개 / 스케치 영역. 코딩 강요 X", "라인업 확정 / 양식 디자인 대기"),
    (6, "60초 발표 스크립트 골격", "⑤", "공개 준비", "두려움→픽션 한 줄→통찰→컨셉→다음 한 걸음 5단 골격", "라인업 확정 / 양식 디자인 대기"),
    (7, "회고 한 줄 + 감정 카드", "회고", "마무리", "한 줄 회고 + 시작·끝 감정 한 단어", "라인업 확정 / 양식 디자인 대기"),
]
for row in worksheets:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(worksheets), r - 1, 6)

ws.freeze_panes = "A5"

# ─── 09_운영_매뉴얼 ───
ws = wb.create_sheet("09_운영_매뉴얼")
set_widths(ws, [4, 22, 50, 30])
r = add_title(ws, "30명 학부생 운영 매뉴얼", "Pod 시스템 + 패스권 + 갤러리워크 + 6.5H 시간표")
merge_title(ws, 1, 4); merge_title(ws, 2, 4)

# 7가지 운영 위협
ws.cell(row=r, column=1, value="A. 운영 위협 진단 (7가지)").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
t_headers = ["#", "위협", "그대로 두면 어떻게 망하나", "대응"]
for i, h in enumerate(t_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 4, color=DARK)
r += 1
threats = [
    (1, "심리적 안전 부족", "모르는 사람 앞에서 두려움 노출 불가 → 픽션이 표면적이 됨 → ②정의 실패", "Pair → Pod → Plenary 단계적 공개"),
    (2, "참여 비대칭", "외향 4~5명이 발언 독점, 25명 관전 모드", "Pod 내 '오늘의 호스트' 역할 + 익명 보드 활용"),
    (3, "30명 1:1 코칭 불가", "강사 1명으로는 막힌 학생 방치", "Pod 코치 2~3명 (보조 퍼실리테이터)"),
    (4, "5.5H 집중력 한계", "정서적 무게 + 학부생 집중력 → 후반 무너짐", "휴식 2회 + 점심 1H 필수 → 총 6.5H"),
    (5, "공개 발표 부담", "깊이 들어간 학생일수록 발표 부담 → 일부러 얕게 가는 역설", "갤러리워크 + 자원 발표만 (강제 X)"),
    (6, "이질성", "전공·AI 경험·언어 격차 — 한 명에 맞추면 다른 한 명에겐 안 맞음", "전공별 키워드 카드 + Pod 코치 1:1 지원"),
    (7, "정서적 위기", "자기 진로 두려움 직시 → 우는 학생·공황 가능", "강사 정서 응급키트 + 패스권 2장"),
]
for row in threats:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(threats), r - 1, 4)
r += 1

# 운영 5원칙
ws.cell(row=r, column=1, value="B. 운영 5원칙 (Operational Playbook)").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
p_headers = ["#", "원칙", "설명", "효과"]
for i, h in enumerate(p_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 4, color=DARK)
r += 1
principles = [
    (1, "Pair → Pod → Plenary", "픽션은 짝(2인)에게만 / 컨셉은 Pod(5~6인) / 전체는 갤러리워크만", "깊이 들어간 학생도 부담 분산"),
    (2, "패스권 명시", "물리 패스 카드 2장 — '저는 패스합니다' 가능", "안전감 → 역설적으로 깊이 끌어냄"),
    (3, "Pod 시스템 + 멀티 퍼실리테이터", "6 Pod × 5명 또는 5 Pod × 6명 + Pod 코치 2~3명", "강사 1명 한계 돌파"),
    (4, "갤러리워크 중심 발표", "벽 회람 + 스티커 + 자원 발표 5~7명만", "모두 노출, 부담은 자원자만"),
    (5, "강사 정서 응급키트", "체크인/체크아웃 + 위기 신호 가이드 + 그라운드 룰 5", "우는 학생 발생 시 안전 대응"),
]
for row in principles:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(principles), r - 1, 4)
r += 1

# 시간표
ws.cell(row=r, column=1, value="C. 6.5H 시간표 (점심·휴식 포함)").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
t_headers = ["#", "시간", "모듈", "비고"]
for i, h in enumerate(t_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 4, color=DARK)
r += 1
timetable = [
    (1, "0:00–0:30", "오프닝 + 익명 두려움 보드 + Pod 분할", "안전감 1차 형성"),
    (2, "0:30–2:00", "① 발견 (Perplexity + Pod 공유)", "90분 강도 높음"),
    (3, "2:00–2:15", "☕ 휴식", "필수"),
    (4, "2:15–3:45", "② 정의 (블랙미러 에피소드 + Pair 공유)", "가장 정서적 단계"),
    (5, "3:45–4:45", "🍱 점심 (1H)", "정서적 디톡스 / Pod 자유 교류"),
    (6, "4:45–5:15", "③ 발산 (AX 4축)", "점심 후 다시 활기"),
    (7, "5:15–5:45", "④ 시제품 (컨셉 시트)", "손 움직이는 활동"),
    (8, "5:45–6:15", "⑤ 갤러리워크 + 자원 발표", "모두에게 노출되되 부담 분산"),
    (9, "6:15–6:30", "회고 + 체크아웃", "정서적 클로저"),
]
for row in timetable:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(timetable), r - 1, 4)
r += 1

# 인력
ws.cell(row=r, column=1, value="D. 인력·물품 산정 (30명 기준)").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
h_headers = ["#", "역할/항목", "수량", "비고"]
for i, h in enumerate(h_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 4, color=DARK)
r += 1
staff = [
    (1, "메인 강사", "1명", "₩600,000/시간 × 5.5H 기준"),
    (2, "Pod 코치 (보조 퍼실리테이터)", "2~3명", "₩100,000/시간 × 5.5H × 2~3명 (보조강사 단가). Pod 코치 없으면 구조적으로 망함"),
    (3, "운영 스태프", "1명", "체크인·다과·기기"),
    (4, "Pod 단위 원형 테이블", "6개", "강의식 ❌"),
    (5, "워크시트 7종 인쇄본", "30부", "탭 08 참조"),
    (6, "패스 카드", "60장", "학생 1인당 2장"),
    (7, "갤러리워크 자재", "—", "벽면 + 마스킹 테이프 + 스티커 5색"),
    (8, "AI 도구 사전 안내", "—", "Perplexity Pro / ChatGPT Plus / Claude 계정 안내"),
    (9, "익명 보드", "—", "Mentimeter or Padlet"),
    (10, "다과·점심", "—", "점심 + 다과 2회"),
]
for row in staff:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(staff), r - 1, 4)
r += 1

# 그라운드 룰
ws.cell(row=r, column=1, value="E. 그라운드 룰 5가지 (워크숍 시작 시 합의)").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
rules = [
    "1. 여기서 들은 이야기는 여기 두고 갑니다 (비밀 유지)",
    "2. 판단하지 않고 듣습니다",
    "3. 패스권은 언제든 사용 가능합니다",
    "4. 발표는 컨셉만 가능합니다 (픽션 강제 X)",
    "5. 도움이 필요하면 손 들기 — 강사·Pod 코치가 옵니다",
]
for rule in rules:
    ws.cell(row=r, column=1, value=rule)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1).alignment = wrap_left("center")
    ws.cell(row=r, column=1).border = thin_border()
    ws.cell(row=r, column=1).fill = fill(LIGHT_YELLOW)
    ws.cell(row=r, column=1).font = base_font()
    r += 1

ws.freeze_panes = "A5"

# ─── 10_TODO_다음단계 ───
ws = wb.create_sheet("10_TODO_다음단계")
set_widths(ws, [4, 30, 50, 18, 14])
r = add_title(ws, "TODO — 다음 단계 작업", "확정된 기획 위에서 남은 작업 + 의사결정 포인트")
merge_title(ws, 1, 5); merge_title(ws, 2, 5)

headers = ["#", "작업", "내용", "우선순위", "상태"]
for i, h in enumerate(headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 5)
r += 1

todos = [
    (1, "슬라이드 HTML 생성", "탭 07 구조 + 탭 05 AX 4축 메시지 반영. modu-slide 스킬로 단일 HTML", "🔥 높음", "대기"),
    (2, "워크시트 7종 디자인", "탭 08 라인업. 인쇄용 PDF 양식 (블랙미러 템플릿·문제정의서·4축 카드 등)", "🔥 높음", "대기"),
    (3, "가을학기 세미나 기획", "AI 블랙미러 Ⅱ — 두려움을 작동하는 해결로 (③④⑤ 깊게). 별도 슬라이드·워크시트", "중", "대기"),
    (4, "전공별 디스토피아 키워드 카드", "예술·인문·사회과학·STEM 각 5개. 학부생 학과 매핑용 (워크시트 #1)", "중", "대기"),
    (5, "강사·Pod 코치 운영 매뉴얼", "탭 09 기반 진행표 + 위기 대응 시나리오 + 사전 브리핑 자료", "중", "대기"),
    (6, "사전 미션 이메일 안내", "1주 전 학생 발송 — 'AI 시대에 내가 가장 두려운 것 한 줄' 미션", "낮음", "대기"),
    (7, "1차 자료 인용 슬라이드 셀렉트", "탭 04에서 핵심 3~4개 인용구·이미지 슬라이드용 셀렉트 (Brooker·Maillet·Foucault·Jung)", "중", "대기"),
    (8, "사업 담당자 보고용 1장 요약", "본 컨셉의 셀링 포인트 (인문학 토대 + AX 정합성 + 운영 안전성)", "낮음", "대기"),
    (9, "20명 vs 30명 옵션 협의", "30명은 운영 상한. 20명 이하 옵션 가능한지 사업 측 협의", "중", "의사결정 필요"),
    (10, "Pod 코치 소싱", "연세 AX 부트캠프 졸업생 / 사회복지·심리·인문 대학원생 / 모두의연구소 퍼실리테이터", "중", "의사결정 필요"),
    (11, "여름·가을 외 추가 연결 검토", "겨울 후속·졸업 포트폴리오 연계 등 — 사업 측 의향 확인", "낮음", "의사결정 필요"),
]
for row in todos:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(todos), r - 1, 5)
r += 2

# 의사결정 포인트
ws.cell(row=r, column=1, value="의사결정 포인트 (사용자/사업 측 답 필요)").font = section_font()
ws.cell(row=r, column=1).fill = fill(CORAL)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
ws.cell(row=r, column=1).alignment = wrap_left("center")
r += 1
d_headers = ["#", "질문", "옵션", "권장", "결정"]
for i, h in enumerate(d_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, 5, color=DARK)
r += 1
decisions = [
    (1, "다음 작업 순서", "슬라이드 먼저 / 워크시트 먼저 / 둘 동시", "둘 동시 (슬라이드 안에 워크시트 임베드)", "대기"),
    (2, "참가 규모", "20명 이하 / 30명 (상한)", "20명 이하 권장. 30명은 Pod 시스템 + 코치 2~3명 필수", "대기"),
    (3, "발표자 표기", "모두의연구소만 / 강사명 명시", "강사 확정 시 명시", "대기"),
    (4, "가을학기 기획 진행 시점", "여름 슬라이드 완성 후 / 병행", "여름 완성 후 직렬 권장", "대기"),
]
for row in decisions:
    for c, val in enumerate(row, 1):
        ws.cell(row=r, column=c, value=val)
    r += 1
style_body(ws, r - len(decisions), r - 1, 5)

ws.freeze_panes = "A5"

# ───── 저장 ─────
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print(f"[OK] Saved: {OUT}")
print(f"[OK] Tabs: {len(wb.sheetnames)} — {wb.sheetnames}")
