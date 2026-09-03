# -*- coding: utf-8 -*-
"""제안서 → 16:9 가로 발표 덱 빌더.

템플릿의 font-size 만 일괄 확대(배율 SCALE)하고, 프레임(1280x720)·여백은 건드리지 않는다.
"""
import re
import os

TPL = "/root/.claude/skills/proposal-deck-landscape/assets/deck-template.html"
OUT = "/home/user/propsal_modulabs/projects"
SCALE = 1.35  # 폰트 확대 배율 (720px 프레임 안에서 자동 축소가 걸리지 않는 상한)

raw = open(TPL, encoding="utf-8").read()

# ── 1) <style> 블록 안의 font-size 값만 배율 적용 ──
style_start = raw.index("<style>")
style_end = raw.index("</style>")
style = raw[style_start:style_end]


def bump(m):
    val = float(m.group(1))
    return "font-size:%gpx" % round(val * SCALE, 1)


style_big = re.sub(r"font-size:([\d.]+)px", bump, style)
raw = raw[:style_start] + style_big + raw[style_end:]

# 큰 글자에 맞춰 본문 여백을 살짝 줄여 세로 공간을 확보한다.
raw = raw.replace(".fit-content{padding:46px 64px;", ".fit-content{padding:54px 72px;")

# ── 2) 예시 슬라이드 3개 제거 (주석 블록 이후 ~ </div></div> 앞까지) ──
raw = re.sub(r"\n    <!-- =+\n         슬라이드 작성 규칙.*?=+ -->\n", "\n", raw, flags=re.S)
head, _, tail = raw.partition("    <!-- ===== 예시 1: 표지 ===== -->")
_, _, tail = tail.partition("  </div>\n</div>\n\n<script>")
SHELL_HEAD = head
SHELL_TAIL = "  </div>\n</div>\n\n<script>" + tail


def write_deck(path, title, slides):
    html = SHELL_HEAD + "\n".join(slides) + "\n\n" + SHELL_TAIL
    html = html.replace("{{DECK_TITLE}}", title)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    print("wrote", path, len(html), "bytes")


def slide(body, cls="", center=False):
    frame = "fit-frame center" if center else "fit-frame"
    return (
        '    <section class="slide %s">\n      <div class="%s">\n        <div class="fit-content">\n'
        % (cls, frame)
        + body
        + "\n        </div>\n      </div>\n    </section>\n"
    )


def hdr(num, kicker, h2, lead=None):
    s = '          <span class="sec-num">%s</span>\n' % num
    s += '          <p class="kicker">%s</p>\n' % kicker
    s += "          <h2>%s</h2>\n" % h2
    if lead:
        s += '          <p class="lead">%s</p>\n' % lead
    return s


# ══════════════════════════════════════════════════════════════
# DECK A — Physical AI 교육 레퍼런스
# ══════════════════════════════════════════════════════════════
A = []

A.append(slide(
    '          <span class="cover-badge">🔴 모두의연구소 &nbsp;·&nbsp; Physical AI 교육</span>\n'
    '          <h1>Physical AI 교육<br><span>레퍼런스</span></h1>\n'
    '          <p class="sub">18시간 특강부터 840시간 전문가 양성까지 — 규모별 수행·설계 실적</p>\n'
    '          <div class="cover-meta">\n'
    '            <span><b>작성</b> · 모두의연구소 비즈팀</span>\n'
    '            <span><b>일자</b> · 2026. 08.</span>\n'
    '            <span><b>범위</b> · 5개 규모 레퍼런스</span>\n'
    '          </div>', cls="cover", center=True))

A.append(slide(
    hdr("01 / 배경", "왜 지금인가",
        "LLM이 두뇌, 로봇이 몸, 시뮬레이션이 세계",
        "Physical AI는 세 축이 맞물려 돌아가는 융합 기술입니다. 2026년 현재 VLA 파운데이션 모델 경쟁이 본격화되며 연구 단계를 넘어 제조·물류·모빌리티 현장에 진입하고 있습니다.")
    + '          <div class="grid g3">\n'
    '            <div class="task"><div class="ti">🧠</div><div class="tt">Brain — LLM</div>'
    '<div class="td">상황을 이해하고 무엇을 할지 계획한다</div></div>\n'
    '            <div class="task"><div class="ti">🦾</div><div class="tt">Body — 로봇</div>'
    '<div class="td">계획을 실제 움직임으로 실행한다</div></div>\n'
    '            <div class="task"><div class="ti">🌐</div><div class="tt">World — 시뮬레이션</div>'
    '<div class="td">안전하게 학습하고 검증한다</div></div>\n'
    '          </div>\n'
    '          <div class="quote" style="margin-top:18px">\n'
    '            <div class="q">교육의 관건은 이 세 축을 어떤 순서로, 어느 깊이까지 다루느냐입니다.</div>\n'
    '            <div class="by">모두의연구소는 이 순서를 실제 운영으로 검증했습니다.</div>\n'
    '          </div>'))

A.append(slide(
    hdr("02 / 계보", "커리큘럼 계보",
        "다섯 개를 따로 만든 게 아니라, 검증된 하나를 재단했습니다",
        "2025년 11~12월 재직자 28시간 과정을 직접 운영하며 커리큘럼·교재·실습 환경을 실전 검증했고, 이를 기반으로 규모별로 확장해 왔습니다.")
    + '          <div class="case">\n'
    '            <div class="ctop"><div class="co">출발점 · 재직자 28H 대면 과정</div>'
    '<div class="cat">운영 완료 · 2025.11~12</div></div>\n'
    '            <div class="desc">커리큘럼 · 교재 · 실습 환경을 실전 검증한 유일한 기준점</div>\n'
    '          </div>\n'
    '          <div class="grid g4" style="margin-top:16px">\n'
    '            <div class="task"><div class="tt">온라인화</div><div class="td">대학원생 18H 비대면 특강</div></div>\n'
    '            <div class="task"><div class="tt">정규 교과화</div><div class="td">대학 피지컬AI실습 초급 45H + 중급 45H</div></div>\n'
    '            <div class="task"><div class="tt">장기 양성화</div><div class="td">국책 나노디그리 60H × 3과목</div></div>\n'
    '            <div class="task"><div class="tt">전문가 양성</div><div class="td">제조 혁신 전문가 840H / 6개월</div></div>\n'
    '          </div>'))

A.append(slide(
    hdr("03 / 실적", "한눈에 보는 성과",
        "28시간 재직자 과정 — 운영 완료 성과",
        "목표 대비 두 배의 수료 인원, 그리고 강사·과정 구성 전 항목에서 4.5점대를 기록했습니다.")
    + '          <div class="grid g4">\n'
    '            <div class="kpi"><div class="n">40<small>명</small></div><div class="l">수료 인원<br>(목표 20명)</div></div>\n'
    '            <div class="kpi"><div class="n">200<small>%</small></div><div class="l">목표 달성률</div></div>\n'
    '            <div class="kpi"><div class="n">4.46<small>/5</small></div><div class="l">전반 만족도<br>강사 4.55 · 구성 4.51</div></div>\n'
    '            <div class="kpi"><div class="n">+0.88</div><div class="l">자가평가 역량 상승<br>3.14 → 4.02</div></div>\n'
    '          </div>\n'
    '          <div class="chips" style="margin-top:20px">\n'
    '            <span class="chip big">대기업 · 연구기관 현업 엔지니어 다수 참여</span>\n'
    '            <span class="chip">전 4회차 운영 완료</span>\n'
    '            <span class="chip">추천 의향 4.49</span>\n'
    '          </div>\n'
    '          <p class="note">출처 · 2025.12 과정 결과보고서 (만족도 조사 및 출석부 기준)</p>'))

