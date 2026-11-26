#!/usr/bin/env python3
"""진행 현장(#portfolio) 섹션 점검: 가로 스크롤·앵커·카드 수·지표 숫자 일치.

사용: LD_LIBRARY_PATH=/workspace/.libs python3 tools/check_portfolio.py [base_url_or_file]
기본값은 로컬 index.html (file://). 배포 후에는 라이브 URL을 인자로 준다.
"""
import os
import re
import sys

from playwright.sync_api import sync_playwright

EXE = "/workspace/.cache/ms-playwright/chromium_headless_shell-1255/chrome-headless-shell-linux64/chrome-headless-shell"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = sys.argv[1] if len(sys.argv) > 1 else "file://" + os.path.join(ROOT, "index.html")
WIDTHS = [360, 390, 768, 1440]
# 화면에 노출되는 단지명(순서 = DOM 순서)
EXPECTED = [
    "양평 서정 풀빌리지", "양평 두메이스타운", "양평 송강리 인포 타운하우스", "양평 몽피에뜨 메종",
    "킨포크 타운", "지평 그린하우스", "용문 몽피에뜨", "양평 송학리 전원주택",
    "현진에버빌", "용인 베일 노블리스", "대조1구역", "영등포구 양평동 오피스텔", "여주 그린하우스",
    "상지카일룸 블랙", "포도 더 블랙",
]

fail = 0


