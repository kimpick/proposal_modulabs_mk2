# Graph Engineering 교육 — 선택지 스펙트럼 정리

**작성일**: 2026-08-07
**목적**: 고객사 AIOps/LLMOps 니즈에 대응하는 교육을 설계하기 위해, 결정해야 할 축을 스펙트럼으로 펼쳐 놓고 우리 포지션을 잡는다.
**선행 문서**: [GraphEngineering_1일교육_리서치.md](GraphEngineering_1일교육_리서치.md)

> 이 문서는 **"무엇을 고를 것인가"의 지도**입니다. 각 축마다 양 끝단과 중간값을 놓고, 우리가 어디에 설지와 그 근거를 표시합니다. (◆ = 권장 포지션)

---

## 축 요약 — 6개 축 한눈에

| # | 축 | 왼쪽 끝 | 오른쪽 끝 | 우리 위치 |
|---|---|---|---|---|
| 1 | **통제 ↔ 자율** | 고정 워크플로우 | 자율 에이전트 루프 | ◆ 중앙(Graph) |
| 2 | **방법론 계층** | Prompt Engineering | Graph Engineering | ◆ 오른쪽 2칸(Loop~Graph) |
| 3 | **프레임워크 추상화** | 고수준(CrewAI) | 저수준(직접 구현) | ◆ 중저(LangGraph) |
| 4 | **관측 플랫폼** | SaaS 종속 | OSS Self-host | ◆ 오른쪽(Langfuse) |
| 5 | **평가 깊이** | 출력 스팟체크 | 프로덕션 온라인 평가 | ◆ 중앙(트레젝토리+오프라인 회귀) |
| 6 | **교육 분량** | 0.5일 인지 | 10일 캡스톤 | ◆ 1일 본과정 + 선행 1일 |

---

## 축 1. 통제 ↔ 자율 — "AI에게 얼마나 맡길 것인가"

고객이 말한 **"AI가 일하는 걸 관리할 수 있는 역량"**은 정확히 이 축 위의 문제입니다.

```
[완전 통제]                                                      [완전 자율]
  ①고정 워크플로우 ──── ②라우팅 ──── ③Graph ──── ④Agent 루프 ──── ⑤멀티에이전트 자율 협상
   (if/else 파이프)     (분기만 LLM)   ◆         (경로를 LLM이 탐색)     (Swarm)
```

| 단계 | 무엇인가 | 예측가능성 | 감사·통제 | 비용 | 적합 업무 |
|---|---|---|---|---|---|
| ① 고정 워크플로우 | 코드가 순서를 다 정함 | 최상 | 최상 | 최저 | 정형 처리 |
| ② 라우팅 | 분기 판단만 LLM | 상 | 상 | 저 | 문의 분류·티켓 배분 |
| **③ Graph** ◆ | 경로는 사람이 설계, 판단은 LLM | **중상** | **중상** | 중 | **심사·검토·리포팅·승인** |
| ④ Agent 루프 | 경로를 LLM이 탐색 | 중하 | 하 | 상 | 리서치·탐색적 코딩 |
| ⑤ 자율 협상(Swarm) | 위계 없는 peer 핸드오프 | 하 | 최하 | **최상** | 실험적 |

**핵심 판단 기준**: *경로를 미리 그릴 수 있으면 ③, 실행하며 찾아야 하면 ④.*

**왜 ③인가**: 기업 업무 대부분(심사·검토·리포팅·문서생성·승인)은 경로를 미리 그릴 수 있습니다. 그리고 ③은 **감사 가능성과 성능의 손익분기점**입니다. ④⑤로 갈수록 데모는 화려해지지만 "왜 그렇게 했는지 설명할 수 없음"이 커지고, 이게 기업 도입의 실제 병목입니다.

> **교육 설계 함의**: ①~⑤를 전부 가르치되 **③에 시간의 60%를 쓰고, ⑤는 "비싸다는 걸 실측으로 보여주는 반면교사"로 20분만** 다루는 게 효율적입니다. 벤치마크상 핸드오프형 Swarm은 같은 과제에서 subagent 패턴 대비 호출 수·토큰이 뚜렷하게 증가합니다.

