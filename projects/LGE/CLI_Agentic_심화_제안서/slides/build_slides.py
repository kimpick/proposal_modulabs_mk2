"""
LGE C-Level 보고용 제안 슬라이드 생성기
==========================================
12장 스토리보드 / Pretendard / 모두의연구소 브랜드 컬러
PyPPTX 1.0.2 호환
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# ──────────────────────────────────────────────────────────────
# 디자인 시스템 (모두의연구소 브랜드)
# ──────────────────────────────────────────────────────────────
PRIMARY = RGBColor(0xF7, 0x58, 0x5C)      # 코랄 #F7585C
DARK = RGBColor(0x03, 0x07, 0x12)          # 다크 #030712
LIGHT_BG = RGBColor(0xF4, 0xF6, 0xF8)      # 라이트 배경 #F4F6F8
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CORAL_BG = RGBColor(0xFF, 0xF2, 0xF2)      # 코랄 틴트 #FFF2F2
GRADIENT_END = RGBColor(0x1A, 0x1F, 0x2E)
BODY_TEXT = RGBColor(0x2E, 0x33, 0x39)     # 본문 텍스트
SECONDARY = RGBColor(0x5F, 0x65, 0x6C)     # 보조 텍스트
MUTED_DARK = RGBColor(0x6B, 0x72, 0x80)
MUTED_LIGHT = RGBColor(0xAA, 0xAE, 0xB5)

# 폰트 (시스템 설치된 Pretendard)
FONT_BOLD = "Pretendard Bold"
FONT_REGULAR = "Pretendard"
FONT_LIGHT = "Pretendard Light"
FONT_MEDIUM = "Pretendard Medium"

# 슬라이드 사이즈 (16:9, 13.333" × 7.5")
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def set_bg(slide, color):
    """슬라이드 배경색 설정"""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, x, y, w, h, color):
    """사각형 추가"""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_rounded_rect(slide, x, y, w, h, color):
    """둥근 사각형"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    try:
        shape.adjustments[0] = 0.06
    except Exception:
        pass
    return shape


def add_text(slide, x, y, w, h, text, *, font=FONT_REGULAR, size=18,
             color=BODY_TEXT, bold=False, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.3, italic=False):
    """텍스트 박스 추가"""
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    tf.vertical_anchor = anchor

    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.bold = bold
        run.font.italic = italic
    return box


def add_runs(slide, x, y, w, h, runs, *, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.3):
    """여러 run을 가진 텍스트 (하이라이트용)"""
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    tf.vertical_anchor = anchor

    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    for r in runs:
        run = p.add_run()
        run.text = r["text"]
        run.font.name = r.get("font", FONT_REGULAR)
        run.font.size = Pt(r.get("size", 18))
        run.font.color.rgb = r.get("color", BODY_TEXT)
        run.font.bold = r.get("bold", False)
        run.font.italic = r.get("italic", False)
    return box


def add_section_label(slide, x, y, text, color=PRIMARY):
    """섹션 라벨 (UPPERCASE, 코랄, 작게)"""
    add_text(slide, x, y, Inches(4), Inches(0.3),
             text.upper(), font=FONT_BOLD, size=12, color=color,
             line_spacing=1.0)


def add_title(slide, x, y, w, text, *, size=32, color=DARK, max_h=1.8):
    """슬라이드 타이틀 (Action Title)"""
    add_text(slide, x, y, w, Inches(max_h),
             text, font=FONT_BOLD, size=size, color=color,
             line_spacing=1.25)


def add_source_caption(slide, text, color=SECONDARY):
    """하단 출처 (작게, 이탤릭)"""
    add_text(slide, Inches(0.7), Inches(7.05), Inches(12), Inches(0.3),
             text, font=FONT_REGULAR, size=10, color=color,
             italic=True, line_spacing=1.2)


def add_card(slide, x, y, w, h, fill_color):
    """카드 배경 (둥근 사각형)"""
    return add_rounded_rect(slide, x, y, w, h, fill_color)


def header_block(slide, label, title, *, title_size=32, label_color=PRIMARY,
                 title_color=DARK, bg_color=WHITE):
    """슬라이드 공통 헤더 (라벨 + 타이틀)"""
    set_bg(slide, bg_color)
    add_section_label(slide, Inches(0.7), Inches(0.6), label, color=label_color)
    add_title(slide, Inches(0.7), Inches(1.0), Inches(12), title,
              size=title_size, color=title_color, max_h=2.0)


