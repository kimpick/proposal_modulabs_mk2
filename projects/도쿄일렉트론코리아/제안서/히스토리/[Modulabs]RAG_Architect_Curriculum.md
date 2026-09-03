# 모두의연구소 — 최신 범용 Advanced & Agentic RAG 마스터 과정

> B2B Enterprise Training | 총 24시간

특정 벤더(Vendor)에 종속되지 않는 범용 프레임워크 기반 교육.
GraphRAG, Agentic RAG 등 글로벌 AI 패러다임을 주도하는 최신 기술을 내재화하여
어떤 클라우드 환경에서도 압도적인 검색 성능을 구현하는 엔지니어를 양성합니다.

---

## 1단계: 데이터 엔지니어링 및 Advanced 인덱싱 (8H)

| 시간 | 모듈명 | 핵심 패러다임 및 주요 학습 내용 | 주요 실습 및 구현 스택 |
|------|--------|-------------------------------|----------------------|
| 2H | RAG 패러다임 전환 | - Naive RAG의 한계와 범용 Advanced RAG 진화 과정<br>- 엔터프라이즈 데이터 처리 철학 (Raw → Cleansed → Vectorized) | - Python 기반 데이터 파이프라인 설계<br>- LangChain / LlamaIndex 기본 구조 |
| 3H | 비정형 데이터 파싱 & 시맨틱 청킹 | - **[Trend]** Vision LLM 기반 복잡한 표/이미지/PDF 파싱<br>- **[Trend]** Contextual & Semantic Chunking (문맥 보존 분할) | - Unstructured.io, PyMuPDF 활용<br>- 메타데이터 추출 및 필터링 실습 |
| 3H | Multi-Representation 인덱싱 | - **[Paradigm]** 문서를 요약본으로 검색하고 원본을 반환하는 Multi-Vector Retriever 패턴<br>- 계층적(Hierarchical) 인덱싱 전략 | - ChromaDB / Qdrant 벡터 DB 구축<br>- BM25 기반 Sparse Index 결합 실습 |

## 2단계: 검색 고도화 및 GraphRAG 패러다임 (8H)

| 시간 | 모듈명 | 핵심 패러다임 및 주요 학습 내용 | 주요 실습 및 구현 스택 |
|------|--------|-------------------------------|----------------------|
| 2H | 하이브리드 검색 및 Re-ranking | - 하이브리드 검색 (키워드 + 시맨틱 검색 결합)<br>- Cross-Encoder를 활용한 검색 결과 재정렬(Re-ranking) | - Reciprocal Rank Fusion(RRF) 구현<br>- Cohere / BGE Re-ranker 연동 |
| 3H | Query Transformation | - **[Trend]** 사용자의 불완전한 질문을 재작성(Query Rewriting, HyDE)<br>- 질문 의도에 따라 데이터 소스를 분기하는 Semantic Routing | - LLM을 활용한 Query 분해 및 재작성 파이프라인 |
| 3H | GraphRAG 기반 관계망 추론 | - **[Paradigm Shift]** 지식 그래프(Knowledge Graph)를 RAG에 결합하여 파편화된 정보의 맥락(Context) 연결 | - Neo4j / NebulaGraph 연동<br>- 텍스트에서 Entity/Relation 추출 |

## 3단계: Agentic RAG & 평가(Evaluation) (8H)

| 시간 | 모듈명 | 핵심 패러다임 및 주요 학습 내용 | 주요 실습 및 구현 스택 |
|------|--------|-------------------------------|----------------------|
| 3H | Agentic RAG & 자가 성찰(Self-Reflect) | - **[Paradigm Shift]** LLM이 스스로 검색 필요성을 판단하고 도구(Tool)를 호출하는 Agent 구조<br>- CRAG(Corrective RAG) 및 Self-RAG: 검색 문서의 품질을 스스로 평가하고 재검색 수행 | - LangGraph 기반 순환형(Cyclic) 파이프라인 워크플로우 구축 |
| 3H | LLM-as-a-Judge 정량적 평가 프레임워크 | - **[Trend]** Context Precision, Answer Relevance 등 RAG 핵심 5대 지표 분석<br>- LLM을 심판(Judge)으로 활용한 대규모 자동화 평가 | - RAGAS / TruLens 프레임워크 실습<br>- 평가 데이터셋(Testset) 자동 생성 |
| 2H | AI Guardrails 및 서빙 통합 | - 환각(Hallucination) 방지 및 민감 데이터 유출 차단을 위한 Guardrails<br>- 사내 REST API 통합 및 시스템 아키텍처(Databricks 등) 매핑 리뷰 | - NeMo Guardrails 활용<br>- FastAPI / 서빙 엔드포인트 연동 |

---

> * 위 과정은 오픈소스 프레임워크(LangChain 등)를 기반으로 하여 Databricks, AWS 등 어떠한 인프라에서도 구현 가능합니다.