---

## 축 2. 방법론 계층 — "어느 층을 가르칠 것인가"

```
Prompt ──→ Context ──→ Harness ──→ Loop ──→ Graph
  (기초)     (기초)      (중급)      ◆────────◆
```

| 층 | 다루는 문제 | 이 층만 배우면 생기는 한계 | 교육 시장 성숙도 |
|---|---|---|---|
| **Prompt** | 요청 한 번을 잘 쓰기 | 재현성 없음, 규모 안 됨 | 포화 (누구나 함) |
| **Context** | 프롬프트 주변에 뭘 넣을지 | 단발성, 반복 자동화 안 됨 | 성숙 (경쟁 많음) |
| **Harness** | 도구·가드레일·검증 시스템 | 에이전트 1개 수준에 머묾 | 성장 중 |
| **Loop** ◆ | 한 에이전트의 반복 자동화 | 복잡 업무 분해 불가 | 성장 중 |
| **Graph** ◆ | 여러 단계·에이전트를 그래프로 | — | **초기 (선점 가능)** |

**우리 포지션**: **Loop~Graph 2개 층.** Prompt/Context는 이미 시장이 포화됐고, 고객이 물어본 건 그 위층입니다.

**단, 아래층을 건너뛸 수는 없습니다.** 계층은 대체가 아니라 누적이라, Context/Harness가 없는 수강생에게 Graph를 던지면 M2에서 전원이 막힙니다. → **이것이 선행 기초 과정이 필요한 유일한 이유**입니다 (축 6).

> **영업 메시지 함의**: "Graph Engineering"은 2026년 7월에 용어가 붙어 아직 교육 상품이 드뭅니다. **선점 가치가 있습니다.** 다만 LangChain 측은 "새로운 게 아니라 LangGraph가 3년간 해온 것"이라는 입장이므로, *유행어 팔이가 아니라 3년치 프로덕션 교훈*으로 포지셔닝해야 신뢰가 유지됩니다.

---

## 축 3. 오케스트레이션 프레임워크 — "무엇으로 실습할 것인가"

```
[고수준 추상화 · 빨리 만듦]                        [저수준 · 통제력 높음]
  CrewAI ── Microsoft Agent Framework ── LangGraph ── 직접 구현
                                            ◆
```

| 프레임워크 | 성격 | 강점 | 약점 | 교육 적합성 |
|---|---|---|---|---|
| **CrewAI** | 역할 기반 크루 | **프로토타입 속도 최고** — 추상화가 직관적 | 프로덕션 관측·에러복구 취약 | 데모용. *"AI가 일하는 걸 관리"* 니즈와 어긋남 |
| **AutoGen** | 멀티에이전트 토론·검증 | 연구·학계 성숙 | 프로덕션 채택 작음 | 연구 대상 교육에만 |
| **Microsoft Agent Framework 1.0** | Semantic Kernel + AutoGen 통합 | 세션 상태·타입 안전·미들웨어·텔레메트리, MCP/A2A 네이티브 | 신생, 자료 적음 | MS 스택 고객이면 검토 |
| **LangGraph 1.x** ◆ | 상태 그래프 저수준 | **2026년 최대 프로덕션 채택**, 체크포인트·HITL·타임트래블 | 학습곡선 있음 | **◆ 이번 과정 채택** |
| **LlamaIndex Workflows 1.0** | 이벤트 기반 워크플로우 | RAG 스택과 결합 좋음 | 멀티에이전트 생태계 작음 | RAG 중심 고객이면 |
| **Pydantic AI V2** | 타입 우선 경량 | 타입 안전성, 가벼움 | 그래프 제어 표현력 낮음 | 기초 과정 후보로는 매력 |
| **Claude Agent SDK** | 하네스형 | 코딩 에이전트 강력 | 그래프 설계 학습에는 부적합 | 축 1의 ④ 영역 |
| 직접 구현 | 프레임워크 없이 | 종속성 없음 | 체크포인트·HITL 다 직접 | 8H 안엔 불가능 |

