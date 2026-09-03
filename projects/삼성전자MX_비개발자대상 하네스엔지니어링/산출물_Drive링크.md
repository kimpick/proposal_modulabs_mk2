# 산출물 Drive 링크 — 삼성전자MX 비개발자 하네스 엔지니어링

리포에는 `*.pdf`가 `.gitignore`로 제외되어 있어, **고객 발송 원본 PDF는 Drive가 단일 진실**입니다.

## 본진 폴더

**`20260803_삼성MX사업부(수원신규)_비개발자AI교육`**
→ https://drive.google.com/drive/folders/1U1eS1D95_EZ2MS1oXftsqbHhlqJQTpDx

| 파일 | 유형 | 발행/수정 | 링크 |
|---|---|---|---|
| [모두의연구소]삼성전자MX_비개발자_하네스엔지니어링_종합제안서.pdf | 제안서 15p | 2026-08-10 | [열기](https://drive.google.com/file/d/12N9P9DH20s5FswC40bJ4nRFhSHXNAr1_/view) |
| [모두의연구소]삼성전자MX_비개발자_하네스엔지니어링_발표덱_가로.pdf | 발표덱 (가로) | 2026-08-10 | [열기](https://drive.google.com/file/d/1br1l2vWae8M8iXxhKXOaJoswjEstoXCJ/view) |
| [모두의연구소] 삼성MX사업부(수원신규)_BIZ25-1054_견적서_260813_7시간.pdf | 견적서 v2 (7H · ₩5,115,000) | 2026-08-14 | [열기](https://drive.google.com/file/d/14hvUaJTxJZqH8wCldmUsWBvuaG3Onu_J/view) |
| [모두의연구소] 삼성MX사업부(수원신규)_BIZ25-1054_견적서_260803.pdf | 견적서 v1 (8H · ₩5,665,000) | 2026-08-03 | [열기](https://drive.google.com/file/d/1zuwqYkFv10qaqcc89Z98ZRmQdVJ8ocLD/view) |
| [모두의연구소] 삼성MX사업부(수원신규)_BIZ25-1054_견적서_260803[49].pdf | 견적서 v1 사본 | 2026-08-10 | [열기](https://drive.google.com/file/d/1PeGTcNVyuKQuNKD-dsNRfzw9V2sfFjQV/view) |
| [비즈] 삼성MX사업부(수원신규)_비개발자AI교육_마스터 시트 | 비즈팀 마스터 시트 | 2026-08-18 갱신 | [열기](https://docs.google.com/spreadsheets/d/1D8zO3XOI3QJg8mHc8ZetRUd_GjrE5updP5aaCl6Duio/edit) |

## 정리용 사본 폴더

**`2608 삼성전자MX 비개발자 대상 하네스엔지니어링`** (2026-08-18 생성, 발표덱 사본 1건)
→ https://drive.google.com/drive/folders/1MWjS0iGQ-ESO1R0rFOGBXR5keFVt8MKi

## 폴더 안의 실행 자료 (Drive 아님 · 2026-08-18 통합)

| 위치 | 내용 |
|---|---|
| `파일럿_실행자료/...커리큘럼_석진희 강사님 (1).docx` | 파일럿 상세 커리큘럼 (8/21 · 7교시 · 석진희 강사) |
| `파일럿_실행자료/MX-harness-kit.zip` + `MX-harness/` | 수강생 배포 실습 키트와 해제본 |
| `파일럿_실행자료/클로드 코드 자동 환경 설치_WINDOWS.txt` | Windows 환경 자동 점검·설치 배치 |
| `파일럿_실행자료/Windows 환경 설치 안내서.html` | 수강생 배포용 설치 안내서 |
| `교육생_배포물/...01_내_업무_정의서.docx` 외 2종 | 교육생 배포물 3종 (+ `build_0*.py`·`_kit.py` 생성 스크립트) |
| `발표덱_가로/...발표덱_가로.pdf` | 발표덱 PDF (Drive 사본과 동일 · gitignore 대상) |

## 리포 ↔ Drive 대응

| Drive 산출물 | 리포 내 편집 가능 원본 | 상태 |
|---|---|---|
| 종합제안서 PDF | `제안서/content.json` → `proposal_render.html` | ✅ 복원 완료 (재빌드 시 15p 일치) |
| 발표덱 가로 PDF | (없음) | ❌ 소실 — 필요 시 `/proposal-deck-landscape` 스킬로 content.json에서 재생성 |
| 견적서 PDF 2버전 | `..._견적서.md` / `.csv` | ✅ 전문 복원 |
| 요구조건 원본 | `요구조건.md` | ⚠️ 역복원 (원본 문구 아님) |
