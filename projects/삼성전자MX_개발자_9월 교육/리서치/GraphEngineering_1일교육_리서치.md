# Graph Engineering 1일 실습 교육 — 리서치 메모

**작성일**: 2026-08-07
**배경**: 고객사에서 "AIOps / LLMOps가 중요해질 것 같다"는 의견. 핵심 포인트는 **"AI가 일하는 것을 관리할 수 있는 역량"**.
**가설**: Graph Engineering 방법론 + LangGraph 멀티에이전트 구성 + Langfuse 기반 트레이싱으로 1일 실습 과정을 구성한다. 이를 위한 선행 기초 tool 교육을 함께 설계한다.

---

## 0. 고객 니즈 재해석 — 왜 이 조합이 맞는가

고객이 말한 "AI가 일하는 걸 관리한다"는 두 가지 역량으로 쪼개집니다.

| 니즈 | 필요 역량 | 도구 |
|---|---|---|
| AI가 **어떻게 일할지 미리 설계**한다 | Graph Engineering (제어 구조·상태·종료조건 설계) | LangGraph |
| AI가 **실제로 어떻게 일했는지 보고 고친다** | Observability & Evaluation (트레이스·평가·회귀) | Langfuse |

즉 **"설계(Graph) → 실행 → 관측(Trace) → 평가(Eval) → 개선"의 닫힌 루프**를 하루 안에 한 바퀴 돌려보는 것이 이 과정의 실질적 목표입니다. 이 루프가 곧 업계에서 AgentOps / LLMOps라고 부르는 것의 최소 단위이고, 강의 메시지로도 가장 잘 팔립니다.

> **제안서 카피 후보**: "AI에게 일을 시키는 법에서, AI가 일하는 방식을 관리하는 법으로"

---

## 1. Graph Engineering이란 — 방법론 정리

### 1.1 용어의 위치: 5단 스택

2026년 7월경부터 업계에서 정리된 계층 구조입니다. **아래 층을 대체하는 게 아니라 위에 쌓입니다.**

```
Prompt Engineering    — 요청 한 번을 어떻게 쓸 것인가 (최소 단위)
  └ Context Engineering  — 그 프롬프트 주변에 무엇을 넣을 것인가 (메모리·검색·상태 슬라이스)
     └ Harness Engineering — 프롬프트/컨텍스트가 돌아가는 시스템 (도구·가드레일·검증)
        └ Loop Engineering   — 에이전트 1개의 반복을 자동화 (ReAct 루프, 종료조건)
           └ Graph Engineering  — 여러 에이전트·단계를 하나의 실행 가능한 그래프로 연결
```

**Graph Engineering 정의**: AI 애플리케이션을 *실행 가능한 그래프*로 표현하는 실천. 그래프에는 에이전트, 도구, 함수, 정책, 데이터 시스템, 평가자, 그리고 **사람의 결정**이 노드로 들어갑니다. 노드가 일을 하고, 엣지가 경로를 정하고, 공유 상태(State)가 그 위를 흐릅니다.

### 1.2 핵심 판단 기준 (이 한 줄이 교육의 중심)

> **경로를 미리 그릴 수 있으면 그래프(Graph). 경로를 실행하면서 찾아야 하면 에이전트 하네스(Loop).**

기업 업무 대부분(심사, 검토, 리포팅, 승인, 문서 생성)은 **경로를 미리 그릴 수 있습니다.** 그래서 기업교육에서 Graph Engineering이 특히 잘 맞습니다. 반대로 "일단 던져놓고 알아서 해봐"류는 루프 영역이고, 통제·감사가 어렵습니다. 이 구분이 고객이 말한 "관리 가능성"의 본질입니다.

### 1.3 설계 4요소 — 실습에서 반복시킬 체크리스트

| 요소 | 설계 질문 | LangGraph 대응 |
|---|---|---|
| **State** | 노드 간에 무엇을 넘기는가? 누가 덮어쓰고 누가 누적하는가? | TypedDict / Pydantic + reducer |
| **Node** | 한 노드의 책임 경계는 어디까지인가? | 함수 / 서브그래프 / ToolNode |
| **Edge** | 분기 조건은 무엇이고 누가 판단하는가 (LLM인가 코드인가)? | conditional edge, `Command` |
| **종료** | 언제 멈추는가? 스텝 예산·재시도 상한은? | 종료 조건 명시, step budget |

