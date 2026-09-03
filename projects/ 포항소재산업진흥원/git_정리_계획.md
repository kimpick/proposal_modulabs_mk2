# Git 브랜치 정리 · main 병합 계획

- **조사 일자** : 2026-07-31
- **저장소** : `kisdevan/propsal_modulabs`
- **실행 위치** : 터미널 (Cowork 샌드박스는 자격증명 없음 + `.git` 삭제 권한 없음)

---

## 요약

**main 병합은 가능하고, fast-forward라 충돌이 없습니다.** 현재 브랜치 `feat/tmux-hermes-dev-workspace`가 `origin/main`을 전부 품고 있습니다(behind 0 / ahead 15).

진짜 일거리는 브랜치가 아니라 **미커밋 1,163개 파일**입니다.

---

## 1. 브랜치 현황

| 브랜치 | main 대비 | 고유 내용 | 조치 |
|---|---|---|---|
| `feat/tmux-hermes-dev-workspace` (현재) | behind 0 / ahead 15 | 연세대 세미나 교안·OKF 파이프라인 등 | **main에 fast-forward** |
| `worktree-yonsei-aug-hackathon-plan` | behind 0 / ahead 4 | 연세대 8월 해커톤 계획안 v1.1~v2.1 | 병합 (충돌 없음) |
| `origin/proposal/c-1cc289a3/...setup-sisyphus` | behind 51 / ahead 1 | 이지스엔터프라이즈 제안서 (296줄) | cherry-pick |
| `origin/proposal/c-a382d2ca/...build-시시푸스` | behind 51 / ahead 1 | `docs/yonsei-ax/claude-setup.html` (999줄) | cherry-pick |
| `worktree-incheon-proposal-update-260710` | behind 46 / ahead 2 | 인천대 제안서 v2 (612줄) + 아카이브 이동 | rebase 후 병합 |
| `feat/...-recovered` | behind 61 / ahead 1 | ❌ 없음 — 내용이 이미 로컬 feat에 있음 | 삭제 |
| `origin/feat/tmux-hermes-dev-workspace` | behind 61 / ahead 1 | ❌ 없음 — 위와 동일 커밋(`5b137ee`) | 강제 갱신 or 삭제 |
| `origin/genspark_ai_developer` | behind 122 / ahead 0 | ❌ 없음 | 삭제 |
| `origin/project-wide-updates-20260713-...` | behind 99 / ahead 0 | ❌ 없음 | 삭제 |
| 로컬 `main` | behind 46 / ahead 0 | — | 갱신만 |

> **확인한 것** — `5b137ee`(tmux workspace + Hermes + Sheets MCP)는 로컬 feat에 커밋 해시로는 없지만 `.tmux.conf`, `scripts/dev.sh` 등 **파일 내용은 이미 들어 있습니다**(`33985e8`에서 재커밋된 것으로 보임). 그래서 `-recovered`와 원격 feat은 삭제해도 잃는 게 없습니다.

---

## 2. 미커밋 현황 — 실제 문제

- 경로 기준 **66건**, 파일 기준 **1,163개**
- 확장자 분포 : xml 270 · md 180 · odttf 153 · json 101 · png 85 · rels 68 · xlsx 54 · py 51 · docx 50 · html 38

### ⚠️ 먼저 걸러야 할 것 — 압축 풀린 Office 내부 파일

| 경로 | 파일 수 |
|---|---|
| `projects/2026 연세대/히스토리/` | 468 |
| `projects/현대카드/unpacked_draft/` | 23 |

`word/`, `docProps/`, `_rels/`, `.odttf`(임베디드 폰트)가 그대로 있습니다. docx를 풀어 놓은 작업 잔여물이므로 커밋하면 안 됩니다. **약 491개 파일이 여기서 빠집니다.**

---

## 3. 실행 절차

### Phase 0 — lock 제거 + 안전망

```bash
cd "/Users/maron/ModualbsProposal 2"
rm -f .git/index.lock                   # ⚠️ Cowork 세션이 남긴 것. 없으면 git add가 전부 막힘
git tag backup/pre-cleanup-260731 feat/tmux-hermes-dev-workspace
git branch backup/feat-260731 feat/tmux-hermes-dev-workspace
```

### Phase 1 — 잔여물 .gitignore 추가

```bash
cat >> .gitignore <<'EOF'

# 압축 해제된 Office 내부 파일 (작업 잔여물)
**/unpacked_draft/
projects/2026 연세대/히스토리/
*.odttf
EOF
git add .gitignore && git commit -m "chore: 압축 해제된 Office 내부 파일 gitignore 추가"
```

