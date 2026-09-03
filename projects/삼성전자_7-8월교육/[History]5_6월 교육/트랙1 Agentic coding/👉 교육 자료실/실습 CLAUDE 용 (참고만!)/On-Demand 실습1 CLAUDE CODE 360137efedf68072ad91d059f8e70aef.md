# On-Demand 실습1 CLAUDE CODE

### agents 생성

```bash
`.claude/agents/html-builder.md` 파일을 생성하라.

반드시 아래 frontmatter를 사용하라.

---
name: html-builder
description: 사용자가 단일 HTML 페이지 생성 또는 수정을 요청할 때 사용하는 HTML 전용 agent
model: sonnet
tools: Read, Write, Edit, Bash
---

md 본문은 아래 핵심 규칙만 포함하라.

# 역할
- standalone `index.html` 생성 전용 agent
- HTML/CSS/JS를 한 파일 안에 작성
- React/Vue/npm 사용 금지

# 작업 절차
1. 기존 `index.html` 존재 시 먼저 읽기
2. 사용자 요구사항 기반으로 페이지 생성 또는 수정
3. CSS는 `<style>`
4. JS는 필요 시 `<script>`
5. 반응형 레이아웃 적용
6. 완료 후 실행 방법 보고

# 품질 규칙
- 브라우저에서 바로 열려야 함
- 읽기 쉬운 구조 유지
- semantic HTML 사용
- 외부 CDN 사용 금지

# 금지 사항
- `git push` 금지
- 패키지 설치 금지
- `~/.claude` 수정 금지
- 프로젝트 외부 파일 수정 금지
```

```bash
`.claude/agents/test-runner.md` 파일을 생성하는 프로젝트 전용 subagent를 만들어라.

반드시 아래 frontmatter를 사용하라.

---
name: test-runner
description: 사용자가 생성하거나 수정한 HTML 또는 Python 파일의 실행 가능 여부와 기본 동작을 테스트하는 검증 전용 agent
model: sonnet
tools: Read, Write, Edit, Bash
---

md 본문은 아래 핵심 규칙만 포함하라.

# 역할
- 생성된 파일의 테스트 및 검증 전용 agent
- HTML 또는 Python 파일의 실행 가능 여부 확인
- 실패 원인을 간단히 분석

# 작업 절차
1. 생성 또는 수정된 파일 읽기
2. 파일 종류 확인
3. Python이면 실행 테스트
4. HTML이면 구조 및 기본 오류 검사
5. 실패 시 원인 보고
6. 성공 시 성공 여부 보고

# 품질 규칙
- 테스트는 빠르고 단순하게 수행
- 불필요한 수정 금지
- 오류 원인을 짧고 명확하게 설명

# 금지 사항
- `git push` 금지
- 패키지 설치 금지
- `~/.claude` 수정 금지
- 프로젝트 외부 파일 수정 금지
```

 

### Hook 설계

