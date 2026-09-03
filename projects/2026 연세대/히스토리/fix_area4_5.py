"""
영역 4의 252회 단락 정리 + 영역 5에 실감미디어 본문 추가 + 영역 5 헤더 라벨 정정
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v13/word/document.xml'
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


# ============================================================
# 1. 영역 4 잔존 단락 → 1줄 안내로 교체 (paragraph 본문 텍스트만 교체)
# ============================================================
old_p = "실감미디어 체험 교육(252회 운영)은 발주처 학술정보원의 VR/AR/MR 인프라를 활용하며, 모두의연구소는 콘텐츠 시나리오 설계·AI 연계 학습지·진행 가이드를 지원합니다. 회당 1시간 흐름은 체험 주제 브리프 10분 → 실감미디어 체험 35분 → ChatGPT/Gemini로 체험 후기 구조화·SNS 카드 1장 즉석 제작 15분으로 구성됩니다. Physical AI 접점으로 VR 캠퍼스 투어 중 시선·동선 데이터를 AI가 요약해 학생 행동 페르소나 카드를 산출하는 사례를 시범 운영합니다."
new_p = "박물관에서 운영되는 실감미디어 체험은 박물관 영역과 통합 운영하며, 자세한 내용은 영역 5(박물관 실감형·인문학 융합)에서 다룹니다."

n1 = content.count(old_p)
content = content.replace(old_p, new_p)
print(f"✅ 영역 4 단락 → 1줄 안내로 교체 ({n1}곳)")


# ============================================================
# 2. 영역 5 헤더 라벨 정정 (split run 형태이므로 텍스트 부분만)
# ============================================================
# 현재: "영역 5. 인문학 × AI 융합 (박물관, 약 5회 + 콘텐츠 5종)"
# 목표: "영역 5. 박물관 실감형·인문학 융합 (5회 + 콘텐츠 5종)"
content = content.replace(
    "영역 5. 인문학 × AI 융합 (박물관, 약 5회 + 콘텐츠 5종)",
    "영역 5. 박물관 실감형·인문학 융합 (5회 + 콘텐츠 5종)"
)
print("✅ 영역 5 헤더 라벨 정정")


# ============================================================
# 3. 영역 5 본문 개요 단락 다음에 실감미디어 신규 단락 삽입
# ============================================================
overview_anchor = "박물관은 본래 시간을 견딘 것들이 모이는 장소이며, AI는 그 시간을 새로운 언어로 다시 읽게 합니다."
idx = content.find(overview_anchor)
if idx >= 0:
    # 그 paragraph 끝
    p_end = content.find('</w:p>', idx) + len('</w:p>')

    new_para_text = (
        "실감형 콘텐츠는 박물관(연세 AX 뮤즈로그)에서 운영되며, 학술정보원의 VR/AR/MR 인프라를 활용합니다. "
        "모두의연구소는 본 사업에서 박물관 자원과 어울리는 실감형 콘텐츠 5종을 기획·제작하며, "
        "콘텐츠 시나리오 설계·AI 연계 학습지·진행 가이드를 함께 지원합니다. "
        "콘텐츠 회당 1시간 흐름은 체험 주제 브리프 10분 → 실감미디어 체험 35분 → ChatGPT·Gemini로 "
        "체험 후기 구조화·SNS 카드 1장 즉석 제작 15분으로 구성됩니다. Physical AI 접점으로 VR 캠퍼스 "
        "투어 중 시선·동선 데이터를 AI가 요약해 학생 행동 페르소나 카드를 산출하는 사례를 시범 운영합니다."
    )
    new_block = normal_para(new_para_text)
    content = content[:p_end] + new_block + content[p_end:]
    print("✅ 영역 5 본문에 실감미디어 신규 단락 추가")
else:
    print("❌ 영역 5 개요 anchor 못 찾음")


with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
after = len(content)
print(f"\n파일 크기: {before} -> {after} (Δ {after - before})")
