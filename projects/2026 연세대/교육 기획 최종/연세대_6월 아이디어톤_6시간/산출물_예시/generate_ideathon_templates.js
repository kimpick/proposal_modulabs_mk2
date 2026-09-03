const pptxgen = require("pptxgenjs");

// ============================================================
// 연세대 AX 캠프 아이디어톤 — 트랙별 PPT 템플릿 생성기
// ============================================================

const OUTPUT_DIR = "C:\\Users\\Admin\\Downloads\\ai-education-proposal\\projects\\2026 연세대\\교육 기획 최종\\연세대_6월 아이디어톤_6시간\\산출물_예시";

// --- 색상 테마 ---
const COLORS = {
  navy: "1E2761",
  iceBlue: "CADCFC",
  white: "FFFFFF",
  dark: "1A1A2E",
  gray: "64748B",
  lightGray: "E2E8F0",
  track1: "0D6EFD",   // 블루
  track1bg: "EFF6FF",
  track2: "7C3AED",   // 퍼플
  track2bg: "F5F3FF",
  track3: "059669",   // 그린
  track3bg: "ECFDF5",
  gold: "F59E0B",
  red: "EF4444",
};

// --- 헬퍼 ---
function addTitleSlide(pres, trackName, trackDesc, accentColor) {
  const slide = pres.addSlide();
  slide.background = { color: COLORS.dark };

  // 좌측 컬러 바
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.15, h: 5.625,
    fill: { color: accentColor }
  });

  slide.addText("2026 연세대 AX 캠프", {
    x: 0.8, y: 1.2, w: 8, h: 0.5,
    fontSize: 14, fontFace: "Arial", color: COLORS.gray,
    charSpacing: 4
  });

  slide.addText("아이디어톤 발표 덱", {
    x: 0.8, y: 1.7, w: 8, h: 0.8,
    fontSize: 36, fontFace: "Arial Black", color: COLORS.white, bold: true
  });

  slide.addText(trackName, {
    x: 0.8, y: 2.6, w: 8, h: 0.6,
    fontSize: 22, fontFace: "Arial", color: accentColor, bold: true
  });

  slide.addText(trackDesc, {
    x: 0.8, y: 3.2, w: 7.5, h: 0.5,
    fontSize: 13, fontFace: "Arial", color: COLORS.lightGray
  });

  // 정보 표
  slide.addText([
    { text: "이름  ", options: { bold: true, color: COLORS.gray, fontSize: 11 } },
    { text: "_____________      ", options: { color: COLORS.white, fontSize: 11 } },
    { text: "소속  ", options: { bold: true, color: COLORS.gray, fontSize: 11 } },
    { text: "_____________      ", options: { color: COLORS.white, fontSize: 11 } },
    { text: "날짜  ", options: { bold: true, color: COLORS.gray, fontSize: 11 } },
    { text: "2026.06.24", options: { color: COLORS.white, fontSize: 11 } },
  ], { x: 0.8, y: 4.5, w: 8, h: 0.4 });

  return slide;
}

