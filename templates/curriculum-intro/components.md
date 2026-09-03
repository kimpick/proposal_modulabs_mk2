# 컴포넌트 라이브러리 — 가로형 교육과정 소개자료

> **재현성 계약.** 문서를 조립할 때 반드시 이 파일의 스니펫을 그대로 복사해서 쓴다.
> 클래스명·구조·중첩을 임의로 변경하면 안 된다. 내용(텍스트)만 변수로 채운다.
> 골든 샘플: `templates/curriculum-intro/golden/롯데이커머스_3트랙_교육과정_소개.html`

## 규칙

1. **컴포넌트 신규 발명 금지.** 아래 12종(+섹션 셸)으로만 조립한다. 새 컴포넌트가 필요하면 스킬 유지자에게 요청해 라이브러리에 추가한다.
2. **클래스명 변경 금지.** CSS(parent.css)와 계약된 클래스명이다.
3. **강조는 `<b>` 태그로.** daycard 본문·lead 내 핵심 키워드는 `<b>` 처리한다(골든 샘플 관례).
4. **이모지는 커버 badge에만 허용** (예: `🔴 모두의연구소 × 고객사`). 본문 섹션에는 쓰지 않는다.

---

## C0. 문서 셸 (보일러플레이트)

모든 문서의 뼈대. `<style>` 안에 `parent.css` **전체를 통째로** 인라인한다 (외부 링크 금지 — 파일 단위 공유 전제).

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{고객사} {주제} · {문서종류}</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<style>
/* parent.css 전체를 여기에 통째로 붙여넣는다 (값 수정 금지) */
</style>
</head>
<body>

<!-- 섹션들이 순서대로 나열된다 -->

<p class="foot">© 모두의연구소 · {고객사} {문서요약} · {YYYY.MM}</p>
</body>
</html>
```

---

## C1. COVER — 커버 (필수 · 첫 장)

```html
<section class="cover">
  <div class="pad">
    <span class="cover-badge">🔴 모두의연구소 &nbsp;×&nbsp; {고객사명}</span>
    <h1>{고객사} {교육 대주제}<br><span>{핵심 구성 요약}</span> 제안</h1>
    <p class="sub">{3단계 요약 문장 — 트랙 흐름을 한 문장씩 압축}</p>
    <div class="cover-meta">
      <span><b>대상</b> · {전사 약 500명}</span>
      <span><b>구성</b> · {3개 트랙 · 5개 과정}</span>
      <span><b>커리큘럼</b> · {총 72H}</span>
      <span><b>기반</b> · {Gemini Enterprise}</span>
    </div>
  </div>
</section>
```

- `cover-meta` 항목 수는 3~5개 자유. 라벨(`대상/구성/커리큘럼/기반/기간` 등)은 내용에 맞게.
- `h1 span`은 포인트 컬러(#ffd0d4)로 강조되는 부분 — 가장 중요한 키워드를 넣는다.

## C2. SECTION HEAD — 섹션 공통 헤더

모든 일반 섹션은 이 헤더로 시작한다.

```html
<section>
  <div class="pad">
    <span class="sec-num">{NN} / {섹션분류}</span>
    <p class="kicker">{트랙/주제 분류 · 대문자}</p>
    <h2>{한 문장 헤드라인 — 설계 의도가 보이게}</h2>
    <p class="lead">{2~3줄 리드 문단 — 왜 이렇게 설계했는지}</p>
    ...
  </div>
</section>
```

- `sec-num`은 조립 순서대로 01, 02, … 자동 채번 (COVER/CLOSING 제외).
- `lead`는 생략 가능 (골든의 트랙 상세 섹션처럼 metastrip으로 바로 갈 수 있음).

## C3. METASTRIP — 정보 칩 스트립

```html
<div class="metastrip">
  <div class="mchip"><div class="ml">대상</div><div class="mv">전 직군 (팀 단위)</div></div>
  <div class="mchip hl"><div class="ml">교육 시간</div><div class="mv">12H · 4H×3일</div></div>
  <div class="mchip"><div class="ml">차수 규모</div><div class="mv">20명 / 반</div></div>
  <div class="mchip"><div class="ml">도구</div><div class="mv">Gemini Enterprise · NotebookLM</div></div>
