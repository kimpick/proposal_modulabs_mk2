#!/usr/bin/env bash
# scripts/dev.sh — 기업별 tmux 4-pane 워크스페이스 런처
# Usage: scripts/dev.sh {기업명} [과정명]
#
# 생성되는 워크스페이스 (tmux 세션 = 기업명):
#
#   ┌──────────────────────┬──────────────────────┐
#   │ 1. Watcher           │ 2. Validation + Git  │
#   │    (content.json     │    (content.json     │
#   │     변경 시 자동 빌드)│     검증 + git 상태) │
#   │                      │                      │
#   ├──────────────────────┼──────────────────────┤
#   │ 3. 버전 히스토리      │ 4. Hermes AI 에이전트 │
#   │    (versions, PDF)    │    (대화형 리뷰)     │
#   └──────────────────────┴──────────────────────┘
#
# 단축키 (Ctrl+B prefix):
#   Ctrl+B, r      tmux.conf 리로드
#   Ctrl+B, |  또는 -    pane 분할 (좌우/위아래)
#   Ctrl+B, h/j/k/l     pane 이동 (vim 스타일)
#   Ctrl+B, B      현재 기업 빌드
#   Ctrl+B, V      content.json 검증
#   Ctrl+B, G      git status

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

COMPANY="${1:-}"
COURSE="${2:-}"

# ── 인자 검증 ────────────────────────────────────────────────────
if [[ -z "$COMPANY" ]]; then
  cat <<'USAGE'
Usage: scripts/dev.sh {기업명} [과정명]

기업 폴더 목록:
USAGE
  ls -1 projects/ 2>/dev/null | grep -v "^_" | sed 's/^/  - /' | head -30
  exit 1
fi

if [[ ! -d "projects/$COMPANY" ]]; then
  echo "❌ 기업 폴더 없음: projects/$COMPANY"
  echo ""
  echo "기존 폴더:"
  ls -1 projects/ 2>/dev/null | grep -v "^_" | sed 's/^/  - /' | head -20
  exit 1
fi

# ── 작업자 자동 감지 ─────────────────────────────────────────────
detect_author() {
  case "${SLACK_USER_ID:-}" in
    U0924H9HSK1) echo "영광"; return ;;
    U03RP0HEZDW) echo "은숙"; return ;;
    U093RP4EZMK) echo "은경"; return ;;
  esac
  local git_user
  git_user=$(git config user.name 2>/dev/null || echo "")
  echo "${git_user:-작업자}"
}
AUTHOR=$(detect_author)

# ── 의존성 체크 ──────────────────────────────────────────────────
for cmd in tmux python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "❌ 필수 명령어 미설치: $cmd"
    [[ "$cmd" == "tmux" ]] && echo "   설치: brew install tmux"
    exit 1
  fi
done

# ── 작업 경로 결정 ───────────────────────────────────────────────
if [[ -n "$COURSE" ]]; then
  WORKDIR="$PROJECT_ROOT/projects/$COMPANY/$COURSE"
  if [[ ! -d "$WORKDIR" ]]; then
    echo "❌ 과정 폴더 없음: $WORKDIR"
    echo ""
    echo "기존 과정:"
    ls -1 "projects/$COMPANY/" 2>/dev/null | sed 's/^/  - /'
    exit 1
  fi
else
  WORKDIR="$PROJECT_ROOT/projects/$COMPANY"
fi

SESSION="$COMPANY"

# ── 세션 중복 체크 ───────────────────────────────────────────────
if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "⚠️  세션 '$SESSION' 이미 실행 중"
  if [[ -t 1 ]]; then
    exec tmux attach -t "$SESSION"
  else
    echo "   tmux attach -t $SESSION"
    exit 0
  fi
fi

echo "🚀 워크스페이스 생성 중: $SESSION"
echo "   작업자: $AUTHOR"
echo "   경로  : $WORKDIR"
echo ""

# ── 4-pane 워크스페이스 생성 ─────────────────────────────────────
tmux new-session -d -s "$SESSION" -c "$WORKDIR" -n "main"
W="$SESSION:main"

# .tmux.conf 를 먼저 로드해야 base-index, pane-base-index 가 적용됨
if [[ -f "$PROJECT_ROOT/.tmux.conf" ]]; then
  tmux source-file "$PROJECT_ROOT/.tmux.conf" 2>/dev/null || true
fi

# Pane 배치:
#   ┌─────────────────────────────────────────────┐
#   │ 1 Watcher           (전체 너비, 상단 30%)     │
#   ├──────────────────────────┬──────────────────┤
#   │ 2 Hermes chat            │ 3 Status         │
#   │   (좌측 하단, 넓게)        │   (validate +    │
#   │                          │    versions 통합) │
#   └──────────────────────────┴──────────────────┘
tmux split-window -v -t "$W.1" -c "$WORKDIR"
tmux split-window -h -t "$W.2" -c "$WORKDIR"
tmux resize-pane -t "$W.1" -y 12

tmux send-keys -t "$W.1" \
  "printf '\\033[2J\\033[H'; echo '📂 [Pane 1] 파일 변경 감지 — content.json 저장 시 자동 빌드'; echo; bash '$PROJECT_ROOT/scripts/watch_build.sh' '$COMPANY' '$AUTHOR'" Enter

tmux send-keys -t "$W.2" \
  "printf '\\033[2J\\033[H'; echo '🤖 [Pane 2] Hermes AI 에이전트'; echo; \
   echo '예: \"content.json 검토해줘\", \"모듈 순서 추천\", \"경쟁사 리서치\"'; echo; \
   if command -v hermes >/dev/null 2>&1; then \
     hermes chat; \
   else \
     echo 'hermes CLI 미설치. 설치: ~/.local/bin/hermes'; \
     bash; \
   fi" Enter

tmux send-keys -t "$W.3" \
  "printf '\\033[2J\\033[H'; echo '📋 [Pane 3] 검증 + 버전 + Git'; echo; \
   echo '── content.json 검증 ──'; \
   PYTHONIOENCODING=utf-8 python3 '$PROJECT_ROOT/scripts/validate_content.py' '$COMPANY' 2>&1 | tail -20; \
   echo; echo '── 버전 히스토리 ──'; \
   PYTHONIOENCODING=utf-8 python3 '$PROJECT_ROOT/scripts/version_manager.py' list 'projects/$COMPANY' 2>/dev/null | tail -8 || echo '  (버전 없음)'; \
   echo; echo '── Git Status ──'; git status -sb | head -10; echo; \
   echo '(갱신: Ctrl+B then V)'" Enter

# ── 완료 ─────────────────────────────────────────────────────────
if [[ -t 1 ]]; then
  # 인터랙티브 터미널: 자동 attach
  exec tmux attach -t "$SESSION"
else
  echo "✅ 세션 생성 완료: $SESSION"
  echo ""
  echo "   Attach:  tmux attach -t '$SESSION'"
  echo "   종료:    tmux kill-session -t '$SESSION'"
  echo "   단축키:  Ctrl+B ? (도움말), Ctrl+B d (detach)"
fi
