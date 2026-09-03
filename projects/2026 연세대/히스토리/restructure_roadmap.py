"""
v10의 AX 역량 인증 3단계 로드맵 본문(▶ 단계 1·2·3 + 항목 7개씩)을
통합 표 1개(7행 × 4열)로 교체.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v10/word/document.xml'
with open(DOC_PATH, 'r', encoding='utf-8') as f:
    content = f.read()
before = len(content)


def empty_para():
    return '<w:p><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/><w:spacing w:before="120" w:after="120"/></w:pPr></w:p>'


def make_table(rows, col_widths, bold_first_col=True, header_fill='F0F4F8'):
    """첫 행은 헤더(굵게+배경), 첫 열도 항목명(굵게+옅은 배경) — 매트릭스 표 스타일"""
    total = sum(col_widths)
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)
    rows_xml = ''
    for r_idx, row in enumerate(rows):
        cells = ''
        for c_idx, cell_text in enumerate(row):
            w = col_widths[c_idx] if c_idx < len(col_widths) else col_widths[-1]
            is_header_row = (r_idx == 0)
            is_first_col = (c_idx == 0 and r_idx > 0)
            if is_header_row:
                fill = header_fill
                bold = True
                color = '222222'
            elif is_first_col and bold_first_col:
                fill = 'FAFCFE'
                bold = True
                color = '1F4E79'
            else:
                fill = 'FFFFFF'
                bold = False
                color = '222222'
            bold_xml = '<w:b/><w:bCs/>' if bold else ''
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
                f'<w:color w:val="{color}"/>'
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
# 식별: ▶ 단계 1.부터 단계 3 마지막 인증 줄까지
# ────────────────────────────────────────────────────────────
START_ANCHOR = "단계 1. 기초 — AX Starter"
END_ANCHOR = "역량 구성: 여러 AI를 묶어 자율 시스템을 만드는 하네스 엔지니어링 + 자기 시제품을 사회적 공개로 잇는 창의적 해결"

# 단계 3의 마지막 줄은 "인증: 총장 명의 AX 역량 인증서 발급"
# 안전하게 그 줄을 끝 anchor로 사용
END_ANCHOR_FINAL = "인증: 총장 명의 AX 역량 인증서 발급"

start_idx = content.find(START_ANCHOR)
end_idx = content.find(END_ANCHOR_FINAL)

if start_idx >= 0 and end_idx >= 0:
    # 시작 paragraph의 시작
    p_start = content.rfind('<w:p>', 0, start_idx)
    p_start_alt = content.rfind('<w:p ', 0, start_idx)
    p_start_pos = max(p_start, p_start_alt)
    # 끝 paragraph의 끝
    p_end_pos = content.find('</w:p>', end_idx) + len('</w:p>')

    # ▶ 단계 1·2·3 본문 영역 모두 식별 완료
    # 통합 표로 교체
    table_rows = [
        ['항목', 'AX Starter (기초)', 'AX Practitioner (활용)', 'AX Creator (심화)'],
        ['슬로건', '"AI를 이해하다"', '"AI로 만들다"', '"AI로 증명하다"'],
        ['대상', '국제캠퍼스 신입생\n(연세 AX 스타트)', '신촌캠퍼스 (연세 AX 아카데미) 및 AX Starter 이수자', '전 캠퍼스 (AX Practitioner 이수자, 공모전·쇼케이스 참여자)'],
        ['핵심 역량', 'AI 기초 리터러시,\n생성형 AI 도구 활용 능력', 'AI 도구 활용 실무 능력,\n주제별 문제 해결 역량', 'AI 기반 창의적 문제 해결,\n프로젝트 완수 및 사회적 확산 능력'],
        ['이수 요건', '체험 교육 + 입문 세미나 + 기초 워크숍 2건 이상', '주제별 워크숍 4건 이상 + 멘토링 프로젝트 1건', '공모전·경진대회 출품 + 최종 쇼케이스 발표 + AX 포트폴리오 제출'],
        ['Joy 매핑', 'Joy of Depth\n— AI 원리 이해', 'Joy of Expansion\n— 자기 전공·관심 도메인 적용', 'Joy of Originality\n— 나만의 결과물 사회적 공개'],
        ['역량 구성', '프롬프트 엔지니어링\n+ 자기 도메인 문제 발견', '컨텍스트 엔지니어링\n+ 문제 정의 → 해결안 설계', '하네스 엔지니어링\n+ 시제품의 사회적 공개'],
        ['인증', 'AX Starter 수료 인증\n(출결 + 기초 과제)', 'AX Practitioner 수료 인증\n(워크숍 이수 + 프로젝트 결과물)', '총장 명의\nAX 역량 인증서'],
    ]
    new_table = make_table(table_rows, [1500, 2700, 2700, 2700])

    # 새 블록: 표 + 빈 단락 (앞뒤 여백)
    new_block = empty_para() + new_table + empty_para()

    content = content[:p_start_pos] + new_block + content[p_end_pos:]
    print("✅ AX 역량 인증 3단계 로드맵 → 통합 표(8행 × 4열)로 교체")
else:
    print(f"❌ anchor 못 찾음: start={start_idx}, end={end_idx}")


with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
after = len(content)
print(f"\n파일 크기: {before} -> {after} (Δ {after - before})")
