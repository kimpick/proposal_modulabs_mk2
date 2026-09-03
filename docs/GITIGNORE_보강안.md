# .gitignore 보강안 (제안)

작성: 2026-08-21 · 대상 `C:\Users\Admin\Downloads\ai-education-proposal\.gitignore`
**이 문서는 제안입니다. 기존 `.gitignore`를 직접 수정하지 않았습니다.**

---

## 0. 요약

| 항목 | 값 |
|---|---|
| 기존 `.gitignore` | 70줄, 존재 |
| 추가 제안 패턴 | **6개 그룹 · 24줄** |
| 예상 효과 | 신규(`??`) 38건 중 **약 20건 소멸**, 향후 재발 방지 |
| ⚠️ 주의 | 추가 패턴 중 **3개 그룹은 이미 추적 중인 파일**과 겹칩니다 → `.gitignore`만으로는 안 빠지고 `git rm --cached`가 필요합니다 (3장) |

---

## 1. 기존 `.gitignore`의 구조적 문제 2가지

### 문제 ① `.claude/*` 패턴이 루트에만 적용됨

```gitignore
# 현재 (70줄 중)
.claude/*
!.claude/skills/
!.claude/settings.json
```

`.claude/*`는 **저장소 루트의 `.claude/`만** 무시합니다. 그래서 아래가 전부 새어나옵니다.

| 새어나온 경로 | 상태 |
|---|---|
| `projects/2026 연세대/.claude/` | 신규(??) |
| `projects/260811_삼성전자MX_임원대상_세미나/.claude/` | 신규(??) |
| `projects/도쿄일렉트론코리아/.claude/` | 신규(??) |
| `templates/.claude/` | 신규(??) |

> 참고: `.claude/worktrees/` 안에 고객사 폴더 사본이 6개 있습니다(`affectionate-kowalevski-dcf022` 등). Claude Code worktree 잔여물로 보이며, 이것도 무시 대상입니다.

### 문제 ② Office 파일 압축 해제물이 추적되고 있음

`origin/main`이 아래를 **이미 추적 중**입니다 — 전부 `projects/2026 연세대/히스토리/unpacked_v1/` 아래입니다.

| 경로 패턴 | 추적 건수 |
|---|---|
| `word/` | **486** |
| `_rels/` | 68 |
| `[Content_Types].xml` | 16 |
| **소계** | **약 570건** |

`.docx`를 풀어놓은 것이므로 **원본 `.docx`만 관리하면 됩니다.** 이 570건이 "수정 792건" 중 상당 부분(특히 `.xml` 270건 · `.rels` 68건)의 정체입니다.

---

## 2. 추가 제안 패턴 (diff 형태)

기존 70줄을 그대로 두고 **파일 끝에 아래를 append**하는 방식입니다.

