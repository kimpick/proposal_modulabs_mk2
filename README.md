# 📘 모두의연구소 AI 교육 제안서 빌더

기업 맞춤형 AI 교육 제안서를 **`content.json` 하나만 작성**하면 자동으로 PDF를 생성하는 템플릿 프로젝트입니다.

---

## 🚀 처음 시작하기 (최초 1회)

### 1단계: 이 프로젝트 클론하기
```bash
git clone https://github.com/kisdevan/propsal_modulabs.git
cd propsal_modulabs
```

### 2단계: Python 패키지 설치
```bash
pip install jinja2
```
> 💡 `jinja2`는 HTML 템플릿 엔진입니다. Python 3.8 이상이면 됩니다.

### 3단계: 잘 되는지 확인 (기존 예시로 테스트)
```bash
python build.py 기웅정보통신
```
`projects/기웅정보통신/` 하위 폴더마다 **PDF**가 생성되면 성공! ✅

---

## 📝 새 기업 제안서 만들기 (Step-by-Step)

### STEP 1. 기업 폴더 만들기

`projects/` 아래에 **기업명** 폴더, 그 안에 **과정명** 폴더를 만듭니다.

```
projects/
└── <기업명>/                    ← 예: "삼성전자"
    └── <과정명>/                ← 예: "직무별_AI_활용_교육안"
```

**터미널에서:**
```bash
mkdir -p projects/삼성전자/직무별_AI_활용_교육안
```

> 💡 과정명 폴더는 여러 개 만들 수 있습니다. 예를 들어:
> ```
> projects/삼성전자/
> ├── 전체_교육_로드맵/
> ├── 직무별_AI_활용_교육안/
> └── 개발자_AI_기초_교육안/
> ```

---

### STEP 2. 어떤 제안서 타입인지 결정하기

제안서에는 **4가지 타입**이 있습니다. 각 타입마다 `content.json` 구조가 다릅니다.

| 타입 | 언제 사용하나요? | 스키마 예시 파일 |
|------|----------------|-----------------|
| **roadmap** | 전체 교육 로드맵 (연간 계획 포함) | `schemas/roadmap.example.json` |
| **track** | 직무별 워크샵 (트랙별 모듈) | `schemas/track.example.json` |
| **module** | 개발자/IT 과정 (단일 모듈 목록) | `schemas/module.example.json` |
| **khp-seminar** | **[K-HP] 기업교육 세미나 전용** | `schemas/khp-seminar.example.json` |

> 💡 **타입 판별 기준**: `build.py`가 `content.json` 안의 특정 키를 보고 자동 판별합니다.
> - `"steps"` 키가 있으면 → **roadmap**
> - `"tracks"` 키가 있으면 → **track**
> - `"seminars"` 키가 있으면 → **khp-seminar** (K-HP 사업 전용)
> - `"modules"` 키가 있으면 → **module**

---

### STEP 3. content.json 작성하기

1. **스키마 예시 파일 복사**
   ```bash
   # 예: track 타입 제안서를 만들 경우
   cp schemas/track.example.json projects/삼성전자/직무별_AI_활용_교육안/content.json
   ```

2. **복사한 `content.json`을 에디터로 열어 내용 수정**

   각 항목의 의미를 아래에서 설명합니다.

#### 📋 공통 항목 (모든 타입에 있음)

```jsonc
{
  "title": "삼성전자 직무별 맞춤형 AI 활용 워크샵",    // 제안서 제목 (큰 글씨)
  "subtitle": "한 줄 요약 설명",                     // 부제목

  "info": {
    "keyword": "직무별 실무 AI 활용",                 // 좌측 상단 키워드 뱃지
    "ax_stage": "2단계 (실무 적용)",                  // AX 단계 표시
    "target": "비IT 직무 임직원",                     // 대상
    "duration": "직군별 1일 (7시간)"                  // 기간
  },

  "intro": "과정 소개 상세 서술...",                  // 01 과정 소개 텍스트
  "objective": "교육 목표 요약...",                   // 02 교육 목표 텍스트

  "tech_stack": ["Claude", "Make", "GPT"],           // 03 핵심 기술 뱃지들
  "infrastructure": [                                // 04 필요 인프라 목록
    "인프라 항목 1",
    "인프라 항목 2"
  ],

  "output": "<ul><li>산출물 항목</li></ul>"           // 산출물 (HTML 가능)
}
```

#### 📋 타입별 추가 항목

<details>
<summary><b>🗺️ roadmap 타입</b> (전체 교육 로드맵)</summary>

