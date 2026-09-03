"""
v6 사업 수행 목표 가·나·다·라 본문 직후에 미니 표 4개 삽입
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v6/word/document.xml'
with open(DOC_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

before = len(content)


def empty_para():
    return (
        '<w:p>'
        '<w:pPr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
        '<w:spacing w:before="120" w:after="120"/>'
        '</w:pPr>'
        '</w:p>'
    )


def make_table(rows, col_widths, bold_header=True):
    total = sum(col_widths)
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)
    rows_xml = ''
    for r_idx, row in enumerate(rows):
        cells = ''
        for c_idx, cell_text in enumerate(row):
            w = col_widths[c_idx] if c_idx < len(col_widths) else col_widths[-1]
            is_header = (r_idx == 0)
            fill = 'F0F4F8' if is_header else 'FFFFFF'
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
                f'<w:tcMar><w:top w:w="100" w:type="dxa"/><w:left w:w="140" w:type="dxa"/><w:bottom w:w="100" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tcMar>'
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
        rows_xml += f'<w:tr><w:trPr><w:trHeight w:val="380"/></w:trPr>{cells}</w:tr>'
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


def insert_after_anchor(content, anchor_text, block_xml):
    """anchor_text가 들어있는 paragraph의 </w:p> 다음에 block_xml 삽입"""
    idx = content.find(anchor_text)
    if idx < 0:
        return content, False
    p_end = content.find('</w:p>', idx) + len('</w:p>')
    return content[:p_end] + block_xml + content[p_end:], True


# ────────────────────────────────────────────────────────────
# 목표 가. 표
# ────────────────────────────────────────────────────────────
ga_rows = [
    ['항목', '세부 내용', '정량 지표'],
    ['운영 기관', '신촌 학술정보관 · 국제캠퍼스 도서관 · 신촌 박물관', '3개 기관'],
    ['프로그램 브랜드', '연세 AX 아카데미 · 연세 AX 스타트 · 연세 AX 뮤즈로그', '기관별 독립 운영'],
    ['교육 유형별 규모', '체험 5 + 세미나 8 + 워크숍 41 + 멘토링 9 + 공모전 7 + 콘텐츠 20', '90건 / 343회 / 549시간'],
    ['단계별 연계', '국제 신입생(스타트) → 신촌 심화(아카데미) 자연 연계', '학부 재학 중 이수 가능'],
    ['검증 방법', '기관별 학기 종료 보고 + 발주처 분기 합동 점검', '분기 4회 + 학기 2회'],
]
ga_block = empty_para() + make_table(ga_rows, [2200, 5400, 2200]) + empty_para()
# anchor: 목표 가의 두 번째 본문 줄 끝
ga_anchor = "달성 기준: 총 90건 과정, 343회, 549시간 교육 운영 완료"
content, ok = insert_after_anchor(content, ga_anchor, ga_block)
print(f"{'✅' if ok else '❌'} 목표 가 표 삽입")

# ────────────────────────────────────────────────────────────
# 목표 나. 표
# ────────────────────────────────────────────────────────────
na_rows = [
    ['시기', '단계', '운영 프로그램', '학생 산출물'],
    ['봄학기 (3~6월)', '문제 발견', '디자인씽킹 워크숍, AX 트렌드 세미나', '자기 도메인 문제 진술서 1편'],
    ['여름방학 (7~8월)', '기술 심화', 'AX 심화 캠프 (워크숍 + 멘토링), 콘텐츠 개발 집중', '동작 시제품(MVP) 1건'],
    ['가을학기 (9~12월)', '프로젝트 수행', '멘토링 프로젝트, 공모전 연계 기술 워크숍', '공모전 출품작 1건'],
    ['겨울방학 (1~2월)', '성과 확산', '최종 쇼케이스, Wild Public Release', '인증 포트폴리오 1건'],
]
na_block = empty_para() + make_table(na_rows, [1700, 1500, 3700, 2900]) + empty_para()
# anchor: 목표 나의 두 번째 본문 줄 끝
na_anchor = "체험 교육(5건) → 세미나(8건) → 워크숍(41건) → 멘토링(9건) → 공모전·성과 공유(7건) + 콘텐츠 개발(20건)의 단계적 교육 체계를 구성합니다"
content, ok = insert_after_anchor(content, na_anchor, na_block)
print(f"{'✅' if ok else '❌'} 목표 나 표 삽입")

# ────────────────────────────────────────────────────────────
# 목표 다. 표
# ────────────────────────────────────────────────────────────
da_rows = [
    ['단계', '인증명', '대상', '핵심 이수 요건', '발급'],
    ['기초', 'AX Starter', '국제캠 신입생', '체험 교육 + 입문 세미나 + 기초 워크숍 2건', 'Starter 수료 인증'],
    ['활용', 'AX Practitioner', '신촌 + Starter 이수자', '주제별 워크숍 4건 + 멘토링 프로젝트 1건', 'Practitioner 수료 인증'],
    ['심화', 'AX Creator', '전 캠퍼스', '공모전 출품 + 쇼케이스 발표 + AX 포트폴리오 제출', '총장 명의 AX 역량 인증서'],
]
da_block = empty_para() + make_table(da_rows, [800, 1700, 1700, 3500, 2100]) + empty_para()
# anchor: 목표 다의 두 번째 본문 줄 끝
da_anchor = "국제캠퍼스 연세 AX 스타트(신입생)에서 신촌캠퍼스 연세 AX 아카데미(심화)로 자연 연계되는 로드맵을 구성합니다"
content, ok = insert_after_anchor(content, da_anchor, da_block)
print(f"{'✅' if ok else '❌'} 목표 다 표 삽입")

# ────────────────────────────────────────────────────────────
# 목표 라. 표
# ────────────────────────────────────────────────────────────
ra_rows = [
    ['구분', '종수', '주제 영역', '활용처'],
    ['실습 교육 콘텐츠', '15종', '생성형 AI / 데이터 분석 / AI 에이전트 / 디지털 콘텐츠 / 인문학 융합', '워크숍·멘토링 운영 자료'],
    ['실감형 콘텐츠', '5종', 'VR/AR/MR 기반 + Physical AI 접점 (공간 인식·센서 연동)', '박물관 체험 교육'],
    ['합계', '20종', '주제별·수준별 + 실감형 통합', '발주처 자산으로 귀속'],
]
ra_block = empty_para() + make_table(ra_rows, [2000, 800, 4400, 2600]) + empty_para()
# anchor: 목표 라의 두 번째 본문 줄 끝
ra_anchor = "Physical AI 기술 요소(센서 데이터 연동, 공간 인식 AI 등)와의 접점을 탐색하여 차세대 실감 교육 콘텐츠를 기획합니다"
content, ok = insert_after_anchor(content, ra_anchor, ra_block)
print(f"{'✅' if ok else '❌'} 목표 라 표 삽입")


with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

after = len(content)
print(f"\n파일 크기: {before} -> {after} (Δ {after - before})")
