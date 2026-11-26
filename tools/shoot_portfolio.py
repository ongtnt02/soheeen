#!/usr/bin/env python3
"""진행 현장 섹션 스크린샷 (390 / 1440). 사용: ... shoot_portfolio.py <base_url> <out_dir> <suffix>
"""
import os
import sys

from playwright.sync_api import sync_playwright

EXE = "/workspace/.cache/ms-playwright/chromium_headless_shell-1255/chrome-headless-shell-linux64/chrome-headless-shell"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = sys.argv[1] if len(sys.argv) > 1 else "file://" + os.path.join(ROOT, "index.html")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "screenshots-20261126")
SUFFIX = sys.argv[3] if len(sys.argv) > 3 else "-17"
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=EXE)
    for w, tag in ((390, "m"), (1440, "d")):
        page = browser.new_page(viewport={"width": w, "height": 900}, device_scale_factor=2 if w == 390 else 1)
        page.goto(BASE, wait_until="load")
        page.wait_for_timeout(300)
        # 요소 캡처에서 고정 헤더가 겹치지 않게 하고, 스크롤 진입 모션은 끈 상태로 찍는다
        page.add_style_tag(
            content="header.site-header,.site-header{position:static!important}"
            "#portfolio .site-card{opacity:1!important;animation:none!important;transform:none!important}"
        )
        page.evaluate(
            """() => { document.querySelectorAll('#portfolio .site-card').forEach(el => el.classList.add('is-in')); }"""
        )
        page.wait_for_timeout(700)
        sec = page.query_selector("#portfolio")
        path = os.path.join(OUT, f"portfolio{SUFFIX}-{tag}.png")
        sec.screenshot(path=path)
        print(path, os.path.getsize(path))
        page.close()
    browser.close()