```jsonc
{
  // ... 공통 항목 ...
  
  "steps": [                           // STEP 카드 목록
    {
      "step_name": "전사 기초 AI 리터러시 (인식 전환)",
      "duration": "2H",
      "items": [                       // ⚠️ 키 이름은 반드시 "items"
        "과정 소개: ...",
        "교육 목표: ...",
        "핵심 기술: ..."
      ]
    }
    // ... 더 많은 step ...
  ],

  "annual_plan": [                     // 연간 계획 테이블 (선택)
    {
      "month": "4월",
      "title": "도입 및 기초 셋업",
      "non_it": "비IT 내용",
      "it": "IT 내용"
    }
  ]
}
```
</details>

<details>
<summary><b>👥 track 타입</b> (직무별 워크샵)</summary>

```jsonc
{
  // ... 공통 항목 ...

  "tracks": [                          // 직군별 트랙 목록
    {
      "track_id": "01",
      "track_name": "영업 및 마케팅 직군",
      "course_title": "세일즈 AI 자동화",
      "target": "영업본부, 마케팅 담당자",
      "duration": "1일 (7시간)",
      "tools": ["Claude", "Genspark"],
      "modules": [                     // 해당 트랙의 모듈 목록
        {
          "module_name": "B2B 세일즈 AI 분석",
          "duration": "2H",
          "items": [
            "학습 내용 1",
            "실습: ..."
          ]
        }
      ]
    }
  ],

  "schedule_message": "※ 일정 안내 메시지"
}
```
</details>

<details>
<summary><b>💻 module 타입</b> (개발자/IT 과정)</summary>

```jsonc
{
  // ... 공통 항목 ...

  "modules": [                         // 모듈 목록
    {
      "module_id": "01",
      "module_name": "Claude Code CLI 중심의 바이브코딩",
      "subtitle": "AI 코딩 기초",      // 왼쪽에 작게 표시
      "duration": "1일 (7시간)",
      "items": [
        "학습 내용 1",
        "실습: ..."
      ]
    }
  ],

  "schedule_message": "※ 일정 안내 메시지"
}
```
</details>

<details>
<summary><b>📚 khp-seminar 타입</b> (K-HP 기업교육 세미나 전용)</summary>

```jsonc
{
  // ... 공통 항목 ...

  "seminars": [                        // 추천 세미나 목록
    {
      "step_name": "[AX 전략] AI 시대 B2B 전략 (연사: 홍길동)",
      "duration": "2H",
      "items": [
        "추천 대상: ...",
        "내용: ...",
        "목적: ..."
      ]
    }
  ],

  "new_curriculums": [                 // 기초심화 커리큘럼 추가 제안
    {
      "step_name": "세일즈 AI 리터칭",
      "duration": "4H",
      "items": [
        "추천 이유: ...",
        "주요 활동: ..."
      ]
    }
  ],

  "schedule_message": "※ 일정 안내 메시지"
}
```
</details>

---

### STEP 4. PDF 빌드하기

```bash
# 방법 1: 특정 기업의 특정 과정만 빌드
python build.py 삼성전자/직무별_AI_활용_교육안

# 방법 2: 특정 기업의 모든 과정 한꺼번에 빌드
python build.py 삼성전자

# 방법 3: 전체 프로젝트 (모든 기업) 빌드
python build.py --all
```

빌드하면 해당 과정 폴더 안에 2개 파일이 생깁니다:
```
projects/삼성전자/직무별_AI_활용_교육안/
├── content.json              ← 내가 작성한 원본
├── proposal_render.html      ← 자동 생성 (중간 파일)
└── 직무별_AI_활용_교육안_제안서.pdf   ← ✅ 최종 결과물!
```

---

### STEP 5. GitHub에 올리기

```bash
git add .
git commit -m "feat: 삼성전자 직무별 AI 활용 제안서 추가"
git push
```

---

## ⚡ tmux dev 워크스페이스 (작업 가속화)

content.json 수정 → 자동 빌드 → AI 검토 → Git push를 **하나의 터미널 화면**에서.
`scripts/dev.sh` 가 3-pane 통합 환경을 엽니다.

> 📖 상세 가이드: [`docs/dev_workspace_guide.md`](docs/dev_workspace_guide.md)

### 시작하기

```bash
# 의존성 (최초 1회)
brew install tmux fswatch
pip install jinja2

# 워크스페이스 실행
bash scripts/dev.sh 기웅정보통신
```

### 워크스페이스 구조