**현장에서 가장 많이 나는 사고는 4번(종료조건 없음)입니다.** Evaluator-Optimizer 루프에서 무한 핑퐁이 나거나, 장기 실행 에이전트가 스텝 예산을 소진하고 답을 내지 못하는 실패가 실행 트레이스 분석에서 최상위 실패 유형으로 보고됩니다. 실습에서 반드시 **일부러 터뜨려 보고** 고치게 해야 합니다.

### 1.4 패턴 카탈로그 (5종) 및 선택 기준

| 패턴 | 구조 | 언제 | 비고 |
|---|---|---|---|
| **Routing** | 요청 판별 후 전문 노드로 분기 | 요청 유형이 명확히 나뉠 때 | 가장 저렴, 가장 먼저 시도 |
| **Parallelization** | 독립 작업 fan-out → 병합 | 작업이 서로 독립일 때 | 지연시간 개선 효과 큼 |
| **Orchestrator-Worker (Supervisor)** | 코디네이터가 위임·통합 | 라우팅에 LLM 추론이 진짜 필요할 때 | **프로덕션에서 가장 널리 쓰이는 형태** |
| **Evaluator-Optimizer** | 생성자 / 검증자 분리, 통과까지 반복 | 품질 기준을 코드로 쓸 수 있을 때 | 종료조건 필수 |
| **Swarm / Network** | 위계 없는 peer 간 핸드오프 | 자율 협상이 필요할 때 | **토큰·호출 비용이 가장 비쌈** |

**실무 권고**: 평평한 Supervisor로 시작하고, 병목이 측정된 뒤에만 계층을 추가한다. 순차 작업·단일 검색에는 Supervisor를 쓰지 않는다 (LLM 라우팅 비용만 늘어남). Swarm 형태의 핸드오프는 같은 과제에서 subagent 패턴 대비 호출 수·토큰이 눈에 띄게 늘어난다는 벤치마크가 있어, "멋있어 보이는 구조가 비싸다"는 것을 실습에서 **비용 대시보드로 직접 보여주는 것**이 임팩트가 큽니다. (→ Langfuse 모듈과 자연스럽게 연결)

### 1.5 논쟁 포인트 (강의에서 언급하면 신뢰도 상승)

LangChain 측은 "Graph Engineering은 새로운 것이 아니라 LangGraph가 3년간 해온 것"이라는 입장입니다. 즉 **용어는 2026년 7월에 붙었지만 실체는 검증된 패턴**입니다. 교육 메시지로는 "유행어를 배우는 게 아니라, 3년치 프로덕션 교훈이 담긴 설계 규율을 배운다"로 잡는 게 안전하고 설득력 있습니다.

---

## 2. 기술 스택 리서치 — LangGraph / Langfuse

### 2.1 LangGraph (버전 상태 및 교육에 넣을 기능)

- **LangGraph 1.0 GA (2025-10)**, 이후 1.x 유지. 프로덕션 지향의 저수준 프레임워크로 포지셔닝.
- **주의 (커리큘럼 정확도 이슈)**: LangChain 1.0에서 `create_agent`가 표준이 되고, 기존 **`create_react_agent`는 deprecated**입니다. 옛 블로그·유튜브 자료를 그대로 쓰면 실습이 깨지므로 **교재는 반드시 1.x 기준으로 새로 작성**해야 합니다.

교육에 넣을 핵심 기능:

| 기능 | 교육 가치 |
|---|---|
| `StateGraph` + 타입 있는 State 스키마 + reducer | Graph Engineering 4요소 중 State를 코드로 체감 |
| conditional edge / `Command` | 분기 설계 |
| `ToolNode` | 도구 호출 표준화 |
| **Checkpointer** (InMemory / SQLite / Postgres) | 스레드 단위 지속성, 중단 후 재개 |
| **Time-travel** | 과거 상태로 되감아 재실행 — "관리 가능성"의 결정적 데모 |
| **`interrupt()` / `Command(resume=...)`** | Human-in-the-Loop 승인 게이트 — 기업 거버넌스 요구와 직결 |
| Streaming (토큰 / 노드 업데이트 / 커스텀) | 운영 UX |
| Subgraph | 팀 단위 모듈화, 인터럽트가 부모로 버블업 |