A.append(slide(
    hdr("04 / 레퍼런스", "규모별 총괄",
        "18시간부터 840시간까지, 다섯 개의 규모",
        "고객의 목표와 예산에 맞춰 아래 다섯 가지 중에서 출발점을 고를 수 있습니다.")
    + '          <table class="prop">\n'
    '            <thead><tr><th>규모</th><th>과정</th><th>대상</th><th class="c">시간</th><th class="c">상태</th></tr></thead>\n'
    '            <tbody>\n'
    '              <tr><td class="trk">특강형</td><td class="course">Physical AI 온라인 집중 특강</td>'
    '<td class="tgt">대학원생 · 비대면</td><td class="hrs">18H<br>(3일)</td>'
    '<td class="c"><span class="badge badge-green">운영</span></td></tr>\n'
    '              <tr><td class="trk">단기 집중</td><td class="course">디지털 트윈으로 만나는 Physical AI</td>'
    '<td class="tgt">재직자 · 실무자</td><td class="hrs">28H<br>(7H×4회)</td>'
    '<td class="c"><span class="badge badge-red">운영 완료 · 검증</span></td></tr>\n'
    '              <tr><td class="trk">정규 교과</td><td class="course">피지컬AI실습 초급 / 중급</td>'
    '<td class="tgt">대학 정규 교과</td><td class="hrs">45H×2<br>(최대 225H)</td>'
    '<td class="c"><span class="badge badge-blue">설계·제안</span></td></tr>\n'
    '              <tr><td class="trk">나노디그리</td><td class="course">Physical AI 나노디그리 3종</td>'
    '<td class="tgt">부트캠프 수강생</td><td class="hrs">60H×3<br>(180H)</td>'
    '<td class="c"><span class="badge badge-blue">설계·제안</span></td></tr>\n'
    '              <tr><td class="trk">전문가</td><td class="course">제조 혁신 Physical AI 전문가 과정</td>'
    '<td class="tgt">제조·로봇 취업 목표</td><td class="hrs">840H<br>(6개월)</td>'
    '<td class="c"><span class="badge badge-blue">설계·제안</span></td></tr>\n'
    '            </tbody>\n'
    '          </table>\n'
    '          <p class="note">상태 · [운영] 실제 진행한 과정 / [설계·제안] 커리큘럼 설계를 완료한 과정</p>'))

def refcol(head, rows):
    """rows: [(제목, 부연)] — 부연은 None 가능"""
    s = '            <div class="refcol">\n'
    s += '              <div class="refhd">%s</div>\n' % head
    s += '              <ul>\n'
    for t, sub in rows:
        s += '                <li>%s%s</li>\n' % (t, (' <span>%s</span>' % sub) if sub else '')
    s += '              </ul>\n            </div>\n'
    return s


# ── 06. 특강형 18H 상세 ──
A.append(slide(
    hdr("05 / 커리큘럼", "특강형 · 18H",
        "Physical AI 온라인 집중 특강 — 3일 전체 시간표",
        "비대면 ZOOM으로 개념·강화학습·모방학습·VLA까지 완주하는 구성입니다.")
    + '          <div class="grid g3">\n'
    + refcol("1일차 · 8H — 개념과 강화학습", [
        ("오리엔테이션 및 개념 이해", "Physical AI 개요 / 발전 방향"),
        ("AI 전체 택사노미", "지도·비지도 / 강화학습 vs 모방학습"),
        ("강화학습 개념", "마르코프 프로퍼티 / MDP"),
        ("강화학습 알고리즘", "DP · 몬테카를로 / TD · SARSA / Q-Learning"),
        ("Deep RL 1", "DQN / REINFORCE"),
        ("Deep RL 2", "A2C / PPO"),
        ("LeRobot 소개", "구성 요소"),
      ])
    + refcol("2일차 · 8H — 하드웨어와 모방학습", [
        ("로봇 하드웨어", "구성요소 / 발전사 / 최신 휴머노이드"),
        ("로보틱스", "Rotation / FK·IK / Control"),
        ("모방학습 기법 1", "Behavior Cloning / DAgger"),
        ("모방학습 기법 2", "Inverse RL / GAIL"),
        ("모방학습 기법 3", "Multi-modal IL / ACT"),
        ("모방학습 최신 기법", "Diffusion Policy / Flow-matching"),
        ("LeRobot 분석", "환경 구성 / 코드 분석"),
      ])
    + refcol("3일차 · 4H — 실습과 VLA", [
        ("VLA 소개 및 개요", "LLM & VLM & VLA / Dataset / Model"),
        ("VLA 상세", "RT-1,2 · OpenVLA / Pi0 · OFT / Pi0.5 · GR00T"),
        ("LeRobot 학습", "데이터 수집 / 구조 / 학습"),
        ("LeRobot 추론", "추론 / SmolVLA"),
      ])
    + '          </div>'))

# ── 07. 단기 집중 28H 상세 (1/2) ──
A.append(slide(
    hdr("05 / 커리큘럼", "단기 집중 · 28H (1/2)",
        "디지털 트윈으로 만나는 Physical AI — 1·2회차",
        "매주 토요일 10:00~17:00, 회차당 7시간. 실물 LeRobot과 시뮬레이션을 병행합니다.")
    + '          <div class="grid g2">\n'
    + refcol("1회차 · 7H — 로봇 제어 기초 (디지털 트윈 구축)", [
        ("10:00 오리엔테이션 및 개념 이해", "Physical AI의 정의와 사례"),
        ("11:00 디지털 트윈 개념·구조", "센서·시뮬레이터·제어기 / 데이터 동기화"),
        ("12:00 LeRobot 실습", "환경 구성 / 센서 제어 / 모터 제어"),
        ("14:00 Unity 디지털 트윈 ①", "설치·조작 / URDF·FBX 임포트 / 모델 로드"),
        ("15:00 Unity 디지털 트윈 ②", "센서 시각화 / ROS·Socket 연동 / PID 제어"),
        ("16:00 LeRobot 통합 테스트", "Unity 시뮬 ↔ LeRobot 연동 시연"),
      ])
    + refcol("2회차 · 7H — 시뮬레이션을 활용한 로봇 제어", [
        ("10:00 강화학습 이론", "MDP · 벨만 / 몬테카를로 · TD / Q러닝 · DQN"),
        ("11:00 강화학습 시뮬레이션 실습", "PPO · SAC / 보상 함수 설계 / MuJoCo 정책 학습"),
        ("12:00 MuJoCo 환경 구성", "URDF·MJCF 로딩 / 관절 상태 / 카메라·GUI"),
        ("14:00 LeRobot+MuJoCo 실습 1", "시연 데이터 수집 → 재생 → ACT 훈련"),
        ("15:00 LeRobot+MuJoCo 실습 2", "정책 배포 / 언어 조건 데이터 / SmolVLA 학습·배포"),
        ("16:00 실물 LeRobot 데이터 수집", "teleoperation 기반 수집"),
      ])
    + '          </div>'))

