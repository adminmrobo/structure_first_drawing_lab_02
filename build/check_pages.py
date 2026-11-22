"""페이지 점검: 콘솔 오류, 실험 패널 실패, 390·1280px 가로 넘침, 패널 스크린샷. python3 build/check_pages.py (서버: localhost:8765)"""
import asyncio, sys, os
from playwright.async_api import async_playwright
PAGES = ["index.html", "01_standing.html", "02_frills.html", "03_sitting.html", "04_light_dir.html", "practice/index.html"]
SHOT = "/tmp/shots"; os.makedirs(SHOT, exist_ok=True)
async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for w in (1280, 390):
            pg = await b.new_page(viewport={"width": w, "height": 900})
            await pg.route("**/fonts.g*/**", lambda r: r.abort())
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            for u in PAGES:
                errs.clear()
                await pg.goto("http://localhost:8765/" + u); await pg.wait_for_timeout(900)
                ov = await pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                fail = await pg.evaluate("[...document.querySelectorAll('[data-panel]')].filter(h=>h.textContent.includes('불러오지 못했습니다')).map(h=>h.dataset.panel)")
                wide = await pg.evaluate("[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>window.innerWidth+1&&r.width>0&&getComputedStyle(e).position!=='fixed'}).slice(0,5).map(e=>e.tagName+'.'+e.className)")
                real = [e for e in errs if "fonts" not in e and "ERR_FAILED" not in e]
                st = "OK" if not real and not fail and ov <= 0 else "XX"
                if st == "XX": bad += 1
                print(st, w, u, "넘침", ov, "패널실패", fail, "오류", real[:3], wide if ov > 0 else "")
                if w == 1280 and u not in ("index.html",):
                    for h in await pg.query_selector_all("[data-panel]"):
                        k = await h.get_attribute("data-panel"); par = await h.evaluate_handle("e=>e.parentNode")
                        await par.as_element().screenshot(path=f"{SHOT}/{k}.png")
            await pg.close()
        await b.close()
    print("전체 통과" if bad == 0 else f"문제 {bad}건"); sys.exit(1 if bad else 0)
asyncio.run(main())
