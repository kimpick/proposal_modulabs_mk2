#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
52개 온라인 과정 커리큘럼 구글 시트 일괄 다운로드 스크립트
실행: python download_curricula.py
결과: curricula_csv/ 폴더에 CSV 파일 52개 생성
"""
import urllib.request, os, time, re

OUTPUT_DIR = "curricula_csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)

courses = [
    ("머신러닝 기초 with 파이썬", "1I7PQlgFUZFju1ai1e8F5QZjCsJ631v2yaoEAo1Inygs"),
    ("데이터 분석으로 보는 기초 통계", "1j-8W_rbAUZsYgkBkARASE6l6mIYeIEsbbnGcLyJrdvI"),
    ("데이터 분석 ABC", "16fLmcXkAgIRO8U4Y-3zRRSkhlbCbEvNnOmmkElLQJZw"),
    ("딥러닝 한번에 끝내기", "1TWIKMUApWWCXeP_wf2RxciTnyOBjehA8Aa_V5vyGOPg"),
    ("자란다 파이썬", "18fnLAOuiOUVcLhvoMUDe5tLhTF9aM54gcrqW_tmqYhI"),
    ("딥러닝으로 시작하는 컴퓨터 비젼", "1UcrgZHWqFqFQnFooFrQ2wv-O16XkUR0BDR2qdhaduLo"),
    ("쉽게 배울 수 있는 라이브러리 기초", "1Sz9w3jK-dAgvXZVZrPTUFRIFACrc6zx9li_6-uUZApM"),
    ("“생성AI 시대” 비즈니스 생존 전략", "1kIxhKD6OfHqOaOp5pQfLrcKplVF8x33ww62WApw4Ono"),
    ("챗GPT로 인싸 크리에이터 되는 법", "1Grtn0LIjSbztnYb-UL1QKz0PEGe2TwGBWyPbwqI1dw4"),
    ("상위 1% 일잘러를 위한 고급 프롬프트 엔지니어링", "1IxK8iFvqEVQlP8p5qjrVtpqPebFjXcUJOhrjXlE5bCs"),
    ("생성형 AI를 활용한 15초 광고(숏폼) 만들기", "1IkExLDEwq1sWe-a6cQMptwW9Os4rA96vJzfKaiOkm3E"),
    ("직장인을 위한 AI 윤리: 신뢰할 수 있는 AI 활용법", "1AHMEgIQn2ZLvds7FPcmyH4qes5-H-ugGakuF-9-4E1E"),
    ("[챗GPT x 사업] 합격하는 예비창업패키지 사업계획서 작성 노하우", "1-LnpetisBlMCf9ZcrjI8K-VsMH2rt87cpBMZapj00s4"),
    ("[노션 x HR] 채용이 쉬워지는 채용대시보드 만들기", "10SvN7u2w4rlCN2dRBl6LXWFPMKsf4mr8Z8Tk3d2pGIo"),
    ("[노션 x 기획] 숲을 볼 수 있는 똑똑한 지식관리법", "1ulCSswipPcHsDMJeR_K3Koug3_5bMf4CAaiCC-D9V2o"),
    ("[노션 x 리더십] 새내기 팀장을 위한 팀 페이지 만들기", "13jEq9OwdriSZXCkfHyKyOkMB4rCKou5QqKaEyX7t5Vc"),
    ("[노션 x 기획] 기록이 성과로 이어지는 업무관리법", "1K9qsTDrGAWYI5PvjXHrhD1owqRQPwpLaptd5Q6ZXHrg"),
    ("[클로드 x 마케팅] AI를 활용한 SNS 광고배너 100개 한 번에 만들기", "1kIxhKD6OfHqOaOp5pQfLrcKplVF8x33ww62WApw4Ono"),
    ("[슬랙 x HR] 센스있는 공지문 발송 슬랙봇 만들기", "1SX6RSIYzRLH8qKFoKOZ1X56WgSWEwFF_okNL1LFXKF0"),
    ("무료 툴로 시작하는 퍼포먼스 마케팅 자동화", "1MZZ3Ec8s0wc_stKB95Px148dCvJzpP0Lic0BDTS8Q24"),
    ("AI 프롬프트 작성법: UX리서치 실무자를 위한 7가지 비법", "1bkLlEqVlrugZgaBGvin7axgS9WW99Q2GoviqWMliJbM"),
    ("AI 프로토타이핑 완벽 가이드: UX 디자인 실무편", "1PAPSpQPt3_qHx0hgS6gNuDWTALghZvf_nkK_yWP97cY"),
    ("Claude로 끝내는 상세페이지 AI 자동화", "1QdnnnPzlPcyEVlH5I8U8fdV1lR5qYwtUcVS-qSwPscA"),
    ("[SQL 입문] ChatGPT로 데이터 분석 시작하기", "1by2RAlbic7DwsiH6d_CbzY1hzkyqKjPCYpaWA2jWs84"),
    ("[노코드] Bolt.new로 하루 만에 MVP 만들기", "1XFV850pgyWPk34hd6zvzksaLf-GHGfrzcoCO3ybQECI"),
    ("Cursor & GPT로 시작하는 바이브 코딩", "1GVnFJ1v-q9uPmKvYIYD69oZBVSEmL4CdKHBkrCQK1wg"),
    ("CS 담당자를 위한 노코드 AI 업무 자동화 with Make", "13LGX16sjlqFUbr2_bxjMXFRXtOyRRkvgi9g46d887pc"),
    ("클릭을 부르는 AI 광고 이미지 제작 입문", "1GrwOzYEg2haG5uZWAXUSO_ednUqDaOQCaIZk7IsSFJU"),
    ("AI 활용 UX 설계: 페르소나부터 어피니티 다이어그램까지", "1KH4ylwNwzxbTATqUx96Y0MA5yGS6gHD0AFtm2I2Djog"),
    ("실무에 써먹는 가상 사용자 인터뷰 with GPTs", "1iISlE5wgYdmv8NEGo37_bQsVvp3pr4OKL080NC9vYzk"),
    ("배워서 바로 쓰자! 하루 2시간 아끼는 협업 툴 & 업무 자동화", "1_wEbKJPzepozSxVUdLZXxL7EiOkGFXLtTDr5i89IT4E"),
    ("[AI 능력자] AI와 함께하는 서비스 개발: 리서치부터 MVP 배포까지", "1vXLf4AJLO_7NxSyX0GIsR3fsmZ8aJFup5pc8Qdh8mcI"),
    ("[AI 능력자] 모르면 뒤쳐지는 AI 활용 콘텐츠 마케팅 스킬", "1CcNCx1ir0L1-P3y78HHffn8Jl_FbdMO0IhF52mXxyMc"),
    ("[첫걸음] 일상부터 업무까지: ChatGPT와 친해지기", "1rzhmG7JaDtbzcwgwlD8mseewg2EFgNpp1FYC_-0XbG4"),
    ("[AI 능력자] AI로 시작하는 콘텐츠 크리에이터", "1A-HEDsR5DQ__Pq4Ocixcgb3wyJHzBakwODywWZFQAN4"),
    ("[첫걸음] 파이썬에 도전하자! 기초부터 프로그래밍까지", "19JYSZkJDYzsPIRAeUUHhF8I3uKV7t2o3AbzPnU0Dk6Q"),
    ("[첫걸음] 데이터를 보는 눈, 파이썬으로 배우는 통계 기초", "1bDtvn1nhkBX11YFcjCah2zGd5oJ3Osq9B7CL6z31Gi4"),
    ("[첫걸음] 기본부터 탄탄하게, 파이썬 데이터 분석 첫 만남", "1Jto9yBLEua_Pov2moTKI6DNF4gufED35ajsmCMbFYKE"),
    ("[AI 능력자] 바이브 코딩 with Cursor: 챗봇, DB 배포까지", "1bHRak-2DXVYPeslpPZumyRpSOJoqw7MMrwRGEwTE7fo"),
    ("[왕초보] 비개발자도 할 수 있는 바이브 코딩 웹 개발", "146ksSu8juFj7iSyKaR0ZmdvHKEb8zAaYOxhOkkchTuk"),
    ("[AI 능력자] 비개발자도 할 수 있는 바이브 코딩 업무 자동화", "1C-SC8G4JEaFJlZ1hLSxHl8oo-paQ8Dd_TJRxoKi3qPE"),
    ("MLOps의 정석: AI 모델 배포부터 운영까지 한 번에 끝내기", "1Aspe_rA-KqjuLT9YGG0DExbFaOUucckPHfkNdCkClq0"),
    ("현직 CTO에게 배우는 데이터 거버넌스 & 엔지니어링", "1u9EXEEcrFz_lq90C2dpdk9n4GMw8Eqey6PQqTCloQFA"),
    ("컴퓨터 비전 실무 완전 정복! 최신 객체 탐지 모델부터 생성형 AI까지", "1TmRRDECGDoEnvoFr6MKnmfoQM0ZjsnM0Bb8pe44aPng"),
    ("실리콘밸리 로보틱스 엔지니어에게 배우는 자율주행 시뮬레이션", "1zg3zbFILIifN2_WLIsAhPiiYT2ONFtttJr5whSB4GXs"),
    ("AI를 활용한 제조 공정 불량 예측 모델 개발의 이론과 실습", "1CJsuBdQ-1RcTTNWu11y9miTH6AbbjdXTIqXgMan5gHw"),
    ("AI 크리에이티브 올인원 패키지: 최신 생성형 AI부터 수익화까지", "1qrGQkMXMfVWW5azIkGz3ITJoR8oNc0wRrR8Sk74dcRo"),
    ("Vibe Coding Fullstack: 입문부터 서비스 배포까지", "1tWuCnUTxTqC8o8gyoZd4w1on6a-OFLzy1Tf3cuNng2A"),
    ("AI를 활용한 PPT 제작: Genspark & GPT", "1Ziu6hJeYfwGVAJ2fjtE0v9HnbkH5fmGPSDQeuxLUGnk"),
    ("[무료] ChatGPT 입문: 로그인부터 커스텀 GPT 만들기까지", "1mM1wY8c4DzIOC6Y8M-hK7bRafv9MTvbKY9BqmxFQA-s"),
    ("[무료] 코딩, 말로 하자! 바이브 코딩 입문 with Windsurf", "1YNXODA1rGhBU4puIQhrewVQsupTFVhtmQmiGbWSnAN8"),
    ("[무료] 중장년을 위한 AI: ChatGPT와 건강 상담하기", "1ZIP50nq1Ny93het3_LCqRoHw14WEf4dkCAnLW0DGo6o"),
]

ok, fail = 0, 0
for i, (name, sid) in enumerate(courses, 1):
    csv_url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv"
    safe_name = re.sub(r'[\\/:*?"<>|]', '_', name)[:60]
    filepath = os.path.join(OUTPUT_DIR, f"{i:02d}_{safe_name}.csv")
    try:
        req = urllib.request.Request(csv_url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        data = resp.read().decode("utf-8-sig")
        with open(filepath, "w", encoding="utf-8-sig") as f:
            f.write(data)
        ok += 1
        print(f"[{i:02d}/52] OK  {name}")
    except Exception as e:
        fail += 1
        print(f"[{i:02d}/52] FAIL {name}: {e}")
    time.sleep(0.5)

print(f"\n완료: {ok}/52 성공, {fail}/52 실패")
print(f"CSV 파일 위치: {os.path.abspath(OUTPUT_DIR)}/")
