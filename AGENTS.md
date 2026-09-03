# AI 교육 제안서 프로젝트

**Generated:** 2026-05-26 | **Commit:** 4d16211 | **Branch:** main

## OVERVIEW
모두의연구소 AI 기업교육 제안서 생성 시스템. 고객 요구사항 → content.json → Jinja2 HTML → Edge Headless PDF. Python + HTML/CSS 템플릿 기반.

## STRUCTURE
```
./
├── build.py              ← 통합 빌드 CLI (content.json → HTML → PDF)
├── templates/            ← Jinja2 HTML 템플릿 + base.css 디자인 시스템
├── schemas/              ← content.json 타입별 예시 (track, module, roadmap, khp-seminar)
├── scripts/              ← validate_content.py (로컬 deterministic 검증)
├── docs/                 ← 가이드 문서 (제안서 생성, 커리큘럼 검토, 리뷰 운영)
├── automation/           ← Slack/n8n/Zapier 자동화 스크립트 (리드 수집)
└── projects/             ← 기업별 산출물 (content.json, PDF, 견적서)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| PDF 빌드 | `build.py` | `python build.py {기업명}` |
| content.json 스키마 | `schemas/*.example.json` | 타입별 4종 |
| 디자인 수정 | `templates/base.css` | 전역 CSS, Pretendard 폰트 |
| HTML 템플릿 | `templates/{type}.html` | track, module, roadmap, khp-seminar, bootcamp, guide |
| 로컬 검증 | `scripts/validate_content.py` | API 비용 없음 |
| 가이드 문서 | `docs/제안서_생성_가이드.md` | 상세 빌드 가이드 |
| 커리큘럼 검토 | `docs/커리큘럼_검토_가이드.md` | 4차원 검토 기준 |
| 리뷰 운영 | `docs/review_governance.md` | 사용자 관리 |
| 견적서 템플릿 | `templates/estimate/template.md` | 견적서 생성용 |
| 자동화 | `automation/` | Slack → n8n → Notion 파이프라인 |

## SLACK 컨텍스트 수집 규칙 (필수)

Slack에서 명령(`/setup`, `/review`, `/build`, `/estimate`)을 받으면 **명령 실행 전에 반드시** 다음 컨텍스트를 수집하세요:

### 1. 스레드 전체 읽기
명령이 스레드 안에서 호출된 경우, `message read` 도구를 사용해 **해당 스레드의 모든 메시지**를 읽습니다:
- `--thread-id`에 부모 메시지의 타임스탬프를 사용
- 봇(TasksCollector)이 작성한 메시지는 제외
- 사람이 작성한 모든 메시지에서 요구사항, 회의 내용, 변경 사항을 추출

### 2. 노션 링크 접근
스레드 메시지에 Notion 링크(`notion.so/` 또는 `notion.site/`)가 포함된 경우:
- Notion MCP 도구를 사용해 해당 페이지 내용을 읽습니다
- 페이지 ID는 URL에서 추출 (예: `https://www.notion.so/페이지명-1c9137efedf6804c98f9ca0ec8745738` → ID = `1c9137ef-edf6-804c-98f9-ca0ec8745738`)
- 노션 내용에서 교육 요구사항, 참가자 정보, 일정 등을 추가로 추출

### 3. 컨텍스트 통합
스레드 메시지 + 노션 페이지 내용을 모두 종합하여 요구사항(`요구조건.md`)을 작성합니다.

### 요구사항 추출 체크리스트
수집한 컨텍스트에서 다음 항목을 반드시 확인:
- [ ] 기업명 (공식 명칭)
- [ ] 교육 대상 (직군, 직급, 인원)
- [ ] 교육 일정 (기간, 차수, 시간)
- [ ] 교육 목표/핵심 키워드
- [ ] 사용 도구 선호 (있는 경우)
- [ ] 예산 범위 (언급된 경우)
- [ ] 특별 요구사항 (산출물, 형태 등)

## CONVENTIONS
- 한글 파일명: `shutil.move()` 사용 (bash mv 금지)
- 인코딩: `PYTHONIOENCODING=utf-8` 필수 (Windows)
- PDF 변환: Edge Headless 모드 (`--headless --no-pdf-header-footer`)
- Jinja2 `autoescape=False` (HTML 그대로 출력)

## PR 워크플로우 (필수)

**main 브랜치에 직접 push 금지. 모든 변경은 Pull Request로.**

각 기업은 **"활성 PR 1개"**를 가질 수 있으며, `/setup → /research → /review → /build → /estimate` 명령이 같은 PR에 커밋으로 누적됩니다. PR이 머지되면 다음 명령 사이클에서 새 PR이 열립니다.

### 규칙

1. **main에 직접 commit/push 절대 금지** (브랜치 보호 + PR 필수)
2. 각 Slack 명령 처리는 **`begin` → 기존 작업 → `finish`** 흐름으로 진행
3. 같은 기업의 열린 PR이 이미 있으면 **새 PR을 만들지 않고** 기존 PR에 커밋 추가
4. `finish`는 허용 파일만 자동 stage (PDF, HTML 렌더, versions/는 강제 제외)
5. **rebase 충돌 시 자동 해결 금지** — 안전하게 abort 후 사용자에게 알림
6. PR 머지는 **리뷰어 승인 후 squash merge** (자동 머지 아직 도입 안 함)

### 실행 흐름

```bash
# 1. 작업 시작 — 브랜치 체크아웃/생성
python scripts/git_workflow.py begin \
  --company {기업명} --command {명령} --author {작업자}

# 2. 기존 작업 수행 (요구조건 작성, content.json 작성, 빌드, 검증, Drive 업로드)
python scripts/validate_content.py {기업명}
python build.py {기업명} --author {작업자} -m "{메시지}"

# 3. 작업 완료 — commit + push + PR 생성/업데이트
python scripts/git_workflow.py finish \
  --company {기업명} --command {명령} --author {작업자} \
  --message "{변경 요약}" \
  --drive-url "https://drive.google.com/drive/folders/{기업폴더ID}" \
  --slack-thread "{Slack 스레드 링크 (있는 경우)}"
```

### 브랜치 명명 규칙

```
proposal/{company_key}/{YYYYMMDD-HHMM}-{command}-{author}

company_key = "c-" + SHA-1(NFC 정규화된 기업명)[:8]
예) proposal/c-a1b2c3d4/20260620-1430-setup-영광
```

한글은 브랜치명에 사용하지 않습니다 (NFC/NFD 이슈, Windows shell 호환성).

### PR 라벨

- `company-{company_key}`: 기업 식별 (같은 기업 열린 PR 찾기)
- `proposal`: 유형 분류

### PR 포함 파일 (자동 필터링)

**포함** (Git 추적 대상):
- `projects/{기업명}/` 아래 확장자 **`.md` `.json` `.csv` `.html`** 전부
  (실제 판정은 `scripts/git_workflow.py` 의 `ALLOWED_EXTENSIONS` 가 담당)
  예: 요구조건.md · content.json · 리서치_*.md · *_견적서.md/.csv ·
      *_이메일_초안.html · 커리큘럼·기획 문서 · 소개자료 HTML

**강제 제외** (자동 stage 안 함):
- `*.pdf` — Drive로만 공유
- `proposal_render.html` — 자동 생성물
- `combined_render.html` — 자동 생성물
- `versions/` — 로컬 빠른 롤백 전용

### 봇 회신에 포함할 링크

```
🔀 GitHub PR: https://github.com/kisdevan/propsal_modulabs/pull/{PR번호}
📂 Google Drive: https://drive.google.com/drive/folders/{기업폴더ID}
📁 Branch Files: https://github.com/kisdevan/propsal_modulabs/tree/{브랜치명}/projects/{기업명}
```

**Drive 링크가 우선** — PDF/HTML 등 최종 산출물은 Drive에서 확인. PR에는 content.json 등 소스만. main에 머지되기 전까지는 Branch Files 링크로 최신 변경을 봐야 함 (main 폴더 링크는 머지 후에만 유효).

### 충돌 처리

- `finish` 실행 시 `git rebase origin/main` 자동 시도
- 충돌 발생 → `git rebase --abort` 후 안전하게 중단, 0이 아닌 exit code 반환
- 사용자에게 "기존 PR 먼저 확인/해결 필요" 메시지 출력
- **절대 강제 push 금지**, **자동 충돌 해제 금지**
- secrets 파일(`.env`, 토큰) 절대 커밋 금지

### CI 자동 검증 (GitHub Actions)

PR이 열리거나 업데이트되면 `.github/workflows/validate-pr.yml`이 실행:
1. 변경된 기업 감지 (git diff)
2. `validate_content.py` 실행 (모든 변경된 content.json)
3. HTML 렌더 smoke test (PDF는 Chrome 의존성 때문에 CI에서 생략)
4. PR 코멘트로 결과 요약

CI 통과 후 리뷰어 1명 승인 → squash merge.

### 커밋 제외 항목 (.gitignore)

- `automation/.env` (토큰 포함)
- `status-worker/` (Cloudflare Worker)
- `.hermes/`, `.omo/`, `.openclaw/`, `.claude/` (AI 에이전트 로컬 상태)
- `versions/` (로컬 빱업 전용)
- `*.pdf`, `proposal_render.html` (자동 생성 산출물)

## COMMANDS
```bash
# PR 워크플로우 (각 Slack 명령 처리 시 필수)
python scripts/git_workflow.py begin --company {기업명} --command {명령} --author {작업자}
python scripts/git_workflow.py finish --company {기업명} --command {명령} --author {작업자} \
    --message "{요약}" --drive-url "{Drive 링크}"
python scripts/git_workflow.py status --company {기업명}    # 열린 PR 조회

# 빌드/검증
python build.py {기업명} --author {작업자}   # 기업 전체 제안서 빌드 (버전 스냅샷 포함)
python build.py {기업명}/{과정명}            # 단일 제안서 빌드
python build.py --all                       # 전체 빌드
python build.py {기업명} --no-drive-upload --no-version-snapshot  # CI/로컬 테스트용
python scripts/validate_content.py {기업명} # 로컬 검증
python scripts/version_manager.py list projects/{기업명}  # 버전 히스토리 확인
```

## 전체 워크플로우

고객 요구사항이 들어오면 **4단계 명령어**로 진행합니다:

```
/setup {기업명}    → Step 1-3: 요구조건 + content.json + PDF 빌드
/research {기업명} → 기업 리서치 + 커리큘럼 초안 생성 (client-research-md 스킬 활용)
/review {기업명}   → Step 3.5: 4차원 커리큘럼 검토 (content.json 수정 후, 빌드 전)
/build {기업명}    → Step 4: PDF 재빌드 (수정 후)
/estimate {기업명} → Step 5: 견적서 + CSV + 이메일 초안
```

자연어로도 호출 가능합니다:
- "삼성전자 커리큘럼 초안 뽑아줘" → `/research 삼성전자`와 동일
- "기웅정보통신 제안서 만들어줘" → `/setup 기웅정보통신`과 동일
- "삼성전자 커리큘럼 검토해줘" → `/review 삼성전자`와 동일

**각 단계 완료 후 다음 단계를 안내하세요.** 사용자가 별도 지시 없으면 자연스럽게 다음 스텝을 제안합니다.

### 진행 가이드

| 현재 상태 | 안내할 내용 |
|---|---|
| 요구조건 작성 완료 | "content.json 작성할까요? `/setup`으로 계속 진행합니다." |
| content.json 작성 완료 | "커리큘럼 검토할까요? `/review`로 4차원 검토합니다." |
| 커리큘럼 검토 완료 (PASS) | "PDF 빌드할까요?" → build 실행 후 미리보기 |
| PDF 생성 완료 | "견적서와 이메일 초안 만들까요? `/estimate`로 진행합니다." |
| 견적서 + 이메일 완료 | "전체 산출물이 준비되었습니다. 폴더 열어볼까요?" |

### 최종 산출물

```
projects/{기업명}/
├── 요구조건.md
├── {기업명}_AI교육_견적서.md          ← 참고용
├── {기업명}_AI교육_견적서.csv         ← 스프레드시트용
├── {기업명}_AI교육_이메일_초안.html    ← Gmail 붙여넣기용
└── 제안서/
    ├── content.json
    ├── proposal_render.html
    └── [모두의연구소]{기업명}_AI교육_제안서.pdf
```

## 템플릿 선택

| 케이스 | 템플릿 | content.json 키 |
|---|---|---|
| 다중 주제/직군 교육 | **track** (가장 많이 사용) | `tracks` |
| 단일 과정 모듈형 | module | `modules` |
| **[K-HP] 기업교육 세미나 전용** | **khp-seminar** | `seminars` |
| 연간 로드맵 | roadmap | `steps` |
| 부트캠프 상세 | bootcamp | `type: "bootcamp"` |

> ⚠️ **`seminars` / `khp-seminar.html`은 K-HP 사업 기반 제안서 전용입니다.** 헤더에 "K-HP 사업 기반 AI 기업교육 제안"이 포함됩니다. 대학 세미나, 일반 기업 세미나는 `tracks` + `track.html`을 사용하세요.

## 도구 일관성 규칙

content.json의 **3곳**에 도구가 명시됩니다. 반드시 일치해야 합니다:

1. **`tech_stack`** — 모든 Track tools의 합집합
2. **`tracks[].tools`** — 해당 Track에서 실제 사용하는 도구
3. **`modules[].items`** — 본문에서 언급하는 도구

content.json 작성 후 반드시 교차 검증하세요.

## 견적서 단가 규칙

- **기본 단가**: ₩600,000/시간
- **할인** (최대 ₩450,000): 차수 많음 (6회+), 예산 규모 큼 (~4억), 확장 가능성
- **보조강사**: 1명당 +₩100,000/시간
- **재료비**: AI 서비스 사용료 포함 가능
- **주강사 기준**: 주강사 비용이 단가 30% 미만이면 전체 단가 인하 검토

## 이메일 초안 규칙

- **비즈니스 커버 메일** 톤 — 간결, 정중
- 견적 상세 테이블 넣지 않음 (첨부파일에 있음)
- 인사말 → 첨부 안내 → 한 줄 요약 → 일정 협의 → 서명
- 서명: 모두의연구소 · 비즈팀 · modu.biz@modulabs.co.kr — **담당자 개인 이름·개인 메일·휴대폰 번호는 넣지 않는다** (개인정보 규칙)
- HTML 인라인 스타일 (Gmail 호환)

## 타이틀 작성 가이드

대상에 맞는 톤을 사용:
- **기업**: "비개발자 맞춤형 AI 실무 교육", "AI 도입 역량 강화"
- **대학**: "AI 스킬업 프로그램", "AI 활용 역량 강화 프로그램"
- "비개발자", "실무" 등은 기업 대상에만 사용

## 알려진 이슈 & 해결법

| 이슈 | 해결법 |
|---|---|
| Windows 인코딩 에러 | `PYTHONIOENCODING=utf-8` 필수 |
| PDF 파일명 중복 | Python shutil로 rename |
| Acrobat 파일 락 | `taskkill //F //IM Acrobat.exe` |
| 한글 파일명 깨짐 | bash mv 대신 Python shutil 사용 |
| Track 번호 위첨자 | `use_simple_track_label: false` 설정 |
| Track 간격 좁음 | base.css 여백 증가 (이미 수정됨) |

## 참조 문서
- 상세 가이드: `docs/제안서_생성_가이드.md`
- 커리큘럼 검토 가이드: `docs/커리큘럼_검토_가이드.md`
- 리뷰 운영 의사결정: `docs/review_governance.md` (사용자 관리)
- 리뷰어 자동 실행 프롬프트: `docs/review_agent_prompts.md` (Codex 관리)
- 로컬 검증 스크립트: `scripts/validate_content.py` (API 비용 없음)
- 견적서 템플릿: `templates/estimate/template.md`
- 견적서 참고 양식: `templates/estimate/references/`
- 기존 사례: `projects/` 디렉토리 내 각 기업 폴더

## 커리큘럼 다차원 검토 (/review)

### 워크플로우

```
/review {기업명}  → 4명의 전문 검토 에이전트 병렬 실행
  ├── Flow Reviewer       → 모듈 순서, 시간 배분, 선행학습, 산출물 연결
  ├── Recency Reviewer     → 도구 최신성, 트렌드 정확성, 버전 확인
  ├── Tone Reviewer        → 대상 맞춤 톤, 도구 일관성, 포맷 통일
  └── Readability Reviewer → PDF 렌더링, 텍스트 길이, 페이지 분할
```

### 실행 규칙

1. `scripts/validate_content.py`로 로컬 deterministic 검증을 먼저 실행 (API 비용 없음)
2. **4개 에이전트를 반드시 병렬로 실행** (순차 실행 금지)
3. 각 에이전트는 content.json을 읽고 독립적으로 판단
4. 결과를 취합하여 종합 판정 도출
5. FIX/WARN 항목은 단순 결과가 아니라 **영향과 수정 선택지**를 함께 제시
6. 사업적 판단이 필요한 항목은 `docs/review_governance.md` 기준으로 사용자에게 결정 요청
7. 사용자가 수정하면 `/review` 재실행 또는 `/build` 진행

### 검토 상세 기준
→ `docs/커리큘럼_검토_가이드.md` 참조

### 종합 판정 규칙

| 조건 | 판정 | 다음 액션 |
|------|------|-----------|
| FIX 1개 이상 | ❌ NEEDS_FIX | 사용자 수정 후 재검토 |
| WARN 3개 이상 | ❌ NEEDS_FIX | 사용자 확인 후 수정 권장 |
| WARN 1-2개 | ⚠️ PASS_WITH_NOTES | `/build` 진행 가능 |
| WARN 0개 | ✅ PASS | 즉시 `/build` 진행 |

## 기업 리서치 + 커리큘럼 초안 (/research)

`/research {기업명}` 또는 자연어("커리큘럼 초안 뽑아줘") 호출 시 실행.

### 워크플로우

1. **스레드 컨텍스트 수집** (위 SLACK 컨텍스트 수집 규칙에 따라)
2. **웹 검색 리서치** (5개 영역, 각 2~3회 검색):
   - 기업 개요 (업종, 규모, 매출, 주요 사업)
   - AI 도입 현황 (현재 AI 활용 수준, 사용 중인 툴)
   - 조직 구조 및 직무 (채용공고 분석, AI 교육 우선 타겟 직군)
   - 최근 뉴스·전략 방향 (최근 6~12개월)
   - 경쟁사 AI 동향 (동종업계 트렌드)
3. **마크다운 리포트 생성** → `projects/{기업명}/리서치_{기업명}.md` 저장
4. **커리큘럼 초안 생성** — 리서치 결과 + 스레드 요구사항을 종합하여 `projects/{기업명}/제안서/content.json` 초안 작성
5. 완료 안내: "리서치 완료. `/review`로 커리큘럼 검토하거나, `/build`로 바로 PDF 생성 가능"

### 리서치 리포트 템플릿

```
## 기업 리서치 리포트: {기업명}
> 작성 목적: AI 교육 제안서 준비용 | 작성일: {날짜}

### 1. 기업 개요 (업종, 설립, 규모, 주요 사업)
### 2. AI 도입 현황 (활용 수준, AI 툴, 디지털전환 단계)
### 3. 조직 구조 및 직무 (부서 구성, AI 교육 우선 타겟)
### 4. 최근 전략 방향 (핵심 이슈, AI 관련 투자)
### 5. 경쟁사 AI 동향 (업계 트렌드, 상대적 위치)
### 6. AI 교육 제안 핵심 인사이트 (타겟 Track, 제안 포인트, 리스크)
### 📎 주요 출처 (공식 홈페이지 필수 포함)
```

### 운영 원칙
- 불확실한 정보는 `[추정]` / `[미확인]` 표시
- 출처는 말미 "주요 출처" 섹션에 하이퍼링크로 정리
- 고객사 공식 홈페이지 출처 필수 포함
- 최근 1~2년 자료 우선

## 커리큘럼 스키마 설계 (필수 단계)

`schemas/*.example.json`은 **참고용 템플릿**이지 고정 형식이 아닙니다. 각 교육과정의 페다고지와 구조에 맞춰 **스키마를 재설계**합니다. 기존 example을 그대로 복사하지 마세요.

### 왜 재설계 단계가 필요한가

기본 템플릿들은 단기 직무 교육용으로 설계되어 있습니다:
- `track.example.json` — 직무별 1일(7H) 워크샵
- `module.example.json` — 개발자/IT 단일 모듈 과정
- `roadmap.example.json` — 연간 로드맵
- `khp-seminar.example.json` — K-HP 세미나

다음 경우에는 **스키마 자체를 재설계**해야 합니다:
- 멀티 트랙 순차 과정 (예: 3주 심화 + 분기 분산)
- 학습-적용-회고 사이클 (강의주 + 현업 적용주 교대)
- 페다고지 중심 심화 (보안 통제, 운영化, 기여도 측정 등)
- 산업/조직 맞춤형 (금융/제조/공공/사내AX 특화)

### 재설계 워크플로우

#### 1. 페다고지 1문장 정의
- "학습-적용-회고 사이클로 분기 분산 3주 심화"
- "단일 직무 1일 집중 워크샵"
- "수준별 5주 코스"

#### 2. 구조 결정
- 트랙 수 (단일 / 멀티 순차 / 멀티 병렬)
- 모듈 수와 단위 (1일 / 5일 / 주 단위)
- 현업 과제 유무 (강의주 사이 과제)
- 통제 모델 / 산출물 레이어

#### 3. 필드 재설계
기본 스키마에서:
- **제거**: 단기 직무 교육에만 의미 있는 필드
- **추가**: 페다고지 구현에 필요한 필드 (예: `learning_cycle`, `inter_session_assignments`, `controls`, `phases`)
- **재해석**: 기존 필드를 새 구조로 (예: `tracks[]` → Week A/B/C, `modules[]` → Day 1~5)

#### 4. `validate_content.py` deterministic 검증 유지
스키마를 바꿔도 기계 검증은 통과해야 합니다:
- `module_name` 15자 이하
- 모듈당 `items` 4개 이하
- `item` 문장 100자 이하
- `tech_stack` = `tracks[].tools` 합집합
- `intro` / `objective` / `schedule_message` HTML 태그 균형

#### 5. (선택) docs에 명시
재설계된 필드/구조가 재사용되면 `schemas/`에 새 example 등록 + `docs/제안서_생성_가이드.md`에 기록.

### 사례: 사내AX 자율 에이전트 보안 3주 심화 (Hermes 기반)

- **페다고지**: 학습-적용-회고 사이클 (분기 분산)
- **재설계 내역**:
  - `info.duration` → "5일 × 7시간 × 3주 (총 105시간) · 분기당 1주 × 3회 + 6주 현업 적용"
  - `info.ax_stage` → "단일 에이전트 → 다중 프로필 통제 → 팀 운영化" (3단계 진행)
  - `tracks[]` → Week A/B/C (Month 1/2/3) 순차 이수
  - `modules[]` → Day 1~5 (총 15 모듈)
  - `design_framework` 안에 **5-Layer (Identity/Tenancy · Allowlist · Arg/Data · Sandbox · Audit & Value Extraction)** 별도 하위 섹션으로 배치
  - `objective`에 "에이전트 기여도 데이터 산출" 항목 추가 (단순 기술 산출물이 아니라 가치 산출 명시)
- **유지**: 기본 골격 필드(title/subtitle/info/intro/objective/tech_stack/infrastructure/tracks/output/schedule_message)는 `build.py` 호환성 위해 보존

### 흔한 오해

**Q. track.example.json 그대로 쓰면 안 되나요?**
A. 단일 직무 1일 과정이면 OK. 3주+ 멀티 트랙, 학습-적용-회고, 산업 맞춤형이면 재설계하세요.

**Q. 스키마 재설계하면 build.py가 깨지지 않나요?**
A. `build.py`는 트랙 타입 기본 골격 필드를 기대합니다. 이 기본 골격은 유지하되, **내부 값과 하위 구조(modules, items, design_framework 내용)**를 재설계하세요.

**Q. 수준별 AI 리터러시 과정도 재설계해야 하나요?**
A. 아니요. 직군별 1일 워크샵, 수준별 5주 리터러시는 track.example/module.example이 그대로 맞습니다. 재설계는 **페다고지가 example과 다를 때만**.

## 버전 관리

### 개요

여러 사용자가 동시에 작업하므로, 빌드/수정 전 기존 산출물을 자동으로 버전 스냅샷으로 저장합니다. 덮어쓰기 대신 버전 히스토리가 쌓입니다.

### 버전 형식

```
v{NNN}_{작업자}_{YYYYMMDD}_{HHMM}
예: v001_영광_20260609_1430, v002_은숙_20260609_1530
```

### 디렉토리 구조

```
projects/{기업명}/
├── 제안서/                          ← 항상 최신 (working copy)
│   ├── content.json
│   ├── proposal_render.html
│   └── *.pdf
├── versions/                        ← 버전 히스토리
│   ├── v001_영광_20260609_1430/
│   │   ├── meta.json               ← {version, author, timestamp, description, files}
│   │   ├── 제안서/
│   │   │   ├── content.json
│   │   │   ├── proposal_render.html
│   │   │   └── *.pdf
│   │   ├── {기업명}_AI교육_견적서.md
│   │   └── ...
│   └── v002_은숙_20260609_1530/
│       └── ...
├── 요구조건.md                      ← 버전 관리 제외 (입력 파일)
└── 리서치_{기업명}.md               ← 버전 관리 제외 (참고 파일)
```

### 작동 방식

1. `/build` 실행 → `build.py --author {작업자}` 호출
2. `version_manager.snapshot()`이 기존 산출물을 `versions/v{NNN}_{작업자}_{날짜}_{시간}/`에 복사
3. 새 파일 생성 (working copy 업데이트)
4. 버전 히스토리 출력

### 사용자 매핑

| Slack User ID | 이름 |
|---------------|------|
| U0924H9HSK1 | 영광 |
| U03RP0HEZDW | 은숙 |
| U093RP4EZMK | 은경 |

### 빌드 명령어

```bash
python build.py {기업명} --author {이름 또는 Slack ID}
python build.py {기업명} --author U03RP0HEZDW -m "2차 수정"
python build.py {기업명} --author 은숙 -m "견적서 업데이트"
```

### 버전 관리 제외 항목

- `요구조건.md` (입력 파일)
- `리서치_{기업명}.md` (참고 파일)
- `versions/` 폴더 자체
- 숨김 파일 (`.git`, `.claude` 등)

### 버전 확인

```bash
python scripts/version_manager.py list projects/{기업명}
python scripts/version_manager.py latest projects/{기업명}
```

## 작업 위생 규칙 (2026-08 추가)

1. **작업 시작 전 반드시 동기화**
   ```bash
   git fetch origin --prune && git switch main && git merge --ff-only origin/main
   ```
   → 이 규칙이 없어 로컬 `main`이 `origin/main`보다 **35 커밋 뒤처진** 사례가 있었다 (2026-08-24 실측).
2. **병합 후 브랜치 삭제** — squash merge 직후 로컬·원격 삭제.
   주 1회 `git branch --merged origin/main` 으로 정리.
3. **개행은 `.gitattributes`가 관리** — `core.autocrlf`를 개인이 바꾸지 않는다.
4. **worktree는 사용 후 정리** — `git worktree prune` + 디렉터리 삭제.
   방치 시 저장소가 수 GB 단위로 비대해진다 (2026-08-24 실측 **6.66GB**).
5. **`.git/index.lock` 이 남아 있으면 즉시 확인** — 실행 중 git 프로세스가 없는데도
   lock이 남아 있으면 모든 커밋이 조용히 실패한다.
   `2026-08-21 16:47` 생성된 0바이트 lock이 3일간 방치되어 미커밋이 쌓인 사례가 있다.
   ```bash
   ls -la .git/index.lock && ps aux | grep -c "[g]it"   # 프로세스 없으면 rm -f .git/index.lock
   ```
