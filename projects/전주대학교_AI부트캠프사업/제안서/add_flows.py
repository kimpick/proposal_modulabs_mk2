"""Add nd1_flow and nd2_flow to content.json (same structure as nd5_flow)"""
import json

filepath = r"C:\Users\Admin\Downloads\ai-education-proposal\projects\전주대학교_AI부트캠프사업\제안서\content.json"

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ── ND1 Flow ──
data["nd1_flow"] = {
    "title": "ND1 내부 학습 흐름 — 단계별 심화 구조",
    "subtitle": "주 5일 몰입형 집중과정 · 15H 모듈 심화",
    "total": "총 60H · 절대평가",
    "steps": [
        {
            "step": "STEP 1",
            "module": "M1.",
            "name": "LLM 파운데이션 & 임베딩",
            "hours": "15H",
            "items": [
                "Transformer 아키텍처 이론 및 초거대 AI 사례 분석",
                "경량 SLM(Llama-3 8B, Qwen 1.5B) 로컬 파인튜닝",
                "HuggingFace 생태계 활용 커스텀 모델 구축",
                "임베딩 기반 유사도 연산 실습"
            ],
            "output": "결과물: 커스텀 경량 언어 모델 로컬 구동"
        },
        {
            "step": "STEP 2",
            "module": "M7.",
            "name": "로봇공학 이론 및 피지컬 인지",
            "hours": "15H",
            "items": [
                "로봇 기구학 원리 및 휴머노이드 사례 분석",
                "Numpy 기반 6DoF 순기구학 계산·가시화",
                "카메라/LiDAR 센서 데이터 기초 처리",
                "Pinhole 캘리브레이션 파이썬 코딩"
            ],
            "output": "결과물: 파이썬 기반 로봇 좌표 연산 코드"
        },
        {
            "step": "STEP 3",
            "module": "M8.",
            "name": "ROS2 생태계 및 로봇 통신 심화",
            "hours": "15H",
            "items": [
                "ROS2 DDS 아키텍처 및 AMR 통신 사례",
                "Python Topic / Action 통신망 실전 구축",
                "URDF 모델 분석 · TF2 좌표 변환 구현",
                "가상 로봇 노드 커맨드 통신 실습"
            ],
            "output": "결과물: ROS2 Python 통신망 구동 데모"
        },
        {
            "step": "STEP 4",
            "module": "M13.",
            "name": "물리 시뮬레이션 및 에이전트 연동",
            "hours": "15H",
            "items": [
                "물리 엔진(MuJoCo) 구조 및 강화학습 사례",
                "파이썬 API 기반 시뮬레이터 로봇 스폰·제어",
                "ROS2 Action 통신 연동 구현",
                "시뮬레이션 내 Pick & Place E2E 캡스톤"
            ],
            "output": "결과물: 시뮬레이션 Pick & Place 데모 영상",
            "is_capstone": True
        }
    ],
    "flow_labels": [
        "M1. LLM 두뇌 기초",
        "M7. 로봇 기구학",
        "M8. ROS2 통신",
        "M13. 시뮬레이션 E2E"
    ]
}

# ── ND2 Flow ──
data["nd2_flow"] = {
    "title": "ND2 내부 학습 흐름 — 단계별 심화 구조",
    "subtitle": "주 5일 몰입형 집중과정 · 15H 모듈 심화",
    "total": "총 60H · 절대평가",
    "steps": [
        {
            "step": "STEP 1",
            "module": "M14.",
            "name": "Isaac Sim / Omniverse 입문",
            "hours": "15H",
            "items": [
                "디지털 트윈·USD 철학 및 GR00T/Cosmos 사례",
                "교육용 PC에서 Isaac Sim 환경 구축",
                "Replicator 도메인 랜덤화 API 실습",
                "시뮬레이터 로봇/객체 배치 실전"
            ],
            "output": "결과물: Isaac Sim 도메인 랜덤화 환경"
        },
        {
            "step": "STEP 2",
            "module": "M16.",
            "name": "합성 데이터·라벨링 파이프라인",
            "hours": "15H",
            "items": [
                "Sim2Real 도메인 갭 분석 및 PGR 지표 이론",
                "바운딩 박스·시맨틱 마스크 자동 대량 추출",
                "YOLO 학습 포맷 변환 파이프라인 스크립트",
                "합성 데이터 유효성 통계 분석"
            ],
            "output": "결과물: 합성 데이터 생성·라벨링 파이프라인"
        },
        {
            "step": "STEP 3",
            "module": "M9.",
            "name": "로봇 비전 인지: 탐지·추적·포즈",
            "hours": "15H",
            "items": [
                "2D/3D 컴퓨터 비전 기초 및 FoundationPose 사례",
                "YOLO11 합성 데이터 전용 파인튜닝 실습",
                "실 데이터 vs 합성 데이터 혼합 학습 검증",
                "탐지 성능 정량 지표(mAP) 산출"
            ],
            "output": "결과물: 합성+실 데이터 혼합 mAP 리포트"
        },
        {
            "step": "STEP 4",
            "module": "M4.",
            "name": "멀티모달 LLM (VLM) 심화",
            "hours": "15H",
            "items": [
                "산업용 VLM(GPT-4o, LLaMA-Vision) 적용 사례",
                "경량 VLM(Florence-2, Qwen-VL) 설치·추론",
                "합성 이미지 VQA 질의응답 파이프라인",
                "VLM 기반 객체 Grounding 종합 캡스톤"
            ],
            "output": "결과물: VLM 기반 합성 이미지 Grounding 데모",
            "is_capstone": True
        }
    ],
    "flow_labels": [
        "M14. 시뮬레이터 구축",
        "M16. 합성 데이터 생성",
        "M9. 비전 모델 튜닝",
        "M4. VLM 접목·캡스톤"
    ]
}

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ nd1_flow + nd2_flow added to content.json successfully.")
