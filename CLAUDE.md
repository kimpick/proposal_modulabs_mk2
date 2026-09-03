# AI 교육 제안서 프로젝트

## 프로젝트 개요
모두의연구소 AI 기업교육 제안서 생성 시스템. 고객 요구사항을 받아 제안서(PDF)와 견적서를 생성합니다.

## 전체 워크플로우

고객 요구사항이 들어오면 **4단계 명령어**로 진행합니다:

```
/setup {기업명}    → Step 1-3: 요구조건 + content.json + PDF 빌드
/review {기업명}   → Step 3.5: 4차원 커리큘럼 검토 (content.json 수정 후, 빌드 전)
/build {기업명}    → Step 4: PDF 재빌드 (수정 후)
/estimate {기업명} → Step 5: 견적서 + CSV + 이메일 초안
```

**선택 명령어**: `/add-instructor-recommendation {기업명}` + 이력서 첨부 → 추천 강사 후보군 카드 섹션 추가 (`.claude/skills/add-instructor-recommendation/SKILL.md` 참조)

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

## 요구조건 버전 관리

요구조건은 회의·이메일 변경마다 바뀔 수 있어 파일 기반 버전 관리를 합니다.

### 폴더 구조
```
projects/{기업명}/
├── 요구조건.md              ← 항상 최신 버전 (단일 진실)
├── 요구조건_history/
│   ├── v1_YYMMDD.md         ← 날짜 기반 아카이브
│   └── v2_YYMMDD.md
└── [회의록]*.md              ← 원본 변경 출처 (그대로 보존)
```

### 프로세스
1. 요구조건 변경 요청(회의록/이메일)이 들어오면 **먼저** 현재 `요구조건.md`를 `요구조건_history/v{N}_{YYMMDD}.md`로 이동 — Python `shutil.move` 사용 (한글 파일명 안전)
2. 새 `요구조건.md`를 작성하고 상단에 **버전 이력 표** 포함
3. 원본 회의록·이메일은 `projects/{기업명}/` 루트에 그대로 보존 (아카이브 이동 금지)
4. 제안서도 함께 업데이트해야 하면 **날짜 기반 새 폴더**(`제안서_YYMMDD/`)로 생성하고 기존 폴더는 보존 — 제안서 자체가 폴더명으로 버전 관리됨

### 버전 이력 표 템플릿
요구조건 문서 상단에 다음 형식으로 포함:

```markdown
## 버전 이력

| 버전 | 일자 | 주요 변경 | 출처 |
|---|---|---|---|
| v2 | YYYY-MM-DD | 변경 내용 요약 | [출처 파일](파일명.md) |
| v1 | YYYY-MM-DD | 초기 요구조건 | [v1 아카이브](요구조건_history/v1_YYMMDD.md) |
```

## 고객사 기억 (필수 선행 단계)

`projects/` 폴더는 **회차/건 단위**로 쪼개져 있어 한 고객사가 여러 폴더에 흩어져 있습니다 (삼성전자 MX사업부 10개 폴더, 공영홈쇼핑 4개 폴더 등). 폴더만 보고 작업하면 과거 합의를 놓칩니다.

### 작업 시작 전

1. `memory/clients/_INDEX.md`에서 **폴더 → 고객사**를 확인합니다. 매핑에 없으면 폴더명 = 고객사명.
2. `memory/clients/{고객사}.md`를 **읽습니다.** 없으면 `memory/clients/_TEMPLATE.md`를 복사해 만듭니다.
3. 해당 폴더에 `MEMORY.md`가 있으면 함께 읽습니다.

### 작업 종료 후

- 회차가 끝나도 남을 맥락(담당자 성향, 확정 조건, 통한 것/거절 사유, 선호 포맷) → `memory/clients/{고객사}.md`
- 이번 회차의 경과·결정·대기 건 → `projects/{폴더}/MEMORY.md` (`memory/clients/_TEMPLATE_project.md` 복사)

### 파일 역할 구분 (중복 금지)