# ──────────────────────────────────────────────────────────────
# 슬라이드 생성 (12장)
# ──────────────────────────────────────────────────────────────

def slide_01_cover(prs):
    """슬라이드 1 — 표지 (다크)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, DARK)
    add_rect(slide, Inches(0.7), Inches(0.95), Inches(0.08), Inches(0.6), PRIMARY)

    add_text(slide, Inches(0.95), Inches(1.0), Inches(8), Inches(0.4),
             "모두의연구소 × LGE  ·  전략 제안",
             font=FONT_BOLD, size=12, color=PRIMARY, line_spacing=1.0)

    add_text(slide, Inches(0.95), Inches(2.3), Inches(11.5), Inches(2.5),
             "개발자 역량 고도화와\n조직 지식 인프라를 위한\nAgentic AI 통합 교육",
             font=FONT_BOLD, size=44, color=WHITE, line_spacing=1.25)

    add_text(slide, Inches(0.95), Inches(5.2), Inches(11.5), Inches(0.5),
             "CLI 마스터리 · Agentic AI 심화 · 지식관리체계  |  총 14일 83H 집중 투자",
             font=FONT_LIGHT, size=18, color=MUTED_LIGHT, line_spacing=1.3)

    add_text(slide, Inches(0.95), Inches(6.8), Inches(11.5), Inches(0.3),
             "2026.07  ·  모두의연구소 AI 기업교육 커리큘럼",
             font=FONT_REGULAR, size=11, color=MUTED_DARK, line_spacing=1.2)

    add_rect(slide, Inches(12.5), Inches(6.85), Inches(0.4), Inches(0.08), PRIMARY)


def slide_02_exec_summary(prs):
    """슬라이드 2 — Executive Summary (화이트)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header_block(slide, "EXECUTIVE SUMMARY",
                 "6일×2트랙 + 5일 집중, 14일 투자로 LGE 개발자와 조직 지식 자산을 동시 전환")

    conclusions = [
        ("01", "Why", "AX 속도가 경쟁우위를 결정 — LGE는 2-3년 내 30% 생산성 향상 목표 (CEO 발표)"),
        ("02", "What", "개발자 역량 라인(6일) + 조직 지식 인프라 라인(5일), 총 14일 83H"),
        ("03", "Ask", "2026 Q3-Q4 실행 승인 — 3개 과정 모듈러 운영, 사후 로드맵 포함"),
    ]

    y = Inches(3.2)
    for num, label, body in conclusions:
        add_text(slide, Inches(0.7), y, Inches(1.2), Inches(0.7),
                 num, font=FONT_BOLD, size=36, color=PRIMARY, line_spacing=1.0)
        add_text(slide, Inches(1.95), y + Inches(0.05), Inches(1.5), Inches(0.4),
                 label, font=FONT_BOLD, size=12, color=PRIMARY, line_spacing=1.0)
        add_text(slide, Inches(1.95), y + Inches(0.4), Inches(10.5), Inches(0.7),
                 body, font=FONT_REGULAR, size=18, color=BODY_TEXT, line_spacing=1.35)
        y += Inches(1.05)

    add_source_caption(slide, "출처: LG Electronics CEO 전사 전략 발표 (2026.01) · 모두의연구소 제안서 종합")


