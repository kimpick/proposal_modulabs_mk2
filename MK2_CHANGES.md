# mk2 변경 요약 (Biz 전용 포크)

> 이 폴더(`propsal_modulabs_mk2`)는 영광님 원본 레포를 **복제**한 뒤, 이번에 합의한 개선을 얹은 **Biz 전용 mk2**입니다.
> 원본은 그대로 두고, mk2에서만 작업합니다. 실행 에이전트: **Claude Code**.
> 생성일: 2026-09-02

---

## ⚠️ 먼저 — 로컬에서 정리할 것 (마운트 삭제 제약으로 제가 못 지운 것)

복제 시 아래가 딸려왔습니다. **Biz님 PC에서 직접 삭제**를 권장합니다(로컬은 즉시 삭제됨):

1. **`automation/`** — 리드 인테이크 자동화. **n8n 크레덧·API 키 등 시크릿 포함** → mk2엔 불필요, 삭제 권장.
2. **`projects/`(약 340MB)** — 원본의 과거 산출물 아카이브(영광님 것). mk2는 새 과업만 담으면 되므로 비워도 됨(원하면 몇 건만 남기기).

```powershell
# 예시 (PowerShell, mk2 폴더에서)
Remove-Item -Recurse -Force .\automation
Remove-Item -Recurse -Force .\projects\*   # 과거 아카이브 비우기 (선택)
```

---

## 설치 — 1회 (Claude Code 커맨드 등록)

`.claude/`는 이 세션에서 쓰기 보호라, 새 명령을 `_mk2_install/commands/`에 넣어뒀습니다. **`.claude/commands/`로 복사**하세요:

```powershell
New-Item -ItemType Directory -Force .\.claude\commands | Out-Null
Copy-Item .\_mk2_install\commands\*.md .\.claude\commands\
```

그러면 Claude Code에서 `/propose`, `/research` 가 뜹니다. (원본의 `/setup /review /build /estimate`도 그대로)

의존성: `pip install jinja2`, PDF는 Edge(윈도우 기본) — 원본과 동일.

---

## 개선 3종 (원본 대비 추가분, 재동기화 시 유지할 것)

### 1. `/review`에 강사·내부정보 컴플라이언스 검증 추가
- **`scripts/validate_content.py`** — `validate_compliance()` 추가(주석 `# ===== mk2 addition`). 결정적으로 잡는 것:
  - 강사 실명 미마스킹 → **FIX**
  - 강사 카드 내 연락처·이메일(개인정보) → **FIX**
  - 강사 카드 내 강의료/단가(내부정보) → **WARN**
  - `schedule_message`·`section_07_title`의 협의 이력('수정사항 반영') 잔존 → **WARN**
- **`docs/review_compliance_reviewer.md`** (신규) — 5번째 리뷰어(맥락 판단: 내부메모 유출·타 고객사명 정책) 스펙.
- 검증됨: 위반 케이스 → NEEDS_FIX(FIX 4·WARN 2), 정상 케이스 → PASS(오탐 없음).

### 2. 오케스트레이터 원커맨드 `/propose` (하드스톱 내장)
- **`_mk2_install/commands/propose.md`** → `.claude/commands/propose.md`.
- 흐름: `/research → context.md ─ G0(방향) ─ content.json ─ G1(/review PASS) ─[하드스톱]─ build → (선택)강사·견적·메일 → git`
- **원칙 #1**: 커리큘럼(content.json)이 `/review` PASS 되기 전엔 **build·강사·견적·메일 금지**(수정 시 재작업 방지).

### 3. 리서치→context 연결 `/research` (조건부 라우팅)
- **`_mk2_install/commands/research.md`** → `.claude/commands/research.md`.
- 사내 1차 + **조건부** 외부 웹(신규·미지 고객사만). 이미 아는 고객사면 외부 생략/축소 → 토큰 절감·중복 제거.
- 산출: `projects/<기업>/context.md` + `memory/clients/<기업>.md`(신규/갱신).
- 무거운 리서치는 **서브에이전트로 돌려 요약만** 받도록 권장(토큰 절감).

---

## 원본과의 관계 (재동기화)
- 변경은 모두 **추가/명시적 표시**(validate_content.py 주석, 신규 파일)라, 영광님 원본을 `git pull` 후 이 3개만 다시 얹으면 됩니다.
- 원본 파일 중 **수정한 것은 `scripts/validate_content.py` 하나**(함수 1개 + 호출 1줄 추가). 나머지는 신규 파일.
- 도구 3-way 검사·4리뷰어·governance 등은 원본 그대로(이미 성숙).

## 검증 완료
- `validate_content.py` 문법 OK, 위반/정상 케이스 동작 확인.
- 실제 PDF 빌드(build.py)는 Edge가 있는 Biz님 PC에서 확인 필요(샌드박스엔 Edge 없음).