function addIdeaListSlide(pres, ideas, trackName, accentColor, bgColor) {
  const slide = pres.addSlide();
  slide.background = { color: "FAFAFA" };

  // 헤더 영역
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.0,
    fill: { color: accentColor }
  });

  slide.addText("① 아이디어 리스트", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 22, fontFace: "Arial Black", color: COLORS.white, bold: true
  });

  slide.addText(`Empathize 단계 — 발산 (Diverge)  |  ${trackName}`, {
    x: 0.5, y: 0.6, w: 9, h: 0.3,
    fontSize: 11, fontFace: "Arial", color: COLORS.white, transparency: 20
  });

  // 아이디어 카드들
  ideas.forEach((idea, i) => {
    const y = 1.2 + i * 0.82;
    const isSelected = idea.selected;

    // 카드 배경
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: y, w: 9, h: 0.72,
      fill: { color: isSelected ? bgColor : COLORS.white },
      line: { color: isSelected ? accentColor : COLORS.lightGray, width: isSelected ? 2 : 1 },
      shadow: { type: "outer", color: "000000", blur: 4, offset: 1, angle: 90, opacity: 0.08 }
    });

    // 번호 원
    slide.addShape(pres.shapes.OVAL, {
      x: 0.65, y: y + 0.13, w: 0.46, h: 0.46,
      fill: { color: isSelected ? accentColor : COLORS.lightGray }
    });
    slide.addText(`${i + 1}`, {
      x: 0.65, y: y + 0.13, w: 0.46, h: 0.46,
      fontSize: 14, fontFace: "Arial", color: COLORS.white, bold: true,
      align: "center", valign: "middle"
    });

    // 아이디어 제목
    slide.addText(idea.title, {
      x: 1.3, y: y + 0.05, w: 6.5, h: 0.35,
      fontSize: 13, fontFace: "Arial", color: COLORS.dark, bold: true
    });

    // 아이디어 설명
    slide.addText(idea.desc, {
      x: 1.3, y: y + 0.38, w: 6.5, h: 0.3,
      fontSize: 10, fontFace: "Arial", color: COLORS.gray
    });

    // Selected 뱃지
    if (isSelected) {
      slide.addShape(pres.shapes.RECTANGLE, {
        x: 8.2, y: y + 0.22, w: 1.1, h: 0.3,
        fill: { color: accentColor }
      });
      slide.addText("✓ 선정", {
        x: 8.2, y: y + 0.22, w: 1.1, h: 0.3,
        fontSize: 10, fontFace: "Arial", color: COLORS.white, bold: true,
        align: "center", valign: "middle"
      });
    }
  });

  // 하단 안내
  slide.addText("💡 DT 단계: 자기 관찰과 AI 대화를 통해 3~5개 아이디어를 발산한 후, 평가표로 1개를 선정합니다.", {
    x: 0.5, y: 5.2, w: 9, h: 0.3,
    fontSize: 9, fontFace: "Arial", color: COLORS.gray, italic: true
  });
}

function addEvaluationSlide(pres, ideas, criteria, trackName, accentColor, bgColor) {
  const slide = pres.addSlide();
  slide.background = { color: "FAFAFA" };

  // 헤더
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.0,
    fill: { color: accentColor }
  });
  slide.addText("② 아이디어 선정 평가표", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 22, fontFace: "Arial Black", color: COLORS.white, bold: true
  });
  slide.addText(`Define 단계 — 수렴 (Converge)  |  ${trackName}`, {
    x: 0.5, y: 0.6, w: 9, h: 0.3,
    fontSize: 11, fontFace: "Arial", color: COLORS.white, transparency: 20
  });

  // 테이블 헤더
  const headers = [{ text: "아이디어", options: { fill: { color: COLORS.dark }, color: COLORS.white, bold: true, fontSize: 10, align: "center", valign: "middle" } }];
  criteria.forEach(c => {
    headers.push({ text: c.label, options: { fill: { color: COLORS.dark }, color: COLORS.white, bold: true, fontSize: 10, align: "center", valign: "middle" } });
  });
  headers.push({ text: "총점", options: { fill: { color: COLORS.dark }, color: COLORS.white, bold: true, fontSize: 10, align: "center", valign: "middle" } });
  headers.push({ text: "비고", options: { fill: { color: COLORS.dark }, color: COLORS.white, bold: true, fontSize: 10, align: "center", valign: "middle" } });

  const tableData = [headers];

  // 아이디어별 점수 행
  ideas.forEach((idea, i) => {
    const row = [{ text: idea.shortTitle, options: { fontSize: 9, color: COLORS.dark, valign: "middle" } }];
    criteria.forEach(c => {
      row.push({ text: String(idea.scores[c.key]), options: { fontSize: 10, align: "center", valign: "middle", color: idea.scores[c.key] >= 4 ? accentColor : COLORS.gray, bold: idea.scores[c.key] >= 4 } });
    });
    const total = criteria.reduce((sum, c) => sum + idea.scores[c.key], 0);
    const maxTotal = criteria.length * 5;
    row.push({ text: `${total}/${maxTotal}`, options: { fontSize: 10, align: "center", valign: "middle", bold: true, color: idea.selected ? accentColor : COLORS.gray } });
    row.push({ text: idea.selected ? "✓ 선정" : "", options: { fontSize: 9, align: "center", valign: "middle", color: accentColor, bold: true } });
    tableData.push(row);
  });

  const colW = [2.8, ...criteria.map(() => 0.9), 0.8, 0.9];
  slide.addTable(tableData, {
    x: 0.5, y: 1.2, w: 9, colW: colW,
    border: { pt: 1, color: COLORS.lightGray },
    rowH: 0.45
  });

  // 평가 기준 설명
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.2 + 0.45 * (ideas.length + 1) + 0.2, w: 9, h: 0.85 + criteria.length * 0.2,
    fill: { color: bgColor },
    line: { color: accentColor, width: 1 }
  });

  slide.addText("📋 평가 기준 (1~5점)", {
    x: 0.7, y: 1.2 + 0.45 * (ideas.length + 1) + 0.25, w: 8, h: 0.3,
    fontSize: 11, fontFace: "Arial", color: accentColor, bold: true
  });

  const criteriaTexts = criteria.map((c, i) => ({
    text: `${c.label}: ${c.desc}\n`,
    options: { breakLine: true, fontSize: 9, color: COLORS.gray }
  }));
  slide.addText(criteriaTexts, {
    x: 0.7, y: 1.2 + 0.45 * (ideas.length + 1) + 0.5, w: 8.5, h: criteria.length * 0.2
  });
}

