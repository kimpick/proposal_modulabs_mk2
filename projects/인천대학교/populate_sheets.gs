/**
 * 인천대학교 바이브코딩 3개 탭 데이터 입력 스크립트
 * 인천대_입문, 인천대_캠프, 인천대_해커톤
 */
function populateIncheonTabs() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // ============================================
  // 1. 인천대_입문 (바이브코딩 입문 6H)
  // ============================================
  var sheet1 = ss.getSheetByName('인천대_입문');
  if (sheet1) {
    sheet1.getRange('B5').setValue('인천대학교 바이브코딩 입문');
    sheet1.getRange('B7').setValue('학부생 대상 AI 코딩 체험 프로그램');
    sheet1.getRange('B9').setValue('바이브코딩 · 프롬프트 엔지니어링 · AI 코딩\n프로토타이핑 · 캡스톤 디자인');
    sheet1.getRange('E9').setValue('1단계 (AI 리터러시)');
    sheet1.getRange('B10').setValue('비전공자 1학년 (동북아국제통상물류학부 등)');
    sheet1.getRange('E10').setValue('총 6시간 (3시간 × 2회)');
    sheet1.getRange('B14').setValue('본 프로그램은 인천대학교 학부생(비전공자)을 대상으로 자연어로 코드를 생성하는 \'바이브코딩\'을 체험하는 입문 과정입니다. 코딩 경험이 없어도 AI 도구를 활용해 웹 페이지를 만들고, 데이터를 분석하고, 프로토타입을 완성할 수 있습니다. Google AI Studio, v0, ChatGPT 등 무료 도구만으로 프롬프트 작성부터 바이브코딩 실습까지 진행하며, 가을학기 캡스톤 디자인과 연계하여 AI 기반 프로젝트 주제를 탐색합니다.');
    sheet1.getRange('B18').setValue('1. 바이브코딩 개념 이해 — 자연어로 AI에게 코딩을 지시하는 방식의 원리와 가능성 체득\n2. 프롬프트 작성 기초 — 효과적인 프롬프트 작성법을 통해 AI 응답 품질을 개선하는 능력 배양\n3. 바이브코딩 실습 — AI 도구로 웹 프로토타입, 데이터 분석, 콘텐츠 생성을 직접 체험\n4. 캡스톤 디자인 연계 — 바이브코딩을 활용한 프로젝트 아이디어 발굴, 팀별 실행 계획 수립');
    sheet1.getRange('B20').setValue('Google AI Studio, v0, ChatGPT');
    sheet1.getRange('E20').setValue('참여자 개인 노트북 지참 (실습 환경)\nWi-Fi 및 인터넷 접속 환경\nGoogle AI Studio 무료 계정 사전 가입\nChatGPT 무료 계정 사전 가입\n빔프로젝터 및 강의실 환경 (대학 측 제공)');
    
    // 상세 커리큘럼 - Row 29~
    sheet1.getRange('B29').setValue('바이브코딩 입문 커리큘럼');
    
    // 모듈 1: Row 31~
    sheet1.getRange('B31').setValue('AI와 대화하는 코딩: 프롬프트 엔지니어링');
    sheet1.getRange('E31').setValue('3시간');
    sheet1.getRange('B32').setValue('바이브코딩이란? — 자연어로 AI에게 코딩을 지시하는 새로운 개발 방식, 코딩 경험 없이도 만들 수 있는 것들');
    sheet1.getRange('B33').setValue('생성형 AI 트렌드 — LLM 작동 원리, ChatGPT·Claude·Gemini 비교, AI가 바꾸는 산업과 직업');
    sheet1.getRange('B34').setValue('프롬프트 작성 기초 — 역할 부여, 구조화된 프롬프트, 예시 기반 작성법(Few-shot), 할루시네이션 대응');
    sheet1.getRange('B35').setValue('Google AI Studio 실습 — Gemini 모델 체험, 프롬프트 실험실, 다양한 모델 응답 비교');
    sheet1.getRange('B36').setValue('ChatGPT로 바이브코딩 체험 — 리포트 개요 생성, 요약·번역·교정, 발표 자료 초안 작성');
    sheet1.getRange('B37').setValue('프롬프트 개선 워크숍 — 참여자가 직접 프롬프트 작성→실행→개선 반복, 품질 비교 및 토론');
    
    // 모듈 2: Row 39~
    sheet1.getRange('B39').setValue('바이브코딩 실습: 아이디어를 프로토타입으로');
    sheet1.getRange('E39').setValue('3시간');
    sheet1.getRange('B40').setValue('v0로 웹 프로토타입 제작 — 프롬프트만으로 웹 페이지 생성, UI 컴포넌트 조합, 반복 개선 실습');
    sheet1.getRange('B41').setValue('Google AI Studio로 데이터 분석 — 스프레드시트 데이터 AI 분석, 시각화 자동 생성 체험');
    sheet1.getRange('B42').setValue('바이브코딩으로 문제 해결 — 전공 관련 과제(물류, 통상 등)에 바이브코딩 적용 시나리오 설계');
    sheet1.getRange('B43').setValue('캡스톤 디자인 주제 탐색 — 바이브코딩 기반 프로젝트 아이디어 발굴, 팀별 주제 선정');
    sheet1.getRange('B44').setValue('프로토타입 시연 — 각 팀이 v0나 ChatGPT로 만든 프로토타입 발표, 피드백 공유');
    sheet1.getRange('B45').setValue('향후 개발 로드맵 — 프로젝트 실행 계획, AI 도구 지속 활용 방안, 학기 중 자습 가이드');
    
    // 예상 산출물
    sheet1.getRange('B48').setValue('바이브코딩 체험 결과물: 참여자가 직접 만든 웹 프로토타입\n캡스톤 프로젝트 기획서: 바이브코딩 기반 프로젝트 주제 및 실행 계획\n프롬프트 엔지니어링 실습 결과: 작성 프롬프트와 개선 과정 기록\n전 과정 수료증 발급');
  }
  
  // ============================================
  // 2. 인천대_캠프 (바이브코딩 캠프 18H)
  // ============================================
  var sheet2 = ss.getSheetByName('인천대_캠프');
  if (sheet2) {
    sheet2.getRange('B5').setValue('인천대학교 바이브코딩 캠프');
    sheet2.getRange('B7').setValue('AI 엔지니어링부터 풀스택 개발까지, 바이브코딩으로 앱 하나 완성하기');
    sheet2.getRange('B9').setValue('바이브코딩 · AI 엔지니어링 · 풀스택 개발\n프론트엔드 · 백엔드 · 데이터베이스 · 보안');
    sheet2.getRange('E9').setValue('2단계 (실무 적용)');
    sheet2.getRange('B10').setValue('대학원생 (전공 무관)');
    sheet2.getRange('E10').setValue('총 18시간 (6시간 × 3일)');
    sheet2.getRange('B14').setValue('본 프로그램은 인천대학교 대학원생을 대상으로 바이브코딩으로 실제 애플리케이션 하나를 완성하는 집중 캠프입니다. Part 1에서는 AI 엔지니어링 기초(프롬프트·컨텍스트·하네스 엔지니어링)를 다져 바이브코딩의 효율을 극대화하고, Part 2에서는 개발 레이어를 하나씩 쌓아가며 풀스택 앱을 완성합니다. AI 활용 핵심 기능부터 프론트엔드, 백엔드, 데이터베이스, 보안까지 전 과정을 바이브코딩으로 진행하여, 코딩 경험이 없어도 완성된 앱을 만들 수 있습니다.');
    sheet2.getRange('B18').setValue('1. AI 엔지니어링 기초 — 프롬프트·컨텍스트·하네스 엔지니어링을 통해 바이브코딩의 효율을 극대화하는 기법 습득\n2. 바이브코딩 풀스택 개발 — 프론트엔드, 백엔드, 데이터베이스, 보안 레이어를 바이브코딩으로 구현\n3. LangChain 실무 연계 — PromptTemplate, Agent 등 LangChain 핵심 컴포넌트 체험\n4. CLI 기반 AI 코딩 — OpenCode + GLM API로 터미널 환경 AI 코딩 경험\n5. 완성된 앱 배포 — 3일간 구축한 풀스택 앱을 실제 배포까지 경험');
    sheet2.getRange('B20').setValue('Google AI Studio, Cursor, Antigravity, Perplexity, OpenCode, GLM API, n8n');
    sheet2.getRange('E20').setValue('참여자 개인 노트북 지참 (실습 환경)\nWi-Fi 및 인터넷 접속 환경\nGoogle AI Studio 무료 계정 사전 가입\nCursor 무료 계정 사전 설치\nGLM API 계정 사전 가입 (Coding Plan Lite, $3/월)\nOpenCode 사전 설치 (오픈소스 CLI)\nPython 3.10+ 설치 (LangChain 실습용)\n빔프로젝터 및 강의실 환경 (대학 측 제공)');
    
    // 상세 커리큘럼
    sheet2.getRange('B29').setValue('바이브코딩 캠프: AI 엔지니어링 + 풀스택 개발');
    
    // Day 1 Part 1: Row 31~
    sheet2.getRange('B31').setValue('Day 1 Part 1: 프롬프트 엔지니어링 심화');
    sheet2.getRange('E31').setValue('3시간');
    sheet2.getRange('B32').setValue('바이브코딩과 AI 엔지니어링 — 바이브코딩의 한계를 넘는 AI 엔지니어링의 3단계(프롬프트→컨텍스트→하네스) 개요');
    sheet2.getRange('B33').setValue('Chain-of-Thought와 Few-shot — 단계별 추론 유도(CoT), 예시 기반 학습 설계, 구조화된 출력 제어(JSON Mode)');
    sheet2.getRange('B34').setValue('고급 프롬프트 설계 실습 — Google AI Studio + Cursor로 프롬프트 작성→검증→최적화 반복, 페르소나 설계');
    sheet2.getRange('B35').setValue('멀티 에이전트 프롬프팅 — 역할 분담 기반 다중 AI 협업, 토론·비평·개선 루프, 프롬프트 품질 관리');
    sheet2.getRange('B36').setValue('LangChain PromptTemplate — ChatPromptTemplate, FewShotChatMessagePromptTemplate으로 재사용 가능한 템플릿 작성');
    sheet2.getRange('B37').setValue('바이브코딩 프롬프트 전략 — 개발 태스크(프론트/백/DB)에 최적화된 프롬프트 패턴 정리');
    
    // Day 1 Part 2: Row 39~
    sheet2.getRange('B39').setValue('Day 1 Part 2: 컨텍스트 & 하네스 엔지니어링');
    sheet2.getRange('E39').setValue('3시간');
    sheet2.getRange('B40').setValue('컨텍스트 엔지니어링 — 컨텍스트 윈도우 이해, RAG(검색 증강 생성) 기초, ReAct 패턴(Thought→Action→Observation)');
    sheet2.getRange('B41').setValue('LangChain 실습 — OutputParser(JsonOutputParser, PydanticOutputParser), Tool Calling Agent 기본 체험');
    sheet2.getRange('B42').setValue('하네스 엔지니어링 기초 — AI 워크플로우 자동화 원리, 에이전트 아키텍처, 도구 통합 패턴');
    sheet2.getRange('B43').setValue('CLI 코딩 환경 입문 — OpenCode 설치, GLM API 연동, 터미널에서 AI 코딩 첫 체험');
    sheet2.getRange('B44').setValue('n8n 자동화 체험 — 노코드 자동화로 AI API 연동 파이프라인 구축, 반복 업무 자동화 실습');
    sheet2.getRange('B45').setValue('Day 1 정리: AI 엔지니어링 툴킷 확보 — 학습한 기법으로 개발 프로젝트에 즉시 활용 가능한 프롬프트·컨텍스트 도구 정리');
    
    // Day 2 Part 1: Row 47~
    sheet2.getRange('B47').setValue('Day 2 Part 1: AI 활용 핵심 기능 + 프론트엔드');
    sheet2.getRange('E47').setValue('3시간');
    sheet2.getRange('B48').setValue('바이브코딩 개발 레이어 개요 — AI 핵심기능→프론트엔드→백엔드→DB→보안, 레이어별 역할과 바이브코딩 전략');
    sheet2.getRange('B49').setValue('AI 핵심 기능 구현 — 바이브코딩으로 챗봇 API 연동, 텍스트 생성/요약, 이미지 처리 기능 구현');
    sheet2.getRange('B50').setValue('LangChain으로 AI 파이프라인 — Sequential Chains로 다단계 AI 처리, AgentExecutor로 도구 통합 에이전트 구축');
    sheet2.getRange('B51').setValue('프론트엔드 바이브코딩 — v0와 Cursor로 UI 컴포넌트 생성, 반응형 레이아웃, 사용자 인터페이스 설계');
    sheet2.getRange('B52').setValue('프론트엔드-백엔드 연동 설계 — API 호출 구조 설계, 상태 관리 기초, 데이터 흐름 기획');
    sheet2.getRange('B53').setValue('프로토타입 v1 완성 — AI 기능이 탑재된 프론트엔드 프로토타입을 바이브코딩으로 완성');
    
    // Day 2 Part 2: Row 55~
    sheet2.getRange('B55').setValue('Day 2 Part 2: 백엔드 개발');
    sheet2.getRange('E55').setValue('3시간');
    sheet2.getRange('B56').setValue('백엔드 바이브코딩 — Cursor와 OpenCode로 서버/API 엔드포인트 생성, REST API 설계 기초');
    sheet2.getRange('B57').setValue('API 라우팅과 비즈니스 로직 — 바이브코딩으로 CRUD 엔드포인트 구현, 데이터 처리 로직 작성');
    sheet2.getRange('B58').setValue('AI API 연동 — GLM API와 OpenAI API를 백엔드에 통합, 프롬프트 체인을 API로 노출');
    sheet2.getRange('B59').setValue('인증 기초 — 바이브코딩으로 기본 로그인/회원가입 기능 구현, JWT 토큰 개념');
    sheet2.getRange('B60').setValue('에러 처리와 로깅 — 바이브코딩으로 예외 처리, API 에러 응답, 로깅 설정');
    sheet2.getRange('B61').setValue('프론트엔드-백엔드 통합 — Day 2 Part 1에서 만든 프론트엔드와 백엔드를 연동하여 동작하는 앱 완성');
    
    // Day 3 Part 1: Row 63~
    sheet2.getRange('B63').setValue('Day 3 Part 1: 데이터베이스 + 보안');
    sheet2.getRange('E63').setValue('3시간');
    sheet2.getRange('B64').setValue('데이터베이스 바이브코딩 — 바이브코딩으로 DB 스키마 설계, 테이블 생성, CRUD 쿼리 작성');
    sheet2.getRange('B65').setValue('ORM과 데이터 모델링 — 바이브코딩으로 ORM 모델 정의, 관계 설정, 마이그레이션 실행');
    sheet2.getRange('B66').setValue('백엔드-DB 연동 — API 엔드포인트에 DB 연동, 데이터 영속성 확보');
    sheet2.getRange('B67').setValue('보안 기본 — API 키 관리, 환경 변수 설정, 입력 검증(Validation), SQL 인젝션 방지 기초');
    sheet2.getRange('B68').setValue('인증/인가 보안 — 비밀번호 해싱, 세션 관리, 권한 제어 기초를 바이브코딩으로 구현');
    sheet2.getRange('B69').setValue('배포 준비 — 환경 변수 정리, 프로덕션 설정, 배포 플랫폼(Vercel/Render) 선택');
    
    // Day 3 Part 2: Row 71~
    sheet2.getRange('B71').setValue('Day 3 Part 2: 종합 풀스택 프로젝트');
    sheet2.getRange('E71').setValue('3시간');
    sheet2.getRange('B72').setValue('풀스택 앱 완성 — 프론트엔드 + 백엔드 + DB + 보안이 통합된 바이브코딩 앱 최종 완성');
    sheet2.getRange('B73').setValue('AI 기능 고도화 — Day 1에서 학습한 AI 엔지니어링 기법(CoT, RAG, Agent)을 앱에 통합');
    sheet2.getRange('B74').setValue('테스트와 디버깅 — 바이브코딩으로 테스트 코드 생성, 버그 수정, 성능 개선');
    sheet2.getRange('B75').setValue('배포 실습 — 완성된 앱을 실제 클라우드에 배포, 공개 URL 확보');
    sheet2.getRange('B76').setValue('팀별 발표 — 각 팀이 완성한 풀스택 바이브코딩 앱 시연, 개발 과정과 AI 활용 전략 발표');
    sheet2.getRange('B77').setValue('회고와 다음 단계 — 바이브코딩 경험 공유, 해커톤 준비 방안, 지속 개발 로드맵 수립');
    
    // 예상 산출물
    sheet2.getRange('B80').setValue('완성된 풀스택 앱: 프론트엔드+백엔드+DB+보안이 통합된 바이브코딩 앱\nAI 엔지니어링 설계서: 프롬프트·컨텍스트·하네스 엔지니어링 적용 결과물\n배포된 앱 URL: 클라우드에 배포된 실제 동작 앱\n팀별 발표 자료: 개발 과정, AI 활용 전략, 회고 정리\n전 과정 수료증 발급');
  }
  
  // ============================================
  // 3. 인천대_해커톤 (바이브코딩 해커톤 8H)
  // ============================================
  var sheet3 = ss.getSheetByName('인천대_해커톤');
  if (sheet3) {
    sheet3.getRange('B5').setValue('인천대학교 바이브코딩 해커톤');
    sheet3.getRange('B7').setValue('물류·AI 융합 바이브코딩 해커톤 운영 위탁');
    sheet3.getRange('B9').setValue('바이브코딩 · 해커톤 · 물류 AI\n프로토타이핑 · 풀스택 · 팀 프로젝트');
    sheet3.getRange('E9').setValue('2단계 (실무 적용)');
    sheet3.getRange('B10').setValue('대학원생 해커톤 + 학부생 아이디어톤 (총 30명 이하)');
    sheet3.getRange('E10').setValue('1일 (총 8시간)');
    sheet3.getRange('B14').setValue('본 프로그램은 인천대학교 학부생과 대학원생이 팀을 구성하여 물류·AI 융합 주제로 바이브코딩으로 애플리케이션을 기획하고 프로토타입을 개발하는 1일 해커톤입니다. 앞선 바이브코딩 입문과 캠프에서 습득한 AI 도구 활용 능력을 실전에 적용하여, 제한 시간 안에 작동하는 앱을 완성합니다. 모두의연구소가 기획·운영·심사·결과보고 전 과정을 위탁 수행합니다.');
    sheet3.getRange('B18').setValue('1. 바이브코딩 실전 프로젝트 — 학습한 AI 도구를 활용해 실제 문제(물류·AI 융합)에 대한 솔루션을 바이브코딩으로 기획·개발\n2. 풀스택 프로토타이핑 — 프론트엔드+백엔드+DB를 바이브코딩으로 제한 시간 내 프로토타입 제작\n3. 팀 협업 역량 — 팀 기반 프로젝트 수행, 역할 분담, 협업 도구 활용 능력 함양\n4. 발표 및 소통 역량 — 팀별 결과 발표, 심사위원 피드백 수용, 아이디어 소통 능력 배양');
    sheet3.getRange('B20').setValue('Google AI Studio, Cursor, Antigravity, v0, OpenCode, GLM API, Perplexity');
    sheet3.getRange('E20').setValue('참여자 개인 노트북 지참 (실습 환경)\nWi-Fi 및 인터넷 접속 환경 (인천대학교 강의실)\n사전 학습 도구 설치 완료 (입문·캠프 참여자)\n빔프로젝터 및 강의실 환경 (대학 측 제공)\n해커톤 운영 물품 (상장, 간식 등 — 모두의연구소 준비)');
    
    // 상세 커리큘럼
    sheet3.getRange('B29').setValue('바이브코딩 해커톤 진행 일정');
    
    // 해커톤 모듈: Row 31~
    sheet3.getRange('B31').setValue('해커톤 진행');
    sheet3.getRange('E31').setValue('8시간');
    sheet3.getRange('B32').setValue('오리엔테이션 및 팀 빌딩 (09:00–09:50) — 해커톤 규칙 안내, 팀 구성(3-4인 1조), 심사 기준 설명, 아이스브레이킹');
    sheet3.getRange('B33').setValue('주제 소개와 바이브코딩 리캡 (09:50–10:40) — 물류·AI 융합 주제 발표, 바이브코딩 개발 전략 요약, 실습 환경 최종 확인');
    sheet3.getRange('B34').setValue('바이브코딩 부스터 세션 (10:40–11:30) — 풀스택 바이브코딩 워크플로우 리뷰, CLI(OpenCode) 활용 팁, Q&A');
    sheet3.getRange('B35').setValue('아이디어 발굴 및 기획 (11:30–12:30) — 팀별 문제 정의, 바이브코딩으로 구현 가능한 AI 솔루션 설계, 기획서 작성');
    sheet3.getRange('B36').setValue('바이브코딩 개발 ① (13:30–15:00) — 프론트엔드+백엔드 바이브코딩, AI 기능 통합, 멘토링 순회 지도');
    sheet3.getRange('B37').setValue('바이브코딩 개발 ② (15:00–16:00) — DB 연동+보안 설정, UI 개선, 발표 자료 준비, 멘토 피드백 반영');
    sheet3.getRange('B38').setValue('팀별 결과 발표 (16:00–17:10) — 팀별 7분 발표 + 3분 질의응답, 작동하는 앱 시연, 심사위원 평가');
    sheet3.getRange('B39').setValue('심사·시상 및 네트워킹 (17:10–18:00) — 심사위원 종합 평가, 시상(최우수상, 우수상, 아이디어상), 참가자 네트워킹');
    
    // 예상 산출물
    sheet3.getRange('B42').setValue('해커톤 결과 보고서: 대학 측 제출용 종합 결과 보고\n팀별 바이브코딩 앱: 시연 가능한 풀스택 AI 솔루션 프로토타입\n수상작 포트폴리오: 최우수/우수/아이디어상 수상작 상세\n참가자 전원 수료증: 해커톤 참여 증명');
  }
  
  SpreadsheetApp.getUi().alert('인천대학교 3개 탭 데이터 입력 완료!');
}
