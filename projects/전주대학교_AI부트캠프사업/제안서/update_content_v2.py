import json

filepath = r"C:\Users\Admin\Downloads\ai-education-proposal\projects\전주대학교_AI부트캠프사업\제안서\content.json"

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update metadata and intro
data["intro"] = "전주대학교 피지컬 AI 부트캠프는 LLM(두뇌)·로봇(몸)·시뮬레이션(환경)의 3축 통합 역량을 갖춘 인재를 양성하는 과정입니다. 모두의연구소는 이 부트캠프에서 <b>핵심 세 과정</b>을 담당합니다.\n\n<b>ND1. 피지컬 AI 핵심 기초 (중급, 60H)</b> — 가상과 현실을 잇는 피지컬 AI의 기초 언어(ROS2)와 물리 법칙, 파운데이션 모델의 뼈대를 세웁니다.\n\n<b>ND2. 합성 데이터 및 멀티모달 데이터셋 구축 (중급, 60H)</b> — 고비용 하드웨어 제약을 시뮬레이션 합성 데이터(SDG)로 돌파하고, VLM을 통해 로봇의 '시각 인지(Vision)' 역량을 확보합니다.\n\n<b>ND5. 로보틱스 LLM 에이전트 구축 (고급, 60H)</b> — 인지된 환경을 바탕으로 LLM 에이전트가 다단계 계획을 수립(Planning)하고, 행동(Action)으로 번역하여 로봇을 제어하는 두뇌를 완성합니다."

data["tech_stack"] = [
    "Python · PyTorch",
    "Hugging Face (Transformers)",
    "LangChain / LlamaIndex / LangGraph",
    "Ultralytics (YOLO11)",
    "Open-source VLMs (Florence-2 / Qwen3-VL-3B)",
    "ROS2 (Humble)",
    "NVIDIA Isaac Sim 6.0 / MuJoCo",
    "FoundationPose (6D Pose) / OpenVLA",
    "MLflow / W&B",
    "Git / GitHub"
]

data["schedule_message"] = "동계(겨울학기) 집중이수 기간을 활용하여, **1월에 ND1(기초)과 ND2(데이터/인지)를 순차적으로 연달아 진행**하여 데이터를 제어할 로봇/인지 체력을 집중적으로 다지고, 여기서 도출된 역량을 바탕으로 **2월에 ND5(에이전트 두뇌/행동 통합)**를 이어가는 몰입형 연속 스케줄을 제안합니다. 이를 통해 몰입형 캠프의 교육 연속성과 최종 캡스톤 시스템 완성도를 극대화할 수 있습니다."

# Redefine tracks completely to apply the new table format and Theory->Practice logic
nd1_modules = [
    {
        "module_name": "M1. LLM 파운데이션 & 임베딩",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "언어 모델과 Transformer 논리 구조 심화 및 초거대 AI(GPT-4o, Claude 3.5) 진화 사례 분석", "hours": "5H"},
            {"method": "실습/심화", "detail": "NVIDIA GPU 환경 기반 경량 SLM(Llama-3 8B, Qwen 1.5B) 로컬 파인튜닝 및 추론 실습", "hours": "6H"},
            {"method": "캡스톤", "detail": "HuggingFace 생태계를 활용한 나만의 커스텀 파라미터 언어 모델 구축 미니 캡스톤", "hours": "4H"}
        ]
    },
    {
        "module_name": "M7. 로봇공학 이론 및 피지컬 인지",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "로봇 기구학 기본 원리 및 Tesla Optimus, Boston Dynamics 등 휴머노이드 모션 제어 사례 프레젠테이션", "hours": "4H"},
            {"method": "실습/심화", "detail": "Numpy 라이브러리를 활용한 6DoF 산업용 매니퓰레이터(UR) 순기구학 계산 및 공간 좌표 가시화 실습", "hours": "6H"},
            {"method": "실습/심화", "detail": "카메라/LiDAR 센서 데이터 기초 처리 및 Pinhole 캘리브레이션 튜토리얼 코딩", "hours": "5H"}
        ]
    },
    {
        "module_name": "M8. ROS2 생태계 및 로봇 통신 심화",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "ROS2 아키텍처 및 DDS 개념, 실제 공장/물류 현장의 다수종 AMR(자율주행로봇) 통합 통신망 구축 방안 사례 탐구", "hours": "5H"},
            {"method": "실습/심화", "detail": "비싼 하드웨어를 대체할 Turtlesim, Turtlebot3 가상 노드를 활용한 실전 Python Topic/Action 통신망 구축 실습", "hours": "6H"},
            {"method": "실습/심화", "detail": "URDF 모델 구조 분석 및 TF2 라이브러리를 이용한 조인트 간 동적 좌표 변환 응용 노드 구현", "hours": "4H"}
        ]
    },
    {
        "module_name": "M13. 물리 시뮬레이션 및 에이전트 기반 연동",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "강체 동역학 및 물리 엔진(MuJoCo) 기초 구조 설계와 OpenAI, DeepMind의 대규모 병렬 강화학습 시뮬레이터 구축 사례", "hours": "5H"},
            {"method": "실습/심화", "detail": "단일 머신 환경에서의 MuJoCo/Isaac Sim 구동, 파이썬 API 기반 시뮬레이터 로봇 스폰 및 기초 토크 제어 실습", "hours": "5H"},
            {"method": "캡스톤", "detail": "과정 융합: ROS2 Action 통신 레이어 연동을 통한 파이썬 스크립트 기반 시뮬레이션 환경 내 Pick & Place 단대단 구현", "hours": "5H"}
        ]
    }
]

