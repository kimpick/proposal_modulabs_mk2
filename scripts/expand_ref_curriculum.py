# -*- coding: utf-8 -*-
"""레퍼런스 소개 content.json — 5개 레퍼런스의 상세 커리큘럼을 원본 수준으로 전부 수록."""
import json

P = "/home/user/propsal_modulabs/projects/Physical AI 레퍼런스/레퍼런스 소개/content.json"
d = json.load(open(P, encoding="utf-8"))


def M(name, dur, items):
    return {"module_name": name, "duration": dur, "items": items}


# ══════════════════════════════════════════════════════════
# 01. 특강형 18H — 온라인 집중 특강 (시간표 단위 전체)
# ══════════════════════════════════════════════════════════
t18 = {
    "track_id": "01",
    "track_name": "특강형 · 18H",
    "course_title": "Physical AI 온라인 집중 특강 [운영]",
    "target": "대학원생 10명 내외 · 비대면(ZOOM)",
    "duration": "총 18시간 (3일)",
    "tools": ["LeRobot", "PPO / SAC", "ACT / Diffusion Policy", "SmolVLA", "OpenVLA"],
    "modules": [
        M("[1일차] Physical AI의 개념과 강화학습", "8H", [
            "10:00~11:00 오리엔테이션 및 Physical AI 개념 이해 — 교육 목적 및 전체 흐름 안내 / Physical AI 개요 / Physical AI의 발전 방향",
            "11:00~12:00 AI 전체 택사노미 — 지도학습과 비지도학습 / 강화학습과 모방학습 / 모방학습과 강화학습의 차이 설명",
            "12:00~13:00 강화학습 개념 — 마르코프 프로퍼티 / 마르코프 결정 과정(MDP)",
            "14:00~15:00 강화학습 알고리즘 — 다이나믹 프로그래밍 & 몬테카를로 방법 / TD & SARSA / Q-Learning",
            "15:00~16:00 Deep RL 1 — DQN / REINFORCE",
            "16:00~17:00 Deep RL 2 — A2C / PPO",
            "17:00~18:00 LeRobot 소개 — LeRobot 소개 / LeRobot 구성 요소",
        ]),
        M("[2일차] Physical AI 하드웨어와 모방학습", "8H", [
            "10:00~10:50 로봇 하드웨어 — 로봇의 기본 구성요소 / 로봇 하드웨어 발전사 / 최신 휴머노이드 및 특수 로봇",
            "11:00~11:50 로보틱스 — Rotation / Forward & Inverse Kinematics / Control",
            "12:00~12:50 모방학습 기법 1 — Behavior Cloning / DAgger",
            "14:00~14:50 모방학습 기법 2 — Inverse Reinforcement Learning / GAIL",
            "15:00~15:50 모방학습 기법 3 — Multi-modal IL / ACT",
            "16:00~16:50 모방학습 최신 기법 — Diffusion Policy / Flow-matching",
            "17:00~17:50 LeRobot 분석 — LeRobot 환경 구성 / LeRobot 코드 분석",
        ]),
        M("[3일차] Physical AI 실습 과정과 VLA", "4H", [
            "09:00~09:50 VLA 소개 및 개요 — LLM & VLM & VLA / VLA Dataset / VLA Model",
            "10:00~10:50 VLA 상세 — RT-1, RT-2 & OpenVLA / Pi0 & OpenVLA-OFT / Pi0.5 & GR00T N",
            "11:00~11:50 LeRobot 학습 — LeRobot 데이터 수집 / 데이터 구조 / 학습",
            "12:00~12:50 LeRobot 추론 — LeRobot 추론 / SmolVLA",
        ]),
        M("[교육 목표]", "—", [
            "Physical AI의 개념을 이해하고, 그 이론적 토대가 되는 강화학습 알고리즘을 설명할 수 있다",
            "로봇 하드웨어 제어를 위한 로보틱스 기초 이론을 이해하고, 주요 모방학습 기법을 구분할 수 있다",
            "영상·언어 기반 행동 제어(VLA)의 핵심 개념을 이해하고, LeRobot을 활용한 데이터 학습 및 추론 과정을 시연을 통해 확인한다",
        ]),
    ],
}