**LangGraph를 고르는 이유 3가지**
1. **축 1의 ③을 코드로 표현하는 데 가장 직접적** — State/Node/Edge/종료조건이 1:1로 대응
2. **관리 역량과 직결되는 기능이 다 있음** — 체크포인트, `interrupt()` 승인 게이트, 타임트래블
3. **프로덕션 채택 1위** — 교육 후 실제 도입 경로가 열려 있음

> ⚠️ **버전 리스크**: LangChain 1.0에서 `create_agent`가 표준이 되고 **`create_react_agent`는 deprecated**입니다. 시중 자료 대부분이 구버전이라 **교재를 1.x 기준으로 새로 써야 합니다.** 이건 견적 산정 시 교재 개발 공수로 반영해야 할 항목입니다.
>
> **사내 자산 주의**: 삼성전자MX 트랙2 과정은 **CrewAI + LangGraph 혼합**입니다. 5대 패턴 카탈로그는 재활용 가치가 크지만 CrewAI 실습부는 이번 건에 그대로 쓰면 안 됩니다.

---

## 축 4. 관측 플랫폼 — "실행을 무엇으로 들여다볼 것인가"

```
[SaaS 종속 · 통합 깊음]                       [OSS Self-host · 종속 없음]
  LangSmith ── Braintrust ── W&B Weave ── AgentOps ── Opik ── Phoenix ── Langfuse
                                                                            ◆
```

| 도구 | 라이선스/호스팅 | 결정적 강점 | 결정적 약점 | 이번 건 판단 |
|---|---|---|---|---|
| **LangSmith** | SaaS (무료 5,000 traces/월) | **LangChain/LangGraph 통합 최심** — 노드별 state diff, 실행 그래프, 리플레이. 오버헤드 거의 0 | 벤더 종속, 사내망 반출 이슈 | 사내 기존 사례(현대차·기웅) |
| **Langfuse** ◆ | OSS, **self-host 무제한 무료** | 트레이싱+평가+비용을 하나로. OTel 기반. **Agent Graph View** | 오버헤드 ~15% 보고 | **◆ 채택** |
| **Arize Phoenix** | OSS, OTel 네이티브 | 프레임워크 무관, 실험·평가 워크플로우 넓음 | 학습 리소스가 Langfuse보다 적음 | 대안 1순위 |
| **Opik (Comet)** | OSS | 오픈소스 대안으로 견실 | 국내 레퍼런스 적음 | 대안 |
| **AgentOps** | SaaS | **400+ 프레임워크 지원, 타임트래블 디버깅** | 프레임워크 고정 시 이점 희석 | 이번 건은 LangGraph 단일이라 불필요 |
| **W&B Weave** | SaaS | 드리프트·리그레션 대규모 탐지 | ML 스택 전제 | 해당 없음 |

**Langfuse를 고르는 이유 3가지**
1. **Self-host가 무료·무제한** → 사내망·데이터 반출 제약이 있는 기업이 *교육 후 실제로 도입 가능*. 이게 LangSmith 대비 최대 차별점
2. **OpenTelemetry 기반** → 프레임워크를 바꿔도 관측 레이어는 유지, 기존 APM과 접점
3. **Agent Graph View** (2026-07~) → *설계한 그래프* vs *실제 실행 경로* 비교 실습이 가능. 이 과정의 하이라이트 장면

**트레이드오프 정직하게**: LangGraph 스택만 놓고 보면 **통합 깊이는 LangSmith가 우위**입니다(노드별 state diff까지). 우리가 Langfuse를 고르는 건 *기술 우위*가 아니라 **도입 가능성(self-host)과 종속 회피** 때문입니다. 제안서에도 이렇게 정직하게 쓰는 게 설득력이 높습니다.

> ⚠️ **리스크**: Langfuse는 사내 첫 적용입니다. **강사 리허설 + 사내망 엔드포인트 접근 확인 필수.**

---

## 축 5. 평가 깊이 — "잘 돌아가는지 어떻게 판단할 것인가"

