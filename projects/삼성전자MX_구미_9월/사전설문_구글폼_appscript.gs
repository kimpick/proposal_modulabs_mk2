/**
 * 삼성전자 MX사업부 구미사업장 — AX조직 에이전틱 AI 실무 교육 (5일 집중 · 34H)
 * 교육생 사전 설문 자동 생성 스크립트 (Google Apps Script)
 *
 * ── 사용법 ────────────────────────────────────────────────────────────
 * 1. script.google.com 접속 → 새 프로젝트
 * 2. 이 파일 내용을 전체 붙여넣기
 * 3. 상단 실행 함수를 createPreTrainingSurvey 로 선택하고 실행
 * 4. 최초 1회 권한 승인 (Google Forms / Sheets 접근)
 * 5. 실행 로그(Ctrl+Enter)에 출력되는 편집 URL·응답 URL 확인
 *
 * ── 설계 기준 ─────────────────────────────────────────────────────────
 * - 응답 소요 10분 내외 (총 15문항, 자유서술 3문항)
 * - 과정 6대 핵심 개념 사전 이해도는 그리드 1문항으로 압축해 응답 부담 최소화
 * - Day1 환경 세팅 리스크를 사전 파악하기 위한 실습 환경 점검 문항 포함
 * ─────────────────────────────────────────────────────────────────────
 */

// ── 과정 6대 핵심 개념 (커리큘럼 Day1~Day4 대응) ──
var CORE_CONCEPTS = [
  'Agentic AI (에이전트에게 업무를 위임하는 방식)',
  'RAG (검색증강생성)',
  '지식그래프 / 문서의 지식 자산화',
  '하네스 · 컨텍스트 엔지니어링',
  'MCP (Model Context Protocol)',
  '멀티 에이전트 · 휴먼인더루프(HITL)'
];

// ── 이해도 5단계 척도 ──
var UNDERSTANDING_LEVELS = [
  '① 처음 들어봄',
  '② 들어봤지만 설명은 어려움',
  '③ 개념을 설명할 수 있음',
  '④ 직접 사용해 본 적 있음',
  '⑤ 업무에 적용하고 있음'
];

function createPreTrainingSurvey() {
  var form = FormApp.create('[모두의연구소] 에이전틱 AI 실무 교육 사전 설문');

  form.setTitle('에이전틱 AI 실무 교육 사전 설문');
  form.setDescription(
    '삼성전자 MX사업부 구미사업장 AX조직 대상 「에이전틱 AI 실무 교육(5일 집중 · 34시간)」 사전 설문입니다.\n\n' +
    '응답해 주신 내용은 실습 난이도 조정, 조 편성, 사전 환경 안내에만 활용되며 개인 평가와는 무관합니다.\n' +
    '응답에는 10분 내외가 소요됩니다.\n\n' +
    '모두의연구소 비즈팀'
  );
  form.setProgressBar(true);
  form.setAllowResponseEdits(true);
  form.setShowLinkToRespondAgain(false);

  buildSectionBasicInfo(form);
  buildSectionAiExperience(form);
  buildSectionConceptLevel(form);
  buildSectionEnvironmentCheck(form);
  buildSectionNeeds(form);

  var sheetUrl = attachResponseSpreadsheet(form);

  Logger.log('─────────────────────────────────────────────');
  Logger.log('설문 생성 완료');
  Logger.log('편집 URL   : ' + form.getEditUrl());
  Logger.log('응답 URL   : ' + form.getPublishedUrl());
  Logger.log('응답 시트  : ' + sheetUrl);
  Logger.log('─────────────────────────────────────────────');

  return {
    editUrl: form.getEditUrl(),
    publishedUrl: form.getPublishedUrl(),
    responseSheetUrl: sheetUrl
  };
}

