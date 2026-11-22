"""실전 연습장 미션 판정 점검: 조작 전에는 통과 0, 정답 조작 뒤에는 모두 통과해야 한다. python3 build/check_missions.py (서버: localhost:8765)"""
import asyncio, sys
from playwright.async_api import async_playwright
async def setr(page,sc,name,v):
    await page.evaluate("([sc,n,v])=>{const e=document.querySelector('#'+sc+' [name='+n+']');if(e.type==='checkbox'){e.checked=v;}else e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}",[sc,name,v])
async def done(page,sc): return await page.evaluate("sc=>[...document.querySelectorAll('#'+sc+' .missions li')].map(l=>l.classList.contains('done'))",sc)
TRUTH={'hip':[0,1,2,3,4],'up':[0,5,1],'sit':[0,7,4,8,6],'walk':[0,4,8,6]}
async def main():
    bad=0
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        page=await b.new_page();await page.route('**/fonts.g*/**',lambda r: r.abort())
        errs=[];page.on("pageerror",lambda e: errs.append(str(e)))
        await page.goto("http://localhost:8765/practice/index.html#contact");await page.wait_for_timeout(700)
        res={}
        for sc in ['contact','frill','light','homework']: res[sc+' 전']=await done(page,sc)
        # 접점 탐정
        for pose in ['hip','sit','walk']:
            await setr(page,'contact','pose',pose)
            for i in range(10): await setr(page,'contact','sp%d'%i, i in TRUTH[pose])
        res['contact 후']=await done(page,'contact')
        # 프릴 공방
        await page.click('.tabs button[data-t=frill]')
        await setr(page,'frill','band',60);await setr(page,'frill','cloth',120);await setr(page,'frill','wave',4);await setr(page,'frill','wave',8)
        res['frill 후']=await done(page,'frill')
        # 조명실
        await page.click('.tabs button[data-t=light]')
        await setr(page,'light','phi',60);await setr(page,'light','elev',-30);await setr(page,'light','phi',170)
        res['light 후']=await done(page,'light')
        # 숙제 책상
        await page.click('.tabs button[data-t=homework]')
        async def run():
            for k in range(6): await page.click(f'#homework .hw[data-k="{k}"]')
        await setr(page,'homework','pic','haru_hoodie');await run()
        await setr(page,'homework','pic','moa_sit');await setr(page,'homework','lt','below');await run()
        res['homework 후']=await done(page,'homework')
        txt=await page.text_content('#homework .promptbox pre'); res['요청문에 턱 아래']=['턱 아래가 밝다' in txt]
        for k,v in res.items():
            want=(k.endswith('전') and not any(v)) or (not k.endswith('전') and all(v))
            bad+= not want; print('OK ' if want else 'XX ',k,v)
        print('페이지 오류',errs); bad+=len(errs)
        await b.close()
    print('전체 통과' if not bad else f'문제 {bad}건'); sys.exit(1 if bad else 0)
asyncio.run(main())