> **HITL은 이번 과정에서 빼지 마세요.** 기업 고객이 "AI를 관리한다"고 할 때 실제로 사고 싶어 하는 건 대개 *승인 게이트*와 *되감기*입니다. `interrupt` + time-travel 두 개가 그 답입니다.

### 2.2 Langfuse (LangSmith 대비 선택 근거 포함)

- 오픈소스 LLM 엔지니어링 플랫폼. **OpenTelemetry 기반** → 벤더 락인 낮음.
- LangChain/LangGraph용 **CallbackHandler**를 붙이면 LLM·툴·리트리버 호출이 자동으로 트레이스로 수집됨. 코드 침습도가 낮아 **1일 실습에 넣기 적합**.
- **Agent Graph View (2026-07~, beta)**: 트레이스에서 에이전트 그래프를 자동 추론해 시각화. **Aggregated**(전체 형상) / **Expanded**(스텝별 실행) 두 모드. → *"내가 설계한 그래프"와 "실제로 실행된 경로"를 나란히 놓고 비교*하는 실습이 가능합니다. **이 과정의 하이라이트 장면으로 추천합니다.**
- Sessions / user_id / tags / metadata — 멀티턴·에이전트 실행 묶어보기
- Scores: `create_score`, **LLM-as-a-judge**, 코드 평가자, 사용자 피드백, 수동 라벨링
- Datasets + `run_experiment` — 오프라인 평가 및 **회귀 테스트** (프롬프트/모델 변경 전후 비교)
- 프롬프트 관리(레지스트리), 플레이그라운드, 비용·지연 추적

**왜 LangSmith가 아니라 Langfuse인가 (고객 설득 논리)**
1. **오픈소스 self-host 가능** → 사내망·데이터 반출 제약이 있는 기업에서 실제 도입 가능
2. OpenTelemetry 표준 기반 → 기존 APM/관측 스택과 접점
3. LangChain 생태계에 종속되지 않음 → 나중에 프레임워크를 바꿔도 관측 레이어는 유지

> 사내 기존 사례: 현대자동차 심화, 기웅정보통신 심화에서는 **LangSmith**를 썼습니다. Langfuse는 이번이 첫 적용이 되므로, **강사 사전 검증(Langfuse Cloud 계정 or Docker self-host 리허설)이 필수**입니다.

---

## 3. 1일(8H) 실습 교육 커리큘럼 — 초안

**과정명(안)**: *Graph Engineering 실전 — LangGraph 멀티에이전트 설계와 Langfuse 관측·평가*
**부제(안)**: 설계 → 실행 → 관측 → 평가, AI의 일하는 방식을 관리하는 한 바퀴
**대상**: 선행 기초 과정 이수자 또는 Python·LLM API 경험자
**형태**: 실습 6H / 강의 2H (실습 75%)

