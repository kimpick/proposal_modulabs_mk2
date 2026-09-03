# 도쿄일렉트론코리아 — RAG 교육 종합 제안서

> 모두의연구소 (B2B Enterprise Training)

---

## 1. 교육 개요

| 항목 | 내용 |
|------|------|
| 과정명 | RAG 기초 및 심화 교육 과정 |
| 대상 | 도쿄일렉트론코리아 사내 엔지니어 |
| 총시간 | 48시간 (기초 24H + 심화 24H) |
| 일정 | 3일 × 3회 (기초-심화-기초), 총 9일 |
| 장소 | 강남 모두연 교육장 |
| 교육방식 | 강의 + 실습 (각 50% 비중) |
| 1일 학습시간 | 8시간 (09:00 ~ 18:00, 점심 포함) |

## 2. 교육 목표

### 기초 과정 (24H)
- RAG 파이프라인의 핵심 구조(임베딩, 벡터 검색, 청킹)를 이해하고 직접 구현
- LangChain 기반 기본 RAG 시스템을 구축하고 평가할 수 있는 역량 확보
- Agentic RAG, GraphRAG 등 심화 과정 진입을 위한 기반 완성

### 심화 과정 (24H)
- 온톨로지 + LLM 하이브리드 벡터화를 활용한 고도화된 인덱스 파이프라인 구축
- Agentic RAG, GraphRAG를 통한 지능형 검색 시스템 구현
- 사내 인프라(Azure Databricks) 기반 프로덕션급 배포 및 운영 역량 확보

## 3. 일정 후보 (기초 → 심화 → 기초)

| 회차 | 1차 후보 | 2차 후보 | 과정 | 비고 |
|------|---------|---------|------|------|
| 1차 (기초) | 4/28 (월) ~ 4/30 (수) | — | 기초 과정 | 1그룹 |
| 2차 (심화) | 5/12 (월) ~ 5/14 (수) | — | 심화 과정 | 공통 |
| 3차 (기초) | 5/19 (월) ~ 5/21 (수) | 5/26 (월) ~ 5/28 (수) | 기초 과정 | 2그룹 |

> 강사 섭외 일정에 따라 상기 후보 중 조정 가능.

## 4. 기초 과정 상세 커리큘럼 (24H)

### 1일차: RAG 기초 및 데이터 처리 (8H)

| 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 |
|------|--------|---------------|----------|
| 2H | RAG 패러다임 이해 & LangChain 기본 | Naive RAG 한계, Advanced RAG 진화, LangChain 기본 구조 | Python 데이터 파이프라인, LangChain Chain 실습 |
| 3H | 벡터 검색 / 임베딩 핵심 개념 | 임베딩 원리, 벡터 유사도, 벡터 DB 인덱싱 | ChromaDB/Qdrant 구축, 임베딩 모델 비교 |
| 3H | 비정형 데이터 파싱 & 시맨틱 청킹 | **[Trend]** Vision LLM PDF 파싱, Contextual/Semantic Chunking | Unstructured.io, PyMuPDF, 메타데이터 추출 |

### 2일차: 검색 고도화 및 프롬프트 엔지니어링 (8H)

| 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 |
|------|--------|---------------|----------|
| 2H | 고급 프롬프트 엔지니어링 | 프롬프트 구조별 검색 품질 차이, Few-shot/CoT | 프롬프트 A/B 비교, RAG 프롬프트 최적화 |
| 3H | 하이브리드 검색 및 Re-ranking | 키워드+시맨틱 결합, Cross-Encoder Re-ranking | RRF 구현, Cohere/BGE Re-ranker 연동 |
| 3H | Query Transformation | **[Trend]** Query Rewriting, HyDE, Semantic Routing | LLM Query 분해/재작성 파이프라인 |

### 3일차: 인덱싱 고도화, 평가 및 온톨로지 기초 (8H)

| 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 |
|------|--------|---------------|----------|
| 3H | Multi-Representation 인덱싱 | **[Paradigm]** Multi-Vector Retriever, 계층적 인덱싱 | BM25 결합, Multi-Vector 검색 파이프라인 |
| 3H | RAG 성능 측정 및 정량적 평가 | **[Trend]** RAG 핵심 5대 지표, LLM-as-a-Judge | RAGAS/TruLens, Testset 자동 생성 |
| 2H | 온톨로지 / 지식그래프 기초 | 지식 그래프 개념, Entity/Relation 추출 기초 | 소규모 Entity/Relation 추출, 그래프-벡터 비교 |

---

## 5. 심화 과정 상세 커리큘럼 (24H)

### 1일차: 하이브리드 벡터화 고도화 (8H)

| 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 |
|------|--------|---------------|----------|
| 3H | 온톨로지 스키마 설계 & 엔티티 자동 추출 | **[Core]** 도메인 온톨로지 설계, LLM 기반 대규모 Entity 추출 | Neo4j 스키마 모델링, 장비 매뉴얼 추출 파이프라인 |
| 3H | 온톨로지-LLM 하이브리드 벡터화 | **[Core]** 지식 그래프 반영 하이브리드 임베딩, 메타데이터 활용 | Graph+Vector 하이브리드 인덱스, 필터링 검색 |
| 2H | 대규모 데이터 적재 및 인덱스 최적화 | 배치 처리, Incremental Index 갱신, 벡터 DB 튜닝 | 대규모 적재 실습, 배치 임베딩 파이프라인 |

