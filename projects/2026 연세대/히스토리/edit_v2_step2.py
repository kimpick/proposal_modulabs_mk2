"""
Step 2: 제안 요청 라인 다음에 모두의연구소의 제안 응답 추가
- "제안 요청:" 두 줄은 RFP 인용으로 유지
- 각 라인 뒤에 직접적인 제안 응답 추가
- 기존에 추가했던 중복 intro 단락은 제거
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PATH = '연세AX_제안서_모두의연구소_v2_260506.docx'
doc = Document(PATH)


def find_para_by_text(doc, contains_text, start_idx=0):
    for i, p in enumerate(doc.paragraphs):
        if i < start_idx:
            continue
        if contains_text in p.text:
            return i
    return -1


def delete_paragraph(para):
    elem = para._element
    elem.getparent().remove(elem)


def insert_paragraph_after(reference_element, text, bold=False):
    new_p = OxmlElement('w:p')
    reference_element.addnext(new_p)
    r = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    if bold:
        b = OxmlElement('w:b')
        rpr.append(b)
        b2 = OxmlElement('w:bCs')
        rpr.append(b2)
    rfonts = OxmlElement('w:rFonts')
    rfonts.set(qn('w:eastAsia'), '맑은 고딕')
    rpr.append(rfonts)
    r.append(rpr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    r.append(t)
    new_p.append(r)
    return new_p


# ====================================================================
# 1. 중복 intro 단락 제거
# ====================================================================
# "총장 명의의 AX 역량 인증서 발급을 위해, 학부 재학 중 이수 가능한 기초–활용–심화 3단계 교육 로드맵을 구성합니다."
idx = find_para_by_text(doc, "총장 명의의 AX 역량 인증서 발급을 위해, 학부 재학 중")
if idx >= 0:
    delete_paragraph(doc.paragraphs[idx])
    print(f"DELETED 중복 intro 단락 [{idx}]")

# ====================================================================
# 2. 첫 번째 "제안 요청" 뒤에 응답 추가
# ====================================================================
idx1 = find_para_by_text(doc, "제안 요청: 학부 재학 중 이수 가능한")
if idx1 >= 0:
    anchor1 = doc.paragraphs[idx1]._element

    # "제안" 헤더는 이미 RFP 요청 표시이므로, 응답을 같은 단락 뒤에 붙임
    # 단락 1개 띄우고 응답 1줄 추가 (안전하게 reverse-order로 삽입)
    response1_text = (
        "→ 모두의연구소는 AX Starter(국제캠퍼스 신입생) → AX Practitioner(신촌캠퍼스 활용 단계) → "
        "AX Creator(공모전·쇼케이스 심화 단계)의 3단계 교육 과정을 설계합니다. "
        "각 단계별 이수 요건을 명확히 정의하여 학부 재학 중 자연스럽게 단계별 AX 역량을 쌓을 수 있는 "
        "성장 경로를 제공합니다."
    )
    # reverse 순서로 삽입 (anchor 바로 다음에 들어가야 하므로 빈줄 먼저 추가)
    insert_paragraph_after(anchor1, response1_text, bold=False)
    print(f"INSERTED 응답1 after [{idx1}]")

# ====================================================================
# 3. 두 번째 "제안 요청" 뒤에 응답 추가
# ====================================================================
idx2 = find_para_by_text(doc, "제안 요청: 총장 명의의 AX 역량 인증서")
if idx2 >= 0:
    anchor2 = doc.paragraphs[idx2]._element
    response2_text = (
        "→ 모두의연구소는 단계별 이수 현황을 체계적으로 관리하고, 최종 단계(AX Creator)에서 "
        "공모전 출품·최종 쇼케이스 발표·AX 포트폴리오 제출 요건을 충족한 학생에게 "
        "총장 명의의 AX 역량 인증서를 발급하는 프로세스를 운영합니다. "
        "사회적 수요를 반영한 AX 역량 도출 및 인증 기준 고도화는 발주처와의 협의를 통해 "
        "지속적으로 발전시킵니다."
    )
    insert_paragraph_after(anchor2, response2_text, bold=False)
    print(f"INSERTED 응답2 after [{idx2}]")

# ====================================================================
# 4. AX 역량 로드맵 섹션의 단계별 표 위에 안내 문구 추가 (있으면 자연스럽게)
# ====================================================================
# "▶ 단계 1. 기초 — AX Starter" 바로 위에 짧은 안내 문구 추가
idx_stage1 = find_para_by_text(doc, "▶ 단계 1. 기초 — AX Starter")
if idx_stage1 >= 0:
    # 위쪽에 안내 문구 삽입
    para_above = doc.paragraphs[idx_stage1 - 1]._element if idx_stage1 > 0 else None
    if para_above is not None:
        insert_paragraph_after(
            para_above,
            "▶ AX 역량 인증 3단계 로드맵",
            bold=True
        )
        print(f"INSERTED 로드맵 헤더 above [{idx_stage1}]")

doc.save(PATH)
print(f"\n✅ Saved: {PATH}")
