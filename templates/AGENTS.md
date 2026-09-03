# 템플릿 (templates)

**Generated:** 2026-05-26 | **Commit:** 4d16211

## OVERVIEW
Jinja2 HTML 템플릿 + CSS 디자인 시스템. content.json → HTML 렌더링에 사용되는 모든 템플릿.

## STRUCTURE
```
templates/
├── base.css              ← 전역 CSS 디자인 시스템 (Pretendard 폰트)
├── base-landscape.css    ← 가로(A4 Landscape) 오버라이드 레이어 (orientation: landscape 시 base.css 뒤에 주입)
├── track.html            ← 다중 직군 트랙형 (가장 많이 사용)
├── module.html           ← 단일 모듈형 (개발자/IT)
├── roadmap.html          ← 로드맵형 (연간 계획)
├── khp-seminar.html      ← K-HP 세미나 전용
├── bootcamp.html         ← 부트캠프 상세
├── guide.html            ← 교육 안내서
├── estimate/             ← 견적서 템플릿 + 참고 양식
├── generate_template.py  ← 템플릿 자동 생성 스크립트
└── 모두의연구소 로고 모음/  ← 로고 에셋
```

## WHERE TO LOOK
| Task | File |
|------|------|
| 디자인 전역 수정 | `base.css` (Primary: #EE3E4C, Secondary: #EBBAC0) |
| 트랙형 템플릿 | `track.html` |
| 모듈형 템플릿 | `module.html` |
| 로드맵 템플릿 | `roadmap.html` |
| K-HP 세미나 | `khp-seminar.html` (K-HP 전용, 일반 기업엔 사용 금지) |
| 견적서 | `estimate/template.md`, `estimate/references/` |
| CSS 변수 | `base.css` 상단 컬러 정의 |

## CONVENTIONS
- Jinja2 변수 접근: `{{ data.field }}` (dict dot notation)
- `autoescape=False` — HTML 태그 그대로 출력 (`output`, `schedule_message` 필드)
- CSS 수정은 `base.css` 하나에서 전체 제어 (기업별 분리 불가)
- Pretendard 폰트 CDN 사용
- PDF 렌더링: Edge Headless → CSS `@page` 설정 무시, `--no-pdf-header-footer` 플래그
- 가로 PDF: content.json에 `"orientation": "landscape"` → `base-landscape.css` 자동 주입 (`@page size: A4 landscape` + 폭 확장). **Chrome 필수** — Edge는 `@page` 무시로 세로 출력됨. 상/하 여백은 `@page margin`이 담당 (body padding 상/하는 첫/마지막 페이지에만 적용되므로 사용 금지). track 템플릿으로만 시각 검증됨

## TEMPLATE → JSON KEY MAPPING
| 템플릿 | content.json 키 | 판별 로직 (`build.py:detect_template_type`) |
|--------|-----------------|---------------------------------------------|
| `track.html` | `tracks` | `"tracks" in data` |
| `module.html` | `modules` | `"modules" in data` |
| `roadmap.html` | `steps` | `"steps" in data` |
| `khp-seminar.html` | `seminars` | `"seminars" in data` |
| `bootcamp.html` | `type: "bootcamp"` | `data.get("type") == "bootcamp"` |
| `guide.html` | `type: "guide"` | `data.get("type") == "guide"` |

## ANTI-PATTERNS
- **DO NOT** `khp-seminar.html`을 일반 기업/대학에 사용 — 헤더에 "K-HP 사업 기반" 포함
- **DO NOT** CSS를 개별 템플릿에 인라인 — `base.css`에서만 관리
- **DO NOT** 템플릿에서 `{{ css }}` 외부 변수명 변경 — `build.py`에서 주입

## DESIGN SYSTEM
| 변수 | 값 | 용도 |
|------|-----|------|
| Primary | `#EE3E4C` | 포인트 컬러 (빨강) |
| Secondary | `#EBBAC0` | 섹션 번호 (라이트 핑크) |
| Border | `#EBEBEB` | 박스 테두리 |
| Text Dark | `#111111` | 제목 |
| Text Body | `#333333` | 본문 |
