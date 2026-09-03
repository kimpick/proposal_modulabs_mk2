# Google Sheets MCP 설정 가이드

Hermes AI 에이전트가 Google Sheets를 직접 읽고 쓸 수 있도록 MCP 서버를 등록.
**모두의연구소 AI 교육 제안서** 프로젝트에서 견적서/리드 관리 자동화에 사용.

---

## 1. 사전 준비 (Google Cloud Console)

### 1.1 GCP 프로젝트 생성
- https://console.cloud.google.com/ → "프로젝트 선택" → "새 프로젝트"
- 이름 예: `modulabs-proposal-bot`

### 1.2 Google Sheets API 활성화
- "API 및 서비스" → "라이브러리" → `Google Sheets API` 검색 → "사용 설정"

### 1.3 Drive API 활성화 (폴더 목록 조회용)
- 동일하게 `Google Drive API` 검색 → "사용 설정"

### 1.4 서비스 계정 생성
- "API 및 서비스" → "사용자 인증 정보" → "사용자 인증 정보 만들기" → "서비스 계정"
- 이름 예: `sheets-bot`
- 역할: 할당 안 함 (권한은 시트 공유로 부여)
- 생성된 서비스 계정 클릭 → "키" 탭 → "키 추가" → JSON → 다운로드

### 1.5 서비스 계정 이메일 확인
- 다운로드한 JSON의 `client_email` 값 (예: `sheets-bot@modulabs-proposal-bot.iam.gserviceaccount.com`)

---

## 2. 서비스 계정 JSON 보관

다운로드한 JSON 파일을 안전한 위치에 저장 (Git 절대 금지):

```bash
mkdir -p ~/.config/gcp
mv ~/Downloads/sheets-bot-xxxxx.json ~/.config/gcp/modulabs-sheets.json
chmod 600 ~/.config/gcp/modulabs-sheets.json
```

> ⚠️ 이 파일은 절대 Git에 커밋하지 마세요. `.gitignore`의 `automation/.env` 와 함께 관리.

---

## 3. Hermes config 업데이트

`~/.hermes/config.yaml` 의 `mcp_servers.google-sheets.env` 블록 수정:

```yaml
mcp_servers:
  google-sheets:
    command: npx
    args:
    - -y
    - mcp-gsheets@latest
    env:
      GOOGLE_APPLICATION_CREDENTIALS: /Users/사용자명/.config/gcp/modulabs-sheets.json
      GOOGLE_PROJECT_ID: modulabs-proposal-bot
    enabled: true   # false → true 로 변경
```

또는 CLI (인터랙티브):

```bash
hermes mcp configure google-sheets
```

---

## 4. 대상 시트를 서비스 계정과 공유

1. https://sheets.google.com 에서 대상 스프레드시트 열기
2. "공유" 버튼 → 1.5에서 확인한 서비스 계정 이메일 입력 → "편집자" 권한 → "전송"

> 💡 폴더 단위 공유 권장 — 새 시트를 만들 때마다 일일이 공유 안 해도 됨.

---

## 5. 연결 테스트

```bash
hermes mcp test google-sheets
```

성공 시:
```
✓ Connected to 'google-sheets'
Tools: list_sheets, read_sheet, write_sheet, ...
```

---

## 6. Hermes 에이전트에서 사용

Pane 4 (Hermes chat)에서 자연어로 호출:

```
> "XXX기업 견적서 시트에서 최근 10행 읽어줘"
> "이 content.json 기반으로 견적서 시트에 새 행 추가해줘"
> "v002 버전 PDF 링크를 마스터 시트에 업데이트"
```

---

## 문제 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| `Connection closed` | env 미설정 또는 JSON 경로 오류 | `~/.hermes/config.yaml` 경로 확인 |
| `Permission denied` on sheet | 서비스 계정에 공유 안 됨 | 시트 "공유"에 서비스 계정 이메일 추가 |
| `API not enabled` | Sheets/Drive API 비활성화 | GCP 콘솔에서 API 활성화 |
| `Project ID mismatch` | JSON의 project_id와 config 불일치 | JSON 파일의 `project_id` 확인 |

---

## 백업 옵션: Python 버전 (mcp-google-sheets)

librarian이 추천한 1순위 `mcp-google-sheets` (Python/uvx) 사용 시:

```bash
# uv 설치 (uvx 포함)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Hermes MCP 교체
hermes mcp remove google-sheets
hermes mcp add google-sheets \
  --command uvx \
  --args mcp-google-sheets@latest \
  --env SERVICE_ACCOUNT_PATH=/Users/사용자명/.config/gcp/modulabs-sheets.json \
  --env DRIVE_FOLDER_ID=shared-folder-id
```

> Python 버전은 `DRIVE_FOLDER_ID` 로 폴더 단위 접근 제어를 명시적으로 지정.
> npm 버전보다 권한 관리가 더 명확하나 uv 설치가 추가 필요.
