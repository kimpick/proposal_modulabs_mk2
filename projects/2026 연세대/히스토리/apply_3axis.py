"""
v7에 3축 구조 반영:
1) 운영 메서드 도입 3문단을 4문단(축 1·2·3 + 만남)으로 확장
2) 시각화 표를 3열 → 4열로 교체 (배움의 즐거움 컬럼 추가)
3) 1.라 도입 + 2.가 응답에 세 축 메시지 추가
4) Trinity of Joy 도입을 "셋째 축"으로 격상
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v7/word/document.xml'
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
    return (
        '<w:p>'
        '<w:pPr><w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/><w:spacing w:before="120" w:after="120"/></w:pPr>'
        '</w:p>'
    )


def make_3axis_table(rows, col_widths):
    """4열 표 (좌: AI 리터러시 / 학생 / 디자인씽킹 / 우: 배움의 즐거움)
    좌·우 컬럼 색상 차별: 1열 #1F4E79, 3열 #7B3F00, 4열 #2D5F3F
    """
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
            color = '222222'
            if not is_header:
                if c_idx == 0:
                    color = '1F4E79'  # 파랑
                elif c_idx == 2:
                    color = '7B3F00'  # 갈색
                elif c_idx == 3:
                    color = '2D5F3F'  # 진초록 (배움의 즐거움)
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
                f'<w:tcMar><w:top w:w="120" w:type="dxa"/><w:left w:w="140" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tcMar>'
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
# 1. 운영 메서드 도입 3문단 → 4문단으로 교체
#    + 그 뒤 시각화 표 도입 문장도 교체
# ────────────────────────────────────────────────────────────

# 첫 문단 교체
old_p1 = "본 사업의 90건은 두 가지 축으로 묶입니다. 첫 번째 축은 도구가 바뀌어도, 전공이 달라도 흔들리지 않는 AI 리터러시입니다. 학생은 프롬프트 엔지니어링(원하는 답을 끌어내는 법) → 컨텍스트 엔지니어링(AI에게 적절한 정보·역할을 설계하는 법) → 하네스 엔지니어링(여러 AI를 묶어 자율 시스템을 만드는 법)으로 이어지는 단계적 심화 경로를 통과합니다. 도구가 ChatGPT에서 Gemini로 바뀌어도, 전공이 인문학에서 공학으로 바뀌어도 동일하게 통하는 역량입니다."
new_p1 = "본 사업의 90건은 세 개의 축이 동시에 작동하는 구조 위에서 운영됩니다. 첫 번째 축은 도구가 바뀌어도, 전공이 달라도 흔들리지 않는 AI 리터러시입니다. 학생은 프롬프트 엔지니어링(원하는 답을 끌어내는 법) → 컨텍스트 엔지니어링(AI에게 적절한 정보·역할을 설계하는 법) → 하네스 엔지니어링(여러 AI를 묶어 자율 시스템을 만드는 법)으로 이어지는 단계적 심화 경로를 통과합니다. 도구가 ChatGPT에서 Gemini로 바뀌어도, 전공이 인문학에서 공학으로 바뀌어도 동일하게 통하는 역량 — 학생의 손에 해당하는 축입니다."

# 셋째 문단(원래 마무리)을 둘로 분리. 두 번째 문단은 그대로 두고, 셋째 축(배움의 즐거움)을 그 사이에 끼움.
old_p3 = "두 축이 만나는 자리가 「AI 시대의 Design Thinking 프로젝트」이며, 아래 5단계 운영 프레임은 그 만남이 90건 모든 과정에서 일관되게 일어나도록 받쳐주는 운영 메서드입니다. 본 사업의 90건 모든 과정은 — 대상이 신입생이든 고학년이든, 형식이 체험·세미나·워크숍·멘토링·공모전이든 — 동일한 5단계 흐름 안에서 운영됩니다."

new_p3_axis3 = (
    "세 번째 축은 배움의 즐거움(The Trinity of Joy)입니다. 앞의 두 축이 학생이 무엇을·어떻게 배우는가를 다룬다면, 이 축은 학생이 왜 학습을 멈추지 않는가에 답합니다. 깊이의 즐거움(Joy of Depth) — 원리를 이해해 도구가 바뀌어도 무섭지 않은 감각, 확장의 즐거움(Joy of Expansion) — 자기 전공·일상에 기술이 닿는 순간의 감각, 자기다움의 즐거움(Joy of Originality) — 자기 결과물에 세상이 반응하는 감각이 학생을 1년 사업 끝까지 움직이게 합니다. 즉, 배움의 즐거움은 본 사업의 원동력입니다."
)

new_p3_meeting = (
    "세 축이 만나는 자리가 「AI 시대의 Design Thinking 프로젝트」이며, 아래 5단계 운영 프레임은 그 만남이 90건 모든 과정에서 일관되게 일어나도록 받쳐주는 운영 메서드입니다. 본 사업의 90건 모든 과정은 — 대상이 신입생이든 고학년이든, 형식이 체험·세미나·워크숍·멘토링·공모전이든 — 동일한 5단계 흐름 안에서 운영됩니다."
)

# 첫 문단 교체
if old_p1 in content:
    content = content.replace(old_p1, new_p1)
    print("✅ 운영 메서드 첫 문단 교체 (3축 도입)")
else:
    print("❌ 운영 메서드 첫 문단 없음")

# 셋째 문단 분할: 셋째 축 단락 추가 + 만남 단락 교체
if old_p3 in content:
    # old_p3의 paragraph element 전체를 신규 두 paragraph로 교체
    # 단순 텍스트 replace로는 안 되니, paragraph 단위 교체
    idx = content.find(old_p3)
    p_start = content.rfind('<w:p>', 0, idx)
    p_start_alt = content.rfind('<w:p ', 0, idx)
    p_start = max(p_start, p_start_alt)
    p_end = content.find('</w:p>', idx) + len('</w:p>')

    # 새 paragraph 두 개로 교체
    new_block = normal_para(new_p3_axis3) + normal_para(new_p3_meeting)
    content = content[:p_start] + new_block + content[p_end:]
    print("✅ 운영 메서드 셋째 문단 → 두 단락으로 (축3 추가 + 만남)")
else:
    print("❌ 운영 메서드 셋째 문단 없음")


# ────────────────────────────────────────────────────────────
# 2. 시각화 표를 4열로 교체
# ────────────────────────────────────────────────────────────
# 시각화 도입 문장 교체
old_viz_intro = "두 축은 서로 떨어진 별개의 학습 영역이 아니라, 학생이 단계를 밟을 때마다 동시에 한 칸씩 깊어지는 구조입니다. 입문 단계의 학생은 프롬프트 엔지니어링을 익히면서 자기 도메인의 문제를 발견하고, 활용 단계에서는 컨텍스트 엔지니어링으로 그 문제를 정의·설계하며, 심화 단계에서는 하네스 엔지니어링으로 시제품을 만들어 세상에 공개합니다."
new_viz_intro = "세 축은 서로 떨어진 별개의 학습 영역이 아니라, 학생이 단계를 밟을 때마다 동시에 한 칸씩 깊어지는 구조입니다. 입문 단계의 학생은 프롬프트 엔지니어링을 익히면서 자기 도메인의 문제를 발견하고, 활용 단계에서는 컨텍스트 엔지니어링으로 그 문제를 정의·설계하며, 심화 단계에서는 하네스 엔지니어링으로 시제품을 만들어 세상에 공개합니다. 매 단계마다 깊이·확장·자기다움이라는 세 가지 즐거움이 학습을 다음 단계로 끌고 갑니다."
content = content.replace(old_viz_intro, new_viz_intro)
print("✅ 시각화 도입 문장 (3축으로)")

# 시각화 헤더 교체
content = content.replace(
    "학생 성장 단계로 본 두 축의 동시 진행",
    "학생 성장 단계로 본 세 축의 동시 진행"
)
print("✅ 시각화 헤더 텍스트 교체")

# 기존 3열 시각화 표를 4열로 교체
# 현재 표 시작은 "AI 리터러시 축\n(도구가 바뀌어도)"부터
old_viz_table_start_marker = '<w:tbl><w:tblPr><w:tblStyle w:val="af1"/><w:tblW w:w="9400" w:type="dxa"/>'
# 안전하게: 기존 3열 표 패턴 찾기 ('AI 리터러시 축' + '디자인씽킹 축' 헤더)
import re
# 시각화 표 삭제 + 새 표 삽입
# 마커 텍스트로 표 위치 확인
viz_cell_marker = "AI 리터러시 축"
idx = content.find(viz_cell_marker)
if idx >= 0:
    # 그 표의 <w:tbl> 시작
    tbl_start = content.rfind('<w:tbl>', 0, idx)
    tbl_end = content.find('</w:tbl>', idx) + len('</w:tbl>')

    # 새 4열 표 데이터
    new_viz_rows = [
        ['AI 리터러시 축\n(도구가 바뀌어도)', '학생 성장 단계', '디자인씽킹 축\n(전공이 달라도)', '배움의 즐거움\n(학습의 원동력)'],
        ['프롬프트 엔지니어링', 'AX Starter\n(입문)', '자기 도메인의 문제 발견', 'Joy of Depth\n— 원리를 이해하는 깊이'],
        ['컨텍스트 엔지니어링', 'AX Practitioner\n(활용)', '문제 정의 → 해결안 설계', 'Joy of Expansion\n— 내 전공·일상에 닿는 확장'],
        ['하네스 엔지니어링', 'AX Creator\n(심화)', '창의적 시제품 → 사회적 공개', 'Joy of Originality\n— 세상이 반응하는 자기다움'],
    ]
    new_viz_table = make_3axis_table(new_viz_rows, [2300, 2000, 2700, 2400])
    content = content[:tbl_start] + new_viz_table + content[tbl_end:]
    print("✅ 시각화 표 4열로 교체 (배움의 즐거움 컬럼 추가)")
else:
    print("❌ 시각화 표 못 찾음")


# ────────────────────────────────────────────────────────────
# 3. 1.라 도입 + 2.가 응답에 셋째 축 한 줄 보강
# ────────────────────────────────────────────────────────────
# 1.라 도입: 두 축 → 세 축
old_a = "본 사업의 골격은 두 축이 만나는 자리에 있습니다. 한 축은 도구가 바뀌어도, 전공이 달라도 흔들리지 않는 AI 리터러시 — 프롬프트 엔지니어링에서 컨텍스트 엔지니어링을 거쳐 하네스 엔지니어링으로 이어지는 단계적 심화입니다. 다른 한 축은 디자인씽킹을 통해 학생 본인의 고유한 문제를 발견하고 창의적으로 풀어내는 경험입니다. 본 사업은 이 두 축이 한 학기 안에 학생에게 도달하도록 설계된 교육 로드맵으로,"
new_a = "본 사업의 골격은 세 축이 함께 작동하는 자리에 있습니다. 첫 번째 축은 도구가 바뀌어도, 전공이 달라도 흔들리지 않는 AI 리터러시 — 프롬프트 엔지니어링에서 컨텍스트 엔지니어링을 거쳐 하네스 엔지니어링으로 이어지는 단계적 심화입니다. 두 번째 축은 디자인씽킹을 통해 학생 본인의 고유한 문제를 발견하고 창의적으로 풀어내는 경험입니다. 세 번째 축은 학습이 멈추지 않게 하는 배움의 즐거움(Trinity of Joy) — 깊이·확장·자기다움의 세 가지 즐거움이 본 사업의 원동력입니다. 본 사업은 이 세 축이 한 학기 안에 학생에게 도달하도록 설계된 교육 로드맵으로,"
if old_a in content:
    content = content.replace(old_a, new_a)
    print("✅ 1.라 도입 → 세 축 메시지로")
else:
    print("❌ 1.라 도입 못 찾음")

# 2.가 응답: 두 축 → 세 축
old_b = "모두의연구소는 위 3대 목표에 응답하기 위해, 두 축의 교차점을 본 사업의 골격으로 삼습니다. 한 축은 도구가 바뀌어도 흔들리지 않는 AI 리터러시 — 프롬프트 · 컨텍스트 · 하네스 엔지니어링의 단계적 심화이며, 다른 한 축은 디자인씽킹을 통한 자기 문제 발견과 창의적 해결입니다. 다음 네 가지 수행 목표는 두 축이 모든 학부생에게 도달하도록 만드는 실행 계획이며, 가·나는 ①·②에, 다는 ②·③에, 라는 ②에 직접 대응합니다."
new_b = "모두의연구소는 위 3대 목표에 응답하기 위해, 세 축의 교차점을 본 사업의 골격으로 삼습니다. 첫 축은 도구가 바뀌어도 흔들리지 않는 AI 리터러시 — 프롬프트 · 컨텍스트 · 하네스 엔지니어링의 단계적 심화, 둘째 축은 디자인씽킹을 통한 자기 문제 발견과 창의적 해결, 셋째 축은 학습이 멈추지 않게 하는 배움의 즐거움(Trinity of Joy)입니다. 다음 네 가지 수행 목표는 세 축이 모든 학부생에게 도달하도록 만드는 실행 계획이며, 가·나는 ①·②에, 다는 ②·③에, 라는 ②에 직접 대응합니다."
if old_b in content:
    content = content.replace(old_b, new_b)
    print("✅ 2.가 응답 → 세 축 메시지로")
else:
    print("❌ 2.가 응답 못 찾음")


# ────────────────────────────────────────────────────────────
# 4. Trinity of Joy 도입을 "셋째 축"으로 격상
# ────────────────────────────────────────────────────────────
old_t_intro = "위 네 가지 목표를 달성하기 위해, 모든 프로그램은 아래 세 가지 즐거움을 설계 원칙으로 삼습니다."
new_t_intro = "Trinity of Joy는 본 사업의 셋째 축이자 학습이 멈추지 않게 하는 원동력입니다. AI 리터러시(첫 축)와 디자인씽킹(둘째 축)이 학생의 손과 시선을 만든다면, 배움의 즐거움은 그 손과 시선이 1년 사업 끝까지 움직이도록 떠받칩니다. 모든 프로그램은 아래 세 가지 즐거움을 설계 원칙으로 삼습니다."
if old_t_intro in content:
    content = content.replace(old_t_intro, new_t_intro)
    print("✅ Trinity of Joy 도입 → 셋째 축 메시지로 격상")
else:
    print("❌ Trinity of Joy 도입 못 찾음")


# ────────────────────────────────────────────────────────────
# 5. 주제 영역별 도입 한 줄 보강 (선택: 영역별도 셋째 축 언급)
# ────────────────────────────────────────────────────────────
old_d = "5대 주제 영역의 대표 워크숍과 학생 산출물을 정리합니다. 영역은 다르지만 모든 워크숍은 동일한 두 축 위에서 운영됩니다. 한 축은 프롬프트 → 컨텍스트 → 하네스 엔지니어링으로 이어지는 AI 리터러시의 단계적 심화이며, 다른 한 축은 디자인씽킹을 통한 자기 문제 발견과 창의적 해결입니다. 따라서 학생이 어느 영역을 선택하든, 어느 캠퍼스에서 시작하든 두 축은 동일하게 작동하며, 각 워크숍의 회별 모듈·도구·산출물이 학생 인증 포트폴리오에 누적됩니다."
new_d = "5대 주제 영역의 대표 워크숍과 학생 산출물을 정리합니다. 영역은 다르지만 모든 워크숍은 동일한 세 축 위에서 운영됩니다. AI 리터러시(프롬프트 → 컨텍스트 → 하네스 엔지니어링), 디자인씽킹(자기 문제 발견과 창의적 해결), 그리고 배움의 즐거움이 학습의 원동력으로 함께 작동합니다. 따라서 학생이 어느 영역을 선택하든, 어느 캠퍼스에서 시작하든 세 축은 동일하게 작동하며, 각 워크숍의 회별 모듈·도구·산출물이 학생 인증 포트폴리오에 누적됩니다."
if old_d in content:
    content = content.replace(old_d, new_d)
    print("✅ 주제 영역별 도입 → 세 축 메시지로")
else:
    print("❌ 주제 영역별 도입 못 찾음")


with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

after = len(content)
print(f"\n파일 크기: {before} -> {after} (Δ {after - before})")