def slide_03_why_now(prs):
    """슬라이드 3 — Why Now (다크)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, DARK)

    add_section_label(slide, Inches(0.7), Inches(0.6), "WHY NOW", color=PRIMARY)

    add_text(slide, Inches(0.7), Inches(1.2), Inches(12), Inches(2.8),
             "\"AX(AI Transformation)의 속도가\n비즈니스의 성패를 좌우한다\"",
             font=FONT_BOLD, size=38, color=WHITE, line_spacing=1.3)

    add_text(slide, Inches(0.7), Inches(4.1), Inches(10), Inches(0.4),
             "— 구자완 LG Electronics CEO, 2025년 사내 메시지 중",
             font=FONT_LIGHT, size=16, color=MUTED_LIGHT, line_spacing=1.3, italic=True)

    add_rect(slide, Inches(0.7), Inches(4.9), Inches(0.6), Inches(0.05), PRIMARY)

    cards = [
        ("LGE 자체 목표", "전사 생산성 30% 향상\n(2-3년 내 달성, 2026.01 발표)"),
        ("제도적 타이밍", "AI 기본법 전면 시행\n(2026.01, 공공 AI 우선 구매)"),
        ("시장 현실", "Fortune 500의 80%가 이미\n활성 AI 에이전트 운영 중"),
    ]

    x = Inches(0.7)
    for title, body in cards:
        add_card(slide, x, Inches(5.2), Inches(3.85), Inches(1.5),
                 GRADIENT_END)
        add_text(slide, x + Inches(0.25), Inches(5.35), Inches(3.4), Inches(0.4),
                 title, font=FONT_BOLD, size=14, color=PRIMARY, line_spacing=1.0)
        add_text(slide, x + Inches(0.25), Inches(5.8), Inches(3.4), Inches(0.8),
                 body, font=FONT_REGULAR, size=14, color=WHITE, line_spacing=1.35)
        x += Inches(4.05)

    add_source_caption(slide,
                       "출처: LG Newsroom (2026.01) · AI Basic Act (2026.01 시행) · Microsoft Security Blog (2026.02)",
                       color=MUTED_DARK)


def slide_04_strategy(prs):
    """슬라이드 4 — 전략 방향 (코랄 액센트)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, PRIMARY)

    add_section_label(slide, Inches(0.7), Inches(0.6),
                      "STRATEGY", color=WHITE)

    add_text(slide, Inches(0.7), Inches(1.2), Inches(12), Inches(1.5),
             "두 축을 동시에 확보해야\nAgentic AI 시대의 주도권을 쥡니다",
             font=FONT_BOLD, size=36, color=WHITE, line_spacing=1.25)

    axes = [
        ("LINE 1", "개발자 역량 고도화",
         "도구 사용자 → 하네스/루프 설계자 → 에이전트 오케스트레이터",
         "Track 1 (3일) + Track 2 (3일) = 48H"),
        ("LINE 2", "조직 지식 인프라",
         "RAG → OKF · 온톨로지 · 자체 MCP 서버 (지식 자산화)",
         "지식관리체계 (5일) = 35H"),
    ]

    x = Inches(0.7)
    for label, title, body, footprint in axes:
        add_card(slide, x, Inches(3.5), Inches(6), Inches(2.9), WHITE)
        add_text(slide, x + Inches(0.4), Inches(3.7), Inches(5), Inches(0.4),
                 label, font=FONT_BOLD, size=13, color=PRIMARY, line_spacing=1.0)
        add_text(slide, x + Inches(0.4), Inches(4.15), Inches(5.2), Inches(0.7),
                 title, font=FONT_BOLD, size=22, color=DARK, line_spacing=1.2)
        add_text(slide, x + Inches(0.4), Inches(4.95), Inches(5.2), Inches(1.0),
                 body, font=FONT_REGULAR, size=14, color=BODY_TEXT, line_spacing=1.4)
        add_text(slide, x + Inches(0.4), Inches(5.85), Inches(5.2), Inches(0.4),
                 footprint, font=FONT_BOLD, size=13, color=PRIMARY, line_spacing=1.2)
        x += Inches(6.3)

    add_text(slide, Inches(0.7), Inches(6.75), Inches(12), Inches(0.4),
             "개발자 한 명의 역량 전환 × 조직 전체의 지식 자산화 = LGE 고유 AX 자산",
             font=FONT_BOLD, size=14, color=WHITE, align=PP_ALIGN.CENTER,
             line_spacing=1.2)


