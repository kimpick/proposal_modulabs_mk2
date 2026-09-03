import json
import os

filepath = r"C:\Users\Admin\Downloads\ai-education-proposal\projects\전주대학교_AI부트캠프사업\제안서\content.json"

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update metadata
data["subtitle"] = "ND1 피지컬 AI 핵심 기초(60H) + ND2 합성 데이터 구축(60H) + ND5 로보틱스 LLM 에이전트(60H) — 교육과정 제안서"
data["info"]["keyword"] = "피지컬 AI\n합성 데이터셋\n비전 VLM\nLLM 에이전트"
data["info"]["ax_stage"] = "중급(ND1, ND2) → 고급(ND5)"
data["info"]["duration"] = "총 180시간\n(ND1 60H + ND2 60H + ND5 60H)"

data["intro"] = "전주대학교 피지컬 AI 부트캠프는 LLM(두뇌)·로봇(몸)·시뮬레이션(환경)의 3축 통합 역량을 갖춘 인재를 양성하는 과정입니다. 모두의연구소는 이 부트캠프에서 <b>핵심 세 과정</b>을 담당합니다.\n\n<b>ND1. 피지컬 AI 핵심 기초 (중급, 60H)</b> — LLM 임베딩, 로보틱스 수학, ROS2 생태계 심화, 물리 시뮬레이션 활용을 아우르며 피지컬 AI에 필수적인 뼈대를 완성합니다.\n\n<b>ND2. 합성 데이터 및 멀티모달 데이터셋 구축 (중급, 60H)</b> — 실습 인프라 제약을 극복하기 위해 Isaac Sim 환경에서 합성 데이터를 생성하고, 최신 경량 오픈소스(YOLO11, Florence-2)로 실습하며, 하이엔드 AI(GR00T, GPT-4o)의 산업 적용 사례를 분석하여 비전-인지 파이프라인 역량을 배양합니다.\n\n<b>ND5. 로보틱스 LLM 에이전트 구축 (고급, 60H)</b> — 이전 과정에서 다져진 오픈소스 활용 역량을 바탕으로 프롬프트·RAG·VLM·에이전트 플래닝을 단계별로 심화하며, 단대단(End-to-End) 시스템을 완성합니다."

data["objective"] = "<ul><li><b>ND1:</b> 오픈소스 생태계(HuggingFace, ROS2, Isaac/MuJoCo)를 활용하며 피지컬 AI의 하드웨어/소프트웨어 맥락을 통합적으로 체득 (역량 인증 Lv3 목표)</li><li><b>ND2:</b> 고비용 하드웨어 없이 PC 시뮬레이션으로 합성 데이터를 구축하고, 경량 VLM 실습과 하이엔드 AI 사례 분석을 통해 Sim2Real 설계 역량 확보 (역량 인증 Lv3 목표)</li><li><b>ND5:</b> Prompt → VLM → 에이전트 플래닝 → LLM-로봇 통합 순차 심화 → 기업 실무 수준 포트폴리오 완성 (역량 인증 Lv4 목표)</li><li>수료 후 피지컬 AI 분야 기업 채용 연계 — 단기 부트캠프 및 프리뷰 데이 운영</li></ul>"

# Update design logic note to include ND2
if "design_logic" in data and "summary" in data["design_logic"]:
    data["design_logic"]["summary"] = "일반적으로 고급 과정은 중급 이수를 전제로 합니다. 그러나 <b>ND5의 핵심은 LLM 소프트웨어 역량</b>입니다. ND1, ND2가 다루는 로봇 하드웨어 제어나 인지 트랙을 거치지 않더라도, AI 기초에서 LLM 기반 역량을 충분히 확보하면 ND5 직행이 가능하지만, <b>ND1과 ND2를 거치며 시뮬레이션·로봇 통신·시각 인지 원리를 습득한다면 ND5 캡스톤 시스템의 완성도를 극대화</b>할 수 있습니다."

# Update Tech Stack
data["tech_stack"] = [
    "Python · PyTorch",
    "Hugging Face (Transformers)",
    "LangChain / LlamaIndex",
    "Ultralytics (YOLO11/YOLO26)",
    "Open-source VLMs (Florence-2 / Qwen3-VL-3B)",
    "ROS2 (Humble) / LeRobot",
    "NVIDIA Isaac Sim 6.0 / Omniverse",
    "FoundationPose (6D Pose)",
    "MLflow / W&B",
    "Git / GitHub"
]