function addProjectPlanSlide(pres, planItems, trackName, accentColor, bgColor, planTitle, planSubtitle) {
  const slide = pres.addSlide();
  slide.background = { color: "FAFAFA" };

  // 헤더
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.0,
    fill: { color: accentColor }
  });
  slide.addText(planTitle || "③ 기획안 (Prototype)", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 22, fontFace: "Arial Black", color: COLORS.white, bold: true
  });
  slide.addText(planSubtitle || `Ideation + Prototype — 구체화  |  ${trackName}`, {
    x: 0.5, y: 0.6, w: 9, h: 0.3,
    fontSize: 11, fontFace: "Arial", color: COLORS.white, transparency: 20
  });

  // 기획안 항목들
  const itemHeight = (4.2 / planItems.length);
  planItems.forEach((item, i) => {
    const y = 1.15 + i * itemHeight;

    // 왼쪽 라벨 영역
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: y, w: 2.2, h: itemHeight - 0.1,
      fill: { color: accentColor }
    });
    slide.addText(item.label, {
      x: 0.5, y: y, w: 2.2, h: itemHeight - 0.1,
      fontSize: 11, fontFace: "Arial", color: COLORS.white, bold: true,
      align: "center", valign: "middle"
    });

    // 내용 영역
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 2.7, y: y, w: 6.8, h: itemHeight - 0.1,
      fill: { color: COLORS.white },
      line: { color: COLORS.lightGray, width: 1 }
    });

    if (item.example) {
      slide.addText(item.example, {
        x: 2.85, y: y + 0.03, w: 6.5, h: itemHeight - 0.15,
        fontSize: 9, fontFace: "Arial", color: COLORS.dark,
        valign: "top", margin: 0
      });
    } else {
      slide.addText("여기에 작성하세요.", {
        x: 2.85, y: y, w: 6.5, h: itemHeight - 0.1,
        fontSize: 10, fontFace: "Arial", color: COLORS.lightGray, italic: true,
        valign: "middle"
      });
    }
  });

  // 하단 안내
  slide.addText("💡 AI와 함께 작업한 과정을 로그로 남겨주세요. 완성도보다 'AI와 얼마나 선명하게 만들었는가'가 평가 기준입니다.", {
    x: 0.5, y: 5.25, w: 9, h: 0.3,
    fontSize: 9, fontFace: "Arial", color: COLORS.gray, italic: true
  });
}