def check(label, ok, detail=""):
    global fail
    if not ok:
        fail += 1
    print(("PASS " if ok else "FAIL ") + label + ((" — " + detail) if detail else ""))


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=EXE)
    for w in WIDTHS:
        page = browser.new_page(viewport={"width": w, "height": 900})
        page.goto(BASE, wait_until="load")
        page.wait_for_timeout(400)
        sw = page.evaluate("document.documentElement.scrollWidth")
        iw = page.evaluate("window.innerWidth")
        check(f"{w}px 가로 스크롤 없음 (scrollWidth={sw}, innerWidth={iw})", sw <= iw + 1)
        # 넘치는 요소 찾기 (가로 스크롤이 있을 때만)
        if sw > iw + 1:
            over = page.evaluate(
                """() => Array.from(document.querySelectorAll('body *'))
                    .filter(el => { const r = el.getBoundingClientRect();
                                    return r.right > window.innerWidth + 1 && r.width > 0; })
                    .slice(0, 12)
                    .map(el => el.tagName.toLowerCase() + '.' + (el.className || '').toString().split(' ')[0]
                         + ' right=' + Math.round(el.getBoundingClientRect().right))"""
            )
            print("   넘치는 요소:", over)
        # 카드 폭이 0이거나 겹치지 않는지
        box = page.evaluate(
            """() => { const c = document.querySelectorAll('#portfolio .site-card');
                       let zero = 0; c.forEach(el => { if (el.getBoundingClientRect().width < 40) zero++; });
                       return {cards: c.length, zero}; }"""
        )
        check(f"{w}px 카드 렌더 (카드 {box['cards']}장, 폭 이상 {box['zero']}장)", box["zero"] == 0)
        # 단지명 노출·카드 안에서 잘리거나 겹치지 않는지
        lay = page.evaluate(
            """() => {
                const out = {noName: [], clipped: [], overlap: [], uneven: []};
                const cards = Array.from(document.querySelectorAll('#portfolio .site-card'));
                const rows = {};
                cards.forEach((c, i) => {
                    const name = c.querySelector('.site-card-name');
                    const txt = name ? name.textContent.trim() : '';
                    if (!txt || (name && name.getBoundingClientRect().width < 40)) out.noName.push(i);
                    const cr = c.getBoundingClientRect();
                    const padB = parseFloat(getComputedStyle(c).paddingBottom);
                    Array.from(c.children).forEach(el => {
                        const r = el.getBoundingClientRect();
                        if (r.bottom > cr.bottom - padB + 1.5 || r.right > cr.right + 1) out.clipped.push(i + ':' + (el.className || el.tagName));
                    });
                    // 같은 카드 안 형제 요소끼리 세로로 겹치는지
                    const kids = Array.from(c.children).map(el => el.getBoundingClientRect());
                    for (let k = 1; k < kids.length; k++) {
                        if (kids[k].top < kids[k - 1].bottom - 1.5) out.overlap.push(i);
                    }
                    // 같은 줄 카드 높이가 같은지 (grid stretch)
                    const key = Math.round(cr.top);
                    (rows[key] = rows[key] || []).push(cr.height);
                });
                Object.values(rows).forEach(hs => {
                    if (Math.max(...hs) - Math.min(...hs) > 1) out.uneven.push(hs.map(h => Math.round(h)).join('/'));
                });
                const names = cards.map(c => (c.querySelector('.site-card-name') || {}).textContent || '').map(t => t.trim());
                return {...out, names};
            }"""
        )
        check(f"{w}px 카드 15장 모두 단지명 노출", not lay["noName"], str(lay["noName"]))
        check(f"{w}px 카드 안 텍스트 잘림 없음", not lay["clipped"], str(lay["clipped"]))
        check(f"{w}px 카드 내부 요소 겹침 없음", not lay["overlap"], str(lay["overlap"]))
        check(f"{w}px 같은 줄 카드 높이 동일", not lay["uneven"], str(lay["uneven"]))
        if w == 360:
            NAMES_AT_360 = lay["names"]
        page.close()

    page = browser.new_page(viewport={"width": 390, "height": 900})
    page.goto(BASE, wait_until="load")
    info = page.evaluate(
        """() => {
            const groups = Array.from(document.querySelectorAll('#portfolio .site-group')).map(g => ({
                head: g.querySelector('.site-group-head span').textContent.trim(),
                count: g.querySelector('.site-group-count').textContent.trim(),
                cards: g.querySelectorAll('.site-card').length
            }));
            const stats = Array.from(document.querySelectorAll('#portfolio .pf-stat-num')).map(e => e.textContent.trim());
            return {groups, stats, h2: document.querySelector('#portfolio h2').textContent.trim()};
        }"""
    )
    print("그룹:", info["groups"])
    print("지표:", info["stats"])
    print("h2:", info["h2"])

    # 단지명 목록·순서 확인
    print("단지명:", NAMES_AT_360)
    check(f"단지명 목록 일치 ({len(EXPECTED)}개)", NAMES_AT_360 == EXPECTED, str([n for n in EXPECTED if n not in NAMES_AT_360]))
    check("'용문'만 적힌 카드 없음", "용문" not in NAMES_AT_360 and "지평" not in NAMES_AT_360)

    total = sum(g["cards"] for g in info["groups"])
    for g in info["groups"]:
        check(f"'{g['head']}' 카드 수 {g['cards']} = 표기 {g['count']}", f"{g['cards']}곳" == g["count"])
    check(f"카드 합계 {total} = 지표 첫 칸", info["stats"][0].startswith(str(total)))
    check(f"h2에 '{total}곳' 표기", f"{total}곳" in info["h2"])
    check(f"권역 지표 = 그룹 수 {len(info['groups'])}", info["stats"][3].startswith(str(len(info["groups"]))))

    # 앵커 검증: 모든 href="#..." / x.html#... 대상 id 존재
    anchors = page.evaluate(
        """() => Array.from(document.querySelectorAll('a[href*="#"]')).map(a => a.getAttribute('href'))"""
    )
    bad = []
    for href in sorted(set(anchors)):
        if href in ("#", "#main"):
            continue
        frag = href.split("#", 1)[1]
        if not frag:
            continue
        target = href.split("#", 1)[0]
        url = BASE if target in ("", "index.html") else BASE.rsplit("/", 1)[0] + "/" + target
        ctx = browser.new_page(viewport={"width": 390, "height": 900})
        ctx.goto(url, wait_until="load")
        exists = ctx.evaluate("id => !!document.getElementById(id)", frag)
        ctx.close()
        if not exists:
            bad.append(href)
    check("깨진 앵커 없음", not bad, str(bad))

    browser.close()

print("\n결과:", "모두 통과" if fail == 0 else f"{fail}건 실패")
sys.exit(0 if fail == 0 else 1)
