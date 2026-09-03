# 전주대학교 AI 부트캠프 커리큘럼 리팩토링 체크리스트 (ND1 & ND5 최적화)

## 1. 사전 분석 및 문제 식별 (완료)
- [x] ND1 및 ND5 데이터 소스([content.json](file:///c:/Users/Admin/Downloads/ai-education-proposal/projects/%EC%A0%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90_AI%EB%B6%80%ED%8A%B8%EC%BA%A0%ED%94%84%EC%82%AC%EC%97%85/%EC%A0%9C%EC%95%88%EC%84%9C/content.json)) 분석 완료
- [x] **모듈간 중복 방지**: ND2(M4)와 ND5(M4)의 중복성을 해소하기 위해 ND5 M4를 VLM 기반 인지에서 VLA(Vision-Language-Action) 및 공간 지능 모델로 고도화 기획
- [x] **실습(교육용 오픈소스) vs 사례(초거대/산업용 하이엔드)** 분리 원칙을 ND1과 ND5 전 모듈에 맵핑 계획 수립

## 2. [content.json](file:///c:/Users/Admin/Downloads/ai-education-proposal/projects/%EC%A0%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90_AI%EB%B6%80%ED%8A%B8%EC%BA%A0%ED%94%84%EC%82%AC%EC%97%85/%EC%A0%9C%EC%95%88%EC%84%9C/content.json) 데이터 리팩토링 (예정)
- [ ] **전체 개요(Intro/Objective) 흐름 강화**: ND1(물리적/통신 기반) -> ND2(시각 인지/데이터) -> ND5(두뇌/행동 플래닝)로 이어지는 3단계 파이프라인 스토리텔링을 보다 명확하고 세련되게 수정
- [ ] **ND1 트랙 고도화**:
  - [ ] M1 (LLM 파운데이션): 이론(GPT-4 등 LLM 진화 사례) vs 실습(Llama-3 8B 등 로컬 파인튜닝) 분리
  - [ ] M7 (로봇공학): 이론(휴머노이드 기구학 사례) vs 실습(Numpy 기반 기초 기구학 연산) 분리
  - [ ] M8 (ROS2 생태계): 사례(산업용 AMR 통신망) vs 실습(Turtlebot/UR 파이썬 노드 통신) 분리
  - [ ] M13 (물리시뮬레이션): 사례(오픈AI/딥마인드 로보틱스 강화학습 환경) vs 실습(MuJoCo/Isaac 픽앤플레이스) 분리
- [ ] **ND5 트랙 고도화**:
  - [ ] M2 (RAG 심화): 사례(엔터프라이즈 RAG 탐색) vs 실습(ChromaDB + 로봇 매뉴얼 RAGAS 평가) 분리
  - [ ] M4 (이름 변경: VLA 및 공간 지능): **ND2와의 차별화**. 사례(Google RT-2, Figure 01) vs 실습(OpenVLA 등 액션 모델 기초 및 공간 지능) 구축
  - [ ] M6 (에이전트 플래닝): 사례(Devin, AutoGPT 등 자율 에이전트) vs 실습(LangGraph/LlamaIndex 기반 워크플로우 추적) 분리
  - [ ] M12 (통합 캡스톤): 사례(실제 E2E 로봇 시스템) vs 실습(LeRobot + ROS2 통합 시뮬레이션 제어) 분리
- [ ] **기술 스택 및 산출물 정비**: VLA (Vision-Language-Action), LangGraph 등 최신 키워드 트렌드 추가 및 ND1/ND5 산출물 내 '하이엔드 사례 분석안' 포함

## 3. 검증 및 렌더링 (예정)
- [ ] JSON 포맷 유효성 검사 (JSON Lint)
- [ ] `update_content_nd1_nd5.py` 스크립트 작성 및 실행
- [ ] HTML / PDF 빌드 및 시각적 검토