</div>
```

- **가장 중요한 칩 1개만 `hl`** (보통 시간). `hl` 남발 금지.
- 라벨 예: 대상 / 교육 시간 / 시간 / 차수 규모 / 레벨 / 도구 / 공통 산출물.

## C4. FLOW — N단계 여정

```html
<div class="flow" style="margin-bottom:22px">
  <div class="step"><div class="st">트랙 1 · 전사 공통</div><div class="sd">AI Agent AX 워크숍</div><div class="ss">전 직군 · 12H · AX 마인드셋 + 팀 MVP</div></div>
  <div class="step"><div class="st">트랙 2 · 직무별</div><div class="sd">직무별 AI 활용</div><div class="ss">MD·영업마케팅·HR재무 · 각 12H</div></div>
  <div class="step"><div class="st">트랙 3 · IT 심화</div><div class="sd">에이전트 엔지니어링</div><div class="ss">개발·인프라·보안 · 24H</div></div>
</div>
```

- 2~4단계. OVERVIEW 섹션 상단에 배치.
- `st` = 분류, `sd` = 과정명, `ss` = 한 줄 요약.

## C5. PROP TABLE — 전체 커리큘럼 요약표

```html
<table class="prop">
  <thead><tr><th>트랙</th><th>과정</th><th>핵심 내용</th><th>대상</th><th class="c">시간</th><th>분류</th></tr></thead>
  <tbody>
    <tr>
      <td class="trk">트랙 1<br>전사 공통</td>
      <td class="course">AI Agent 기반<br>AX 워크숍</td>
      <td class="core">{핵심 내용 — '→'로 흐름 연결}</td>
      <td class="tgt">전 직군<br>(차수당 20명)</td>
      <td class="hrs">12H<br><span style="font-weight:600;color:var(--muted);font-size:10px">4H×3일</span></td>
      <td><span class="badge badge-blue">Level 1 · 전사 공통</span></td>
    </tr>
    <!-- 같은 트랙의 연속 행은 첫 행의 trk에 rowspan, 이후 행에서 trk 셀 생략 -->
    <tr class="sumrow"><td colspan="4">전체 커리큘럼 · {요약}</td><td class="hrs">총 72H</td><td><span class="badge badge-green">5개 과정</span></td></tr>
  </tbody>
</table>
```

- **badge 색语义**: `badge-blue` 전사공통/기초 · `badge-red` 직무 자동화 · `badge-purple` 심화/엔지니어링 · `badge-green` 합계/집계.
- 마지막 `sumrow`는 항상 포함 (총시간·과정수 검증 역할).
- `hrs` 셀의 `4H×3일` 보조 스팬은 분할 운영일 때만.

## C6. DAYGRID / DAYCARD — 일차별 커리큘럼 (핵심 컴포넌트)

```html
<div class="daygrid">
  <div class="daycard">
    <div class="dh"><div class="dn">DAY 1</div><div class="dt">{일차 테마}</div><span class="dhh">4H</span></div>
    <div class="db">
      <div class="m"><span class="mh">M1 · 1H</span>내용 — <b>핵심 강조</b></div>
      <div class="m"><span class="mh">M2 · 1.5H</span>내용</div>
      <div class="m">모듈 시간 표기 없는 단순 목록형</div>
    </div>
  </div>
  <!-- DAY 2, DAY 3 ... -->
</div>
```

- `.dn` 라벨: `DAY 1` / `STEP 1` (다일차 과정은 DAY, 파트별 과정은 STEP — 골든 관례).
- `.mh` 모듈 시간 표기(`M1 · 1H`)는 **시간 정보가 있을 때만**. 없으면 `.m` 단독.
- 일차 수에 따라: 3일 → `.daygrid`(기본 3열), 2일 → `.daygrid cols-2`, 4파트 → `.daygrid cols-4`(2×2).
- `.db` 모듈 수는 카드당 3~5개 적정.

## C7. OUTBOX — 산출물 박스

```html
<div class="outbox">
  <div class="ot">산출물</div>
  <div class="op"><span>{산출물 1}</span><span>{산출물 2}</span><span>{산출물 3}</span></div>
