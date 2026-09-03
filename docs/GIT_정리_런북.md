# Git 정리 런북 — ai-education-proposal

작성: 2026-08-21 · 저장소 `github.com/kisdevan/propsal_modulabs` (**private 확인됨**)
**용도**: 위에서 아래로 순서대로 실행하면 미커밋 841건 정리가 끝나는 단일 문서. 다른 문서를 참조하지 않아도 완결됩니다.
**환경**: Windows PowerShell · 저장소 루트 `C:\Users\Admin\Downloads\ai-education-proposal`

> **이 문서의 위치를 `docs/`로 정한 이유**: 브랜치·`.gitignore`·worktree는 저장소 전체 관심사이고 특정 고객사 산출물이 아닙니다. 기존 문서 관례(`docs/review_governance.md`, `docs/제안서_생성_가이드.md`)와 일관됩니다.

---

## ⚠️ 실행 기록 및 정정 (2026-08-24)

이 런북을 2026-08-24에 실제로 실행했습니다. **작성 시점(8/21) 추정과 실측이 여러 곳에서 달랐습니다.** 아래가 실측 기준입니다.

### 수치 정정

| 항목 | 런북 원안(8/21) | 실측(8/24) | 원인 |
|---|---|---|---|
| 미커밋 건수 | 841 | **105** | `.gitattributes`가 **미추적 상태로 워킹트리에 존재**. gitattributes는 인덱스가 아니라 워킹트리에서 읽히므로 커밋 전에도 이미 적용되어 CRLF 노이즈가 이미 안 보이는 상태였음 |
| PR ① 파일 수 | 약 731 | **7** | 위와 같은 이유 |
| worktree 용량 | 약 4.0GB | **6.66GB** | 원안은 `.claude/worktrees/`만 계산. `projects/2026 연세대/`(1.98GB)·`한기대`(0.64GB) 등 하위 경로 누락 |
| 압축 해제물 | 562건 | **551건** | — |
| 연세대 히스토리 원본 문서 | 30건 | **25건** | 단 `unpacked_v1~v15` **전부** 대응 원본 `.docx`가 추적됨을 1:1 확인. 제거 안전성 결론은 유지 |

### 근본 원인 추가 — `.git/index.lock` 3일 방치

**`2026-08-21 16:47`에 생성된 0바이트 `.git/index.lock`이 3일간 남아 있었습니다.** 실행 중인 git 프로세스는 없었습니다. 8/21 진단 세션에서 크래시한 잔여물로 보이며, 이 lock 때문에 **모든 git 쓰기가 실패**하고 있었습니다.

런북 5-C는 자동 PR hook 스킵을 악순환의 원인으로 지목했지만, **실제 1차 원인은 이 lock이었습니다.** hook이 아니라 git 자체가 멈춰 있었습니다. → `AGENTS.md` 작업 위생 규칙 5번으로 점검 절차를 추가했습니다.

### 절차 변경 — PR 머지를 STEP 1보다 먼저

**런북 순서를 그대로 실행하면 PR ①이 오염됩니다.** STEP 1의 `git add --renormalize .`는 워킹트리 전부를 스테이징하는데, 실측 결과 수정 64건 중 **40건이 열린 PR #49(개인 휴대폰 번호 제거)와 바이트 단위로 동일**했습니다. 그대로 실행하면 "개행 정규화만"이어야 할 PR ①에 개인정보 제거 실변경 40건이 섞입니다.

→ **STEP 0 다음에 열린 PR을 먼저 머지하십시오.** 8/24에는 #44 #46 #47 #48 #49 #50을 머지해 워킹트리 105건 중 56건이 자동 소멸했고, 그 결과 로컬 `main`의 35커밋 뒤처짐도 해소됐습니다.

### 그 외 실행 중 조정

| 조정 | 내용 |
|---|---|
| `.gitignore` 패턴 | `**/unpacked_v*/` → **`**/unpacked_*/`**. `projects/현대카드/unpacked_draft/`(23건)가 원안 패턴에 누락됨 |
| PR ①에서 unpacked 제외 | renormalize가 `-text` 속성 때문에 unpacked 316건을 CRLF 방향으로 스테이징하는데, STEP 2에서 어차피 추적 해제할 대상이라 PR ①에서 unstage |
| Drive 포인터 | 런북은 `projects/KCB/강사목록_KCB.gsheet`를 지목했으나 그 파일은 **애초에 미추적**. 추적 중이던 것은 `projects/NIA/users_nia.gsheet` 1건 |
| `combined_render.html` | 코드 제외 목록 추가에 더해, 추적 중이던 1건(`projects/기웅정보통신/컨설팅_제안서/`)도 추적 해제 |
| STEP 1 브랜치 이동 | 워킹트리가 더러워 `git switch main`이 반복 거부됨. ① origin/main에 존재하는 미추적 15건을 `../_untracked_backup`으로 이동 ② 실제 변경을 `git stash` ③ 개행만 다른 3건은 백업 후 `--force` 전환 순서로 해소 |

### 미완료 이월

| 항목 | 상태 |
|---|---|
| PR #45 (대덕전자) | `memory/clients/대덕전자.md` 충돌. #49의 휴대폰 번호 제거를 살리고 #45의 추가분을 얹어야 함 |
| `../_untracked_backup` 9건 | main 버전과 내용이 달라 선별 필요 |
| `git stash` 1건 | `cleanup-260824: STEP1 전 추적변경 shelve` — 수정 13 + 삭제 11(260811 폴더 재구조화) |
| 260811 8/12 회의록 | 이동 흔적 없이 삭제된 상태. `CLAUDE.md` 규칙상 회의록 원본은 보존해야 함 |

---

## 0. 전체 그림

| STEP | 내용 | PR | 예상 소요 |
|---|---|---|---|
| **0** | 백업 + 사전 점검 | — | 15~25분 |
| **1** | `.gitattributes` + 개행 정규화 | **PR ①** | 20~30분 |
| **2** | `.gitignore` 보강 + `git rm --cached` + 문서·코드 수정 | **PR ②** | 30~40분 |
| **3** | 롯데이커머스 산출물 커밋 | **PR ③** | 15~20분 |
| **4** | 브랜치·worktree 정리 | — | 20~30분 |
| **5** | 재발 방지 설정 | (PR ② 포함) | 10분 |
| | | | **약 2시간** |

