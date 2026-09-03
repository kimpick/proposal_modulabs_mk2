"""
Step 5: AI 시대의 Design Thinking 프로젝트 컨셉 도입
- 추진 전략(Trinity of Joy=철학) 다음에 운영 메서드로 배치
- 90건 전 과정을 단일 프레임으로 묶음
- 1.라 요약, 4계절 흐름 표에도 한 줄씩 반영
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PATH = '연세AX_제안서_모두의연구소_v2_260506(보완3).docx'
doc = Document(PATH)


def find_para_by_text(doc, contains_text, start_idx=0):
    for i, p in enumerate(doc.paragraphs):
        if i < start_idx:
            continue
        if contains_text in p.text:
            return i
    return -1


def insert_paragraph_after(reference_element, text, bold=False):
    new_p = OxmlElement('w:p')
    reference_element.addnext(new_p)
    r = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    if bold:
        rpr.append(OxmlElement('w:b'))
        rpr.append(OxmlElement('w:bCs'))
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


def insert_table_after(reference_element, data, bold_header=True):
    rows_n = len(data)
    cols_n = max(len(row) for row in data) if data else 0
    tbl = OxmlElement('w:tbl')
    tblPr = OxmlElement('w:tblPr')
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '5000')
    tblW.set(qn('w:type'), 'pct')
    tblPr.append(tblW)
    tblBorders = OxmlElement('w:tblBorders')
    for border_type in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        b = OxmlElement(f'w:{border_type}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:color'), '000000')
        tblBorders.append(b)
    tblPr.append(tblBorders)
    tbl.append(tblPr)
    tblGrid = OxmlElement('w:tblGrid')
    for _ in range(cols_n):
        tblGrid.append(OxmlElement('w:gridCol'))
    tbl.append(tblGrid)
    for r_idx, row_data in enumerate(data):
        tr = OxmlElement('w:tr')
        for c_idx in range(cols_n):
            tc = OxmlElement('w:tc')
            tc.append(OxmlElement('w:tcPr'))
            p = OxmlElement('w:p')
            p.append(OxmlElement('w:pPr'))
            r = OxmlElement('w:r')
            rPr = OxmlElement('w:rPr')
            if r_idx == 0 and bold_header:
                rPr.append(OxmlElement('w:b'))
                rPr.append(OxmlElement('w:bCs'))
            rfonts = OxmlElement('w:rFonts')
            rfonts.set(qn('w:eastAsia'), '맑은 고딕')
            rPr.append(rfonts)
            r.append(rPr)
            t = OxmlElement('w:t')
            t.text = row_data[c_idx] if c_idx < len(row_data) else ''
            t.set(qn('xml:space'), 'preserve')
            r.append(t)
            p.append(r)
            tc.append(p)
            tr.append(tc)
        tbl.append(tr)
    reference_element.addnext(tbl)
    return tbl


# ====================================================================
# 1. AI 시대의 Design Thinking 프로젝트 — 새 운영 메서드 섹션
#    위치: "교육 체계 설계 및 운영 방안" 헤딩 바로 위
# ====================================================================
idx = find_para_by_text(doc, "교육 체계 설계 및 운영 방안")
if idx >= 0:
    # 그 위 paragraph element 찾기
    target_para = doc.paragraphs[idx]
    prev_elem = target_para._element.getprevious()

    # prev_elem이 빈 단락이면 그 위로 더 거슬러 올라감
    while prev_elem is not None and prev_elem.tag.endswith('}p'):
        text_in_p = ''
        for tt in prev_elem.iter(qn('w:t')):
            text_in_p += tt.text or ''
        if text_in_p.strip():
            break
        # 빈 단락이면 그 위로
        upper = prev_elem.getprevious()
        if upper is None:
            break
        prev_elem = upper
        if prev_elem.tag.endswith('}p'):
            text_in_p2 = ''
            for tt in prev_elem.iter(qn('w:t')):
                text_in_p2 += tt.text or ''
            if text_in_p2.strip():
                break

    # 안전하게: "Wild Public Release" 줄 찾아서 그 다음에 삽입
    anchor_idx = -1
    for i, p in enumerate(doc.paragraphs):
        if 'Wild Public Release를 통한 SNS 배포' in p.text:
            anchor_idx = i
            break

    if anchor_idx >= 0:
        anchor = doc.paragraphs[anchor_idx]._element

        # 본문 (역순 삽입)
        intro_paras = [
            ("", False),
            ("운영 메서드: AI 시대의 Design Thinking 프로젝트", True),
            ("", False),
            ("앞서 제시한 세 가지 즐거움이 본 사업의 학습 경험에 대한 약속이라면, AI 시대의 Design Thinking 프로젝트는 그 약속을 실현하는 운영 메서드입니다. 본 사업의 90건 모든 과정은 — 대상이 신입생이든 고학년이든, 형식이 체험·세미나·워크숍·멘토링·공모전이든 — 동일한 5단계 흐름 안에서 운영됩니다.", False),
            ("", False),
            ("이 메서드를 채택한 이유는 간단합니다. 도구 중심 교육은 학생을 \"AI를 잘 다루는 사람\"으로 만들지만, 학생이 졸업할 때 필요한 것은 \"AI로 자기 문제를 푸는 사람\"입니다. 출발점이 도구가 아니라 문제여야 하는 이유입니다. Design Thinking은 본래 사용자 중심 문제 해결 방법론이지만, 본 사업에서는 학생 본인을 사용자로 두고 자기 도메인의 문제를 AI로 풀어내는 흐름으로 변형하여 운영합니다.", False),
            ("", False),
        ]
        for text, bold in reversed(intro_paras):
            insert_paragraph_after(anchor, text, bold=bold)

        # 5단계 프레임 표
        # 다시 anchor 위치 찾기 (위에서 본문 삽입했으므로)
        # 마지막 빈 paragraph 위치 찾아서 표 삽입
        last_intro_text = "출발점이 도구가 아니라 문제여야 하는 이유입니다"
        for p in doc.paragraphs:
            if last_intro_text in p.text:
                # 그 paragraph 다음의 빈 단락 element를 anchor로
                target_anchor = p._element
                nxt = target_anchor.getnext()
                while nxt is not None and nxt.tag.endswith('}p'):
                    nxt_text = ''
                    for tt in nxt.iter(qn('w:t')):
                        nxt_text += tt.text or ''
                    if nxt_text.strip():
                        break
                    target_anchor = nxt
                    nxt = nxt.getnext()
                break

        # 5단계 프레임 표
        framework_data = [
            ['단계', '학생의 행동', '운영 도구·산출물'],
            ['① 발견 (Empathize)',
             '자기 전공·관심 영역에서 AI로 풀 만한 문제를 찾는다. \"불편한가, 반복되는가, AI에게 시킬 만한가\"를 묻는다.',
             '체험 교육·세미나에서 영감을 얻고, 인터뷰·관찰·자가 회고로 문제를 좁힘'],
            ['② 정의 (Define)',
             '문제를 AI가 다룰 수 있는 형태로 다시 쓴다. 입력·출력·맥락을 명시한 한 줄 문제 진술서를 만든다.',
             'AX 트렌드 세미나·디자인씽킹 워크숍에서 문제 진술서 작성'],
            ['③ 발산 (Ideate)',
             '생성형 AI를 동료처럼 활용해 가능한 해결안을 빠르게 다양화한다. 처음 떠오른 답에서 멈추지 않는다.',
             'ChatGPT·Gemini로 아이디어 확장, NotebookLM으로 자료 정리'],
            ['④ 시제품 (Prototype)',
             '자연어로 동작하는 최소 기능 시제품을 만든다. 코딩 가능 여부와 무관하게 본인이 만든 것을 본다.',
             'Codex 기반 Vibe Coding, Canva·Capcut·Gamma로 콘텐츠 시제품'],
            ['⑤ 공개 (Release)',
             '시제품을 강의실 밖으로 내보낸다. 사용자 피드백을 받고, 다음 사이클을 시작한다.',
             '공모전·쇼케이스·SNS 공개(Wild Public Release), 인증 포트폴리오로 누적'],
        ]
        insert_table_after(target_anchor, framework_data)

        # 표 위에 짧은 안내
        insert_paragraph_after(target_anchor, "▶ 5단계 운영 프레임", bold=True)
        # 표 위 빈 줄
        # insert_paragraph_after(target_anchor, "", bold=False)

        print("✅ 5단계 프레임 표 삽입")

        # 표 다음 — 프로그램 유형 매핑 표 + 마무리 문단
        # 마무리 문단을 anchor로 잡아서 추가 삽입
        # 가장 마지막에 삽입한 표 element 찾기
        # 안전하게: 마지막 framework 데이터 텍스트로 위치 다시 찾기
        # framework table은 이제 doc.tables에 있음. 마지막 표가 framework 표.

        # 새 anchor: framework 표 다음에 매핑 표 추가
        # framework 표 element 찾기
        last_table = doc.tables[-1]
        framework_tbl_elem = last_table._element
        # 확인: header가 ['단계', '학생의 행동', ...]인가
        if last_table.rows[0].cells[0].text.strip().startswith('단계') and '학생' in last_table.rows[0].cells[1].text:
            # 매핑 표 데이터
            mapping_data = [
                ['프로그램 유형', '주요 단계', '본 사업에서의 역할'],
                ['체험 교육 (5건)', '①', '도서관 실감미디어 인프라에서 AI·기술과 처음 만나며 \"내가 만들고 싶은 것\"의 단서를 얻음'],
                ['세미나 (8건)', '①·②', 'IT·미디어 산업 전문가의 관점에서 자기 문제를 다시 봄. 인문학 세미나는 박물관 자원을 문제 영역으로 끌어옴'],
                ['워크숍 (41건)', '②·③·④', '문제 진술서 → 아이디어 발산 → 시제품까지 한 사이클을 압축적으로 경험'],
                ['멘토링 (9건)', '③·④·⑤', '시제품을 실제 작동하는 결과물로 키우는 단계. 멘토는 학생의 사이클이 막힌 지점을 풀어줌'],
                ['공모전·경진대회 (7건)', '⑤', '강의실 밖 사용자에게 공개하고 피드백을 받는 단계. 인증 포트폴리오에 결과물을 누적'],
                ['교육 콘텐츠 개발 (20건)', '전 단계', '5단계 흐름이 모든 과정에서 일관되게 운영되도록 받쳐주는 학습 자료·실감형 콘텐츠'],
            ]

            # 표 위 헤더용 빈 단락 + 헤더 추가
            insert_paragraph_after(framework_tbl_elem, "", bold=False)
            insert_table_after(framework_tbl_elem, mapping_data)
            insert_paragraph_after(framework_tbl_elem, "▶ 프로그램 유형별 단계 매핑", bold=True)
            insert_paragraph_after(framework_tbl_elem, "", bold=False)

            print("✅ 프로그램 유형 매핑 표 삽입")

            # 마무리 문단 (매핑 표 다음)
            mapping_tbl_elem = doc.tables[-1]._element  # 방금 추가한 표
            closing_paras = [
                ("", False),
                ("이 메서드의 효과는 다음과 같이 정리됩니다.", False),
                ("", False),
                ("· 학생 입장: 어떤 과정에 들어가도 자기 결과물이 누적된다. 워크숍 한 번으로 끝나지 않고, 같은 흐름이 다음 학기·다음 캠퍼스에서도 이어진다.", False),
                ("· 발주처 입장: 90건 과정의 학습 성과를 동일한 기준(문제 진술 → 시제품 → 공개)으로 비교하고 관리할 수 있다. 캠퍼스·학기·강사가 달라도 운영의 일관성이 유지된다.", False),
                ("· 모두의연구소 입장: 사업 종료 후에도 학생 결과물이 모두의연구소 학습 커뮤니티(풀잎스쿨·AIFFEL)와 자연스럽게 연결되며, 우수 사례는 다음 해 본 사업의 교육 콘텐츠로 환류된다.", False),
                ("", False),
                ("AI 시대의 Design Thinking 프로젝트는 본 사업이 90건의 개별 과정으로 흩어지지 않도록 하는 운영 원리이자, 학생이 \"나는 AI로 어떤 문제를 풀었는가\"를 자기 언어로 답할 수 있도록 만드는 학습 설계입니다.", False),
                ("", False),
            ]
            for text, bold in reversed(closing_paras):
                insert_paragraph_after(mapping_tbl_elem, text, bold=bold)
            print("✅ 마무리 문단 삽입")

# ====================================================================
# 2. 1.라 제안 내용 요약에 한 줄 추가
#    위치: "핵심 운영 방향은 다음과 같습니다." 다음 4개 불릿 뒤에 추가
# ====================================================================
target_text = "이공계 중심 AI 교육의 한계를 보완"
idx = find_para_by_text(doc, target_text)
if idx >= 0:
    anchor = doc.paragraphs[idx]._element
    extra_line = "· 위 운영 방향을 관통하는 단일 메서드로 \"AI 시대의 Design Thinking 프로젝트\"를 도입합니다. 90건 전 과정이 발견-정의-발산-시제품-공개의 동일한 흐름 위에서 운영되어, 캠퍼스·학기·과정이 달라도 학생의 결과물이 연속적으로 누적됩니다."
    insert_paragraph_after(anchor, extra_line, bold=False)
    print("✅ 1.라 메서드 한 줄 추가")

# ====================================================================
# 3. 핵심 운영 방향 도입 문장 살짝 보강
# ====================================================================
# (생략 — 이미 충분)

# ====================================================================
# Save
# ====================================================================
try:
    doc.save(PATH)
    print(f"\n✅ Saved: {PATH}")
except PermissionError:
    alt = '연세AX_제안서_모두의연구소_v2_260506(보완5).docx'
    doc.save(alt)
    print(f"\n⚠️ 잠금되어 사본 저장: {alt}")