function addProcessSlide(pres, trackName, accentColor, processSteps) {
  const slide = pres.addSlide();
  slide.background = { color: COLORS.white };

  // 헤더
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.9,
    fill: { color: COLORS.dark }
  });
  slide.addText("AI 활용 과정", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 20, fontFace: "Arial Black", color: COLORS.white, bold: true
  });
  slide.addText(`${trackName} — 프롬프트 및 대화 로그 요약`, {
    x: 0.5, y: 0.58, w: 9, h: 0.3,
    fontSize: 11, fontFace: "Arial", color: COLORS.gray
  });

  // 프로세스 스텝들
  processSteps.forEach((step, i) => {
    const y = 1.1 + i * 0.85;

    // 스텝 번호
    slide.addShape(pres.shapes.OVAL, {
      x: 0.5, y: y + 0.05, w: 0.4, h: 0.4,
      fill: { color: accentColor }
    });
    slide.addText(`${i + 1}`, {
      x: 0.5, y: y + 0.05, w: 0.4, h: 0.4,
      fontSize: 12, fontFace: "Arial", color: COLORS.white, bold: true,
      align: "center", valign: "middle"
    });

    // 내용
    slide.addText(step.title, {
      x: 1.1, y: y, w: 8, h: 0.3,
      fontSize: 12, fontFace: "Arial", color: COLORS.dark, bold: true
    });
    slide.addText(step.desc, {
      x: 1.1, y: y + 0.3, w: 8, h: 0.45,
      fontSize: 9, fontFace: "Arial", color: COLORS.gray
    });
  });
}