> ✅ `projects/2026 연세대/히스토리/` 는 통째로 제외해도 된다고 확인받음 (2026-07-31). 별도 백업 불필요.

### Phase 2 — 카테고리별 커밋

`git add .` 금지. 아래 순서로 나눠서 진행합니다.

```bash
# 1) 이번 건
git add "projects/ 포항소재산업진흥원/"
git commit -m "docs: 포항 임베디드 Claude 교육 8차수 커리큘럼·제안 덱 추가"

# 2) 기업 프로젝트
git add projects/KCB projects/KCB_코리아크레딧뷰로 projects/KCH \
        projects/LGE projects/LG전자 projects/NIA projects/현대카드 \
        projects/삼성전자MX_* projects/삼성전자_*
git commit -m "docs: 기업 프로젝트 제안·산출물 정리 (KCB·KCH·LGE·NIA·현대카드·삼성전자)"

# 3) 대학·공공
git add "projects/2026 연세대" projects/인천대학교 projects/한기대 \
        projects/전주대학교_* projects/한국고려사 projects/한국도로공사 \
        projects/서울강북청년센터 projects/안산마음건강센터
git commit -m "docs: 대학·공공 프로젝트 제안 산출물 정리"

# 4) 나머지 projects
git add projects/
git commit -m "docs: 잔여 프로젝트 폴더 정리"

# 5) 템플릿·문서·자동화
git add templates/
git commit -m "chore: 제안서·견적 템플릿 추가"
git add docs/
git commit -m "docs: 라벨 배지·제안서 생성·커리큘럼 검토 가이드 추가"
git add automation/
git commit -m "chore: 메일 발송 자동화 스크립트 정리"

# 6) 루트 레퍼런스
git add "공고문 레퍼런스" "제안서 레퍼런스"
git commit -m "docs: 공고문·제안서 레퍼런스 자료 추가"

# 7) 남은 것 확인 후 마무리
git status --short
```

> 폴더명이 자소 분리(NFD)로 저장돼 있어 탭 자동완성이 어긋날 수 있습니다. 안 먹으면 `git add "projects/"` 로 한 번에 잡고 `git status`로 확인하세요.

### Phase 3 — main 병합 (fast-forward)

```bash
git checkout main
git pull --ff-only origin main          # 로컬 main 46 behind 해소
git merge --ff-only feat/tmux-hermes-dev-workspace
git push origin main
```

`--ff-only`가 통과하면 충돌 없이 끝난 것입니다. 실패하면 Phase 2에서 뭔가 어긋난 것이니 멈추고 확인하세요.

### Phase 4 — 나머지 브랜치 흡수

```bash
# 연세대 해커톤 (behind 0 — 깔끔)
git merge worktree-yonsei-aug-hackathon-plan
git push origin main

# 이지스 제안서 + yonsei-ax claude-setup (커밋 1개씩)
git fetch origin
git cherry-pick 608a413      # 이지스엔터프라이즈 제안서
git cherry-pick 01ab968      # docs/yonsei-ax/claude-setup.html
git push origin main

# 인천대 (base가 46커밋 낡음 — rebase 필요)
git rebase main worktree-incheon-proposal-update-260710
git checkout main && git merge --ff-only worktree-incheon-proposal-update-260710
git push origin main
```

> 인천대 브랜치는 잠긴 worktree(`.claude/worktrees/incheon-proposal-update-260710`)에 체크아웃돼 있습니다. rebase가 거부되면 그 worktree 안에서 실행하거나 `git worktree unlock` 후 진행하세요.

### Phase 5 — 브랜치 삭제

```bash
# 원격 — 고유 내용 없음
git push origin --delete genspark_ai_developer
git push origin --delete project-wide-updates-20260713-0f8d6e8
git push origin --delete feat/tmux-hermes-dev-workspace

# 원격 — cherry-pick 완료 후
git push origin --delete proposal/c-1cc289a3/20260630-0948-setup-sisyphus
git push origin --delete "proposal/c-a382d2ca/20260625-1516-build-시시푸스"

# 로컬
git branch -d feat/tmux-hermes-dev-workspace-recovered
git branch -d feat/tmux-hermes-dev-workspace
git branch -d worktree-yonsei-aug-hackathon-plan
git worktree list                      # 잠긴 worktree 정리 여부 확인
```

정리 후 `main` + 백업 태그 1개만 남습니다.

---

## 4. 되돌리기

```bash
git reset --hard backup/pre-cleanup-260731
```

원격에 이미 push한 뒤라면 `git push --force-with-lease origin main`. **다른 사람이 그 사이 push했으면 위험하니** 혼자 쓰는 저장소인지 먼저 확인하세요.
