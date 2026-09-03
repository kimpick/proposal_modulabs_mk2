"""
v9의 추진 전략 파트를 3축으로 재정렬:
A) RFP 3대 목표 ①②③ → 표
B) Trinity of Joy 본문 12개 paragraph → 새 3축 추진 전략 (도입 + 표 + 전략별 본문 + Trinity 압축 표)
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v9/word/document.xml'
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
        '<w:pPr><w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/><w:spacing w:before="120" w:after="120"/></w:pPr>'
        '</w:p>'
    )

def arrow_heading(text):
    return (
        '<w:p>'
        '<w:pPr><w:spacing w:before="200" w:after="80"/></w:pPr>'
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

def quote_para(text):
    """이탤릭 인용문 단락"""
    return (
        '<w:p>'
        '<w:pPr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
        '<w:spacing w:before="120" w:after="120"/>'
        '<w:ind w:left="400"/>'
        '<w:jc w:val="left"/>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
        '<w:i/><w:iCs/>'
        '<w:color w:val="555555"/>'
        '</w:rPr>'
        '</w:pPr>'
        '<w:r>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
        '<w:i/><w:iCs/>'
        '<w:color w:val="555555"/>'
        '</w:rPr>'
        f'<w:t xml:space="preserve">{text}</w:t>'
        '</w:r>'
        '</w:p>'
    )


def make_table(rows, col_widths, bold_header=True, header_fill='F0F4F8'):
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
                f'<w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr>'
                f'<w:r>'
                f'<w:rPr>'
                f'<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
                f'{bold_xml}'
                f'<w:color w:val="222222"/>'
                f'<w:sz w:val="20"/><w:szCs w:val="20"/>'
                f'</w:rPr>'
                f'<w:t xml:space="preserve">{cell_text}</w:t>'
                f'</w:r>'
                f'</w:p>'
                f'</w:tc>'
            )
        rows_xml += f'<w:tr><w:trPr><w:trHeight w:val="450"/></w:trPr>{cells}</w:tr>'
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
# A) RFP 3대 목표 ①②③ Bold paragraph 3개 → 표
# ────────────────────────────────────────────────────────────
# 3개 paragraph를 식별: ①, ②, ③로 시작하는 짧은 paragraph
import re

# ①②③ paragraph 문자열 (대략 일치)
old_p1_text = "① AI 전환 시대 대응 통합 교육 체계 구축 — 미래형 융합 인재 양성"
old_p2_text = "② 핵심 AX 기술 기반 문제 해결 중심 실전형 교육 경험 제공"
old_p3_text = "③ 수요 기반 맞춤형 교육과 지속적 품질 관리를 통한 교육 효과 극대화"

# 3개 paragraph 모두 찾기 (Bold rPr 포함)
def find_para_with_text(content, search_text):
    idx = content.find(search_text)
    if idx < 0:
        return -1, -1
    p_start = content.rfind('<w:p>', 0, idx)
    p_start_alt = content.rfind('<w:p ', 0, idx)
    p_start = max(p_start, p_start_alt)
    p_end = content.find('</w:p>', idx) + len('</w:p>')
    return p_start, p_end

# 3개 paragraph가 연속으로 있다면 한 번에 교체
ps_p1 = find_para_with_text(content, old_p1_text)
ps_p3 = find_para_with_text(content, old_p3_text)

if ps_p1[0] >= 0 and ps_p3[1] > 0:
    # ① 시작 ~ ③ 끝까지 한 덩어리로 교체
    rfp_table_rows = [
        ['#', '발주처 제시 목표', '모두의연구소 응답'],
        ['①', 'AI 전환 시대 대응 통합 교육 체계 구축 — 미래형 융합 인재 양성', '목표 가·나'],
        ['②', '핵심 AX 기술 기반 문제 해결 중심 실전형 교육 경험 제공', '목표 가·나·다·라'],
        ['③', '수요 기반 맞춤형 교육과 지속적 품질 관리를 통한 교육 효과 극대화', '목표 다·라'],
    ]
    rfp_table = empty_para() + make_table(rfp_table_rows, [600, 6900, 2300]) + empty_para()

    content = content[:ps_p1[0]] + rfp_table + content[ps_p3[1]:]
    print("✅ A. RFP 3대 목표 ①②③ → 표로 교체")
else:
    print("❌ A. RFP 3대 목표 paragraph 못 찾음")


# ────────────────────────────────────────────────────────────
# B) Trinity of Joy 격상 도입 + 전략 1·2·3 본문 → 새 3축 추진 전략
# ────────────────────────────────────────────────────────────

# 시작 anchor: "Trinity of Joy는 본 사업의 셋째 축이자" 단락
B_START_ANCHOR = "Trinity of Joy는 본 사업의 셋째 축이자 학습이 멈추지 않게 하는 원동력입니다"
# 끝 anchor: 마지막 (Joy of Originality 연결 줄) "이 전략은 학생이 자기만의 결과물을 세상에 공개하는 디자인씽킹의 도착점입니다."
B_END_ANCHOR = "이 전략은 학생이 자기만의 결과물을 세상에 공개하는 디자인씽킹의 도착점입니다"

start_idx = content.find(B_START_ANCHOR)
end_idx = content.find(B_END_ANCHOR)

if start_idx >= 0 and end_idx >= 0:
    # 시작 paragraph의 시작점
    p_start1 = content.rfind('<w:p>', 0, start_idx)
    p_start1_alt = content.rfind('<w:p ', 0, start_idx)
    p_start_pos = max(p_start1, p_start1_alt)
    # 끝 paragraph의 끝점
    p_end_pos = content.find('</w:p>', end_idx) + len('</w:p>')

    # 새 본문 빌드
    new_block = ""

    # B-1. 도입 단락
    new_block += normal_para(
        "본 사업의 추진 전략은 세 가지 축으로 구성됩니다. AI 리터러시는 학생의 손, AX 디자인씽킹은 학생의 시선, 배움의 즐거움은 학생을 계속 움직이게 하는 원동력입니다. 세 축이 모든 프로그램에서 동시에 작동할 때, 학생은 도구·전공·동기 어느 쪽에도 흔들리지 않는 AX 인재로 성장합니다."
    )
    new_block += empty_para()

    # B-2. 추진 전략 표 (3행)
    strategy_rows = [
        ['전략', '핵심 메시지', '학생이 기를 역량', '구현 프로그램'],
        ['전략 1. AI 리터러시 (도구가 바뀌어도)', '도구가 바뀌어도 흔들리지 않는 손', '프롬프트 → 컨텍스트 → 하네스 엔지니어링 단계적 심화', 'AX 기술 실습 워크숍 41건, 여름 AX 심화 캠프'],
        ['전략 2. AX 디자인씽킹 (전공이 달라도)', '전공이 달라도 통하는 시선', '자기 문제 발견 → 정의 → 창의적 해결', '디자인씽킹 워크숍, 멘토링 프로젝트 9건'],
        ['전략 3. 배움의 즐거움 (학습의 원동력)', '학습이 멈추지 않게 하는 동력', 'Joy of Depth + Expansion + Originality', '공모전·쇼케이스 7건, Wild Public Release, 총장 명의 인증서'],
    ]
    new_block += make_table(strategy_rows, [2400, 1900, 2900, 2600])
    new_block += empty_para()

    # B-3. 전략 1·2·3 본문
    new_block += arrow_heading("전략 1. AI 리터러시 — 도구가 바뀌어도")
    new_block += normal_para(
        "도구 숙련 중심 교육은 \"얼마나 빠르게\"를 묻지만, \"왜 배우는가\"에는 답하지 못합니다. 기술을 표면적으로 익힌 학생은 다음 트렌드가 오면 다시 처음부터 시작해야 하지만, 원리를 이해한 학생은 도구가 바뀌어도 스스로 적응합니다. 본 사업은 프롬프트 엔지니어링(원하는 답을 끌어내는 법) → 컨텍스트 엔지니어링(AI에게 정보·역할을 설계하는 법) → 하네스 엔지니어링(여러 AI를 묶어 자율 시스템을 만드는 법)의 단계적 심화 경로로 학생의 손을 단련합니다."
    )

    new_block += arrow_heading("전략 2. AX 디자인씽킹 — 전공이 달라도")
    new_block += normal_para(
        "대학 AI 교육의 문제는 기술 부족이 아니라 적용 맥락 부족입니다. 이공계 중심 설계 속에서 인문·예체능 학생이 '나와 무관한 기술'로 인식하고 이탈하는 일이 반복됩니다. 본 사업은 디자인씽킹 메서드(공감 → 문제 정의 → 발산 → 시제품 → 검증)를 모든 과정의 운영 골격으로 삼아, 학생이 자기 전공·일상·관심사에서 출발해 자기만의 문제를 발견하고 창의적으로 풀어내도록 시선을 단련합니다."
    )

    new_block += arrow_heading("전략 3. 배움의 즐거움 — 학습의 원동력 (The Trinity of Joy)")
    new_block += normal_para(
        "수료 후 학습이 멈추는 이유는 배움이 학생의 것이 되지 않기 때문입니다. 본 사업은 학생을 1년 사업 끝까지 움직이게 하는 세 가지 즐거움(Trinity of Joy)을 모든 프로그램의 설계 원칙으로 삼습니다."
    )
    new_block += empty_para()

    # Trinity 3행 압축 표
    trinity_rows = [
        ['즐거움', '학생이 갖게 되는 감각', '학생의 한 마디'],
        ['Joy of Depth (깊이)', '원리를 이해해 도구가 바뀌어도 무섭지 않은 감각', '"나는 AI가 어떻게 작동하는지 안다."'],
        ['Joy of Expansion (확장)', '자기 전공·일상에 기술이 닿는 순간의 감각', '"나는 내 전공으로 AI를 활용할 수 있다."'],
        ['Joy of Originality (자기다움)', '자기 결과물에 세상이 반응하는 감각', '"나는 AI를 도구로 삼아 세상에 내 결과물을 공개했다."'],
    ]
    new_block += make_table(trinity_rows, [2400, 4500, 2900])
    new_block += empty_para()

    # 교체
    content = content[:p_start_pos] + new_block + content[p_end_pos:]
    print("✅ B. Trinity of Joy 본문 → 3축 추진 전략 (도입 + 표 + 전략별 본문 + Trinity 압축 표)")
else:
    print(f"❌ B. anchor 못 찾음: start={start_idx}, end={end_idx}")


# 저장
with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
after = len(content)
print(f"\n파일 크기: {before} -> {after} (Δ {after - before})")