| 모듈 | 시간 | 내용 |
|---|---|---|
| **M1. Graph Engineering 방법론** | **1.0H** | · Prompt → Context → Harness → Loop → Graph 5단 스택<br>· **"경로를 미리 그릴 수 있으면 그래프"** 판단 기준<br>· 설계 4요소(State / Node / Edge / 종료조건)<br>· 5대 패턴 카탈로그와 선택 기준(비용·지연 트레이드오프 포함)<br>· **[워크숍]** 각자 자기 업무 프로세스를 그래프로 그리기 (Mermaid, 25분) — 이 산출물이 하루 종일 따라다님 |
| **M2. LangGraph 코어 — 상태와 제어** | **2.0H** | · `StateGraph`, Pydantic State + reducer(덮어쓰기 vs 누적)<br>· 노드 / conditional edge / `Command`<br>· `ToolNode`로 도구 연결<br>· Checkpointer + thread → 중단·재개<br>· **[실습]** 조건 분기가 있는 단일 에이전트 그래프 완성 |
| **M3. 멀티에이전트 구성** | **2.0H** | · **[실습 A]** Supervisor(Orchestrator-Worker): 감독 노드가 전문 워커에 위임·통합<br>· **[실습 B]** 병렬 fan-out → fan-in<br>· **[실습 C]** Evaluator-Optimizer 자기수정 루프<br>· **[의도적 실패]** 종료조건 없이 무한 핑퐁을 만들어 본 뒤, 스텝 예산·종료 엣지로 수습 |
| **M4. Langfuse 트레이싱 — 실행을 들여다보기** | **1.5H** | · CallbackHandler 연결 (5줄)<br>· trace / span / generation 구조 읽기<br>· **Agent Graph View**로 *설계한 그래프* vs *실제 실행 경로* 비교<br>· session / user / tag로 실행 묶기<br>· 비용·지연 대시보드로 **Supervisor vs Swarm 비용 차이 실측**<br>· **[실습]** 고장난 실행 하나를 트레이스만 보고 원인 찾기 |
| **M5. 평가와 운영 루프** | **1.5H** | · 실패 트레이스 → **데이터셋에 등록**<br>· LLM-as-a-judge + 코드 평가자로 **스코어** 붙이기<br>· `run_experiment`로 프롬프트 수정 전후 **회귀 비교**<br>· `interrupt()` 승인 게이트 + time-travel 되감기<br>· **[마무리]** M1에서 그린 내 업무 그래프에 관측·평가·승인 게이트 붙이기 → 운영 체크리스트 도출 |
| 합계 | **8.0H** | |

### 최종 산출물 (수강생 1인 기준)
1. 동작하는 멀티에이전트 그래프 1개 (Supervisor + 자기수정 루프)
2. Langfuse 대시보드에 쌓인 실행 트레이스와 비용 리포트
3. 실패 케이스 기반 평가 데이터셋 + judge 스코어
4. 본인 업무 프로세스의 그래프 설계도 + 운영 체크리스트

### 설계 의도 (제안서에 쓸 근거)
- **하루 안에 루프를 완주**시키는 것이 핵심. 설계만 하고 끝나면 "관리 역량"이 남지 않고, 트레이싱만 하면 "왜 그렇게 설계했나"가 남지 않습니다.
- 의도적 실패(무한 루프) → 트레이스로 진단 → 평가로 재발 방지, 이 3연타가 AIOps/LLMOps의 정서적 실체를 하루에 전달합니다.
- M1 워크숍 산출물을 M5에서 회수하는 구조라 **"우리 업무에 뭘 적용할까"가 자연스럽게 남습니다.**

---

## 4. 선행 기초 tool 교육 — 리서치 결과 및 권고

### 4.1 무엇이 진짜 전제조건인가

리서치 기준 LangGraph의 명시적 전제조건은 두 가지로 수렴합니다.

> **① Chat model 다루기 ② Function/Tool calling**

여기에 실무적으로 하나가 더 붙습니다.

> **③ Pydantic 기반 구조화 출력** — LangGraph의 State 스키마와 도구 스키마가 전부 이 위에 서 있습니다. 이게 안 되면 M2에서 전원이 막힙니다.

**프로덕션 권고사항**: 에이전트 로직을 쓰기 *전에* 도구 스키마를 엄격한 타입·validator·description으로 먼저 정의하고, 그 스키마를 중심으로 그래프를 짠다. → 기초 과정의 뼈대가 여기서 나옵니다.

### 4.2 권장안 — 선행 1일(8H) "Agent 기초: 도구를 쓰는 AI 만들기"

| 모듈 | 시간 | 내용 | 본 과정과의 연결 |
|---|---|---|---|
| M0. 개발환경 셋업 | 0.5H | uv / 가상환경, `.env`·API 키 관리, VS Code(또는 Claude Code) | 실습 이탈률을 가장 크게 좌우 |
| M1. LLM API & 프롬프트·컨텍스트 기초 | 1.5H | Chat model 호출, 파라미터, 시스템 프롬프트, 컨텍스트 윈도우 감각 | 5단 스택의 1~2층 |
| M2. **구조화 출력 & Pydantic** | 1.5H | Pydantic v2 모델, `with_structured_output()`, 검증 실패 처리 | **→ M2 State 스키마의 전제** |
| M3. **Tool Calling & 단일 에이전트 루프** | 2.5H | 도구 정의(타입·description), `create_agent`, ReAct 루프, 종료 조건 | **→ M2 ToolNode, M3 워커의 전제** |
| M4. 컨텍스트 엔지니어링·메모리 기초 | 1.0H | 무엇을 넣고 무엇을 뺄 것인가, 대화 메모리 vs 장기 메모리 | **→ State 설계 감각** |
| M5. 미니 프로젝트 | 1.5H | **도구 2개를 쓰는 단일 에이전트 완성** | **★ 이 에이전트가 다음 날 그래프의 노드가 됩니다** |