| 파일 | 담는 것 |
|---|---|
| `memory/clients/{고객사}.md` | 고객사 단위 **장기 기억** — 회차가 바뀌어도 유지되는 것 |
| `projects/{폴더}/MEMORY.md` | 이 회차의 **진행 경과·결정·대기 건** |
| `projects/{폴더}/context.md` | 제안 설계 입력 — 배경·대상·제약 (기존 관례 유지) |
| `projects/{폴더}/요구조건.md` | 확정 요구조건 (버전 관리 대상) |
| Notion 「영업/제안현황」 DB | 계약·단가·매출·실적 **확정 사실의 원본** |
| `memory/YYYY-MM-DD-HHMM.md` | OpenClaw 자동 세션 로그 — 손대지 않음 |

> 기억 파일의 모든 항목에 `[출처: 파일 또는 날짜]`를 답니다. 확인 안 된 내용은 **`(미확인)`** 으로 표시하고 사실처럼 쓰지 않습니다.
> ⚠️ 고객사 파일의 §4(확정된 조건)는 CLAUDE.md 기본 규칙을 **덮어씁니다**. 예: 삼성전자 MX는 보조강사를 직접 섭외하므로 견적에 보조강사비를 넣지 않습니다.

## 템플릿 선택

| 케이스 | 템플릿 | content.json 키 |
|---|---|---|
| 다중 주제/직군 교육 | **track** (가장 많이 사용) | `tracks` |
| 단일 과정 모듈형 | module | `modules` |
| **[K-HP] 기업교육 세미나 전용** | **khp-seminar** | `seminars` |
| 연간 로드맵 | roadmap | `steps` |
| 부트캠프 상세 | bootcamp | `type: "bootcamp"` |

> ⚠️ **`seminars` / `khp-seminar.html`은 K-HP 사업 기반 제안서 전용입니다.** 헤더에 "K-HP 사업 기반 AI 기업교육 제안"이 포함됩니다. 대학 세미나, 일반 기업 세미나는 `tracks` + `track.html`을 사용하세요.

### 가로(A4 Landscape) 버전

커리큘럼 가독성이 필요할 때 content.json에 `"orientation": "landscape"` 추가 → `templates/base-landscape.css` 자동 적용. 기존 세로 제안서 무영향(opt-in). **Chrome 필수** (Edge는 `@page` 무시 → 세로로 출력). track 템플릿으로만 시각 검증됨.

## 타겟별 기본 프리셋

요구조건 수집 시 아래 프리셋을 기본값으로 제안. 고객이 명시적으로 다른 요구를 하면 그에 맞춰 조정합니다.

### 시니어 대상 (임원·팀장급, 결정권자)
- **총 시간**: 1일 5시간 (트렌드 0.5H + 실습 4.5H)
- **툴 세트 (7개)**: ChatGPT, Claude, Gemini 3, Perplexity, NotebookLM, Canva, Google AI Studio
- **제외**: Napkin (시각화 비핵심 — NotebookLM/Canva로 대체), Manus (Agent AI 맛보기 — 실험적이라 우선순위 낮음)
- **산출물**: 의사결정 메모 / 리서치 브리프 / 비디오 리포트 / 대시보드 프로토타입 (4종)
- **근거**: 시니어는 의사결정 메모·리서치 브리프·비디오 리포트·대시보드 프로토타입 같은 end-to-end 실무 산출물 경험이 핵심. 폭넓은 툴 노출보다 집중된 워크플로우가 효과적.
- **출처**: 삼성전자 MX사업부 시니어 대상 제안(260417) 요구조건 반영

> 다른 타겟(실무자/주니어 등)은 샘플이 부족해 일반화가 어려워 프리셋을 두지 않습니다. 해당 건은 고객 요구조건에 맞춰 매번 설계합니다.

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

## 자동화 Hook

`.claude/settings.json`에 등록된 hook이 Drive 업로드·PR 처리를 **결정적으로** 보장합니다.
Claude의 판단에 의존하지 않으므로, 아래 동작은 매번 실행됩니다.

| Hook | 시점 | 동작 |
|---|---|---|
| `SessionStart` | 세션 시작 | Drive 인증(`token.json`) 확인 + access token 자동 갱신. 문제 시 **경고만** (빌드 차단 안 함) |
| `PostToolUse` (Bash) | `build.py` 실행 직후 | Drive 업로드 누락 감지 시 보완 업로드 후 링크 회신 |
| `Stop` | 응답 종료 | `projects/{기업명}/` 미커밋 변경 감지 → `git_workflow.py begin`+`finish` 자동 실행 (커밋·push·PR) |