# ── 08. 단기 집중 28H 상세 (2/2) ──
A.append(slide(
    hdr("05 / 커리큘럼", "단기 집중 · 28H (2/2)",
        "디지털 트윈으로 만나는 Physical AI — 3·4회차",
        "모방학습으로 피킹을 익히고, VLA 통합 에이전트로 마무리합니다.")
    + '          <div class="grid g2">\n'
    + refcol("3회차 · 7H — AI·로봇 피킹 (지능 고도화)", [
        ("10:00 강화학습과 모방학습 비교", "PPO · SAC 설명"),
        ("11:00 모방학습: ACT", "Action Chunking Transformer 구조"),
        ("12:00 모방학습: Diffusion Policy", "구조 이해"),
        ("14:00 ACT 데이터 수집", "LeRobot을 이용한 수집"),
        ("15:00 ACT 학습", "Colab 학습 환경 / 학습 파이프라인"),
        ("16:00 ACT 추론 및 평가", "Trajectory 분석 및 행동 비교"),
      ])
    + refcol("4회차 · 7H — VLA 기반 통합 에이전트", [
        ("10:00 VLA 개요 및 원리", "VLM 구조 / CLIP·BLIP 매핑 / 행동 제어 원리"),
        ("11:00 MuJoCo+LeRobot 환경 및 VLA 연동", "시뮬레이터 설정 / SDK 설치"),
        ("12:00 SmolVLA 모델 분석", "아키텍처 및 경량화 특징"),
        ("14:00 데이터 수집", "언어 명령 → 행동 연동 / 시각+언어+행동 수집"),
        ("15:00 SmolVLA 학습 파이프라인", "토큰화 / 사전학습 모델 Fine-tuning"),
        ("16:00 자연어 명령 시연 및 평가", "멀티모달 행동 생성 / 정확도·일관성 분석"),
      ])
    + '          </div>'))

# ── 09. 정규 교과 45H×2 ──
A.append(slide(
    hdr("05 / 커리큘럼", "정규 교과 · 45H × 2",
        "피지컬AI실습 초급 / 중급 — 대학 정규 학점 교과",
        "전 모듈에 기업 실무 멘토링을 연계해 편성합니다.")
    + '          <div class="grid g2">\n'
    + refcol("초급 45H — 시뮬레이션 기반 로봇 제어 입문", [
        ("Embodied AI와 Digital Twin 입문", "3H · Unity 기초 환경 구축"),
        ("Unity 기초와 가상 환경 제어", "6H · 물리 환경 내 객체 제어"),
        ("LeRobot 오픈소스 활용 기초", "6H · 로봇 팔 제어 구조"),
        ("[프로젝트] Phosphobot 제어", "6H · 소형 로봇 기초 모션 제어"),
        ("강화학습(RL) 기초 구현", "6H · Grid World 에이전트"),
        ("MuJoCo 물리 엔진 활용", "6H · 모델 로딩 / 물리 상호작용"),
        ("LeRobot with MuJoCo", "6H · 통합 시뮬레이션"),
        ("[프로젝트] 기초 주행 로봇 시뮬레이션", "6H · 이동 제어 / 센서 처리"),
      ])
    + refcol("중급 45H — VLA 파인튜닝과 Sim2Real", [
        ("심화 강화학습 로봇 제어", "9H · PPO·SAC를 로봇 팔·휴머노이드에 적용"),
        ("확산 모델(Diffusion) 기반 제어", "6H · Diffusion Policy 행동 생성"),
        ("[프로젝트] LeRobot Data Collection", "6H · 데모 데이터 수집 파이프라인"),
        ("VLA 기초", "3H · 시각·언어를 행동으로 연결"),
        ("VLA 모델 파인튜닝", "9H · OpenVLA Fine-tuning"),
        ("SmolVLA 경량화 모델 활용", "6H · 엣지 배포 및 추론 최적화"),
        ("[프로젝트] Digital Twin 기반 Sim2Real", "6H · 정책 검증"),
      ])
    + '          </div>'))

# ── 10. 정규 교과 연계 135H ──
A.append(slide(
    hdr("05 / 커리큘럼", "정규 교과 · 연계 교과 135H",
        "Physical AI 계열을 최대 225시간까지 확장",
        "위 초급·중급 90H에 아래 3개 교과를 더하면 정규 교과 체계가 완성됩니다.")
    + '          <table class="prop">\n'
    '            <thead><tr><th>교과</th><th>구성 모듈 (전체)</th><th class="c">시간</th></tr></thead>\n'
    '            <tbody>\n'
    '              <tr><td class="trk">고급<br>딥러닝</td><td class="core">딥러닝 레이어 심층 분석(3H) · Convolution 레이어 심층 분석(3H) · Embedding 레이어(3H) · Recurrent 레이어와 시계열(3H) · 시퀀스 투 시퀀스(3H) · [프로젝트] 작사가 AI(3H) · 강화학습 기초 이론(3H) · DQN(3H) · Policy Gradient(3H) · PPO와 SAC(3H) · <b>VLA 모델(3H)</b> · <b>Diffusion Models for Control(3H)</b> · <b>Imitation Learning 심화(3H)</b> · [프로젝트] 딥러닝 기반 로봇 제어(6H)</td><td class="hrs">45H</td></tr>\n'
    '              <tr><td class="trk">인공지능과<br>자율주행</td><td class="core">자율주행 기술 개요(3H) · ROS2와 시뮬레이션 환경(3H) · [실습] ROS2 프로그래밍 기초(3H) · 컴퓨터 비전 기반 차선 인식(3H) · [프로젝트] 라인 트래킹 로봇(9H) · LiDAR 센서와 장애물 감지(3H) · [프로젝트] 장애물 회피 주행(9H) · sLAM과 내비게이션(3H) · 강화학습 기반 자율주행(3H) · [프로젝트] 도심 주행 시뮬레이션(6H)</td><td class="hrs">45H</td></tr>\n'
    '              <tr><td class="trk">임베디드 OS<br>(Edge AI)</td><td class="core">Edge AI 개요·아키텍처(3H) · 엣지 디바이스 환경 구축(3H) · 경량 AI 프레임워크(3H) · 경량화① Quantization(3H) · 경량화② Pruning(3H) · TensorRT 추론 최적화(3H) · ROS2 기초와 로봇 제어(3H) · Gazebo 시뮬레이션(3H) · 센서 기반 주행 제어(3H) · [프로젝트] 강화학습 자율주행(3H) · 실시간 비전 AI on Edge(3H) · 온디바이스 음성·언어 AI(3H) · Edge AI 시스템 통합(3H) · [최종 프로젝트] Edge AI 솔루션 ①②(6H)</td><td class="hrs">45H</td></tr>\n'
    '              <tr class="sumrow"><td class="trk">합계</td><td>피지컬AI실습 초급·중급 90H + 연계 교과 135H</td><td class="hrs">225H</td></tr>\n'
    '            </tbody>\n'
    '          </table>'))