**M5 → 본 과정 M3 연결이 이 2일 구성의 최대 강점입니다.** "어제 만든 내 에이전트를 오늘 그래프 안에 워커로 꽂는다" — 수강 만족도와 제안 설득력 모두에 유리합니다.

### 4.3 대상별 분기 — 사전 진단으로 결정

| 수강생 프로필 | 선행 과정 | 총 구성 |
|---|---|---|
| Python 능숙 + LLM API 경험 있음 | **0.5일(4H) 압축** (M2·M3만) | 1.5일 |
| Python 가능, LLM API 처음 | **1일(8H) 권장안** | 2일 |
| Python 미숙 / 비개발자 포함 | 선행 2일 (Python 기초 1일 + 위 1일) | 3일 |

> 사내에 **사전진단 자산이 있습니다**: `projects/삼성전자_7-8월교육/진단/사전진단_가이드.md`. 이 건에도 재활용해 Python·API·LangChain 경험을 먼저 측정하고 선행 과정 길이를 확정할 것을 권합니다.

### 4.4 기초 과정에 **넣지 말 것** (스코프 방어)

| 항목 | 판단 |
|---|---|
| RAG / 벡터DB | 그래프의 노드 *하나*일 뿐. 넣으면 하루가 RAG 수업이 됨 → **별도 과정** |
| MCP | 개념 15분 언급으로 충분. 실습 넣으면 도구 연결 디버깅에 시간 다 씀 |
| Docker / 배포 | Langfuse self-host를 수강생이 직접 할 게 아니면 불필요 |
| 파인튜닝 | 이번 니즈(운영·관리)와 무관 |
| CrewAI 등 타 프레임워크 | 이번엔 **LangGraph 단일**로 가는 게 8H 안에서 깊이가 나옴 |

---

## 5. 사내 자산 및 차별점

| 자산 | 위치 | 활용 |
|---|---|---|
| 멀티에이전트 오케스트레이션 실전 (8H) | `projects/삼성전자MX_트랙2 최종/멀티에이전트_오케스트레이션_실전/` | **5대 패턴 카탈로그를 그대로 재활용 가능** (M1). 단 CrewAI 비중이 높고 관측/평가가 없음 |
| AI Agent 심화 10일 (LangGraph+LangSmith+HITL) | `projects/현대자동차/제안서_H2심화/` | 장기 과정 설계·HITL 정책 참고 |
| 개발자 AI 심화 (LangGraph Multi-Agent + LangSmith) | `projects/기웅정보통신/개발자_AI_심화_교육안/` | 모니터링·비용 추적 모듈 참고 |
| 사전진단 가이드 | `projects/삼성전자_7-8월교육/진단/` | 선행 과정 길이 결정 |

**이번 과정의 차별점 3가지**
1. **CrewAI를 걷어내고 LangGraph 단일** → 8H 안에서 상태·제어를 깊게
2. **Langfuse(오픈소스·self-host 가능) 관측/평가를 정식 모듈로 편성** → 사내망 기업도 실제 도입 가능
3. **"Graph Engineering"이라는 최신 방법론 프레임으로 재포장** → AIOps/LLMOps 니즈에 정확히 조준

---

## 6. 리스크 및 사전 확인 사항