def slide_05_market_evidence(prs):
    """슬라이드 5 — 시장 증거 (라이트)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header_block(slide, "MARKET EVIDENCE",
                 "전 세계 개발자 90%가 이미 AI를 씁니다 — 그럼 LGE 개발자의 위치는?",
                 bg_color=LIGHT_BG)

    stats = [
        ("90%", "개발자 AI 도구 사용", "Google DORA 2025"),
        ("55%", "코딩 속도 향상", "GitHub Copilot 실증 (Microsoft)"),
        ("80%", "Fortune 500 AI 에이전트 운영", "Microsoft Security 2026"),
    ]

    x = Inches(0.7)
    for stat, label, source in stats:
        add_card(slide, x, Inches(3.2), Inches(3.85), Inches(3.0), WHITE)
        add_text(slide, x + Inches(0.3), Inches(3.5), Inches(3.3), Inches(1.3),
                 stat, font=FONT_BOLD, size=78, color=PRIMARY, line_spacing=1.0)
        add_text(slide, x + Inches(0.3), Inches(4.95), Inches(3.3), Inches(0.5),
                 label, font=FONT_BOLD, size=18, color=DARK, line_spacing=1.25)
        add_text(slide, x + Inches(0.3), Inches(5.55), Inches(3.3), Inches(0.4),
                 source, font=FONT_REGULAR, size=12, color=SECONDARY,
                 line_spacing=1.2, italic=True)
        x += Inches(4.05)

    add_text(slide, Inches(0.7), Inches(6.5), Inches(12), Inches(0.5),
             "경쟁사는 이미 움직이고 있습니다. LGE가 우위를 점할 시간적 여유가 줄어들고 있습니다.",
             font=FONT_BOLD, size=14, color=DARK, line_spacing=1.3)

    add_source_caption(slide,
                       "출처: Google DORA State of AI-Assisted Software Development (2025) · Microsoft Research Copilot Study · Microsoft Security Blog (2026.02)")


def slide_06_portfolio(prs):
    """슬라이드 6 — 제안 포트폴리오 한눈에 (화이트)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header_block(slide, "PROPOSAL PORTFOLIO",
                 "3개 과정, 2개 라인, 총 14일 83H — 모듈러 선택 가능")

    courses = [
        ("LINE 1 · TRACK 1", "CLI 도구 입문",
         "Codex + Claude Code 마스터리",
         "3일", "24H",
         ["에이전틱 패러다임", "Codex CLI (GPT-5.6)", "Claude Code (4.7)", "Subagents · Hooks · Skills", "MCP 파이프라인"],
         LIGHT_BG),
        ("LINE 1 · TRACK 2", "Agentic AI 심화",
         "하네스 + 루프 엔지니어링",
         "3일", "24H",
         ["AGENTS.md 설계", "Architectural Constraints", "AORR 상태 머신", "Self-Correcting TDD", "마스터-워커 오케스트레이션"],
         LIGHT_BG),
        ("LINE 2", "지식관리체계",
         "RAG → OKF · MCP 서버 개발",
         "5일", "35H",
         ["온톨로지 설계", "OKF 아카이빙 자동화", "FastMCP 서버 직접 개발", "에이전트 통합 · 자가교정", "팀 미니 프로젝트"],
         CORAL_BG),
    ]

    x = Inches(0.7)
    for label, title, subtitle, days, hours, modules, bg_color in courses:
        add_card(slide, x, Inches(3.0), Inches(3.85), Inches(4.0), bg_color)
        add_text(slide, x + Inches(0.3), Inches(3.2), Inches(3.3), Inches(0.4),
                 label, font=FONT_BOLD, size=11, color=PRIMARY, line_spacing=1.0)
        add_text(slide, x + Inches(0.3), Inches(3.55), Inches(3.3), Inches(0.5),
                 title, font=FONT_BOLD, size=22, color=DARK, line_spacing=1.2)
        add_text(slide, x + Inches(0.3), Inches(4.05), Inches(3.3), Inches(0.4),
                 subtitle, font=FONT_REGULAR, size=13, color=SECONDARY,
                 line_spacing=1.2, italic=True)
        add_runs(slide, x + Inches(0.3), Inches(4.55), Inches(3.3), Inches(0.6),
                 [
                     {"text": days, "font": FONT_BOLD, "size": 28, "color": DARK},
                     {"text": "  ·  ", "font": FONT_BOLD, "size": 20, "color": MUTED_LIGHT},
                     {"text": hours, "font": FONT_BOLD, "size": 28, "color": PRIMARY},
                 ])
        y = Inches(5.35)
        for m in modules:
            add_rect(slide, x + Inches(0.3), y + Inches(0.1), Inches(0.08), Inches(0.08), PRIMARY)
            add_text(slide, x + Inches(0.5), y, Inches(3.0), Inches(0.32),
                     m, font=FONT_REGULAR, size=12, color=BODY_TEXT, line_spacing=1.2)
            y += Inches(0.3)
        x += Inches(4.05)

    add_source_caption(slide, "모듈러 운영: 3개 과정을 순차 이수 또는 개별 선택 가능 · 그룹별 12-15명 권장 · 주강사 1 + 보조강사 1")


