# 삼성전자MX 개발자 9월 교육

> AIOps/LLMOps 니즈 대응 — Graph Engineering 중심 LangGraph 멀티에이전트 + Langfuse 관측·평가 교육

## 현황

| 항목 | 상태 |
|---|---|
| 요구조건 | 🟡 v1 초안 (고객 확인 대기) |
| 리서치 | ✅ 완료 |
| content.json | ⬜ 미착수 |
| PDF 제안서 | ⬜ 미착수 |
| 견적서 | ⬜ 미착수 |

**다음 액션**: 고객 확인 6문항 회신 대기 (최우선 = 사내망에서 LLM API·Langfuse 접근 가능 여부)

## 폴더 구조

```
삼성전자MX_개발자_9월 교육/
├── README.md                 ← 이 파일 (프로젝트 현황·인덱스)
├── 요구조건.md               ← 항상 최신 버전 (단일 진실)
├── 요구조건_history/         ← 요구조건 변경 시 이전 버전 아카이브
├── 회의록/                   ← 회의록·이메일 등 변경 출처 원본
├── 리서치/
│   ├── GraphEngineering_1일교육_리서치.md   ← 방법론·커리큘럼 초안·선행과정 권고
│   └── GraphEngineering_교육_스펙트럼.md    ← 6개 축 선택지 비교 + 권장 포지션
└── 제안서/                   ← content.json / proposal_render.html / PDF
```

## 핵심 방향 요약

**한 문장**: 경로를 미리 그릴 수 있는 기업 업무를 LangGraph로 설계하고 Langfuse로 관측·평가해 **개선 루프를 하루에 한 바퀴 완주**시키는 과정. 오픈소스 self-host 스택이라 교육 후 사내에 그대로 남습니다.

- **선행 1일** (Agent 기초: Tool Calling · Pydantic 구조화 출력 · 단일 에이전트)
- **본과정 1일** (Graph Engineering: 설계 → 관측 → 평가 루프)
- 선행 과정 산출물(단일 에이전트)이 본과정 그래프의 **워커 노드로 그대로 투입**

## 워크플로우

```
/setup 삼성전자MX_개발자_9월 교육     → 요구조건 + content.json + PDF
/review 삼성전자MX_개발자_9월 교육    → 4차원 커리큘럼 검토
/build 삼성전자MX_개발자_9월 교육     → PDF 재빌드
/estimate 삼성전자MX_개발자_9월 교육  → 견적서 + CSV + 이메일 초안
```
