"""
v5에 일관성 보강 4가지 적용:
- 변경 1: Joy of Depth 구현 프로그램 용어 통일 (Vibe/Agentic/Harness → 프롬프트/컨텍스트/하네스 엔지니어링)
- 변경 2: AX 역량 로드맵 각 단계에 '역량 구성' 줄 추가 (두 축 자연스럽게)
- 변경 3: Trinity of Joy 각 전략에 자연스러운 연결 한 줄 추가
- 시각화: 운영 메서드 도입 직후 "두 축 ↔ 학생 성장 단계" 시각 표 추가
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v5/word/document.xml'

with open(DOC_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

before = len(content)


# ─── 빌딩 블록 ────────────────────────────────────────────────
def normal_para(text):
    return (
        '<w:p>'
        '<w:pPr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
        '<w:spacing w:before="200" w:after="180"/>'
        '<w:jc w:val="both"/>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
        '<w:color w:val="222222"/>'
        '</w:rPr>'
        '</w:pPr>'
        '<w:r>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
        '<w:color w:val="222222"/>'
        '</w:rPr>'
        f'<w:t xml:space="preserve">{text}</w:t>'
        '</w:r>'
        '</w:p>'
    )

def empty_para():
    return (
        '<w:p>'
        '<w:pPr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
        '<w:spacing w:before="200" w:after="180"/>'
        '<w:jc w:val="both"/>'
        '</w:pPr>'
        '</w:p>'
    )

def arrow_heading(text):
    return (
        '<w:p>'
        '<w:pPr><w:spacing w:before="160" w:after="60"/></w:pPr>'
        '<w:r>'
        '<w:rPr><w:b/><w:bCs/><w:color w:val="F7585C"/></w:rPr>'
        '<w:t xml:space="preserve">▶ </w:t>'
        '</w:r>'
        '<w:r>'
        '<w:rPr><w:b/><w:bCs/><w:color w:val="1A1A2E"/></w:rPr>'
        f'<w:t xml:space="preserve">{text}</w:t>'
        '</w:r>'
        '</w:p>'
    )

def make_table(rows, col_widths, header_fill='F0F4F8'):
    total = sum(col_widths)
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)
    rows_xml = ''
    for r_idx, row in enumerate(rows):
        cells = ''
        for c_idx, cell_text in enumerate(row):
            w = col_widths[c_idx] if c_idx < len(col_widths) else col_widths[-1]
            is_header = (r_idx == 0)
            fill = header_fill if is_header else 'FFFFFF'
            bold_xml = '<w:b/><w:bCs/>' if is_header else ''
            # 좌·우 컬럼은 강조 색상 (3열 표 가정)
            color = '222222'
            if not is_header and len(row) == 3:
                if c_idx == 0:
                    color = '1F4E79'  # 좌측 - AI 리터러시 축 (파랑)
                elif c_idx == 2:
                    color = '7B3F00'  # 우측 - 디자인씽킹 축 (갈색)
            cells += (
                f'<w:tc>'
                f'<w:tcPr>'
                f'<w:tcW w:w="{w}" w:type="dxa"/>'
                f'<w:tcBorders>'
                f'<w:top w:val="single" w:sz="3" w:space="0" w:color="B3C6D9"/>'
                f'<w:left w:val="single" w:sz="3" w:space="0" w:color="B3C6D9"/>'
                f'<w:bottom w:val="single" w:sz="3" w:space="0" w:color="B3C6D9"/>'
                f'<w:right w:val="single" w:sz="3" w:space="0" w:color="B3C6D9"/>'
                f'</w:tcBorders>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
                f'<w:tcMar><w:top w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>'
                f'</w:tcPr>'
                f'<w:p>'
                f'<w:pPr><w:spacing w:before="0" w:after="0"/><w:jc w:val="center"/></w:pPr>'
                f'<w:r>'
                f'<w:rPr>'
                f'<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
                f'{bold_xml}'
                f'<w:color w:val="{color}"/>'
                f'<w:sz w:val="20"/><w:szCs w:val="20"/>'
                f'</w:rPr>'
                f'<w:t xml:space="preserve">{cell_text}</w:t>'
                f'</w:r>'
                f'</w:p>'
                f'</w:tc>'
            )
        rows_xml += f'<w:tr><w:trPr><w:trHeight w:val="500"/></w:trPr>{cells}</w:tr>'
    return (
        f'<w:tbl>'
        f'<w:tblPr>'
        f'<w:tblStyle w:val="af1"/>'
        f'<w:tblW w:w="{total}" w:type="dxa"/>'
        f'<w:tblInd w:w="-2" w:type="dxa"/>'
        f'<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>'
        f'<w:tblLayout w:type="fixed"/>'
        f'</w:tblPr>'
        f'<w:tblGrid>{grid}</w:tblGrid>'
        f'{rows_xml}'
        f'</w:tbl>'
    )


# ────────────────────────────────────────────────────────────
# 변경 1: Joy of Depth 구현 프로그램 줄 텍스트 교체
# ────────────────────────────────────────────────────────────
old_1 = "구현 프로그램: AX 기술 실습 워크숍(41건), 여름 AX 심화 캠프 (Vibe Coding → Agentic Coding → Harness Engineering 단계별 심화)"
new_1 = "구현 프로그램: AX 기술 실습 워크숍(41건), 여름 AX 심화 캠프 — 프롬프트 엔지니어링 → 컨텍스트 엔지니어링 → 하네스 엔지니어링으로 이어지는 AI 리터러시 단계적 심화"
if old_1 in content:
    content = content.replace(old_1, new_1)
    print("✅ 변경 1: Joy of Depth 구현 프로그램 용어 통일")
else:
    print("❌ 변경 1: 원본 텍스트 못 찾음")


# ────────────────────────────────────────────────────────────
# 변경 3: Trinity of Joy 각 전략에 자연스러운 연결 한 줄 추가
# ────────────────────────────────────────────────────────────
# Joy of Expansion 구현 프로그램 줄 다음에 추가
exp_anchor = "구현 프로그램: 3개 캠퍼스 특성화 운영, AX 트렌드 세미나(8건), 박물관 인문학 역량 강화 융합 교육, 실감미디어 체험 프로그램(5건)"
exp_extra = "이 전략은 학생이 자기 전공·관심사를 AI로 풀어내는 디자인씽킹의 출발점입니다."

# 해당 paragraph 찾아서 그 뒤에 단락 추가
def insert_para_after_text(content, anchor_text, new_para):
    """anchor_text가 들어있는 paragraph 다음에 new_para 삽입"""
    idx = content.find(anchor_text)
    if idx < 0:
        return content, False
    p_end = content.find('</w:p>', idx) + len('</w:p>')
    return content[:p_end] + new_para + content[p_end:], True

content, ok = insert_para_after_text(content, exp_anchor, normal_para(exp_extra))
print(f"{'✅' if ok else '❌'} 변경 3-1: Joy of Expansion 연결 줄 추가")

ori_anchor = "구현 프로그램: 멘토링 프로젝트(9건), 공모전·경진대회·쇼케이스(7건), Wild Public Release를 통한 SNS 배포 및 사회적 확산"
ori_extra = "이 전략은 학생이 자기만의 결과물을 세상에 공개하는 디자인씽킹의 도착점입니다."
content, ok = insert_para_after_text(content, ori_anchor, normal_para(ori_extra))
print(f"{'✅' if ok else '❌'} 변경 3-2: Joy of Originality 연결 줄 추가")

# Joy of Depth: 변경 1로 이미 "프롬프트 → 컨텍스트 → 하네스" 들어갔으므로 추가 줄 불필요
# 다만 Originality·Expansion과 형식 통일을 위해 한 줄 추가
depth_anchor = new_1  # 변경 1 후의 새 문장
depth_extra = "이 전략의 학습 결과는 도구가 바뀌어도 학생이 무너지지 않는 AI 리터러시의 깊이입니다."
content, ok = insert_para_after_text(content, depth_anchor, normal_para(depth_extra))
print(f"{'✅' if ok else '❌'} 변경 3-3: Joy of Depth 연결 줄 추가")


# ────────────────────────────────────────────────────────────
# 변경 2: AX 역량 로드맵 각 단계에 '역량 구성' 줄 추가
# ────────────────────────────────────────────────────────────
# 각 Joy 매핑 줄 다음에 역량 구성 줄 추가

# Starter
starter_anchor = "Joy 매핑: Joy of Depth — AI가 무엇이고 어떻게 작동하는지 이해하는 단계"
starter_extra = "역량 구성: AI에 원하는 답을 끌어내는 프롬프트 엔지니어링 + 자기 도메인에서 \"AI로 풀 만한 문제\" 발견"
content, ok = insert_para_after_text(content, starter_anchor, normal_para(starter_extra))
print(f"{'✅' if ok else '❌'} 변경 2-1: Starter 역량 구성 추가")

# Practitioner
prac_anchor = "Joy 매핑: Joy of Expansion — 배운 기술을 자신의 전공·관심 도메인에 적용하는 단계"
prac_extra = "역량 구성: AI에게 정보·역할을 설계해주는 컨텍스트 엔지니어링 + 문제 정의에서 해결안 설계까지의 디자인씽킹"
content, ok = insert_para_after_text(content, prac_anchor, normal_para(prac_extra))
print(f"{'✅' if ok else '❌'} 변경 2-2: Practitioner 역량 구성 추가")

# Creator
creator_anchor = "Joy 매핑: Joy of Originality — 나만의 결과물(MVP)을 만들어 세상에 공개하는 단계"
creator_extra = "역량 구성: 여러 AI를 묶어 자율 시스템을 만드는 하네스 엔지니어링 + 자기 시제품을 사회적 공개로 잇는 창의적 해결"
content, ok = insert_para_after_text(content, creator_anchor, normal_para(creator_extra))
print(f"{'✅' if ok else '❌'} 변경 2-3: Creator 역량 구성 추가")


# ────────────────────────────────────────────────────────────
# 시각화: "두 축 ↔ 학생 성장 단계" 표 추가
#   위치: 운영 메서드 도입 3문단 직후, "▶ 5단계 운영 프레임" 직전
# ────────────────────────────────────────────────────────────
# Anchor: 운영 메서드 마무리 도입 문장
# "두 축이 만나는 자리가 「AI 시대의 Design Thinking 프로젝트」이며..."
anchor_methodology = "두 축이 만나는 자리가 「AI 시대의 Design Thinking 프로젝트」이며, 아래 5단계 운영 프레임은 그 만남이 90건 모든 과정에서 일관되게 일어나도록 받쳐주는 운영 메서드입니다"

# 시각 표 데이터
viz_rows = [
    ['AI 리터러시 축\n(도구가 바뀌어도)', '학생 성장 단계', '디자인씽킹 축\n(전공이 달라도)'],
    ['프롬프트 엔지니어링', 'AX Starter\n(입문)', '자기 도메인의 문제 발견'],
    ['컨텍스트 엔지니어링', 'AX Practitioner\n(활용)', '문제 정의 → 해결안 설계'],
    ['하네스 엔지니어링', 'AX Creator\n(심화)', '창의적 시제품 → 사회적 공개'],
]

viz_block = (
    empty_para() +
    arrow_heading('학생 성장 단계로 본 두 축의 동시 진행') +
    normal_para('두 축은 서로 떨어진 별개의 학습 영역이 아니라, 학생이 단계를 밟을 때마다 동시에 한 칸씩 깊어지는 구조입니다. 입문 단계의 학생은 프롬프트 엔지니어링을 익히면서 자기 도메인의 문제를 발견하고, 활용 단계에서는 컨텍스트 엔지니어링으로 그 문제를 정의·설계하며, 심화 단계에서는 하네스 엔지니어링으로 시제품을 만들어 세상에 공개합니다.') +
    empty_para() +
    make_table(viz_rows, [3000, 2400, 4000]) +
    empty_para()
)

idx = content.find(anchor_methodology)
if idx >= 0:
    p_end = content.find('</w:p>', idx) + len('</w:p>')
    content = content[:p_end] + viz_block + content[p_end:]
    print("✅ 시각화: 두 축 ↔ 학생 성장 단계 표 추가")
else:
    print("❌ 시각화: anchor 못 찾음")


with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

after = len(content)
print(f"\n파일 크기: {before} -> {after} (Δ {after - before})")
