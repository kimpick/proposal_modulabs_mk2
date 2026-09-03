"""
v3에 5대 주제 영역별 상세 커리큘럼 섹션을 삽입
- 위치: '5대 주제 영역' 표 다음
- 형식: 영역별 (헤더 + 개요 본문 + 워크숍 표)
- 서식: v1 표준 (Noto Sans KR + #222222, ▶ 헤더 split, 표는 af1 스타일)
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOC_PATH = 'unpacked_v3/word/document.xml'

with open(DOC_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# ─── 표준 빌딩 블록 ────────────────────────────────────────────
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
        '<w:pPr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
        '<w:spacing w:before="200" w:after="180"/>'
        '<w:jc w:val="both"/>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
        '<w:color w:val="222222"/>'
        '</w:rPr>'
        '</w:pPr>'
        '</w:p>'
    )

def emphasis_heading(text):
    return (
        '<w:p>'
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

def arrow_heading(text):
    """▶ 헤더 — split run"""
    return (
        '<w:p>'
        '<w:pPr>'
        '<w:spacing w:before="160" w:after="60"/>'
        '</w:pPr>'
        '<w:r>'
        '<w:rPr><w:b/><w:bCs/><w:color w:val="F7585C"/></w:rPr>'
        '<w:t xml:space="preserve">▶ </w:t>'
        '</w:r>'
        '<w:r>'
        '<w:rPr><w:b/><w:bCs/><w:color w:val="1A1A2E"/></w:rPr>'
        f'<w:t xml:space="preserve">{text}</w:t>'
        '</w:r>'
        '</w:p>'
    )

def make_table(rows, col_widths):
    """v1 표준 표 스타일 (af1)"""
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
                f'<w:tcMar>'
                f'<w:top w:w="120" w:type="dxa"/>'
                f'<w:left w:w="160" w:type="dxa"/>'
                f'<w:bottom w:w="120" w:type="dxa"/>'
                f'<w:right w:w="160" w:type="dxa"/>'
                f'</w:tcMar>'
                f'</w:tcPr>'
                f'<w:p>'
                f'<w:pPr>'
                f'<w:spacing w:before="0" w:after="0"/>'
                f'<w:rPr>'
                f'<w:rFonts w:ascii="Noto Sans KR" w:eastAsia="Noto Sans KR" w:hAnsi="Noto Sans KR" w:cs="Noto Sans KR"/>'
                f'{bold_xml}'
                f'<w:color w:val="222222"/>'
                f'<w:sz w:val="20"/><w:szCs w:val="20"/>'
                f'</w:rPr>'
                f'</w:pPr>'
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
        rows_xml += f'<w:tr><w:trPr><w:trHeight w:val="400"/></w:trPr>{cells}</w:tr>'

    return (
        f'<w:tbl>'
        f'<w:tblPr>'
        f'<w:tblStyle w:val="af1"/>'
        f'<w:tblW w:w="{total}" w:type="dxa"/>'
        f'<w:tblInd w:w="-2" w:type="dxa"/>'
        f'<w:tblBorders>'
        f'<w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/>'
        f'<w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
        f'</w:tblBorders>'
        f'<w:tblLayout w:type="fixed"/>'
        f'</w:tblPr>'
        f'<w:tblGrid>{grid}</w:tblGrid>'
        f'{rows_xml}'
        f'</w:tbl>'
    )


# ─── 5대 영역별 컨텐츠 정의 ────────────────────────────────────
sections = []

# 영역 헤더
sections.append(emphasis_heading('주제 영역별 상세 커리큘럼'))
sections.append(normal_para('5대 주제 영역의 대표 워크숍과 학생 산출물을 정리합니다. 모든 워크숍은 「AI 시대의 Design Thinking 프로젝트」 5단계 메서드 위에서 운영되며, 각 워크숍의 회별 모듈·도구·산출물이 학생 인증 포트폴리오에 누적됩니다.'))
sections.append(empty_para())

# ─── 1. 생성형 AI ───
sections.append(arrow_heading('영역 1. 생성형 AI (약 29건)'))
sections.append(normal_para('본 사업 90건 중 약 32%가 생성형 AI 영역입니다. 학부생이 졸업 시 ChatGPT·Gemini·Perplexity·NotebookLM을 활용해 자기 전공의 문제를 정의하고, 자연어로 시제품을 만들어 공개하는 일련의 흐름을 자기 주도로 수행하도록 설계합니다. 모든 차시에서 학생은 자기 전공·동아리·진로의 실제 문제를 가져와 5단계를 통과시키며, 마지막 공개 단계에서 산출물을 외부에 공개합니다.'))
sections.append(empty_para())
gen_ai_rows = [
    ['워크숍', '대상·시간', '핵심 도구', '학생 산출물', 'DT 단계'],
    ['프롬프트 엔지니어링 실전 — 리서치에서 보고서까지', '신촌 25명·4H', 'ChatGPT, Perplexity, NotebookLM', '문제 진술서, 리서치 브리프(A4 3매), 프롬프트 라이브러리 5개', '①②③'],
    ['자연어로 만드는 첫 시제품 — Codex 입문', '국제 20명·4H', 'Codex, ChatGPT, Gemini', '동작 웹앱 1개, 공개 URL, 디버깅 로그', '④⑤'],
    ['NotebookLM 기반 컬렉션 큐레이션', '박물관 20명·3H', 'NotebookLM, ChatGPT, Gamma', '큐레이션 텍스트(800자), Gamma 패널 5장', '①②④'],
    ['공모전 출품작 만들기 — 아이디어에서 발표 자료까지', '국제 30명·4H', 'Gemini, Codex, Gamma', '아이디어 보드, 시제품, 발표 10장, 90초 피칭', '②③④⑤'],
]
sections.append(make_table(gen_ai_rows, [3000, 1500, 2200, 2700, 800]))
sections.append(empty_para())
sections.append(normal_para('국제캠퍼스 2학기 「공모전 연계 코딩 및 생성형 AI 워크숍」 10건은 1·2회차 발산(Gemini·Perplexity), 3·4회차 정의·시제품(Codex), 5·6회차 보강·발표자료(Gamma), 7·8회차 멘토링 클리닉, 9회차 리허설, 10회차 본선 쇼케이스로 직렬 연결되어 한 팀이 한 출품작을 완성하는 구조입니다.'))
sections.append(empty_para())

# ─── 2. 데이터 분석 ───
sections.append(arrow_heading('영역 2. 데이터 분석 (약 5~6건)'))
sections.append(normal_para('학부생이 마주하는 과제·인턴 업무 대부분은 흩어진 자료에서 의미 있는 패턴을 찾아 한 장으로 설명하는 일입니다. 비전공자에게 데이터 분석은 더 이상 SQL·통계 수식 암기가 아니라, 질문을 잘 정의하고 AI에게 적절히 맡기고 결과를 비판적으로 해석하는 능력입니다. 이공계 학생에게는 Codex·Colab 기반 자연어 분석 코드 생성을, 비전공 학생에게는 NotebookLM 중심 해석 워크플로우를 제공해 출발점이 달라도 같은 산출물에 도달하도록 설계합니다.'))
sections.append(empty_para())
data_rows = [
    ['워크숍', '대상·시간', '핵심 도구', '학생 산출물', 'DT 단계'],
    ['공공데이터로 내 동네·내 학과 질문에 답하기', '신촌·4H', '공공데이터포털, NotebookLM, ChatGPT', '공공데이터 인사이트 리포트(A4 2매)', '①②'],
    ['NotebookLM으로 리서치에서 분석 질문 뽑아내기', '신촌·4H', 'NotebookLM, Gemini', '분석 설계서, 인터뷰 질문지 10개, 데이터 후보 3건', '②③'],
    ['Codex·Colab로 자연어 분석 코드 만들기', '신촌·4H', 'Codex, ChatGPT, Colab', '시각화 3종, Colab 노트북, 1장 요약 슬라이드', '④⑤'],
]
sections.append(make_table(data_rows, [3000, 1200, 2300, 2700, 1000]))
sections.append(empty_para())
sections.append(normal_para('워크숍 W1에서 정의한 동네·학과 질문은 여름 AX 캠프 프로젝트의 출발 주제로, W2의 분석 설계서는 멘토링 1주차 검토 자료로, W3의 Colab 노트북은 캠프 중간 산출물의 분석 백본으로 이어집니다. 워크숍 4시간이 6주 프로젝트의 1차 시제품으로 자연스럽게 확장됩니다.'))
sections.append(empty_para())

# ─── 3. AI 에이전트 ───
sections.append(arrow_heading('영역 3. AI 에이전트 (약 5~7건, Codex 중심)'))
sections.append(normal_para('AI 에이전트는 자연어 지시만으로 코드 생성·도구 호출·작업 자동화를 수행하는 시스템으로, 학부생이 전공과 무관하게 자신의 학습·연구·일상 문제를 직접 해결하게 만드는 결정적 도구입니다. Codex를 활용하면 코딩 경험이 0~1년인 학생도 한국어로 의도를 설명하는 것만으로 동작하는 시제품을 만들 수 있어 진입장벽이 사실상 사라집니다. 본 영역은 Vibe Coding(의도→코드) → Agentic Coding(AI가 도구 사용·자율 판단) → Harness Engineering(멀티 에이전트 오케스트레이션)의 3단계로 학생을 만드는 사람으로 전환시킵니다.'))
sections.append(empty_para())
agent_rows = [
    ['워크숍', '단계', '핵심 도구', '학생 산출물'],
    ['내 일상을 자동화하는 AI 비서 만들기', 'Vibe Coding', 'Codex, ChatGPT', '개인 AI 비서 1개 (과제·이메일·노션 자동 정리)'],
    ['리서치를 대신해주는 에이전트 만들기', 'Agentic Coding', 'Codex, Gemini', '자율 리서치 에이전트 1개 (주제 → 출처 포함 2페이지 브리프)'],
    ['여러 에이전트가 협업하는 워크플로우', 'Harness Engineering', 'Codex, n8n, Zapier', '3개 에이전트 협업 워크플로우 1개'],
]
sections.append(make_table(agent_rows, [2900, 1700, 2000, 3600]))
sections.append(empty_para())
sections.append(normal_para('여름 AX 캠프 Track B(AI 에이전트 트랙)는 4시간 × 5일 집중 + 멘토링 2주로 운영됩니다. 1일차 Vibe Coding 입문, 2일차 Tool-use 기초, 3일차 ReAct 루프, 4일차 멀티 에이전트 분업, 5일차 데모데이로 구성됩니다. 팀별 최종 산출물은 신입생 수강신청 어시스턴트, 학과 공지 자동 큐레이션 봇 같은 실생활 문제 해결 에이전트 서비스 1개와 시연 영상, 운영 매뉴얼입니다.'))
sections.append(empty_para())

# ─── 4. 디지털 콘텐츠 제작 ───
sections.append(arrow_heading('영역 4. 디지털 콘텐츠 제작 (약 16건)'))
sections.append(normal_para('인문·예체능 학부생에게 디지털 콘텐츠 제작은 자기 서사를 사회와 연결하는 언어입니다. 졸업 후 SNS 릴스, 링크드인 포트폴리오, 공모전 출품, 첫 직장의 브랜드 운영 업무에서 즉시 요구되는 표현 문법입니다. AI 시대의 콘텐츠 제작은 Canva·CapCut 같은 도구 숙련이 아니라, 기획 의도를 정확한 프롬프트로 번역하고 AI 생성물을 자기 관점으로 큐레이션·재편집하는 판단력을 기르는 일입니다.'))
sections.append(empty_para())
content_rows = [
    ['워크숍', '대상·시간', '핵심 도구', '학생 산출물'],
    ['3시간 만의 브랜드 미니 캠페인', '국제 신입생 25명·3H', 'ChatGPT, Midjourney, Canva', 'SNS 캠페인 키트 1세트 (슬로건·비주얼 4컷·채널 포맷 3종)'],
    ['숏폼 다큐 — 내 동네 3분', '국제 20명·3H', 'CapCut, Suno, ChatGPT', '3분 다큐 영상 1편 + 메이킹 노트'],
    ['책을 한 장의 인포그래픽으로 (AX 북클럽)', '북클럽 25명·3H', 'Gemini, Gamma, Canva', '인포그래픽 1장 + 발표 슬라이드 5장'],
    ['북클럽 → 공모전 출품작 만들기', '출품 희망자 20명·3H', 'ChatGPT, Midjourney, Suno, CapCut', '60초 출품 영상 1편 + 출품 신청서'],
]
sections.append(make_table(content_rows, [3000, 1700, 2100, 3400]))
sections.append(empty_para())
sections.append(normal_para('실감미디어 체험 교육(252회 운영)은 발주처 학술정보원의 VR/AR/MR 인프라를 활용하며, 모두의연구소는 콘텐츠 시나리오 설계·AI 연계 학습지·진행 가이드를 지원합니다. 회당 1시간 흐름은 체험 주제 브리프 10분 → 실감미디어 체험 35분 → ChatGPT/Gemini로 체험 후기 구조화·SNS 카드 1장 즉석 제작 15분으로 구성됩니다. Physical AI 접점으로 VR 캠퍼스 투어 중 시선·동선 데이터를 AI가 요약해 학생 행동 페르소나 카드를 산출하는 사례를 시범 운영합니다.'))
sections.append(empty_para())

# ─── 5. 인문학 × AI 융합 ───
sections.append(arrow_heading('영역 5. 인문학 × AI 융합 (박물관, 약 6건)'))
sections.append(normal_para('박물관은 본래 시간을 견딘 것들이 모이는 장소이며, AI는 그 시간을 새로운 언어로 다시 읽게 합니다. 신촌캠퍼스 박물관에서 AI 교육을 한다는 것은 기술을 가르치는 일이 아니라, 인문학이 디지털 시대에 어떻게 더 멀리 닿을 수 있는지를 함께 묻는 일입니다. 디지털은 인문학을 대체하지 않으며, 오히려 한글 고문헌·연세 역사 자료·박물관 컬렉션을 더 많은 사람과 연결하는 통로가 됩니다.'))
sections.append(empty_para())
humanities_rows = [
    ['프로그램', '주제·진행', '연사·도구', '학생 산출물'],
    ['인문학 세미나 1', 'AX 시대, 인문학의 미래 (강연·Q&A)', '디지털 인문학·미디어철학 연구자 / NotebookLM', '강연록 정리 1편'],
    ['인문학 세미나 2', 'AX 시대, 인문학의 미래 (사례 토론)', '문화비평가·콘텐츠 기획자 / ChatGPT', '토론 회고문 1편'],
    ['인문학 세미나 3', '한글을 지킨 연세의 거인들 (유물 투어 + 강의)', '국어학·연세 사학 전공자 / Gemini', '인물 아카이브 카드'],
    ['AI 창작 워크숍 (기초)', '컬렉션을 다시 읽다 (3H)', 'NotebookLM, ChatGPT, Midjourney, Suno', '멀티미디어 큐레이션 카드 1세트'],
    ['AI 창작 워크숍 (심화)', '큐레이션과 전시 (3H)', 'ChatGPT, Midjourney, Suno, Canva, Gamma', 'AI 협업 작품 1점 + 전시 패널·발표자료'],
    ['문화유산 기반 AX 공모전', '한글 고문헌 재해석 / 연세 인물 헌정 / 미공개 유물 큐레이션', '평가: 인문학 깊이 40 + 창의성 30 + AI 활용 20 + 완성도 10', '공모전 출품작 (우수작은 박물관 전시)'],
]
sections.append(make_table(humanities_rows, [2200, 2900, 2400, 2700]))
sections.append(empty_para())

# ─── 5대 영역 통합 정리 ───
sections.append(arrow_heading('5대 영역 통합 정리'))
summary_rows = [
    ['영역', '분량', '운영 캠퍼스', '핵심 도구', '대표 산출물'],
    ['생성형 AI', '약 29건', '신촌·국제', 'ChatGPT, Gemini, Perplexity, NotebookLM, Codex, Gamma', '문제 진술서, 리서치 브리프, 시제품, 공모전 출품작'],
    ['데이터 분석', '약 5~6건', '신촌', 'NotebookLM, ChatGPT, Codex, Colab', '인사이트 리포트, 시각화, 분석 노트북'],
    ['AI 에이전트', '약 5~7건', '신촌', 'Codex(중심), n8n, Zapier', '개인 AI 비서, 자율 리서치 에이전트, 멀티 에이전트 워크플로우'],
    ['디지털 콘텐츠 제작', '약 16건', '국제', 'Canva, CapCut, Gamma, Midjourney, Suno', '캠페인 키트, 숏폼 다큐, 인포그래픽, 공모전 영상'],
    ['인문학 × AI 융합', '약 6건', '박물관', 'NotebookLM, ChatGPT, Midjourney, Suno, Canva', '큐레이션 카드, AI 협업 작품, 전시 패널'],
]
sections.append(make_table(summary_rows, [2000, 1100, 1400, 2900, 2800]))
sections.append(empty_para())

new_xml = ''.join(sections)
print(f"새 섹션 XML 크기: {len(new_xml)} bytes")

# ─── 삽입 위치 찾기: '5대 주제 영역' 표 다음 ───
# 표는 first row에 '주제 영역', '세부 내용'이 있음
# document.xml에서 그 표의 </w:tbl>를 찾아서 그 뒤에 삽입

# '주제 영역' 텍스트가 들어 있는 표 찾기
# 패턴: <w:tbl> ... '주제 영역' ... '세부 내용' ... </w:tbl>
# 좀 더 정확히: '주제 영역'을 포함한 표의 끝 </w:tbl> 위치
target_text_pos = content.find('주제 영역')
if target_text_pos < 0:
    print("ERROR: '주제 영역' 키워드 없음")
    sys.exit(1)

# 그 뒤로 '세부 내용'이 있는지 확인
detail_pos = content.find('세부 내용', target_text_pos)
# '인문학 × AI 융합'까지 있는 표인지 (5대 영역 표)
human_pos = content.find('인문학 × AI 융합', target_text_pos)
if human_pos < 0:
    print("ERROR: '인문학 × AI 융합' 없음")
    sys.exit(1)

# 그 표의 끝 </w:tbl>
table_end = content.find('</w:tbl>', human_pos) + len('</w:tbl>')
if table_end < 0:
    print("ERROR: 표 끝을 찾지 못함")
    sys.exit(1)

print(f"삽입 위치 (5대 주제 영역 표 끝): {table_end}")

# 삽입
new_content = content[:table_end] + new_xml + content[table_end:]

with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ 5대 영역별 상세 섹션 삽입 완료")
print(f"파일 크기: {len(content)} -> {len(new_content)} bytes (+{len(new_content) - len(content)})")