</div>
```

- TRACK-DETAIL 섹션 하단에 배치. 산출물 3~5개.
- 각 span에는 결과물 이름을 명사형으로 (예: "상세페이지 카피 생성기").

## C8. JOB GRID — 직군 개요 카드

```html
<div class="grid g3">
  <div class="job">
    <div class="jt">MD (상품기획)</div>
    <div class="js">상세페이지·매출/재고·경쟁사 반복업무</div>
    <ul><li>{에이전트/성과 1}</li><li>{에이전트/성과 2}</li><li>{에이전트/성과 3}</li></ul>
  </div>
  <!-- 직군 수만큼: 2개면 g2, 4개면 g4 -->
</div>
```

- 트랙 내 여러 직군을 한 장에 요약할 때 (TRACK-GROUP 섹션).
- `jt` 직군명 / `js` 페인포인트 한 줄 / `ul` 해당 직군 에이전트·성과 3개.

## C9. OP TABLE — 운영 차수표

```html
<table class="op-tbl">
  <thead><tr><th>직군</th><th class="c">비율</th><th class="c">인원</th><th>반 편성 (20명)</th><th class="c">운영 차수</th><th class="c">반당 시간</th></tr></thead>
  <tbody>
    <tr><td><b>MD</b></td><td class="c">30%</td><td class="c">150명</td><td>20명×7 + 10명×1</td><td class="hl">8차수</td><td class="c">12H</td></tr>
    <tr class="tot"><td colspan="2">합계</td><td class="c">500명</td><td>직무별 + IT</td><td class="hl">26차수</td><td class="c">—</td></tr>
  </tbody>
</table>
<p class="note">※ {운영 전제·조정 가능 항목·일정 조건}</p>
```

- OPERATION 섹션 전용. 다크 헤더 + `tot` 합계행 + `note` 각주 세트로 쓴다.
- 차수 산정 로직(인원÷반규모 올림)은 note에 명시해 검증 가능하게.

## C10. NOTE — 각주

```html
<p class="note">※ {전제 조건, 조정 가능성, 일정 의존성}</p>
```

- 표 하단 전제·예외를 남긴다. 문장이 길어도 한 문단 유지.

## C11. CLOSING — 맺음말 (필수 · 마지막 장)

```html
<section class="closing">
  <div class="pad">
    <p class="kicker" style="color:#ffd0d4">맺음말</p>
    <h2>{한 문장 마무리 메시지}</h2>
    <p class="msg">{커리큘럼 전체를 관통하는 가치 서술 — 고객사명 포함}</p>
    <div class="sign">
      <span><b>모두의연구소</b> · 비즈팀 · modu.biz@modulabs.co.kr</span>
    </div>
  </div>
</section>
```

- `sign`은 **비즈팀 공용 서명 1줄로 고정** — 담당자 개인 이름·개인 메일·휴대폰 번호는 넣지 않는다.

## C12. FOOT — 푸터

```html
<p class="foot">© 모두의연구소 · {고객사} {문서요약} · {YYYY.MM}</p>
```

---

## 섹션 아키타입 → 컴포넌트 조합표

| 아키타입 | 조합 | 사용 시점 |
|---|---|---|
| **COVER** | C1 | 항상 첫 장 |
| **OVERVIEW** | C2 + C4(flow) + C5(prop) | 트랙/과정이 2개 이상일 때 |
| **TRACK-DETAIL** | C2 + C3 + C6(daygrid) + C7 | 교육과정 1개 상세 (과정마다 1섹션) |
| **TRACK-GROUP** | C2 + C8(job) + C3 | 여러 직군을 한 장에 요약할 때 |
| **OPERATION** | C2 + C9(op-tbl) + C10 | 대규모 인원·차수 운영이 있을 때 |
| **CLOSING** | C11 | 항상 마지막 장 |

- 최소 구성: COVER + TRACK-DETAIL + CLOSING (과정 1개짜리 소개자).
- sec-num 채번: COVER 다음 첫 일반 섹션이 01.