// ============================================================
// TRACK 1: AI 연구자동화 / 논문 작성
// ============================================================
function createTrack1() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "모두의연구소";
  pres.title = "Track 1 - 아이디어톤 발표 덱";

  const accent = COLORS.track1;
  const bg = COLORS.track1bg;
  const trackName = "Track 1 · AI 연구자동화 / 논문 작성";

  const ideas = [
    { title: "LLM 기반 학술 논문 자동 요약: 분야별 요약 품질 비교 연구", desc: "LLM이 서로 다른 학문 분야(이공계/인문사회계) 논문을 요약할 때의 품질 차이를 체계적으로 비교", shortTitle: "LLM 논문 자동 요약 품질 비교", selected: true, scores: { A: 5, B: 4, C: 5, D: 5 } },
    { title: "AI 튜터가 대학생 학업 성취도에 미치는 영향", desc: "ChatGPT 기반 AI 튜터 활용이 학습 성과에 미치는 영향을 실험 설계를 통해 검증", shortTitle: "AI 튜터의 학업 성취도 영향", selected: false, scores: { A: 3, B: 4, C: 3, D: 4 } },
    { title: "의료 진단 보조 AI의 신뢰성에 대한 사용자 인식 연구", desc: "의료진과 일반인을 대상으로 AI 진단 보조 도구에 대한 신뢰도 조사 및 요인 분석", shortTitle: "의료 AI 신뢰도 인식 연구", selected: false, scores: { A: 3, B: 3, C: 2, D: 3 } },
    { title: "멀티모달 LLM의 교육 평가 자동화 가능성 탐색", desc: "이미지+텍스트 기반 LLM이 서술형 평가 채점을 어디까지 신뢰롭게 수행할 수 있는지 탐색", shortTitle: "멀티모달 LLM 평가 자동화", selected: false, scores: { A: 4, B: 4, C: 3, D: 3 } },
  ];

  const criteria = [
    { key: "A", label: "Research Gap 명확성", desc: "기존 문헌의 공백(Gap)을 얼마나 명확하게 겨냥하고 있는가?" },
    { key: "B", label: "기여 가능성", desc: "해당 연구가 학문 또는 실무에 의미 있는 기여를 할 수 있는가?" },
    { key: "C", label: "검증·데이터 확보", desc: "검증 방법과 데이터 수집 계획이 현실적으로 실행 가능한가?" },
    { key: "D", label: "관심·전공 연결", desc: "본인의 관심 분야 및 전공과 얼마나 깊이 연결되어 있는가?" },
  ];

  const planItems = [
    { label: "연구 질문", example: "LLM이 학술 논문을 요약할 때, 자연과학(STEM)과 인문사회계열 간 요약 품질(충실도·정확도·완성도) 차이가 존재하는가? 어떤 요인이 품질 편차를 결정하는가?" },
    { label: "가설 / 기여 포인트", example: "가설: LLM은 자연과학 논문에서 구조적 요약 품질이 더 높고, 인문사회 논문에서 논리적 일관성이 떨어질 것이다.\n기여: 분야별 LLM 요약 품질 편차의 원인을 규명하고, 맞춤형 프롬프트 전략을 제안" },
    { label: "검증 방법", example: "1) STEM/인문 각 15편씩 논문 수집 (arXiv, KCI)\n2) GPT-4, Claude, Gemini에 동일 프롬프트로 요약 요청\n3) ROUGE, BERTScore + 인간 평가(루브릭 5점)로 품질 측정\n4) 요약 품질 차이의 요인 분석" },
    { label: "데이터 수집 전략", example: "arXiv(자연과학 15편) + RISS/KCI(인문사회 15편) 무작위 추출\n· AI 도구: ChatGPT(GPT-4), Claude 3.5, Gemini Pro\n· 평가 지표: ROUGE-L, BERTScore F1, 인간 루브릭(충실도/간결성/일관성)" },
  ];

  const processSteps = [
    { title: "관심 분야 탐색 — AI와 브레인스토밍", desc: "ChatGPT에게 자신의 전공과 관심사를 알려주고, 현재 연구 트렌드 & 미해결 문제(Gap)를 함께 찾음" },
    { title: "문헌 조사 — AI 리서치 파이프라인", desc: "Semantic Scholar API + Elicit + Consensus로 관련 논문 30편 검색, AI로 초록 요약 및 갭 분석" },
    { title: "아이디어 발산 — 5개 후보 도출", desc: "AI와 대화하며 5개 연구 아이디어를 도출. 각각의 Research Gap, 기여 포인트, 실행 가능성을 1페이지로 정리" },
    { title: "평가 및 선정 — 루브릭 기반 수렴", desc: "4가지 평가 기준(1~5점)으로 5개 아이디어를 채점. 'LLM 논문 요약 품질 비교'가 총점 19/20으로 선정" },
    { title: "기획안 작성 — AI와 프로토타입", desc: "선정된 아이디어로 연구 설계서 초안을 AI와 함께 작성. 연구 질문 → 가설 → 검증 방법 → 데이터 전략을 1시간 내 완성" },
  ];

  addTitleSlide(pres, trackName, "LLM과 함께 연구 질문부터 논문 초안까지", accent);
  addIdeaListSlide(pres, ideas, trackName, accent, bg);
  addEvaluationSlide(pres, ideas, criteria, trackName, accent, bg);
  addProjectPlanSlide(pres, planItems, trackName, accent, bg,
    "③ 기획안 · 연구 설계 개요",
    "Prototype (HOW) — 무슨 연구를, 어떻게 할 것인가  |  " + trackName);
  addProcessSlide(pres, trackName, accent, processSteps);

  pres.writeFile({ fileName: `${OUTPUT_DIR}\\Track1_아이디어톤_템플릿.pptx` });
  console.log("Track 1 PPTX generated");
}