# ── 11. 나노디그리 180H (1/3) — ND1 ──
A.append(slide(
    hdr("05 / 커리큘럼", "나노디그리 · 180H (1/3)",
        "ND1 피지컬 AI 핵심 기초 (60H)",
        "집중이수 주 5일 몰입형. 15시간 4개 모듈로 구성되며, 모듈마다 이론·실습·캡스톤 시간이 분리 편성됩니다.")
    + '          <table class="prop">\n'
    '            <thead><tr><th class="c">과목</th><th>모듈</th><th>세부 구성</th><th class="c">시간</th></tr></thead>\n'
    '            <tbody>\n'
    '              <tr><td class="trk" rowspan="4">ND1<br>핵심 기초</td><td class="course">M1. LLM 파운데이션 &amp; 임베딩</td><td class="core">[이론 5H] Transformer 구조 심화·초거대 AI 진화 사례 · [실습 6H] 경량 SLM(Llama-3 8B, Qwen 1.5B) 로컬 파인튜닝 · [캡스톤 4H] HuggingFace 커스텀 모델 구축</td><td class="hrs">15H</td></tr>\n'
    '              <tr><td class="course">M7. 로봇공학 이론 및 피지컬 인지</td><td class="core">[이론 4H] 로봇 기구학·휴머노이드 모션 제어 사례 · [실습 6H] Numpy 기반 6DoF 매니퓰레이터 순기구학·좌표 가시화 · [실습 5H] 카메라·LiDAR 처리 및 Pinhole 캘리브레이션</td><td class="hrs">15H</td></tr>\n'
    '              <tr><td class="course">M8. ROS2 생태계 및 로봇 통신 심화</td><td class="core">[이론 5H] ROS2 아키텍처·DDS, 다수종 AMR 통합 통신망 사례 · [실습 6H] Turtlesim·Turtlebot3 Topic/Action 통신망 구축 · [실습 4H] URDF 분석 및 TF2 좌표 변환 노드</td><td class="hrs">15H</td></tr>\n'
    '              <tr><td class="course">M13. 물리 시뮬레이션 및 에이전트 연동</td><td class="core">[이론 5H] 강체 동역학·MuJoCo 구조, 대규모 병렬 RL 시뮬레이터 사례 · [실습 5H] MuJoCo·Isaac Sim 로봇 스폰·토크 제어 · [캡스톤 5H] ROS2 연동 Pick &amp; Place 단대단</td><td class="hrs">15H</td></tr>\n'
    '            </tbody>\n'
    '          </table>'))

# ── 11b. 나노디그리 180H (2/3) — ND2 ──
A.append(slide(
    hdr("05 / 커리큘럼", "나노디그리 · 180H (2/3)",
        "ND2 합성 데이터 및 멀티모달 데이터셋 구축 (60H)",
        "시뮬레이션으로 데이터를 찍어내고, 그 데이터로 비전·VLM 모델을 학습시키는 파이프라인 전체를 다룹니다.")
    + '          <table class="prop">\n'
    '            <thead><tr><th class="c">과목</th><th>모듈</th><th>세부 구성</th><th class="c">시간</th></tr></thead>\n'
    '            <tbody>\n'
    '              <tr><td class="trk" rowspan="4">ND2<br>합성 데이터</td><td class="course">M14. Isaac Sim / Omniverse 입문</td><td class="core">[이론 5H] USD 구조 철학·NVIDIA GR00T·Cosmos 사례 · [실습 5H] Isaac Sim 환경 구축·이동체·매니퓰레이터 로드 · [실습 5H] Replicator 도메인 랜덤화(빛·재질·노이즈)</td><td class="hrs">15H</td></tr>\n'
    '              <tr><td class="course">M16. 합성데이터·라벨링 파이프라인</td><td class="core">[이론 4H] Sim2Real 도메인 갭·유효성 지표(PGR) · [실습 6H] 2D 박스·시맨틱 마스크 자동 대량 추출 · [실습 5H] YOLO 학습 포맷 데이터셋화 파이프라인·통계 분석</td><td class="hrs">15H</td></tr>\n'
    '              <tr><td class="course">M9. 로봇 비전 인지: 탐지·추적·포즈</td><td class="core">[이론 4H] 2D/3D 비전 수학 기초·제로샷 6D Pose(FoundationPose) · [실습 6H] YOLO11 합성 데이터 객체 탐지 파인튜닝 · [캡스톤 5H] 실장비 vs 합성 혼합 학습 검증·mAP 산출</td><td class="hrs">15H</td></tr>\n'
    '              <tr><td class="course">M4. 멀티모달 LLM (VLM) 심화</td><td class="core">[이론 4H] 상용 VLM 공정 시각 검수·불량 검출 사례 · [실습 6H] 오픈소스 VLM(Florence-2, Qwen-VL-3B) 설치·추론 · [캡스톤 5H] 합성 이미지 VQA 및 객체 Grounding</td><td class="hrs">15H</td></tr>\n'
    '            </tbody>\n'
    '          </table>'))

# ── 12. 나노디그리 180H (3/3) ──
A.append(slide(
    hdr("05 / 커리큘럼", "나노디그리 · 180H (3/3)",
        "ND5 로보틱스 LLM 에이전트 구축 · 전체 운영 체계",
        "고급 과정은 LLM 에이전트가 로봇을 지휘하는 단대단 아키텍처로 마무리됩니다.")
    + '          <table class="prop">\n'
    '            <thead><tr><th class="c">과목</th><th>모듈</th><th>세부 구성</th><th class="c">시간</th></tr></thead>\n'
    '            <tbody>\n'
    '              <tr><td class="trk" rowspan="4">ND5<br>LLM 에이전트</td><td class="course">M2. 프롬프트 엔지니어링 &amp; RAG 심화</td><td class="core">[이론 4H] 프롬프트 체인 고도화·엔터프라이즈 Search RAG 사례 · [실습 6H] 로봇 매뉴얼·ROS2 문서 색인(ChromaDB) 단대단 RAG · [실습 5H] 환각 억제 Guardrail·RAGAS 신뢰성 개선</td><td class="hrs">15H</td></tr>\n'
    '              <tr><td class="course">M4. VLA 및 공간 지능의 이해</td><td class="core">[이론 4H] RT-2·Figure 01 등 VLA 파운데이션 동향 · [실습 5H] OpenVLA 레이어 구조·3D 좌표계 반환 메커니즘 · [실습 6H] 사물 관계 추론·지시어 공간 지능 분해 및 프롬프트 파싱</td><td class="hrs">15H</td></tr>\n'
    '              <tr><td class="course">M6. 에이전트 플래닝 및 정렬</td><td class="core">[이론 4H] ReAct 한계·계층적 멀티 에이전트 트렌드 · [실습 6H] LangGraph 상태 기반 다단계 워크플로우 에이전트 · [실습 5H] 도구 풀 정의·MLflow 사고 추적 및 플래닝 검증</td><td class="hrs">15H</td></tr>\n'
    '              <tr><td class="course">M12. 로봇 시스템 E2E 통합 캡스톤</td><td class="core">[이론 4H] Task→Skill→Action 3원화 상용 아키텍처 · [실습 5H] LeRobot 연계 통신·ROS2 Action 브릿지 레이어 · [캡스톤 6H] 자연어 지시만으로 인지→플래닝→움직임→검증 데모</td><td class="hrs">15H</td></tr>\n'
    '            </tbody>\n'
    '          </table>\n'
    '          <p class="note"><b>전체 나노디그리 운영 체계</b><br>'
    '초급 AI 기초(3학점, P/F) &nbsp;|&nbsp; 중급 ND1 핵심 기초 · ND2 합성 데이터 · ND3 자율주행/로봇 인지 &nbsp;|&nbsp; '
    '고급 ND4 Sim2Real · ND5 LLM 에이전트 · ND6 산업 디지털 트윈 (각 6학점)<br>'
    '평가 절대평가 75점 이상, 포트폴리오 + 캡스톤 &nbsp;·&nbsp; 운영 학기 중 야간·주말 집중이수, 하계·동계 주 5일 몰입형</p>'))