```
[가볍고 얕음]                                              [무겁고 깊음]
 ①눈으로 확인 ── ②출력 단위 평가 ── ③트레젝토리 평가 ── ④오프라인 회귀 ── ⑤프로덕션 온라인 평가
                                        ◆──────────────◆
```

| 단계 | 무엇을 보는가 | 도구 | 8H 안에 가능? |
|---|---|---|---|
| ① 스팟체크 | 결과가 그럴듯한가 | 없음 | — |
| ② 출력 평가 | 정답 대비 품질 | RAGAS, DeepEval | 가능 |
| **③ 트레젝토리 평가** ◆ | **경로가 옳았는가** — 도구 호출 정확도, 목표 달성, 스텝 수 | Langfuse scores, RAGAS 에이전트 지표 | **◆ 핵심** |
| **④ 오프라인 회귀** ◆ | 프롬프트/모델 바꾸면 나빠지는가 | Langfuse datasets + `run_experiment` | **◆ 핵심** |
| ⑤ 온라인 평가 | 프로덕션에서 실시간 | 커스텀 파이프라인 | 8H 초과 → 개념만 |

**③이 이 과정의 심장인 이유**: 에이전트는 최종 답이 맞아도 **20스텝을 돌며 정책 위반 호출을 두 번 했으면 실패한 트레젝토리**입니다. 출력만 보는 평가로는 이걸 절대 못 잡습니다. 고객이 말한 "AI가 일하는 걸 관리"는 결과가 아니라 **과정을 본다**는 뜻이고, 그게 트레젝토리 평가입니다.

**보조 도구 스펙트럼** (이번 과정엔 넣지 않되 로드맵으로 언급 가치 있음)

| 도구 | 특화 | 언제 |
|---|---|---|
| **Promptfoo** | 레드티밍·보안 검증 | 보안 요구가 큰 고객 (예: 현대차 사례) |
| **DeepEval** | pytest 기반 **CI/CD 통합** | 개발조직에 평가를 파이프라인화할 때 |
| **RAGAS** | RAG + 에이전트 지표(목표 달성도, 툴콜 정확도/F1, 주제 준수) | RAG가 그래프 노드로 들어갈 때 |

> ⚠️ **강의에서 반드시 말해야 할 한계**: LLM-as-judge는 **길이·위치·자기선호 편향**이 있고, 비결정적이며, 판정마다 모델 호출 비용이 듭니다. 실제로 YC 에이전트 빌더 다수가 "오프라인 평가셋을 최신으로 유지하는 건 불가능하고, 프로덕션에서 매 턴 돌리는 곳은 없다"고 답합니다. **평가를 만능으로 팔면 안 되고, "완벽한 자동 평가"가 아니라 "회귀를 잡는 안전망"으로 포지셔닝**해야 현장에서 배신당하지 않습니다.

---

## 축 6. 교육 분량 — "얼마나 길게 할 것인가"

```
[가벼움]                                                          [무거움]
 0.5일 ──── 1일 ──── 1.5일 ──── 2일 ──── 5일 ──── 10일 캡스톤
  인지      실습     압축세트    ◆권장    심화     조직 전환
```

### 6-A. 본과정 분량 스펙트럼

| 분량 | 도달 지점 | 적합 대상 | 리스크 |
|---|---|---|---|
| 0.5일 (4H) | 방법론 인지 + 데모 | 임원·기획 | 손이 안 움직여 "봤다"로 끝남 |
| **1일 (8H)** ◆ | **설계→관측→평가 루프 1바퀴 완주** | 실무 개발자 | 과밀 — 스캐폴딩 코드 필수 |
| 1.5일 | 위 + 자기 업무 적용 실습 | 실무 개발자 | — |
| 2일 | 위 + HITL/배포 | 팀 단위 도입 | — |
| 5~10일 | 캡스톤·사내 과제 적용 | 조직 전환 | 사내 과제 확보 필요 (현대차 10일 사례) |

### 6-B. 선행 기초 과정 스펙트럼 — 이번 질문의 핵심

**전제조건은 리서치상 딱 셋으로 수렴합니다.**
> ① Chat model 다루기 · ② Tool/Function calling · ③ **Pydantic 구조화 출력**