# ══════════════════════════════════════════════════════════
# 02. 단기 집중 28H — 재직자 대면 (운영 완료, 시간표 단위 전체)
# ══════════════════════════════════════════════════════════
t28 = {
    "track_id": "02",
    "track_name": "단기 집중 · 28H",
    "course_title": "디지털 트윈으로 만나는 Physical AI [운영 완료 · 성과 검증]",
    "target": "Physical AI에 관심 있는 재직자·실무자 (대기업·연구기관 엔지니어 다수 참여)",
    "duration": "총 28시간 (7H × 4회, 주 1회 토요일 10:00~17:00)",
    "tools": ["Unity", "LeRobot (실물)", "MuJoCo", "PPO / SAC", "ACT / Diffusion Policy", "SmolVLA"],
    "modules": [
        M("[성과] 정량 지표", "검증", [
            "수료 40명 — 목표 20명 대비 달성률 200% (수료 기준: 1회 이상 참여, 출석부 서명)",
            "전반 만족도 4.46 / 5.0 · 강사 만족도 4.55 · 과정 구성 4.51 · 교육환경 4.22 · 추천 의향 4.49",
            "수강생 자가평가 역량 3.14 → 4.02 (+0.88 상승)",
            "회차별 신청/출석 — 1회차 34/22 · 2회차 36/23 · 3회차 41/20 · 4회차 39/17",
            "대기업·연구기관 현업 엔지니어 다수 참여, 전 4회차 운영 완료",
        ]),
        M("[1회차] 로봇 제어 기초 — Physical AI를 위한 디지털 트윈 구축", "7H", [
            "10:00~10:50 오리엔테이션 및 Physical AI 개념 이해 — 교육 목적 및 전체 흐름 / Physical AI의 정의와 사례 (이론 1H)",
            "11:00~11:50 디지털 트윈 개념 및 구조 이해 — 구성요소(센서·시뮬레이터·제어기) / 실제 로봇-가상 환경 간 데이터 동기화 방식 (이론 1H)",
            "12:00~12:50 LeRobot 실습 — 실습 환경 구성 / LeRobot 센서 제어 / LeRobot 모터 제어 (실습 1H)",
            "14:00~14:50 Unity 디지털 트윈 실습 ① — Unity 설치 및 기본 조작 / URDF·FBX 모델 가져오기 / LeRobot 로봇 모델 불러오기 및 환경 구성 (실습 1H)",
            "15:00~15:50 Unity 디지털 트윈 실습 ② — 센서 데이터 시각화 / ROS·Socket 연동 실시간 데이터 전송 / 모션 시뮬레이션 및 PID 제어 (실습 1H)",
            "16:00~16:50 LeRobot 통합 테스트 — Unity 시뮬레이션 ↔ LeRobot 제어 연동 / 센서 입력 기반 동작 시연 및 종합 실습 (실습 1H)",
            "활용 장비·SW: Unity, LeRobot / 사전 준비물: 개인 노트북, 필기도구",
        ]),
        M("[2회차] 시뮬레이션을 활용한 로봇 제어 — 가상/실물 환경에서의 제어", "7H", [
            "10:00~10:50 강화학습 이론 — 마르코프 결정 과정(MDP) / 벨만 방정식 / 동적 다이나믹 / 몬테카를로 · TD법 / 신경망과 Q러닝 / DQN (이론 1H)",
            "11:00~11:50 강화학습 시뮬레이션 실습 — PPO 알고리즘 원리 / SAC 알고리즘 원리 / 보상 함수 설계 / MuJoCo 환경 구성 및 정책 학습 (실습 1H)",
            "12:00~12:50 MuJoCo 환경 구성 실습 — LeRobot URDF·MJCF 모델 로딩 / 로봇 관절 상태 데이터 확인 / 시뮬레이터 카메라 및 GUI 조작 (실습 1H)",
            "14:00~14:50 LeRobot + MuJoCo 가상환경 실습 1 — 설치 / 1. 시연 데이터 수집 / 2. 데이터 재생 / 3. ACT(행동-청킹-트랜스포머) 훈련 (실습 1H)",
            "15:00~15:50 LeRobot + MuJoCo 가상환경 실습 2 — 4. 정책 배포 / 5-6. 언어 조건 환경에서 데이터 수집 및 시각화 / 7. SmolVLA 학습 및 배포 (실습 1H)",
            "16:00~16:50 실제 환경 LeRobot 데이터 수집 — 실습 환경 구성 / teleoperation을 통한 데이터 수집 (실습 1H)",
            "활용 장비·SW: MuJoCo, LeRobot / 사전 준비물: 개인 노트북, 필기도구",
        ]),
        M("[3회차] AI·로봇 피킹 시스템 구축 — Physical AI 지능 고도화", "7H", [
            "10:00~10:50 강화학습과 모방학습 비교 — 모방학습 vs 강화학습 / 강화학습 PPO 설명 / 강화학습 SAC 설명 (이론 1H)",
            "11:00~11:50 모방학습: ACT — 모방학습의 개념 / ACT(Action Chunking Transformer) 구조 이해 (이론 1H)",
            "12:00~12:50 모방학습: Diffusion Policy — Diffusion Policy 구조 이해 (이론 1H)",
            "14:00~14:50 모방학습: ACT 데이터 수집 — LeRobot을 이용한 데이터 수집 (실습 1H)",
            "15:00~15:50 모방학습: ACT 학습 — Colab 기반 학습 환경 구축 / ACT 학습 파이프라인 (실습 1H)",
            "16:00~16:50 모방학습: ACT Inference 및 평가 — 학습된 ACT 모델 추론 / Trajectory 분석 및 행동 비교 (실습 1H)",
            "활용 장비·SW: MuJoCo, LeRobot / 사전 준비물: 개인 노트북, 필기도구",
        ]),
        M("[4회차] 비전 및 딥러닝 기초 — VLA 기반 통합 에이전트", "7H", [
            "10:00~10:50 VLA 개요 및 원리 이해 — VLM 개념 및 구조 / CLIP·BLIP 기반 시각-언어 매핑 / VLA의 행동 제어 원리 (이론 1H)",
            "11:00~11:50 MuJoCo + LeRobot 환경 구축 및 VLA 연동 — MuJoCo 시뮬레이터 설정 / LeRobot SDK 설치 및 로봇 제어 실습 (실습 1H)",
            "12:00~12:50 SmolVLA 모델 분석 — Vision-Language-Action 모델 구조 분석 / SmolVLA 아키텍처 분석 및 경량화 특징 (이론 1H)",
            "14:00~14:50 데이터 수집 — SmolVLA 모델과 로봇 제어 연결 / 언어 명령 → 행동 출력 연동 테스트 / LeRobot 기반 멀티모달 데이터 수집(시각+언어+행동) (실습 1H)",
            "15:00~15:50 SmolVLA 학습 파이프라인 — 입력 토큰화 및 데이터셋 구성 / 사전학습 모델 로딩 및 Fine-tuning 실습 (실습 1H)",
            "16:00~16:50 자연어 명령 기반 시연 및 평가 — 자연어 명령 기반 로봇 행동 시연 / 멀티모달 입력(영상+텍스트) 기반 행동 생성 / 정확도·일관성 평가 및 성능 분석 (실습 1H)",
            "활용 장비·SW: MuJoCo, LeRobot / 사전 준비물: 개인 노트북, 필기도구",
        ]),
    ],
}