### Stop hook 안전장치
자동 PR 처리는 아래 중 하나라도 걸리면 **경고만** 하고 넘어갑니다.

1. 변경된 기업이 2곳 이상 (기업당 활성 PR 1개 모델이라 모호)
2. 현재 브랜치가 `main`도 `proposal/*`도 아님 → `PROPOSAL_HOOK_ANY_BRANCH=1`로 해제
3. 직전에 같은 상태로 실패 → 같은 실패를 매 턴 반복하지 않음
4. `stop_hook_active` (hook이 촉발한 재실행 — 무한루프 방지)

### 환경변수

| 변수 | 용도 |
|---|---|
| `PROPOSAL_HOOKS_DISABLE=1` | 전체 hook 킬 스위치 |
| `PROPOSAL_AUTHOR` | 작업자명 (기본: `git config user.name`) |
| `PROPOSAL_HOOK_COMMAND` | Stop hook의 `/명령` 추론 강제 지정 |
| `PROPOSAL_HOOK_ANY_BRANCH=1` | 어느 브랜치에서든 PR 자동 처리 |

### 점검 명령
```bash
python scripts/hooks/check_drive_auth.py --verify   # Drive 인증·권한 실제 확인
python scripts/hooks/test_hooks.py                 # hook 파싱 로직 회귀 테스트
```

> ⚠️ hook은 `.claude/settings.json`에 있고, `.gitignore`가 `.claude/*`를 제외하므로
> **이 파일만 예외 처리**되어 있습니다. hook을 추가·수정하면 반드시 커밋해서 팀에 공유하세요.
> `settings.local.json`은 개인 설정이라 계속 git 제외 대상입니다.

## 알려진 이슈 & 해결법

| 이슈 | 해결법 |
|---|---|
| Windows 인코딩 에러 | `PYTHONIOENCODING=utf-8` 필수 |
| PDF 파일명 중복 | Python shutil로 rename |
| Acrobat 파일 락 | `taskkill //F //IM Acrobat.exe` |
| 한글 파일명 깨짐 | bash mv 대신 Python shutil 사용 |
| Track 번호 위첨자 | `use_simple_track_label: false` 설정 |
| Track 간격 좁음 | base.css 여백 증가 (이미 수정됨) |
| Drive 업로드가 산발적으로 안 됨 | 4개 원인 모두 수정됨 (아래 참조) — 재발 시 `check_drive_auth.py --verify` |

### Drive 업로드 산발 실패 — 원인 4가지 (모두 수정됨)
1. **access token 미갱신**: `token.json`의 `expiry`를 `Credentials`에 넘기지 않아 `creds.expired`가 항상 `False` → 갱신이 한 번도 일어나지 않았음. access token 수명이 1시간이라 **인증 직후엔 되고 그 뒤엔 401**. → `expiry` 전달 + 자동 refresh + 재저장
2. **2단계 경로 누락**: `build.py {기업명}/{과정명}`은 `build_proposal()`을 타서 업로드 코드를 아예 안 지났음 → `upload_to_drive()` 추가
3. **조용한 ImportError**: google 라이브러리 미설치 시 `upload_company_files = None`으로 무증상 스킵 → 실패 사유 출력
4. **`SystemExit` 미포착**: `token.json` 없을 때 `sys.exit(1)`이 `except Exception`에 안 잡혀 빌드 프로세스가 종료됐음 → `DriveAuthError` 예외로 변경

## 참조 문서
- **고객사 기억 인덱스: `memory/clients/_INDEX.md`** (작업 시작 전 필독)
- 상세 가이드: `docs/제안서_생성_가이드.md`
- 커리큘럼 검토 가이드: `docs/커리큘럼_검토_가이드.md`
- 라벨 배지 가이드: `docs/라벨_배지_가이드.md` (차수/콘텐츠 태그 카탈로그·사례)
- 견적서 템플릿: `templates/estimate/template.md`
- 견적서 참고 양식: `templates/estimate/references/`
- 기존 사례: `projects/` 디렉토리 내 각 기업 폴더
