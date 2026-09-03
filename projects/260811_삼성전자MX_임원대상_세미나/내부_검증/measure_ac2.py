# -*- coding: utf-8 -*-
"""AC-2 가독성 게이트 — 어떤 슬라이드도 축소되지 않는다.

판정: 모든 .fit-content의 computed transform이 none 또는 scale >= 0.999.
근거: 덱의 fitContent()는 축소 전용(확대 분기 없음)이므로,
      "축소 없음"과 "참조 덱 토큰 크기가 그대로 유지됨"이 동등한 명제가 된다.
      따라서 컴포넌트별 폰트 하한표는 판별력이 0이며 쓰지 않는다. (계획 v3 ADR-003)

사용:
  python measure_ac2.py                # 정상 렌더
  python measure_ac2.py --font-break   # 폰트 폴백 재현 (Pretendard → PretendardZZ 치환 사본)
  python measure_ac2.py --only 2,3     # 특정 슬라이드만

주의: 이 머신에는 Pretendard가 시스템 폰트로 설치되어 있어 CDN 차단만으로는
      폴백 경로를 타지 않는다. 그래서 --font-break는 패밀리명 자체를 치환한다.
"""
import io, os, re, sys, argparse, pathlib

sys.stdout.reconfigure(encoding='utf-8')

HERE = pathlib.Path(__file__).resolve().parent
DECK = HERE.parent / '발표덱_가로' / '삼성전자MX_임원_토큰최적화_발표덱_가로.html'
REPORT = HERE / 'ac2_report.md'
FLOOR = 0.999


def build_target(font_break: bool) -> pathlib.Path:
    if not font_break:
        return DECK
    html = io.open(DECK, encoding='utf-8').read()
    # 패밀리명을 존재하지 않는 이름으로 바꿔 실제 폴백 경로를 강제한다
    html = html.replace("'Pretendard'", "'PretendardZZ'").replace('pretendard.min.css', 'pretendard-absent.css')
    tmp = HERE / '_fontbreak.html'
    io.open(tmp, 'w', encoding='utf-8').write(html)
    return tmp


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--font-break', action='store_true')
    ap.add_argument('--only', default='')
    args = ap.parse_args()

    only = {int(x) for x in args.only.split(',') if x.strip()} if args.only else None
    target = build_target(args.font_break)
    mode = 'font-break' if args.font_break else 'normal'

    from playwright.sync_api import sync_playwright

    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1280, 'height': 720})
        page.goto(target.as_uri(), wait_until='load')
        page.wait_for_timeout(900)  # load 훅의 fitContent 일괄 실행 대기

        total = page.evaluate("document.querySelectorAll('.slide').length")
        for i in range(total):
            n = i + 1
            if only and n not in only:
                continue
            # 각 슬라이드를 활성화하고 재측정 (숨은 슬라이드도 scrollHeight는 유효하나
            # 활성 상태에서 재실행해 실제 표시 조건과 일치시킨다)
            page.evaluate("""(i)=>{
                const s=document.querySelectorAll('.slide');
                s.forEach(x=>x.classList.remove('is-active'));
                s[i].classList.add('is-active');
                if (typeof fitContent==='function') fitContent(s[i]);
            }""", i)
            page.wait_for_timeout(120)
            m = page.evaluate("""(i)=>{
                const s=document.querySelectorAll('.slide')[i];
                const fr=s.querySelector('.fit-frame'), c=s.querySelector('.fit-content');
                const t=getComputedStyle(c).transform;
                let sc=1;
                if (t && t!=='none'){ const v=t.match(/matrix\\(([^)]+)\\)/); if(v) sc=parseFloat(v[1].split(',')[0]); }
                const h2=s.querySelector('h2');
                return {scale:sc, need:c.scrollHeight, avail:fr.clientHeight,
                        title:(h2?h2.textContent:(s.querySelector('h1')?'(표지)':'')).trim().slice(0,34)};
            }""", i)
            rows.append((n, m['title'], m['need'], m['avail'], m['scale']))
        browser.close()

    if args.font_break and target != DECK:
        try:
            os.remove(target)
        except OSError:
            pass

    fails = [r for r in rows if r[4] < FLOOR]
    lines = ['# AC-2 실측 리포트 — ' + mode, '',
             '판정 기준: 모든 `.fit-content`의 scale >= %.3f (축소 없음)' % FLOOR, '',
             '| # | 슬라이드 | need | avail | 여유 | scale | 판정 |', '|---|---|---|---|---|---|---|']
    for n, title, need, avail, sc in rows:
        lines.append('| %d | %s | %d | %d | %+d | %.4f | %s |'
                     % (n, title, need, avail, avail - need, sc, 'PASS' if sc >= FLOOR else 'FAIL'))
    lines += ['', '결과: %d장 중 %d장 통과, %d장 실패' % (len(rows), len(rows) - len(fails), len(fails))]
    if fails:
        lines.append('')
        lines.append('실패 시 조치는 폰트 확대가 아니라 **내용 축소**다 (ADR-003).')
    body = '\n'.join(lines) + '\n'

    prev = io.open(REPORT, encoding='utf-8').read() if REPORT.exists() else ''
    keep = '' if mode in prev.split('\n')[0] else prev
    io.open(REPORT, 'w', encoding='utf-8').write((keep + '\n\n' if keep else '') + body)

    print(body)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