| 리스크 | 대응 |
|---|---|
| **Langfuse 사내 첫 적용** | 강사 리허설 필수. Langfuse Cloud 사용 가능 여부 / 불가 시 Docker self-host 사전 구축 |
| **사내망 방화벽** — LLM API·Langfuse 엔드포인트 차단 | 요구조건 수집 시 **반드시 사전 확인**. 차단 시 로컬 LLM 또는 프록시 대안 필요 |
| **`create_react_agent` deprecated** | 교재를 LangChain/LangGraph **1.x 기준으로 신규 작성**. 기존 자료 재사용 시 검증 |
| 8H에 M1~M5 과밀 | 코드 스캐폴딩(빈칸 채우기) 제공으로 타이핑 시간 제거. 완성 코드 단계별 체크포인트 배포 |
| 수강생 수준 편차 | 사전진단 → 선행 과정 길이 확정. 보조강사 1명 편성 검토(견적 +₩100,000/시간) |

---

## 7. 다음 단계

1. **고객사·대상·인원·일정 확정** → 선행 과정 길이 결정(0.5일 / 1일 / 2일)
2. 사전진단 설문 발송 (기존 가이드 재활용)
3. 사내망·API 접근 가능 여부 확인
4. 확정되면 `/setup {기업명}`으로 요구조건 → content.json → PDF 진행

---

## 참고 출처

- [3 Years of Graph Engineering with LangGraph — LangChain](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph)
- [Prompt Engineering vs Loop Engineering vs Graph Engineering — MarkTechPost](https://www.marktechpost.com/2026/07/29/prompt-engineering-vs-loop-engineering-vs-graph-engineering/)
- [Graph Engineering for AI Agents: A Complete Guide in LangGraph — Analytics Vidhya](https://www.analyticsvidhya.com/blog/2026/07/graph-engineering/)
- [Prompt vs Loop vs Graph Engineering — Medium](https://medium.com/the-gravity/prompt-vs-loop-vs-graph-engineering-565bf0ba714d)
- [Benchmarking Multi-Agent Architectures — LangChain](https://www.langchain.com/blog/benchmarking-multi-agent-architectures)
- [Multi-Agent Orchestration in LangGraph: Supervisor vs Swarm — DEV](https://dev.to/focused_dot_io/multi-agent-orchestration-in-langgraph-supervisor-vs-swarm-tradeoffs-and-architecture-1b7e)
- [Swarm vs. Supervisor: Multi-Agent Architecture Guide — Augment Code](https://www.augmentcode.com/guides/swarm-vs-supervisor)
- [LangChain and LangGraph Agent Frameworks Reach v1.0 Milestones](https://blog.langchain.com/langchain-langgraph-1dot0/)
- [LangGraph 1.0 GA — LangChain Changelog](https://changelog.langchain.com/announcements/langgraph-1-0-is-now-generally-available)
- [Human-in-the-Loop and Interrupts — DeepWiki (langchain-ai/langgraph)](https://deepwiki.com/langchain-ai/langgraph/3.7-human-in-the-loop-and-interrupts)
- [Langfuse Observability Overview](https://langfuse.com/docs/observability/overview)
- [LangChain Tracing & Callbacks — Langfuse](https://langfuse.com/integrations/frameworks/langchain)
- [AI Agent Observability, Tracing & Evaluation with Langfuse](https://langfuse.com/blog/2024-07-ai-agent-observability-with-langfuse)
- [langfuse/langfuse — GitHub](https://github.com/langfuse/langfuse)
- [Langfuse for LLM Observability: Tracing & Evals (2026 Guide) — QASkills](https://qaskills.sh/blog/langfuse-llm-observability-guide-2026)
- [LangGraph Structured Output & Self-Correcting Agents — MachineLearningPlus](https://machinelearningplus.com/gen-ai/langgraph-structured-output-validation-self-correcting/)
- [LangGraph — Structuring LLM Tool Calls with Pydantic — Medium](https://medium.com/@shuv.sdr/langgraph-structuring-llm-tool-calls-with-pydantic-and-json-serialization-1715f7a0c2e0)
- [The Practitioner's Guide to AgentOps — MachineLearningMastery](https://machinelearningmastery.com/the-practitioners-guide-to-agentops/)
- [AI Agent Observability: A Complete Guide for 2026 — Atlan](https://atlan.com/know/ai-agent-observability/)
- [The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break — arXiv](https://arxiv.org/html/2604.11978v1)
- [LLM Agent Evaluation Metrics in 2026 — Confident AI](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide)
