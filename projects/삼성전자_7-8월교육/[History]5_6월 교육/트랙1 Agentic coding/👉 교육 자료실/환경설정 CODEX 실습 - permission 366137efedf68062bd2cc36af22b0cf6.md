# 환경설정 CODEX 실습 - permission

### 커스텀 config.toml - codex - window

```markdown
approval_policy = "on-request"
default_permissions = "lecture-demo"

# Windows에서 Codex의 로컬 작업 격리 환경을 관리자 권한 기반 방식으로 세팅하라는 설정이다.
# 보통 Windows 네이티브 환경에서는 elevated가 권장된다.
[windows]
sandbox = "elevated"

[features]
codex_git_commit = true

[permissions.lecture-demo.workspace_roots]
'C:\Users\computer\Desktop\harness_codex\practice_main' = true

[permissions.lecture-demo.filesystem]
":minimal" = "read"

[permissions.lecture-demo.filesystem.":workspace_roots"]
"." = "write"
"text/protect.txt" = "deny"

[permissions.lecture-demo.network]
enabled = false
```

### ACL 권한 - auto commit 관련

.git/index.lock을 만들고 .git/index를 갱신한다. 
git commit은 .git/objects, .git/refs, .git/logs도 바꾼다. 
그래서 .git에 OS 쓰기 권한이 없으면 커밋 자동화가 막힌다.

```markdown
. Windows ACL에서 .git Modify 권한 부여

# 1. 현재 실행 계정 확인 
whoami 

# 2. .git 소유권을 현재 사용자로 가져오기 
takeown /F .git /R /D Y 

# 3. 현재 사용자 변수 만들기 
$me = "$env:USERDOMAIN\$env:USERNAME" 

# 4. .git 폴더와 하위 전체에 Modify 권한 부여 
icacls .git /grant "${me}:(OI)(CI)M" /T
```

### 1번 확인 사항

```markdown
### 전역 경로 !!!!
~/.codex/config.toml 

### 프로젝트 경로
.codex/config.toml
```

### 2번 확인 사항

```markdown
경로 문제 절대 경로 & 상대 경로 개념을 살펴서, 
현재 프로젝트 스코프에 알맞게 경로를 변경/업데이트하라. 
```

### 커스텀 config.toml - codex - Mac

```markdown
approval_policy = "on-request"
default_permissions = "lecture-demo"

[macos]
sandbox = "standard"  # 또는 도구 지원에 따라 생략하거나 기본값 사용

[features]
codex_git_commit = true

[permissions.lecture-demo.workspace_roots]
'/Users/computer/Desktop/harness_codex/practice_main' = true

[permissions.lecture-demo.filesystem]
":minimal" = "read"

[permissions.lecture-demo.filesystem.":workspace_roots"]
"." = "write"
"text/protect.txt" = "deny"

[permissions.lecture-demo.network]
enabled = false
```

```json
아래 작업을 순차적으로 진행하라.

  1. text 폴더에 모든 .txt 파일 맨 끝 줄에 My name is Jiwoong Yang. 을 덧붙이고, 성공/실패를 출력하라.
  2. 1번 성공/실패의 결과와 상관없이 text 폴더에 변경사항이 존재한다면  git auto commit을 진행하라.
```