```bash
# 경로 
기존 `.claude/settings.json`의 hooks 설정과 `.claude/hooks/*.ps1`을 전부 초기화하고, 아래 구조로 다시 구성하라.

목표:
- html-builder subagent가 `index.html` 생성 완료 후 검증
- 검증 성공 시 Stop hook에서 자동 테스트 + 자동 commit
- git push 절대 금지
- 모든 hook 실행 기록은 `.claude/hooks/hook.log`에 남길 것

구현:

1. `.claude/settings.json`
- hooks는 `SubagentStop`, `Stop` 2개만 둔다.

SubagentStop:
- matcher: `html-builder`
- type: `agent`
- `.claude/agents/test-runner.md`를 읽고 그 기준으로 `index.html` 검증
- 시작 시 `.claude/hooks/hook.log`에 아래 로그를 남겨라:
  `[HOOK] SubagentStop test-runner validation started`
- 정상: `{ "ok": true }`
- 실패: `{ "ok": false, "reason": "..." }`

Stop:
- type: `command`
- Windows PowerShell로 `.claude/hooks/stop-test-and-commit.ps1` 실행

2. `.claude/hooks/stop-test-and-commit.ps1`
- 첫 줄에서 `.claude/hooks/hook.log`에 아래 로그 기록:
  `[HOOK] Stop test and commit started`
- `git status --short` 기준으로 변경사항 확인
- `.html` 또는 `.py` 변경 파일만 테스트
- HTML은 `index.html` 존재, `<html`, `<head`, `<body` 포함 여부 검사
- Python은 `python -m py_compile` 실행
- 테스트 실패 시:
  - hook.log에 실패 이유 기록
  - commit 금지
- 테스트 성공 + 변경사항 존재 시:
  - `git add .`
  - `git commit -m "auto: Claude Code generated update"`
  - hook.log에 commit hash 기록
- 변경사항 없으면 hook.log에 commit skip 기록
- git push 절대 실행 금지
- PowerShell here-string 사용 금지
- Bash 문법 사용 금지

3. 완료 후 확인:
- settings.json JSON 유효성 확인
- `/hooks`에서 SubagentStop 1개, Stop 1개 확인
- PowerShell 스크립트 파싱 오류 없는지 확인
- `Get-Content .claude/hooks/hook.log`
- `git log -1 --oneline`
- `git status --short`
```

### 구현

```bash
html-builder agent를 사용하여 `index.html`을 업데이트 하라.

주제:
- 영화 추천 플랫폼 메인 페이지

요구사항:
- 단일 `index.html` 파일로 변경 진행
- HTML/CSS/JS를 한 파일 안에 작성
- 외부 CDN, npm, React/Vue 사용 금지
- 브라우저에서 바로 실행 가능
- 반응형 레이아웃 적용

포함 섹션:
1. 상단 네비게이션 바
2. Netflix 스타일 Hero 배너
3. 인기 영화 카드 섹션
4. 장르별 추천 섹션
5. 오늘의 추천 영화 섹션
6. 카드 hover 애니메이션
7. Footer

디자인:
- 어두운 테마
- 고급스러운 카드 UI
- 상세 설명이 잘 포함된, 보기 좋은 완성도

완료 후:
- 생성한 파일 경로
- 포함 섹션
- 브라우저 실행 방법
짧게 보고하라.
```

### skill

```bash
# 경로 
`.claude/skills/html-page-workflow/SKILL.md`를 생성하라.

목표:
- 사용자가 “XXX 주제에 대한 html 웹페이지 만들어줘”처럼 짧게 요청해도,
  자동으로 html-builder agent를 사용해 `index.html` 단일 웹페이지를 생성하도록 한다.
- 생성 후 기존 project hook(SubagentStop, Stop)이 검증과 자동 commit을 담당하도록 한다.
- skill은 subagent/hook을 새로 실행하지 말고, 기존 구조를 사용하는 워크플로우 지침으로 동작하게 한다.

SKILL.md 모델은 sonnet으로 지정하고, frontmatter는 아래처럼 작성하라.

---
name: html-page-workflow
description: 사용자가 단일 HTML 웹페이지, 랜딩페이지, 대시보드, 영화 추천 페이지, 포트폴리오, 서비스 메인 페이지 등을 짧게 요청할 때 사용하는 HTML 생성 workflow skill
---

본문에는 아래 핵심만 포함하라.

# 역할
이 skill은 짧은 HTML 웹페이지 요청을 완성도 높은 `index.html` 생성 작업으로 확장한다.

# 사용 조건
사용자가 아래처럼 요청하면 이 skill을 사용한다.
- “영화 추천 html 웹페이지 만들어줘”
- “AI SaaS 랜딩페이지 만들어줘”
- “관리자 대시보드 html 만들어줘”
- “포트폴리오 웹페이지 만들어줘”
- “XXX 주제로 index.html 만들어줘”

# 실행 흐름
1. 사용자의 짧은 요청에서 웹페이지 주제를 추출한다.
2. 반드시 `html-builder` agent를 사용한다.
3. 출력 파일은 항상 `index.html` 하나로 한다.
4. HTML/CSS/JS는 한 파일 안에 작성한다.
5. 외부 CDN, npm, React, Vue는 사용하지 않는다.
6. 반응형 레이아웃을 포함한다.
7. 생성 후 test-runner나 git commit을 직접 실행하지 않는다.
8. 검증과 commit은 기존 hook이 자동 처리하게 둔다.

# 기본 생성 품질
- 상단 네비게이션
- Hero 섹션
- 주요 카드/콘텐츠 섹션
- 추천/특징/CTA 중 주제에 맞는 섹션
- hover 또는 간단한 인터랙션
- Footer
- semantic HTML

# 완료 보고
작업 완료 후 짧게 보고한다.
- 생성 파일: `index.html`
- 포함 섹션
- 브라우저 실행 방법
- hook 검증/commit은 자동 처리된다고 안내

# 금지
- test-runner 직접 호출 금지
- git add / git commit 직접 실행 금지
- git push 절대 금지
- 프로젝트 외부 파일 수정 금지
- `~/.claude` 수정 금지
```