"""
v4의 핵심 문장 4곳을 두 축(AI 리터러시 + 디자인씽킹) 메시지로 교체
- 변형 A: 1.라 제안 내용 요약 도입
- 변형 B: 2.가 RFP 3대 목표 응답
- 변형 C: 운영 메서드 도입 (2문단 → 3문단)
- 변형 D: 주제 영역별 도입
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v4/word/document.xml'

with open(DOC_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

before = len(content)

# ─── 표준 본문 paragraph 빌더 (v1 표준 서식) ──────────────────
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


def replace_paragraph_containing(content, search_text, new_para_xml):
    """search_text가 들어있는 paragraph 1개를 new_para_xml로 통째 교체"""
    # paragraph 시작/끝 위치 찾기
    idx = content.find(search_text)
    if idx < 0:
        print(f"⚠️ NOT FOUND: '{search_text[:40]}...'")
        return content, False
    # idx 위치에서 거꾸로 <w:p ... > 또는 <w:p> 찾기
    p_start = content.rfind('<w:p>', 0, idx)
    p_start_alt = content.rfind('<w:p ', 0, idx)
    p_start = max(p_start, p_start_alt)
    if p_start < 0:
        print(f"⚠️ p_start not found for: '{search_text[:40]}...'")
        return content, False
    p_end = content.find('</w:p>', idx) + len('</w:p>')
    if p_end < 0:
        print(f"⚠️ p_end not found")
        return content, False
    return content[:p_start] + new_para_xml + content[p_end:], True


def replace_consecutive_paragraphs(content, anchor_text_first, anchor_text_last_in_block, new_paras_xml):
    """anchor_text_first 들어있는 paragraph부터 anchor_text_last_in_block 들어있는 paragraph까지 모두 new_paras_xml로 교체"""
    idx_first = content.find(anchor_text_first)
    idx_last = content.find(anchor_text_last_in_block)
    if idx_first < 0 or idx_last < 0:
        print(f"⚠️ NOT FOUND: '{anchor_text_first[:30]}' or '{anchor_text_last_in_block[:30]}'")
        return content, False
    p_start1 = content.rfind('<w:p>', 0, idx_first)
    p_start1_alt = content.rfind('<w:p ', 0, idx_first)
    p_start = max(p_start1, p_start1_alt)
    p_end = content.find('</w:p>', idx_last) + len('</w:p>')
    if p_start < 0 or p_end < 0:
        return content, False
    return content[:p_start] + new_paras_xml + content[p_end:], True


# ────────────────────────────────────────────────────────────
# 변형 A: 1.라 제안 내용 요약 도입 첫 단락 교체
# ────────────────────────────────────────────────────────────
A_OLD_ANCHOR = "본 제안서는 연세대학교가 추진하는 「연세 AX 역량 강화 교육 위탁 용역」"
A_NEW = (
    "본 제안서는 「연세 AX 역량 강화 교육 위탁 용역」에 대한 모두의연구소의 사업 수행 계획입니다. "
    "본 사업의 골격은 두 축이 만나는 자리에 있습니다. 한 축은 도구가 바뀌어도, 전공이 달라도 흔들리지 않는 "
    "AI 리터러시 — 프롬프트 엔지니어링에서 컨텍스트 엔지니어링을 거쳐 하네스 엔지니어링으로 이어지는 "
    "단계적 심화입니다. 다른 한 축은 디자인씽킹을 통해 학생 본인의 고유한 문제를 발견하고 창의적으로 "
    "풀어내는 경험입니다. 본 사업은 이 두 축이 한 학기 안에 학생에게 도달하도록 설계된 교육 로드맵으로, "
    "신촌캠퍼스 학술정보관(연세 AX 아카데미), 국제캠퍼스 언더우드기념도서관(연세 AX 스타트), "
    "신촌캠퍼스 박물관(연세 AX 뮤즈로그) 3개 기관에서 학부생 전체를 대상으로 1년간 90건 과정, 343회, "
    "549시간 규모의 교육을 운영합니다."
)
content, ok = replace_paragraph_containing(content, A_OLD_ANCHOR, normal_para(A_NEW))
print(f"변형 A (1.라 도입): {'✅' if ok else '❌'}")

# ────────────────────────────────────────────────────────────
# 변형 B: 2.가 RFP 3대 목표 응답 단락 교체
# ────────────────────────────────────────────────────────────
B_OLD_ANCHOR = "모두의연구소는 위 3대 목표에 응답하기 위해, 다음 네 가지 수행 목표를 설정하고"
B_NEW = (
    "모두의연구소는 위 3대 목표에 응답하기 위해, 두 축의 교차점을 본 사업의 골격으로 삼습니다. "
    "한 축은 도구가 바뀌어도 흔들리지 않는 AI 리터러시 — 프롬프트 · 컨텍스트 · 하네스 엔지니어링의 "
    "단계적 심화이며, 다른 한 축은 디자인씽킹을 통한 자기 문제 발견과 창의적 해결입니다. "
    "다음 네 가지 수행 목표는 두 축이 모든 학부생에게 도달하도록 만드는 실행 계획이며, "
    "가·나는 ①·②에, 다는 ②·③에, 라는 ②에 직접 대응합니다."
)
content, ok = replace_paragraph_containing(content, B_OLD_ANCHOR, normal_para(B_NEW))
print(f"변형 B (2.가 응답): {'✅' if ok else '❌'}")

# ────────────────────────────────────────────────────────────
# 변형 C: 운영 메서드 도입 두 문단 → 세 문단 교체
# ────────────────────────────────────────────────────────────
C_OLD_FIRST_ANCHOR = "앞서 제시한 세 가지 즐거움이 본 사업의 학습 경험에 대한 약속이라면"
C_OLD_LAST_ANCHOR = "Design Thinking은 본래 사용자 중심 문제 해결 방법론이지만"

C_NEW_PARAS = (
    normal_para(
        "본 사업의 90건은 두 가지 축으로 묶입니다. 첫 번째 축은 도구가 바뀌어도, 전공이 달라도 "
        "흔들리지 않는 AI 리터러시입니다. 학생은 프롬프트 엔지니어링(원하는 답을 끌어내는 법) → "
        "컨텍스트 엔지니어링(AI에게 적절한 정보·역할을 설계하는 법) → 하네스 엔지니어링(여러 AI를 "
        "묶어 자율 시스템을 만드는 법)으로 이어지는 단계적 심화 경로를 통과합니다. 도구가 ChatGPT에서 "
        "Gemini로 바뀌어도, 전공이 인문학에서 공학으로 바뀌어도 동일하게 통하는 역량입니다."
    ) +
    normal_para(
        "두 번째 축은 디자인씽킹을 통한 자기 발견입니다. 학생은 자기 전공·일상·관심사에서 출발해 "
        "자기만의 문제를 정의하고, 그 문제를 창의적으로 풀어내는 경험을 누적합니다. 도구 숙련만으로는 "
        "닿을 수 없는 자리, 즉 'AI로 무엇을 풀 것인가'에 대한 본인의 답을 만드는 자리입니다."
    ) +
    normal_para(
        "두 축이 만나는 자리가 「AI 시대의 Design Thinking 프로젝트」이며, 아래 5단계 운영 프레임은 "
        "그 만남이 90건 모든 과정에서 일관되게 일어나도록 받쳐주는 운영 메서드입니다. 본 사업의 90건 "
        "모든 과정은 — 대상이 신입생이든 고학년이든, 형식이 체험·세미나·워크숍·멘토링·공모전이든 — "
        "동일한 5단계 흐름 안에서 운영됩니다."
    )
)

# C_OLD_LAST_ANCHOR 텍스트가 들어있는 paragraph는 좀 길어서, 끝 부분 텍스트도 같이 식별
content, ok = replace_consecutive_paragraphs(
    content, C_OLD_FIRST_ANCHOR, C_OLD_LAST_ANCHOR, C_NEW_PARAS
)
print(f"변형 C (운영 메서드 도입): {'✅' if ok else '❌'}")

# ────────────────────────────────────────────────────────────
# 변형 D: 주제 영역별 도입 단락 교체
# ────────────────────────────────────────────────────────────
D_OLD_ANCHOR = "5대 주제 영역의 대표 워크숍과 학생 산출물을 정리합니다. 모든 워크숍은"
D_NEW = (
    "5대 주제 영역의 대표 워크숍과 학생 산출물을 정리합니다. 영역은 다르지만 모든 워크숍은 "
    "동일한 두 축 위에서 운영됩니다. 한 축은 프롬프트 → 컨텍스트 → 하네스 엔지니어링으로 이어지는 "
    "AI 리터러시의 단계적 심화이며, 다른 한 축은 디자인씽킹을 통한 자기 문제 발견과 창의적 해결입니다. "
    "따라서 학생이 어느 영역을 선택하든, 어느 캠퍼스에서 시작하든 두 축은 동일하게 작동하며, "
    "각 워크숍의 회별 모듈·도구·산출물이 학생 인증 포트폴리오에 누적됩니다."
)
content, ok = replace_paragraph_containing(content, D_OLD_ANCHOR, normal_para(D_NEW))
print(f"변형 D (주제 영역별 도입): {'✅' if ok else '❌'}")

with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

after = len(content)
print(f"\n파일 크기: {before} -> {after} (Δ {after - before})")
print("✅ 4개 변형 적용 완료")
