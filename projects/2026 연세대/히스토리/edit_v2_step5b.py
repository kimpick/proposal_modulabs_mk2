"""
Step 5b: 매핑 표 + 마무리 문단 누락분 추가
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PATH = '연세AX_제안서_모두의연구소_v2_260506(보완3).docx'
doc = Document(PATH)


def insert_paragraph_after(reference_element, text, bold=False):
    new_p = OxmlElement('w:p')
    reference_element.addnext(new_p)
    r = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    if bold:
        rpr.append(OxmlElement('w:b'))
        rpr.append(OxmlElement('w:bCs'))
    rfonts = OxmlElement('w:rFonts')
    rfonts.set(qn('w:eastAsia'), '맑은 고딕')
    rpr.append(rfonts)
    r.append(rpr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    r.append(t)
    new_p.append(r)
    return new_p


def insert_table_after(reference_element, data, bold_header=True):
    cols_n = max(len(row) for row in data) if data else 0
    tbl = OxmlElement('w:tbl')
    tblPr = OxmlElement('w:tblPr')
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '5000')
    tblW.set(qn('w:type'), 'pct')
    tblPr.append(tblW)
    tblBorders = OxmlElement('w:tblBorders')
    for border_type in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        b = OxmlElement(f'w:{border_type}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:color'), '000000')
        tblBorders.append(b)
    tblPr.append(tblBorders)
    tbl.append(tblPr)
    tblGrid = OxmlElement('w:tblGrid')
    for _ in range(cols_n):
        tblGrid.append(OxmlElement('w:gridCol'))
    tbl.append(tblGrid)
    for r_idx, row_data in enumerate(data):
        tr = OxmlElement('w:tr')
        for c_idx in range(cols_n):
            tc = OxmlElement('w:tc')
            tc.append(OxmlElement('w:tcPr'))
            p = OxmlElement('w:p')
            p.append(OxmlElement('w:pPr'))
            r = OxmlElement('w:r')
            rPr = OxmlElement('w:rPr')
            if r_idx == 0 and bold_header:
                rPr.append(OxmlElement('w:b'))
                rPr.append(OxmlElement('w:bCs'))
            rfonts = OxmlElement('w:rFonts')
            rfonts.set(qn('w:eastAsia'), '맑은 고딕')
            rPr.append(rfonts)
            r.append(rPr)
            t = OxmlElement('w:t')
            t.text = row_data[c_idx] if c_idx < len(row_data) else ''
            t.set(qn('xml:space'), 'preserve')
            r.append(t)
            p.append(r)
            tc.append(p)
            tr.append(tc)
        tbl.append(tr)
    reference_element.addnext(tbl)
    return tbl


# 5단계 프레임 표 정확히 식별
target_table = None
for t in doc.tables:
    if len(t.rows) > 0:
        first = [c.text.strip() for c in t.rows[0].cells]
        if first == ['단계', '학생의 행동', '운영 도구·산출물']:
            target_table = t
            print(f"Found framework table")
            break

if target_table is None:
    print("ERROR: framework table not found")
    sys.exit(1)

framework_tbl_elem = target_table._element

# 매핑 표 데이터
mapping_data = [
    ['프로그램 유형', '주요 단계', '본 사업에서의 역할'],
    ['체험 교육 (5건)', '①', '도서관 실감미디어 인프라에서 AI·기술과 처음 만나며 \"내가 만들고 싶은 것\"의 단서를 얻음'],
    ['세미나 (8건)', '①·②', 'IT·미디어 산업 전문가의 관점에서 자기 문제를 다시 봄. 인문학 세미나는 박물관 자원을 문제 영역으로 끌어옴'],
    ['워크숍 (41건)', '②·③·④', '문제 진술서 → 아이디어 발산 → 시제품까지 한 사이클을 압축적으로 경험'],
    ['멘토링 (9건)', '③·④·⑤', '시제품을 실제 작동하는 결과물로 키우는 단계. 멘토는 학생의 사이클이 막힌 지점을 풀어줌'],
    ['공모전·경진대회 (7건)', '⑤', '강의실 밖 사용자에게 공개하고 피드백을 받는 단계. 인증 포트폴리오에 결과물을 누적'],
    ['교육 콘텐츠 개발 (20건)', '전 단계', '5단계 흐름이 모든 과정에서 일관되게 운영되도록 받쳐주는 학습 자료·실감형 콘텐츠'],
]

# 역순 삽입: 빈줄 → 표 → 헤더 → 빈줄
# framework_tbl_elem 바로 뒤에 추가하니, 마지막 추가물이 framework 표 다음으로 옴
# 따라서 역순: 마지막 마무리 문단부터 거꾸로 삽입

closing_paras = [
    ("", False),
    ("이 메서드의 효과는 다음과 같이 정리됩니다.", False),
    ("", False),
    ("· 학생 입장: 어떤 과정에 들어가도 자기 결과물이 누적된다. 워크숍 한 번으로 끝나지 않고, 같은 흐름이 다음 학기·다음 캠퍼스에서도 이어진다.", False),
    ("· 발주처 입장: 90건 과정의 학습 성과를 동일한 기준(문제 진술 → 시제품 → 공개)으로 비교하고 관리할 수 있다. 캠퍼스·학기·강사가 달라도 운영의 일관성이 유지된다.", False),
    ("· 모두의연구소 입장: 사업 종료 후에도 학생 결과물이 모두의연구소 학습 커뮤니티(풀잎스쿨·AIFFEL)와 자연스럽게 연결되며, 우수 사례는 다음 해 본 사업의 교육 콘텐츠로 환류된다.", False),
    ("", False),
    ("AI 시대의 Design Thinking 프로젝트는 본 사업이 90건의 개별 과정으로 흩어지지 않도록 하는 운영 원리이자, 학생이 \"나는 AI로 어떤 문제를 풀었는가\"를 자기 언어로 답할 수 있도록 만드는 학습 설계입니다.", False),
]

# 1) framework 표 다음에 빈 줄 (제일 먼저 들어갈 자리)
# 2) 헤더 단락 "▶ 프로그램 유형별 단계 매핑"
# 3) 매핑 표
# 4) 마무리 문단들

# 역순으로 삽입 (각 element가 framework_tbl_elem 바로 뒤에 들어감)
# 따라서 결과 순서를 위해 역순 삽입

# 마무리 문단 (역순)
for text, bold in reversed(closing_paras):
    insert_paragraph_after(framework_tbl_elem, text, bold=bold)

# 매핑 표 삽입 (헤더 위에 들어가야 하니, 일단 framework 다음에 매핑 표 넣음 — 그러면 표가 closing 위에 오게 됨)
insert_table_after(framework_tbl_elem, mapping_data)

# 매핑 표 헤더 (framework_tbl_elem 바로 뒤에 들어가야 매핑 표 위에 오게 됨)
insert_paragraph_after(framework_tbl_elem, "▶ 프로그램 유형별 단계 매핑", bold=True)

# 헤더 위 빈 줄
insert_paragraph_after(framework_tbl_elem, "", bold=False)

print("✅ 매핑 표 + 마무리 문단 삽입 완료")

try:
    doc.save(PATH)
    print(f"✅ Saved: {PATH}")
except PermissionError:
    alt = '연세AX_제안서_모두의연구소_v2_260506(보완5b).docx'
    doc.save(alt)
    print(f"⚠️ 잠금되어 사본 저장: {alt}")