### 2일차: 고도화된 검색 파이프라인 (8H)

| 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 |
|------|--------|---------------|----------|
| 3H | GraphRAG 기반 관계망 추론 | **[Paradigm Shift]** Multi-Hop 맥락 검색, 그래프+벡터 결합 | Neo4j Cypher+Vector 하이브리드, Multi-Hop 추론 |
| 3H | Agentic RAG & 자가 성찰 | **[Paradigm Shift]** Agent 구조, CRAG, Self-RAG | LangGraph 순환형 파이프라인, Tool-calling Agent |
| 2H | 검색 품질 고도화 및 End-to-End 평가 | 단계별 병목 진단, A/B 테스트 기반 개선 | RAGAS 심화 평가, 파이프라인 프로파일링 |

### 3일차: 사용자 검색 경험 및 프로덕션 배포 (8H)

| 시간 | 모듈명 | 핵심 학습 내용 | 주요 실습 |
|------|--------|---------------|----------|
| 3H | 사용자 검색 인터페이스 설계 | **[Core]** 자연어 질의→검색→결과 렌더링, 대화형 검색 | FastAPI 검색 API, Streamlit/Gradio 데모 UI |
| 3H | 사내 인프라 통합 (Azure Databricks) | Databricks 배포, Telnuat 연동, 사내 데이터소스 연결 | Databricks Notebook 배포, REST API 연동 설계 |
| 2H | AI Guardrails & 운영 체계 | Hallucination 방지, 기밀 유출 차단, 품질 모니터링 | NeMo Guardrails, 모니터링 대시보드 설계 |

---

## 6. 사전 환경 구성 안내 (개인 PC)

교육 시작 전 아래 환경을 개인 노트북에 구성해 주셔야 합니다.
설치 과정에서 어려움이 있을 경우 사전 지원을 드립니다.

### 필수 설치

| 항목 | 버전 | 용도 | 설치 방법 |
|------|------|------|----------|
| Python | 3.10 이상 | 실습 언어 | [python.org](https://python.org) |
| VS Code | 최신 | 코드 편집기 | [code.visualstudio.com](https://code.visualstudio.com) |
| Git | 최신 | 버전 관리 | [git-scm.com](https://git-scm.com) |
| conda (Miniconda) | 최신 | 가상환경 관리 | [docs.conda.io](https://docs.conda.io/en/latest/miniconda.html) |

### Python 패키지 (사전 설치)

```bash
# 가상환경 생성 및 활성화
conda create -n rag-course python=3.10 -y
conda activate rag-course

# 필수 패키지 설치
pip install langchain langchain-openai langchain-community
pip install llama-index
pip install chromadb qdrant-client
pip install unstructured pymupdf
pip install ragas trulens
pip install sentence-transformers
pip install neo4j              # 심화 과정용
pip install langgraph          # 심화 과정용
pip install fastapi uvicorn    # 심화 과정용
pip install streamlit          # 심화 과정용
pip install jupyter notebook
```

### API 키 준비

| 서비스 | 용도 | 준비 방법 |
|--------|------|----------|
| OpenAI API Key | LLM 호출, 임베딩 | [platform.openai.com](https://platform.openai.com) |

> API 키는 교육 당일 안내드리는 방식으로 개별 설정합니다.

### 심화 과정 추가 환경

| 항목 | 용도 | 설치 방법 |
|------|------|----------|
| Docker Desktop | Neo4j 등 컨테이너 실행 | [docker.com](https://docker.com) |
| Neo4j Desktop | 지식 그래프 DB (로컬) | [neo4j.com/download](https://neo4j.com/download) |

### 환경 구성 점검 스크립트

교육 전일에 아래 명령어로 설치 상태를 확인합니다:

```bash
python --version        # Python 3.10+
conda --version         # conda 설치 확인
pip list | grep lang    # LangChain 패키지 확인
pip list | grep chroma  # ChromaDB 확인
```

---

## 7. 교육장 안내

| 항목 | 내용 |
|------|------|
| 장소 | 강남 모두연 교육장 |
| 주소 | 서울특별시 강남구 (상세 주소 별도 안내) |
| 시간 | 09:00 ~ 18:00 (점심시간 12:00~13:00 포함) |
| 준비물 | 개인 노트북 (사전 환경 구성 완료 필수) |
| 제공 | Wi-Fi, 전원, 간식 (별도 협의) |

---

## 8. 참고사항

- 본 과정은 오픈소스 프레임워크(LangChain 등)를 기반으로 하여 Databricks, AWS 등 어떠한 인프라에서도 구현 가능합니다.
- 기초 과정 이수자를 대상으로 심화 과정이 진행됩니다.
- 교육 자료 (실습 코드, 슬라이드)는 사전에 공유드립니다.
- 일정 및 세부 내용은 협의 후 조정 가능합니다.
