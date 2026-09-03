# tmux dev 워크스페이스 사용 가이드

`scripts/dev.sh` 가 켜는 3-pane 통합 작업 환경 사용법. 영광 · 은숙 · 은경 3인
동시 작업을 전제로 설계됨.

---

## 빠른 시작 (Quick Start)

```bash
# 1. 기업별 워크스페이스 시작
bash scripts/dev.sh 기웅정보통신

# 2. (처음이라면) 터미널 너비 150 col 이상 권장. iTerm2/Terminal 창 넓히기.
# 3. 끝내려면: Ctrl+B 누른 후 d (detach). 세션은 백그라운드에 살아 있음.
# 4. 다시 들어가려면: tmux attach -t 기웅정보통신
# 5. 완전히 종료: tmux kill-session -t 기웅정보통신
```

---

## 워크스페이스 구조

```
┌──────────────────────────────────────────────────────────┐
│ 1 Watcher          (전체 너비, 상단 30%)                    │
│   content.json 저장 시 자동으로 PDF 빌드                    │
├────────────────────────────────┬─────────────────────────┤
│ 2 Hermes chat                  │ 3 Status                │
│   AI 에이전트 (GLM-5.2)          │   validate_content.py   │
│   자연어로 커리큘럼 검토/수정    │   버전 히스토리          │
│   Google Sheets MCP 연동        │   Git status            │
└────────────────────────────────┴─────────────────────────┘
```

### Pane 1 — Watcher (자동 빌드)

- `content.json` 변경 시 자동으로 `python build.py {기업명} --author {작업자}` 실행
- 빌드 결과(HTML, PDF 생성)가 이 pane에 실시간 출력
- 종료: `Ctrl+C` (빌드 감지 중지)
- 수동 재실행: `Ctrl+B` 누른 후 `B`

### Pane 2 — Hermes AI 에이전트

대화형 AI 비서. 자연어로 다음 작업 가능:

```
> 이 기업 content.json 검토해줘 — 모듈 순서/시간 배분/도구 일관성
> 4차원 검토 (Flow/Recency/Tone/Readability) 각각 1문장 요약
> 모듈 3개 더 추가해줘, 타겟은 시니어 임원
> 시트 ID 1ABC23xyz 의 A1:Z100 읽고 마스터 시트에 이 기업 행 추가
```

- 모델: GLM-5.2 via Z.AI Coding Plan (구독 — 크레딧 소진 없음)
- 진입 즉시 AGENTS.md 자동 로드 (프로젝트 규칙 인식)
- 종료: `/quit` 또는 `Ctrl+D`

### Pane 3 — Status (정보 패널)

- `validate_content.py` 결과 (PASS/FAIL/WARN)
- 버전 히스토리 (v001, v002, …)
- Git status (수정/추가/삭제 파일)
- 갱신: `Ctrl+B` 누른 후 `V`

---

## 단축키 (Ctrl+B prefix)

### 기본 (tmux 기본)

| 단축키 | 동작 |
|---|---|
| `Ctrl+B` `?` | 전체 단축키 도움말 |
| `Ctrl+B` `d` | detach (세션 백그라운드로 빠져나옴) |
| `Ctrl+B` `c` | 새 window |
| `Ctrl+B` `1`/`2`/`3` | pane 이동 (숫자) |
| `Ctrl+B` `o` | 다음 pane으로 이동 |
| `Ctrl+B` `;` | 직전 pane으로 이동 |
| `Ctrl+B` `z` | 현재 pane 전체화면 토글 |
| `Ctrl+B` `[` | 스크롤 모드 진입 (방향키/q로 종료) |

### 커스텀 (이 프로젝트 전용)

| 단축키 | 동작 |
|---|---|
| `Ctrl+B` `r` | `.tmux.conf` 리로드 (설정 변경 시) |
| `Ctrl+B` `\|` | pane 좌우 분할 |
| `Ctrl+B` `-` | pane 상하 분할 |
| `Ctrl+B` `h`/`j`/`k`/`l` | vim 스타일 pane 이동 |
| `Ctrl+B` `B` | 현재 기업 강제 재빌드 |
| `Ctrl+B` `V` | content.json 재검증 (Pane 3 갱신) |
| `Ctrl+B` `G` | git status 표시 |
| `Alt+←`/`→` | pane 크기 조정 (5 col 씩) |
| `Shift+←`/`→` | window 이동 |

---

## 일반적인 작업 흐름 (Workflow)

### A. content.json 수정 → PDF 재생성

```
1. 외부 에디터(VS Code 등)에서 content.json 열고 수정 + 저장
2. tmux Pane 1 (Watcher)가 자동으로 변경 감지
3. 자동 빌드 실행 → HTML/PDF 생성 로그가 Pane 1에 표시
4. 빌드 실패 시 에러 메시지 확인 → 수정 → 다시 저장
5. 성공 시 PDF 폴더 열어 확인: open projects/{기업명}/{과정명}/
```

### B. AI로 커리큘럼 검토 (4차원)

```
1. Pane 2 (Hermes)로 이동: Ctrl+B 2
2. 자연어로 요청:
   > "지금 content.json 기준으로 4차원 검토해줘"
3. AI가 Flow/Recency/Tone/Readability 각각 평가
4. 수정 제안 받아들일 경우:
   > "Flow 2번 제안 적용해줘 — modules 순서 swap"
5. AI가 파일 직접 수정 → Pane 1이 자동으로 재빌드
```