def slide_07_track1(prs):
    """슬라이드 7 — Track 1 CLI 입문 (라이트)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header_block(slide, "LINE 1 · TRACK 1 (기초)",
                 "Codex + Claude Code CLI 마스터리 — 개발자 개인 역량의 첫 도약",
                 bg_color=LIGHT_BG, title_size=28)

    days = [
        ("DAY 1", "패러다임 + Codex",
         ["에이전틱 코딩 개념", "Codex CLI 환경 구축", "스캐폴딩 · 멀티파일", "PR 기반 코드 리뷰"],
         "8H"),
        ("DAY 2", "Claude Code 심화",
         ["Claude Code CLI 환경", "디버깅 · 리팩토링", "Subagents 분업", "Hooks · SKILL.md"],
         "8H"),
        ("DAY 3", "통합 실전",
         ["컨텍스트 엔지니어링", "MCP 서버 연동", "Codex+Claude 분업", "팀 프로젝트 발표"],
         "8H"),
    ]

    x = Inches(0.7)
    for day, title, items, hours in days:
        add_card(slide, x, Inches(3.1), Inches(3.85), Inches(3.5), WHITE)
        add_text(slide, x + Inches(0.3), Inches(3.25), Inches(2), Inches(0.4),
                 day, font=FONT_BOLD, size=13, color=PRIMARY, line_spacing=1.0)
        add_text(slide, x + Inches(2.9), Inches(3.25), Inches(0.7), Inches(0.4),
                 hours, font=FONT_BOLD, size=14, color=PRIMARY, align=PP_ALIGN.RIGHT,
                 line_spacing=1.0)
        add_text(slide, x + Inches(0.3), Inches(3.75), Inches(3.3), Inches(0.6),
                 title, font=FONT_BOLD, size=20, color=DARK, line_spacing=1.2)
        add_rect(slide, x + Inches(0.3), Inches(4.45), Inches(0.4), Inches(0.04), PRIMARY)
        y = Inches(4.7)
        for item in items:
            add_rect(slide, x + Inches(0.3), y + Inches(0.12), Inches(0.07), Inches(0.07), PRIMARY)
            add_text(slide, x + Inches(0.5), y, Inches(3.0), Inches(0.35),
                     item, font=FONT_REGULAR, size=13, color=BODY_TEXT, line_spacing=1.3)
            y += Inches(0.42)
        x += Inches(4.05)

    add_text(slide, Inches(0.7), Inches(6.75), Inches(12), Inches(0.4),
             "→  산출물: CLI 자동화 프로젝트 1건 + Hooks+Skills 적용 Claude Code 환경",
             font=FONT_BOLD, size=13, color=DARK, line_spacing=1.2)

    add_source_caption(slide, "선수: Python/Node 기초 이상, CLI·Git 능숙 · 최신 도구: Codex CLI v0.145, Claude Code v2.1, GPT-5.6, Claude 4.7")


def slide_08_track2(prs):
    """슬라이드 8 — Track 2 Agentic AI 심화 (화이트)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header_block(slide, "LINE 1 · TRACK 2 (심화)",
                 "Agentic AI 하네스 + 루프 엔지니어링 — 에이전트 오케스트레이터로 도약",
                 title_size=28)

    days = [
        ("DAY 1", "하네스 엔지니어링",
         ["하네스 패러다임", "AGENTS.md 설계", "제약 + 엔트로피", "Sandbox · 가드레일"],
         "구조"),
        ("DAY 2", "루프 엔지니어링",
         ["AORR 상태 머신", "Self-Correcting TDD", "영구 메모리", "무한루프 탈출 · HITL"],
         "동적 흐름"),
        ("DAY 3", "오케스트레이션 실전",
         ["마스터-워커 하이브리드", "Tmux 4분할 관제소", "Git Worktree 샌드박스", "버그 티켓 자율 루프"],
         "통합"),
    ]

    x = Inches(0.7)
    for day, title, items, theme in days:
        add_card(slide, x, Inches(3.1), Inches(3.85), Inches(3.5), LIGHT_BG)
        add_text(slide, x + Inches(0.3), Inches(3.25), Inches(2), Inches(0.4),
                 day, font=FONT_BOLD, size=13, color=PRIMARY, line_spacing=1.0)
        add_text(slide, x + Inches(2.0), Inches(3.25), Inches(1.6), Inches(0.4),
                 theme, font=FONT_BOLD, size=11, color=SECONDARY, align=PP_ALIGN.RIGHT,
                 line_spacing=1.0, italic=True)
        add_text(slide, x + Inches(0.3), Inches(3.75), Inches(3.3), Inches(0.6),
                 title, font=FONT_BOLD, size=20, color=DARK, line_spacing=1.2)
        add_rect(slide, x + Inches(0.3), Inches(4.45), Inches(0.4), Inches(0.04), PRIMARY)
        y = Inches(4.7)
        for item in items:
            add_rect(slide, x + Inches(0.3), y + Inches(0.12), Inches(0.07), Inches(0.07), PRIMARY)
            add_text(slide, x + Inches(0.5), y, Inches(3.0), Inches(0.35),
                     item, font=FONT_REGULAR, size=13, color=BODY_TEXT, line_spacing=1.3)
            y += Inches(0.42)
        x += Inches(4.05)

    add_text(slide, Inches(0.7), Inches(6.75), Inches(12), Inches(0.4),
             "→  산출물: 버그 자율 해결 파이프라인 + LGE 30/60/90일 도입 로드맵",
             font=FONT_BOLD, size=13, color=DARK, line_spacing=1.2)

    add_source_caption(slide,
                       "선수: Track 1 수료 또는 CLI 에이전틱 코딩 실무 경험 · Boris Cherny 루프 3단계 · Anthropic Engineering Blog 기반")


