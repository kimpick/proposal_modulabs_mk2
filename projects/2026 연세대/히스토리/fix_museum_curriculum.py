"""
박물관 영역 5 커리큘럼 정리:
1. Table 32 (박물관 통합 표) 교체 — 세미나 3→2, AI 창작 기초·심화 → 통합 워크숍 2회
2. Table 25, 26 워크숍명 수정 (기초·심화 → 매체별 다양화)
3. 본문에 매체 다양화 안내 단락 추가
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v14/word/document.xml'
with open(DOC_PATH, 'r', encoding='utf-8') as f:
    content = f.read()
before = len(content)


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


# ============================================================
# 1. Table 25, 26의 "AI 창작 워크숍 (기초·심화)" 텍스트 수정
# ============================================================
content = content.replace(
    'AI 창작 워크숍 (기초·심화)',
    'AI 활용 실감형 콘텐츠 제작·기획 워크숍'
)
print("✅ Table 25·26 워크숍명 수정")


# ============================================================
# 2. Table 32 (박물관 통합 표) 전면 교체
# ============================================================
# 기존 표 식별 마커: '인문학 세미나 1' 셀
old_marker = 'AX 시대, 인문학의 미래 (강연·Q&amp;A)'
idx = content.find(old_marker)
if idx >= 0:
    tbl_start = content.rfind('<w:tbl>', 0, idx)
    tbl_end = content.find('</w:tbl>', idx) + len('</w:tbl>')

    new_rows = [
        ['프로그램', '주제·진행', '도구·연사', '학생 산출물'],
        ['인문학 세미나 1',
         'AX 시대, 인문학의 미래 (강연·Q&amp;A)',
         '디지털 인문학·미디어철학 연구자 / NotebookLM',
         '강연록 정리 1편'],
        ['인문학 세미나 2',
         '한글을 지킨 연세의 거인들 (박물관 유물 투어 + 강의)',
         '국어학·연세 사학 전공자 / Gemini',
         '인물 아카이브 카드'],
        ['AI 활용 실감형 콘텐츠 제작·기획 워크숍 (1회차)',
         '박물관 컬렉션 재해석 → AI로 첫 시제품 제작 (3H)',
         'NotebookLM, ChatGPT, Midjourney, Suno + 매체별 도구',
         'AR 콘텐츠 / VR 공간 / MR 인터랙션 / Physical AI 중 1점 (택1)'],
        ['AI 활용 실감형 콘텐츠 제작·기획 워크숍 (2회차)',
         '시제품 발전 → 박물관 미니 전시·공유 (3H)',
         'ChatGPT, Canva, Gamma + 매체별 도구',
         '완성 작품 1점 + 전시 패널 1세트'],
        ['문화유산 기반 AX 공모전',
         '한글 고문헌 재해석 / 연세 인물 헌정 / 미공개 유물 큐레이션',
         '평가: 인문학 깊이 40 + 창의성 30 + AI 활용 20 + 완성도 10',
         '공모전 출품작 (우수작은 박물관 전시·디지털 아카이브)'],
    ]
    new_table = make_table(new_rows, [2700, 2700, 2200, 2400])
    content = content[:tbl_start] + new_table + content[tbl_end:]
    print("✅ Table 32 (박물관 통합 표) 교체 — 5행 (세미나 2 + 워크숍 2 + 공모전 1)")
else:
    print("❌ Table 32 marker 못 찾음")


# ============================================================
# 3. 본문에 매체 다양화 안내 단락 추가 (Table 32 위 또는 영역 5 본문 끝)
# ============================================================
# 영역 5 실감미디어 본문 단락 (Physical AI 사례 산출 시범 운영) 다음에 추가
anchor_text = "Physical AI 접점으로 VR 캠퍼스 투어 중 시선·동선 데이터를 AI가 요약해 학생 행동 페르소나 카드를 산출하는 사례를 시범 운영합니다."
idx = content.find(anchor_text)
if idx >= 0:
    p_end = content.find('</w:p>', idx) + len('</w:p>')

    extra_para = normal_para(
        "AI 활용 실감형 콘텐츠 제작·기획 워크숍은 학생이 박물관 컬렉션을 재해석하여 자기만의 실감형 콘텐츠를 직접 제작하는 자리입니다. 매체는 AR(유물에 덧붙는 증강현실 카드)·VR(박물관 공간 투어)·MR(손 제스처 인터랙션)·Physical AI(센서·동선 연동) 중에서 학생이 선택하며, 박물관 자원과 어울리는 형태를 본인이 결정합니다. 즉, 같은 워크숍 안에서 매체 선택에 따라 산출물 종류가 달라지며, 모두의연구소가 별도 개발하는 실감형 콘텐츠 5종은 이 워크숍의 학습 자료 겸 박물관 정규 운영 자산으로 활용됩니다."
    )
    content = content[:p_end] + extra_para + content[p_end:]
    print("✅ 영역 5 본문에 매체 다양화 안내 단락 추가")
else:
    print("❌ 영역 5 본문 anchor 못 찾음")


with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
after = len(content)
print(f"\n파일 크기: {before} -> {after} (Δ {after - before})")
