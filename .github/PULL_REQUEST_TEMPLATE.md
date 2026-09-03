<!--
PR 템플릿 — 자동 PR(git_workflow.py finish)에는 사용되지 않습니다.
이 템플릿은 수동 PR(시스템 변경, 긴급 수정 등)에만 표시됩니다.
기업 제안서 PR은 scripts/git_workflow.py가 자동으로 본문을 생성합니다.
-->

## 📝 변경 유형

<!-- 해당하는 항목에 [x] 표시 -->

- [ ] 🏢 기업 제안서 (setup/build/estimate)
- [ ] 🔧 시스템/스크립트 변경 (build.py, git_workflow.py 등)
- [ ] 📚 문서/가이드 (AGENTS.md, docs/)
- [ ] 🎨 템플릿/CSS (templates/)
- [ ] 🐛 버그 수정
- [ ] 🔥 긴급 핫픽스

## 📋 변경 요약

<!-- 무엇을, 왜 변경했는지 1-3줄 -->

-

## 🔗 관련 링크

- **기업명**: 
- **작업자**: 
- **Slack 명령**: (예: /setup 삼성전자)
- **Google Drive**: 
- **Slack thread**: 

## ✅ 체크리스트

### 기업 제안서 PR인 경우
- [ ] `python scripts/validate_content.py <기업명>` PASS
- [ ] `python build.py <기업명> --no-drive-upload` 빌드 성공
- [ ] 도구 일관성 (`tech_stack` ↔ `tracks[].tools` ↔ `modules[].items`)
- [ ] PDF가 정상 생성됨 (로컬에서 확인)
- [ ] 버전 스냅샷이 저장됨 (자동)

### 시스템/스크립트 변경인 경우
- [ ] 로컬 테스트 완료
- [ ] AGENTS.md 가이드와 일치 (해당 시)
- [ ] 기존 워크플로우 호환성 확인

### 공통
- [ ] `main` 브랜치에 직접 push 하지 않음 (PR 워크플로우 준수)
- [ ] 한글 파일명 인코딩 문제 없음 (NFC 정규화)
- [ ] 민감정보(.env, 토큰) 포함하지 않음

## ⚠️ 특이사항

<!-- 충돌, 강제 push, 롤백 필요 등 특이사항이 있으면 기재 -->

-

## 🧪 테스트 방법

<!-- 리뷰어가 변경사항을 검증할 수 있는 방법 -->

```bash
# 예: python scripts/validate_content.py 삼성전자
# 예: python build.py 삼성전자 --no-drive-upload
```
