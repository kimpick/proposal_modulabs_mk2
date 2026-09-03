"""
v11의 4.가 추가 제안 내용 확장:
- 도입 단락 보강 (2가지 → 6가지)
- 통합 표 신규 추가 (6개 제안 한눈에)
- 신규 제안 4개 (모두콘 / VOD / AI 트렌드 세미나 / LAB 패컬티) 본문 + 이미지 placeholder
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v11/word/document.xml'
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

def empty_para():
    return '<w:p><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/><w:spacing w:before="120" w:after="120"/></w:pPr></w:p>'

def emphasis_heading(text):
    return (
        '<w:p>'
        '<w:pPr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="E6EEF5"/>'
        '<w:spacing w:before="240" w:after="120"/>'
        '<w:jc w:val="both"/>'
        '</w:pPr>'
        '<w:r>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
        '<w:b/><w:bCs/>'
        '<w:color w:val="002B5C"/>'
        '<w:sz w:val="22"/><w:szCs w:val="22"/>'
        '<w:shd w:val="clear" w:color="auto" w:fill="E6EEF5"/>'
        '</w:rPr>'
        f'<w:t xml:space="preserve">{text}</w:t>'
        '</w:r>'
        '</w:p>'
    )

def url_para(text):
    """URL 안내 단락 — 작은 회색 글자"""
    return (
        '<w:p>'
        '<w:pPr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
        '<w:spacing w:before="0" w:after="120"/>'
        '<w:jc w:val="both"/>'
        '</w:pPr>'
        '<w:r>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
        '<w:color w:val="666666"/>'
        '<w:sz w:val="18"/><w:szCs w:val="18"/>'
        '</w:rPr>'
        f'<w:t xml:space="preserve">{text}</w:t>'
        '</w:r>'
        '</w:p>'
    )


def make_strategy_table(rows, col_widths):
    """일반 4열 표 - 추가 제안 통합용"""
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


def make_image_placeholder(caption):
    """이미지 첨부 공간 — 회색 박스 1행 1열 표"""
    return (
        '<w:tbl>'
        '<w:tblPr>'
        '<w:tblW w:w="9400" w:type="dxa"/>'
        '<w:tblInd w:w="-2" w:type="dxa"/>'
        '<w:tblBorders>'
        '<w:top w:val="dashed" w:sz="6" w:space="0" w:color="B3C6D9"/>'
        '<w:left w:val="dashed" w:sz="6" w:space="0" w:color="B3C6D9"/>'
        '<w:bottom w:val="dashed" w:sz="6" w:space="0" w:color="B3C6D9"/>'
        '<w:right w:val="dashed" w:sz="6" w:space="0" w:color="B3C6D9"/>'
        '<w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
        '</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/>'
        '</w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="9400"/></w:tblGrid>'
        '<w:tr><w:trPr><w:trHeight w:val="2200"/></w:trPr>'
        '<w:tc>'
        '<w:tcPr>'
        '<w:tcW w:w="9400" w:type="dxa"/>'
        '<w:shd w:val="clear" w:color="auto" w:fill="F8FAFC"/>'
        '<w:tcMar><w:top w:w="400" w:type="dxa"/><w:left w:w="200" w:type="dxa"/><w:bottom w:w="400" w:type="dxa"/><w:right w:w="200" w:type="dxa"/></w:tcMar>'
        '<w:vAlign w:val="center"/>'
        '</w:tcPr>'
        '<w:p>'
        '<w:pPr><w:spacing w:before="0" w:after="80"/><w:jc w:val="center"/></w:pPr>'
        '<w:r>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
        '<w:b/><w:bCs/>'
        '<w:color w:val="888888"/>'
        '<w:sz w:val="22"/><w:szCs w:val="22"/>'
        '</w:rPr>'
        '<w:t xml:space="preserve">[ 이미지 첨부 위치 ]</w:t>'
        '</w:r>'
        '</w:p>'
        '<w:p>'
        '<w:pPr><w:spacing w:before="0" w:after="0"/><w:jc w:val="center"/></w:pPr>'
        '<w:r>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
        '<w:i/><w:iCs/>'
        '<w:color w:val="999999"/>'
        '<w:sz w:val="20"/><w:szCs w:val="20"/>'
        '</w:rPr>'
        f'<w:t xml:space="preserve">{caption}</w:t>'
        '</w:r>'
        '</w:p>'
        '</w:tc>'
        '</w:tr>'
        '</w:tbl>'
    )


# ────────────────────────────────────────────────────────────
# 1) 도입 단락 보강 (2가지 → 6가지)
# ────────────────────────────────────────────────────────────
old_intro = "연세대학교가 본 사업을 통해 만들고자 하는 것은 단발성 교육 운영 결과가 아니라, 학부생이 졸업 이후에도 AI 시대를 자기 언어로 살아갈 수 있는 역량입니다. 모두의연구소는 본 사업의 90건 과정 운영에 더해, 다음 두 가지 차별화 제안을 함께 드립니다. 두 제안 모두 별도 비용 부담 없이 본 사업 예산 내에서 수행 가능합니다."
new_intro = "연세대학교가 본 사업을 통해 만들고자 하는 것은 단발성 교육 운영 결과가 아니라, 학부생이 졸업 이후에도 AI 시대를 자기 언어로 살아갈 수 있는 역량입니다. 모두의연구소는 본 사업의 90건 과정 운영에 더해, 다음 6가지 차별화 제안을 함께 드립니다. 모든 제안은 모두의연구소가 이미 운영 중인 학습 자산을 본 사업에 연계하는 방식이므로, 별도 비용 부담 없이 본 사업 예산 내에서 수행 가능합니다."
content = content.replace(old_intro, new_intro)
print("✅ 도입 단락 보강 (6가지로)")


# ────────────────────────────────────────────────────────────
# 2) 통합 표 + 신규 제안 4개를 마지막 마무리 단락 앞에 삽입
# ────────────────────────────────────────────────────────────
# 마지막 마무리 anchor 찾기
END_ANCHOR = "두 제안의 의미는 명확합니다. 본 사업이 종료된 뒤에도 학생의 AX 역량은 누적되고 연결됩니다"
end_idx = content.find(END_ANCHOR)
if end_idx < 0:
    print("❌ 마무리 anchor 못 찾음")
    sys.exit(1)

# 마무리 paragraph 시작점 (그 직전에 삽입)
p_start_pos = content.rfind('<w:p>', 0, end_idx)
p_start_alt = content.rfind('<w:p ', 0, end_idx)
p_start_pos = max(p_start_pos, p_start_alt)

# 마무리 본문도 6가지 반영하여 살짝 보강
old_closing = "두 제안의 의미는 명확합니다. 본 사업이 종료된 뒤에도 학생의 AX 역량은 누적되고 연결됩니다. 인증서가 학생의 손을 떠나는 순간 효력이 사라지는 일반적인 인증제와, 인증서가 학생의 다음 단계와 연결되는 본 제안의 차이는 결국 학생이 졸업할 때 본인의 AX 역량을 어떻게 설명할 수 있는가의 차이로 나타납니다."
new_closing = "여섯 가지 제안의 의미는 명확합니다. 본 사업이 종료된 뒤에도 학생의 AX 역량은 누적되고 연결됩니다. 인증서가 학생의 손을 떠나는 순간 효력이 사라지는 일반적인 인증제와, 인증서가 학생의 다음 단계(컨퍼런스·VOD·세미나·LAB·동문 네트워크)로 연결되는 본 제안의 차이는 결국 학생이 졸업할 때 본인의 AX 역량을 어떻게 설명할 수 있는가의 차이로 나타납니다."
content = content.replace(old_closing, new_closing)
print("✅ 마무리 단락 보강")


# 다시 마무리 paragraph 시작점 찾기 (replace 후 위치 변동)
end_idx = content.find("여섯 가지 제안의 의미는 명확합니다")
p_start_pos = content.rfind('<w:p>', 0, end_idx)
p_start_alt = content.rfind('<w:p ', 0, end_idx)
p_start_pos = max(p_start_pos, p_start_alt)

# 추가할 블록 빌드
new_block = ""

# 통합 표 헤더
new_block += emphasis_heading("6가지 차별화 제안 요약")

# 통합 표
summary_rows = [
    ['#', '제안', '핵심 내용', '학생 효과'],
    ['1', 'AX 역량 인증제 고도화', '학습 이력 누적 + 자가진단 + 결과물 포트폴리오', '인증이 졸업 후로 이어짐'],
    ['2', '풀잎스쿨·AIFFEL 동문 연계', '거꾸로 학습 모임, AI 혁신학교 동문 네트워크', '수료 후에도 학습 동료 연결'],
    ['3', '모두콘 우수자 세션 참여', '국내 대표 AI·테크 컨퍼런스 (2018~)', '산업 현장과 직접 연결'],
    ['4', '맞춤형 온라인 VOD 제공', '멘토링 참여자 자기주도 학습', '시간·장소 제약 없는 보강 학습'],
    ['5', '매달 AI 트렌드 세미나 초대', '모두의연구소 정기 무료 세미나', '학습 후에도 트렌드 지속 노출'],
    ['6', '모두의연구소 LAB 패컬티 소개', '60개 이상 분야별 연구 모임', '심화 연구·진로 연결'],
]
new_block += make_strategy_table(summary_rows, [600, 2400, 4000, 2400])
new_block += empty_para()


# 신규 제안 3·4·5·6 본문 + 이미지 placeholder
# 제안 3. 모두콘
new_block += emphasis_heading('제안 3. 모두콘 우수자 세션 참여 — "AI 컨퍼런스 무대로 가는 길"')
new_block += empty_para()
new_block += normal_para(
    "모두콘은 모두의연구소가 2018년부터 매년 개최해 온 국내 대표 커뮤니티 기반 AI·테크 컨퍼런스입니다. 현업 전문가들이 모여 최신 기술 트렌드와 실전 사례를 공유하는 행사로, 2025년에는 모두의연구소 10주년을 맞아 AI의 현재·미래·커뮤니티 확장을 다루는 특별 세션이 진행되었습니다. 본 사업의 우수 수료자에게는 모두콘 세션 참가 기회를 우선 제공하며, 우수 결과물의 발표 기회까지 안내합니다. 학부생이 강의실 안에서 만든 결과물을 산업 현장의 청중과 만나게 하는 통로입니다."
)
new_block += url_para("자세히 보기: moducon.modulabs.co.kr")
new_block += empty_para()
new_block += make_image_placeholder("모두콘 메인 비주얼 / 행사 사진 / 키비주얼")
new_block += empty_para()


# 제안 4. VOD
new_block += emphasis_heading('제안 4. 멘토링 참여 인원 맞춤형 온라인 VOD 제공 — "끊기지 않는 학습"')
new_block += empty_para()
new_block += normal_para(
    "멘토링 프로젝트에 참여한 학생에게는 모두의연구소가 운영하는 온라인 클래스의 맞춤형 VOD를 멘토링의 일환으로 제공합니다. 멘토가 학생의 학습 경로에 맞춰 강의 1~3개를 선별·추천하며, 학생은 시간·장소 제약 없이 자기 주도로 보강 학습을 이어갈 수 있습니다. 본 사업의 워크숍·멘토링 시간 외에도 학습이 끊기지 않도록 받쳐주는 보조 장치입니다."
)
new_block += url_para("자세히 보기: class.modulabs.co.kr")
new_block += empty_para()
new_block += make_image_placeholder("모두의연구소 온라인 클래스 화면 / VOD 라이브러리 캡처")
new_block += empty_para()


# 제안 5. 트렌드 세미나
new_block += emphasis_heading('제안 5. 매달 AI 트렌드 세미나 초대 — "변화의 흐름을 놓치지 않게"')
new_block += empty_para()
new_block += normal_para(
    "모두의연구소는 매달 AI 분야의 최신 트렌드를 다루는 무료 세미나를 운영합니다. 본 사업에 참여한 모든 학생은 사업 종료 이후에도 이 세미나에 우선 안내됩니다. 학기·졸업 등 학사 일정 변화와 무관하게 학생이 AI 변화의 흐름을 놓치지 않도록 지속적인 학습 접점을 제공합니다."
)
new_block += url_para("자세히 보기: modulabs.co.kr (메인 세미나 섹션)")
new_block += empty_para()
new_block += make_image_placeholder("모두의연구소 정기 세미나 일정 / 세미나 행사 사진")
new_block += empty_para()


# 제안 6. LAB
new_block += emphasis_heading('제안 6. 모두의연구소 LAB 패컬티 소개·참여 기회 — "심화 연구로 가는 길"')
new_block += empty_para()
new_block += normal_para(
    "모두의연구소 LAB은 분야별 연구원·실무자가 자율적으로 운영하는 60개 이상의 연구 모임입니다. AX Creator 인증을 받은 학부생 중 심화 연구를 원하는 학생에게 관심 분야 LAB을 소개하고 참여 기회를 제공합니다. 학부생이 졸업 후 산업·연구 현장의 실무자와 직접 연결되는 통로로 작동하며, 본 사업에서 만든 결과물이 LAB의 후속 연구로 발전하는 사례도 만들 수 있습니다."
)
new_block += url_para("자세히 보기: modulabs.co.kr/labs")
new_block += empty_para()
new_block += make_image_placeholder("모두의연구소 LAB 페이지 캡처 / LAB 활동 사진")
new_block += empty_para()


# 삽입
content = content[:p_start_pos] + new_block + content[p_start_pos:]
print("✅ 통합 표 + 신규 제안 4개(본문 + 이미지 placeholder) 삽입")


# 기존 제안 1·2 헤딩 정리: "제안 1.", "제안 2."
# 이는 일반 paragraph로 들어가 있어서 그대로 유지 (내부 일관성을 위해)
# 다만 도입에서 "다음 두 가지 차별화 제안" 표현이 도입 보강으로 "6가지"로 바뀜


with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
after = len(content)
print(f"\n파일 크기: {before} -> {after} (Δ {after - before})")
