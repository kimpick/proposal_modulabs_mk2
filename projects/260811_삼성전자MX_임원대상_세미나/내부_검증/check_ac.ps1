<#
AC 일괄 검증 — 삼성전자MX 임원 세미나 산출물 (US-011)

검증 범위: AC-1 · AC-3 · AC-4 · AC-5 · AC-7 · AC-8
  AC-2 는 별도 스크립트(measure_ac2.py)의 실측 리포트를 참조만 한다.
  AC-6 은 P2-8 이 최초 실행 시점이므로 이 스토리 범위 밖이다.
  AC-9 (PDF 3종 · [모두의연구소] 명명 · Drive 업로드 · 커밋) 는 산출물 존재 여부만 보조 확인한다.

실행:
  powershell -ExecutionPolicy Bypass -File 내부_검증\check_ac.ps1

주의: [모두의연구소] 접두 파일명은 대괄호가 와일드카드로 해석되므로
      모든 경로 접근에 -LiteralPath 를 쓴다.
#>

$ErrorActionPreference = 'Stop'
$OutputEncoding = [Text.Encoding]::UTF8
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$Root     = Split-Path -Parent $PSScriptRoot
$Deck     = Join-Path $Root '발표덱_가로\삼성전자MX_임원_토큰최적화_발표덱_가로.html'
$Check    = Join-Path $Root '배포물\체크리스트.html'
$Guide    = Join-Path $Root '배포물\직접_해보는_가이드.html'
$Curric   = Join-Path $Root '커리큘럼_초안_v1.md'
$Mail     = Join-Path $Root '삼성전자MX_임원세미나_커리큘럼초안_이메일.html'
$Evidence = Join-Path $Root '내부_근거_대조표.md'
$Ac2      = Join-Path $PSScriptRoot 'ac2_report.md'

# 고객 대면물 — 내부_* 문서는 제외한다
$Facing = @($Deck, $Check, $Guide, $Curric, $Mail)

$script:Fail = 0
$script:Pass = 0

function Read-File([string]$Path) {
    return Get-Content -LiteralPath $Path -Raw -Encoding UTF8
}

function Get-RenderText([string]$Html) {
    # 렌더 텍스트만 남긴다: 주석 · script · style 제거 후 태그 제거
    $t = [regex]::Replace($Html, '(?s)<!--.*?-->', ' ')
    $t = [regex]::Replace($t, '(?s)<script\b.*?</script>', ' ')
    $t = [regex]::Replace($t, '(?s)<style\b.*?</style>', ' ')
    $t = [regex]::Replace($t, '(?s)<svg\b.*?</svg>', ' ')
    $t = [regex]::Replace($t, '<[^>]+>', ' ')
    return $t
}

function Report([string]$Id, [bool]$Ok, [string]$Detail) {
    if ($Ok) {
        $script:Pass++
        Write-Host ("  PASS  {0}  {1}" -f $Id, $Detail)
    } else {
        $script:Fail++
        Write-Host ("  FAIL  {0}  {1}" -f $Id, $Detail)
    }
}

Write-Host ''
Write-Host '=== AC 일괄 검증 — 삼성전자MX 임원 세미나 ==='
Write-Host ("대상 폴더: {0}" -f $Root)
Write-Host ''

# ── 전제: 파일 존재 ────────────────────────────────────────────────
Write-Host '[0] 산출물 존재'
foreach ($f in @($Deck, $Check, $Guide, $Curric, $Mail, $Evidence)) {
    Report 'FILE ' (Test-Path -LiteralPath $f) (Split-Path -Leaf $f)
}
Write-Host ''

# ── AC-1: 슬라이드 10~15장 ────────────────────────────────────────
#   원 기준은 10~11장. 고객 요청으로 슬라이드가 세 차례 늘어 상한을 조정해 왔다.
#     260813 강사 소개 추가 → 12
#     260813 진행 구성 · 시연 · 업무 매트릭스 추가 → 15
#   고객 지시가 "시간 제약 생각하지 말고 일단 다 넣어, 나중에 정리한다"이므로
#   상한은 현재 내용을 담는 선에서 두고, 분량 정리 라운드에서 다시 좁힌다.
Write-Host '[AC-1] 슬라이드 장수 10~15'
$deckHtml = Read-File $Deck
$slides = ([regex]::Matches($deckHtml, '<section\s+class="[^"]*\bslide\b')).Count
Report 'AC-1' ($slides -ge 10 -and $slides -le 15) ("슬라이드 {0}장" -f $slides)
Write-Host ''