# ── 13. 전문가 840H (1/2) ──
A.append(slide(
    hdr("05 / 커리큘럼", "전문가 양성 · 840H (1/2)",
        "제조 혁신 Physical AI 전문가 과정 — 정규 교과 365H",
        "6개월 전일제 비대면 실시간. 기초 3과목으로 다지고 Physical AI 핵심 5과목으로 심화합니다.")
    + '          <table class="prop">\n'
    '            <thead><tr><th class="c">구분</th><th>교과목</th><th>세부내용</th><th class="c">시간</th></tr></thead>\n'
    '            <tbody>\n'
    '              <tr><td class="trk" rowspan="3">기초<br>98H</td><td class="course">아이펠 적응하기</td><td class="core">협업 툴 및 교육 철학 이해, 리눅스·터미널 기초, GitHub 사용법 및 레포지토리 구성 실습</td><td class="hrs">14H</td></tr>\n'
    '              <tr><td class="course">딥러닝 기초 다지기</td><td class="core">데이터 전처리·시각화, 사이킷런 머신러닝, Regularization·비지도학습, 캐글 경진대회 실습</td><td class="hrs">49H</td></tr>\n'
    '              <tr><td class="course">딥러닝 심화</td><td class="core">파이토치 기초, CNN·RNN 구현, Transformer 이해, 모델 구현 실습</td><td class="hrs">35H</td></tr>\n'
    '              <tr><td class="trk" rowspan="5">Physical AI<br>핵심 267H</td><td class="course">컴퓨터 비전</td><td class="core">Object Detection, Segmentation, Depth Estimation, 산업용 비전 검사 시스템</td><td class="hrs">49H</td></tr>\n'
    '              <tr><td class="course">NVIDIA Isaac Sim</td><td class="core">Isaac Sim 환경 구축, URDF 로봇 시뮬레이션, ROS2 통합, Synthetic Data Generation</td><td class="hrs">56H</td></tr>\n'
    '              <tr><td class="course">Robot Learning</td><td class="core">강화학습 기반 로봇 제어, Isaac Lab 활용, Imitation Learning, Sim-to-Real Transfer</td><td class="hrs">56H</td></tr>\n'
    '              <tr><td class="course">LeRobot 실습</td><td class="core">LeRobot 프레임워크, Diffusion Policy 모델, 로봇 데이터셋 구축 및 학습</td><td class="hrs">49H</td></tr>\n'
    '              <tr><td class="course">Physical AI 배포</td><td class="core">Jetson 기반 엣지 배포, 실시간 추론 최적화, 로봇 시스템 통합</td><td class="hrs">57H</td></tr>\n'
    '            </tbody>\n'
    '          </table>'))

# ── 14. 전문가 840H (2/2) ──
A.append(slide(
    hdr("05 / 커리큘럼", "전문가 양성 · 840H (2/2)",
        "프로젝트 454H — 전체의 54%",
        "훈련 시간의 절반 이상을 실제 제조 현장 과제 해결에 씁니다.")
    + '          <table class="prop">\n'
    '            <thead><tr><th class="c">구분</th><th>과정</th><th>세부내용</th><th class="c">시간</th></tr></thead>\n'
    '            <tbody>\n'
    '              <tr><td class="trk" rowspan="3">프로젝트<br>454H</td><td class="course">로보틱스 해커톤</td><td class="core">시뮬레이션 기반 로봇 제어 미니 해커톤, 팀 협업 및 피어 리뷰</td><td class="hrs">28H</td></tr>\n'
    '              <tr><td class="course">미니아이펠톤</td><td class="core">중간 점검 프로젝트, 멘토 피드백 및 개선</td><td class="hrs">35H</td></tr>\n'
    '              <tr><td class="course">365 챌린지</td><td class="core">제조 현장 Physical AI 솔루션 개발, PoC 구현 및 최종 발표</td><td class="hrs">391H</td></tr>\n'
    '              <tr><td class="trk">기타<br>21H</td><td class="course">OT·수료식 / 재량교과</td><td class="core">OT 및 졸업식(14H) · 현직자 세미나(7H)</td><td class="hrs">21H</td></tr>\n'
    '              <tr class="sumrow"><td class="trk">합계</td><td colspan="2">정규 교과 365H + 프로젝트 454H + 기타 21H &nbsp;|&nbsp; 120일 / 6개월 / 비대면 실시간 100%</td><td class="hrs">840H</td></tr>\n'
    '            </tbody>\n'
    '          </table>\n'
    '          <div class="grid g4" style="margin-top:16px">\n'
    '            <div class="kpi"><div class="n">60<small>%</small></div><div class="l">목표 취업률</div></div>\n'
    '            <div class="kpi"><div class="n">90<small>%</small></div><div class="l">목표 수료율</div></div>\n'
    '            <div class="kpi"><div class="n">25<small>명</small></div><div class="l">기수당 정원<br>(연 2기 시 50명)</div></div>\n'
    '            <div class="kpi"><div class="n">4.7<small>/5</small></div><div class="l">목표 훈련생 만족도</div></div>\n'
    '          </div>'))

A.append(slide(
    hdr("06 / 역량", "기술 스택과 실습 환경",
        "Digital Twin에서 VLA까지, 전 구간을 다룹니다",
        "과정 규모에 따라 아래 스택 중 필요한 범위를 선택해 구성합니다.")
    + '          <div class="chips">\n'
    + "".join('            <span class="chip">%s</span>\n' % t for t in [
        "Unity (Digital Twin)", "MuJoCo / Isaac Sim", "LeRobot (Hugging Face)", "Phosphobot",
        "PPO / SAC", "ACT / Diffusion Policy", "SmolVLA / OpenVLA", "ROS2 (Humble)",
        "Python · PyTorch", "Google Colab"])
    + '          </div>\n'
    '          <div class="grid g2" style="margin-top:22px">\n'
    '            <div class="refcol">\n'
    '              <div class="refhd">실물 실습형 인프라</div>\n'
    '              <ul>\n'
    '                <li>LeRobot 로봇팔 <span>2인 1대 권장</span></li>\n'
    '                <li>실습 공간 및 안정적 네트워크 <span>대면 과정</span></li>\n'
    '                <li>개인 노트북 <span>전 과정 공통</span></li>\n'
    '              </ul>\n'
    '            </div>\n'
    '            <div class="refcol">\n'
    '              <div class="refhd">시뮬레이션 중심 인프라</div>\n'
    '              <ul>\n'
    '                <li>Google Colab 또는 클라우드 GPU <span>1인 1환경</span></li>\n'
    '                <li>로봇 장비 <span>불필요</span></li>\n'
    '                <li>도달 범위 <span>장비 없이 VLA 파인튜닝까지 완주 가능</span></li>\n'
    '              </ul>\n'
    '            </div>\n'
    '          </div>'))