### PR을 3개로 나누는 이유

| PR | 왜 이 순서여야 하는가 |
|---|---|
| **① 개행 정규화** | **반드시 첫 번째.** 이걸 안 하고 다른 파일을 `git add` 하면 그 파일 **전체가 개행 변경으로 커밋**되어 실제 변경이 무엇인지 영구히 알 수 없게 됩니다 |
| **② .gitignore + 추적 해제** | 개행이 정리된 상태에서 해야 `git rm --cached` diff가 깨끗합니다. 562건 삭제는 단독 커밋이어야 `git revert` 한 번으로 되돌아갑니다 |
| **③ 롯데 산출물** | 저장소 위생과 무관한 **업무 산출물**이므로 분리해야 리뷰어가 내용만 보고 판단할 수 있습니다 |

---

## 사전 조사 결론 (판정 완료 — 추가 확인 불필요)

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| **1** | `unpacked_v*` 압축 해제물 **562건 제거** | ✅ **안전하게 제거 가능** | 원본이 git에 함께 추적됨 — `연세AX_제안서_모두의연구소_v10~v16_*.docx` 등 **원본 문서 30건 확인**. 압축 해제물은 그 파생물 |
| **2** | `.claude/worktrees/` 등 worktree | ✅ **전부 정리 대상** (단 `%TEMP%\opencode\aegis-wt` 1곳은 **정리 불필요** — 저장소 밖 임시 폴더, 무해) | `git worktree list` 결과 **15개 전부 `prunable`(죽음)**, 활성 0개. `.claude/worktrees/` 8개만 **약 4.0GB** |
| **3** | `memory/` | ⚠️ **분리 판정** — 신규 6건은 제외, `clients/`는 유지 | 신규 6건은 `# Session:` + `Session Key: agent:main:telegram:direct:...` 형태의 **에이전트 세션 로그**(개인 ID 포함). 추적 중인 `memory/clients/` 6건은 고객 정보 **팀 자산** |
| **4** | `openwiki/` | ✅ **ignore 후보에서 제외** | `.github/workflows/openwiki-update.yml` — `cron "0 8 * * *"` + `peter-evans/create-pull-request@v7`로 브랜치 `openwiki/update`에 PR 생성. **CI가 관리하는 팀 산출물** |

> ⚠️ **조사 4의 부수 발견**: 위 워크플로의 `add-paths`에 **`AGENTS.md`와 `CLAUDE.md`가 포함**되어 있습니다. 즉 openwiki 자동 PR이 이 두 파일을 갱신할 수 있으므로, STEP 2에서 `AGENTS.md`를 수동 수정하면 **`openwiki/update` PR과 충돌할 수 있습니다.** 충돌 시 openwiki PR을 먼저 머지하고 rebase하세요.

---

# STEP 0 — 백업 및 사전 점검

> 소요 15~25분 · 파괴적 명령 없음

### 실행 전 확인

```powershell
# 저장소 실제 용량 확인 — worktree 4GB 때문에 zip이 매우 커집니다
cd C:\Users\Admin\Downloads
"{0:N1} GB" -f ((Get-ChildItem .\ai-education-proposal -Recurse -Force -ErrorAction SilentlyContinue |
  Measure-Object Length -Sum).Sum / 1GB)

# gh CLI 설치 확인 (STEP 3에서 필요)
gh --version
gh auth status
```

