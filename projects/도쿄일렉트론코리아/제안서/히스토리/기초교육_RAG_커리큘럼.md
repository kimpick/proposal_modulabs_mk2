# 도쿄일렉트론코리아 — RAG 기초 교육 과정 (제안용 초안)

> 총 24시간 | 오픈소스 프레임워크 기반 벤더 비종속 교육

기본 RAG 파이프라인을 이해하고 실무에 즉시 투입 가능한 수준까지 실습합니다.
Agentic RAG, GraphRAG 심화, 대규모 배포 등은 **후속 심화 과정**에서 다룹니다.

---

## 1단계: RAG 기초 및 데이터 처리 (8H)

| 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 및 구현 스택 |
|------|--------|---------------|----------------------|
| 2H | RAG 패러다임 이해 & LangChain 기본 | - Naive RAG의 한계와 Advanced RAG 진화 과정<br>- 엔터프라이즈 데이터 처리 철학 (Raw → Cleansed → Vectorized)<br>- LangChain 기본 구조 및 컴포넌트 이해 | - Python 기반 데이터 파이프라인 설계<br>- **LangChain 기본 개념 + 간단한 Chain 실습** |
| 3H | 벡터 검색 / 임베딩 핵심 개념 | - 텍스트 → 임베딩 변환 원리 (Dense / Sparse)<br>- 코사인 유사도, L2 거리 등 벡터 유사도 척도<br>- 벡터 DB 역할 및 인덱싱 기초 | - ChromaDB / Qdrant 벡터 DB 구축<br>- 임베딩 모델 비교 실습 (OpenAI, HuggingFace) |
| 3H | 비정형 데이터 파싱 & 시맨틱 청킹 | - **[Trend]** Vision LLM 기반 복잡한 표/이미지/PDF 파싱<br>- **[Trend]** Contextual & Semantic Chunking (문맥 보존 분할)<br>- 장비 매뉴얼 등 복잡한 비정형 문서 전처리 실무 | - Unstructured.io, PyMuPDF 활용<br>- 메타데이터 추출 및 필터링 실습 |

## 2단계: 검색 고도화 및 프롬프트 엔지니어링 (8H)

| 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 및 구현 스택 |
|------|--------|---------------|----------------------|
| 2H | 고급 프롬프트 엔지니어링 | - 프롬프트 구조에 따른 검색 품질 차이 체감<br>- System / Context / Instruction 프롬프트 설계<br>- Few-shot, Chain-of-Thought를 활용한 답변 품질 제어 | - 프롬프트 템플릿 설계 및 A/B 비교 실습<br>- RAG 파이프라인 내 프롬프트 최적화 |
| 3H | 하이브리드 검색 및 Re-ranking | - 하이브리드 검색 (키워드 + 시맨틱 검색 결합)<br>- Cross-Encoder를 활용한 검색 결과 재정렬(Re-ranking)<br>- BM25 Sparse Index와 Dense Vector의 상호 보완 | - Reciprocal Rank Fusion(RRF) 구현<br>- Cohere / BGE Re-ranker 연동 |
| 3H | Query Transformation | - **[Trend]** 사용자의 불완전한 질문을 재작성(Query Rewriting, HyDE)<br>- 질문 의도에 따라 데이터 소스를 분기하는 Semantic Routing | - LLM을 활용한 Query 분해 및 재작성 파이프라인 |

## 3단계: 인덱싱 고도화, 평가 및 온톨로지 기초 (8H)

| 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 및 구현 스택 |
|------|--------|---------------|----------------------|
| 3H | Multi-Representation 인덱싱 | - **[Paradigm]** 문서를 요약본으로 검색하고 원본을 반환하는 Multi-Vector Retriever 패턴<br>- 계층적(Hierarchical) 인덱싱 전략<br>- Parent-Document Retriever 구조 | - BM25 기반 Sparse Index 결합 실습<br>- Multi-Vector 검색 파이프라인 구축 |
| 3H | RAG 성능 측정 및 정량적 평가 | - **[Trend]** Context Precision, Answer Relevance 등 RAG 핵심 5대 지표 분석<br>- "시스템이 잘 동작하는가?"를 정량으로 판단하는 Evaluation 철학<br>- LLM을 심판(Judge)으로 활용한 자동화 평가 | - RAGAS / TruLens 프레임워크 실습<br>- 평가 데이터셋(Testset) 자동 생성 |
| 2H | 온톨로지 / 지식그래프 기초 | - 지식 그래프(Knowledge Graph)와 온톨로지 개념 이해<br>- Entity / Relation 추출 기초<br>- **대규모 구축 및 최적화는 심화 과정에서 다룸** | - 소규모 텍스트에서 Entity/Relation 추출 실습<br>- 그래프 기반 검색과 벡터 검색 비교 체험 |

---

## 심화 과정으로 이관되는 항목 (기초에서 제외)

| 항목 | 이관 사유 |
|------|----------|
| Agentic RAG & Self-Reflect (CRAG, Self-RAG) | 기본 RAG 파이프라인 이해를 방해할 수 있는 고난도 주제 |
| GraphRAG 심화 (대규모 지식 그래프 구축) | 기초에서 개념만 다루고, 구축/최적화는 심화에서 |
| 대규모 배포 (엔터프라이즈 인프라 세팅) | 기초 RAG 모델 완성 후 다루는 것이 적절 |
| AI Guardrails & 서빙 통합 | 기초 완성 후 프로덕션 단계에서 필요 |
| Azure Databricks & Telnuat | 벤더 종속 플랫폼 — 오픈소스 표준으로 기본 원리 우선 |

---

> * 본 과정은 오픈소스 프레임워크(LangChain 등)를 기반으로 하여 Databricks, AWS 등 어떠한 인프라에서도 구현 가능합니다.