nd2_modules = [
    {
        "module_name": "M14. Isaac Sim / Omniverse 입문",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "디지털 트윈 기반 시뮬레이터 구조(USD) 철학 및 산업계 하이엔드 최상위 적용 사례 (NVIDIA 'GR00T', 'Cosmos') 모델 입체 분석", "hours": "5H"},
            {"method": "실습/심화", "detail": "교육용 PC 사양에서도 유연하게 구동되는 Isaac Sim 환경 구축 완료 및 무인 이동체, 매니퓰레이터 로드 실습", "hours": "5H"},
            {"method": "실습/심화", "detail": "Replicator 파이프라인 API 코딩을 통한 필수 도메인 랜덤화 (빛 변화, 재질 무작위성, 카메라 노이즈) 구성 실습", "hours": "5H"}
        ]
    },
    {
        "module_name": "M16. 합성데이터·라벨링 파이프라인 구축",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "Sim2Real 시의 픽셀/피처 도메인 갭 발생 원인 심층 분석 및 합성 데이터 유효성 측정 지표 (PGR; Performance Gap Recovered)", "hours": "4H"},
            {"method": "실습/심화", "detail": "Isaac Sim 프레임워크를 이용한 장면 내 객체 바운딩 박스(2D) 및 픽셀 단위 시맨틱 세그멘테이션 마스크 자동 대량 추출 실습", "hours": "6H"},
            {"method": "실습/심화", "detail": "대량으로 렌더링된 메타데이터를 Ultralytics YOLO 학습 전용 포맷으로 데이터셋화하는 파이프라인 스크립트 작성 및 통계 분석", "hours": "5H"}
        ]
    },
    {
        "module_name": "M9. 로봇 비전 인지: 탐지·추적·포즈",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "로봇 공학 내 2D/3D 컴퓨터 비전 인지 수학적 기초 및 최신 제로샷 6D Pose 하이엔드 모델(NVIDIA FoundationPose) 트렌드 브리핑", "hours": "4H"},
            {"method": "실습/심화", "detail": "초경량·고성능 API로 실습 편의성이 극대화된 오픈소스 최상위 프레임워크(YOLO11)를 활용한 합성 데이터 전용 객체 탐지 파인튜닝", "hours": "6H"},
            {"method": "캡스톤", "detail": "실 장비 테스트 데이터(소량) vs 시뮬레이션 라벨링 합성 데이터(대량) 혼합 학습 검증 및 탐지 성능 지표(mAP) 산출 미니 리뷰", "hours": "5H"}
        ]
    },
    {
        "module_name": "M4. 멀티모달 LLM (VLM) 심화",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "초거대 상용 VLM (GPT-4o, LLaMA-3.2-Vision 등)의 공정 자동화 시각 검수 및 산업 불량 검출 등 하이엔드 현장 적용 사례 보고", "hours": "4H"},
            {"method": "실습/심화", "detail": "학교 인프라 제약 없이 Google Colab 및 기본 PC에서도 가볍게 구동되는 오픈소스 교육용 VLM (Florence-2, Qwen-VL-3B 등) 설치 및 추론", "hours": "6H"},
            {"method": "캡스톤", "detail": "시뮬레이션으로 방금 찍어낸 합성 이미지 내부의 다중 객체에 대하여, VLM 기반 질의응답(VQA) 및 모델 자체 자연어 기반 객체 Grounding 종합", "hours": "5H"}
        ]
    }
]

