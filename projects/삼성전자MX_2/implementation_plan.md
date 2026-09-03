# 삼성전자 AI 에이전틱 코딩 교육 — 종합 계획 (v3)

## 📐 프로젝트 범위

| 항목 | 내용 |
|---|---|
| **4월** | 수준별 4개 과정 × 8시간 (입문→실전→발전→심화) |
| **5월** | 주제별 8개 과정 × 8시간 (병렬 시리즈) |
| **산출물** | 커리큘럼 콘텐츠(JSON) + 대시보드 웹앱 (PDF 빌드 제외) |
| **보안** | 재택 교육, 보안망 제약 없음 |

---

## 📚 교육 프레임워크

> **arxiv 2505.19443** 「Vibe Coding vs. Agentic Coding」 기반
> - 입문(Vibe Coding) → 심화(Agentic Coding) 점진적 전환 하이브리드 접근

---

## 🔧 핵심 툴 에코시스템

| 툴 | 유형 | 수준 |
|---|---|---|
| **Google AI Studio** | 바이브 코딩 플랫폼 | 입문 |
| **Claude CoWork** | 데스크톱 에이전트 | 입문~실전 |
| **Claude Code + Skills** | 터미널 AI 코딩 | 실전 |
| **OpenCode** | 오픈소스 AI 코딩 (75+ LLM) | 실전~발전 |
| **Cline** | VS Code 자율 에이전트 | 발전 |
| **OpenClaw** | 로컬 AI 어시스턴트 | 발전~심화 |
| **NanoClaw** | 보안 특화 (Docker/MicroVM 격리) | 심화 |

| 리소스 서비스 | 용도 |
|---|---|
| **21st.dev** | shadcn/ui 컴포넌트 레지스트리 |
| **v0 (Vercel)** | 자연어→프로덕션 코드 |
| **Lovable / Bolt** | 노코드 AI 웹/앱 빌더 |

---

## 📅 4월: 수준별 에이전틱 코딩 시리즈 (각 8시간)

### Level 1. 입문 — "AI와 함께 첫 앱 만들기"
| 모듈 | 시간 | 내용 |
|---|---|---|
| Vibe Coding 이해 | 1.5H | Vibe vs Agentic 개념, 에이전틱 AI 생태계 전체 조망 |
| Google AI Studio 실전 | 2.5H | Prompt-to-App, Firebase 연동, 원클릭 배포 실습 |
| Claude CoWork 데스크톱 자동화 | 2H | CoWork 모드 체험, 파일·앱 자동화, 반복 업무 시나리오 |
| 나만의 AI 앱 아이디어 기획 | 2H | Pain Point → 아이디어 → Google AI Studio 프로토타입 + 발표 |
| **도구**: Google AI Studio, Claude CoWork | | |

### Level 2. 실전 — "개발 파이프라인에 AI 심기"
| 모듈 | 시간 | 내용 |
|---|---|---|
| Claude Code CLI 마스터 | 2H | 설치·컨텍스트 주입, 프롬프트 엔지니어링, PRD 기반 코드 생성 |
| Claude Skills 워크플로우 | 2H | Skills(CLAUDE.md) 작성, 코드리뷰·테스트·배포 스킬, 팀 표준 라이브러리 |
| OpenCode 오픈소스 활용 | 2H | TUI/IDE 확장, 멀티 LLM 전환, Git 통합, BYOK 비용 최적화 |
| 파이프라인 자동화 워크샵 | 2H | CI/CD 파이프라인 설계 + 기획서 작성 |
| **도구**: Claude Code, Skills, OpenCode, 21st.dev | | |

### Level 3. 발전 — "자율 에이전트와 협업하기"
| 모듈 | 시간 | 내용 |
|---|---|---|
| Cline 자율 코딩 에이전트 | 2H | VS Code 확장, 자율 실행, 파일·명령·브라우저 제어 |
| OpenClaw 로컬 에이전트 | 2.5H | 설치·보안 설정, MCP 서버 연동, 쉘·파일·브라우저 자동화 |
| 멀티 에이전트 협업 패턴 | 1.5H | Reflection, Planning, Multi-Agent 설계 패턴 |
| 에이전트 파이프라인 워크샵 | 2H | 멀티 에이전트 아키텍처 기획서 + 프로토타입 시연 |
| **도구**: Cline, OpenClaw, v0, 21st.dev | | |

