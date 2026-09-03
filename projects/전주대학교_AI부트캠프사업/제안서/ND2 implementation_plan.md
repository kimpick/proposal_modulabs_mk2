# 전주대학교 AI 부트캠프 커리큘럼 개편 기획안 (ND1 & AI 기초)

이전 제안서(content.json)에서 **'AI 기초(45H)'로 잘못 명명되었던 과정이 실제로는 'ND1(피지컬 AI 핵심 기초)'의 초안**이었음을 확인했습니다. 

따라서 기존 45시간짜리 초안(LLM/Transformer 기초 20H, 로봇공학 10H, ROS2 10H, 물리시뮬레이션 5H)을 모태로 하여 역량과 실습의 깊이를 고도화해 **90시간 분량의 완벽한 ND1 과정**으로 확장합니다. 

아울러, 부트캠프의 진짜 첫 관문이 될 **'AI 기초(45H)' 과정은 바이브 코딩과 에이전트 맛보기를 전면 배치하여 완전히 새롭게 기획**합니다.

## User Review Required
> [!IMPORTANT]
> - 기존 45시간 초안의 4개 모듈(LLM, 로봇, ROS2, 시뮬레이션)을 90시간으로 2배 확대하면서 비율을 어떻게 가져갈지 (예: 시뮬레이션과 ROS 연동 비중 강화) 확인이 필요합니다.
> - 새롭게 기획한 'AI 기초(45H)' 내용(바이브 코딩, 프롬프트, API 활용 등)이 의도하신 바가 맞는지 리뷰를 부탁드립니다.

---

## Proposed Changes

### 1. ND2. 합성 데이터 및 멀티모달 데이터셋 구축 (중급, 60H) 신규 기획

엑셀(전주대_BIZ_이관)에 명시된 필수 모듈(⑭, ⑯, ⑨, ④)을 준수하여 총 60시간(각 15시간) 설계로 맞춥니다. 피지컬 AI에 필수적인 '가상 시뮬레이션 환경 기반의 합성 데이터 생성'부터 '멀티모달 시각 인지 모델 활용'까지 이어지는 커리큘럼입니다.

*   **[M14] Isaac Sim / Omniverse 입문 (15H)**
    1. 물리 엔진 및 NVIDIA Omniverse 생태계 이해, USD (Universal Scene Description) 포맷 구조 파악
    2. 로봇 시뮬레이터(Isaac Sim) 튜토리얼 (환경 세팅, 센서 부착, 로봇 제어)
    3. 도메인 랜덤화(Domain Randomization) 개념 이해 및 조명/텍스처 무작위화 파이프라인 실습
*   **[M16] 합성데이터·라벨링 파이프라인 구축 (15H)**
    1. Isaac Sim 기반 Synthetic Data Generation (SDG) 파이프라인 실습
    2. 바운딩 박스(2D/3D), 시맨틱 세그멘테이션, 깊이(Depth) 맵 자동 라벨링 추출 (Replicator 기반)
    3. 생성된 데이터셋 분석 및 딥러닝 학습용 포맷 전환(YOLO format 등)
*   **[M9] 로봇 비전·인지: 탐지·추적·포즈 (15H)**
    1. 로봇 환경에서의 Computer Vision 기초 (OpenCV 심화 및 ROS2 연동)
    2. 합성 데이터로 파인튜닝한 YOLOv8 모델을 이용한 객체 탐지 및 추적(Tracking)
    3. 6D Pose Estimation 인지 모델 실습 및 ROS2 환경 퍼블리시
*   **[M4] 멀티모달 LLM(VLM) & Grounding 심화 (15H)**
    1. VLM (LLaVA, GPT-4o 등) 시각 인지 및 Open-Vocab 기반 객체 탐지(Grounding DINO) 특성 파악
    2. 합성(가상) 이미지 vs 실제 이미지(Real)의 도메인 갭 분석 (Sim2Real 관점)
    3. (캡스톤/통합) 특정 공간의 다양한 변화(도메인 랜덤화)를 준 합성 데이터를 생성하고 VLM 에이전트를 이용해 환경을 구조화(Grounding)하는 워크플로 구축