nd5_modules = [
    {
        "module_name": "M2. 프롬프트 엔지니어링 & RAG 심화",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "프롬프트 체인 구조 고도화 전략 및 Perplexity 류의 거대 엔터프라이즈 Search 기반 RAG 파이프라인 구성 사례 분석", "hours": "4H"},
            {"method": "실습/심화", "detail": "로봇 제조사 PDF 매뉴얼, ROS2 공식 도큐먼트 등 방대한 특화 문서를 쪼개고 색인(ChromaDB)하는 단대단 RAG 정보 시스템 구축", "hours": "6H"},
            {"method": "실습/심화", "detail": "환각 현상(Hallucination) 억제를 위한 방어막(Guardrail) 설계 및 RAGAS 정량 지표 기반 응답 신뢰성/정확도 개선 비교 실험", "hours": "5H"}
        ]
    },
    {
        "module_name": "M4. VLA (Vision-Language-Action) 및 공간 지능의 이해",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "단순 시각 이해(VLM)를 넘어 입력-시각-행동을 종단간 직결하는 구글 RT-2, Figure 01과 같은 'VLA' 파운데이션 최상위 동향 분석", "hours": "4H"},
            {"method": "실습/심화", "detail": "OpenVLA와 같은 대표 오픈소스 행동 액션 모델의 레이어 구조 탐구 및, 로봇의 3D 공간 제어 좌표계 반환 메커니즘 해석", "hours": "5H"},
            {"method": "실습/심화", "detail": "사물 관계(위/아래/옆) 추론 및 지시어(\"빨간 큐브를 파란 접시로 옮겨\")에 숨겨진 공간 지능(Spatial Intelligence) 분해 및 프롬프트 파싱", "hours": "6H"}
        ]
    },
    {
        "module_name": "M6. 에이전트 플래닝 및 정렬",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "전통적 ReAct 구조의 한계 분석과 Devin, AutoGPT 주도 다수 전문 노드들이 협동하는 계층적 멀티 에이전트 트렌드 파악", "hours": "4H"},
            {"method": "실습/심화", "detail": "LangGraph 프레임워크를 기반으로 상태(State)를 가지는 다단계 워크플로우 제어망(Multi-step Task Planning) 에이전트 구축", "hours": "6H"},
            {"method": "실습/심화", "detail": "사용 가능한 도구 풀(액션 공간) 정의 실습 및 MLflow 프레임워크 연동을 통한 에이전트 사고 추적(Tracing) 및 플래닝 성능 검증", "hours": "5H"}
        ]
    },
    {
        "module_name": "M12. 로봇 시스템 E2E 통합 캡스톤",
        "duration": "15H",
        "items": [
            {"method": "이론/사례", "detail": "사용자 인텐트 해석(Task Layer) ➔ 단위 모듈 선택(Skill Layer) ➔ 로봇 기구학 동작(Action Layer) 3원화 시스템 상용 아키텍처 사례", "hours": "4H"},
            {"method": "실습/심화", "detail": "HuggingFace LeRobot 플랫폼 연계 통신 및, LLM 에이전트의 사고 결과를 ROS2 Action 서버의 목표 좌표로 변환하는 브릿지 레이어 구축", "hours": "5H"},
            {"method": "캡스톤", "detail": "과정 최종 정리: 가상 시뮬레이터 환경 안에서 사용자의 자연어 지시만으로 '인지 ➔ 플래닝 ➔ 로봇 움직임 ➔ 자체 검증'이 이루어지는 데모 시연", "hours": "6H"}
        ]
    }
]

data["tracks"][0]["modules"] = nd1_modules
data["tracks"][1]["modules"] = nd2_modules
data["tracks"][2]["modules"] = nd5_modules

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("content.json successfully updated with table-ready structure and Theory/Practice overhaul.")
