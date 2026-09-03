#!/usr/bin/env bash
# Usage: scripts/watch_build.sh COMPANY [AUTHOR]

set -uo pipefail

COMPANY="${1:?usage: watch_build.sh COMPANY [AUTHOR]}"
AUTHOR="${2:-작업자}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

TARGET="projects/$COMPANY"
if [[ ! -d "$TARGET" ]]; then
  echo "FAIL 기업 폴더 없음: $TARGET"
  exit 1
fi

echo "WATCH $TARGET/**/content.json"
echo "AUTHOR $AUTHOR — 저장 시 자동 빌드"
echo "STOP  Ctrl+C"
echo ""

LAST_BUILD=0

run_build() {
  local now=$(date +%s)
  if (( now - LAST_BUILD < 2 )); then
    return
  fi
  LAST_BUILD=$now

  echo "[$(date +%H:%M:%S)] CHANGE — 빌드 시작"
  echo "──────────────────────────────────────────"

  if PYTHONIOENCODING=utf-8 python3 build.py "$COMPANY" --author "$AUTHOR" 2>&1; then
    echo "──────────────────────────────────────────"
    echo "OK 빌드 완료 $(date +%H:%M:%S)"
  else
    echo "──────────────────────────────────────────"
    echo "FAIL 빌드 실패 $(date +%H:%M:%S)"
  fi
  echo ""
}

if command -v fswatch >/dev/null 2>&1; then
  exec fswatch -0 \
    --event Created --event Updated --event AttributeModified \
    --include='content\.json$' \
    --exclude='.*' \
    --latency=0.5 \
    "$TARGET" | while IFS= read -r -d '' _event; do
    run_build
  done
elif command -v inotifywait >/dev/null 2>&1; then
  exec inotifywait -m -e modify,create,move \
    --format '%w%f' -r \
    "$TARGET" 2>/dev/null | while IFS= read -r event; do
    [[ "$event" == *content.json ]] && run_build
  done
else
  echo "WARN fswatch/inotifywait 미설치 — 5초 폴링 모드"
  echo "  macOS: brew install fswatch"
  echo "  Linux: apt install inotify-tools"
  echo ""
  declare -A LAST_MTIME
  while true; do
    while IFS= read -r f; do
      [[ -f "$f" ]] || continue
      mtime=$(stat -f "%m" "$f" 2>/dev/null || stat -c "%Y" "$f" 2>/dev/null)
      prev="${LAST_MTIME[$f]:-0}"
      if [[ "$mtime" -gt "$prev" ]]; then
        LAST_MTIME[$f]=$mtime
        if [[ "$prev" -ne 0 ]]; then
          run_build
        fi
      fi
    done < <(find "$TARGET" -name "content.json")
    sleep 5
  done
fi
