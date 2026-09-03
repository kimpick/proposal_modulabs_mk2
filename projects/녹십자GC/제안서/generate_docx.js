const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak, TabStopType, TabStopPosition
} = require("docx");

// ─── Constants ───
const CONTENT_W = 9506;
const COL_FULL = [CONTENT_W];
const COL_HALF = [4753, 4753];
const COL_THIRD = [3168, 3168, 3170];
const COL_QUARTER = [2376, 2376, 2376, 2378];

const CLR_NAVY = "1B3A5C";
const CLR_MNAVY = "2E5D8A";
const CLR_LNAVY = "3A7CA5";
const CLR_HDR_BG = "1B3A5C";
const CLR_ALT_ROW = "F0F4F8";
const CLR_BORDER = "B0C4DE";
const CLR_GRAY = "999999";

const FONT = "Malgun Gothic";

// ─── Helpers ───
const border = { style: BorderStyle.SINGLE, size: 1, color: CLR_BORDER };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

function hdrCell(text, width, opts = {}) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: CLR_HDR_BG, type: ShadingType.CLEAR },
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({ alignment: opts.align || AlignmentType.CENTER,
      children: [new TextRun({ text, bold: true, color: "FFFFFF", font: FONT, size: 20 })] })]
  });
}

function dataCell(text, width, opts = {}) {
  const runs = [];
  if (opts.bold) {
    runs.push(new TextRun({ text, bold: true, font: FONT, size: 20, color: opts.color || "333333" }));
  } else {
    runs.push(new TextRun({ text, font: FONT, size: 20, color: opts.color || "333333" }));
  }
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({ alignment: opts.align || AlignmentType.LEFT,
      spacing: { before: 40, after: 40 }, children: runs })]
  });
}

function row(cells, opts = {}) {
  return new TableRow({ children: cells, ...(opts.header ? { tableHeader: true } : {}) });
}

function makeTable(colWidths, rows) {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: colWidths,
    rows
  });
}

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 240 },
    children: [new TextRun({ text, bold: true, font: FONT, size: 28, color: CLR_NAVY })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 180 },
    children: [new TextRun({ text, bold: true, font: FONT, size: 24, color: CLR_MNAVY })]
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text, bold: true, font: FONT, size: 22, color: CLR_LNAVY })]
  });
}

function bodyText(text, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.spaceBefore || 60, after: opts.spaceAfter || 60 },
    alignment: opts.align || AlignmentType.LEFT,
    children: [new TextRun({ text, font: FONT, size: 22, color: "333333", ...(opts.bold ? { bold: true } : {}) })]
  });
}

function bodyRuns(runs, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.spaceBefore || 60, after: opts.spaceAfter || 60 },
    alignment: opts.align || AlignmentType.LEFT,
    children: runs.map(r => new TextRun({ font: FONT, size: 22, color: "333333", ...r }))
  });
}

function bulletItem(text, ref = "bullets") {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, font: FONT, size: 22, color: "333333" })]
  });
}

function numberedItem(text, ref = "nums") {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, font: FONT, size: 22, color: "333333" })]
  });
}

function spacer(h = 120) {
  return new Paragraph({ spacing: { before: h, after: 0 }, children: [] });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function infoRow(label, value, shading) {
  return row([
    dataCell(label, 2200, { bold: true, shading }),
    dataCell(value, CONTENT_W - 2200, { shading })
  ]);
}

// ─── Cover Page ───
const coverSection = {
  properties: {
    page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1200, bottom: 1440, left: 1200 } }
  },
  children: [
    spacer(3000),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [new TextRun({ text: "GC\uB179\uC2ED\uC790", font: FONT, size: 48, bold: true, color: CLR_NAVY })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
      children: [new TextRun({ text: "AI \uC804\uD658(AX) \uC5ED\uB7C9 \uAC15\uD654\uB97C \uC704\uD55C", font: FONT, size: 32, color: CLR_MNAVY })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
      children: [new TextRun({ text: "\uB9DE\uCDA4\uD615 \uAD50\uC721 \uD504\uB85C\uADF8\uB7A8", font: FONT, size: 32, color: CLR_MNAVY })] }),
    spacer(600),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: "\uC81C \uC548 \uC11C", font: FONT, size: 40, bold: true, color: CLR_NAVY })] }),
    spacer(1200),
    // Info block
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [
        new TextRun({ text: "\uC758\uB824\uCC98 : ", font: FONT, size: 22, color: "666666" }),
        new TextRun({ text: "GC\uB179\uC2ED\uC790 AX Unit", font: FONT, size: 22, color: "333333" })
      ] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [
        new TextRun({ text: "\uC218\uD589\uCC98 : ", font: FONT, size: 22, color: "666666" }),
        new TextRun({ text: "\uBAA8\uB450\uC758\uC5F0\uAD6C\uC18C", font: FONT, size: 22, color: "333333" })
      ] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [
        new TextRun({ text: "\uC81C\uCD9C\uC77C : ", font: FONT, size: 22, color: "666666" }),
        new TextRun({ text: "2026\uB144 5\uC6D4", font: FONT, size: 22, color: "333333" })
      ] }),
  ]
};

// ─── Main Content Section ───
const children = [];

// TOC
children.push(heading1("\uBAA9  \uCC28"));
children.push(new TableOfContents("\uBAA9\uCC28", { hyperlink: true, headingStyleRange: "1-3" }));
children.push(pageBreak());

// ── Section 3: \uBAA8\uB450\uC758\uC5F0\uAD6C\uC18C \uC18C\uAC1C
children.push(heading1("\uBAA8\uB450\uC758\uC5F0\uAD6C\uC18C \uC18C\uAC1C"));
children.push(bodyText("\uBAA8\uB450\uC758\uC5F0\uAD6C\uC18C\uB294 AI \uC2E4\uBB34 \uAD50\uC721 \uC804\uBB38 \uAE30\uAD00\uC73C\uB85C, 300\uAC1C \uC774\uC0C1\uC758 \uAE30\uC5C5\uC744 \uB300\uC0C1\uC73C\uB85C \uB9DE\uCDA4\uD615 AI \uAD50\uC721\uC744 \uC81C\uACF5\uD569\uB2C8\uB2E4. \uBE44\uAC1C\uBC1C\uC790 \uB9DE\uCDA4\uD615 \uAD50\uC721, \uBC14\uC774\uBE0C\uCF54\uB529, AI Agent \uC81C\uC791 \uB4F1 \uC2E4\uBB34 \uC911\uC2EC \uD504\uB85C\uADF8\uB7A8\uC744 \uC6B4\uC601\uD558\uACE0 \uC788\uC73C\uBA70, \uB300\uD45C \uD504\uB85C\uADF8\uB7A8\uC73C\uB85C AI \uB3C4\uAD6C \uC81C\uC791 \uC2E4\uC804 \uACFC\uC815, AX \uB9AC\uB354 \uC6CC\uD06C\uC0F5, \uC804\uC0AC \uD574\uCEE4\uD1A4 \uB4F1\uC774 \uC788\uC2B5\uB2C8\uB2E4."));
children.push(pageBreak());

// ── Section 4: \uC0AC\uC5C5 \uC774\uD574
children.push(heading1("\uC0AC\uC5C5 \uC774\uD574"));

children.push(heading2("\uC0AC\uC5C5 \uBC30\uACBD"));
children.push(bulletItem("GC\uB179\uC2ED\uC790\uB294 2026\uB144 4\uC6D4 AX Unit\uC744 \uC2E0\uC124(\uAE30\uC874 \uB514\uC9C0\uD138\uD601\uC2E0\uD300 \uC18C\uC18D\u2192\uB3C5\uB9BD)\uD558\uC5EC \uBCF8\uACA9\uC801\uC778 AI \uC804\uD658\uC744 \uCD94\uC9C4 \uC911"));
children.push(bulletItem("\uC804\uC0AC\uC801 AI \uB3C4\uAD6C HeyGC(GWS \uBE44\uC988\uB2C8\uC2A4 \uBAA8\uB378) \uC6B4\uC601 \uC911\uC774\uBA70, \uD50C\uB7AB\uD3FC\uD300\uB3C4 \uC2E0\uC124\uB418\uC5B4 1\uCC28 \uD504\uB85C\uD1A0\uD0C0\uC785 \uC774\uD6C4 \uB0B4\uBD80 \uACE0\uB3C4\uD654\uB97C \uACC4\uD68D"));
children.push(bulletItem("2025\uB144 \uB2E8\uBC1C\uC131 AI \uAD50\uC721\uC744 \uC218\uD589\uD558\uC600\uC73C\uB098, \uC0AC\uB840\uAC00 \uAC1C\uC778 \uCC28\uC6D0\uC5D0 \uBA38\uBB34\uB974\uBA70 \uC870\uC9C1\uC801 \uC131\uACFC\uB85C \uC774\uC5B4\uC9C0\uC9C0 \uC54A\uC74C"));
children.push(bulletItem("2026\uB144\uC740 \uBA64\uBC84\uC2ED \uD615\uD0DC\uC758 \uC9C0\uC18D\uC801 \uC6B4\uC601\uC744 \uD1B5\uD574 \uC870\uC9C1\uC801 \uCC28\uC6D0\uC758 AI \uD65C\uC6A9 \uC131\uACFC \uB3C4\uCD9C\uC744 \uBAA9\uD45C\uB85C \uD568"));
children.push(spacer(80));