```diff
--- a/.gitignore
+++ b/.gitignore
@@ (파일 끝에 추가) @@
+
+# ─────────────────────────────────────────────────────────
+# 보강 (2026-08-21) — 하위 경로 누출 및 압축 해제물 차단
+# ─────────────────────────────────────────────────────────
+
+# ① AI 에이전트 설정을 하위 경로까지 적용
+#    기존 `.claude/*` 는 루트에만 걸려 projects/*/.claude 가 새어나갔다
+**/.claude/*
+!**/.claude/skills/
+!**/.claude/settings.json
+**/.claude/worktrees/
+
+# ② Office 파일 압축 해제물 (원본 .docx/.pptx/.xlsx 만 관리)
+**/unpacked_v*/
+**/_rels/
+**/word/
+**/ppt/
+**/xl/
+**/docProps/
+**/customXml/
+**/[Content_Types].xml
+
+# ③ 임시·상태 파일
+tmp_commit_msg.txt
+template_dump.txt
+openclaw-workspace-state.json
+
+# ④ OpenWiki 생성물 (GitHub Action이 PR로 갱신 — 로컬 사본은 제외)
+#    ⚠️ 아래는 판단 필요. openwiki/ 를 팀 공유 대상으로 유지하려면 이 줄을 빼세요.
+# openwiki/
+
+# ⑤ Google Drive 포인터 파일
+*.gsheet
+*.gdoc
+*.gslides
+
+# ⑥ 에이전트 세션 메모 (개인 로컬 기록)
+#    ⚠️ 아래는 판단 필요. memory/ 를 팀 공유 대상으로 유지하려면 이 줄을 빼세요.
+# memory/2*.md
```

### 그룹별 판정

| # | 그룹 | 추적 중? | 조치 |
|---|---|---|---|
| ① | `**/.claude/*` | **일부 추적** (`.claude/settings.local.json`) | ignore 추가 + `git rm --cached` (3-1) |
| ② | Office 압축 해제물 | **약 570건 추적** | ignore 추가 + `git rm --cached` (3-2) |
| ③ | 임시 파일 3종 | 미추적 | **ignore만 추가하면 끝** |
| ④ | `openwiki/` | 미추적 | ⚠️ **판단 필요** — 아래 참조. 기본은 주석 처리 |
| ⑤ | `*.gsheet` | **1건 추적** (`projects/KCB/강사목록_KCB.gsheet`) | ignore 추가 + `git rm --cached` (3-3) |
| ⑥ | `memory/2*.md` | **3건 추적** | ⚠️ **판단 필요.** 기본은 주석 처리 |

### ⚠️ ④ `openwiki/` 는 무시하면 안 될 가능성이 높습니다

`.github/workflows/openwiki-update.yml`이 **매일 08:00 UTC에 `openwiki code --update`를 돌려 PR을 생성**합니다. 즉 `openwiki/`는 CI가 관리하는 **팀 공유 산출물**입니다. 로컬에서 신규(`??`)로 잡힌 것은 아직 그 PR이 머지되지 않았거나 로컬이 origin/main보다 35 커밋 뒤처져서일 수 있습니다.

**권고: ④는 추가하지 마세요.** (제안 diff에서 주석 처리해 뒀습니다)

### ⚠️ ⑥ `memory/` 도 판단이 필요합니다

`origin/main`이 `memory/` 3건을 추적 중입니다. 로컬 신규 6건(`memory/2026-06-*.md`)이 개인 세션 메모인지, 팀 공유 자산인지에 따라 갈립니다. `memory/clients/삼성전자MX.md`처럼 고객 정보가 들어가는 경로도 있어 **일괄 ignore는 위험**합니다.

**권고: ⑥도 추가하지 말고, 6건을 개별 확인 후 커밋 여부를 정하세요.**

---

## 3. ⚠️ 이미 추적 중인 파일을 빼는 명령 (`git rm --cached`)

`.gitignore`는 **아직 추적되지 않은 파일**만 막습니다. 이미 추적 중인 파일은 아래처럼 인덱스에서만 제거해야 합니다.

> **`--cached`가 핵심입니다.** 이 옵션이 있으면 **워킹트리 파일은 지워지지 않고** git 추적만 해제됩니다. 빠뜨리면 실제 파일이 삭제됩니다.

### 3-1. `.claude/settings.local.json` (개인 설정)

기존 `.gitignore` 주석에 "`settings.local.json`은 개인용이라 계속 git 제외 대상"이라고 적혀 있으나 **실제로는 추적되고 있습니다** (과거에 커밋된 것으로 보임).

```powershell
# 확인
git ls-files .claude/settings.local.json

# 추적 해제 (파일은 디스크에 남음)
git rm --cached .claude/settings.local.json
```

### 3-2. Office 압축 해제물 약 570건 (⚠️ 가장 큰 변경)

```powershell
# ── 먼저 확인: 무엇이 빠지는지 목록으로 (실행 전 필수)
git ls-files | Select-String -Pattern 'unpacked_v|/_rels/|/word/|/ppt/|/xl/|/docProps/|Content_Types' |
  Tee-Object -FilePath ..\_rm_cached_preview.txt | Measure-Object -Line

# ── 원본 .docx 가 추적되고 있는지 확인 (없으면 절대 제거하면 안 됩니다)
git ls-files "projects/2026 연세대/히스토리" | Select-String '\.docx$'

# ⚠️ 위험: 위 두 확인을 통과한 뒤에만 실행하세요.
#    --cached 이므로 디스크 파일은 그대로 남습니다.
git rm -r --cached "projects/2026 연세대/히스토리/unpacked_v1"

# ── 확인
git status --short | Select-Object -First 20
```

> ⚠️ **원본 `.docx`가 추적되지 않는 상태에서 압축 해제물을 제거하면 이력이 사라집니다.** 위 두 번째 확인 명령으로 원본 존재를 먼저 확인하세요. 없으면 원본을 먼저 커밋한 뒤 제거하세요.

### 3-3. `*.gsheet` 1건

```powershell
git ls-files | Select-String '\.gsheet$'
git rm --cached "projects/KCB/강사목록_KCB.gsheet"
```

---

## 4. 권장 실행 순서

```
Phase 1 (개행 정규화)  ← 먼저. .gitattributes 커밋 + git add --renormalize
   ↓
Phase 2 (롯데 PR)      ← 이번 산출물
   ↓
Phase 4-a  .gitignore 보강 커밋 (①②③⑤만. ④⑥ 제외)
   ↓
Phase 4-b  git rm --cached 3건 (3-1 → 3-3 → 3-2 순서. 3-2가 가장 큼)
```

**`.gitattributes`(Phase 1)를 먼저 하는 이유**: 개행 정규화 없이 `git rm --cached`를 하면, 남은 파일들이 여전히 CRLF 허위 변경 상태라 diff가 뒤섞여 무엇이 실제 변경인지 구분되지 않습니다.

**②를 별도 커밋으로 분리하는 이유**: 570건 삭제는 되돌릴 일이 생길 수 있는 큰 변경입니다. 단독 커밋이면 `git revert` 한 번으로 복구됩니다.

---

## 5. 예상 효과

| 시점 | 미커밋 건수 (추정) |
|---|---|
| 현재 | **841** |
| Phase 1 (개행 정규화) 후 | 약 **110** |
| Phase 4-a (.gitignore ①②③⑤) 후 | 약 **90** |
| Phase 4-b (`git rm --cached`) 후 | 약 **85** (실제 작업 산출물만 남음) |

남는 약 85건은 **실제로 커밋해야 할 산출물**입니다 — 요구조건.md 다수, 삼성전자MX 임원세미나 폴더 리팩터링, 신규 프로젝트 폴더(대덕전자·SK마케팅·데이블), `docs/가로형_교육과정_소개자료_가이드.md`, `.claude/skills/curriculum-intro/` 등. 기업별로 나눠 `git_workflow.py`로 PR을 올리면 정리됩니다.

---

## 6. 미결정 — 확인 부탁드립니다

| # | 질문 | 선택지 |
|---|---|---|
| 1 | `openwiki/`를 git으로 관리합니까? | CI가 PR로 갱신하므로 **관리 권고**(ignore 추가 안 함) / 로컬 생성물로 보고 제외 |
| 2 | `memory/2026-06-*.md` 6건은 개인 메모입니까 팀 자산입니까? | 팀 자산이면 커밋 / 개인이면 ignore |
| 3 | `projects/2026 연세대/히스토리/unpacked_v1/` 원본 `.docx`가 어딘가 보관돼 있습니까? | 있으면 570건 제거 진행 / 없으면 원본 먼저 확보 |
| 4 | `.claude/worktrees/` 6개(고객사 폴더 사본 포함)는 삭제해도 됩니까? | Claude Code 잔여물이면 정리 / 진행 중 작업이면 보존 |