# ══════════════════════════════════════════════════════════
# 03. 정규 교과 45H×2 (+ 연계 45H×3)
# ══════════════════════════════════════════════════════════
t45 = {
    "track_id": "03",
    "track_name": "정규 교과 · 45H × 2 (+연계 135H)",
    "course_title": "대학 정규 교과 — 피지컬AI실습 초급 / 중급 [설계·제안]",
    "target": "대학 학부·대학원 정규 교과 편성 (학점 이수, 기업 참여 멘토링 연계)",
    "duration": "45H × 2과목 · 연계 교과 포함 시 Physical AI 계열 최대 225H",
    "tools": ["Unity", "Phosphobot", "MuJoCo", "LeRobot", "OpenVLA / SmolVLA",
              "Diffusion Policy", "ROS2 / Gazebo", "Jetson / TensorRT"],
    "modules": [
        M("[초급 45H] 피지컬AI실습 — 시뮬레이션 기반 로봇 제어 입문", "45H", [
            "Embodied AI와 Digital Twin 입문 (3H) — Embodied AI 개념 이해 및 Digital Twin 기술(Unity) 기초 환경 구축 / 실습: Unity 설치 및 기본 환경 구축",
            "Unity 기초와 가상 환경 제어 (6H) — Unity 인터페이스 익히기 및 가상 물리 환경 내 객체 제어 기초 / 실습: 가상 환경에서 객체 제어",
            "LeRobot 오픈소스 활용 기초 (6H) — LeRobot 플랫폼 설치 및 기본 예제 실행, 로봇 팔 제어 구조 파악 / 실습: LeRobot 설치 및 로봇 팔 제어",
            "[프로젝트] Phosphobot 제어 실습 (6H) — 소형 로봇(Phosphobot)의 구동 원리 이해 및 기초 모션 제어 프로젝트",
            "강화학습(RL) 기초 구현 (6H) — 강화학습의 기본 원리(Agent·Environment·Reward) 이해 / 실습: Grid World 강화학습 에이전트 구현",
            "MuJoCo 물리 엔진 활용 (6H) — MuJoCo 시뮬레이터 환경 설정 및 로봇 모델 로딩, 물리 상호작용 테스트",
            "LeRobot with MuJoCo (6H) — MuJoCo 환경 내에서 LeRobot 라이브러리를 활용한 로봇 팔 제어 시뮬레이션",
            "[프로젝트] 기초 주행 로봇 시뮬레이션 (6H) — 가상 환경 내 주행 로봇의 이동 제어 및 센서 데이터 처리 기초 구현",
            "※ 전 모듈 기업 실무 멘토링 연계 편성",
        ]),
        M("[중급 45H] 피지컬AI실습 — VLA 파인튜닝과 Sim2Real", "45H", [
            "심화 강화학습(RL) 로봇 제어 (9H) — PPO·SAC 등 최신 RL 알고리즘을 MuJoCo 환경의 로봇 팔/휴머노이드에 적용 및 학습",
            "확산 모델(Diffusion) 기반 제어 (6H) — 생성형 AI인 Diffusion Model을 로봇 행동 생성(Policy)에 적용하는 최신 기법 실습",
            "[프로젝트] LeRobot 심화: Data Collection (6H) — LeRobot 플랫폼을 활용한 로봇 데모 데이터 수집 파이프라인 구축 및 동작(Move) 생성",
            "Vision-Language-Action (VLA) 기초 (3H) — 시각(Vision)과 언어(Language)를 로봇 행동(Action)으로 연결하는 VLA 모델 이해",
            "VLA 모델 파인튜닝 (9H) — OpenVLA 등 사전 학습된 VLA 모델을 특정 로봇 작업에 맞게 미세 조정(Fine-tuning)",
            "SmolVLA 경량화 모델 활용 (6H) — 엣지 환경을 고려한 소형 VLA 모델(SmolVLA)의 배포 및 추론 최적화",
            "[프로젝트] Digital Twin 기반 Sim2Real (6H) — 시뮬레이션에서 학습된 VLA/Diffusion 정책을 가상 환경 내 다양한 시나리오에서 검증",
        ]),
        M("[연계 교과 ①] 고급딥러닝", "45H", [
            "딥러닝 레이어 심층 분석 (3H) — 선형 레이어의 수학적 원리, 가중치 행렬의 역할, 실전 구현 및 최적화",
            "Convolution 레이어 심층 분석 (3H) — 합성곱 레이어의 수학적 원리, 다양한 커널 설계, 파라미터 효율성 분석",
            "Embedding 레이어 이해 (3H) — 임베딩의 개념, 단어·범주형 데이터의 벡터 표현, 차원 축소 효과",
            "Recurrent 레이어와 시계열 (3H) — RNN·LSTM·GRU 구조적 차이, 그래디언트 소실 문제 해결",
            "시퀀스 투 시퀀스 모델 (3H) — Seq2Seq 구조, Encoder-Decoder 아키텍처, 시계열 예측 및 제어 응용",
            "[프로젝트] 작사가 인공지능 구현 (3H) — LSTM을 활용한 텍스트 생성 모델",
            "강화학습 기초 이론 (3H) — MDP, Bellman Equation, Value Function과 Policy의 이해",
            "Deep Q-Network (3H) — Q-Learning의 딥러닝 확장, Experience Replay, Target Network",
            "Policy Gradient Methods (3H) — REINFORCE, Actor-Critic 구조, A2C/A3C",
            "PPO와 SAC 알고리즘 (3H) — Proximal Policy Optimization, Soft Actor-Critic 원리 및 로봇 제어 응용",
            "Vision-Language-Action 모델 (3H) — 시각과 언어를 행동으로 연결하는 VLA 모델의 구조와 원리, 멀티모달 학습",
            "Diffusion Models for Control (3H) — Diffusion 모델의 원리, 로봇 행동 생성(Policy) 적용, Diffusion Policy 이해",
            "Imitation Learning 심화 (3H) — Behavioral Cloning, DAgger, Inverse RL의 원리 및 로봇 학습 응용",
            "[프로젝트] 딥러닝 기반 로봇 제어 (6H) — 강화학습·VLA·Diffusion 기법을 활용한 시뮬레이션 로봇 제어 종합 프로젝트",
        ]),
        M("[연계 교과 ②] 인공지능과 자율주행", "45H", [
            "자율주행 기술 개요 (3H) — 자율주행 레벨, 핵심 기술(인지·판단·제어), ROS2 미들웨어의 이해",
            "ROS2와 시뮬레이션 환경 (3H) — ROS2 노드·토픽 통신, Gazebo 시뮬레이터 설치 및 환경 설정",
            "[실습] ROS2 프로그래밍 기초 (3H) — Python 기반 ROS2 Publisher/Subscriber 구현 및 센서 데이터 처리",
            "컴퓨터 비전 기반 차선 인식 (3H) — OpenCV 이미지 전처리, 엣지 검출, 차선 추출 알고리즘 구현",
            "[프로젝트] 라인 트래킹 로봇 구현 (9H) — PID 제어를 활용한 시뮬레이션 차선 추종 주행",
            "LiDAR 센서와 장애물 감지 (3H) — LiDAR 데이터 구조, 포인트 클라우드 처리, 장애물 거리 측정 및 회피",
            "[프로젝트] 장애물 회피 주행 (9H) — 동적·정적 장애물 인식 및 회피 경로 생성 주행",
            "sLAM과 내비게이션 (3H) — 위치 추정(Localization), 지도 작성(Mapping), 경로 계획(Path Planning)",
            "강화학습 기반 자율주행 (3H) — 자율주행에 적용되는 강화학습(DQN·PPO) 개념 및 모델 학습 기초",
            "[프로젝트] 도심 주행 시뮬레이션 (6H) — 신호등·교차로 등 복잡한 도심 환경 자율주행 미션 수행",
        ]),
        M("[연계 교과 ③] 임베디드 운영체제 (Edge AI)", "45H", [
            "Edge AI 개요와 아키텍처 (3H) — 클라우드 AI vs Edge AI 비교, Edge Computing의 필요성 및 산업 응용",
            "엣지 디바이스 환경 구축 (3H) — NVIDIA Jetson, Raspberry Pi 등 주요 엣지 디바이스 및 개발 환경 설정",
            "경량 AI 프레임워크 입문 (3H) — TensorFlow Lite, ONNX Runtime, PyTorch Mobile 온디바이스 추론",
            "모델 경량화 ① Quantization (3H) — 양자화 원리 및 Dynamic/Static Quantization 적용, INT8 최적화",
            "모델 경량화 ② Pruning (3H) — 가지치기 원리 및 Structured/Unstructured Pruning, Fine-tuning 후 성능 비교",
            "TensorRT 추론 최적화 (3H) — NVIDIA TensorRT 추론 가속화 및 Jetson 배포 실습",
            "ROS2 기초와 로봇 제어 (3H) — ROS2 핵심 개념, 노드·토픽 프로그래밍 및 로봇 제어 기초",
            "Gazebo 시뮬레이션 환경 (3H) — Gazebo 활용 로봇 환경 구성 및 센서 시뮬레이션",
            "센서 기반 주행 제어 (3H) — OpenCV 라인 감지, LiDAR 기반 장애물 회피 시스템 구현",
            "[프로젝트] 강화학습 자율주행 (3H) — TD3·SAC 등 강화학습 기반 자율주행 모델 학습 및 시뮬레이션",
            "실시간 비전 AI on Edge (3H) — 경량 객체 탐지(YOLO-Nano), 얼굴 인식, Pose Estimation 엣지 실행",
            "온디바이스 음성·언어 AI (3H) — Whisper Tiny, Small LLM 등 경량 모델을 엣지 디바이스에 배포",
            "Edge AI 시스템 통합 (3H) — 센서 데이터 수집, AI 추론, 액추에이터 제어를 통합한 엣지 시스템 설계",
            "[최종 프로젝트] Edge AI 솔루션 개발 ① (3H) — 실제 문제 해결을 위한 시스템 설계 및 하드웨어 선정",
            "[최종 프로젝트] Edge AI 솔루션 개발 ② (3H) — 경량 AI 모델 배포, 실시간 추론, 하드웨어 통합 및 최종 시연",
        ]),
    ],
}