### 2. ND1. 피지컬 AI 핵심 기초 (중급, 60H) — 기존 45H 초안의 확장

기존 초안의 4개 모듈 기반에서, 모든 모듈을 **균일하게 15시간**으로 배분하여 오픈소스 생태계와 이론적 깊이를 더한 60시간 코스로 재설계합니다.

*   **[M1] LLM 파운데이션 & 임베딩 (15H)**
    *   Transformer Attention 수식 심화 및 오픈소스 LLM(1.5B/8B) 아키텍처 이해
    *   HuggingFace 기반 파인튜닝 맛보기 및 로컬 LLM 추론 실습
*   **[M7] 로봇공학 이론 및 피지컬 인지 (15H)**
    *   로봇 기구학 수식 기반 파이썬 구현(Numpy) 및 가시화
    *   카메라/LiDAR 센서 데이터 처리 및 오픈소스 인지 모델(YOLO, Grounding DINO) 적용
*   **[M8] ROS2 생태계 및 통신 심화 (15H)**
    *   ROS2 Node, Topic, Service, Action 구조의 파이썬 기반 심화 개발 실습
    *   오픈소스 로봇(Turtlebot3/UR)의 URDF 패키지 분석 및 TF2 좌표 변환 실습
*   **[M13] 물리 시뮬레이션 및 에이전트 연동 (15H)**
    *   Isaac Sim 및 MuJoCo 환경 구축, 강체 동역학 기초
    *   LLM 작업 분해 → ROS2 Action 통신 연동 → 시뮬레이션 픽앤플레이스 파이프라인 단대단 연동

### 3. ND5. 로보틱스 LLM 에이전트 구축 (고급, 60H)

마찬가지로 4개 모듈을 각각 **15시간**으로 배분하여, 심화된 LLM 에이전트 구축 및 로봇 통합을 60시간 분량으로 설계합니다.

*   **[M2] 프롬프트 엔지니어링 & RAG 심화 (15H)**
    *   로봇 특화 문서(매뉴얼 등) 기반 RAG 시스템 단대단 구축
    *   환각 방지 전략 수립 및 프롬프트 캐싱/최적화 기법
*   **[M4] 멀티모달 LLM(VLM) & Grounding (15H)**
    *   자연어 명령 -> 시각 환경 인식(VLM) -> 오픈 보캐블러리 기반 좌표 출력(Grounding) 실습
    *   안전성을 위한 Fallback 설계 지표 측정
*   **[M6] 에이전트 · 플래닝 · 정렬 (15H)**
    *   ReAct, Plan-and-Execute 패턴 기반 LLM 에이전트 구축 (LangChain/LlamaIndex)
    *   다단계 작업 계획(Multi-step Task Planning) 에이전트 완성
*   **[M12] LLM · 로봇 시스템 통합 캡스톤 (15H)**
    *   로봇 시뮬레이터를 활용한 전체 에이전트 파이프라인 E2E 완성 (LLM 두뇌 + VLM 인지 + ROS2 제어)
    *   실시간 모니터링 및 성능 최적화, 팀 프로젝트 최종 결과물 도출

---

## Verification Plan

### Manual Verification
1.  이 기획안([implementation_plan.md](file:///C:/Users/Admin/.gemini/antigravity/brain/548d8067-902c-475d-9f0a-443680aa957d/implementation_plan.md))의 구성이 기존 파일([content.json](file:///C:/Users/Admin/Downloads/ai-education-proposal/projects/KCH/Step1_AI_%EB%A7%88%EC%9D%B8%EB%93%9C%EC%85%8B_%EC%84%B8%EB%AF%B8%EB%82%98/content.json))의 의도를 올바르게 90H로 확장했는지 확인합니다.
2.  사용자(USER)에게 바이브 코딩이 포함된 신규 AI 기초(45H)와 심화된 ND1(90H)의 모듈별 시간 배분을 승인받습니다.
