---
name: curriculum-intro
description: "가로형(A4 landscape) 교육과정 소개자료 HTML/PDF 생성 스킬. 커버→트랙 상세→클로징까지 섹션 카드를 고객사 커리큘럼에 맞춰 자유 조합하되, 디자인은 parent.css + 컴포넌트 라이브러리로 100% 재현한다. 다음 상황에 반드시 이 스킬을 사용하세요: - '교육과정 소개자료', '커리큘럼 소개 페이지', '가로형 제안서', '3트랙 소개' 등 가로(H landscape) 형태의 교육과정 안내 문서 요청 - 롯데이커머스 3트랙 소개자료 스타일 재현 요청 - 미팅용/사전 공유용 커리큘럼 요약 문서 (정식 세로 제안서는 build.py 시스템 사용, 발표 슬라이드는 modu-slide 사용)"
---

# Curriculum Intro — 가로형 교육과정 소개자료

## 포지셔닝 (다른 시스템과 구분 — 절대 혼용 금지)

| 시스템 | 형태 | 용도 |
|---|---|---|
| `build.py` + `templates/*.html` | 세로 A4 PDF | 정식 제안서 (계약 문서) |
| `modu-slide` 스킬 | 16:9 인터랙티브 덱 | 강의·세미나 화면 발표 |
| **curriculum-intro (이 스킬)** | **가로 A4 문서** | **미팅·공유용 커리큘럼 소개** |

## 아키텍처 (3계층 — 재현성의 원천)

```
1. parent.css        ← 디자인 시스템 전체. 통째 복사. 값 수정 금지.
2. 컴포넌트 라이브러리  ← 12종 정규 스니펫. 신규 발명 금지.
3. 섹션 조합          ← 고객사마다 자유 설계 (유일한 가변 계층)
```

**파일 위치** (repo 루트 기준):
- `templates/curriculum-intro/parent.css` — 부모 CSS
- `templates/curriculum-intro/components.md` — 컴포넌트 라이브러리 (계약서)
- `templates/curriculum-intro/golden/롯데이커머스_3트랙_교육과정_소개.html` — 골든 샘플 (스타일 기준)

> 스킬은 repo 내에서 실행한다고 가정한다. 경로가 없으면 사용자에게 위치 확인 후 진행.

---

## 워크플로우

### Step 0 — 트리거 확인

이 스킬은 **가로형 소개자료**에만 쓴다. 요청이 세로 제안서면 기존 `build.py` 흐름으로, 발표 슬라이드면 `modu-slide`로 안내를 바꾼다.

### Step 1 — 입력 수집

프로젝트 폴더(`projects/{기업명}/`)의 `요구조건.md`, `리서치_{기업명}.md`, 기존 `제안서/content.json`이 있으면 먼저 읽는다. 없으면 대화에서 추출한다:

| 필수 | 선택 |
|---|---|
| 기업명 · 교육 대상(직군/인원) | 고객사 브랜드 컬러 (기본: 모연 레드 유지) |
| 트랙/과정 구조와 시간 | 도구 스택 (Gemini/Claude/GPT 등) |
| 각 과정의 일차·모듈 구성 | 운영 차수 정보 (대규모일 때) |
| 핵심 메시지/강조점 | PDF 필요 여부 (기본: HTML+PDF 둘 다) |

부족한 정보는 **한 번에 모아서** 질문한다.

### Step 2 — 섹션 설계 제안 (구조 재구성 단계)

아키타입 조합표(`components.md` 하단)로 목차를 설계하고 사용자에게 보여준다:

```
COVER → OVERVIEW → [TRACK-GROUP | TRACK-DETAIL]* → [OPERATION] → CLOSING
```

- 과정 1개: `COVER + TRACK-DETAIL 1 + CLOSING` (3장)
- N트랙 M과정: `COVER + OVERVIEW + (TRACK-GROUP + TRACK-DETAIL×M) + OPERATION? + CLOSING`
- 섹션 수 = 자동 = 인쇄 페이지 수. 채번(01/02/…)은 조립 순서대로.

### Step 3 — HTML 조립

1. `templates/curriculum-intro/parent.css`를 **통째로** 읽어 `<style>`에 인라인 (값 수정 금지).
2. 컴포넌트는 `components.md` 스니펫을 복사해 내용만 교체.
3. 저장: `projects/{기업명}/{기업명}_{구성}_교육과정_소개.html` (예: `{기업명}_3트랙_교육과정_소개.html`)

**변수 vs 고정 (재현성 계약):**