/** 1. 기본 정보 — 3문항 */
function buildSectionBasicInfo(form) {
  form.addSectionHeaderItem()
    .setTitle('1. 기본 정보')
    .setHelpText('조 편성과 실습 사례 선정에 활용합니다.');

  form.addTextItem()
    .setTitle('성함과 소속 팀을 입력해 주세요.')
    .setHelpText('예: 홍길동 / 금형기술팀')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('담당 업무를 가장 잘 나타내는 항목을 선택해 주세요.')
    .setChoiceValues([
      '금형 · 기구 개발',
      '설비 · 공정 기술',
      '품질 · 신뢰성',
      '생산 · 제조 관리',
      '개발 지원 · 기획 · 관리',
      'AX 과제 기획 · 추진 전담'
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('현재 담당 업무 경력은 어느 정도인가요?')
    .setChoiceValues([
      '3년 미만',
      '3년 이상 ~ 7년 미만',
      '7년 이상 ~ 15년 미만',
      '15년 이상'
    ])
    .setRequired(true);
}

/** 2. AI 도구 사용 경험 — 4문항 */
function buildSectionAiExperience(form) {
  form.addPageBreakItem()
    .setTitle('2. AI 도구 사용 경험')
    .setHelpText('현재 수준을 있는 그대로 응답해 주시면 됩니다. 정답이 있는 문항이 아닙니다.');

  form.addMultipleChoiceItem()
    .setTitle('생성형 AI 챗봇(ChatGPT, Claude, Gemini 등)을 얼마나 자주 사용하시나요?')
    .setChoiceValues([
      '사용해 본 적 없음',
      '몇 번 써 본 정도',
      '월 1~2회',
      '주 1~2회',
      '거의 매일'
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('사용해 본 적 있는 도구를 모두 선택해 주세요.')
    .setChoiceValues([
      'ChatGPT',
      'Claude',
      'Gemini',
      'NotebookLM',
      'GitHub Copilot',
      'Claude Code / OpenAI Codex 등 코딩 에이전트',
      'MCP 서버를 연결해 본 경험',
      '사내 제공 AI 도구',
      '사용해 본 도구 없음'
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('AI를 실제 담당 업무에 적용해 본 경험이 있으신가요?')
    .setChoiceValues([
      '없음',
      '단순 문서 작성 · 번역 · 요약 정도',
      '자료 조사나 분석 보조로 활용',
      '반복 업무 일부를 자동화해 봄',
      '업무 프로세스에 상시 적용 중'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('프로그래밍 또는 스크립트 작성 경험은 어느 정도인가요?')
    .setHelpText('본 과정은 코드 작성을 에이전트에 위임하는 방식으로 진행하므로, 개발 경험이 없어도 참여에 문제가 없습니다.')
    .setChoiceValues([
      '전혀 없음',
      '엑셀 수식 · 매크로 수준',
      '남이 만든 코드를 수정해 본 정도',
      '필요할 때 직접 작성 가능 (Python, VBA 등)',
      '실무에서 상시 개발 · 자동화 수행'
    ])
    .setRequired(true);
}

/** 3. 과정 핵심 개념 사전 이해도 — 그리드 1문항 (6개 행) */
function buildSectionConceptLevel(form) {
  form.addPageBreakItem()
    .setTitle('3. 과정 핵심 개념 사전 이해도')
    .setHelpText('교육에서 다룰 6가지 개념입니다. 현재 이해 수준을 선택해 주세요. 실습 난이도 조정에 직접 반영됩니다.');

  form.addGridItem()
    .setTitle('각 개념에 대한 현재 이해 수준을 선택해 주세요.')
    .setRows(CORE_CONCEPTS)
    .setColumns(UNDERSTANDING_LEVELS)
    .setRequired(true);
}

/** 4. 실습 환경 사전 점검 — 3문항 */
function buildSectionEnvironmentCheck(form) {
  form.addPageBreakItem()
    .setTitle('4. 실습 환경 사전 점검')
    .setHelpText('교육 첫날 환경 세팅 시간을 줄이기 위한 문항입니다. 잘 모르시면 "확인 필요"를 선택해 주세요.');

  form.addMultipleChoiceItem()
    .setTitle('교육 중 사용할 실습 PC는 어떤 것인가요?')
    .setChoiceValues([
      '회사 노트북 (관리자 권한 있음)',
      '회사 노트북 (관리자 권한 없음)',
      '개인 노트북',
      '교육장 제공 PC 사용 예정',
      '아직 확인 필요'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('해당 PC에 개발 도구를 새로 설치할 수 있나요?')
    .setHelpText('예: 코딩 에이전트 실행 환경, 터미널 도구 등')
    .setChoiceValues([
      '자유롭게 설치 가능',
      '승인 절차를 거치면 가능',
      '설치 불가',
      '아직 확인 필요'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('해당 PC에서 사외망(외부 인터넷) 접속이 가능한가요?')
    .setHelpText('본 교육은 외부 AI 서비스를 사용하므로 사외망 접속이 필요합니다.')
    .setChoiceValues([
      '가능',
      '별도 사외망 환경에서만 가능',
      '불가',
      '아직 확인 필요'
    ])
    .setRequired(true);
}

/** 5. 교육 니즈 — 4문항 (자유서술 3문항) */
function buildSectionNeeds(form) {
  form.addPageBreakItem()
    .setTitle('5. 교육 니즈')
    .setHelpText('마지막 항목입니다. 작성해 주신 내용은 실습 과제와 사례 선정에 직접 반영됩니다.');

  var focusItem = form.addCheckboxItem();
  focusItem
    .setTitle('가장 기대하는 학습 테마를 최대 2개까지 선택해 주세요.')
    .setChoiceValues([
      'Agentic AI 기초 — 에이전트에게 업무를 위임하는 방식',
      '지식 자산화 — 팀 문서를 AI가 활용할 수 있게 만들기',
      '하네스 · 컨텍스트 엔지니어링 — AI 작업 환경 설계',
      'MCP — 사내 데이터 · 도구와 AI 연결',
      '멀티 에이전트 · HITL — 역할 분담과 안전한 통제',
      '종합 워크숍 — 내 업무 자동화 파이프라인 직접 구현'
    ])
    .setRequired(true);
  focusItem.setValidation(
    FormApp.createCheckboxValidation()
      .requireSelectAtMost(2)
      .build()
  );

  form.addParagraphTextItem()
    .setTitle('현재 담당 업무 중 "이건 AI로 자동화하고 싶다"고 생각하시는 일이 있다면 적어 주세요.')
    .setHelpText('구체적일수록 좋습니다. 예: 설비 이상 로그를 매주 취합해 요약 보고서를 만드는 일')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('교육 참여에 앞서 걱정되거나 우려되는 점이 있다면 적어 주세요.')
    .setHelpText('예: 개발 경험이 없어서 따라갈 수 있을지, 실습 속도 등')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('강사에게 미리 전달하고 싶은 질문이 있다면 자유롭게 적어 주세요.')
    .setRequired(false);
}

/** 응답 수집용 스프레드시트를 생성해 폼에 연결하고 URL을 반환한다. */
function attachResponseSpreadsheet(form) {
  var ss = SpreadsheetApp.create('[응답] 에이전틱 AI 실무 교육 사전 설문');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  return ss.getUrl();
}

/**
 * 응답 현황을 요약해 로그로 출력한다. 설문 마감 후 실행하면
 * 개념별 평균 이해 수준과 환경 점검 리스크 건수를 빠르게 확인할 수 있다.
 */
function summarizeResponses() {
  var forms = DriveApp.getFilesByName('[모두의연구소] 에이전틱 AI 실무 교육 사전 설문');
  if (!forms.hasNext()) {
    Logger.log('설문을 찾을 수 없습니다. createPreTrainingSurvey 를 먼저 실행하세요.');
    return;
  }

  var form = FormApp.openById(forms.next().getId());
  var responses = form.getResponses();
  Logger.log('총 응답 수: ' + responses.length);

  if (responses.length === 0) {
    return;
  }

  var conceptTotals = {};
  var conceptCounts = {};
  var riskCount = 0;

  for (var i = 0; i < responses.length; i++) {
    var itemResponses = responses[i].getItemResponses();

    for (var j = 0; j < itemResponses.length; j++) {
      var item = itemResponses[j];
      var type = item.getItem().getType();
      var answer = item.getResponse();

      if (type === FormApp.ItemType.GRID) {
        for (var k = 0; k < CORE_CONCEPTS.length; k++) {
          var level = UNDERSTANDING_LEVELS.indexOf(answer[k]) + 1;
          if (level > 0) {
            var name = CORE_CONCEPTS[k];
            conceptTotals[name] = (conceptTotals[name] || 0) + level;
            conceptCounts[name] = (conceptCounts[name] || 0) + 1;
          }
        }
      }

      if (typeof answer === 'string' && (answer === '설치 불가' || answer === '불가')) {
        riskCount++;
      }
    }
  }

  Logger.log('── 개념별 평균 이해 수준 (1~5) ──');
  for (var c = 0; c < CORE_CONCEPTS.length; c++) {
    var concept = CORE_CONCEPTS[c];
    if (conceptCounts[concept]) {
      var avg = conceptTotals[concept] / conceptCounts[concept];
      Logger.log(concept + ' : ' + avg.toFixed(2));
    }
  }
  Logger.log('── 실습 환경 리스크 응답 수: ' + riskCount + ' ──');
}