children.push(heading2("\uC0AC\uC5C5 \uBAA9\uC801"));
children.push(bodyText("\uC784\uC6D0\u2192\uCC44\uD53C\uC5B8\u2192\uC804\uC0AC\uB85C \uC774\uC5B4\uC9C0\uB294 3\uB2E8\uACC4 \uC5F0\uACC4 \uAD50\uC721 \uAD6C\uC870\uB97C \uD1B5\uD574:"));
children.push(numberedItem("\uC784\uC6D0\uC9C4\uC774 AI \uC804\uD658\uC744 \uC8FC\uB3C4\uD558\uACE0 \uAC70\uBC84\uB10C\uC2A4\uB97C \uC218\uB9BD"));
children.push(numberedItem("AX \uCC44\uD53C\uC5B8 30\uBA85\uC774 \uC2E4\uC81C \uC0AC\uC6A9 \uAC00\uB2A5\uD55C AI \uB3C4\uAD6C\uB97C \uC81C\uC791"));
children.push(numberedItem("\uC804 \uC784\uC9C1\uC6D0\uC774 \uD574\uCEE4\uD1A4\uC744 \uD1B5\uD574 AI\uB97C \uCCB4\uD5D8\uD558\uACE0 \uC870\uC9C1\uC801 \uD655\uC0B0"));
children.push(spacer(80));

children.push(heading2("\uC0AC\uC5C5 \uAE30\uAC04 \uBC0F \uC608\uC0B0"));
children.push(bodyRuns([
  { text: "\uC0AC\uC5C5 \uAE30\uAC04 : ", bold: true },
  { text: "2026\uB144 6\uC6D4 ~ 2026\uB144 12\uC6D4 (\uCD1D 9\uD68C \uAD50\uC721 + 1\uD68C \uD574\uCEE4\uD1A4 + \uC5F0\uB9D0 \uACB0\uACFC \uBC1C\uD45C)" }
]));
children.push(bodyRuns([
  { text: "\uD611\uC758 \uC608\uC0B0 : ", bold: true },
  { text: "\u20A929,000,000 (VAT \uBCC4\uB3C4)" }
]));
children.push(pageBreak());

// ── Section 5: \uC804\uCCB4 \uC5F0\uACC4 \uB85C\uB4DC\uB9F5
children.push(heading1("\uC804\uCCB4 \uC5F0\uACC4 \uB85C\uB4DC\uB9F5"));
children.push(bodyText("GC\uB179\uC2ED\uC790 AX \uAD50\uC721\uC740 \uB2E8\uBC1C\uC131 \uAD50\uC721\uC774 \uC544\uB2CC, '\uC784\uC6D0\uC774 \uBC29\uD5A5\uC744 \uC81C\uC2DC\uD558\uACE0 \u2192 \uCC44\uD53C\uC5B8\uC774 \uB3C4\uAD6C\uB97C \uB9CC\uB4E4\uACE0 \u2192 \uC804\uC0AC\uAC00 \uD568\uAED8 \uC2E4\uD589\uD558\uB294' \uC870\uC9C1\uC801 \uC5EC\uC815\uC785\uB2C8\uB2E4. \uBCF8 \uB85C\uB4DC\uB9F5\uC740 3\uAC1C \uAD50\uC721 \uD504\uB85C\uADF8\uB7A8\uC774 \uC5B4\uB5BB\uAC8C \uC5F0\uACC4\uB418\uC5B4 \uC6B4\uC601\uB418\uB294\uC9C0, \uAC01 \uB2E8\uACC4\uC5D0\uC11C \uC5B4\uB5A4 \uC0B0\uCD9C\uBB3C\uC774 \uB3C4\uCD9C\uB418\uACE0 \uB2E4\uC74C \uB2E8\uACC4\uB85C \uC5B4\uB5BB\uAC8C \uC5F0\uACB0\uB418\uB294\uC9C0\uB97C \uBCF4\uC5EC\uC90D\uB2C8\uB2E4."));
children.push(spacer(80));

children.push(heading2("\uC5F0\uACB0 \uAD6C\uC870"));
const phaseData = [
  ["Phase 1", "\uC784\uC6D0 1\uD68C\uCC28 (6\uC6D4\uB9D0)", "\uC601\uAC10/\uBC29\uD5A5 \uC81C\uC2DC", "AI \uC778\uC2DD \uC804\uD658 + \uBC14\uC774\uBE0C\uCF54\uB529 \uCCB4\uD5D8"],
  ["Phase 2", "\uBA64\uBC84\uC2ED 1~2\uD68C\uCC28 (6~7\uC6D4)", "\uC0B0\uCD9C\uBB3C \uACF5\uC720", "\uB514\uC790\uC778\uC2DD\uD0A9 + AI \uC2EC\uD654 & \uB370\uC774\uD130 \uC790\uB3D9\uD654"],
  ["Phase 3", "\uC784\uC6D0 2\uD68C\uCC28 (7~8\uC6D4)", "\uD53C\uB4DC\uBC31 \uBC18\uC601", "\uBA64\uBC84\uC2ED \uC0B0\uCD9C\uBB3C \uB9AC\uBDF0 + \uC5C5\uBB34\uC6A9 AI \uB3C4\uAD6C \uACE0\uC548"],
  ["Phase 4", "\uBA64\uBC84\uC2ED 3~4\uD68C\uCC28 (9\uC6D4)", "30\uBA85\uC774 \uCF54\uCE58\uB85C \uD22C\uC785", "\uBC14\uC774\uBE0C\uCF54\uB529 & \uBBF8\uB2C8 \uD574\uCEE4\uD1A4"],
  ["Phase 5", "\uC804\uC0AC \uD574\uCEE4\uD1A4 (10\uC6D4)", "\uACB0\uACFC \uACF5\uC720", "\uC804 \uC784\uC9C1\uC6D0 AI \uCCB4\uD5D8 \uBC0F \uACFC\uC81C \uD574\uACB0"],
  ["Phase 6", "\uC784\uC6D0 3\uD68C\uCC28 (10~11\uC6D4)", "\uAC70\uBC84\uB10C\uC2A4 \uC218\uB9BD", "\uD574\uCEE4\uD1A4 \uACB0\uACFC \uB9AC\uBDF0 + AI \uD65C\uC6A9 \uAC70\uBC84\uB10C\uC2A4"],
  ["Phase 7", "\uC5F0\uB9D0 \uACB0\uACFC \uBC1C\uD45C (11~12\uC6D4)", "\uC131\uACFC \uC815\uB9AC", "\uC804\uCCB4 AX \uC5EC\uC815 \uC131\uACFC \uACF5\uC720"]
];
const phaseRows = [
  row([hdrCell("\uB2E8\uACC4", 1200), hdrCell("\uC77C\uC815", 2200), hdrCell("\uC5F0\uACC4 \uD2B9\uC9D5", 2400), hdrCell("\uD575\uC2EC \uB0B4\uC6A9", 3706)], { header: true }),
  ...phaseData.map((r, i) => {
    const bg = i % 2 === 1 ? CLR_ALT_ROW : undefined;
    return row([dataCell(r[0], 1200, { bold: true, align: AlignmentType.CENTER, shading: bg }),
                dataCell(r[1], 2200, { shading: bg }), dataCell(r[2], 2400, { shading: bg }), dataCell(r[3], 3706, { shading: bg })]);
  })
];
children.push(makeTable([1200, 2200, 2400, 3706], phaseRows));
children.push(spacer(120));

children.push(heading2("\uC6D4\uBCC4 \uC5F0\uAC04 \uACC4\uD68D"));
const annualData = [
  ["6\uC6D4", "AX \uC5EC\uC815 \uC2DC\uC791", "\uC784\uC6D0 1\uD68C\uCC28: AI \uC778\uC2DD \uC804\uD658 + \uBC14\uC774\uBE0C\uCF54\uB529 \uCCB4\uD5D8\n\uBA64\uBC84\uC2ED 1\uD68C\uCC28: \uB514\uC790\uC778\uC2DD\uD0A9 + AI \uAE30\uCD08", "\uC784\uC6D0\uC774 \uCCB4\uD5D8\uD55C \uBC14\uC774\uBE0C\uCF54\uB529 \u2192 \uCC44\uD53C\uC5B8\uC5D0\uAC8C \uBC29\uD5A5 \uC81C\uC2DC"],
  ["7\uC6D4", "\uC0B0\uCD9C\uBB3C \uB3C4\uCD9C", "\uBA64\uBC84\uC2ED 2\uD68C\uCC28: AI \uC2EC\uD654 & \uB370\uC774\uD130 \uC790\uB3D9\uD654", "\uBA64\uBC84\uC2ED Use-case\u00B7\uD504\uB85C\uD1A0\uD0C0\uC785 \u2192 \uC784\uC6D0 2\uD68C\uCC28 \uB9AC\uBDF0 \uB300\uC0C1"],
  ["7~8\uC6D4", "\uAD50\uCC28 \uAC80\uC99D", "\uC784\uC6D0 2\uD68C\uCC28: \uBA64\uBC84\uC2ED \uC0B0\uCD9C\uBB3C \uB9AC\uBDF0 + \uC5C5\uBB34\uC6A9 AI \uB3C4\uAD6C \uACE0\uC548", "\uC784\uC6D0 \uD53C\uB4DC\uBC31 \u2192 \uBA64\uBC84\uC2ED 3~4\uD68C\uCC28\uC5D0 \uBC18\uC601"],
  ["9\uC6D4", "AI \uB3C4\uAD6C \uC644\uC131", "\uBA64\uBC84\uC2ED 3~4\uD68C\uCC28: \uBC14\uC774\uBE0C\uCF54\uB529 + \uBBF8\uB2C8 \uD574\uCEE4\uD1A4", "30\uBA85 \uCC44\uD53C\uC5B8, \uC2E4\uC81C \uC0AC\uC6A9 \uAC00\uB2A5\uD55C AI \uB3C4\uAD6C \uC644\uC131 \u2192 \uD574\uCEE4\uD1A4 \uCF54\uCE58\uB85C \uD22C\uC785"],
  ["10\uC6D4", "\uC804\uC0AC \uD655\uC0B0", "\uC804\uC0AC \uD574\uCEE40\uB9E4 (\uCF54\uCE58: \uBA64\uBC84\uC2ED 30\uBA85 + \uBCF4\uC870\uCF54\uCE58 2\uC778 / \uC2EC\uC0AC: \uC784\uC6D0\uC9C4)", "\uCC44\uD53C\uC5B8\uC758 \uC5ED\uB7C9\uC774 \uC804\uC0AC\uB85C \uD655\uC0B0 / \uD574\uCEE40\uB9E4 \uACB0\uACFC \u2192 \uC784\uC6D0 3\uD68C\uCC28 \uAC70\uBC84\uB10C\uC2A4 \uC124\uACC4"],
  ["10~11\uC6D4", "\uAC70\uBC84\uB10C\uC2A4 \uC218\uB9BD", "\uC784\uC6D0 3\uD68C\uCC28: \uD574\uCEE40\uB9E4 \uACB0\uACFC \uAE30\uBC18 AI \uD65C\uC6A9 \uAC70\uBC84\uB10C\uC2A4 \uC124\uACC4 + \uC804\uC0AC \uD655\uC0B0 \uC804\uB7B5", "\uC2E4\uD5D8 \u2192 \uC2E4\uD589: \uC870\uC9C1\uC801 AI \uD65C\uC6A9 \uCCB4\uACC4\uD654"],
  ["11~12\uC6D4", "\uC131\uACFC \uC815\uB9AC", "\uC5F0\uB9D0 \uACB0\uACFC\uBB3C \uBC1C\uD45C (\uC804 \uC784\uC9C1\uC6D0 \uCC38\uC5EC, \uC784\uC6D0\uC9C4 \uC2EC\uC0AC)", "\uC804\uCCB4 AX \uC5EC\uC815 \uC131\uACFC \uACF5\uC720, \uB0B4\uB144 AX \uB85C\uB4DC\uB9F5 \uC218\uB9BD"]
];
const annualRows = [
  row([hdrCell("\uC6D4", 1100), hdrCell("\uB2E8\uACC4", 1500), hdrCell("\uD575\uC2EC \uD65C\uB3D9", 3506), hdrCell("\uC5F0\uACC4 \uD750\uB984", 3400)], { header: true }),
  ...annualData.map((r, i) => {
    const bg = i % 2 === 1 ? CLR_ALT_ROW : undefined;
    // Split content by \n for multi-line cells
    const contentLines = r[2].split("\n");
    const contentParas = contentLines.map(line =>
      new Paragraph({ spacing: { before: 20, after: 20 }, children: [new TextRun({ text: line, font: FONT, size: 18, color: "333333" })] })
    );
    return row([
      dataCell(r[0], 1100, { bold: true, align: AlignmentType.CENTER, shading: bg }),
      dataCell(r[1], 1500, { shading: bg }),
      new TableCell({ borders, width: { size: 3506, type: WidthType.DXA }, shading: bg ? { fill: bg, type: ShadingType.CLEAR } : undefined, margins: cellMargins, verticalAlign: "center", children: contentParas }),
      dataCell(r[3], 3400, { shading: bg })
    ]);
  })
];
children.push(makeTable([1100, 1500, 3506, 3400], annualRows));
children.push(pageBreak());