# ── AC-3: 외부 로드 자원 0 또는 Malgun Gothic 폴백 확보 ───────────
Write-Host '[AC-3] 외부 자원 / 한글 폰트 폴백'
foreach ($f in @($Deck, $Check, $Guide, $Mail)) {
    $h = Read-File $f
    $ext = ([regex]::Matches($h, '(?:src|href)\s*=\s*[\x22\x27]https?://')).Count
    $hasFallback = ($h -match 'Malgun Gothic')
    $name = Split-Path -Leaf $f
    if ($ext -eq 0) {
        Report 'AC-3' $true ("{0} — 외부 자원 0건" -f $name)
    } else {
        Report 'AC-3' $hasFallback ("{0} — 외부 자원 {1}건, Malgun Gothic 폴백 {2}" -f $name, $ext, $(if ($hasFallback) { '확보' } else { '없음' }))
    }
    # 한글 폰트명 오타 가드 ('맑은 고징' 등)
    if ($h -match '맑은\s*고징') {
        Report 'AC-3' $false ("{0} — 폰트명 오타 '맑은 고징' 잔존" -f $name)
    }
}
Write-Host ''

# ── AC-4: 고객 대면물 렌더 텍스트 이모지 0건 ──────────────────────
Write-Host '[AC-4] 렌더 텍스트 이모지 0건 (내부_* 제외)'
# 보조 기호(→ 등)는 제외하고 이모지·픽토그램 영역만 본다
$emojiPattern = '[\uD83C-\uDBFF][\uDC00-\uDFFF]|[☀-➿]|[⬀-⯿]|️|⃣'
foreach ($f in $Facing) {
    $raw = Read-File $f
    $txt = if ($f -like '*.md') { $raw } else { Get-RenderText $raw }
    $m = [regex]::Matches($txt, $emojiPattern)
    $name = Split-Path -Leaf $f
    if ($m.Count -eq 0) {
        Report 'AC-4' $true ("{0} — 0건" -f $name)
    } else {
        $sample = ($m | Select-Object -First 5 | ForEach-Object { $_.Value }) -join ' '
        Report 'AC-4' $false ("{0} — {1}건 (예: {2})" -f $name, $m.Count, $sample)
    }
}
Write-Host ''

# ── AC-5: 덱·배포물 플레이스홀더 0 + 커리큘럼 미확정 항목 명시 ────
Write-Host '[AC-5] 플레이스홀더 / 미확정 항목 표기'
# 기입용 밑줄(.fill)과 작성 예시 대괄호는 의도된 서식이므로 대상에서 제외한다
$phPattern = 'TBD|TODO|XXX+|PLACEHOLDER|수치\s*주입|기입\s*예정|협의\s*회신\s*시|추후\s*기재|반영해\s*기재합니다'
foreach ($f in @($Deck, $Check, $Guide)) {
    $raw = Read-File $f
    $m = [regex]::Matches($raw, $phPattern, 'IgnoreCase')
    $name = Split-Path -Leaf $f
    if ($m.Count -eq 0) {
        Report 'AC-5' $true ("{0} — 플레이스홀더 0건" -f $name)
    } else {
        $sample = ($m | Select-Object -First 3 | ForEach-Object { $_.Value }) -join ' / '
        Report 'AC-5' $false ("{0} — {1}건 ({2})" -f $name, $m.Count, $sample)
    }
}
# AC-5 갱신분: (고객 확인 필요) 마커 3건 대신 「협의 항목표」로 미확정 항목을 명시한다
#   근거: 2026-08-13 4차원 리뷰 — 마커가 §8 확정 필요 협의 항목 표 + 각주로 실질 대체됨
$cur = Read-File $Curric
$hasTable = ($cur -match '협의\s*항목')
$rowCount = ([regex]::Matches($cur, '(?m)^\|.*확인.*\|')).Count
Report 'AC-5' $hasTable ("커리큘럼 — 협의 항목표 표기 {0}" -f $(if ($hasTable) { '확인' } else { '없음' }))
Write-Host ''

# ── AC-7: 근거 대조표의 근거 열 빈 값 0 ───────────────────────────
Write-Host '[AC-7] 근거 대조표 빈 셀 0건'
$ev = Read-File $Evidence
$emptyCells = 0
$emptyRows = @()
foreach ($line in ($ev -split "`r?`n")) {
    if ($line -notmatch '^\s*\|') { continue }
    if ($line -match '^\s*\|[\s\-:|]+\|\s*$') { continue }   # 구분선 행
    $cells = ($line -split '\|')
    for ($i = 1; $i -lt $cells.Count - 1; $i++) {
        if ($cells[$i].Trim() -eq '') {
            $emptyCells++
            if ($emptyRows.Count -lt 3) { $emptyRows += $line.Trim() }
        }
    }
}
Report 'AC-7' ($emptyCells -eq 0) ("빈 셀 {0}건{1}" -f $emptyCells, $(if ($emptyRows.Count) { " (예: " + ($emptyRows[0]) + ")" } else { '' }))
Write-Host ''