A.append(slide(
    hdr("07 / 노하우", "실제 운영에서 얻은 것",
        "28시간을 직접 운영하며 확인한 네 가지")
    + '          <div class="why">\n'
    '            <h3>운영 노하우</h3>\n'
    '            <ul>\n'
    '              <li><b>장비 대수가 학습 몰입을 좌우합니다.</b> 로봇팔 1대를 3~4명이 공유하면 실습 밀도가 급격히 떨어집니다. '
    '실물 실습은 2인 1대를 권장하며, 예산 제약이 있으면 시뮬레이션 중심으로 전환해 1인 1환경을 확보하는 편이 효과적입니다.</li>\n'
    '              <li><b>설치 시간은 실습 시간이 아닙니다.</b> 로컬 설치가 필요한 도구는 사전 안내 자료를 배포하거나, '
    'Colab 기반으로 설계해 설치 단계를 제거합니다.</li>\n'
    '              <li><b>인프라를 먼저 확정하고 커리큘럼을 설계합니다.</b> 가용 장비·공간·네트워크 기준을 먼저 정한 뒤 '
    '환경 세팅~평가까지의 시간을 역산합니다.</li>\n'
    '              <li><b>현업 엔지니어에게는 엔지니어링 깊이가 필요합니다.</b> 단순 체험을 넘어 Tele-operation 데이터 수집의 정교함, '
    '캘리브레이션 등 실무 관점 가이드를 제공합니다.</li>\n'
    '            </ul>\n'
    '          </div>'))

A.append(slide(
    '          <p class="kicker">맺음말</p>\n'
    '          <h2>규모와 목표를 알려주시면,<br>거기에 맞춰 재단해 드리겠습니다.</h2>\n'
    '          <p class="msg">18시간 특강부터 840시간 전문가 양성까지, 같은 뿌리에서 나온 커리큘럼입니다. '
    '실제로 운영해 본 과정이 기준점에 있기 때문에 어느 규모로 조정하더라도 무엇이 빠지고 무엇이 남아야 하는지 판단할 수 있습니다.</p>\n'
    '          <div class="sign">\n'
    '            <span><b>모두의연구소 기업교육</b></span>\n'
    '            <span>교육 문의 · modu.biz@modulabs.co.kr</span>\n'
    '          </div>', cls="closing", center=True))

write_deck(os.path.join(OUT, "Physical AI 레퍼런스", "레퍼런스 소개",
                        "PhysicalAI_레퍼런스_발표덱_가로.html"),
           "Physical AI 교육 레퍼런스 — 모두의연구소", A)


# ══════════════════════════════════════════════════════════════
# DECK B — 삼성전자 Physical AI 제안
# ══════════════════════════════════════════════════════════════
B = []

B.append(slide(
    '          <span class="cover-badge">🔴 모두의연구소 &nbsp;×&nbsp; 삼성전자</span>\n'
    '          <h1>Physical AI<br><span>실무 교육 제안</span></h1>\n'
    '          <p class="sub">시뮬레이션 중심 설계로 장비 없이 VLA까지 — 1일 8시간 / 5일 40시간</p>\n'
    '          <div class="cover-meta">\n'
    '            <span><b>작성</b> · 모두의연구소 비즈팀</span>\n'
    '            <span><b>일자</b> · 2026. 08.</span>\n'
    '            <span><b>범위</b> · 2개 과정 (체험형 · 엔지니어 심화형)</span>\n'
    '          </div>', cls="cover", center=True))

B.append(slide(
    hdr("01 / 문제", "왜 이 제안인가",
        "Physical AI 교육의 가장 큰 걸림돌은 장비입니다",
        "실제로 28시간 과정을 운영하며 확인한 문제입니다. 장비를 나눠 쓰면 실습이 얕아지고, 인원수만큼 갖추면 예산이 감당되지 않습니다.")
    + '          <div class="grid g3">\n'
    '            <div class="task"><div class="ti">⏳</div><div class="tt">대기 시간이 실습을 잠식</div>'
    '<div class="td">로봇팔 1대를 3~4명이 공유하면 만지는 시간보다 기다리는 시간이 길어집니다</div></div>\n'
    '            <div class="task"><div class="ti">🔧</div><div class="tt">설치·세팅에 소모되는 시간</div>'
    '<div class="td">로컬 설치와 캘리브레이션이 실습 시간의 상당 부분을 가져갑니다</div></div>\n'
    '            <div class="task"><div class="ti">💰</div><div class="tt">1인 1대의 예산 부담</div>'
    '<div class="td">인원수만큼 장비를 갖추면 이번엔 비용이 문제가 됩니다</div></div>\n'
    '          </div>\n'
    '          <div class="quote" style="margin-top:20px">\n'
    '            <div class="q">2026년 현재, 이 문제는 기술적으로 해소 가능합니다.</div>\n'
    '            <div class="by">경량 VLA 모델과 표준 시뮬레이션 벤치마크의 등장으로 전제가 바뀌었습니다.</div>\n'
    '            <div class="mark">"</div>\n'
    '          </div>'))

B.append(slide(
    hdr("02 / 기술 지형", "2026년의 변화 (1/2)",
        "무엇이 달라졌는가 — 세 가지",
        "최신 기술 동향을 커리큘럼에 그대로 반영했습니다.")
    + '          <div class="grid g3">\n'
    '            <div class="case">\n'
    '              <div class="ctop"><div class="co">VLA 모델 경쟁</div><div class="cat">01</div></div>\n'
    '              <div class="desc">GR00T N1.7(3B) · π0.5(3.3B) · Gemini Robotics가 잇따라 공개되며 범용 로봇 모델 경쟁이 시작됐습니다.</div>\n'
    '              <div class="taglist"><b>반영</b> · 모델 지형도를 읽는 눈 자체를 교육 내용으로 편성</div>\n'
    '            </div>\n'
    '            <div class="case">\n'
    '              <div class="ctop"><div class="co">Flow matching</div><div class="cat">02</div></div>\n'
    '              <div class="desc">π0 계열이 RT-2·OpenVLA의 discrete token 예측을 대체했습니다. 접촉이 많은 조작에서 더 매끄러운 궤적을 만듭니다.</div>\n'
    '              <div class="taglist"><b>반영</b> · ACT → Diffusion Policy → Flow matching 계보로 재구성</div>\n'
    '            </div>\n'
    '            <div class="case">\n'
    '              <div class="ctop"><div class="co">World Model</div><div class="cat">03</div></div>\n'
    '              <div class="desc">NVIDIA Cosmos Predict/Transfer가 물리 시뮬레이션만으로는 메우지 못하던 시각적 사실성 갭을 메우기 시작했습니다.</div>\n'
    '              <div class="taglist"><b>반영</b> · 5일 과정에 신규 모듈로 추가</div>\n'
    '            </div>\n'
    '          </div>'))