def slide_09_knowledge(prs):
    """슬라이드 9 — 지식관리체계 (라이트)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header_block(slide, "LINE 2 · 조직 지식 인프라",
                 "RAG를 넘어 OKF · 온톨로지 · 자체 MCP 서버로 조직 지식을 자산화",
                 bg_color=LIGHT_BG, title_size=28)

    days = [
        ("DAY 1", "지식 아키텍처", "LLMwiki 핸즈온"),
        ("DAY 2", "OKF 아카이빙", "문서 → OKF 자동 변환"),
        ("DAY 3", "MCP 서버 개발", "FastMCP Resource · Tool"),
        ("DAY 4", "에이전트 통합", "에러북 자가교정"),
        ("DAY 5", "미니 프로젝트", "팀 파이프라인 완성"),
    ]

    x = Inches(0.7)
    card_w = Inches(2.36)
    for i, (day, title, sub) in enumerate(days):
        bg = CORAL_BG if i == 4 else WHITE
        add_card(slide, x, Inches(3.0), card_w, Inches(2.4), bg)
        add_text(slide, x + Inches(0.2), Inches(3.15), card_w - Inches(0.4), Inches(0.4),
                 day, font=FONT_BOLD, size=12, color=PRIMARY, line_spacing=1.0)
        add_text(slide, x + Inches(0.2), Inches(3.55), card_w - Inches(0.4), Inches(0.6),
                 title, font=FONT_BOLD, size=16, color=DARK, line_spacing=1.2)
        add_text(slide, x + Inches(0.2), Inches(4.3), card_w - Inches(0.4), Inches(0.9),
                 sub, font=FONT_REGULAR, size=12, color=SECONDARY, line_spacing=1.35)
        if i < len(days) - 1:
            add_text(slide, x + card_w - Inches(0.1), Inches(3.9), Inches(0.4), Inches(0.5),
                     "›", font=FONT_BOLD, size=24, color=PRIMARY, align=PP_ALIGN.CENTER,
                     line_spacing=1.0)
        x += card_w + Inches(0.1)

    value_y = Inches(5.7)
    values = [
        ("데이터 주권", "사내 지식이 외부 LLM에 유출되지 않는 구조"),
        ("에이전트 친화적", "에이전트가 사내 지식을 자율 조회·활용"),
        ("복리 효과", "지식이 쓸수록 축적되는 compounding 구조"),
    ]

    x = Inches(0.7)
    for title, body in values:
        add_text(slide, x, value_y, Inches(3.85), Inches(0.4),
                 "● " + title, font=FONT_BOLD, size=13, color=PRIMARY, line_spacing=1.2)
        add_text(slide, x + Inches(0.25), value_y + Inches(0.35), Inches(3.6), Inches(0.6),
                 body, font=FONT_REGULAR, size=11, color=BODY_TEXT, line_spacing=1.3)
        x += Inches(4.05)

    add_source_caption(slide,
                       "선수: Python 기초 이상 (FastMCP 서버 코딩 포함) · OKF: Google Cloud 2026.06 공개 스펙 · APEX-MEM: Amazon Science 2026.04")


def slide_10_synergy(prs):
    """슬라이드 10 — 결합 시너지 (코랄 틴트)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, CORAL_BG)

    add_section_label(slide, Inches(0.7), Inches(0.6), "SYNERGY", color=PRIMARY)
    add_title(slide, Inches(0.7), Inches(1.0), Inches(12),
              "두 라인이 만나면 LGE 고유의 'Agentic AX 자산'이 완성됩니다",
              size=30, color=DARK, max_h=2.0)

    synergies = [
        ("개발자 + 지식 서버",
         "Track 1·2 수료 개발자가\n자체 MCP 서버를 직접 확장"),
        ("조직 지식 + 에이전트",
         "사내 문서가 에이전트를 통해\n현업 의사결정에 실시간 활용"),
        ("복리 효과 창출",
         "교육 일회성이 아니라\n지속 진화하는 자산 형성"),
    ]

    x = Inches(0.7)
    for title, body in synergies:
        add_card(slide, x, Inches(3.5), Inches(3.85), Inches(2.7), WHITE)
        add_text(slide, x + Inches(0.3), Inches(3.7), Inches(3.3), Inches(0.7),
                 title, font=FONT_BOLD, size=17, color=DARK, line_spacing=1.2)
        add_rect(slide, x + Inches(0.3), Inches(4.5), Inches(0.5), Inches(0.05), PRIMARY)
        add_text(slide, x + Inches(0.3), Inches(4.75), Inches(3.3), Inches(1.4),
                 body, font=FONT_REGULAR, size=15, color=BODY_TEXT, line_spacing=1.45)
        x += Inches(4.05)

    add_text(slide, Inches(0.7), Inches(6.5), Inches(12), Inches(0.5),
             "개별 과정의 단순 합(14일)을 넘어 — LGE가 독자적으로 운영·확장하는 Agentic AX 체계로 진화",
             font=FONT_BOLD, size=15, color=DARK, align=PP_ALIGN.CENTER,
             line_spacing=1.3)