### CLAUDE settings.json

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Read(./**)",
      "Write(./**)",
      "Edit(./**)",
      "Bash(*)",
      "Bash(Write-Output *)",
      "Bash(New-Item *)",
      "Bash(Get-Content *)",
      "Bash(Test-Path *)",
      "Bash(Set-Content *)",
      "PowerShell(*)",
      "Bash(Select-String *)",
      "Bash(ls *)"
    ],
    "deny": [
      "Write(~/.claude/**)",
      "Edit(~/.claude/**)",
      "Bash(*~/.claude*)",
      "Bash(git push *)",
      "PowerShell(git push *)"
    ]
  },
  "model": "opusplan",
  "language": "korean",
  "showClearContextOnPlanAccept": true,
  "plansDirectory": ".claude/plans"
}

```

# 프롬프트로 진행

### 1. 1번 실습!! config.toml - 에이전트가 동작할 때, 파일 권한 제어

```markdown
이 새 프로젝트를 Codex 작업용으로 초기 설정하라.

이번 단계의 목표는 오직 하나다.

- 프로젝트 루트에 `.codex/config.toml`만 생성한다.
- `AGENTS.md`는 수정하지 않는다.

반드시 생성할 구조:

.
└── .codex/
    └── config.toml

`.codex/config.toml`에는 아래 TOML 설정만 정확히 작성하라.
값을 바꾸지 말고, 다른 설정을 추가하지 마라.

```toml
model = "gpt-5.4-mini"
model_reasoning_effort = "medium"
plan_mode_reasoning_effort = "high"
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[agents]
max_threads = 4
max_depth = 1
job_max_runtime_seconds = 1800

단, 각 설정 바로 위에는 TOML 주석(`#`)으로 설명을 붙여라.

각 주석은 반드시 아래 순서로 작성하라.

1. 이 설정이 무엇을 조절하는지 한 문장으로 설명한다.
2. 현재 값이 어떤 의미인지 설명한다.
3. 대표적으로 선택 가능한 다른 설정 값은 무엇이 있는지 반드시 포함하라!
4. 값을 낮추거나 높이면 어떤 효과가 있는지 설명한다.

주석 작성 방식:
- 기계적인 용어 나열이 아니라, 처음 보는 사람도 이해할 수 있게 직관적으로 작성한다.
- “다른 값은 더 작은 수나 더 큰 수가 있다”처럼 무의미한 설명을 쓰지 않는다.
- 가능한 경우 실제 존재하는 옵션 예시를 전부 설명에 포함한다. 
- 각 설정당 주석은 3~5줄 이내로 유지한다.
- 실제 설정값은 절대 바꾸지 않는다. 단, 대표적으로 선택 가능한 다른 설정 값이 주석에 포함되지 않으면 실패다.
- 주석 때문에 TOML 문법이 깨지면 안 된다.
```

### rules - 터미널 명령 실행 제어

### 형식 - prefix_rule

```json

prefix_rule(
    pattern = ["", ""],
    decision = "forbidden",
    justification = "",
)

prefix_rule(
    pattern = ["", ""],
    decision = "prompt",
    justification = "",
)

prefix_rule(
    pattern = ["", ""],
    decision = "allow",
    justification = "",
)
```

### 예시

```json
# git push 차단
prefix_rule(
    pattern = ["git", "push"],
    decision = "forbidden",
    justification = "원격 저장소 push는 사용자가 직접 수행",
)

# git commit은 자동 허용 
prefix_rule(
    pattern = ["git", "commit"],
    decision = "allow",
    justification = "커밋은 자동 허용",
)

# git add는 자동 허용
prefix_rule(
    pattern = ["git", "add"],
    decision = "allow",
    justification = "추적은 자동 허용",
)
```

### 2 번 실습

### `.codex/rules/default.rules` 실제 구현 실습

```markdown
원문 docs url: 
https://developers.openai.com/codex/rules 

를 확인하고, 터미널 명령 제어 관점에서 이 프로젝트의 기본 안전 설정 구현 plan을 작성하라.

목표:
- 프로젝트 루트에 `.codex/rules/default.rules`만 생성한다.

반드시 생성할 구조:

.
└── .codex/
    └── rules/
        └── default.rules

현재 로컬 운영 환경을 먼저 파악하라.

확인할 항목은 OS, shell/terminal, 프로젝트 루트, git 사용 가능 여부, python/node/npm 사용 가능 여부다.
환경 정보를 확인할 수 없으면 추정하지 말고 UNKNOWN으로 기록하라.

작업 범위는 현재 프로젝트 루트 내부로만 제한하라.
프로젝트 내부의 기본 탐색, 읽기, 쓰기, 수정은 가능한 한 자동 진행되도록 설계하라.

단, 삭제 계열 명령은 기본적으로 금지하도록 설계하라.

특히 파악한 환경에 맞는 rm, del, Remove-Item 등 파일 삭제 명령은 forbidden 대상으로 분류하라.
git push, git push --force, 원격 저장소 변경 명령은 forbidden 대상으로 분류하라.
.env 파일을 읽거나 출력하는 명령은 금지 대상으로 설계하라.

prefix_rules 는 총 10개를 넘기지 않는다. 핵심 형태만 골격을 잡도록 plan 진행하라. 

allow, prompt, forbidden 규칙을 각각 어떤 명령에 적용할지 표로 정리하라.
최종 plan에는 생성/수정 예정 파일 목록, 검증 방법, 실패 시 확인할 항목만 짧게 포함하라.
```