### C. 버전 관리 + Git push

```
1. 빌드 성공 후 versions/ 폴더에 자동 스냅샷 생성 (v001, v002, …)
2. Pane 3 (Status)에서 버전 히스토리 확인
3. AGENTS.md 규칙대로 Git push:
   git pull --rebase origin main
   git add projects/{기업명}/
   git commit -m "/build {기업명} — {작업자} ({변경 요약})"
   git push origin main
```

### D. Google Sheets 동기화

```
1. 견적서 시트를 서비스 계정과 미리 공유해 둠
   (hermes@slackbot-gayoung.iam.gserviceaccount.com)
2. Pane 2에서:
   > "이 content.json 기반으로 견적서 행 추가해줘.
   >  시트 ID: 1ABC23xyz, 탭: 견적서, 컬럼: 기업명/과정/차수/인원/금액"
3. AI가 sheets_append_values 도구 호출 → 행 추가
```

---

## 멀티유저 시나리오

영광 · 은숙 · 은경 각자 자기 PC에서 동시 작업:

| 작업자 | 세션 | 작업 대상 |
|---|---|---|
| 영광 | `bash scripts/dev.sh 삼성전자` | 삼성전자 제안서 |
| 은숙 | `bash scripts/dev.sh KCB` | KCB 제안서 |
| 은경 | `bash scripts/dev.sh 현대카드` | 현대카드 제안서 |

- 세션 이름 = 기업명 → 충돌 없음
- 각자의 `~/.hermes/` 인증 사용 (공유 X)
- Git push 시 `git pull --rebase` 먼저 → 충돌 시 사용자에게 알림

**작업자 자동 감지**:
- 환경변수 `SLACK_USER_ID` 있으면 매핑 (U0924H9HSK1 → 영광 등)
- 없으면 `git config user.name` 사용
- 둘 다 없으면 "작업자" (권장: `git config --global user.name "본명"`)

---

## 문제 해결 (Troubleshooting)

### 세션이 안 만들어져요

```bash
# 1. tmux 설치 확인
which tmux || brew install tmux

# 2. 죽은 세션 정리
tmux kill-server

# 3. 재시도
bash scripts/dev.sh 기웅정보통신
```

### 빌드가 안 돼요 (Pane 1)

- `python3` 대신 `python` 인식 문제: `brew install python` 으로 Python 3 설치
- Edge 브라우저 없음: AGENTS.md "PDF 빌드" 섹션 참고
- 한글 파일명 깨짐: `git config --global core.quotePath false` (이미 설정됨)

### Hermes가 응답 안 해요 (Pane 2)

```bash
# 1. 인증 상태 확인
hermes status

# 2. API 키 확인
cat ~/.hermes/.env | grep ZAI

# 3. 크레딧/구독 상태: https://docs.z.ai/devpack/overview
```

### Google Sheets MCP 호출 실패

```bash
# MCP 상태
hermes mcp list
hermes mcp test google-sheets

# 시트가 공유 안 됐을 가능성 90%
# 시트 "공유" 버튼 → 서비스 계정 이메일 추가:
#   hermes@slackbot-gayoung.iam.gserviceaccount.com
```

### 한글이 깨져요 / pane이 좁아요

- 터미널 창을 최소 150 col 너비로 확대
- macOS Terminal 환경설정 → 폰트 크기 작게 (14pt 권장)
- Pane 전체화면: `Ctrl+B z`

### detach 한 세션 다시 안 보여요

```bash
# 살아있는 세션 목록
tmux ls

# 특정 세션 attach
tmux attach -t 기웅정보통신

# 가장 최근 세션 attach
tmux attach
```

---

## 의존성 (Dependencies)

| 도구 | 용도 | 설치 |
|---|---|---|
| `tmux` | 워크스페이스 | `brew install tmux` |
| `fswatch` | 파일 변경 감지 (macOS) | `brew install fswatch` |
| `python3` | 빌드 스크립트 | `brew install python` |
| `hermes` | AI 에이전트 | 별도 설치 (`~/.local/bin/hermes`) |
| `jinja2` | HTML 템플릿 | `pip install jinja2` |
| Edge browser | PDF 변환 | macOS용 Edge 설치 |

---

## 파일 위치 요약

| 파일 | 용도 |
|---|---|
| `scripts/dev.sh` | 워크스페이스 런처 |
| `scripts/watch_build.sh` | content.json 변경 감지 → 자동 빌드 |
| `scripts/validate_content.py` | 스키마/도구일관성 검증 |
| `.tmux.conf` | tmux 설정 (단축키/테마) |
| `.hermes/` | 프로젝트 로컬 Hermes 워크스페이스 |
| `~/.hermes/config.yaml` | Hermes 글로벌 설정 (모델, MCP) |

---

## 참고

- 상세 스키마: `schemas/*.example.json`
- 검토 가이드: `docs/커리큘럼_검토_가이드.md`
- Google Sheets 설정: `docs/google_sheets_mcp_setup.md`
- 제안서 생성 전체 흐름: `docs/제안서_생성_가이드.md`
- 버전 관리 규칙: `AGENTS.md` 의 "버전 관리" 섹션