def slide_11_impact(prs):
    """슬라이드 11 — 기대 효과 (라이트, 과장 없이)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header_block(slide, "BUSINESS IMPACT",
                 "정량적 임팩트 — 모든 숫자에 명확한 출처가 있습니다",
                 bg_color=LIGHT_BG, title_size=28)

    metrics = [
        ("개발 생산성", "+55%", "코딩 속도 향상",
         "Microsoft Research Copilot 실증 (16,223명)", PRIMARY),
        ("에이전트 성능", "+90.2%", "단일 대비 성능",
         "Anthropic Multi-agent 연구 (breadth-first 작업 한정)", DARK),
        ("조직 데이터 활용", "1/480", "분석 시간 단축",
         "LGE CHATDA 사례: 3-5일 → 30분 (CEO 발표 인용)", PRIMARY),
        ("기술 부채 리스크", "↓ 73%", "AI 코드 유지보수 우려",
         "GitLab 2026 — 본 과정으로 통제 역량 확보", DARK),
    ]

    positions = [
        (Inches(0.7), Inches(3.0)),
        (Inches(6.95), Inches(3.0)),
        (Inches(0.7), Inches(5.05)),
        (Inches(6.95), Inches(5.05)),
    ]

    for (label, value, sub, source, color), (x, y) in zip(metrics, positions):
        add_card(slide, x, y, Inches(6.0), Inches(1.85), WHITE)
        add_text(slide, x + Inches(0.3), y + Inches(0.2), Inches(2.5), Inches(0.4),
                 label, font=FONT_BOLD, size=12, color=SECONDARY, line_spacing=1.0)
        add_text(slide, x + Inches(0.3), y + Inches(0.65), Inches(2.2), Inches(1.0),
                 value, font=FONT_BOLD, size=44, color=color, line_spacing=1.0)
        add_text(slide, x + Inches(2.6), y + Inches(0.3), Inches(3.1), Inches(0.4),
                 sub, font=FONT_BOLD, size=14, color=DARK, line_spacing=1.2)
        add_text(slide, x + Inches(2.6), y + Inches(0.75), Inches(3.1), Inches(1.0),
                 source, font=FONT_REGULAR, size=11, color=SECONDARY,
                 line_spacing=1.35, italic=True)

    add_source_caption(slide,
                       "※  모든 수치는 공개 출처 기반. LGE 내부 환경에서의 실제 효과는 파일럿 그룹 사후 측정 권장. 과장된 예측 배제.")


def slide_12_next_step(prs):
    """슬라이드 12 — Next Step + The Ask (다크)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, DARK)

    add_section_label(slide, Inches(0.7), Inches(0.6), "NEXT STEPS · THE ASK", color=PRIMARY)
    add_title(slide, Inches(0.7), Inches(1.0), Inches(12),
              "2026 Q3-Q4 실행 승인을 요청드립니다",
              size=36, color=WHITE, max_h=2.0)

    asks = [
        ("결정 1", "일정",
         "2026 Q3~Q4 중 14일 확보",
         "트랙별 그룹 편성 유연성 확보"),
        ("결정 2", "규모",
         "그룹당 12-15명 × N회차",
         "개발자 역량 진단 후 라인 배정"),
        ("결정 3", "강사",
         "주강사 1 + 보조강사 1",
         "실습 구간마다 개인별 멘토링"),
    ]

    x = Inches(0.7)
    for label, title, body, footnote in asks:
        add_card(slide, x, Inches(3.0), Inches(3.85), Inches(2.7),
                 GRADIENT_END)
        add_text(slide, x + Inches(0.3), Inches(3.2), Inches(2), Inches(0.4),
                 label, font=FONT_BOLD, size=12, color=PRIMARY, line_spacing=1.0)
        add_text(slide, x + Inches(0.3), Inches(3.55), Inches(3.3), Inches(0.6),
                 title, font=FONT_BOLD, size=22, color=WHITE, line_spacing=1.2)
        add_text(slide, x + Inches(0.3), Inches(4.3), Inches(3.3), Inches(0.6),
                 body, font=FONT_REGULAR, size=14, color=WHITE, line_spacing=1.35)
        add_text(slide, x + Inches(0.3), Inches(5.05), Inches(3.3), Inches(0.6),
                 footnote, font=FONT_REGULAR, size=11, color=MUTED_LIGHT,
                 line_spacing=1.35, italic=True)
        x += Inches(4.05)

    add_rect(slide, Inches(0.7), Inches(6.1), Inches(0.08), Inches(0.6), PRIMARY)
    add_text(slide, Inches(0.95), Inches(6.15), Inches(11), Inches(0.4),
             "다음 단계",
             font=FONT_BOLD, size=12, color=PRIMARY, line_spacing=1.0)
    add_text(slide, Inches(0.95), Inches(6.45), Inches(11.5), Inches(0.5),
             "상세 일정 협의 → 사전 역량 진단 → 교육 확정 → 1주일 전 사전 설치 가이드 → 착수",
             font=FONT_BOLD, size=16, color=WHITE, line_spacing=1.3)

    add_text(slide, Inches(0.7), Inches(7.05), Inches(12), Inches(0.3),
             "모두의연구소  ·  dohee.kim@modulabs.co.kr",
             font=FONT_REGULAR, size=11, color=MUTED_LIGHT, line_spacing=1.2)


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_builders = [
        slide_01_cover,
        slide_02_exec_summary,
        slide_03_why_now,
        slide_04_strategy,
        slide_05_market_evidence,
        slide_06_portfolio,
        slide_07_track1,
        slide_08_track2,
        slide_09_knowledge,
        slide_10_synergy,
        slide_11_impact,
        slide_12_next_step,
    ]

    for i, builder in enumerate(slide_builders, 1):
        builder(prs)
        print(f"  Slide {i:02d}/{len(slide_builders)} built")

    out = "C:\\Users\\Admin\\Downloads\\ai-education-proposal\\projects\\LGE\\CLI_Agentic_심화_제안서\\slides\\LGE_Agentic_AI_제안_CLevel.pptx"
    prs.save(out)
    print(f"\nSaved: {out}")
    print(f"   Slides: {len(prs.slides)}")
    import os
    print(f"   Size: {os.path.getsize(out):,} bytes")


if __name__ == "__main__":
    main()