# ── AC-8: SVG 2건 명시 height + .svg-fallback 존재 ────────────────
Write-Host '[AC-8] SVG height 명시 / .svg-fallback'
$svgs = [regex]::Matches($deckHtml, '<svg\b[^>]*>')
$withHeight = @($svgs | Where-Object { $_.Value -match '\bheight\s*=' })
$overLimit = @()
foreach ($s in $withHeight) {
    if ($s.Value -match '\bheight\s*=\s*[\x22\x27]?(\d+)') {
        if ([int]$Matches[1] -gt 451) { $overLimit += $Matches[1] }
    }
}
# 원 기준은 SVG 2건. 2026-08-13 고객 지적("월말 잔량 곡선은 의미없는 그래프")으로 해당 도표를
# 삭제해 1건이 되었다. 판정 핵심은 개수가 아니라 "모든 SVG가 height를 명시했는가"이므로 그렇게 바꾼다.
Report 'AC-8' ($svgs.Count -ge 1 -and $withHeight.Count -eq $svgs.Count) ("SVG {0}건 / height 명시 {1}건" -f $svgs.Count, $withHeight.Count)
Report 'AC-8' ($overLimit.Count -eq 0) ("height 상한 451px 준수{0}" -f $(if ($overLimit.Count) { " — 초과 " + ($overLimit -join ',') } else { '' }))
Report 'AC-8' ($deckHtml -match 'svg-fallback') '.svg-fallback 마크업 존재'
Write-Host ''

# ── 참조: AC-2 (measure_ac2.py 실측 리포트) ───────────────────────
Write-Host '[AC-2] 참조 — measure_ac2.py 실측 리포트'
if (Test-Path -LiteralPath $Ac2) {
    $r = Read-File $Ac2
    $failCount = ([regex]::Matches($r, '\|\s*FAIL\s*\|')).Count
    $runs = ([regex]::Matches($r, '# AC-2 실측 리포트')).Count
    Report 'AC-2' ($failCount -eq 0 -and $runs -ge 2) ("리포트 {0}회 실행 / FAIL {1}건 — 상세는 ac2_report.md" -f $runs, $failCount)
} else {
    Report 'AC-2' $false 'ac2_report.md 없음 — python 내부_검증/measure_ac2.py 를 먼저 실행할 것'
}
Write-Host ''

# ── 보조: AC-9 산출물 존재 ────────────────────────────────────────
Write-Host '[AC-9] 보조 확인 — PDF 3종 · [모두의연구소] 명명'
# 납품물 PDF만 센다. 프로젝트 루트의 PDF(강사 이력서 등 원본 입력 자료)는 명명 규칙 대상이 아니다.
$deliverableDirs = @((Join-Path $Root '발표덱_가로'), (Join-Path $Root '배포물'))
$pdfs = @($deliverableDirs | Where-Object { Test-Path -LiteralPath $_ } |
         ForEach-Object { Get-ChildItem -LiteralPath $_ -Recurse -Filter '*.pdf' -ErrorAction SilentlyContinue })
$branded = @($pdfs | Where-Object { $_.Name.StartsWith('[모두의연구소]') })
Report 'AC-9' ($pdfs.Count -ge 3) ("PDF {0}개" -f $pdfs.Count)
Report 'AC-9' ($pdfs.Count -gt 0 -and $branded.Count -eq $pdfs.Count) ("[모두의연구소] 접두 {0}/{1}" -f $branded.Count, $pdfs.Count)
foreach ($p in $branded) {
    # 대괄호 파일명은 -LiteralPath 로만 접근한다
    $len = (Get-Item -LiteralPath $p.FullName).Length
    Write-Host ("        - {0} ({1:N0} bytes)" -f $p.Name, $len)
}
Write-Host ''

# ── 범위 밖 명시 ──────────────────────────────────────────────────
Write-Host '[AC-6] 범위 밖 — 금지 리터럴 17개 검사는 P2-8 이 최초 실행 시점이므로 이 스토리에서 판정하지 않는다.'
Write-Host ''

Write-Host ('=== 결과: PASS {0} / FAIL {1} ===' -f $script:Pass, $script:Fail)
if ($script:Fail -gt 0) { exit 1 } else { exit 0 }
