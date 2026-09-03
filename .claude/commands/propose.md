---
description: 신규 제안서 원커맨드 오케스트레이터 (리서치→content→검토 하드스톱→빌드)
argument-hint: "{기업명} [과정명]"
---

# /propose — 제안서 오케스트레이터 (mk2)

신규 교육 제안 요청을 받았을 때, 아래 단계를 **순서대로** 진행한다.
`$ARGUMENTS` = 기업명 [과정명].

## 원칙 #1 (가장 중요) — 커리큘럼 하드스톱
> **커리큘럼(content.json)이 `/review`에서 PASS(또는 PASS_WITH_NOTES + 사용자 OK)가 되기 전에는
> 절대 downstream을 만들지 않는다.** downstream = PDF 빌드, 추천 강사 섹션, 견적서, 섭외 메일.
> 커리큘럼이 확정되기 전에 이것들을 만들면, 커리큘럼 수정 시 전부 재작업이 된다.

## 실행 순서

### STEP 0. 컨텍스트 확보 (게이트 G0: 커리큘럼 방향)
1. `AGENT_GUIDE.md`와 `CLAUDE.md`의 규칙을 숙지한다.
2. `memory/clients/<기업명>.md`가 있으면 읽는다(기존 고객사 = 장기 기억). `memory/clients/_INDEX.md`로 폴더↔고객사 매핑 확인.
3. `projects/<기업명>/context.md`가 없으면 **`/research <기업명>`을 먼저 실행**해 `context.md`를 만든다.
4. 커리큘럼 **방향**(대상·목표·범위)을 사용자와 확정한다. — **여기서 한 번 멈추고 사용자 입력을 받는다.**

### STEP 1. content.json 작성
1. 제안 타입 결정: 전사 로드맵→`roadmap` / 직무별→`track` / IT·개발→`module` / K-HP 세미나→`khp-seminar`.
2. `schemas/<타입>.example.json`을 `projects/<기업명>/<과정명>/content.json`으로 복사 후 값 교체.
3. `context.md`·`memory`의 확정 정보만 반영. 임의 창작 금지(미정은 `[협의 필요]`).
4. 도구 일관성: `tech_stack` = 모든 `tracks[].tools`의 합집합.

### STEP 2. 검토 — 하드스톱 게이트 (G1: 커리큘럼 확정)
1. 로컬 결정적 검증(무비용):
   ```bash
   PYTHONIOENCODING=utf-8 python3 scripts/validate_content.py <기업명>/<과정명>
   ```
2. 5개 관점 리뷰(원본 4 + mk2 Compliance):
   - Flow / Recency / Tone / Readability — `docs/review_agent_prompts.md`
   - **Compliance** (강사 마스킹·개인정보·강의료·협의이력·타 고객사) — `docs/review_compliance_reviewer.md`
3. 종합 판정(FIX 1개+ 또는 WARN 3개+ → NEEDS_FIX)을 사용자에게 보고한다.
4. **정지**:
   - `NEEDS_FIX` → 사용자가 수정 → STEP 2 재실행. **build 금지.**
   - `PASS` → STEP 3.
   - `PASS_WITH_NOTES` → 참고사항 안내 후 **사용자 OK를 받고** STEP 3.
   > 컴플라이언스 FIX(실명·개인정보)는 사업 판단 대상이 아니다. 반드시 제거 후 통과.

### STEP 3. 빌드 (커리큘럼 확정 이후에만)
```bash
PYTHONIOENCODING=utf-8 python3 build.py <기업명>/<과정명>
```
생성된 HTML/PDF를 확인(오타·레이아웃·스키마).

`instructors`가 렌더되는 제안서는 **PDF 2종**이 자동으로 나온다.

| 산출물 | 파일명 | 추천 강사 후보군 | 용도 |
|---|---|---|---|
| 고객사용 | `..._제안서.pdf` | 포함 | 고객사 제출 |
| 강사공유용 | `..._제안서_강사공유용.pdf` | **제외** | 섭외 강사에게 커리큘럼 안내 시 첨부 |

강사에게 보내는 첨부는 **반드시 `_강사공유용`** 인지 확인한다. 다른 강사 후보가 보이면 안 된다.
강사 섹션이 애초에 렌더되지 않는 제안서는 1종만 생성된다(같은 파일을 두 번 만들지 않는다).

### STEP 4. (선택) downstream — 확정된 커리큘럼 위에서만
- 추천 강사: `/add-instructor-recommendation <기업명>` + 이력서 → 재빌드(2종 갱신)
- 견적·고객 메일: `/estimate <기업명>` → 견적서 md·csv + 이메일 초안 html 3종
- 강사 섭외 메일: 강사 확정·강사료 확정 후. 첨부는 `_강사공유용` PDF.

### STEP 5. 저장
`git add/commit/push` (기업 폴더 단위). 고객사 장기 기억 갱신이 필요하면 `memory/clients/<기업명>.md` 업데이트.

## 요약 흐름
```
/research → context.md ─ G0(방향 확정) ─ content.json ─ G1(/review PASS) ─┐ 하드스톱
                                                                          ↓ (통과 후에만)
                                              build.py → PDF ─ (선택) 강사·견적·메일 → git
```