`gh`가 없으면 [cli.github.com](https://cli.github.com)에서 설치하거나 `winget install GitHub.cli` 후 `gh auth login`.

### 실행

```powershell
cd C:\Users\Admin\Downloads

# ── 0-1. 백업. 죽은 worktree 4GB와 versions/ 를 제외해 용량을 줄입니다.
$dst = ".\ai-education-proposal_backup_$(Get-Date -Format yyyyMMdd_HHmm)"
robocopy .\ai-education-proposal $dst /E /R:1 /W:1 `
  /XD worktrees versions node_modules __pycache__ /NFL /NDL /NJH
#   → .git 은 포함됩니다(이력 보존에 필수)

# ── 0-2. 현재 상태 스냅샷 (나중에 대조용)
cd .\ai-education-proposal
$env:GIT_OPTIONAL_LOCKS=0
git status --porcelain > ..\git_status_before.txt
git branch -a > ..\git_branches_before.txt
git worktree list > ..\git_worktrees_before.txt
git log --oneline -10 > ..\git_log_before.txt

# ── 0-3. ⚠️ 필수: 저장소 전체 관심사 문서 3건의 롯데 폴더 사본 삭제
#    docs/ 로 이미 이동(복사)되어 있고, 롯데 폴더 사본이 남아 있으면
#    PR ③ 에 저장소 위생 문서가 섞여 리뷰 범위가 흐려집니다.
#    (샌드박스에서 삭제 권한이 없어 이 단계만 수동입니다. 내용은 docs/ 에 동일하게 있습니다.)
$P = "projects\260720 롯데이커머스 전사교육"

# 먼저 docs/ 사본이 정상인지 확인 — 3개 모두 존재해야 함
Get-Item docs\GITIGNORE_보강안.md, docs\제안서_인덱스_홈페이지_기획안.md, docs\GIT_저장소_진단기록_260821.md |
  Select-Object Name, Length

# 확인 후 롯데 폴더 사본 삭제
Remove-Item "$P\GITIGNORE_보강안.md"
Remove-Item "$P\제안서_인덱스_홈페이지_기획안.md"
Remove-Item "$P\GIT_브랜치_전략_및_작업절차.md"     # docs/GIT_저장소_진단기록_260821.md 로 개명 이동됨
```

### 실행 후 검증

```powershell
Get-Item ..\git_status_before.txt | Select Name, Length
(Get-Content ..\git_status_before.txt).Count      # 841 이어야 함
Test-Path $dst                                     # True

# 0-3 검증 — 롯데 폴더에 저장소 위생 문서가 남아 있지 않아야 함
Get-ChildItem "projects\260720 롯데이커머스 전사교육" -Filter "GIT*" ; `
Get-ChildItem "projects\260720 롯데이커머스 전사교육" -Filter "제안서_인덱스*"
#   → 아무것도 출력되지 않으면 정상

# 롯데 폴더에 남아야 하는 파일 5개 확인
Get-ChildItem "projects\260720 롯데이커머스 전사교육" -File |
  Where-Object { $_.Extension -in ".md",".html" } | Select-Object Name
#   → CLAUDE.md / 롯데e커머스_2차교육_운영기획안_v3.md / 롯데e커머스_3차교육_설계안_v1.md /
#     롯데e커머스_의사결정_대기목록.md / 롯데이커머스_전사AI교육_1-3차_통합기획_보고용.html
#     (+ 기존 롯데이커머스_3트랙_교육과정_소개.html)
```

### 되돌리기

이후 어떤 단계에서든 문제가 생기면 백업 폴더를 원본 위치로 되돌립니다.

---

# STEP 1 — PR ①: `.gitattributes` + 개행 정규화

> 소요 20~30분 · **841건 중 731건(87%)을 해소하는 핵심 단계**

**왜 첫 번째인가**: 현재 워킹트리 파일은 모든 줄이 CRLF인데 git 인덱스는 LF입니다. `.gitattributes` 없이 어떤 파일이든 `git add` 하면 그 파일 전체가 "모든 줄 변경"으로 커밋되어 실제 변경 내용이 diff에 묻힙니다.

### 실행 전 확인

```powershell
# .gitattributes 는 이미 저장소 루트에 작성되어 있습니다 (2026-08-21)
Get-Content .gitattributes | Select-Object -First 15

# 적용 확인 — text: set / eol: lf 로 나와야 함
git check-attr text eol -- "README.md"

# Office 임베디드 폰트가 binary 로 잡히는지 (정규화되면 문서가 깨짐)
git check-attr binary -- "projects/2026 연세대/히스토리/unpacked_v1/word/fonts/font1.odttf"

# 압축 해제물이 -text(정규화 금지)로 잡히는지
git check-attr text -- "projects/2026 연세대/히스토리/unpacked_v1/word/document.xml"
```

### 실행

```powershell
git config core.autocrlf false          # .gitattributes 가 우선하도록 명시
git fetch origin --prune

# ⚠️ 브랜치 이동 전 untracked 충돌 파일 비켜두기
#    현재 브랜치에서 untracked 인데 origin/main 에는 tracked 인 파일이 있어
#    그대로 switch 하면 git 이 거부합니다.
New-Item -ItemType Directory -Force -Path ..\_untracked_backup | Out-Null
Copy-Item ".\projects\260720 롯데이커머스 전사교육\롯데이커머스_3트랙_교육과정_소개.html" `
  ..\_untracked_backup -Force

# main 을 origin/main 으로 따라잡기 (로컬 main 이 35 커밋 뒤처져 있음)
git switch main
git merge --ff-only origin/main         # ff-only 라 이력이 꼬이지 않음

git switch -c chore/gitattributes-eol-normalize
git add .gitattributes
git add --renormalize .                 # 인덱스만 갱신. 워킹트리 파일 내용은 안 바뀝니다
```

> ⚠️ `git switch main` 이 실패하면: 에러에 적힌 untracked 파일을 `..\_untracked_backup` 으로 옮긴 뒤 재시도하세요. **"local changes would be overwritten"** 이 나오면 그 파일이 삼성전자MX 작업물일 수 있습니다 → 아래 분기 참조.

### 분기 — 삼성전자MX 미커밋 작업물이 걸릴 경우

현재 브랜치 `proposal/c-25a4c40d/20260813-1806-review-영광`에 삼성전자MX 임원세미나 작업물이 커밋되지 않은 상태입니다(실제 변경 61건 중 다수 + 삭제 11건 + 신규 하위 폴더 `context/` `internal/` `gates/` `state/` `sessions/`).

```powershell
git switch proposal/c-25a4c40d/20260813-1806-review-영광
git add -A "projects/260811_삼성전자MX_임원대상_세미나"
git status --short | Select-Object -First 30      # ⚠️ 무엇이 담기는지 눈으로 확인
git diff --cached --stat | Select-Object -Last 1
git commit -m "review 260811_삼성전자MX_임원대상_세미나 — 폴더 구조 정리 및 내부 검증 산출물 이동"
git push
# 그 다음 STEP 1 처음으로 복귀
```

> ⚠️ `.gitattributes` 적용 전 커밋이므로 개행 변경이 섞입니다. 삼성 폴더에 한정되므로 감수 가능합니다.

### 커밋 및 push

```powershell
git diff --cached --stat | Select-Object -Last 1   # 몇 건이 담기는지 확인
git commit -m "chore: .gitattributes 도입 및 개행 LF 정규화 (CRLF 노이즈 731건 해소)"
git push -u origin chore/gitattributes-eol-normalize
gh pr create --base main --title "chore: .gitattributes 도입 및 개행 LF 정규화" --body-file docs\_PR1_BODY.md
```

### 실행 후 검증

```powershell
git status --porcelain | Measure-Object -Line      # 841 → 약 110 이어야 함
git check-attr text eol -- "README.md"            # text: set / eol: lf
# 바이너리가 깨지지 않았는지 표본 확인 (파일 크기가 그대로여야 함)
git diff --stat HEAD~1 -- "*.odttf" | Select-Object -Last 1   # 출력 없으면 정상
```

### 되돌리기

```powershell
git switch main
git branch -D chore/gitattributes-eol-normalize
git push origin --delete chore/gitattributes-eol-normalize    # push 했다면
```

---

# STEP 2 — PR ②: `.gitignore` 보강 + 추적 해제 + 문서·코드 수정

> 소요 30~40분 · **562건 추적 해제 포함. 커밋을 3개로 나눕니다.**

### 실행 전 확인

```powershell
git switch main
git fetch origin --prune
git merge --ff-only origin/main          # PR ① 머지 후라면 최신화
git switch -c chore/repo-hygiene-260821

# 제거 대상 목록을 파일로 남겨 눈으로 확인
git -c core.quotePath=false ls-files |
  Select-String -Pattern 'unpacked_v' |
  Tee-Object -FilePath ..\_rm_cached_preview.txt |
  Measure-Object -Line                   # 약 562건

# ⚠️ 원본 문서가 추적되고 있는지 재확인 (없으면 제거 금지)
git -c core.quotePath=false ls-files "projects/2026 연세대/히스토리" |
  Select-String '\.(docx|xlsx|pdf)$'     # 30건 나와야 함
```

### 2-A. `.gitignore` 보강 (커밋 1/3)

기존 70줄을 유지하고 **파일 끝에 append** 합니다.

```powershell
@'

# ─────────────────────────────────────────────────────────
# 보강 (2026-08-21) — 하위 경로 누출 및 압축 해제물 차단
# ─────────────────────────────────────────────────────────

# ① AI 에이전트 설정을 하위 경로까지 적용
#    기존 `.claude/*` 는 루트에만 걸려 projects/*/.claude 가 새어나갔다
**/.claude/*
!**/.claude/skills/
!**/.claude/settings.json
**/.claude/worktrees/

# ② Office 파일 압축 해제물 (원본 .docx/.xlsx 만 관리)
**/unpacked_v*/

# ③ 임시·상태 파일
tmp_commit_msg.txt
template_dump.txt
openclaw-workspace-state.json

# ④ Google Drive 포인터 파일
*.gsheet
*.gdoc
*.gslides

# ⑤ 에이전트 세션 로그 (개인 대화 기록. memory/clients/ 는 팀 자산이라 제외 안 함)
memory/20??-??-??-*.md
'@ | Add-Content -Encoding UTF8 .gitignore

git status --porcelain | Measure-Object -Line     # 약 110 → 약 95 확인
git add .gitignore
git commit -m "chore: .gitignore 하위 경로 패턴 보강 및 압축 해제물·세션 로그 제외"
```

**넣지 않은 것과 이유**

| 제외한 후보 | 이유 |
|---|---|
| `openwiki/` | `openwiki-update.yml`이 매일 PR로 갱신하는 **팀 산출물**. ignore하면 CI와 싸움 |
| `memory/clients/` | 고객 정보 팀 자산(공영홈쇼핑·대덕전자·삼성전자MX + 템플릿). `memory/20??-??-??-*.md` 패턴으로 세션 로그만 좁혀 제외 |
| `**/_rels/` `**/word/` 등 개별 패턴 | `**/unpacked_v*/` 하나로 충분. 넓은 패턴은 정상 폴더를 오차단할 위험 |

### 2-B. 추적 해제 `git rm --cached` (커밋 2/3)

> ⚠️ **`--cached`가 핵심입니다.** 이 옵션이 있으면 **워킹트리 파일은 그대로 남고** git 추적만 해제됩니다. 빠뜨리면 **실제 파일이 삭제됩니다.**

```powershell
# ── 2-B-1. 개인 설정 파일 (기존 .gitignore 주석은 "제외 대상"이라 하는데 실제로는 추적 중)
git ls-files .claude/settings.local.json          # 확인
git rm --cached .claude/settings.local.json

# ── 2-B-2. Google Drive 포인터
git -c core.quotePath=false ls-files | Select-String '\.gsheet$'
git rm --cached "projects/KCB/강사목록_KCB.gsheet"

# ── 2-B-3. ⚠️ 위험: 압축 해제물 562건. 위 "실행 전 확인"의 원본 30건을 확인한 뒤에만.
git rm -r --cached "projects/2026 연세대/히스토리/unpacked_v1"
Get-ChildItem "projects/2026 연세대/히스토리" -Directory -Filter "unpacked_v*" |
  ForEach-Object { git rm -r --cached "projects/2026 연세대/히스토리/$($_.Name)" }

# ── 검증: 워킹트리 파일이 살아 있는지 (반드시 확인)
Test-Path "projects\2026 연세대\히스토리\unpacked_v1\word\document.xml"   # True 여야 함
git status --short | Select-Object -First 15
git diff --cached --stat | Select-Object -Last 1                          # 약 562 deletions

git commit -m "chore: Office 압축 해제물·개인 설정·Drive 포인터 파일 git 추적 해제 (원본 docx 30건은 유지)"
```

### 2-C. 문서·코드 수정 (커밋 3/3)

**① `AGENTS.md` — 코드와 문서 불일치 정정**

`scripts/git_workflow.py` 65행은 `ALLOWED_EXTENSIONS = {".json", ".md", ".csv", ".html"}` 로 **확장자 화이트리스트**인데, `AGENTS.md`는 파일명 예시로 좁게 서술해 오해를 만듭니다.

`AGENTS.md`의 "PR 포함 파일 (자동 필터링)" 섹션에서 **포함** 목록을 아래로 교체:

```diff
  **포함** (Git 추적 대상):
- - `projects/{기업명}/요구조건.md`
- - `projects/{기업명}/제안서/content.json`
- - `projects/{기업명}/리서치_{기업명}.md`
- - `projects/{기업명}/*_견적서.md`, `*_견적서.csv`
- - `projects/{기업명}/*_이메일_초안.html`
+ - `projects/{기업명}/` 아래 확장자 **`.md` `.json` `.csv` `.html`** 전부
+   (실제 판정은 `scripts/git_workflow.py` 의 `ALLOWED_EXTENSIONS` 가 담당)
+   예: 요구조건.md · content.json · 리서치_*.md · *_견적서.md/.csv ·
+       *_이메일_초안.html · 커리큘럼·기획 문서 · 소개자료 HTML
```

**② `scripts/git_workflow.py` — 빌드 산출물 1건 추가 (1줄)**

`combined_render.html` 8건이 빌드 산출물인데 어느 제외 목록에도 없습니다.

```diff
- FORCE_EXCLUDE_NAMES = {"proposal_render.html"}
+ FORCE_EXCLUDE_NAMES = {"proposal_render.html", "combined_render.html"}
```

**③ 런북·재발 방지 규칙 커밋**

```powershell
git add AGENTS.md scripts/git_workflow.py
git add docs/GIT_정리_런북.md docs/GIT_저장소_진단기록_260821.md `
        docs/GITIGNORE_보강안.md docs/제안서_인덱스_홈페이지_기획안.md
git status --short
git diff --cached -- AGENTS.md scripts/git_workflow.py     # 변경 내용 눈으로 확인
git commit -m "docs: PR 포함 파일 규칙을 코드와 일치시키고 빌드 산출물 제외 보강 + git 정리 런북·진단기록 추가"
git push -u origin chore/repo-hygiene-260821
gh pr create --base main --title "chore: 저장소 위생 정리 (.gitignore·추적 해제·문서 정정)" --body-file docs\_PR2_BODY.md
```

### PR ②에 들어가는 파일 (총 8건)

| # | 경로 | 성격 |
|---|---|---|
| 1 | `.gitignore` | 하위 경로 패턴 보강 (커밋 1/3) |
| 2 | `.claude/settings.local.json` | 추적 해제 (커밋 2/3) |
| 3 | `projects/KCB/강사목록_KCB.gsheet` | 추적 해제 (커밋 2/3) |
| 4 | `projects/2026 연세대/히스토리/unpacked_v*/` **약 562건** | 추적 해제 (커밋 2/3) |
| 5 | `AGENTS.md` | ⚠️ **문서 문구 변경 — 리뷰 필요** (커밋 3/3) |
| 6 | `scripts/git_workflow.py` | 1줄 — `combined_render.html` 제외 추가 (커밋 3/3) |
| 7 | `docs/GIT_정리_런북.md` | 신규 — 실행 절차 (권위 문서) |
| 8 | `docs/GIT_저장소_진단기록_260821.md`<br>`docs/GITIGNORE_보강안.md`<br>`docs/제안서_인덱스_홈페이지_기획안.md` | 신규 — 진단 근거·배경 자료 3건 (롯데 폴더에서 `docs/`로 재배치) |

### 실행 후 검증

```powershell
git status --porcelain | Measure-Object -Line          # 약 85 (실제 작업 산출물만)
Test-Path "projects\2026 연세대\히스토리\unpacked_v1"   # True — 파일은 살아 있음
git check-ignore -v "projects/2026 연세대/히스토리/unpacked_v1/word/document.xml"   # ignore 규칙 매칭 확인
```

### 되돌리기

```powershell
git reset --soft HEAD~1              # 마지막 커밋만 취소 (파일 유지, 안전)
git restore --staged .               # 스테이징만 해제 (안전)
git switch main; git branch -D chore/repo-hygiene-260821
# 머지 후 되돌리려면 커밋 단위 revert (562건 삭제가 단독 커밋이라 깔끔)
git revert <추적해제_커밋해시>
```

---

# STEP 3 — PR ③: 롯데이커머스 산출물 커밋

> 소요 15~20분 · **`scripts/git_workflow.py` 사용 (규정 경로)**

**방법을 `git_workflow.py`로 확정한 이유**: `AGENTS.md` 규정 경로이고, `company-{key}` 라벨로 **같은 기업의 열린 PR을 자동으로 찾아 커밋을 누적**시켜 "기업당 활성 PR 1개" 규칙을 자동 준수합니다. 수동 `git add`로는 이 중복 방지가 안 됩니다.

### 실행 전 확인

```powershell
git switch main
git fetch origin --prune
git merge --ff-only origin/main

# ⚠️ 같은 기업의 열린 PR이 이미 있는지 먼저 확인 (있으면 새 PR을 만들지 않습니다)
gh pr list --label "company-c-6477ec02" --state open

# 계획만 출력 (실제 변경 없음). 브랜치명·company_key·대상 파일을 확인
python scripts\git_workflow.py begin `
  --company "260720 롯데이커머스 전사교육" --command review --author 영광 --dry-run
```

`company_key`는 `c-6477ec02`이며 브랜치는 `proposal/c-6477ec02/{YYYYMMDD-HHMM}-review-영광` 형식으로 자동 생성됩니다.

### 이 PR에 들어가는 파일 — 롯데 프로젝트 산출물 **5건**

경로 접두: `projects/260720 롯데이커머스 전사교육/`

| # | 파일 | 성격 |
|---|---|---|
| 1 | `CLAUDE.md` | 프로젝트 세션 인수인계 문서 |
| 2 | `롯데이커머스_전사AI교육_1-3차_통합기획_보고용.html` | 보고용 통합 문서 (12섹션) |
| 3 | `롯데e커머스_의사결정_대기목록.md` | 미결정 17건 · 견적 4시나리오 |
| 4 | `롯데e커머스_2차교육_운영기획안_v3.md` | 2차 상세 설계 |
| 5 | `롯데e커머스_3차교육_설계안_v1.md` | 3차 상세 설계 |

전부 `.md`·`.html`이라 `ALLOWED_EXTENSIONS = {".json", ".md", ".csv", ".html"}`에 걸려 **자동 스테이징**됩니다.

> 저장소 전체 관심사였던 3건(`GIT_저장소_진단기록_260821.md` · `GITIGNORE_보강안.md` · `제안서_인덱스_홈페이지_기획안.md`)은 **`docs/`로 재배치되어 PR ②에 포함**됩니다. STEP 0-3에서 롯데 폴더 사본을 삭제했으므로 이 PR에는 들어오지 않습니다.

> ⚠️ **가드**: 아래 명령이 무언가를 출력하면 STEP 0-3을 건너뛴 것입니다. 되돌아가서 삭제하십시오.
> ```powershell
> Get-ChildItem "projects\260720 롯데이커머스 전사교육" -Filter "GIT*","제안서_인덱스*"
> ```

### 실행

```powershell
python scripts\git_workflow.py begin `
  --company "260720 롯데이커머스 전사교육" --command review --author 영광

git status --short                    # 브랜치 이동 후 상태 확인

python scripts\git_workflow.py finish `
  --company "260720 롯데이커머스 전사교육" --command review --author 영광 `
  --message "1~3차 통합 기획 확정 — 2차 운영기획안 v3(멘토링+과제 구간, 세션 1회, 서면 3종) · 3차 설계안 v1(부서 단위 해커톤 8H) · 의사결정 17건 · 보고용 통합 HTML" `
  --drive-url "https://drive.google.com/drive/folders/1AHZ4x1qL4IZ46rexyy-AUxN4H9Hhxa20"
```

### 실행 후 검증

```powershell
git log --oneline -1
gh pr list --label "company-c-6477ec02"       # PR 생성/갱신 확인
python scripts\git_workflow.py status --company "260720 롯데이커머스 전사교육"
```

### 되돌리기

```powershell
git reset --soft HEAD~1
git switch main
git branch -D "proposal/c-6477ec02/..."       # 실제 생성된 브랜치명으로
gh pr close <PR번호>
```

---

# STEP 4 — 브랜치·worktree 정리

> 소요 20~30분 · **약 4GB 디스크 회수**

### 4-A. 죽은 worktree 정리

`git worktree list` 결과 **15개 전부 `prunable`(죽음)** 이고 활성 worktree는 없습니다.

```powershell
# ── 실행 전 확인: 목록을 눈으로 보세요
git worktree list                              # 전부 prunable 인지 확인

# ── 메타데이터 정리 (안전 — 파일을 지우지 않습니다)
git worktree prune -v

# ── ⚠️ 위험: 실제 디렉터리 삭제. 위 prune 후 목록이 비었는지 확인한 뒤에만.
#    .claude/worktrees/ 8개 = 약 4.0GB
Get-ChildItem .claude\worktrees -Directory |
  Select-Object Name, @{n='GB';e={ "{0:N2}" -f ((Get-ChildItem $_.FullName -Recurse -Force -EA SilentlyContinue | Measure-Object Length -Sum).Sum/1GB) }}
# 목록 확인 후:
Remove-Item .claude\worktrees -Recurse -Force

# 하위 경로 worktree 4곳도 동일하게 (경로를 눈으로 확인한 뒤)
#   projects\2026 연세대\.claude\worktrees\  (3곳)
#   projects\한기대\.claude\worktrees\  (1곳)
#   projects\현대자동차\현대자동차_최종 첨부자료\.claude\worktrees\  (1곳)
Get-ChildItem . -Recurse -Directory -Filter worktrees -Force -EA SilentlyContinue |
  Select-Object FullName
# 확인 후 개별 삭제
```

> **`C:\Users\Admin\AppData\Local\Temp\opencode\aegis-wt` — 정리 불필요 (확정)**
> 저장소 밖 Windows 임시 폴더이고 `git worktree prune`이 메타데이터를 이미 정리합니다. 디스크 영향도 무해하므로 **손대지 않습니다.**

**검증**: `git worktree list` 가 저장소 본체 1줄만 출력 / `git status` 에 이상 없음

### 4-B. 병합 완료 브랜치 삭제

로컬 52개 / 원격 43개. `proposal/*` 24 · `claude/*` 22 · `chore/*` 4 · `feat/*` 1 · `main`.

```powershell
git fetch origin --prune

# ── ⚠️ 실행 전 목록을 눈으로 확인하세요
git branch --merged origin/main --format="%(refname:short)" |
  Where-Object { $_ -notin @("main") } |
  Tee-Object -FilePath ..\_branches_to_delete.txt

# ── 삭제 (-d 는 미병합 브랜치를 거부하므로 -D 보다 안전)
Get-Content ..\_branches_to_delete.txt | ForEach-Object { git branch -d $_ }

# ── 병합 안 된 브랜치 확인 — 삭제하지 말고 남겨두세요
git branch --no-merged origin/main --format="%(refname:short)"
```

**`claude/*` 22개 처리 방침**: Claude Code가 자동 생성한 것이며 방금 정리한 죽은 worktree들이 이 브랜치들을 참조하고 있었습니다.

| 조건 | 처리 |
|---|---|
| `--merged origin/main` 목록에 있음 | 삭제 (위 명령에 포함됨) |
| `--no-merged` 목록에 있음 | **삭제 금지.** 미병합 작업이 남아 있을 수 있음 → `git log origin/main..<브랜치> --oneline`으로 내용 확인 후 개별 판단 |

**원격 브랜치**: 로컬 정리 후 GitHub 웹에서 머지된 PR의 브랜치를 삭제하거나 `git push origin --delete <브랜치>`. 원격은 팀 공유물이라 **한 번에 일괄 삭제하지 말고 머지 확인된 것만** 지우세요.

### 되돌리기

브랜치 삭제는 커밋을 지우지 않습니다. `git reflog`로 해시를 찾아 `git branch <이름> <해시>`로 복구 가능합니다(약 90일). worktree 디렉터리 삭제는 되돌릴 수 없으나 **모두 prunable 상태였고 브랜치 자체는 저장소에 남아 있어** 손실이 없습니다.

---

# STEP 5 — 재발 방지 설정

> 소요 10분 · 설정은 즉시, 문서화는 PR ②에 포함

### 5-A. 로컬 설정 (각 작업자 PC에서 1회)

```powershell
git config core.autocrlf false        # .gitattributes 우선
git config pull.ff only               # merge 커밋 남기지 않음
git config fetch.prune true           # fetch 시 죽은 원격 추적 자동 정리
```

### 5-B. `AGENTS.md`에 추가할 규칙 (PR ② 커밋 3/3에 포함)

```markdown
### 작업 위생 규칙 (2026-08 추가)

1. **작업 시작 전 반드시 동기화**
   `git fetch origin --prune && git switch main && git merge --ff-only origin/main`
   → 이 규칙이 없어 로컬 main이 origin/main보다 35 커밋 뒤처진 사례가 있었다.
2. **병합 후 브랜치 삭제** — squash merge 직후 로컬·원격 삭제.
   주 1회 `git branch --merged origin/main`으로 정리.
3. **개행은 `.gitattributes`가 관리** — `core.autocrlf`를 개인이 바꾸지 않는다.
4. **worktree는 사용 후 정리** — `git worktree prune` + 디렉터리 삭제.
   방치 시 저장소가 수 GB 단위로 비대해진다.
```

### 5-C. ⚠️ 근본 원인 제안 — 자동 PR hook이 계속 스킵되는 문제

`CLAUDE.md` 148~151행에 따르면 Stop hook은 **"변경된 기업이 2곳 이상이면 경고만 하고 넘어감"** 입니다. 지금처럼 수십 개 기업 폴더가 동시에 더러운 상태에서는 **hook이 영구히 스킵**되고, 그래서 커밋이 안 되고, 더러운 폴더가 더 늘어나는 악순환이 됩니다.

**제안 (코드 수정은 하지 않았습니다. 검토 후 별도 PR로)**

| 안 | 내용 | 장단 |
|---|---|---|
| **A (권고)** | 스킵 대신 **"가장 최근 수정된 기업 1곳만 처리"** — 나머지는 경고 목록으로 안내 | 악순환을 끊음. 매번 최소 1개는 정리됨 |
| B | 기업별로 순차 처리(N개 PR 생성) | 확실하지만 PR 폭증 위험 |
| C | 스킵 임계값을 환경변수로 (`PROPOSAL_HOOK_MAX_COMPANIES`) | 유연하나 근본 해결은 아님 |

**전제**: STEP 1~2로 더러운 폴더 수가 크게 줄면 hook이 정상 동작하기 시작합니다. 즉 **이 런북 실행 자체가 1차 처방**이고, A안은 재발 방지용입니다.

---

# 부록 A — PR ① 본문 (`docs/_PR1_BODY.md`로 저장)

```markdown
## 📝 변경 유형

- [ ] 🏢 기업 제안서 (setup/build/estimate)
- [x] 🔧 시스템/스크립트 변경
- [ ] 📚 문서/가이드
- [ ] 🎨 템플릿/CSS
- [ ] 🐛 버그 수정
- [ ] 🔥 긴급 핫픽스

## 📋 변경 요약

`.gitattributes`를 도입해 개행을 LF로 정규화합니다. 미커밋 841건 중 **731건(87%)이 "내용은 동일한데 개행만 다른" 허위 변경**이었고, 원인은 `core.autocrlf` 미설정 + `.gitattributes` 부재였습니다.

- 워킹트리는 모든 줄이 CRLF, git 인덱스는 LF → 전체 파일이 수정으로 표시됨
- `git diff --ignore-all-space --numstat` 결과 실제 내용 변경은 **61건**뿐
- `git add --renormalize .`로 인덱스만 갱신 (워킹트리 파일 내용은 변경 없음)

### 바이너리 보호 (중요)

| 대상 | 조치 | 이유 |
|---|---|---|
| **`.odttf` 153건** | `binary` | Office 임베디드 폰트. 정규화되면 문서 폰트가 깨짐 |
| `.hwpx` `.xlsx` `.docx` `.pptx` `.pdf` `.png` `.m4a` | `binary` | 변환 시 파일 손상 |
| `**/unpacked_v*/` `**/_rels/` `**/word/` `[Content_Types].xml` | `-text` (정규화 금지) | Office 재조립 시 바이트 일치 필요 |
| `.bat` `.cmd` `.ps1` | `eol=crlf` | `.bat`은 CRLF 아니면 실행 실패 |

## 🔗 관련 링크

- **작업자**: 영광
- **관련 문서**: `docs/GIT_정리_런북.md` (PR ②에 포함)

## ✅ 체크리스트

- [ ] `git status --porcelain` 건수 841 → 약 110 감소 확인
- [ ] `git check-attr text eol -- README.md` → `text: set` / `eol: lf`
- [ ] 바이너리 파일 diff 없음 확인 (`git diff --stat HEAD~1 -- "*.odttf"` 출력 없음)
- [ ] Office 문서 1건을 열어 정상 동작 확인
- [ ] 검토자 1명 이상 승인

## 🔍 리뷰 포인트

**이 PR은 파일 수가 매우 많습니다(약 731건).** 전부 개행만 바뀐 것이며 내용 변경은 없습니다. `git diff --ignore-all-space` 로 보면 비어 있어야 정상입니다.

**반드시 첫 번째로 머지되어야 합니다.** 다른 PR을 먼저 머지하면 그 파일들이 개행 변경과 섞여 실제 변경 내용을 추적할 수 없게 됩니다.
```

---

# 부록 B — PR ② 본문 (`docs/_PR2_BODY.md`로 저장)

```markdown
## 📝 변경 유형

- [ ] 🏢 기업 제안서 (setup/build/estimate)
- [x] 🔧 시스템/스크립트 변경
- [x] 📚 문서/가이드
- [ ] 🎨 템플릿/CSS
- [ ] 🐛 버그 수정
- [ ] 🔥 긴급 핫픽스

## 📋 변경 요약

저장소 위생 정리입니다. 커밋 3개로 분리했습니다.

**1/3 `.gitignore` 보강**
- `.claude/*`가 루트에만 적용되어 `projects/*/.claude/`, `templates/.claude/` 4곳이 누출 → `**/.claude/*`로 교체
- Office 압축 해제물(`**/unpacked_v*/`), 임시 파일 3종, Drive 포인터(`*.gsheet`), 에이전트 세션 로그(`memory/20??-??-??-*.md`) 제외
- ⚠️ `openwiki/`는 **제외하지 않았습니다** — `openwiki-update.yml`이 매일 PR로 갱신하는 팀 산출물
- ⚠️ `memory/clients/`는 **유지** — 고객 정보 팀 자산

**2/3 추적 해제 (`git rm --cached`, 워킹트리 파일은 유지)**
- `projects/2026 연세대/히스토리/unpacked_v*/` **약 562건** — 원본 `.docx` 30건(`연세AX_제안서_모두의연구소_v10~v16` 등)이 함께 추적되고 있어 파생물 제거가 안전함을 확인
- `.claude/settings.local.json` 1건 — 기존 `.gitignore` 주석은 제외 대상이라 하는데 실제로는 추적 중이었음
- `projects/KCB/강사목록_KCB.gsheet` 1건

**3/3 문서·코드 정정 + 런북 추가**
- **⚠️ 문서 문구 변경 — 리뷰 필요**: `AGENTS.md`의 "PR 포함 파일" 목록이 실제 코드와 불일치. `git_workflow.py`는 `ALLOWED_EXTENSIONS = {".json", ".md", ".csv", ".html"}` 확장자 화이트리스트인데 문서는 파일명 예시로 좁게 서술해 오해를 유발했습니다(실제로 이 오해로 작업 중 잘못된 판단이 있었음). 코드 기준으로 문서를 맞춥니다.
- `scripts/git_workflow.py` 1줄: `FORCE_EXCLUDE_NAMES`에 `combined_render.html` 추가 (빌드 산출물 8건이 어느 제외 목록에도 없었음)
- **문서 4건 추가 (그중 3건은 재배치)**
  - `docs/GIT_정리_런북.md` — 신규. 실행 절차 **권위 문서**
  - `docs/GIT_저장소_진단기록_260821.md` — 롯데 프로젝트 폴더의 `GIT_브랜치_전략_및_작업절차.md`를 **개명 이동**. 절차 중복을 없애려 C·D장을 "런북으로 대체됨"으로 표기하고 진단 근거(A·B장)만 유효화
  - `docs/GITIGNORE_보강안.md` — 롯데 폴더에서 **이동**. `.gitignore` 판정 근거
  - `docs/제안서_인덱스_홈페이지_기획안.md` — 롯데 폴더에서 **이동**. 별도 안건(보류 상태) 기획안
  - 이동 이유: 저장소 전체 관심사 문서가 특정 고객사 폴더에 있으면 발견되지 않고, PR ③의 리뷰 범위를 흐립니다

## 🔗 관련 링크

- **작업자**: 영광
- **선행 PR**: PR ① (`.gitattributes` 개행 정규화) — **먼저 머지되어야 합니다**

## ✅ 체크리스트

- [ ] `Test-Path "projects\2026 연세대\히스토리\unpacked_v1\word\document.xml"` → **True** (워킹트리 파일 생존 확인)
- [ ] 원본 `.docx` 30건이 여전히 추적됨 확인
- [ ] `git status --porcelain` 약 110 → 약 85 감소
- [ ] `git check-ignore -v` 로 새 패턴 매칭 확인
- [ ] **`AGENTS.md` 문구 변경 검토** ← 리뷰어 확인 필요
- [ ] `scripts/git_workflow.py` 1줄 변경이 hook·CI에 영향 없음 확인
- [ ] 검토자 1명 이상 승인

## 🔍 리뷰 포인트

**1. `AGENTS.md` 문구 변경은 팀 규칙 문서 변경입니다.** 코드와 일치시키는 방향이지만, 의도적으로 좁게 써둔 것이라면 반대로 **코드를 문서에 맞춰 좁히는** 선택도 가능합니다. 판단 부탁드립니다.

**2. ⚠️ `openwiki-update.yml`의 `add-paths`에 `AGENTS.md`·`CLAUDE.md`가 포함되어 있습니다.** 자동 `openwiki/update` PR과 충돌할 수 있습니다. 충돌 시 openwiki PR을 먼저 머지하고 rebase하세요.

**3. 562건 삭제는 단독 커밋입니다.** 문제가 생기면 `git revert <해시>` 한 번으로 되돌아갑니다.

**4. `git rm --cached`만 사용했습니다.** 워킹트리 파일은 하나도 지워지지 않았습니다.
```

---

# 부록 C — PR ③ 본문

`scripts/git_workflow.py finish`가 `PR_BODY_TEMPLATE`으로 본문을 **자동 생성**합니다. 아래는 생성 후 GitHub에서 덧붙일 리뷰 포인트입니다.

```markdown
## 🔍 리뷰 포인트

**이 PR은 "설계 확정"이지 "견적 확정"이 아닙니다. 미결정 17건이 대기 중입니다.**

특히 아래 3건이 정해지지 않으면 고객에게 제안서를 낼 수 없습니다.
- **예산 기준선** — 고객 잠정 5,000만 / 협의예산 3,510만(1차 한정) / 마스터시트 계약총액 2억 5,317만
- **3차 시간 12H vs 8H** — 고객 회신에 "인당 4h × 3번 = 12시간"이 명시돼 있어 **8H는 정면 충돌**입니다. 협의 논리 5개를 문서에 정리했으나 수용 여부는 미확인
- **3차 대상 350명 전원 vs 120명 선별** — 3차가 전체 견적의 60%. 축소하면 "전원 3차" 요구와 충돌

**요구조건 충족 현황**: 충족 14 / 부분충족 2 / 협의필요 3 / **정면충돌 1**

**예산**: 1·2차 합계만 ₩71,675,000으로 고객 잠정 예산 5,000만원을 초과. 전체 ₩180,575,000. 원가율은 전 단계 30% 가드레일 통과(1차 27.4% / 2차 17.2% / 3차 26.4%).

**설계 판단 2건 — 고객 확인이 필요합니다**
1. **2차 관리 단위를 개인으로 전환** — 고객 회신은 "팀에서 1개 과제, 3~5인 그룹"이지만 1차 산출물이 "1인 1 Gems"라 팀으로 묶으면 산출물 대부분이 방치됩니다. 3층 분리(과제 소유=개인 / 관리 묶음=에이전트 유형 / 성과·확산=부서)로 재해석하고 팀 요구는 3차 부서 내 3~5인 팀으로 충족시켰습니다.
2. **아카이빙 주체를 고객사로 이전(보안)** — 모두연이 350건 에이전트 정보를 취합·카탈로그화하는 구조를 폐기하고, 3차 실습으로 고객사 부서가 직접 구축하게 했습니다.

**동일 산출물 4건이 Google Drive에도 업로드되어 있습니다** (바이트 단위 무결성 검증 완료).
```

---

# 부록 D — 최종 검증 체크리스트

세 PR 모두 머지된 뒤 실행:

```powershell
cd C:\Users\Admin\Downloads\ai-education-proposal
git fetch origin --prune
git switch main
git merge --ff-only origin/main

git status --porcelain | Measure-Object -Line     # 목표: 100 미만
git branch --list | Measure-Object -Line           # 52 → 대폭 감소
git worktree list                                  # 본체 1줄만
git check-attr text eol -- "README.md"             # text: set / eol: lf
git config core.autocrlf                           # false
"{0:N1} GB" -f ((Get-ChildItem . -Recurse -Force -EA SilentlyContinue | Measure-Object Length -Sum).Sum/1GB)
```

| 지표 | 시작 | 목표 |
|---|---|---|
| 미커밋 건수 | 841 | **100 미만** |
| 로컬 브랜치 | 52 | 정리 후 확인 |
| worktree | 15 (전부 죽음) | **1 (본체)** |
| 저장소 용량 | — | **약 4GB 감소** |
| `main` vs `origin/main` | 35 뒤처짐 | **동기화** |