// ============================================================
// TRACK 2: AI 브랜딩 / 퍼스널 브랜딩
// ============================================================
function createTrack2() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "모두의연구소";
  pres.title = "Track 2 - 아이디어톤 발표 덱";

  const accent = COLORS.track2;
  const bg = COLORS.track2bg;
  const trackName = "Track 2 · AI 브랜딩 / 퍼스널 브랜딩";

  const ideas = [
    { title: "비건 라이프스타일 × AI 레시피 크리에이터", desc: "비건 식단과 AI를 결합한 맞춤형 레시피 콘텐츠로 건강한 라이프스타일 브랜드 구축", shortTitle: "비건 × AI 레시피 크리에이터", selected: true, scores: { A: 5, B: 4, C: 5, D: 4 } },
    { title: "공대생의 AI 스타트업 인턴십 스토리텔링", desc: "공대생이 AI 스타트업에서 겪는 실전 경험을 인스타/브런치 콘텐츠로 연재", shortTitle: "공대생 AI 스타트업 스토리", selected: false, scores: { A: 4, B: 3, C: 4, D: 3 } },
    { title: "음악 전공자의 AI 작곡 도구 리뷰 채널", desc: "클래식 전공자가 AI 작곡 도구(Suno, Udio)를 음악이론 관점에서 리뷰", shortTitle: "음악 전공자의 AI 작곡 리뷰", selected: false, scores: { A: 4, B: 5, C: 3, D: 4 } },
    { title: "글로벌 취업 준비생을 위한 AI 이력서 최적화 가이드", desc: "AI 도구로 외국계 기업 이력서/커버레터를 최적화하는 방법을 콘텐츠화", shortTitle: "AI 이력서 최적화 가이드", selected: false, scores: { A: 3, B: 3, C: 4, D: 3 } },
  ];

  const criteria = [
    { key: "A", label: "Sweet Spot", desc: "지식 × 취향 × 관점이 교차하는 고유한 영역인가? (나만의 스윗스팟)" },
    { key: "B", label: "차별적 각도", desc: "기존 크리에이터와 차별화되는 독창적인 관점이나 접근법인가?" },
    { key: "C", label: "커리어 연결성", desc: "이 콘텐츠가 본인의 커리어 목표와 얼마나 직접적으로 연결되는가?" },
    { key: "D", label: "지속 가능성", desc: "최소 6개월 이상 지속해서 콘텐츠를 생산할 수 있는 주제인가?" },
  ];

  const planItems = [
    { label: "정체성 · Sweet Spot", example: "지식(식품영양학) × 취향(비건 요리) × 관점(AI로 라이프스타일 최적화)\n한 줄 정의: 'AI로 비건 라이프스타일을 최적화하는 데이터 기반 식단 크리에이터'" },
    { label: "전문성 스토리아크", example: "기원: 건강상 비건 시작 → 3개월간 영양 불균형(단백질/B12 부족) 실패\n전환: ChatGPT에 식단 추천받으니 영양 균형 회복 → 'AI가 비건 진입장벽(메뉴 선택)을 해결한다' 깨달음\n현재: AI로 매일 식단 기획, 인스타 500 팔로워(3개월)\n비전: 한국 최초 'AI×비건' 라이프스타일 크리에이터 1만 팔로워, 식품기업 콜라보" },
    { label: "가치 제안 · 차별 각도", example: "타깃: 환경 보호에 공감하지만 비건이 막막한 20~30대 1인 가구\n차별: 일반 비건 크리에이터(레시피만) vs 나(AI 영양 데이터 + 레시피 + 스토리텔링)\n슬로건: 'AI와 함께하는 비건 라이프 — 매일 1분이면 맞춤 영양식'" },
    { label: "1년 / 10년 목표", example: "1년(2026-27): 인스타 3천 팔로워, 첫 브랜드 협업 1건, 식품기업 인턴십 제안\n10년(2036): 'AI 비건 라이프스타일' 1위 크리에이터(10만+), AI 맞춤 비건 식단 구독 창업 또는 식품기업 CMO, 한국 비건 인구 5% 확대 기여" },
  ];

  const processSteps = [
    { title: "자기 발견 — Sweet Spot 찾기", desc: "AI에게 자신의 지식(영양학), 취향(요리), 관점(환경보호)을 입력하고 교집합을 분석하여 스윗스팟 도출" },
    { title: "오디언스 리서치 — AI 페르소나 생성", desc: "ChatGPT로 타깃 오디언스 페르소나 3개를 생성하고, 각각의 니즈/페인포인트를 분석" },
    { title: "아이디어 발산 — 콘텐츠 5개 후보", desc: "스윗스팟 × 오디언스 매트릭스로 5개 콘텐츠 아이디어를 도출. 각각의 차별성과 지속 가능성을 평가" },
    { title: "평가 및 선정 — 루브릭 기반 수렴", desc: "4가지 평가 기준(1~5점)으로 채점. '비건 × AI 레시피 크리에이터'가 총점 18/20으로 선정" },
    { title: "커리어 계획서 작성 — AI와 프로토타입", desc: "선정된 아이디어로 커리어 계획서(정체성·스토리아크·가치제안·1년/10년 목표)를 AI와 작성. 이 계획서가 7월 콘텐츠 전략 기획(Word)의 목적지가 됨" },
  ];

  addTitleSlide(pres, trackName, "AI 시대 커리어 설계의 주도권 갖기", accent);
  addIdeaListSlide(pres, ideas, trackName, accent, bg);
  addEvaluationSlide(pres, ideas, criteria, trackName, accent, bg);
  addProjectPlanSlide(pres, planItems, trackName, accent, bg,
    "③ 기획안 · 커리어 계획서",
    "Prototype (WHO/WHERE) — 나는 누구이고, 어디로 갈 것인가  |  " + trackName);
  addProcessSlide(pres, trackName, accent, processSteps);

  pres.writeFile({ fileName: `${OUTPUT_DIR}\\Track2_아이디어톤_템플릿.pptx` });
  console.log("Track 2 PPTX generated");
}