# ══════════════════════════════════════════════════════════
# 04. 나노디그리 180H — ND1 / ND2 / ND5 (원본 모듈 전체)
# ══════════════════════════════════════════════════════════
t180 = {
    "track_id": "04",
    "track_name": "나노디그리 · 60H × 3",
    "course_title": "국책 부트캠프 — Physical AI 나노디그리 3종 (총 180H) [설계·제안]",
    "target": "부트캠프 수강생 (비전공자 포함) · 절대평가 75점 이상, 포트폴리오 + 캡스톤",
    "duration": "60H × 3과목 = 총 180시간 (집중이수, 주 5일 몰입형)",
    "tools": ["ROS2 (Humble)", "Isaac Sim / MuJoCo", "YOLO11", "Florence-2 / Qwen3-VL",
              "FoundationPose", "OpenVLA", "LangChain / LangGraph", "ChromaDB", "MLflow / W&B"],
    "modules": [
        M("[ND1] 피지컬 AI 핵심 기초 — 중급 (60H)", "60H", [
            "M1. LLM 파운데이션 & 임베딩 (15H) — [이론/사례 5H] 언어 모델과 Transformer 논리 구조 심화 및 초거대 AI 진화 사례 분석 · [실습 6H] NVIDIA GPU 환경 기반 경량 SLM(Llama-3 8B, Qwen 1.5B) 로컬 파인튜닝 및 추론 · [캡스톤 4H] HuggingFace 생태계 기반 커스텀 언어 모델 구축",
            "M7. 로봇공학 이론 및 피지컬 인지 (15H) — [이론/사례 4H] 로봇 기구학 기본 원리 및 Tesla Optimus·Boston Dynamics 휴머노이드 모션 제어 사례 · [실습 6H] Numpy 기반 6DoF 산업용 매니퓰레이터(UR) 순기구학 계산 및 공간 좌표 가시화 · [실습 5H] 카메라·LiDAR 센서 데이터 기초 처리 및 Pinhole 캘리브레이션 코딩",
            "M8. ROS2 생태계 및 로봇 통신 심화 (15H) — [이론/사례 5H] ROS2 아키텍처 및 DDS 개념, 공장·물류 현장 다수종 AMR 통합 통신망 구축 사례 · [실습 6H] Turtlesim·Turtlebot3 가상 노드를 활용한 Python Topic/Action 통신망 구축 · [실습 4H] URDF 모델 구조 분석 및 TF2 기반 조인트 간 동적 좌표 변환 노드 구현",
            "M13. 물리 시뮬레이션 및 에이전트 기반 연동 (15H) — [이론/사례 5H] 강체 동역학 및 MuJoCo 물리 엔진 구조, OpenAI·DeepMind 대규모 병렬 강화학습 시뮬레이터 사례 · [실습 5H] MuJoCo/Isaac Sim 구동, 파이썬 API 기반 로봇 스폰 및 기초 토크 제어 · [캡스톤 5H] ROS2 Action 연동 시뮬레이션 환경 내 Pick & Place 단대단 구현",
        ]),
        M("[ND2] 합성 데이터 및 멀티모달 데이터셋 구축 — 중급 (60H)", "60H", [
            "M14. Isaac Sim / Omniverse 입문 (15H) — [이론/사례 5H] 디지털 트윈 시뮬레이터 구조(USD) 철학 및 NVIDIA GR00T·Cosmos 적용 사례 분석 · [실습 5H] 교육용 PC 사양에서 구동되는 Isaac Sim 환경 구축, 무인 이동체·매니퓰레이터 로드 · [실습 5H] Replicator 파이프라인 API 코딩을 통한 도메인 랜덤화(빛·재질·카메라 노이즈) 구성",
            "M16. 합성데이터·라벨링 파이프라인 구축 (15H) — [이론/사례 4H] Sim2Real 픽셀·피처 도메인 갭 발생 원인 분석 및 합성 데이터 유효성 지표(PGR) · [실습 6H] Isaac Sim 기반 2D 바운딩 박스 및 시맨틱 세그멘테이션 마스크 자동 대량 추출 · [실습 5H] 렌더링 메타데이터를 Ultralytics YOLO 학습 포맷으로 데이터셋화하는 파이프라인 작성 및 통계 분석",
            "M9. 로봇 비전 인지: 탐지·추적·포즈 (15H) — [이론/사례 4H] 2D/3D 컴퓨터 비전 인지 수학적 기초 및 제로샷 6D Pose 모델(FoundationPose) 트렌드 · [실습 6H] YOLO11을 활용한 합성 데이터 전용 객체 탐지 파인튜닝 · [캡스톤 5H] 실장비 소량 데이터 vs 시뮬레이션 합성 대량 데이터 혼합 학습 검증 및 mAP 산출",
            "M4. 멀티모달 LLM (VLM) 심화 (15H) — [이론/사례 4H] 초거대 상용 VLM의 공정 자동화 시각 검수 및 산업 불량 검출 현장 적용 사례 · [실습 6H] Colab·기본 PC에서 구동되는 오픈소스 VLM(Florence-2, Qwen-VL-3B) 설치 및 추론 · [캡스톤 5H] 합성 이미지 내 다중 객체에 대한 VQA 및 자연어 기반 객체 Grounding",
        ]),
        M("[ND5] 로보틱스 LLM 에이전트 구축 — 고급 (60H)", "60H", [
            "M2. 프롬프트 엔지니어링 & RAG 심화 (15H) — [이론/사례 4H] 프롬프트 체인 고도화 전략 및 엔터프라이즈 Search 기반 RAG 파이프라인 사례 · [실습 6H] 로봇 제조사 PDF 매뉴얼·ROS2 도큐먼트를 색인(ChromaDB)하는 단대단 RAG 시스템 구축 · [실습 5H] 환각 억제 Guardrail 설계 및 RAGAS 정량 지표 기반 신뢰성 개선 실험",
            "M4. VLA 및 공간 지능의 이해 (15H) — [이론/사례 4H] 입력-시각-행동을 종단간 직결하는 RT-2, Figure 01 등 VLA 파운데이션 동향 분석 · [실습 5H] OpenVLA 레이어 구조 탐구 및 로봇 3D 공간 제어 좌표계 반환 메커니즘 해석 · [실습 6H] 사물 관계 추론 및 지시어에 숨겨진 공간 지능 분해 및 프롬프트 파싱",
            "M6. 에이전트 플래닝 및 정렬 (15H) — [이론/사례 4H] ReAct 구조의 한계 분석과 계층적 멀티 에이전트 트렌드 · [실습 6H] LangGraph 기반 상태(State)를 가지는 다단계 워크플로우 제어망 에이전트 구축 · [실습 5H] 도구 풀(액션 공간) 정의 및 MLflow 연동 에이전트 사고 추적(Tracing)·플래닝 성능 검증",
            "M12. 로봇 시스템 E2E 통합 캡스톤 (15H) — [이론/사례 4H] Task Layer → Skill Layer → Action Layer 3원화 시스템 상용 아키텍처 사례 · [실습 5H] HuggingFace LeRobot 연계 통신 및 LLM 에이전트 결과를 ROS2 Action 서버 목표 좌표로 변환하는 브릿지 레이어 구축 · [캡스톤 6H] 자연어 지시만으로 '인지 → 플래닝 → 로봇 움직임 → 자체 검증'이 이루어지는 데모 시연",
        ]),
        M("[운영 체계] 전체 나노디그리 로드맵", "—", [
            "초급 — AI 기초 (3학점, 집중이수, P/F 결과물 제시)",
            "중급 — ND1 피지컬 AI 핵심 기초 / ND2 합성 데이터 및 멀티모달 데이터셋 구축 / ND3 자율주행 및 로봇 인지 (각 6학점)",
            "고급 — ND4 Sim2Real 로봇 제어 전문가 / ND5 로보틱스 LLM 에이전트 구축 / ND6 산업 디지털 트윈 및 LLM 배포 (각 6학점)",
            "평가 — 절대평가 75점 이상, 포트폴리오 + 캡스톤",
            "운영 — 1학기 AI 기초(야간·주말) / 하계 ND1·ND2·ND3 몰입형(주 5일) / 2학기 AI 기초 / 동계 ND1·ND5, ND2·ND3 몰입형",
        ]),
    ],
}

