import json
import copy
import os

MASTER_JSON = os.path.join(os.path.dirname(__file__), "제안서", "content.json")

def generate():
    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    base_dir = os.path.dirname(__file__)

    def save_proposal(folder_name, data):
        output_dir = os.path.join(base_dir, folder_name)
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "content.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Generated {folder_name}/content.json")

    # 1. Comprehensive (종합 제안서)
    # 기획안: 종합 제안서에서는 세부 커리큘럼 표(tracks)를 숨기고 3개의 핵심 플로우 모두 노출.
    comp_data = copy.deepcopy(master_data)
    comp_data["tracks"] = [] 
    comp_data.pop("time_allocation", None)
    comp_data.pop("design_logic", None)
    save_proposal("제안서_종합", comp_data)

    # 2. ND1 단독 제안서
    nd1_data = copy.deepcopy(master_data)
    nd1_data["tracks"] = [t for t in nd1_data.get("tracks", []) if t.get("track_id") == "ND1"]
    nd1_data.pop("nd2_flow", None)
    nd1_data.pop("nd5_flow", None)
    nd1_data.pop("design_logic", None)
    nd1_data.pop("time_allocation", None)
    nd1_data["title"] = "모두의연구소 × 전주대학교 AI 부트캠프 [ND1 단독]"
    nd1_data["subtitle"] = "ND1 피지컬 AI 핵심 기초(60H) — 입문/초급을 위한 로보틱스 기초 완벽 가이드"
    nd1_data["info"] = {
        "keyword": "ROS2\n로봇 기구학\n물리 시뮬레이션\n파인튜닝",
        "ax_stage": "입문/초급",
        "target": "입문자/비전공자",
        "duration": "총 60시간"
    }
    nd1_data["intro"] = "본 제안서는 전주대학교 피지컬 AI 부트캠프 중 <b>[ND1] 피지컬 AI 핵심 기초</b> 트랙을 위한 단독 커리큘럼입니다. 가상과 현실을 잇는 피지컬 AI의 기초 언어(ROS2)와 물리 법칙, 파운데이션 모델의 뼈대를 세우며, LLM부터 시뮬레이션 환경 제어까지 단대단(End-to-End) 구동을 목표로 합니다."
    nd1_data["objective"] = "<ul><li>오픈소스 생태계(HuggingFace, ROS2, Isaac/MuJoCo)를 활용하며 피지컬 AI의 하드웨어/소프트웨어 맥락을 통합적으로 체득</li><li>LLM 기초부터 로봇 물리 제어, 시뮬레이션 환경 구축까지 단계적 습득</li></ul>"
    save_proposal("제안서_ND1", nd1_data)

    # 3. ND2 단독 제안서
    nd2_data = copy.deepcopy(master_data)
    nd2_data["tracks"] = [t for t in nd2_data.get("tracks", []) if t.get("track_id") == "ND2"]
    nd2_data.pop("nd1_flow", None)
    nd2_data.pop("nd5_flow", None)
    nd2_data.pop("design_logic", None)
    nd2_data.pop("time_allocation", None)
    nd2_data["title"] = "모두의연구소 × 전주대학교 AI 부트캠프 [ND2 단독]"
    nd2_data["subtitle"] = "ND2 합성 데이터 및 멀티모달 데이터셋 구축(60H) — 소프트웨어 지향 데이터 파이프라인"
    nd2_data["info"] = {
        "keyword": "합성 데이터(SDG)\nYOLO11\nVLM 공간지능\nIsaac Sim",
        "ax_stage": "중급",
        "target": "데이터/컴퓨터비전 지향 학습자",
        "duration": "총 60시간"
    }
    nd2_data["intro"] = "본 제안서는 <b>[ND2] 합성 데이터 및 멀티모달 데이터셋 구축</b> 트랙 단독 커리큘럼입니다. 로봇 하드웨어 없이 PC 환경에서 고품질 데이터 파이프라인(SDG)과 시각 인식(VLM, 객체 탐지) 역량을 쌓으며 데이터 연금술 파이프라인을 완성합니다."
    nd2_data["objective"] = "<ul><li>고비용 하드웨어 없이 PC 시뮬레이션으로 합성 데이터를 구축하고 파이프라인화</li><li>경량 VLM 실습과 하이엔드 AI 사례 분석을 통해 Sim2Real 설계 역량 확보</li></ul>"
    save_proposal("제안서_ND2", nd2_data)

    # 4. ND5 단독 제안서
    nd5_data = copy.deepcopy(master_data)
    nd5_data["tracks"] = [t for t in nd5_data.get("tracks", []) if t.get("track_id") == "ND5"]
    nd5_data.pop("nd1_flow", None)
    nd5_data.pop("nd2_flow", None)
    nd5_data.pop("design_logic", None)
    nd5_data.pop("time_allocation", None)
    nd5_data["title"] = "모두의연구소 × 전주대학교 AI 부트캠프 [ND5 단독]"
    nd5_data["subtitle"] = "ND5 로보틱스 LLM 에이전트 구축(60H) — 하이엔드 아키텍처"
    nd5_data["info"] = {
        "keyword": "LLM Agent\nLangGraph\nRAG\nVLM",
        "ax_stage": "고급",
        "target": "AI 기초/LLM 활용 유경험자",
        "duration": "총 60시간"
    }
    nd5_data["intro"] = "본 제안서는 <b>[ND5] 로보틱스 LLM 에이전트 구축</b> 트랙 단독 커리큘럼입니다. 인지된 환경을 바탕으로 LLM 에이전트가 다단계 계획을 수립(Planning)하고, 행동(Action)으로 번역하여 로봇을 제어하는 고수익 하이엔드 역량을 완성합니다."
    nd5_data["objective"] = "<ul><li>Prompt → VLM → 에이전트 플래닝 → LLM-로봇 통합 순차 심화</li><li>기업 실무 수준 포트폴리오(다단계 작업 계획 에이전트 E2E 시스템) 완성</li></ul>"
    save_proposal("제안서_ND5", nd5_data)

    print("Success: Generated content.json for 4 proposal versions.")

    print("\nStarting HTML/PDF generation for all versions...")
    import subprocess
    import sys
    
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
    build_script = os.path.join(project_root, "build.py")

    target_folders = ["제안서_종합", "제안서_ND1", "제안서_ND2", "제안서_ND5"]
    for folder in target_folders:
        print(f"\n--- Building {folder} ---")
        cmd = [sys.executable, build_script, f"전주대학교_AI부트캠프사업/{folder}"]
        subprocess.run(cmd, cwd=project_root)

    print("\n✅ All JSON extraction and PDF generation finished.")

if __name__ == '__main__':
    generate()