B.append(slide(
    hdr("02 / 기술 지형", "2026년의 변화 (2/2)",
        "장비 최소화를 가능하게 한 두 가지",
        "이 두 변화가 이번 제안의 핵심 근거입니다.")
    + '          <div class="grid g2">\n'
    '            <div class="case">\n'
    '              <div class="ctop"><div class="co">경량 VLA — 단일 GPU 학습</div><div class="cat">04</div></div>\n'
    '              <div class="desc">SmolVLA 450M은 24GB VRAM 1장에서 파인튜닝을 완주합니다. 고가 GPU 클러스터가 없어도 됩니다.</div>\n'
    '              <div class="taglist"><b>의미</b> · 수강생 1인 1환경을 Colab만으로 확보 가능</div>\n'
    '            </div>\n'
    '            <div class="case">\n'
    '              <div class="ctop"><div class="co">LIBERO — 표준 평가 벤치마크</div><div class="cat">05</div></div>\n'
    '              <div class="desc">Robosuite 기반 130개 언어조건 태스크(Spatial·Object·Goal·Long)로 실물 텔레오퍼레이션 없이 데이터 수집~평가를 완주할 수 있습니다.</div>\n'
    '              <div class="taglist"><b>의미</b> · 로봇 장비 없이도 논문과 같은 기준의 성능 숫자를 얻음</div>\n'
    '            </div>\n'
    '          </div>\n'
    '          <div class="why" style="margin-top:18px">\n'
    '            <h3>결론</h3>\n'
    '            <ul>\n'
    '              <li><b>장비를 줄이면 실습이 얕아진다</b>는 전제가 2026년에는 더 이상 성립하지 않습니다. '
    '시뮬레이션 중심으로 설계하면 오히려 <b>1인 1환경 · 설치 시간 0 · 표준 벤치마크 평가</b> 세 가지를 동시에 얻습니다.</li>\n'
    '            </ul>\n'
    '          </div>'))

B.append(slide(
    hdr("03 / 제안", "과정 구성",
        "대상과 목표에 따라 두 가지로 나눴습니다")
    + '          <div class="grid g2">\n'
    '            <div class="track t1">\n'
    '              <div class="th"><div class="tk">TRACK 01 · 체험형</div><div class="tn">Physical AI 이해와 체험</div>'
    '<div class="tp">1일 8시간 · 비개발 실무자</div></div>\n'
    '              <div class="tb">\n'
    '                <p style="margin:0 0 10px">사전 지식과 코드 작성 없이, 제공된 노트북을 실행하며 Physical AI가 어떻게 작동하는지 체감합니다.</p>\n'
    '                <div class="chips">\n'
    '                  <span class="chip">개념 이해</span><span class="chip">브라우저 실습</span>'
    '<span class="chip">적용 시나리오 도출</span>\n'
    '                </div>\n'
    '                <p style="margin:12px 0 0;font-weight:700;color:#C92434">최종 산출물 · 내 문장으로 움직인 로봇 시연 영상</p>\n'
    '              </div>\n'
    '            </div>\n'
    '            <div class="track t4">\n'
    '              <div class="th"><div class="tk">TRACK 02 · 엔지니어 심화</div><div class="tn">Physical AI 구현</div>'
    '<div class="tp">5일 40시간 · 연구원 · 엔지니어</div></div>\n'
    '              <div class="tb">\n'
    '                <p style="margin:0 0 10px">시뮬레이션 환경에서 VLA 모델을 직접 파인튜닝하고, 표준 벤치마크로 성능을 평가합니다.</p>\n'
    '                <div class="chips">\n'
    '                  <span class="chip">강화학습</span><span class="chip">모방학습</span>'
    '<span class="chip">VLA 파인튜닝</span><span class="chip">Sim2Real</span>\n'
    '                </div>\n'
    '                <p style="margin:12px 0 0;font-weight:700;color:#1D4FD8">최종 산출물 · 파인튜닝한 정책 + 벤치마크 성능 리포트</p>\n'
    '              </div>\n'
    '            </div>\n'
    '          </div>\n'
    '          <p class="note">전제 · 40시간 과정은 Python 및 딥러닝 기초 이해를 요구합니다.</p>'))

B.append(slide(
    hdr("04 / 커리큘럼", "1일 8시간 — 비개발 실무자",
        "코드 작성 없이, 개념 이해에서 자사 적용 판단까지")
    + '          <table class="prop">\n'
    '            <thead><tr><th class="c">구분</th><th>모듈</th><th>주요 내용</th><th class="c">시간</th></tr></thead>\n'
    '            <tbody>\n'
    '              <tr><td class="trk">이해</td><td class="course">Physical AI란 무엇이고, 왜 지금인가</td>'
    '<td class="core">3축 구조 · 2026 VLA 모델 지형(GR00T·π0.5·Gemini Robotics) · 산업 적용 사례</td><td class="hrs">1H</td></tr>\n'
    '              <tr><td class="trk">이해</td><td class="course">로봇이 배우는 세 가지 방식</td>'
    '<td class="core">강화학습 · 모방학습(ACT·Diffusion Policy) · VLA의 차이와 선택 기준</td><td class="hrs">1H</td></tr>\n'
    '              <tr><td class="trk">실습</td><td class="course">브라우저에서 로봇 세우기</td>'
    '<td class="core">설치 없이 Colab MuJoCo 실행 · 관절 구조와 물리 엔진 직접 확인</td><td class="hrs">1.5H</td></tr>\n'
    '              <tr><td class="trk">실습</td><td class="course">사전학습 VLA 모델로 로봇 움직이기</td>'
    '<td class="core">LIBERO 태스크 · SmolVLA 추론 실행 · 성공/실패 케이스 비교</td><td class="hrs">1.5H</td></tr>\n'
    '              <tr><td class="trk">실습</td><td class="course">내 문장으로 로봇 제어하기</td>'
    '<td class="core">자연어 명령 변경에 따른 행동 변화 · 실패 원인 분석 · 시연 영상 산출</td><td class="hrs">2H</td></tr>\n'
    '              <tr><td class="trk">적용</td><td class="course">우리 업무에 어디 쓸 수 있을까</td>'
    '<td class="core">도입이 유효한 업무의 조건 · 가능/불가능 구분 · 조별 시나리오 도출</td><td class="hrs">1H</td></tr>\n'
    '              <tr class="sumrow"><td class="trk">합계</td><td colspan="2">Physical AI 이해와 체험 과정</td>'
    '<td class="hrs">8H</td></tr>\n'
    '            </tbody>\n'
    '          </table>'))

B.append(slide(
    hdr("04 / 커리큘럼", "5일 40시간 — 엔지니어 심화",
        "4일차 VLA 파인튜닝이 과정의 무게중심입니다")
    + '          <table class="prop">\n'
    '            <thead><tr><th class="c">일차</th><th>주제</th><th>주요 내용</th><th class="c">시간</th></tr></thead>\n'
    '            <tbody>\n'
    '              <tr><td class="trk">1일차</td><td class="course">Physical AI 지형과 시뮬레이션 기초</td>'
    '<td class="core">2026 VLA 모델 비교 · 로보틱스 기초(기구학·제어) · MuJoCo/MJX 구축 · '
    'Isaac Lab 개관 · LeRobot v2 포맷 분석</td><td class="hrs">8H</td></tr>\n'
    '              <tr><td class="trk">2일차</td><td class="course">강화학습 기반 로봇 제어</td>'
    '<td class="core">MDP·벨만 · DQN → Policy Gradient · PPO/SAC 원리 · 보상 함수 설계 · '
    'MuJoCo 로봇 팔 정책 학습</td><td class="hrs">8H</td></tr>\n'
    '              <tr><td class="trk">3일차</td><td class="course">모방학습과 데이터 파이프라인</td>'
    '<td class="core">BC·DAgger·IRL·GAIL 계보 · ACT chunking · Diffusion Policy · '
    'Flow matching · LIBERO→LeRobot v2 변환</td><td class="hrs">8H</td></tr>\n'
    '              <tr><td class="trk">4일차</td><td class="course"><b>VLA 파인튜닝 — 핵심</b></td>'
    '<td class="core">VLM→VLA 계보 · SmolVLA 450M 아키텍처 · <b>LIBERO-Spatial 파인튜닝(단일 GPU)</b> · '
    '벤치마크 성공률 측정 · 실패 케이스 분석</td><td class="hrs">8H</td></tr>\n'
    '              <tr><td class="trk">5일차</td><td class="course">월드모델 · Sim2Real · 캡스톤</td>'
    '<td class="core">NVIDIA Cosmos 역할 · 합성 데이터 증강 · 도메인 랜덤화 · '
    '실물 이관 경로 설계 · 팀별 캡스톤 발표</td><td class="hrs">8H</td></tr>\n'
    '              <tr class="sumrow"><td class="trk">합계</td><td colspan="2">Physical AI 구현 — VLA 파인튜닝 실무 과정</td>'
    '<td class="hrs">40H</td></tr>\n'
    '            </tbody>\n'
    '          </table>'))