# Track data update
nd1_track = data["tracks"][0]
# Fix ND1 M13 module
for mod in nd1_track["modules"]:
    if "M13. 물리 시뮬레이션" in mod["module_name"]:
        mod["items"] = [
            "(이론 4H) Isaac Sim 및 MuJoCo 개요, 강체 동역학 및 물리 엔진 구조 이해",
            "(실습 5H) 시뮬레이터 로봇 로드 및 Python API 기반 환경 제어 실습",
            "(캡스톤 6H) LLM 작업 분해 → ROS2 Action 통신 연동 → 환경 내 픽앤플레이스 시나리오 E2E 작동 구현(데모)"
        ]

nd5_track = data["tracks"][1]

nd2_track = {
    "track_id": "ND2",
    "track_name": "ND2. 합성 데이터 및 멀티모달 데이터셋 구축 — 중급 (60H)",
    "course_title": "현실 공간의 한계를 넘는 데이터 연금술 : 시뮬레이션과 경량 VLM 오픈소스 실습",
    "target": "AI 기초 전 과정 수료 및 파이썬 활용 능숙자 (ND1 이수 적극 권장)",
    "duration": "60시간 (하계 2026년 집중이수, 주 5일 몰입형)",
    "tools": [
        "Isaac Sim 6.0",
        "YOLO11",
        "Florence-2 / Qwen3-VL",
        "FoundationPose (사례)"
    ],
    "modules": [
        {
            "module_name": "M14. Isaac Sim / Omniverse 입문",
            "duration": "15H",
            "items": [
                "(사례&이론 4H) 시뮬레이터 구조(USD) 및 산업계 하이엔드 적용 사례(NVIDIA GR00T, Cosmos) 분석 기법",
                "(실습 6H) 교육용 PC에 적합한 Isaac Sim 환경 세팅 및 로봇, 센서(RGB-D) 부착 오프라인 제어 실습",
                "(실습 5H) Replicator API를 활용한 도메인 랜덤화(조명, 카메라, 위치 무작위화) 파이프라인 실습"
            ]
        },
        {
            "module_name": "M16. 합성데이터·라벨링 파이프라인 구축",
            "duration": "15H",
            "items": [
                "(이론 3H) Synthetic Data Generation(SDG) 퀄리티 검증(PGR 지표 등) 및 도메인 갭 발생 이유와 Sim2Real 브리핑",
                "(실습 6H) Isaac Sim 기반 바운딩박스(2D) 및 뎁스/시맨틱 자동 라벨링 추출 실습 (YOLO 포맷 전환)",
                "(실습 6H) 대량의 합성 데이터 셋 자동 생성 파이프라인 E2E 완성 및 추출한 데이터셋 통계 분석"
            ]
        },
        {
            "module_name": "M9. 로봇 비전·인지: 탐지·추적·포즈",
            "duration": "15H",
            "items": [
                "(사례&이론 3H) 6D Pose 최신 하이엔드 트렌드(NVIDIA FoundationPose 등) 분석 및 2D/3D 객체 인지 수학적 원리",
                "(실습 6H) 실습용 경량 최신 모델(Ultralytics YOLO11)을 활용한 합성 데이터 객체 탐지 파인튜닝 실습",
                "(실습 6H) 실 데이터(소량) vs 합성 데이터 혼합 학습 및 성능 지표(mAP) 산출·비교 리포트 작성 실습"
            ]
        },
        {
            "module_name": "M4. 멀티모달 LLM(VLM) 심화",
            "duration": "15H",
            "items": [
                "(사례&이론 3H) 대형 하이엔드 VLM(GPT-4o, LLaMA-3.2-Vision)의 공정 자동화, 불량 검출 등 산업계 적용 사례 심층 브리핑",
                "(실습 6H) 인프라 제약 없이 콜랩/데스크탑도 구동되는 교육용 경량 VLM (Florence-2, Qwen-VL-3B) 로컬 실습",
                "(캡스톤 6H) 합성 이미지 내 다중 객체에 대한 VLM VQA 및 자연어 기반 객체 Grounding 융합 캡스톤 구현"
            ]
        }
    ]
}

data["tracks"] = [nd1_track, nd2_track, nd5_track]

# Output
data["output"] = "<ul><li><b>[ND1 M8/M13 산출물]</b> LLM-ROS2 연동을 통한 에이전트 기반 시뮬레이션 제어 데모 영상</li><li><b>[ND2 산출물]</b> Isaac Sim 도메인 랜덤화 기반 합성 데이터셋 생성 스크립트 및 YOLO11 학습 결과 로그 (PGR 지표 산출)</li><li><b>[ND2 VLM 캡스톤]</b> 교육용 경량 VLM(Florence-2/YOLO11)을 활용한 시뮬레이션 합성 화면 속 객체 Grounding 파이프라인 구축</li><li><b>[ND5 M12 캡스톤]</b> LLM 기반 로봇 제어 단대단(E2E) 시스템 — Git/README + 실행 스크립트 + 데모 영상 (역량 인증 Lv4)</li></ul>"

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("content.json updated successfully!")