| 고정 (절대 수정 금지) | 변수 (고객사마다 변경) |
|---|---|
| parent.css의 모든 값 (색·폰트·간격·radius·shadow) | 기업명, 날짜, 커버 메타 |
| 컴포넌트의 HTML 구조·클래스명 | 메시지 카피 (kicker/h2/lead) |
| Pretendard CDN v1.3.9 링크 | 트랙·과정 수, 일차·모듈 구성 |
| 섹션=1페이지 print 규칙 | 산출물, 직군, 운영 차수 |
| sign 비즈팀 공용 서명 1줄 (개인 연락처 금지) | 테마 스왑 시 `--primary` 계열 토큰만 |

### Step 4 — 데이터 정합성 검증

- [ ] 표기 총시간(커버/sumrow) = 각 과정 시간의 합
- [ ] 각 daycard 모듈 시간 합 = `.dhh` 시간
- [ ] prop-table `rowspan` 수 = 해당 트랙 과정 수
- [ ] sec-num 연번 겹침/누락 없음
- [ ] op-table 인원 합 = tot 행, 차수 산정 = ceil(인원/반규모)

### Step 5 — PDF 변환 (검증된 커맨드)

**반드시 `--headless=new`** 를 쓴다 (구형 `--headless`는 `@page` landscape를 무시해 세로로 나옴 — repo 알려진 이슈):

```bash
# Windows PowerShell (repo 루트 기준)
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (!(Test-Path $edge)) { $edge = "C:\Program Files\Microsoft\Edge\Application\msedge.exe" }
$src  = (Resolve-Path "projects\{기업명}\{파일명}.html").Path
$out  = (Join-Path (Split-Path $src) "{기업명}_교육과정_소개.pdf")
& $edge --headless=new --disable-gpu --no-pdf-header-footer "--print-to-pdf=$out" "file:///$($src -replace '\\','/')"
```

검증 방법: PDF 바이트에서 MediaBox 확인 → `841.92 594.96`(=A4 가로)이면 성공.

```bash
python -c "import pathlib,re; d=pathlib.Path(r'{pdf경로}').read_bytes(); print(set(re.findall(rb'/MediaBox\s*\[([^\]]+)\]',d)))"
```

기대값: `{b'0 0 841.91998 594.95996'}` — 세로 값(`595.x 841.x`)이 나오면 `--headless=new` 누락 여부를 확인.

### Step 6 — 품질 체크리스트 & 완료

- [ ] `<style>`에 parent.css가 **전체** 인라인 (외부 CSS 링크 없음 — 파일 공유 전제)
- [ ] Pretendard CDN 링크 존재
- [ ] COVER가 첫 장, CLOSING이 마지막 장
- [ ] 컴포넌트를 라이브러리 외에서 변형·발명하지 않았음
- [ ] `hl` mchip은 섹션당 1개 이하
- [ ] 본문 강조는 `<b>` 사용, 이모지는 커버 badge에만
- [ ] PDF 페이지 수 = 섹션 수 (넘치면 daycard 모듈 정리 — 카드당 5개 이하)
- [ ] 골든 샘플(`templates/curriculum-intro/golden/`)과 나란히 띄워 스타일 육안 대조

완료 안내 예: "가로형 소개자료 생성 완료 (총 N페이지). PDF: `{경로}` · 다음으로 견적서가 필요하면 `/estimate`로 진행합니다."

---

## 금지사항 (반칙 목록)

1. parent.css 값을 "개선"하지 않는다 — 여백·색·폰트 크기 조정은 전부 금지.
2. 컴포넌트를 새로 만들지 않는다 — 필요하면 사용자에게 보고 후 `components.md`에 등록하고 쓴다.
3. 인라인 style로 레이아웃을 임의 조정하지 않는다 (골든에 있는 보조 인라인 `margin-bottom:22px` 등 관례 스타일은 제외).
4. 세로 제안서 흐름(info-grid, section-block 등 build.py 클래스)을 가져오지 않는다.
5. `--headless`(구형)로 PDF를 만들지 않는다 — 세로로 출력된다.
6. 생성물을 `templates/`에 저장하지 않는다 — 산출물은 항상 `projects/{기업명}/`.

## 유지보수

- 스타일 개선 제안은 parent.css를 직접 고치지 말고 PR로 — 골든 샘플과의 diff 검증 후 반영.
- 새 컴포넌트 추가 시: components.md에 스니펫+사용처 등록 → parent.css에 필요 CSS 추가(값 보존 원칙) → 골든 샘플은 갱신하지 않음(원본 기준 유지).
