# /review — Compliance Reviewer (mk2 추가 · 5번째 리뷰어)

> 원본(영광님 repo)의 4리뷰어(Flow·Recency·Tone·Readability)에 더해, mk2는 **강사·내부정보 컴플라이언스**를 5번째 관점으로 검토한다.
> 결정적으로 잡을 수 있는 항목은 `scripts/validate_content.py`의 `validate_compliance()`가 API 비용 없이 사전 차단하고, 이 문서는 그 위에서 LLM이 맥락으로 보는 관점을 정의한다.

## Compliance Reviewer

**검토 관점**: 고객 제출본에 나가면 안 되는 정보(개인정보·내부정보)와, 강사·타 고객사 노출 정책 준수.

**공통 출력 형식**: 다른 리뷰어와 동일한 JSON(`reviewer/verdict/findings[]/summary`).

**중점 질문**

1. `instructors[].name`이 모두 마스킹됐는가? (예: 홍길동 → 홍*동, 4글자 이상은 가운데 전부)
2. 강사 카드(bio·experience·metrics 등)에 **연락처·이메일·주소·생년월일** 등 개인정보가 없는가?
3. 강사 카드에 **강의료·단가·시간당 금액** 등 내부 단가가 없는가? (견적은 별도 견적서)
4. 강사 우선순위/적합도 등급/"컨택 필요" 같은 **내부 매칭 메모**가 흘러 들어가지 않았는가?
5. `schedule_message`·`section_07_title`에 **협의 이력('수정사항 반영')**이 최종본에 남아 있지 않은가? (반영 결과는 커리큘럼 본문에 녹이고 섹션은 제거)
6. 강사 이력의 **타 고객사명** 노출이 정책에 맞는가? (설득 근거로 실명 노출은 허용하되, 경쟁사 민감 건이면 업종/기관유형으로 순화할지 사용자 판단)

**판정 기준**

| 조건 | severity |
|---|---|
| 실명 미마스킹, 개인정보(연락처·이메일) 노출, 내부 메모 유출 | FIX |
| 강의료/단가 표현, 협의 이력 잔존, 타 고객사명 노출 정책 확인 필요 | WARN |
| 순화 표현 제안, 표기 통일 | INFO |

**결정적 사전검증(로컬)**: `PYTHONIOENCODING=utf-8 python3 scripts/validate_content.py {기업명}/{제안서}` 가 1·2·3·5번의 명백한 위반을 FIX/WARN으로 먼저 잡는다. LLM 리뷰어는 4·6번처럼 맥락 판단이 필요한 부분을 보완한다.

## 종합 판정 반영

메인 에이전트는 기존 4리뷰어 + Compliance Reviewer + `validate_content.py` 결과를 합쳐 판정한다. 판정 규칙(FIX 1개 이상 또는 WARN 3개 이상 → NEEDS_FIX)은 원본과 동일.

> ⚠️ 컴플라이언스 FIX(실명·개인정보)는 **사업 판단(WARN 허용) 대상이 아니다.** 고객 제출 전 반드시 제거한다.