```
┌────────────────────────────────────────────────────┐
│ 1 Watcher   content.json 저장 시 자동 PDF 빌드      │
├──────────────────────────┬─────────────────────────┤
│ 2 Hermes chat            │ 3 Status                │
│   AI 커리큘럼 검토/수정   │   validator + 버전 + Git │
│   (GLM-5.2, Sheets MCP)  │                         │
└──────────────────────────┴─────────────────────────┘
```

### 자주 쓰는 단축키 (Ctrl+B prefix)

| 단축키 | 동작 |
|---|---|
| `Ctrl+B` `1`/`2`/`3` | pane 이동 |
| `Ctrl+B` `d` | detach (세션은 백그라운드 유지) |
| `Ctrl+B` `B` | 현재 기업 강제 재빌드 |
| `Ctrl+B` `V` | content.json 재검증 |
| `Ctrl+B` `z` | 현재 pane 전체화면 토글 |

### 세션 관리

```bash
tmux ls                          # 실행 중인 세션 목록
tmux attach -t 기웅정보통신       # 다시 진입
tmux kill-session -t 기웅정보통신 # 완전 종료
```

### Hermes AI 로 할 수 있는 일 (Pane 2)

```
> 이 content.json 4차원 검토해줘 (Flow/Recency/Tone/Readability)
> 모듈 3개 추가해줘, 타겟은 시니어 임원
> 시트 ID 1ABC...xyz 에 견적서 행 추가해줘
```

- 모델: GLM-5.2 via Z.AI Coding Plan (구독 — 크레딧 소진 없음)
- Sheets 연동: [`docs/google_sheets_mcp_setup.md`](docs/google_sheets_mcp_setup.md)

---
---

## 🎨 디자인 수정하고 싶을 때

모든 제안서의 디자인은 `templates/base.css` 한 파일에서 관리됩니다.

| 컬러 변수 | 현재 값 | 역할 |
|-----------|---------|------|
| Primary | `#EE3E4C` | 포인트 컬러 (빨강) |
| Secondary | `#EBBAC0` | 섹션 번호 (라이트 핑크) |
| Border | `#EBEBEB` | 박스 테두리 |
| Text Dark | `#111111` | 제목 텍스트 |
| Text Body | `#333333` | 본문 텍스트 |

CSS를 수정하면 **모든 제안서에 일괄 적용**됩니다.

---

## 📁 전체 프로젝트 구조

```
propsal_modulabs/
├── build.py                    ← 통합 빌드 CLI
├── README.md                   ← 이 가이드
├── .gitignore
├── templates/                  ← 공유 디자인 & HTML 템플릿
│   ├── base.css                   (CSS 디자인 시스템)
│   ├── roadmap.html               (로드맵 타입)
│   ├── track.html                 (직무별 타입)
│   ├── module.html                (개발자 타입)
│   └── khp-seminar.html          (K-HP 세미나 전용)
├── schemas/                    ← content.json 빈 예시
│   ├── roadmap.example.json
│   ├── track.example.json
│   └── module.example.json
└── projects/                   ← 기업별 프로젝트
    └── 기웅정보통신/              (예시 — 5종 포함)
        ├── 전체_교육_로드맵/
        ├── 직무별_AI_활용_교육안/
        ├── 개발자_AI_기초_교육안/
        ├── 개발자_AI_심화_교육안/
        └── 기초_AI_리터러시_제안서/
```

## ⚙️ 요구사항

| 항목 | 요구 |
|------|------|
| Python | 3.8 이상 |
| 패키지 | `jinja2` (`pip install jinja2`) |
| PDF 변환 | Microsoft Edge (Windows 기본 설치) |

---

## ❓ FAQ

**Q. content.json에 HTML 태그를 써도 되나요?**  
A. 네, `output`이나 `schedule_message` 필드에는 `<ul>`, `<li>`, `<b>`, `<br>` 등의 HTML을 직접 사용할 수 있습니다.

**Q. 한 기업에 제안서를 여러 개 만들 수 있나요?**  
A. 네, `projects/<기업명>/` 아래에 폴더를 원하는 만큼 만들고, 각각에 `content.json`을 넣으면 됩니다.

**Q. 디자인을 기업별로 다르게 할 수 있나요?**  
A. 현재는 `base.css` 하나로 전체 통일입니다. 기업별 커스텀이 필요하면 `templates/` 안에 별도 CSS나 HTML을 추가할 수 있습니다.

**Q. PDF가 안 만들어져요.**  
A. Microsoft Edge가 설치되어 있는지 확인해 주세요. Edge의 Headless 모드를 사용하여 PDF를 생성합니다.