# ══════════════════════════════════════════════════════════
# 05. 전문가 양성 840H
# ══════════════════════════════════════════════════════════
t840 = {
    "track_id": "05",
    "track_name": "전문가 양성 · 840H",
    "course_title": "제조 혁신 Physical AI 전문가 과정 (6개월) [설계·제안]",
    "target": "제조·로봇 분야 입문자 및 개발자, Python 프로그래밍 기초 역량 보유자 (정원 25명)",
    "duration": "총 840시간 / 120일 / 6개월 · 비대면 실시간 100% · 프로젝트 454H(54%)",
    "tools": ["NVIDIA Isaac Sim", "Isaac Lab", "LeRobot", "Diffusion Policy",
              "ROS2", "PyTorch", "Jetson / TensorRT", "컴퓨터 비전"],
    "modules": [
        M("[훈련 목표]", "—", [
            "제조 현장의 비전 검사, 로봇 제어, 시뮬레이션 구현 역량을 갖춘 Physical AI 전문가 양성",
            "AI 직무: Physical AI 엔지니어 (AI 융합가 직군)",
            "디지털 트윈 기반 공정 시뮬레이션 및 Physical AI 솔루션 구축으로 생산 최적화 가능한 인력 배출",
            "산학 협업 구조 — 도메인 전문가(시뮬레이션·로보틱스)가 현장 요구사항 정의 및 데이터 특성 자문, AI 전문인력이 모델링 및 Sim-to-Real 전이 학습 설계",
        ]),
        M("[정규 교과 ①] 기초 다지기", "98H", [
            "아이펠 적응하기 (14H) — 협업 툴 및 교육 철학 이해, 리눅스·터미널 기초, GitHub 사용법 및 레포지토리 구성 실습",
            "딥러닝 기초 다지기 (49H) — 데이터 전처리·시각화, 사이킷런 머신러닝, Regularization·비지도학습, 캐글 경진대회 실습",
            "딥러닝 심화 (35H) — 파이토치 기초, CNN·RNN 구현, Transformer 이해, 모델 구현 실습",
        ]),
        M("[정규 교과 ②] Physical AI 핵심", "267H", [
            "컴퓨터 비전 (49H) — Object Detection, Segmentation, Depth Estimation, 산업용 비전 검사 시스템",
            "NVIDIA Isaac Sim (56H) — Isaac Sim 환경 구축, URDF 로봇 시뮬레이션, ROS2 통합, Synthetic Data Generation",
            "Robot Learning (56H) — 강화학습 기반 로봇 제어, Isaac Lab 활용, Imitation Learning, Sim-to-Real Transfer",
            "LeRobot 실습 (49H) — LeRobot 프레임워크, Diffusion Policy 모델, 로봇 데이터셋 구축 및 학습",
            "Physical AI 배포 (57H) — Jetson 기반 엣지 배포, 실시간 추론 최적화, 로봇 시스템 통합",
        ]),
        M("[프로젝트] 454H (전체의 54%)", "454H", [
            "로보틱스 해커톤 (28H) — 시뮬레이션 기반 로봇 제어 미니 해커톤, 팀 협업 및 피어 리뷰",
            "미니아이펠톤 (35H) — 중간 점검 프로젝트, 멘토 피드백 및 개선",
            "365 챌린지 (391H) — 제조 현장 Physical AI 솔루션 개발, PoC 구현 및 최종 발표",
        ]),
        M("[기타 및 성과 목표]", "21H", [
            "OT 및 수료식 (14H) · 재량교과 현직자 세미나 (7H)",
            "성과 목표 — 취업률 60% · 수료율 90% · 모집률 80% · 훈련생 만족도 4.7/5.0",
            "운영 규모 — 기수당 25명, 연 2기 운영 시 연간 50명 배출",
            "PBL 전 과정 적용 — 참여기업의 실제 데이터·과제 기반 프로젝트 수행",
        ]),
    ],
}

d["tracks"] = [t18, t28, t45, t180, t840]
d["curriculum_title"] = "규모별 레퍼런스 — 상세 커리큘럼"

json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

total = sum(len(m["items"]) for t in d["tracks"] for m in t["modules"])
print("트랙 %d개 · 모듈 %d개 · 세부 항목 %d개"
      % (len(d["tracks"]), sum(len(t["modules"]) for t in d["tracks"]), total))