③이 없으면 State 스키마·도구 스키마가 안 서서 본과정 M2에서 전원이 막힙니다.

**후보 스펙트럼 — 필수부터 제외까지**

| 우선순위 | 항목 | 시간 | 판단 근거 |
|---|---|---|---|
| **필수** | Tool Calling & 단일 에이전트 루프 | 2.5H | LangGraph 공식 전제조건 |
| **필수** | Pydantic 구조화 출력 | 1.5H | State·툴 스키마의 토대 |
| **필수** | LLM API & 프롬프트/컨텍스트 기초 | 1.5H | 5단 스택 1~2층 |
| **필수** | 개발환경 셋업 (uv/.env/키관리) | 0.5H | 실습 이탈률을 가장 크게 좌우 |
| **강력권장** | 미니 프로젝트 — 도구 2개 쓰는 에이전트 | 1.5H | **★ 이 산출물이 다음 날 그래프의 워커 노드가 됨** |
| 권장 | 컨텍스트 엔지니어링·메모리 기초 | 1.0H | State 설계 감각 |
| 선택 | AI 코딩 도구 (Claude Code/Cursor) | 0.5H | 실습 속도는 오르나 본질 아님 |
| **제외** | RAG / 벡터DB | — | 그래프의 노드 *하나*일 뿐. 넣으면 하루가 RAG 수업 → **별도 과정** |
| **제외** | MCP 실습 | — | 개념 15분이면 충분. 실습 넣으면 연결 디버깅에 시간 소진 |
| **제외** | Docker / Langfuse self-host 구축 | — | 수강생이 직접 할 게 아니면 불필요 |
| **제외** | 파인튜닝 | — | 운영·관리 니즈와 무관 |
| **제외** | CrewAI 등 타 프레임워크 | — | 8H 안 깊이가 죽음 |

**→ 필수+강력권장 = 7.5H ≈ 선행 1일(8H)**

### 6-C. 대상별 총 분량 분기

| 수강생 프로필 | 선행 | 본과정 | 총 | 판단 |
|---|---|---|---|---|
| Python 능숙 + LLM API 경험 | 0.5일 (Pydantic·툴콜만) | 1일 | **1.5일** | 사전진단 상위군 |
| Python 가능, LLM API 처음 | 1일 | 1일 | **2일** ◆ | **가장 흔한 케이스** |
| Python 미숙 / 비개발자 포함 | 2일 (Python 기초 + 위) | 1일 | **3일** | 이탈 위험 — 분반 검토 |

> **결정 방법**: 추측하지 말고 **사전진단을 먼저 돌립니다.** 사내 자산 재활용 가능 — `projects/삼성전자_7-8월교육/진단/사전진단_가이드.md`

---

## 종합 — 우리가 서는 자리

```
축 1  통제 ────────────●───────── 자율        Graph (경로는 설계, 판단은 LLM)
축 2  Prompt ──────────●●──────── Graph       Loop~Graph 2개 층
축 3  고수준 ────────●─────────── 저수준      LangGraph 1.x 단일
축 4  SaaS ─────────────────●──── OSS         Langfuse (self-host)
축 5  얕음 ──────────●●───────── 깊음         트레젝토리 + 오프라인 회귀
축 6  0.5일 ───────────●───────── 10일        선행 1일 + 본과정 1일
```

**한 문장 포지셔닝**
> 경로를 미리 그릴 수 있는 기업 업무를, LangGraph로 설계하고 Langfuse로 관측·평가해 **개선 루프를 하루에 한 바퀴 완주**시키는 과정. 오픈소스 self-host 스택이라 **교육 후 사내에 그대로 남습니다.**

**차별점 3가지 (경쟁 교육 대비)**
1. CrewAI 데모형이 아니라 **LangGraph 단일 심화** — 상태·제어를 코드로
2. 설계만 가르치는 과정이 아니라 **관측·평가를 정식 모듈로** — AIOps/LLMOps 니즈에 직조준
3. **Self-host 가능한 오픈소스 스택** — 사내망 기업도 실제 도입 가능

---

