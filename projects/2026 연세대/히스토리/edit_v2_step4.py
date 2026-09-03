"""
Step 4: 1.라 제안 내용 요약 + 4.가 추가 제안 작성
- 자연스러운 비즈니스 문서 톤 (AI 광고체 회피)
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

PATH_LOCKED = '연세AX_제안서_모두의연구소_v2_260506.docx'
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
        b = OxmlElement('w:b')
        rpr.append(b)
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
# 1.라 제안 내용 요약
# ====================================================================
idx = find_para_by_text(doc, "라. 제안 내용 요약")
if idx >= 0:
    anchor = doc.paragraphs[idx]._element

    # 본문 (역순 삽입)
    paragraphs = [
        ("", False),
        ("본 제안서는 연세대학교가 추진하는 「연세 AX 역량 강화 교육 위탁 용역」에 대한 모두의연구소의 사업 수행 계획입니다. 신촌캠퍼스 학술정보관(연세 AX 아카데미), 국제캠퍼스 언더우드기념도서관(연세 AX 스타트), 신촌캠퍼스 박물관(연세 AX 뮤즈로그) 3개 기관에서 학부생 전체를 대상으로 1년간 90건 과정, 343회, 549시간 규모의 교육을 운영합니다.", False),
        ("", False),
        ("교육 설계의 출발점은 다음 세 가지 문제 인식입니다. 첫째, 도구 숙련에 치우친 교육은 도구가 바뀌는 순간 학습이 무의미해집니다. 둘째, 단발성 강의는 학생이 자기 결과물을 완성하기까지의 흐름을 끊어놓습니다. 셋째, 수료 후 결과물이 강의실 밖으로 나가지 못하면 학습은 학생의 자산으로 남지 않습니다. 본 제안서의 모든 운영 계획은 이 세 가지 한계를 해소하기 위한 설계로 구성됩니다.", False),
        ("", False),
        ("핵심 운영 방향은 다음과 같습니다.", False),
        ("", False),
        ("· 기관별 독립 운영을 원칙으로 하되, 국제캠퍼스 신입생(연세 AX 스타트)에서 신촌캠퍼스 심화 과정(연세 AX 아카데미)으로 자연 연계되는 단계별 학습 경로를 설계합니다.", False),
        ("· 봄학기 문제 발견(디자인씽킹), 여름방학 기술 심화(AX 캠프), 가을학기 프로젝트 수행, 겨울방학 MVP 완성과 쇼케이스로 이어지는 4계절 전주기 교육을 운영합니다.", False),
        ("· 총장 명의 AX 역량 인증서 발급을 위해 기초(AX Starter) – 활용(AX Practitioner) – 심화(AX Creator) 3단계 인증 체계를 구축합니다. 단순 출결이 아닌 결과물 기반 인증으로 운영합니다.", False),
        ("· 인문학 자원과 박물관 콘텐츠를 AI와 결합한 융합 교육(연세 AX 뮤즈로그)을 별도로 설계하여 이공계 중심 AI 교육의 한계를 보완합니다.", False),
        ("", False),
        ("모두의연구소가 본 사업에 적합한 이유는 세 가지입니다. ① 단일 건 30억 원 이상 규모의 AI 교육 운영 경험을 다수 보유하고 있습니다(KT DS, 네이버커넥트재단, 한국장애인고용공단 등). ② 풀잎스쿨·AIFFEL 등 자체 학습 커뮤니티를 10년간 운영하며 5,000명 이상의 강사·멘토 풀을 축적했습니다. ③ 기획 인력 모두 관련 분야 10년 이상 경력을 보유하고 있으며, 사업 기간 중 실제 참여를 보장합니다.", False),
        ("", False),
        ("본 사업의 산출물은 90건의 교육 운영 자체에 그치지 않습니다. 학부생이 실제로 만든 결과물, 그 결과물이 사회와 만나는 경험, 그리고 본인의 학업과 진로에 연결되는 AX 역량의 누적 — 이 세 가지가 본 사업의 실질적인 성과입니다.", False),
        ("", False),
    ]

    for text, bold in reversed(paragraphs):
        insert_paragraph_after(anchor, text, bold=bold)

    # 한 줄 요약 표
    summary_table_data = [
        ['구분', '내용'],
        ['사업명', '연세 AX 역량 강화 교육 위탁 용역'],
        ['교육 대상', '연세대학교 학부생 (신촌·국제캠퍼스)'],
        ['운영 기관', '신촌 학술정보관 / 국제캠퍼스 도서관 / 신촌 박물관'],
        ['운영 규모', '90건 과정, 343회, 549시간'],
        ['운영 기간', '계약일 ~ 2027년 2월 28일'],
        ['핵심 차별점', '4계절 전주기 교육 + 단계별 인증제 + 자체 커뮤니티 연계'],
        ['수행사', '모두의연구소 (MODULABS)'],
    ]
    # 본문 끝에 표 삽입 — anchor에서 본문 paragraphs 다음 위치
    # 본문 마지막 paragraph element를 찾아서 그 뒤에 삽입
    # 위에서 anchor 바로 뒤에 paragraphs를 reverse로 삽입했으니, anchor의 next는 첫 paragraph
    # 표는 마지막에 넣어야 하므로, 마지막 paragraph element를 찾아야 함
    last_inserted = anchor.getnext()
    while last_inserted is not None and last_inserted.tag.endswith('}p'):
        nxt = last_inserted.getnext()
        if nxt is None or not nxt.tag.endswith('}p'):
            break
        # 다음 단락의 텍스트가 우리 본문의 일부인지 확인
        if not any(text in (last_inserted.findtext('.//' + qn('w:t'), default='') or '') for text, _ in paragraphs):
            break
        last_inserted = nxt

    # 더 안전하게: 본문 마지막 줄(텍스트 매칭)을 찾기
    target_text = "이 세 가지가 본 사업의 실질적인 성과입니다"
    target_elem = None
    for p in doc.paragraphs:
        if target_text in p.text:
            target_elem = p._element
    if target_elem is not None:
        # 그 뒤의 빈 단락까지 건너뛰기
        nxt = target_elem.getnext()
        while nxt is not None and nxt.tag.endswith('}p'):
            t_text = ''
            for tt in nxt.iter(qn('w:t')):
                t_text += tt.text or ''
            if t_text.strip() == '':
                target_elem = nxt
                nxt = nxt.getnext()
            else:
                break
        # 한 줄 요약 표 삽입
        insert_table_after(target_elem, summary_table_data)
        # 표 위에 헤더
        insert_paragraph_after(target_elem, "▶ 한 줄 요약", bold=True)
        # 표 다음 빈 줄
        # 이미 충분히 빈줄 있음

    print("✅ 1.라 제안 내용 요약 작성 완료")


# ====================================================================
# 4.가 추가 제안 내용
# ====================================================================
# 위치: "※ 평가 항목 「추가 제안 내용의 적정성」..." 안내 줄 뒤
idx = find_para_by_text(doc, "추가 제안 내용의 적정성")
if idx >= 0:
    anchor = doc.paragraphs[idx]._element

    paragraphs_4ga = [
        ("", False),
        ("연세대학교가 본 사업을 통해 만들고자 하는 것은 단발성 교육 운영 결과가 아니라, 학부생이 졸업 이후에도 AI 시대를 자기 언어로 살아갈 수 있는 역량입니다. 모두의연구소는 본 사업의 90건 과정 운영에 더해, 다음 두 가지 차별화 제안을 함께 드립니다. 두 제안 모두 별도 비용 부담 없이 본 사업 예산 내에서 수행 가능합니다.", False),
        ("", False),
        ("제안 1. AX 역량 인증제 고도화 — \"인증서가 끝이 아닌 시작이 되도록\"", True),
        ("", False),
        ("기존의 수료증·인증서는 발급 시점에서 효력이 끝납니다. 본 사업의 AX 역량 인증서는 발급 이후에도 학생의 학습 이력을 누적·연결하는 도구로 운영합니다. 구체적으로는 다음 세 가지 요소를 포함합니다.", False),
        ("", False),
        ("· 학습 이력 누적: 학생이 어떤 단계의 어떤 과정을 이수했는지, 어떤 결과물을 만들었는지를 단일 프로필에 정리하여 본인이 언제든 확인하고 외부에 공개할 수 있도록 합니다.", False),
        ("· 자가진단 도구: 학기 초 사전진단과 학기 말 사후진단을 통해 학생 본인의 AX 역량 변화를 수치로 확인하도록 합니다. 진단 문항은 기존 모두의연구소 AI 리터러시 진단(KCH 사업 운영) 결과를 기반으로 본 사업에 맞게 조정합니다.", False),
        ("· 결과물 포트폴리오: AX Creator 단계에서 제출한 MVP·공모전 출품작·쇼케이스 발표 자료를 인증 프로필에 연결하여, 졸업 후 취업·대학원 진학·창업 시 활용 가능한 형태로 보존합니다.", False),
        ("", False),
        ("제안 2. 모두의연구소 학습 커뮤니티 연계 — \"수료가 단절이 되지 않도록\"", True),
        ("", False),
        ("AX Creator 인증을 받은 학부생은 모두의연구소가 운영하는 외부 학습 네트워크에 우선 접근할 수 있습니다. 이는 본 사업이 끝난 뒤에도 학생이 동료·멘토와 연결되어 학습을 지속할 수 있는 통로입니다.", False),
        ("", False),
        ("· 풀잎스쿨 연계: 모두의연구소가 2017년부터 운영해 온 거꾸로 학습 기반 풀잎스쿨에 우선 참여할 수 있도록 안내합니다. 분야별 모임에서 동료 학습자와 직접 연결되며, 이 중 일부는 향후 본 사업의 멘토 풀로 환류할 수 있습니다.", False),
        ("· AIFFEL 동문 네트워크: 2020년부터 운영되어 온 AI 혁신학교 AIFFEL 수료생 네트워크와의 연결점을 만들어, 학부생이 산업 현장의 AI 실무자로부터 비공식 멘토링을 받을 수 있도록 합니다.", False),
        ("· 사후 학습 기회: 본 사업 종료 이후에도 모두의연구소가 운영하는 무료 세미나·해커톤 정보를 인증 보유자에게 우선 안내합니다.", False),
        ("", False),
        ("두 제안의 의미는 명확합니다. 본 사업이 종료된 뒤에도 학생의 AX 역량은 누적되고 연결됩니다. 인증서가 학생의 손을 떠나는 순간 효력이 사라지는 일반적인 인증제와, 인증서가 학생의 다음 단계와 연결되는 본 제안의 차이는 결국 학생이 졸업할 때 본인의 AX 역량을 어떻게 설명할 수 있는가의 차이로 나타납니다.", False),
        ("", False),
    ]

    for text, bold in reversed(paragraphs_4ga):
        insert_paragraph_after(anchor, text, bold=bold)

    print("✅ 4.가 추가 제안 내용 작성 완료")


# ====================================================================
# 4.나 기타 사항 (간단히)
# ====================================================================
idx = find_para_by_text(doc, "나. 기타 사항")
if idx >= 0:
    # 다음 빈 단락 찾기
    anchor = doc.paragraphs[idx]._element

    paragraphs_4na = [
        ("", False),
        ("본 사업은 연세대학교의 학부 교육 정책 및 학사 일정과 긴밀히 연계되어 운영되어야 합니다. 모두의연구소는 다음 사항을 본 사업 수행 시 우선 고려하겠습니다.", False),
        ("", False),
        ("· 발주처 협의 우선: 운영 방식, 교육과정 구성, 강사 섭외, 홍보 채널 등 주요 의사결정 항목은 발주처와의 사전 협의를 우선합니다. 특히 발주처가 선정한 강사가 있는 경우 우선 배정합니다.", False),
        ("· 학사 일정 정합성: 국제캠퍼스 신입생 대상 교육은 학기 중 평일 야간(17:00~21:00) 우선 편성, 신촌캠퍼스 심화 교육은 방학 기간 집중 개설 원칙을 준수합니다.", False),
        ("· 현장 상주 인력 운영: 교육 개설 준비 및 운영 기간 중 발주처가 요청하는 장소에 전문 인력을 상주시켜, 의사소통 지연이 발생하지 않도록 합니다.", False),
        ("· 운영비 직접 집행 협조: 교육 환경 및 교육생 관리 등 현장에서 수시로 발생하는 운영비는 발주처가 직접 집행 가능한 구조로 운영합니다.", False),
        ("· 콘텐츠 권리 귀속: 본 사업으로 제작되는 모든 교육 콘텐츠의 소유권 및 저작권은 연세대학교에 귀속되며, 분쟁 발생 시 모두의연구소가 일체 비용을 부담합니다.", False),
    ]

    for text, bold in reversed(paragraphs_4na):
        insert_paragraph_after(anchor, text, bold=bold)
    print("✅ 4.나 기타 사항 작성 완료")


# ====================================================================
# Save
# ====================================================================
try:
    doc.save(PATH)
    print(f"\n✅ Saved: {PATH}")
except PermissionError:
    alt = '연세AX_제안서_모두의연구소_v2_260506(보완4).docx'
    doc.save(alt)
    print(f"\n⚠️ 잠금되어 사본 저장: {alt}")