### Level 4. 심화 — "보안·거버넌스·프로덕션"
| 모듈 | 시간 | 내용 |
|---|---|---|
| NanoClaw 보안 특화 에이전트 | 2.5H | Docker/MicroVM 격리, OpenClaw 보안 취약점 사례, 안전한 배포 |
| 프로덕션 거버넌스 | 2H | AI 코드 품질 검증, Supply Chain 보안, DLP, 기업 정책 수립 |
| 엔터프라이즈 아키텍처 | 1.5H | 대규모 오케스트레이션, 모니터링·감사, 비용 최적화 |
| 최종 프로젝트 발표 | 2H | 팀별 에이전트 프로젝트 완성 → 발표 → 실무 로드맵 |
| **도구**: NanoClaw, OpenClaw, Claude Code + Skills | | |

---

## 📅 5월: 주제별 에이전틱 코딩 시리즈 (각 8시간)

> 컨셉: **"에이전틱 코딩으로 ~~~ AI 에이전트 만들기"** 병렬 시리즈

### 1. 업무 자동화 AI 에이전트 만들기
이메일·문서·일정 자동화, 승인 프로세스 자동화, 보고서 자동 생성
→ **도구**: Claude CoWork, OpenClaw, Claude Skills

### 2. 데이터 분석 AI 에이전트 만들기
자연어 데이터 질의, 시각화 대시보드 생성, 인사이트 추출 자동화
→ **도구**: Google AI Studio, v0, Claude Code

### 3. 고객 응대 AI 에이전트 만들기
FAQ 챗봇, 멀티채널 응대, 자동 에스컬레이션, 고객 분류
→ **도구**: Google AI Studio, Bolt, OpenClaw

### 4. 콘텐츠 생성 AI 에이전트 만들기
랜딩페이지·소셜미디어 자동 생성, 다국어 번역, A/B 테스트 자동화
→ **도구**: Lovable, Claude Code + Skills, 21st.dev

### 5. 회의·보고서 AI 에이전트 만들기
회의록 자동 작성·요약, 주간/월간 보고서 자동 생성, 액션아이템 추적
→ **도구**: Claude CoWork, Claude Skills, OpenCode

### 6. 영업·세일즈 AI 에이전트 만들기
리드 분석·스코어링, 제안서 자동 생성, CRM 데이터 정리, 세일즈 시나리오 시뮬레이션
→ **도구**: Claude Code, Google AI Studio, v0

### 7. 사내 지식관리 AI 에이전트 만들기
사내 위키·문서 검색 챗봇, 온보딩 가이드 자동 생성, FAQ 자동 업데이트
→ **도구**: OpenClaw, Claude Skills, Cline

### 8. 프로젝트 관리 AI 에이전트 만들기
태스크 자동 분배·추적, 진행 상황 대시보드 생성, 리스크 감지·알림 자동화
→ **도구**: Claude Code, OpenCode, v0, Bolt

---

## 🖥️ 커리큘럼 대시보드 웹앱

**스택**: Vite + React, 커스텀 CSS (Pretendard, glassmorphism)

| 페이지 | 핵심 기능 |
|---|---|
| 수강신청 (메인) | 시간표 그리드 뷰, 과목 카드 (난이도 뱃지·도구·시작일), 배너 |
| 과목 상세 | 과목정보 (시작일·강사·일정·기간·난이도·도구), 강의 회차, 과제 |
| 내 강의실 | 수강 과목 그리드, 진도율, 학습 요약 |
| 강의 뷰어 | 슬라이드 뷰어, 학습 완료 표시 |

---

## 🚀 세션 실행 전략

> [!TIP]
> **세션 3개를 병렬로 실행하면 가장 효율적입니다**

| 세션 | 작업 | 예상 소요 | 비고 |
|---|---|---|---|
| **세션 A** (현재) | 4월 수준별 4개 과정 커리큘럼 콘텐츠 작성 | ~15분 | context.md + 4개 content.json |
| **세션 B** (새로 시작) | 5월 주제별 8개 과정 커리큘럼 콘텐츠 작성 | ~20분 | 8개 content.json |
| **세션 C** (새로 시작) | 커리큘럼 대시보드 웹앱 개발 | ~30분 | Vite+React 프로젝트 |

### 실행 방법
```
[세션 A — 현재] "4월 수준별 4개 과정 content.json 작성해줘"
[세션 B — 새 창] "5월 주제별 8개 과정 content.json 작성해줘. implementation_plan.md 참고"  
[세션 C — 새 창] "커리큘럼 대시보드 웹앱 만들어줘. implementation_plan.md 참고"
```

> [!IMPORTANT]
> **세션 C(웹앱)는 A·B 완료 후 시작하는 것을 권장** — 웹앱이 커리큘럼 JSON 데이터를 사용하기 때문.
> 또는 세션 C에서 먼저 UI 뼈대를 잡고, A·B 완료 후 데이터를 연결하는 것도 가능합니다.