// ── Section 6: \uD504\uB85C\uADF8\uB7A8 A \u2014 \uC784\uC6D0 \uAD50\uC721
children.push(heading1("\uD504\uB85C\uADF8\uB7A8 A \u2014 [\uC784\uC6D0 \uAD50\uC721] \uB9AC\uB354\uB97C \uC704\uD55C AX \uC6CC\uD06C\uC0F5"));
children.push(bodyRuns([
  { text: "\uC758\uC0AC\uACB0\uC815\uC790\uC5D0\uC11C \uAC70\uBC84\uB10C\uC2A4 \uC124\uACC4\uC790\uB85C \u2014 \uC870\uC9C1\uC758 AI \uC804\uD658\uC744 \uC774\uB04C\uB294 3\uD68C\uCC28 \uC2E4\uC804 \uC6CC\uD06C\uC0F5", italics: true, color: CLR_LNAVY }
], { align: AlignmentType.CENTER }));
children.push(spacer(60));

// Info table
children.push(heading2("\uAE30\uBCF8 \uC815\uBCF4"));
children.push(makeTable(COL_HALF, [
  row([hdrCell("\uD56D\uBAA9", 4753), hdrCell("\uB0B4\uC6A9", 4753)]),
  row([dataCell("\uB300\uC0C1", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("GC\uB179\uC2ED\uC790 \uC784\uC6D0", 4753, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uADE0\uBAA8", 4753, { bold: true }), dataCell("\uCD1D 3\uD68C \u00D7 3\uC2DC\uAC04 (9\uC2DC\uAC04)", 4753)]),
  row([dataCell("\uC77C\uC815", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("1\uD68C\uCC28: 6\uC6D4\uB9D0 / 2\uD68C\uCC28: 7~8\uC6D4 / 3\uD68C\uCC28: 10~11\uC6D4", 4753, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uC0AC\uC6A9 \uB3C4\uAD6C", 4753, { bold: true }), dataCell("Codex Desktop", 4753)]),
  row([dataCell("AX \uB2E8\uACC4", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("1~3\uB2E8\uACC4 (\uC778\uC2DD\uC804\uD658 \u2192 \uC2E4\uBB34\uCCB4\uD5D8 \u2192 \uAC70\uBC84\uB10C\uC2A4)", 4753, { shading: CLR_ALT_ROW })])
]));
children.push(spacer(80));

children.push(heading2("\uD504\uB85C\uADF8\uB7A8 \uC18C\uAC1C"));
children.push(bodyText("GC\uB179\uC2ED\uC790 AX \uC804\uD658\uC758 \uD575\uC2EC\uC740 '\uC784\uC6D0\uC774 \uC9C1\uC811 \uCCB4\uD5D8\uD558\uACE0, \uC870\uC9C1\uC5D0 \uBC29\uD5A5\uC744 \uC81C\uC2DC\uD558\uACE0, \uAC70\uBC84\uB10C\uC2A4\uB97C \uC218\uB9BD\uD558\uB294 \uAC83'\uC785\uB2C8\uB2E4. \uBCF8 \uACFC\uC815\uC740 3\uD68C\uCC28\uC5D0 \uAC78\uCCD0 \uC784\uC6D0\uC9C4\uC774 AI \uB3C4\uAD6C\uB97C \uC9C1\uC811 \uCCB4\uD5D8\uD558\uACE0, AX \uBA64\uBC84\uC2ED \uAD50\uC721\uC758 \uC0B0\uCD9C\uBB3C\uC744 \uAC80\uD1A0\uD558\uBA70, \uC804\uC0AC \uD574\uCEE40\uB9E4\uC758 \uACB0\uACFC\uB97C \uBC14\uD0D5\uC73C\uB85C \uC2E4\uC81C \uD65C\uC6A9\uC744 \uC704\uD55C \uAC70\uBC84\uB10C\uC2A4\uB97C \uC124\uACC4\uD558\uB294 \uC6CC\uD06C\uC0F5\uC785\uB2C8\uB2E4. \uAC01 \uD68C\uCC28\uB294 \uBA64\uBC84\uC2ED \uAD50\uC721\u00B7\uD574\uCEE40\uB9E4\uACFC \uC5F0\uACC40\uB418\uC5B4, \uC870\uC9C1 \uC804\uCCB4\uC758 AX \uC5EC\uC815\uC744 \uC784\uC6D0\uC774 \uC8FC\uB3C4\uC801\uC73C\uB85C \uC774\uB04C\uB294 \uAD6C\uC870\uB85C \uC124\uACC4\uB418\uC5C8\uC2B5\uB2C8\uB2E4."));
children.push(spacer(60));

children.push(heading2("\uAD50\uC721 \uBAA9\uD45C"));
children.push(numberedItem("1\uD68C\uCC28: AI \uC804\uD658 \uC778\uC2DD \uD655\uB9BD + \uBC14\uC774\uBE0C\uCF54\uB529 \uCCB4\uD5D8\uC73C\uB85C '\uC758\uC0AC\uACB0\uC815\uC758 \uC18D\uB3C4\uAC00 \uAAF8 \uC2E4\uD589\uC758 \uC18D\uB3C4'\uB97C \uCCB4\uAC10"));
children.push(numberedItem("2\uD68C\uCC28: AX \uBA64\uBC84\uC2ED \uC0B0\uCD9C\uBB3C \uAC80\uD1A0\uB97C \uD1B5\uD574 \uBCF8\uC778 \uC5C5\uBB34\uC5D0 \uC801\uC6A9 \uAC00\uB2A5\uD55C AI \uB3C4\uAD6C \uACE0\uC548"));
children.push(numberedItem("3\uD68C\uCC28: \uC804\uC0AC \uD574\uCEE40\uB9E4 \uACB0\uACFC\uB97C \uBC14\uD0D5\uC73C\uB85C AI \uD65C\uC6A9 \uAC70\uBC84\uB10C\uC2A4 \uBC0F \uC804\uC0AC \uD655\uC0B0 \uC804\uB7B5 \uC218\uB9BD"));
children.push(spacer(60));

// Session 1
children.push(heading2("[1\uD68C\uCC28] AI \uC804\uD658 \uC778\uC2DD & \uBC14\uC774\uBE0C\uCF54\uB529 \uB9DB\uBCF4\uAE30 (3\uC2DC\uAC04)"));
children.push(bodyRuns([{ text: "\u201C\uC758\uC0AC\uACB0\uC815\uC758 \uC18D\uB3C4\uAC00 \uAAF8 \uC2E4\uD589\uC758 \uC18D\uB3C4\u201D", italics: true, color: CLR_LNAVY }], { align: AlignmentType.CENTER }));
children.push(numberedItem("AI \uC804\uD658 \uC2DC\uB300\uC640 \uC784\uC6D0\uC758 \uC5ED\uD560 (\uAC15\uC758\u00B7\uD1A0\uB860): \uC0DD\uC131\uD615 AI\uAC00 \uACBD\uC601 \uC758\uC0AC\uACB0\uC815\uC5D0 \uBBF8\uCE58\uB294 \uAD6C\uC870\uC801 \uBCC0\uD654, AI \uD65C\uC6A9 \uC870\uC9C1 vs \uBBF8\uD65C\uC6A9 \uC870\uC9C1\uC758 \uC0DD\uC0B0\uC131 \uACA9\uCC28 \uC0AC\uB840"));
children.push(numberedItem("\uBC14\uC774\uBE0C\uCF54\uB529 \uCCB4\uD5D8 \uC6CC\uD06C\uC0F5 (\uC2E4\uC2B5): Codex Desktop\uC73C\uB85C \uC544\uC774\uB514\uC5B4\u2192\uACB0\uACFC\uBB3C \uAD6C\uD604 \uCCB4\uAC10 \u2014 \uAC04\uB2E8\uD55C \uC5C5\uBB34 \uC790\uB3D9\uD654 \uB3C4\uAD6C \uC9C1\uC811 \uC0DD\uC131"));
children.push(numberedItem("\uBCF8\uC778 \uC5C5\uBB34 \uBB38\uC81C \uC815\uC758 \uC6CC\uD06C\uC0F5: \uAC01 \uB9AC\uB354\uAC00 \uBCF8\uC778 \uC870\uC9C1\uC5D0\uC11C AI\uB85C \uD574\uACB0\uD558\uACE0 \uC2F6\uC740 \uACFC\uC81C 1\uAC1C\uB97C \uC815\uC758"));
children.push(numberedItem("\uC870\uC9C1\uBCC4 AI \uC2E4\uD589 \uACFC\uC81C \uC124\uC815: \uC815\uC758\uB41C \uACFC\uC81C\uB97C \uC870\uC9C1\uBCC4\uB85C \uACF5\uC720, \uBA64\uBC84\uC2ED \uAD50\uC721 \uB300\uC0C1\uC790\uC640\uC758 \uC5F0\uACC4 \uBC29\uC548 \uB17C\uC758"));
children.push(spacer(60));

// Session 2
children.push(heading2("[2\uD68C\uCC28] \uBA64\uBC84\uC2ED \uC0B0\uCD9C\uBB3C \uB9AC\uBDF0 & \uC5C5\uBB34\uC6A9 \uB3C4\uAD6C \uACE0\uC548 (3\uC2DC\uAC04)"));
children.push(bodyRuns([{ text: "\u201C\uC2E4\uD589\uC790\uC758 \uACB0\uACFC\uBB3C\uB85C \uC784\uC6D0\uC758 \uC758\uC0AC\uACB0\uC815 \uB3C4\uAD6C\uB97C \uB9CC\uB4E4\uB2E4\u201D", italics: true, color: CLR_LNAVY }], { align: AlignmentType.CENTER }));
children.push(numberedItem("AX \uBA64\uBC84\uC2ED \uAD50\uC721 \uC0B0\uCD9C\uBB3C \uB9AC\uBDF0 (\uAC15\uC758\u00B7\uD1A0\uB860): \uBA64\uBC84\uC2ED 1~2\uD68C\uCC28\uC5D0\uC11C \uB3C4\uCD9C\uB41C Use-case\u00B7\uD504\uB85C\uD1A0\uD0C0\uC785 \uBC1C\uD45C \uCCAD\uCDE8"));
children.push(numberedItem("\uC0B0\uCD9C\uBB3C \uAE30\uBC18 \uC5C5\uBB34\uC6A9 AI \uB3C4\uAD6C \uACE0\uC548 \uC6CC\uD06C\uC0F5: \uBA64\uBC84\uC2ED \uC0B0\uCD9C\uBB3C\uC744 \uCC38\uACE0\uD558\uC5EC \uBCF8\uC778 \uC5C5\uBB34\uC5D0 \uC801\uC6A9 \uAC00\uB2A5\uD55C AI \uB3C4\uAD6C \uC544\uC774\uB514\uC5B4 \uAD6C\uCCB4\uD654"));
children.push(numberedItem("\uC870\uC9C1\uBCC4 \uC2E4\uD589 \uACC4\uD68D \uC218\uB9BD: \uACE0\uC548\uB41C AI \uB3C4\uAD6C\uB97C \uC2E4\uC81C \uC5C5\uBB34\uC5D0 \uB3C4\uC785\uD558\uAE30 \uC704\uD55C \uC77C\uC815\u00B7\uB9AC\uC18C\uC2A4\u00B7\uAC80\uC99D \uAE30\uC900 \uC124\uC815"));
children.push(numberedItem("\uBA64\uBC84\uC2ED 3~4\uD68C\uCC28 \uBC0F \uC804\uC0AC \uD574\uCEE40\uB9E4 \uBC29\uD5A5 \uC81C\uC2DC: \uC784\uC6D0 \uAD00\uC810\uC5D0\uC11C \uAE30\uB300\uC0AC\uD56D \uBA85\uD655\uD788 \uC804\uB2EC"));
children.push(spacer(60));

// Session 3
children.push(heading2("[3\uD68C\uCC28] \uC804\uC0AC \uD574\uCEE40\uB9E4 \uACB0\uACFC \uB9AC\uBDF0 & \uAC70\uBC84\uB10C\uC2A4 \uC218\uB9BD (3\uC2DC\uAC04)"));
children.push(bodyRuns([{ text: "\u201C\uC2E4\uD5D8\uC5D0\uC11C \uC2E4\uD589\uC73C\uB85C \u2014 \uC870\uC9C1\uC801 AI \uD65C\uC6A9\uC758 \uAC70\uBC84\uB10C\uC2A4\uB97C \uC138\uC6B0\uB2E4\u201D", italics: true, color: CLR_LNAVY }], { align: AlignmentType.CENTER }));
children.push(numberedItem("\uC804\uC0AC \uD574\uCEE40\uB9E4 \uACB0\uACFC \uB9AC\uBDF0 (\uAC15\uC758\u00B7\uD1A0\uB860): \uD574\uCEE40\uB9E4 \uC6B0\uC218 \uD300 \uBC1C\uD45C \uCCAD\uCDE8, \uC804\uC0AC\uC801 \uD655\uC0B0 \uAC00\uB2A5 \uACFC\uC81C\uC640 \uCD94\uAC00 \uAC1C\uBC1C \uD544\uC694 \uACFC\uC81C \uAD6C\uBD84"));
children.push(numberedItem("AI \uD65C\uC6A9 \uAC70\uBC84\uB10C\uC2A4 \uC218\uB9BD \uC6CC\uD06C\uC0F5: AI \uACB0\uACFC\uBB3C \uAC80\uC99D \uC6D0\uCE59 (\uD658\uAC01\u00B7\uD3B8\uD5A5\u00B7\uB9E5\uB77D \uC624\uB958 \uB300\uC751). \uD300 \uB2E8\uC704 AI \uB3C4\uC785 \uC2DC \uCC45\uC784\u00B7\uBCF4\uC548\u00B7\uC815\uD655\uC131 \uAE30\uC900 \uC218\uB9BD"));
children.push(numberedItem("\uC804\uC0AC \uD655\uC0B0 \uC804\uB7B5 \uC218\uB9BD: \uC784\uC6D0\u2192\uD300\uC6D0 AI \uB3C5\uB824 \uBC29\uC548. AX \uBA64\uBC84\uC2ED 30\uBA85\uC758 \uC9C0\uC18D\uC801 \uC5ED\uD560 \uC815\uC758 (\uC0AC\uB0B4 AI \uCC44\uD53C\uC5B8)"));
children.push(numberedItem("\uC870\uC9C1\uBCC4 AI \uC2E4\uD589 \uB85C\uB4DC\uB9F5 \uCD5C\uC885 \uD655\uC815: 3\uD68C\uCC28\uC5D0 \uAC78\uCCD0 \uC815\uC758\u00B7\uACE0\uC548\u00B7\uAC80\uC99D\uB41C \uC870\uC9C1\uBCC4 AI \uC2E4\uD589 \uACC4\uD68D\uC744 \uCD5C\uC885 \uBB38\uC11C\uD654"));
children.push(spacer(60));

children.push(heading2("\uD68C\uCC28\uBCC4 \uC0B0\uCD9C\uBB3C"));
children.push(bulletItem("1\uD68C\uCC28: \uC870\uC9C1\uBCC4 AI \uD574\uACB0 \uACFC\uC81C \uC815\uC758\uC11C \uBC0F \uBA64\uBC84\uC2ED \uC5F0\uACC40\uBC29\uC548"));
children.push(bulletItem("2\uD68C\uCC28: \uC784\uC6D0 \uC5C5\uBB34\uC6A9 AI \uB3C4\uAD6C \uC544\uC774\uB514\uC5B4 \uBC0F \uC2E4\uD589 \uACC4\uD68D\uC11C"));
children.push(bulletItem("3\uD68C\uCC28: AI \uD65C\uC6A9 \uAC70\uBC84\uB10C\uC2A4 \uAC00\uC774\uB4DC\uB77C\uC778 \uBC0F \uC804\uC0AC \uD655\uC0B0 \uC804\uB7B5, \uC870\uC9C1\uBCC4 AI \uC2E4\uD589 \uB85C\uB4DC\uB9F5"));
children.push(pageBreak());

// ── Section 7: \uD504\uB85C\uADF8\uB7A8 B \u2014 \uBA64\uBC84\uC2ED \uAD50\uC721
children.push(heading1("\uD504\uB85C\uADF8\uB7A8 B \u2014 [AX \uBA64\uBC84\uC2ED \uAD50\uC721] AI \uB3C4\uAD6C \uC81C\uC791 \uC2E4\uC804 \uACFC\uC815"));
children.push(bodyRuns([
  { text: "\uB514\uC790\uC778\uC2DD\uD0A9\uC73C\uB85C \uBB38\uC81C\uB97C \uC815\uC758\uD558\uACE0, \uBC14\uC774\uBE0C\uCF54\uB529\uC73C\uB85C AI \uB3C4\uAD6C\uB97C \uB9CC\uB4E4\uB2E4", italics: true, color: CLR_LNAVY }
], { align: AlignmentType.CENTER }));
children.push(spacer(60));

children.push(heading2("\uAE30\uBCF8 \uC815\uBCF4"));
children.push(makeTable(COL_HALF, [
  row([hdrCell("\uD56D\uBAA9", 4753), hdrCell("\uB0B4\uC6A9", 4753)]),
  row([dataCell("\uB300\uC0C1", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("AX \uCC44\uD53C\uC5B8 30\uBA85 (\uAC01 \uC2E4\u00B7\uBCF8\uBD80 \uB300\uD45C, \uACFC\uC81C \uC120\uBC1C)", 4753, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uADE0\uBAA8", 4753, { bold: true }), dataCell("\uCD1D 4\uD68C \u00D7 7\uC2DC\uAC04 (28\uC2DC\uAC04)", 4753)]),
  row([dataCell("\uC77C\uC815", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("1~2\uD68C\uCC28: 6~7\uC6D4 / 3~4\uD68C\uCC28: 9\uC6D4", 4753, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uC0AC\uC6A9 \uB3C4\uAD6C", 4753, { bold: true }), dataCell("OpenCode, OhMyAgent", 4753)]),
  row([dataCell("AX \uB2E8\uACC4", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("2~4\uB2E8\uACC4 (\uBB38\uC81C\uC815\uC758 \u2192 \uC2E4\uBB34\uC801\uC6A9 \u2192 \uC0B0\uCD9C\uBB3C \uCC3D\uCD9C)", 4753, { shading: CLR_ALT_ROW })])
]));
children.push(spacer(80));

children.push(heading2("\uD504\uB85C\uADF8\uB7A8 \uC18C\uAC1C"));
children.push(bodyText("GC\uB179\uC2ED\uC790 AX \uBA64\uBC84\uC2ED\uC740 '\uBC30\uC6B0\uACE0 \uB05D\uB098\uB294 \uAD50\uC721'\uC774 \uC544\uB2CC, '\uC2E4\uC81C AI \uB3C4\uAD6C\uB97C \uB9CC\uB4E4\uC5B4 \uC870\uC9C1\uC5D0 \uC801\uC6A9\uD558\uB294 \uC0B0\uCD9C\uBB3C \uC911\uC2EC \uACFC\uC815'\uC785\uB2C8\uB2E4. \uB514\uC790\uC778\uC2DD\uD0A9\uC73C\uB85C \uC870\uC9C1\uC758 \uBB38\uC81C\uB97C \uC815\uC758\uD558\uACE0, AI \uC2EC\uD654 \uAD50\uC721\uC73C\uB85C \uD574\uACB0 \uBC29\uC548\uC744 \uC124\uACC4\uD558\uBA70, \uBC14\uC774\uBE0C\uCF54\uB529\uC73C\uB85C \uC9C1\uC811 AI \uB3C4\uAD6C\uB97C \uAD6C\uD604\uD569\uB2C8\uB2E4. \uCD5C\uC885 \uBBF8\uB2C8 \uD574\uCEE40\uB9E4\uC5D0\uC11C \uC0B0\uCD9C\uBB3C\uC744 \uC644\uC131\uD558\uACE0, 10\uC6D4 \uC804\uC0AC \uD574\uCEE40\uB9E4\uC5D0\uC11C\uB294 30\uBA85\uC774 \uCF54\uCE58\uB85C \uCC38\uC5EC\uD558\uC5EC \uC804\uC0AC \uD655\uC0B0\uC744 \uC774\uB04C\uC2B5\uB2C8\uB2E4."));
children.push(spacer(60));

children.push(heading2("\uAD50\uC721 \uBAA9\uD45C"));
children.push(numberedItem("\uB514\uC790\uC778\uC2DD\uD0A9\uC744 \uD1B5\uD574 \uC870\uC9C1\uC758 \uC2E4\uC81C \uBB38\uC81C\uB97C \uC815\uC758\uD558\uACE0 AI \uC801\uC6A9 Use-case \uB3C4\uCD9C"));
children.push(numberedItem("OpenCode\uC640 OhMyAgent\uB97C \uD65C\uC6A9\uD55C AI \uB3C4\uAD6C \uC81C\uC791 \uC5ED\uB7C9 \uD655\uBCF4"));
children.push(numberedItem("\uC2E4\uC81C \uC5C5\uBB34\uC5D0 \uC801\uC6A9 \uAC00\uB2A5\uD55C AI \uB3C4\uAD6C/\uC194\uB8E8\uC158 \uC0B0\uCD9C\uBB3C \uC644\uC131"));
children.push(numberedItem("10\uC6D4 \uC804\uC0AC \uD574\uCEE40\uB9E4 \uCF54\uCE58 \uC5ED\uD560 \uC218\uD589 \uC5ED\uB7C9 \uD655\uBCF4"));
children.push(spacer(60));

// Session 1
children.push(heading2("[1\uD68C\uCC28] \uB514\uC790\uC778\uC2DD\uD0A9 & AI \uAE30\uCD08 (7\uC2DC\uAC04)"));
children.push(bodyRuns([{ text: "\u201C\uBB38\uC81C\uB97C \uC815\uC758\uD558\uB294 \uAC83\uC774 \uD574\uACB0\uC758 \uC2DC\uC791\uC774\uB2E4\u201D", italics: true, color: CLR_LNAVY }], { align: AlignmentType.CENTER }));
children.push(makeTable([800, 4706, 1500, 2500], [
  row([hdrCell("\uC21C\uC11C", 800), hdrCell("\uB0B4\uC6A9", 4706), hdrCell("\uC2DC\uAC04", 1500), hdrCell("\uD615\uD0DC", 2500)]),
  row([dataCell("1", 800, { align: AlignmentType.CENTER }), dataCell("\uB514\uC790\uC778\uC2DD\uD0A9 \uC6CC\uD06C\uC258: \uACF5\uAC10\u2192\uBB38\uC81C\uC815\uC758\u2192\uC544\uC774\uB514\uC5B4 \uBC1C\uC0B0\u2192\uD504\uB85C\uD1A0\uD0C0\uC785\u2192\uD14C\uC2A4\uD2B8 \uC804\uCCB4 \uC0AC\uC774\uD074 \uCCB4\uD5D8", 4706), dataCell("4\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER }), dataCell("\uC6CC\uD06C\uC258", 2500, { align: AlignmentType.CENTER })]),
  row([dataCell("2", 800, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uC0DD\uC131\uD615 AI \uC2E4\uBB34 \uC785\uBB38: OpenCode \uAE30\uBCF8 \uD65C\uC6A9\uBC95, \uD504\uB86C\uD504\uD2B8 \uC5D4\uC9C0\uB2C8\uC5B4\uB9C1 \uAE30\uCD08, MS 365(Excel\u00B7PowerPoint)\uC640 AI \uC5F0\uB3D9 \uC2E4\uC2B5", 4706, { shading: CLR_ALT_ROW }), dataCell("2\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uC2E4\uC2B5", 2500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW })]),
  row([dataCell("3", 800, { align: AlignmentType.CENTER }), dataCell("Use-case \uBC1C\uAD74 \uC6CC\uD06C\uC258: \uB514\uC790\uC778\uC2DD\uD0A9\uC5D0\uC11C \uB3C4\uCD9C\uD55C \uACFC\uC81C\uB97C AI \uC801\uC6A9 Use-case\uB85C \uAD6C\uCCB4\uD654, \uD300\uBCC4 \uACFC\uC81C \uC120\uC815", 4706), dataCell("1\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER }), dataCell("\uC6CC\uD06C\uC258", 2500, { align: AlignmentType.CENTER })])
]));
children.push(spacer(60));

// Session 2
children.push(heading2("[2\uD68C\uCC28] AI \uC2EC\uD654 & \uB370\uC774\uD130 \uC790\uB3D9\uD654 (7\uC2DC\uAC04)"));
children.push(bodyRuns([{ text: "\u201C\uBC18\uBCF5 \uC5C5\uBB34\uB97C \uC790\uB3D9\uD654\uD558\uACE0 \uB370\uC774\uD130\uB85C \uC758\uC0AC\uACB0\uC815\uD55C\uB2E4\u201D", italics: true, color: CLR_LNAVY }], { align: AlignmentType.CENTER }));
children.push(makeTable([800, 4706, 1500, 2500], [
  row([hdrCell("\uC21C\uC11C", 800), hdrCell("\uB0B4\uC6A9", 4706), hdrCell("\uC2DC\uAC04", 1500), hdrCell("\uD615\uD0DC", 2500)]),
  row([dataCell("1", 800, { align: AlignmentType.CENTER }), dataCell("AI Agent \uC124\uACC4 \uC2E4\uC2B5: OhMyAgent\uB97C \uD65C\uC6A9\uD55C Agent \uAD6C\uC870 \uC124\uACC4, \uBC18\uBCF5 \uC5C5\uBB34 \uC790\uB3D9\uD654 \uC6D0\uB9AC \uC774\uD574 \uBC0F \uC2E4\uC2B5", 4706), dataCell("2\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER }), dataCell("\uC2E4\uC2B5", 2500, { align: AlignmentType.CENTER })]),
  row([dataCell("2", 800, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uB370\uC774\uD130 \uCDE8\uD569 & \uBD84\uC11D \uC790\uB3D9\uD654: OpenCode\uB85C \uB370\uC774\uD130 \uCC98\uB9AC \uC790\uB3D9\uD654, MS Excel + AI \uC5F0\uB3D9\uC73C\uB85C \uB9AC\uD3EC\uD2B8 \uC790\uB3D9 \uC0DD\uC131", 4706, { shading: CLR_ALT_ROW }), dataCell("2\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uC2E4\uC2B5", 2500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW })]),
  row([dataCell("3", 800, { align: AlignmentType.CENTER }), dataCell("\uC5C5\uBB34 \uB8F0\uD2F4 \uC790\uB3D9\uD654 \uC2E4\uC2B5: \uC0AC\uB0B4 \uC5C5\uBB34 \uB8F0\uD2F4(\uBCF4\uACE0\uC11C \uC791\uC131, \uB370\uC774\uD130 \uC815\uB9AC, \uC774\uBA54\uC77C \uC694\uC57D \uB4F1)\uC744 AI\uB85C \uC790\uB3D9\uD654\uD558\uB294 \uC2E4\uC2B5", 4706), dataCell("2\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER }), dataCell("\uC2E4\uC2B5", 2500, { align: AlignmentType.CENTER })]),
  row([dataCell("4", 800, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uD300\uBCC4 \uACFC\uC81C \uC9C4\uD589 \uBC0F \uC911\uAC04 \uC810\uAC80: 1\uD68C\uCC28 \uC120\uC815 \uACFC\uC81C\uC5D0 AI \uC194\uB8E8\uC158 \uC801\uC6A9, \uCF54\uCE58 \uBA58\uD1A0\uB9C1", 4706, { shading: CLR_ALT_ROW }), dataCell("1\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uBA58\uD1A0\uB9C1", 2500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW })])
]));
children.push(spacer(60));

// Session 3
children.push(heading2("[3\uD68C\uCC28] \uBC14\uC774\uBE0C\uCF54\uB529 & \uD504\uB85C\uD1A0\uD0C0\uC785 \uC81C\uC791 (7\uC2DC\uAC04)"));
children.push(bodyRuns([{ text: "\u201C\uC544\uC774\uB514\uC5B4\uB97C \uCF54\uB4DC\uB85C \uAD6C\uD604\uD55C\uB2E4\u201D", italics: true, color: CLR_LNAVY }], { align: AlignmentType.CENTER }));
children.push(makeTable([800, 4706, 1500, 2500], [
  row([hdrCell("\uC21C\uC11C", 800), hdrCell("\uB0B4\uC6A9", 4706), hdrCell("\uC2DC\uAC04", 1500), hdrCell("\uD615\uD0DC", 2500)]),
  row([dataCell("1", 800, { align: AlignmentType.CENTER }), dataCell("\uBC14\uC774\uBE0C\uCF54\uB529 \uC2E4\uC2B5: OpenCode\uB97C \uD65C\uC6A9\uD55C \uBC14\uC774\uBE0C\uCF54\uB529 \u2014 \uC790\uC5F0\uC5B4\uB85C \uC6F9 \uB300\uC2DC\uBCF4\uB4DC\u00B7\uC790\uB3D9\uD654 \uD234\u00B7\uCC57\uBD07 \uB4F1 \uD504\uB85C\uD1A0\uD0C0\uC785 \uAD6C\uD604. \uBE44\uAC1C\uBC1C\uC790\uB3C4 \uAD6C\uD604 \uAC00\uB2A5\uD55C \uC218\uC900", 4706), dataCell("3\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER }), dataCell("\uC2E4\uC2B5", 2500, { align: AlignmentType.CENTER })]),
  row([dataCell("2", 800, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("OhMyAgent \uC2EC\uD654 \uD65C\uC6A9: OhMyAgent\uB85C \uBA40\uD2F0\uC2A4\uD15D Agent \uAD6C\uCDA9, \uC2E4\uC81C \uC5C5\uBB34 \uC2DC\uB098\uB9AC\uC624\uC5D0 \uC801\uC6A9", 4706, { shading: CLR_ALT_ROW }), dataCell("2\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uC2E4\uC2B5", 2500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW })]),
  row([dataCell("3", 800, { align: AlignmentType.CENTER }), dataCell("\uD300\uBCC4 \uD504\uB85C\uC81D\uD2B8 \uC2EC\uD654: \uC120\uC815 \uACFC\uC81C\uC758 MVP \uAD6C\uD604, \uCF54\uCE58 \uBA58\uD1A0\uB9C1 \uBC0F \uD53C\uB4DC\uBC31", 4706), dataCell("1\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER }), dataCell("\uBA58\uD1A0\uB9C1", 2500, { align: AlignmentType.CENTER })]),
  row([dataCell("4", 800, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uBC1C\uD45C \uC900\uBE44: \uD300\uBCC4 \uC911\uAC04 \uBC1C\uD45C \uC790\uB8CC \uC900\uBE44, \uD53C\uB4DC\uBC31 \uC218\uC6A9 \uBC0F \uAC1C\uC120\uC0AC\uD56D \uC815\uB9AC", 4706, { shading: CLR_ALT_ROW }), dataCell("1\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uC2E4\uC2B5", 2500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW })])
]));
children.push(spacer(60));

// Session 4
children.push(heading2("[4\uD68C\uCC28] \uBBF8\uB2C8 \uD574\uCEE40\uB9E4 (7\uC2DC\uAC04)"));
children.push(bodyRuns([{ text: "\u201C\uBC30\uC6B4 \uAC83\uC744 \uB9CC\uB4E4\uACE0, \uB9CC\uB4E0 \uAC83\uC744 \uBC1C\uD45C\uD55C\uB2E4\u201D", italics: true, color: CLR_LNAVY }], { align: AlignmentType.CENTER }));
children.push(makeTable([800, 4706, 1500, 2500], [
  row([hdrCell("\uC21C\uC11C", 800), hdrCell("\uB0B4\uC6A9", 4706), hdrCell("\uC2DC\uAC04", 1500), hdrCell("\uD615\uD0DC", 2500)]),
  row([dataCell("1", 800, { align: AlignmentType.CENTER }), dataCell("\uBBF8\uB2C8 \uD574\uCEE40\uB9E4 \uC544\uC774\uB514\uC5D0\uC774\uC158: \uD300\uBCC4 \uCD5C\uC885 \uC544\uC774\uB514\uC5B4 \uAD6C\uCCB4\uD654, MVP \uBC94\uC704 \uC124\uC815", 4706), dataCell("1\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER }), dataCell("\uC6CC\uD06C\uC258", 2500, { align: AlignmentType.CENTER })]),
  row([dataCell("2", 800, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uBBF8\uB2C8 \uD574\uCEE40\uB9E4 MVP \uAD6C\uD604: OpenCode + OhMyAgent\uB85C \uC2E4\uC81C \uB3D9\uC791\uD558\uB294 \uD504\uB85C\uD1A0\uD0C0\uC785 \uAD6C\uD604. \uCF54\uCE58 \uBA58\uD1A0\uB9C1 \uBCD1\uD589", 4706, { shading: CLR_ALT_ROW }), dataCell("3\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uC2E4\uC2B5", 2500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW })]),
  row([dataCell("3", 800, { align: AlignmentType.CENTER }), dataCell("\uD300\uBCC4 \uCD5C\uC885 \uBC1C\uD45C: \uD300\uBCC4 \uC0B0\uCD9C\uBB3C \uBC1C\uD45C (5\uBD84 \uBC1C\uD45C + 3\uBD84 \uD53C\uB4DC\uBC31). \uC6B0\uC218 \uC0AC\uB840 \uACF5\uC720", 4706), dataCell("2\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER }), dataCell("\uBC1C\uD45C", 2500, { align: AlignmentType.CENTER })]),
  row([dataCell("4", 800, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uC804\uC0AC \uD574\uCEE40\uB9E4 \uCF54\uCE58 \uC5ED\uD560 \uC548\uB0B4: 30\uBA85\uC774 \uC804\uC0AC \uD574\uCEE40\uB9E4\uC5D0\uC11C \uCF54\uCE58\uB85C \uCC38\uC5EC\uD558\uB294 \uC5ED\uD560\u00B7\uAC00\uC774\uB4DC\uB77C\uC778", 4706, { shading: CLR_ALT_ROW }), dataCell("1\uC2DC\uAC04", 1500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW }), dataCell("\uAC15\uC758", 2500, { align: AlignmentType.CENTER, shading: CLR_ALT_ROW })])
]));
children.push(spacer(60));

children.push(heading2("\uD68C\uCC28\uBCC4 \uC0B0\uCD9C\uBB3C"));
children.push(bulletItem("1\uD68C\uCC28: \uC870\uC9C1\uBCC4 \uB514\uC790\uC778\uC2DD\uD0A9 \uACFC\uC81C \uC815\uC758\uC11C \uBC0F AI Use-case"));
children.push(bulletItem("2\uD68C\uCC28: \uC5C5\uBB34 \uC790\uB3D9\uD654 \uD504\uB85C\uD1A0\uD0C0\uC785 (\uB370\uC774\uD130 \uCC98\uB9AC, \uB9AC\uD3EC\uD2B8 \uC0DD\uC131 \uB4F1)"));
children.push(bulletItem("3\uD68C\uCC28: \uBC14\uC774\uBE0C\uCF54\uB529 \uAE30\uBC18 AI \uB3C4\uAD6C MVP"));
children.push(bulletItem("4\uD68C\uCC28: \uBBF8\uB2C8 \uD574\uCEE40\uB9E4 \uC0B0\uCD9C\uBB3C \u2014 \uC2E4\uC81C \uC0AC\uC6A9 \uAC00\uB2A5\uD55C AI \uB3C4\uAD6C/\uC194\uB8E8\uC158"));
children.push(bulletItem("\uACF5\uD1B5: 10\uC6D4 \uC804\uC0AC \uD574\uCEE40\uB9E4 \uCF54\uCE58 \uC5ED\uD560 \uC218\uD589 \uC5ED\uB7C9"));
children.push(pageBreak());

// ── Section 8: \uD504\uB85C\uADF8\uB7A8 C \u2014 \uC804\uC0AC \uD574\uCEE40\uB9E4
children.push(heading1("\uD504\uB85C\uADF8\uB7A8 C \u2014 [\uC804\uC0AC \uD574\uCEE40\uB9E4] GC\uB179\uC2ED\uC790 AX \uD574\uCEE40\uB9E4"));
children.push(bodyRuns([
  { text: "\uC804 \uC784\uC9C1\uC6D0\uC774 AI\uB85C \uC870\uC9C1\uC758 \uACFC\uC81C\uB97C \uD574\uACB0\uD558\uB294 1\uC77C \uC9D1\uC911 \uD574\uCEE40\uB9E4", italics: true, color: CLR_LNAVY }
], { align: AlignmentType.CENTER }));
children.push(spacer(60));

children.push(heading2("\uAE30\uBCF8 \uC815\uBCF4"));
children.push(makeTable(COL_HALF, [
  row([hdrCell("\uD56D\uBAA9", 4753), hdrCell("\uB0B4\uC6A9", 4753)]),
  row([dataCell("\uB300\uC0C1", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("GC\uB179\uC2ED\uC790 \uC804 \uC784\uC9C1\uC6D0", 4753, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uADE0\uBAA8", 4753, { bold: true }), dataCell("1\uC77C / 8\uC2DC\uAC04", 4753)]),
  row([dataCell("\uC77C\uC815", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("10\uC6D4 (\uAD6C\uCCB4\uC801 \uC77C\uC815 \uD611\uC758)", 4753, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uCF54\uCE58\uC9C4", 4753, { bold: true }), dataCell("\uBA64\uBC84\uC2ED 30\uBA85 + \uBCF4\uC870\uCF54\uCE58 2\uC778", 4753)]),
  row([dataCell("\uC2EC\uC0AC", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("\uC784\uC6D0\uC9C4", 4753, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uC0AC\uC6A9 \uB3C4\uAD6C", 4753, { bold: true }), dataCell("OpenCode, OhMyAgent, Codex Desktop", 4753)]),
  row([dataCell("AX \uB2E8\uACC4", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("5\uB2E8\uACC4 (\uC804\uC0AC \uD655\uC0B0)", 4753, { shading: CLR_ALT_ROW })])
]));
children.push(spacer(80));

children.push(heading2("\uD504\uB85C\uADF8\uB7A8 \uC18C\uAC1C"));
children.push(bodyText("GC\uB179\uC2AD\uC790 \uC804\uC0AC AX \uD574\uCEE40\uB9E4\uC740 AX \uBA64\uBC84\uC2ED \uAD50\uC721\uC5D0\uC11C \uD655\uBCF4\uD55C \uC5ED\uB7C9\uC744 \uC804\uC0AC\uB85C \uD655\uC0B0\uD558\uB294 \uD575\uC2EC \uC774\uBCA4\uD2B8\uC785\uB2C8\uB2E4. AX \uBA64\uBC84\uC2ED 30\uBA85\uC774 \uAC01 \uD300\uC758 \uCF54\uCE58\uB85C \uCC38\uC5EC\uD558\uC5EC, \uC804 \uC784\uC9C1\uC6D0\uC774 AI \uB3C4\uAD6C\uB97C \uD65C\uC6A9\uD574 \uC2E4\uC81C \uC870\uC9C1 \uACFC\uC81C\uB97C \uD574\uACB0\uD558\uB294 \uD480 \uC0AC\uC774\uD074\uC744 \uACBD\uD5D8\uD569\uB2C8\uB2E4. \uC544\uC774\uB514\uC5B4 \uBE4C\uB529\uBD80\uD130 MVP \uAD6C\uD604, \uBC1C\uD45C\uAE4C\uC9C0 \uD55C \uC0AC\uC774\uD074\uC744 \uC644\uC8FC\uD558\uBA70, \uC6B0\uC218 \uACFC\uC81C\uB294 \uC5F0\uB9D0 \uACB0\uACFC \uBC1C\uD45C \uBC0F \uC2E4\uC81C \uB3C4\uC785\uC73C\uB85C \uC774\uC5B4\uC9D1\uB2C8\uB2E4."));
children.push(spacer(60));

children.push(heading2("\uAD50\uC721 \uBAA9\uD45C"));
children.push(numberedItem("\uC804 \uC784\uC9C1\uC6D0 \uB300\uC0C1 AI \uCCB4\uD5D8 \uAE30\uD68C \uC81C\uACF5\uC73C\uB85C AX \uC778\uC2DD \uD655\uC0B0"));
children.push(numberedItem("\uBA64\uBC84\uC2ED \uAD50\uC721 \uC0B0\uCD9C\uBB3C\uC758 \uC2E4\uC804 \uAC80\uC99D \uBC0F \uD53C\uB4DC\uBC31"));
children.push(numberedItem("\uC870\uC9C1\uC801 \uCC28\uC6D0\uC758 AI \uD65C\uC6A9 Use-case \uBC1C\uAD74 \uBC0F \uC2E4\uC81C \uB3C4\uC785 \uACFC\uC81C \uC120\uC815"));
children.push(numberedItem("\uC5F0\uB9D0 \uACB0\uACFC\uBB3C \uBC1C\uD45C\uB97C \uC704\uD55C \uACFC\uC81C \uC2DC\uB4DC \uBC1C\uAD74"));
children.push(spacer(60));

children.push(heading2("\uC77C\uC815 \uD0C0\uC784\uD14C\uC774\uBE14"));
children.push(makeTable([2000, 2000, 5506], [
  row([hdrCell("\uC2DC\uAC04", 2000), hdrCell("\uC138\uC158", 2000), hdrCell("\uB0B4\uC6A9", 5506)], { header: true }),
  row([dataCell("09:00~09:20", 2000), dataCell("\uC624\uD504\uB2DD", 2000), dataCell("\uD574\uCEE40\uB9E4 \uBAA9\uD45C\u00B7\uB8F0 \uC124\uBA85, \uC2EC\uC0AC \uAE30\uC900 \uC548\uB0B4, \uCF54\uCE58 \uC18C\uAC1C", 5506)]),
  row([dataCell("09:20~09:40", 2000, { shading: CLR_ALT_ROW }), dataCell("\uD300 \uBE4C\uB529", 2000, { shading: CLR_ALT_ROW }), dataCell("\uC0AC\uC804 \uAD6C\uC131\uB41C \uD300\uBCC4 \uCC29\uC11D, \uD300\uC6D0 \uC18C\uAC1C \uBC0F \uC5ED\uD560 \uBD84\uB2F9", 5506, { shading: CLR_ALT_ROW })]),
  row([dataCell("09:40~11:00", 2000), dataCell("\uC544\uC774\uB514\uC5D0\uC774\uC158", 2000), dataCell("\uC870\uC9C1\uC758 \uC2E4\uC81C \uACFC\uC81C\uB97C \uC8FC\uC81C\uB85C \uC544\uC774\uB514\uC5B4 \uBC1C\uC0B0, \uCF54\uCE58\uAC00 \uB514\uC790\uC778\uC2DD\uD0A9 \uAE30\uBC18\uC73C\uB85C \uC544\uC774\uB514\uC5B4 \uC218\uB834 \uC9C0\uC6D0, \uCD5C\uC885 \uC544\uC774\uB514\uC5B4 1\uAC1C \uC120\uC815", 5506)]),
  row([dataCell("11:00~12:00", 2000, { shading: CLR_ALT_ROW }), dataCell("\uC624\uC804 \uAC1C\uBC1C", 2000, { shading: CLR_ALT_ROW }), dataCell("\uD504\uB85C\uD1A0\uD0C0\uC785 \uC544\uD0A4\uD14D\uCC98 \uC124\uACC4, \uB370\uC774\uD130 \uC900\uBE44, \uCD08\uAE30 \uAC1C\uBC1C", 5506, { shading: CLR_ALT_ROW })]),
  row([dataCell("12:00~13:00", 2000), dataCell("\uC810\uC2EC", 2000), dataCell("\u2014", 5506)]),
  row([dataCell("13:00~16:00", 2000, { shading: CLR_ALT_ROW }), dataCell("\uC624\uD6C4 \uAC1C\uBC1C", 2000, { shading: CLR_ALT_ROW }), dataCell("MVP \uAD6C\uD604 \uC9D1\uC911 \uAC1C\uBC1C, \uCF54\uCE58 \uC21C\uD68C \uBA58\uD1A0\uB9C1 (15:00 \uC911\uAC04 \uCCB4\uD06C\uD3EC\uC778\uD2B8)", 5506, { shading: CLR_ALT_ROW })]),
  row([dataCell("16:00~16:30", 2000), dataCell("\uBC1C\uD45C \uC900\uBE44", 2000), dataCell("\uD300\uBCC4 \uBC1C\uD45C \uC790\uB8CC(3~5\uC7A5) \uC900\uBE44, \uB370\uBAA8 \uD658\uACBD \uC810\uAC80", 5506)]),
  row([dataCell("16:30~17:30", 2000, { shading: CLR_ALT_ROW }), dataCell("\uD300\uBCC4 \uBC1C\uD45C", 2000, { shading: CLR_ALT_ROW }), dataCell("\uD300\uB2F9 5\uBD84 \uBC1C\uD45C + 3\uBD84 \uC9C8\uC758\uC751\uB2F5, \uB370\uBAA8 \uC2DC\uC5F0 \uD3EC\uD568, \uC784\uC6D0\uC9C4 \uD3C9\uAC00", 5506, { shading: CLR_ALT_ROW })]),
  row([dataCell("17:30~17:50", 2000), dataCell("\uC2EC\uC0AC \uBC0F \uC2DC\uC0C1", 2000), dataCell("\uC6B0\uC218\uD300 \uBC1C\uD45C, \uC2DC\uC0C1. \uC6B0\uC218 \uACFC\uC81C\uB294 \uC5F0\uB9D0 \uACB0\uACFC \uBC1C\uD45C \uBC0F \uC2E4\uC81C \uB3C4\uC785 \uD6C4\uBCF4\uB85C \uC120\uC815", 5506)]),
  row([dataCell("17:50~18:00", 2000, { shading: CLR_ALT_ROW }), dataCell("\uD074\uB85C\uC9D5", 2000, { shading: CLR_ALT_ROW }), dataCell("\uD574\uCEE40\uB9E4 \uC131\uACFC \uC694\uC57D, \uC5F0\uB9D0 \uACB0\uACFC\uBB3C \uBC1C\uD45C \uC77C\uC815 \uC548\uB0B4", 5506, { shading: CLR_ALT_ROW })])
]));
children.push(spacer(60));

children.push(heading2("\uC0B0\uCD9C\uBB3C"));
children.push(bulletItem("\uD300\uBCC4 AI \uB3C4\uAD6C \uD504\uB85C\uD1A0\uD0C0\uC785 (MVP)"));
children.push(bulletItem("\uC804\uC0AC\uC801 \uD655\uC0B0 \uAC00\uB2A5 Use-case \uD6C4\uBCF4"));
children.push(bulletItem("\uC5F0\uB9D0 \uACB0\uACFC\uBB3C \uBC1C\uD45C \uB300\uC0C1 \uACFC\uC81C \uC120\uC815"));
children.push(bulletItem("\uCC38\uAC00\uC790 \uC804\uC6D0 AI \uCCB4\uD5D8 \uACBD\uD5D8 \uBC0F \uC778\uC2DD \uC804\uD658"));
children.push(pageBreak());

// ── Section 9: \uAD50\uC721 \uD658\uACBD \uBC0F \uC778\uD504\uB77C
children.push(heading1("\uAD50\uC721 \uD658\uACBD \uBC0F \uC778\uD504\uB77C"));

children.push(heading2("\uACF5\uD1B5 \uC694\uAD6C\uC0AC\uD56D"));
children.push(makeTable(COL_HALF, [
  row([hdrCell("\uD56D\uBAA9", 4753), hdrCell("\uB0B4\uC6A9", 4753)]),
  row([dataCell("\uAD50\uC721\uC7A5", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("\uC640\uC774\uD30C\uC774 \uBC0F \uBE44\uD504\uB85C\uC81D\uD130 \uD658\uACBD", 4753, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uAC1C\uC778 \uAE30\uAE30", 4753, { bold: true }), dataCell("\uC218\uAC15\uC0DD \uAC1C\uC778 \uB178\uD2B8\uBD81 (\uAC01 \uB3C4\uAD6C\uBCC4 \uC0AC\uC804 \uC124\uCE58 \uD544\uC694)", 4753)]),
  row([dataCell("\uC0AC\uB0B4 AI", 4753, { bold: true, shading: CLR_ALT_ROW }), dataCell("HeyGC \uC811\uC18D \uD658\uACBD (\uC0AC\uB0B4\uB9DD)", 4753, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uC0AC\uC804 \uC900\uBE44", 4753, { bold: true }), dataCell("\uAD50\uC721 1\uC8FC\uC77C \uC804 \uC124\uCE58 \uC548\uB0B4 \uBC0F \uC0AC\uC804 \uAC00\uC774\uB4DC \uBC30\uD3EC", 4753)])
]));
children.push(spacer(80));

children.push(heading2("\uD504\uB85C\uADF8\uB7A8\uBCC4 \uC694\uAD6C\uC0AC\uD56D"));
children.push(makeTable([2500, 3506, 3500], [
  row([hdrCell("\uD504\uB85C\uADF8\uB7A8", 2500), hdrCell("\uC124\uCE58 \uB3C4\uAD6C", 3506), hdrCell("\uBE44\uACE0", 3500)]),
  row([dataCell("\uC784\uC6D0 \uAD50\uC721", 2500, { bold: true, shading: CLR_ALT_ROW }), dataCell("Codex Desktop", 3506, { shading: CLR_ALT_ROW }), dataCell("\uC784\uC6D0 \uB178\uD2B8\uBD81 \uC0AC\uC804 \uC124\uCE58 \uC69C\uCCAD", 3500, { shading: CLR_ALT_ROW })]),
  row([dataCell("\uBA64\uBC84\uC2ED \uAD50\uC721", 2500, { bold: true }), dataCell("OpenCode, OhMyAgent", 3506), dataCell("MS 365 \uD658\uACBD (Excel\u00B7PowerPoint\u00B7Teams \uC911\uC2EC \uC2E4\uC2B5)", 3500)]),
  row([dataCell("\uC804\uC0AC \uD574\uCEE40\uB9E4", 2500, { bold: true, shading: CLR_ALT_ROW }), dataCell("OpenCode, OhMyAgent, Codex Desktop", 3506, { shading: CLR_ALT_ROW }), dataCell("\uB300\uD615 \uAD50\uC721\uC7A5 \uB610\uB294 \uCEE8\uD37C\uB7F0\uC2A4\uD640, \uD300\uBCC4 \uD14C\uC774\uBE14 \uAD6C\uC131", 3500, { shading: CLR_ALT_ROW })])
]));
children.push(spacer(80));

children.push(heading2("\uC81C\uC57D\uC0AC\uD56D"));
children.push(bulletItem("MS 365 \uD658\uACBD: Google Sheets \uB4F1 \uAD6C\uAE00 \uC11C\uBE44\uC2A4 \uC0AC\uC6A9 \uBD88\uAC00"));
children.push(bulletItem("\uC0AC\uB0B4 \uBCF4\uC548: \uC0AC\uB0B4 \uCEF4\uD4E8\uD130 \uC678\uBD80 \uC811\uC18D \uC81C\uD55C \uAC00\uB2A5, \uC0AC\uC804 \uC124\uCE58 \uC69C\uCCAD \uD544\uC694"));
children.push(bulletItem("AI \uC2E4\uC2B5\uC6A9 \uACC4\uC815: \uAD50\uC721 \uAE30\uAC04 \uD55C\uC815 \uC138\uD551 \uD544\uC694"));
children.push(pageBreak());

// ── Section 10: \uAE30\uB300 \uD6A8\uACFC
children.push(heading1("\uAE30\uB300 \uD6A8\uACFC"));
children.push(numberedItem("\uC784\uC6D0 \uC8FC\uB3C4 AX \uAC70\uBC84\uB10C\uC2A4 \uCCB4\uACC4 \uD655\uB9BD \u2014 AI \uD65C\uC6A9 \uAC80\uC99D \uC6D0\uCE59, \uCC45\uC784\u00B7\uBCF4\uC548 \uAE30\uC900 \uC218\uB9BD"));
children.push(numberedItem("30\uBA85 AX \uCC44\uD53C\uC5B8 \uC591\uC131 \u2014 \uC2E4\uC81C \uC0AC\uC6A9 \uAC00\uB2A5\uD55C AI \uB3C4\uAD6C \uC81C\uC791 \uC5ED\uB7C9 \uBCF4\uC720"));
children.push(numberedItem("\uC804\uC0AC\uC801 AI \uC778\uC2DD \uC804\uD658 \u2014 \uD574\uCEE40\uB9E4\uB97C \uD1B5\uD55C \uC804 \uC784\uC9C1\uC6D0 AI \uCCB4\uD5D8 \uACBD\uD5D8"));
children.push(numberedItem("\uC870\uC9C1\uC801 AI \uD65C\uC6A9 \uC131\uACFC \uB3C4\uCD9C \u2014 \uAC1C\uC778 \uCC28\uC6D0\uC744 \uB118\uC5B4\uC120 \uC870\uC9C1\uC801 Use-case \uBC1C\uAD74 \uBC0F \uC2E4\uC81C \uB3C4\uC785"));
children.push(numberedItem("\uB0B4\uB144 AX \uB85C\uB4DC\uB9F5 \uAE30\uBC18 \uD655\uBCF4 \u2014 \uC5F0\uB9D0 \uC131\uACFC \uBC1C\uD45C\uB97C \uD1B5\uD574 \uC9C0\uC18D\uC801 AI \uC804\uD658 \uAE30\uBC18 \uB9C8\uB828"));
children.push(pageBreak());

// ── Section 11: \uCC99\uBD80 \uC548\uB0B4
children.push(heading1("\uCC99\uBD80 \uC548\uB0B4"));
children.push(bulletItem("\uBCF8 \uC81C\uC548\uC11C\uB294 \uD1B5\uD569 \uC81C\uC548\uC11C\uB85C, \uD504\uB85C\uADF8\uB7A8\uBCC4 \uC0C1\uC138 \uC81C\uC548\uC11C(PDF 4\uC885)\uAC00 \uBCC4\uB3C4 \uCC99\uBD80\uB429\uB2C8\uB2E4"));
children.push(bulletItem("\uC0C1\uC138 \uACA9\uC801\uC11C\uB294 \uBCC4\uB3C4 \uBB38\uC11C\uB85C \uC81C\uCD9C\uB429\uB2C8\uB2E4"));
children.push(bulletItem("\uAC15\uC0AC\uC9C4 \uC774\uB825\uC11C\uB294 \uBCC4\uB3C4 \uBB38\uC11C\uB85C \uC81C\uCD9C\uB429\uB2C8\uB2E4"));

// ─── Assemble Document ───
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: FONT, size: 22 } }
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: FONT, color: CLR_NAVY },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: FONT, color: CLR_MNAVY },
        paragraph: { spacing: { before: 240, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: FONT, color: CLR_LNAVY },
        paragraph: { spacing: { before: 180, after: 120 }, outlineLevel: 2 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "nums",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [
    coverSection,
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, right: 1200, bottom: 1440, left: 1200 }
        }
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            children: [new TextRun({ text: "GC\uB179\uC2ED\uC790 AX \uAD50\uC721 \uC81C\uC548\uC11C  |  \uBAA8\uB450\uC758\uC5F0\uAD6C\uC18C", font: FONT, size: 18, color: CLR_GRAY })]
          })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "\u2014 ", font: FONT, size: 18, color: CLR_GRAY }),
              new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, color: CLR_GRAY }),
              new TextRun({ text: " \u2014", font: FONT, size: 18, color: CLR_GRAY })
            ]
          })]
        })
      },
      children
    }
  ]
});

// ─── Write File ───
const OUTPUT = "C:\\Users\\Admin\\AppData\\Local\\Temp\\opencode\\GC_AX_Proposal.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUTPUT, buffer);
  console.log("SUCCESS: " + OUTPUT);
  console.log("Size: " + (buffer.length / 1024).toFixed(1) + " KB");
}).catch(err => {
  console.error("ERROR:", err.message);
  process.exit(1);
});