B.append(slide(
    hdr("05 / 산출물", "수강생이 가져가는 것",
        "'들었다'가 아니라 '만들었다'로 끝나는 과정")
    + '          <div class="grid g2">\n'
    '            <div class="mvp">\n'
    '              <div class="mh"><div class="idx">8H</div><div class="mt">비개발 실무자 체험형</div></div>\n'
    '              <div class="row"><span class="tag">산출</span><span class="val">본인의 자연어 명령으로 동작시킨 로봇 시연 영상</span></div>\n'
    '              <div class="row"><span class="tag">이해</span><span class="val tech">Physical AI 기술 지형 및 적용 가능/불가능 판단 기준</span></div>\n'
    '              <div class="row"><span class="tag">적용</span><span class="val eff">조별 사내 적용 시나리오 후보 리스트</span></div>\n'
    '            </div>\n'
    '            <div class="mvp">\n'
    '              <div class="mh"><div class="idx">40H</div><div class="mt">엔지니어 심화형</div></div>\n'
    '              <div class="row"><span class="tag">모델</span><span class="val">직접 파인튜닝한 SmolVLA 정책 체크포인트</span></div>\n'
    '              <div class="row"><span class="tag">평가</span><span class="val tech">LIBERO 벤치마크 성능 리포트 (성공률·베이스라인 대비·실패 분석)</span></div>\n'
    '              <div class="row"><span class="tag">역량</span><span class="val">LeRobot v2 포맷 데이터 파이프라인 구축 경험</span></div>\n'
    '              <div class="row"><span class="tag">프로젝트</span><span class="val eff">팀별 캡스톤 결과물 및 발표 자료</span></div>\n'
    '              <div class="row"><span class="tag">확장</span><span class="val eff">실물 로봇 도입 시 활용 가능한 Sim2Real 이관 설계안</span></div>\n'
    '            </div>\n'
    '          </div>\n'
    '          <p class="note">LIBERO는 실제 VLA 모델 논문들이 성능을 보고하는 표준 벤치마크입니다. '
    '여기서 측정한 성공률은 학계·산업계와 같은 기준으로 비교 가능한 숫자입니다.</p>'))

B.append(slide(
    hdr("06 / 인프라", "필요한 것과 필요 없는 것",
        "브라우저만 열면 실습이 시작됩니다")
    + '          <div class="ba-head"><div>항목</div><div>기존 실물 실습형</div><div></div>'
    '<div class="h-after">본 제안 (시뮬레이션 중심)</div><div>효과</div></div>\n'
    '          <div class="ba"><div class="task-name">로봇 장비</div>'
    '<div class="before">LeRobot 1대를 3~4명 공유</div><div class="arrow">→</div>'
    '<div class="after">불필요 (옵션: 데모 스테이션 2~4대)</div><div class="gain">장비비<br>대폭 절감</div></div>\n'
    '          <div class="ba"><div class="task-name">실습 환경</div>'
    '<div class="before">Unity 등 로컬 설치 필요</div><div class="arrow">→</div>'
    '<div class="after">Google Colab — 설치 일절 없음</div><div class="gain">세팅 시간<br>0</div></div>\n'
    '          <div class="ba"><div class="task-name">1인당 환경</div>'
    '<div class="before">공유로 인한 대기 발생</div><div class="arrow">→</div>'
    '<div class="after">1인 1환경 보장</div><div class="gain">실습 밀도<br>극대화</div></div>\n'
    '          <div class="ba"><div class="task-name">GPU</div>'
    '<div class="before">고사양 워크스테이션</div><div class="arrow">→</div>'
    '<div class="after">24GB VRAM급 1장 (Colab Pro 가능)</div><div class="gain">진입 장벽<br>완화</div></div>\n'
    '          <div class="ba"><div class="task-name">성능 평가</div>'
    '<div class="before">정성적 시연 확인</div><div class="arrow">→</div>'
    '<div class="after">LIBERO 표준 벤치마크 성공률</div><div class="gain">객관적<br>수치 확보</div></div>'))

B.append(slide(
    hdr("07 / 운영", "운영 방안과 사전 확인 사항",
        "실제 28시간 운영에서 확인한 문제를 설계로 해소했습니다")
    + '          <div class="split">\n'
    '            <div class="why">\n'
    '              <h3>설계에 반영한 것</h3>\n'
    '              <ul>\n'
    '                <li><b>장비 공유 문제</b> — 전 과정 시뮬레이션으로 1인 1환경 확보</li>\n'
    '                <li><b>설치 시간</b> — 로컬 설치 도구 제거, Colab으로 통일</li>\n'
    '                <li><b>가짜 실습 우려</b> — LIBERO 표준 벤치마크로 객관적 성능 측정</li>\n'
    '                <li><b>실물 경험</b> — 데모 스테이션 2~4대 옵션으로 절충 가능</li>\n'
    '              </ul>\n'
    '            </div>\n'
    '            <div class="refcol">\n'
    '              <div class="refhd">사전 확인이 필요한 사항</div>\n'
    '              <ul>\n'
    '                <li>GPU 환경 <span>Colab Pro 사용 여부 또는 사내 GPU 서버 활용 가능 여부</span></li>\n'
    '                <li>외부 네트워크 정책 <span>Hugging Face 모델·데이터셋 다운로드 허용 여부</span></li>\n'
    '                <li>수강 인원 및 사전 역량 <span>40H 과정은 Python·딥러닝 기초 전제</span></li>\n'
    '              </ul>\n'
    '            </div>\n'
    '          </div>'))

B.append(slide(
    '          <p class="kicker">맺음말</p>\n'
    '          <h2>장비 없이도,<br>실습은 얕아지지 않습니다.</h2>\n'
    '          <p class="msg">경량 VLA 모델과 표준 시뮬레이션 벤치마크가 자리 잡으면서 '
    '"장비를 줄이면 실습이 얕아진다"는 전제는 더 이상 성립하지 않습니다. '
    '본 제안은 실제 28시간 과정을 운영하며 확인한 문제들을 그대로 설계에 반영한 결과입니다. '
    '교육 일정과 인원이 확정되면 세부 운영 계획과 견적을 드리겠습니다.</p>\n'
    '          <div class="sign">\n'
    '            <span><b>모두의연구소 기업교육</b></span>\n'
    '            <span>교육 문의 · modu.biz@modulabs.co.kr</span>\n'
    '          </div>', cls="closing", center=True))

write_deck(os.path.join(OUT, "삼성전자_PhysicalAI", "제안서",
                        "삼성전자_PhysicalAI_발표덱_가로.html"),
           "삼성전자 Physical AI 실무 교육 제안 — 모두의연구소", B)
