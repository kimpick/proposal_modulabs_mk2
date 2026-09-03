"""
v2(보완3)의 새로 추가된 paragraph들을 v1 원본 표준 서식으로 일괄 변환
- 빈 paragraph: 본문 표준 pPr만
- 일반 본문: Noto Sans KR + #222222
- ▶ heading: 2개 run으로 분리 (▶=#F7585C, 텍스트=#1A1A2E)
- 일반 bold heading: 큰 강조 박스 (#002B5C + bg #E6EEF5)
"""
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v2/word/document.xml'

with open(DOC_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

before_size = len(content)

# ─── 표준 서식 블록 ────────────────────────────────────────────
NORMAL_PPR = (
    '<w:pPr>'
    '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
    '<w:spacing w:before="200" w:after="180"/>'
    '<w:jc w:val="both"/>'
    '<w:rPr>'
    '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
    '<w:color w:val="222222"/>'
    '</w:rPr>'
    '</w:pPr>'
)
NORMAL_RPR = (
    '<w:rPr>'
    '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
    '<w:color w:val="222222"/>'
    '</w:rPr>'
)

EMPHASIS_PPR = (
    '<w:pPr>'
    '<w:shd w:val="clear" w:color="auto" w:fill="E6EEF5"/>'
    '<w:spacing w:before="240" w:after="120"/>'
    '<w:jc w:val="both"/>'
    '<w:rPr>'
    '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
    '<w:b/><w:bCs/>'
    '<w:color w:val="002B5C"/>'
    '<w:sz w:val="22"/><w:szCs w:val="22"/>'
    '<w:shd w:val="clear" w:color="auto" w:fill="E6EEF5"/>'
    '</w:rPr>'
    '</w:pPr>'
)
EMPHASIS_RPR = (
    '<w:rPr>'
    '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
    '<w:b/><w:bCs/>'
    '<w:color w:val="002B5C"/>'
    '<w:sz w:val="22"/><w:szCs w:val="22"/>'
    '<w:shd w:val="clear" w:color="auto" w:fill="E6EEF5"/>'
    '</w:rPr>'
)

ARROW_PPR = (
    '<w:pPr>'
    '<w:spacing w:before="160" w:after="60"/>'
    '</w:pPr>'
)

# ─── 패턴 정의 (우리가 python-docx로 추가한 단순 형태) ────────
# 1. 빈 paragraph
empty_pattern = re.compile(
    r'<w:p>\s*<w:r>\s*<w:rPr>\s*<w:rFonts w:eastAsia="맑은 고딕"/>\s*</w:rPr>\s*<w:t xml:space="preserve"/>\s*</w:r>\s*</w:p>',
    re.DOTALL
)

# 2. 일반 본문 paragraph (b/bCs 없음)
normal_pattern = re.compile(
    r'<w:p>\s*<w:r>\s*<w:rPr>\s*<w:rFonts w:eastAsia="맑은 고딕"/>\s*</w:rPr>\s*<w:t xml:space="preserve">(.*?)</w:t>\s*</w:r>\s*</w:p>',
    re.DOTALL
)

# 3. Bold paragraph
bold_pattern = re.compile(
    r'<w:p>\s*<w:r>\s*<w:rPr>\s*<w:b/>\s*<w:bCs/>\s*<w:rFonts w:eastAsia="맑은 고딕"/>\s*</w:rPr>\s*<w:t xml:space="preserve">(.*?)</w:t>\s*</w:r>\s*</w:p>',
    re.DOTALL
)


def replace_normal(m):
    text = m.group(1)
    return f'<w:p>{NORMAL_PPR}<w:r>{NORMAL_RPR}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def replace_bold(m):
    text = m.group(1)
    stripped = text.strip()
    if stripped.startswith('▶'):
        # ▶ heading: 2개 run으로 분리
        idx = text.find('▶')
        prefix = text[:idx + 1]   # ▶ 부분 (앞에 공백 있을 수도)
        rest = text[idx + 1:]
        # ▶ 다음 공백 prefix에 포함
        if rest.startswith(' '):
            prefix += ' '
            rest = rest[1:]
        arrow_run = (
            '<w:r>'
            '<w:rPr><w:b/><w:bCs/><w:color w:val="F7585C"/></w:rPr>'
            f'<w:t xml:space="preserve">{prefix}</w:t>'
            '</w:r>'
        )
        text_run = (
            '<w:r>'
            '<w:rPr><w:b/><w:bCs/><w:color w:val="1A1A2E"/></w:rPr>'
            f'<w:t xml:space="preserve">{rest}</w:t>'
            '</w:r>'
        )
        return f'<w:p>{ARROW_PPR}{arrow_run}{text_run}</w:p>'
    elif stripped.startswith('①') or stripped.startswith('②') or stripped.startswith('③'):
        # ① ② ③ 헤더 (RFP 3대 목표): emphasis 서식
        return f'<w:p>{EMPHASIS_PPR}<w:r>{EMPHASIS_RPR}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'
    else:
        # 일반 bold heading: 강조 박스 (Joy of Depth와 동일)
        return f'<w:p>{EMPHASIS_PPR}<w:r>{EMPHASIS_RPR}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


# 적용 순서: bold(특수) → empty → normal
n_bold = len(bold_pattern.findall(content))
content = bold_pattern.sub(replace_bold, content)

n_empty = len(empty_pattern.findall(content))
EMPTY_REPLACEMENT = f'<w:p>{NORMAL_PPR}</w:p>'
content = empty_pattern.sub(EMPTY_REPLACEMENT, content)

n_normal = len(normal_pattern.findall(content))
content = normal_pattern.sub(replace_normal, content)

print(f"변환: bold={n_bold}, empty={n_empty}, normal={n_normal}")

with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

after_size = len(content)
print(f"파일 크기: {before_size} -> {after_size} bytes")
print(f"✅ 서식 변환 완료: {DOC_PATH}")