// ============================================================
// TRACK 3: AI 비즈니스 랩 (Agentic)
// ============================================================
function createTrack3() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "모두의연구소";
  pres.title = "Track 3 - 아이디어톤 발표 덱";

  const accent = COLORS.track3;
  const bg = COLORS.track3bg;
  const trackName = "Track 3 · AI 비즈니스 랩 (Agentic)";

  const ideas = [
    { title: "Hermes Agent 기반 중고 거래 분쟁 해결 봇", desc: "Telegram 봇으로 중고 거래 분쟁(환불/반품)을 AI가 양측 입장을 들어 조정하는 서비스", shortTitle: "중고 거래 분쟁 해결 봇", selected: true, scores: { A: 5, B: 4, C: 4, D: 5 } },
    { title: "AI 기반 대학생 맞춤형 식단 추천 서비스", desc: "예산/영양/취향을 입력하면 AI가 일주일 식단과 마트 장보기 리스트를 생성", shortTitle: "대학생 AI 식단 추천", selected: false, scores: { A: 3, B: 3, C: 4, D: 3 } },
    { title: "AI 튜터 매칭 플랫폼 (과외 + Agent)", desc: "학습자 레벨과 목표를 AI Agent가 분석해 최적의 튜터를 매칭하고 진행을 관리", shortTitle: "AI 튜터 매칭 플랫폼", selected: false, scores: { A: 4, B: 4, C: 3, D: 4 } },
    { title: "지역 상권 AI 분석 리포트 구독 서비스", desc: "AI가 매월 동네 상권 트렌드를 분석한 PDF 리포트를 자동 생성해 구독자에게 발송", shortTitle: "지역 상권 AI 분석 구독", selected: false, scores: { A: 3, B: 3, C: 3, D: 3 } },
  ];

  const criteria = [
    { key: "A", label: "문제 선명도", desc: "해결하고자 하는 문제가 구체적이고 명확하게 정의되어 있는가?" },
    { key: "B", label: "사업성 (지불 의사)", desc: "고객이 이 서비스에 돈을 지불할 의사가 있는가? (Willingness to Pay)" },
    { key: "C", label: "실행 가능성", desc: "현재 가진 리소스(AI 도구, 시간, 기술)로 2주 내 프로토타입을 만들 수 있는가?" },
    { key: "D", label: "AI Agent 활용도", desc: "AI Agent가 서비스의 핵심 가치 창출에 얼마나 깊이 관여하는가?" },
  ];

  const planItems = [
    { label: "미션 · 고객 · 문제", example: "미션: '중고 거래의 신뢰를 AI로 회복한다'\n고객: 당근마켓/번개장터 월 1회+ 이용자 (20~30대)\n문제: 거래 후 분쟁(불량품/환불거부) 시 감정싸움으로 번지고, 저비용 해결 창구가 전무함" },
    { label: "오퍼 (1줄)", example: "분쟁 발생 시 Telegram 봇에 거래 내역을 올리면, AI Agent가 양측 입장을 분석해 24시간 내 객관적 조정안을 제시한다.\n※ 가격·결제 모델 디테일은 사업계획서(Word)로" },
    { label: "AI Agent 핵심 가치", example: "왜 AI인가 — 유사 분쟁 사례 DB(RAG) 기반의 '객관적 판단' + 멀티모달 LLM의 '사진 손상 분석' + 24시간 무중단 '신속성'이, 인간 CS(3일·주관적)와 법률 상담(50만 원+)의 빈틈을 단번에 메운다" },
    { label: "초기 시그널 (1줄)", example: "8월 MVP 4주: 분쟁 해결 10건 / 만족도 4.5 / 첫 100인 = '분쟁 0원 해결' 캠페인으로 확보\n※ 실행 로드맵·채널 전략·재무 모델은 사업계획서(Word)로" },
  ];

  const processSteps = [
    { title: "미션 탐색 — AI와 자기 관찰", desc: "Hermes Agent에게 자신의 일상에서 겪은 불편함을 이야기하고, 해결 가능한 문제를 함께 탐색" },
    { title: "고객 인터뷰 — AI가 질문 생성", desc: "AI가 생성한 인터뷰 가이드로 주변 5명에게 중고 거래 분쟁 경험을 인터뷰. 페인포인트 정량화" },
    { title: "아이디어 발산 — 솔루션 5개 후보", desc: "문제 정의를 바탕으로 AI와 함께 5개 서비스 아이디어를 도출. 각각의 사업성과 실행 가능성을 평가" },
    { title: "평가 및 선정 — 루브릭 기반 수렴", desc: "4가지 평가 기준(1~5점)으로 채점. '분쟁 해결 봇'이 총점 18/20으로 선정" },
    { title: "사업 기획안 작성 — AI와 프로토타입", desc: "선정된 아이디어로 사업 기획안을 AI와 작성. 미션 → 고객 → 오퍼 → 채널 → AI Agent 활용을 1시간 내 완성" },
  ];

  addTitleSlide(pres, trackName, "AI Agent와 함께 사업 기회를 설계하는 3주 실행 과정", accent);
  addIdeaListSlide(pres, ideas, trackName, accent, bg);
  addEvaluationSlide(pres, ideas, criteria, trackName, accent, bg);
  addProjectPlanSlide(pres, planItems, trackName, accent, bg,
    "③ 기획안 · 사업 기획안 (1장 요약)",
    "Prototype (WHY/WHAT) — 어떤 사업 아이템인가, 왜 유망한가  |  " + trackName);
  addProcessSlide(pres, trackName, accent, processSteps);

  pres.writeFile({ fileName: `${OUTPUT_DIR}\\Track3_아이디어톤_템플릿.pptx` });
  console.log("Track 3 PPTX generated");
}

// ============================================================
// 실행
// ============================================================
(async () => {
  createTrack1();
  createTrack2();
  createTrack3();
  console.log("All 3 track templates generated!");
})();