## 아직 안 정해진 것 (고객 확인 필요)

| # | 질문 | 답에 따라 갈리는 것 |
|---|---|---|
| 1 | 수강생 Python·LLM API 숙련도? | 선행 0.5일 / 1일 / 2일 (축 6) |
| 2 | 사내망에서 LLM API·Langfuse 엔드포인트 접근 가능? | **불가 시 스택 전면 재설계** (로컬 LLM/프록시) |
| 3 | 교육 후 사내 도입까지 볼 것인가, 역량 인지까지인가? | 본과정 1일 vs 2일~ (축 6-A) |
| 4 | 보안·레드티밍 요구 있는가? | Promptfoo 모듈 추가 여부 (축 5) |
| 5 | 사내 스택이 MS 계열인가? | Microsoft Agent Framework 검토 (축 3) |
| 6 | RAG가 이미 사내에 있는가? | RAG를 그래프 노드로 넣을지 (축 6-B 제외 항목 재검토) |

---

## 참고 출처

**Graph Engineering 방법론**
- [3 Years of Graph Engineering with LangGraph — LangChain](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph)
- [Prompt Engineering vs Loop Engineering vs Graph Engineering — MarkTechPost](https://www.marktechpost.com/2026/07/29/prompt-engineering-vs-loop-engineering-vs-graph-engineering/)
- [Graph Engineering for AI Agents: A Complete Guide in LangGraph — Analytics Vidhya](https://www.analyticsvidhya.com/blog/2026/07/graph-engineering/)

**오케스트레이션 프레임워크**
- [The best AI agent frameworks in 2026 — LangChain](https://www.langchain.com/resources/ai-agent-frameworks)
- [A Detailed Comparison of Top 6 AI Agent Frameworks in 2026 — Turing](https://www.turing.com/resources/ai-agent-frameworks)
- [Best AI Agent Frameworks 2026: 7 Compared — AliceLabs](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026)
- [Multi-Agent Orchestration Frameworks 2026 — Presenc AI](https://presenc.ai/research/multi-agent-orchestration-frameworks-2026)
- [Benchmarking Multi-Agent Architectures — LangChain](https://www.langchain.com/blog/benchmarking-multi-agent-architectures)
- [Swarm vs. Supervisor: Multi-Agent Architecture Guide — Augment Code](https://www.augmentcode.com/guides/swarm-vs-supervisor)
- [LangChain and LangGraph Agent Frameworks Reach v1.0 Milestones](https://blog.langchain.com/langchain-langgraph-1dot0/)

**관측 플랫폼**
- [14 best AI agent observability tools in 2026 — Arize](https://arize.com/blog/best-ai-observability-tools-for-autonomous-agents-in-2026/)
- [LLMOps Observability: LangSmith vs Arize vs Langfuse vs W&B — Medium](https://medium.com/@kanerika/llmops-observability-langsmith-vs-arize-vs-langfuse-vs-w-b-f1baeabd1bbf)
- [Agent Observability: LangSmith, Langfuse, Arize 2026 — Digital Applied](https://www.digitalapplied.com/blog/agent-observability-platforms-langsmith-langfuse-arize-2026)
- [15 AI Agent Observability Tools in 2026 — AIMultiple](https://aimultiple.com/agentic-monitoring)
- [Langfuse Observability Overview](https://langfuse.com/docs/observability/overview)
- [LangChain Tracing & Callbacks — Langfuse](https://langfuse.com/integrations/frameworks/langchain)

**평가**
- [AI Agent Evaluation Frameworks (2026): 7 Compared — Morph](https://www.morphllm.com/ai-agent-evaluation-frameworks)
- [Top 5 LLM Evaluation Frameworks in 2026 — DeepEval](https://deepeval.com/blog/top-5-llm-evaluation-frameworks)
- [LLM Agent Evaluation Metrics in 2026 — Confident AI](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide)
- [The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break — arXiv](https://arxiv.org/html/2604.11978v1)
- [The Practitioner's Guide to AgentOps — MachineLearningMastery](https://machinelearningmastery.com/the-practitioners-guide-to-agentops/)
