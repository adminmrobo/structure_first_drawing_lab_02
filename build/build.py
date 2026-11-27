# -*- coding: utf-8 -*-
"""구조 먼저 그리기 연구실 02 · 실천편 — 페이지 빌드.
python3 build/build.py 로 index.html, 01~04 페이지, practice/index.html 을 다시 만든다.
그림 파일(assets/img/{키}.webp)이 있으면 넣고, 없으면 '그림 준비 중' 자리만 둔다."""
import json, os, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_a import P1, P2
from content_b import P3, P4
from prompt_lab import PL, PAIR_NOTE, PAIR_SEEN, PAIR_LESSON, STYLE as PSTYLE, NEG as PNEG, CHAR as PCHAR
from make_lab import EX, a_prompt, a_key, SEEN, MK_LESSON, RETRY, RETRY_SEEN, RETRY_LESSON, RETRY3, RETRY3_SEEN
from prompt_data import BODY as DBODY, NEG as DNEG, ARW as DARW, HARU as DHARU, SIA as DSIA, MOA as DMOA, BODYS as DBODYS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = "v1.0"
DATE = "2026-11-23"
SITE = "https://adminmrobo.github.io/structure_first_drawing_lab_02/"
REPO = "https://github.com/adminmrobo/structure_first_drawing_lab_02"
BASE = "https://adminmrobo.github.io/adminmrobo-structure_first_drawing_lab/"
AUTHOR_URL = "https://adminmrobo.github.io/who_am_i/who_am_i.html"
CHARREPO = "https://github.com/adminmrobo/fruitfly-lab-expressions"
SERIES = "구조 먼저 그리기 연구실 02 · 실천편"
E = html.escape
PARTS = [P1, P2, P3, P4]
PXFIX = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "px_fix.html")).read()  # 픽셀 깨짐 보정(px-fix v1)

CH = {
 "doctor": ("박사", "해설. 단계마다 현장 질문으로 열고 해석 문장으로 닫는다"),
 "haru": ("조수 하루", "모델(1부, 후드 집업) + 수식 상자 담당. 어려운 식을 대신 묻는다"),
 "sia": ("시아", "인턴1 · 모델(2부). 프릴 많은 메이드복의 주인공"),
 "moa": ("모아", "인턴2 · 모델(3부). 블레이저를 입고 바닥에 앉는다"),
 "jupanbot": ("주판봇", "화가 A. 주름·그림자를 감으로 먼저 넣는다 — 흔한 실수 담당"),
 "fruitfly": ("초파리 연구원", "화가 B. 접점과 광원부터 찾는다. \"이걸 눌러 봐\""),
 "x1": ("X1", "평가단. 닮음을 본다"),
 "x2": ("X2", "평가단. 입체감을 본다"),
 "x3": ("X3", "평가단. 자연스러움을 본다"),
}
COLOR = {"doctor": "doc", "haru": "asst", "fruitfly": "fly", "jupanbot": "robo", "sia": "sia", "moa": "moa", "x1": "x", "x2": "x", "x3": "x"}

def face(k, e="e13", pre="", cls=""):
    n = CH[k][0]
    return f'<img src="{pre}assets/chars/{k}_{e}.webp" alt="{E(n)}" width="96" height="96" loading="lazy"{(" class=%s" % cls) if cls else ""}>'

def has_img(key):
    return os.path.exists(os.path.join(ROOT, "assets", "img", key + ".webp"))

def art(key, alt, ar="16/9", cap=None, pre="", cls=""):
    cap_html = f"<figcaption>{E(cap)}</figcaption>" if cap else ""
    if has_img(key):
        return f'<figure class="art {cls}" data-img="{key}"><img src="{pre}assets/img/{key}.webp" alt="{E(alt)}" loading="lazy" decoding="async">{cap_html}</figure>'
    return (f'<figure class="art {cls}" data-img="{key}"><div class="ph-art" style="--ar:{ar}" role="img" aria-label="{E(alt)}">'
            f'<b>그림 준비 중 · {key}</b><span>{E(alt)}</span></div>{cap_html}</figure>')

def head(title, desc, og, path, pre=""):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:type" content="article"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}assets/og/{og}"><meta property="og:url" content="{SITE}{path}"><meta name="twitter:card" content="summary_large_image">
<meta name="author" content="안상선">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/lab.css">
{PXFIX}</head>
<body data-root="{pre}">
<div id="prog"></div>
"""

def nav(links, pre=""):
    a = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in links)
    return f'<nav class="top"><div class="row"><a class="logo" href="{pre}index.html">구조 먼저 <i>실천편</i></a><div class="links">{a}</div></div></nav>\n'

def cover(key, cap, cast, pre=""):
    if has_img(key):
        return f'<div class="cover"><div class="frame" data-img="{key}"><img class="art" src="{pre}assets/img/{key}.webp" alt="{E(cap)}" width="1920" height="1080" fetchpriority="high" decoding="async"></div></div>\n'
    # 그림이 오기 전 픽셀 대체 표지: 네모 격자 + 상자·원기둥 마네킹(픽셀 블록) + 픽셀 캐릭터
    cells = []
    for x in range(0, 1600, 40):
        for y in range(0, 900, 40):
            if (x // 40 + y // 40) % 2 == 0:
                cells.append(f'<rect x="{x}" y="{y}" width="40" height="40" fill="#f3f6fa"/>')
    blocks = [(1180, 140, 80, 100, "#c9d3e6"), (1200, 240, 40, 30, "#d8dfeb"), (1150, 270, 140, 140, "#b9c6df"), (1160, 410, 120, 90, "#a9b8d6"),
              (1110, 280, 40, 120, "#cdd6e8"), (1290, 280, 40, 120, "#cdd6e8"), (1100, 400, 40, 100, "#dfe5ef"), (1300, 400, 40, 100, "#dfe5ef"),
              (1170, 500, 50, 170, "#b9c6df"), (1230, 500, 50, 170, "#b9c6df"), (1170, 670, 50, 130, "#a9b8d6"), (1230, 670, 50, 130, "#a9b8d6")]
    bl = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="#1e2f6e" stroke-width="6"/>' for x, y, w, h, c in blocks)
    easel = '<rect x="240" y="180" width="300" height="380" fill="#ffffff" stroke="#8a5a2b" stroke-width="12"/><rect x="270" y="560" width="20" height="260" fill="#8a5a2b"/><rect x="490" y="560" width="20" height="260" fill="#8a5a2b"/>' + \
            "".join(f'<rect x="{300+i*40}" y="{240+j*40}" width="40" height="40" fill="{c}"/>' for i, j, c in [(1,0,"#e9909a"),(2,0,"#e9909a"),(1,1,"#f6d3b8"),(2,1,"#f6d3b8"),(0,2,"#a99ac8"),(1,2,"#a99ac8"),(2,2,"#a99ac8"),(3,2,"#a99ac8"),(1,3,"#fbfbfd"),(2,3,"#fbfbfd"),(1,4,"#5b7fb8"),(2,4,"#5b7fb8")])
    imgs = "".join(face(k, e, pre) for k, e in cast)
    return f"""<div class="cover"><div class="frame" data-img="{key}"><svg class="grid" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true" shape-rendering="crispEdges">{''.join(cells)}{easel}{bl}</svg>
<span class="cap">{E(cap)}</span><span class="badge">표지 그림 준비 중 · {key}</span><div class="cast" style="image-rendering:pixelated">{imgs}</div></div></div>
"""

def three(a, b, c, abbr):
    dl = "".join(f"<dt>{E(x)}</dt><dd>{E(y)}</dd>" for x, y in abbr)
    return f"""<div class="three"><h2>처음 오신 분께 — 세 줄 요약</h2><ul>
<li><b>무엇을</b>: {E(a)}</li><li><b>왜 중요한가</b>: {E(b)}</li><li><b>작업에서는</b>: {E(c)}</li></ul>
<p>그림 실력·코드·수식을 몰라도 됩니다. 실험을 눌러 보며 따라오세요.</p>
<details class="abbr"><summary>낱말·약어 풀이 (펼치기)</summary><dl>{dl}</dl></details></div>\n"""

ABBR = [("접점", "천이 몸에 걸리거나 붙잡힌 곳. 주름의 출발점"), ("꼭대기", "가슴·무릎처럼 가장 볼록해 천이 걸려 버티는 곳"),
        ("당김 주름 · 모임 주름 · 처짐 주름", "힘이 당겨서 / 남는 천이 모여서 / 중력으로 늘어져서 생긴 주름"),
        ("입체 그림자", "빛을 등진 면에 생기는 그림자(陰)"), ("떨어지는 그림자", "다른 물체가 빛을 가려 생기는 그림자(影)"),
        ("개더 · 프릴", "긴 천을 짧은 띠에 줄여 꿰매 만든 물결 주름"), ("플리츠(주름치마)", "같은 간격으로 접어 다린 주름"),
        ("고정 주름", "단추처럼 천을 한 점에 붙잡은 곳에서 퍼지는 주름"), ("라디안", "각도를 '반지름 몇 개만큼의 호'로 잰 단위. 180° = 3.14"),
        ("깊이 지도", "가까울수록 밝게 칠한 흑백 그림. AI에 겹침 순서를 알려 준다"), ("노멀 지도", "면이 향한 방향을 빨강·초록·파랑으로 저장한 그림"),
        ("다시 조명(리라이팅)", "그림을 다시 그리지 않고 광원만 바꿔 그림자를 새로 계산하는 일")]

def talk(lines, pre=""):
    out = []
    for k, e, t in lines:
        side = " r" if k in ("moa", "sia") else ""
        out.append(f'<div class="line{side}">{face(k, e, pre)}<div class="bub"><b style="color:var(--c-{COLOR[k]})">{E(CH[k][0])}</b>{E(t)}</div></div>')
    return '<div class="talk">' + "".join(out) + "</div>"

def quiz(q, opts, ans, ok, no):
    b = "".join(f'<button type="button">{E(o)}</button>' for o in opts)
    return f'<div class="quiz" data-ans="{ans}"><div class="qq">확인 퀴즈 — {E(q)}</div><div class="opts">{b}</div><div class="fb" aria-live="polite"></div><span class="qok" hidden>{E(ok)}</span><span class="qno" hidden>{E(no)}</span></div>'

def panel(no, i, p):
    return (f'<div class="panel"><div class="ph"><b>실험 {no}-{i}</b><small>{E(p["note"])}</small></div>'
            f'<div id="pp-{p["key"]}" data-panel="{p["key"]}"></div><div class="ctrl">{p["ctrl"]}</div><div class="readout" aria-live="polite"></div></div>')

def mathbox(m):
    tries = "".join(f"<div>{E(t)}</div>" for t in m["tries"])
    pcs = "".join(f"<tr><td class='m'>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in m["pieces"])
    return f"""<div class="box mathbox"><h4>수학 수식을 어려워하는 조수가 대신 물어봅니다</h4>
<div class="q">{face('haru','e04')}<div><b>조수</b> {E(m['ask'])}</div></div>
<div class="easy"><b>말로 하면</b> — {E(m['words'])}</div>
<p><b>학교 수학으로 보면</b> — {E(m['school'])}</p>
<div class="fx">{E(m['formula'])}</div>
<table><thead><tr><th>식 조각</th><th>뜻</th></tr></thead><tbody>{pcs}</tbody></table>
<div class="try"><b>숫자로 한 번 해 보기</b>{tries}</div>
<div class="q">{face('haru','e16')}<div><b>조수</b> {E(m['comment'])}</div></div></div>"""

def step(P, i, s):
    no = P["no"]
    labels = ["무엇이 문제인가", "그냥 하면 막히는 곳", "이렇게 푼다"]
    why = "".join(f"<li><b>{labels[k]}</b> — {E(x)}</li>" for k, x in enumerate(s["why"]))
    whybox = f'<div class="box why"><h4>왜 이렇게 하나</h4><ol>{why}</ol><div class="easy"><b>쉽게 말하면</b> — {E(s["easy"])}</div></div>'
    calm = talk([("doctor", "e08", "여기서 한 번 멈춰도 괜찮아요. 식이 낯설면 건너뛰고 아래 실험부터 눌러 보세요. 숫자는 실험이 대신 계산해 줍니다.")])
    duo = f'<div class="duo">{whybox}{mathbox(s["math"])}</div>{calm}' if s.get("math") else f'<div style="margin:16px 0">{whybox}</div>'
    solve = "".join(f"<p>{E(x)}</p>" for x in s["solve"])
    extra = ""
    if s.get("order"):
        extra += order_box(s["order"])
    img = art(s["img"][0], s["img"][1], s["img"][2], s["img"][1], cls="tall" if s["img"][2] == "2/3" else "") if s.get("img") else ""
    q = s["quiz"]
    return f"""<section class="room" id="{s['id']}"><div class="wrap">
<div class="roomno">{no}부 · {i}단계</div>
<h2>{E(s['title'])}</h2><p class="muted">{E(s['sub'])}</p>
<div class="tags"><span class="tag how">{E(s['how'])}</span><span class="tag day">{E(s['day'])}</span></div>
{duo}
<div class="pair"><div class="box"><h4>일상으로 치면</h4><p>{E(s['daily'])}</p></div><div class="box ml"><h4>그림·VFX 현장에서는</h4><p>{E(s['field'])}</p></div></div>
{talk(s['talk'])}
{panel(no, i, s['panel'])}
<div class="solve"><h4>실험 결과 읽기</h4>{solve}</div>
{extra}{img}
<div class="solve"><h4>AI 결과, 그대로 써도 될까?</h4><p>{E(s['ai'][0])}</p><details class="code"><summary>확인해 보기</summary><p>{E(s['ai'][1])}</p></details></div>
<div class="limit"><b>주의할 점</b> — {E(s['limit'])}</div>
{quiz(q[0], q[1], q[2], q[3], q[4])}
</div></section>
"""

def judge(J):
    rows = ""
    for idx, item in enumerate(J["items"]):
        a, b = J["a"][1][idx], J["b"][1][idx]
        mx = 8 if "8개" in item else 10
        rows += f'<span>{E(item)}</span><span class="bar" title="{J["a"][0]} {a}"><i style="width:{a/mx*100:.0f}%"></i></span><span class="bar" title="{J["b"][0]} {b}"><i style="width:{b/mx*100:.0f}%;background:var(--teal)"></i></span>'
    sa, sb = sum(J["a"][1]), sum(J["b"][1])
    tbl = "".join(f"<tr><td>{E(it)}</td><td>{J['a'][1][k]}</td><td>{J['b'][1][k]}</td></tr>" for k, it in enumerate(J["items"]))
    return f"""<section class="room" id="judge"><div class="wrap"><div class="roomno">평가단 채점</div><h2>{E(J['title'])}</h2>
{talk(J['setup'])}
<div class="judge"><h4>평가단 X1·X2·X3의 점수</h4>
<div class="score"><span></span><b>{E(J['a'][0])}</b><b>{E(J['b'][0])}</b>{rows}</div>
<div class="tbl" style="margin-top:10px"><table><thead><tr><th>항목</th><th>{E(J['a'][0])}</th><th>{E(J['b'][0])}</th></tr></thead><tbody>{tbl}<tr><th>합계</th><th>{sa}</th><th>{sb}</th></tr></tbody></table></div>
{talk(J['comments'])}</div>
{talk(J['result'])}
<p class="hint">점수는 이야기 속 예시입니다. 실제 그림을 평가한 값이 아닙니다.</p>
</div></section>
"""

def summary(P):
    rows = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in P["summary"])
    return f"""<section id="sum"><div class="wrap"><h2>{P['no']}부 정리</h2>
<div class="tbl"><table><thead><tr><th>주제</th><th>핵심</th><th>작업에서는</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>
"""

def outro(P):
    return f"""<section id="outro"><div class="wrap"><h2>다음으로</h2>{talk(P['outro'])}
<div class="next"><a href="{P['prev'][0]}">{E(P['prev'][1])}</a><a href="{P['next'][0]}">{E(P['next'][1])}</a></div></div></section>
"""


def order_box(o):
    return ""

# ---------------- 지식 색인
KG = [
 ("concept/contact-point", "Concept", "접점", "Contact points", "01_standing.html", "#s1", "천이 몸에 걸리거나 붙잡힌 곳. 주름은 여기서 시작한다"),
 ("concept/bend-difference", "Concept", "굽힌 관절의 길이 차", "Inner/outer length at a bent joint", "01_standing.html", "#s2", "바깥 − 안쪽 = 두께 × 굽힌 각(라디안)"),
 ("concept/peak-direction", "Concept", "꼭대기와 주름 방향", "Folds point toward the peak", "01_standing.html", "#s3", "주름은 접점과 볼록한 꼭대기를 잇는다"),
 ("method/big-form-first", "Method", "큰 형체 그림자 먼저", "Big-form shading first", "01_standing.html", "#s4", "광원 → 구·원기둥 그림자 → 주름 그림자"),
 ("concept/step-shadow", "Concept", "단차의 떨어지는 그림자", "Cast shadow under a small step", "01_standing.html", "#s5", "그림자 길이 = 단차 높이 ÷ tan(빛이 면과 이루는 각)"),
 ("concept/gather-ratio", "Concept", "개더 비율과 프릴", "Gather ratio and ruffles", "02_frills.html", "#s1", "물결 하나에 든 천 = 물결 폭 × 비율"),
 ("concept/cinch", "Concept", "조임 주름", "Cinched folds", "02_frills.html", "#s2", "조인 선을 향해 위아래에서 모인다"),
 ("method/coarse-to-fine", "Method", "큰 선 먼저, 잔물결 나중", "Coarse-to-fine drawing", "02_frills.html", "#s3", "덩어리 → 중간 물결 → 레이스"),
 ("method/paired-guides", "Method", "짝 장식 기준선", "Paired ornaments on guide lines", "02_frills.html", "#s4", "높이 차 = 가로 거리 × tan(몸의 기울기)"),
 ("concept/mixed-shadow", "Concept", "섞인 그림자와 그림자의 주인", "Mixed form and cast shadows", "02_frills.html", "#s5", "떨어지는 그림자는 위 천의 윤곽을 닮는다"),
 ("concept/sitting-joints", "Concept", "앉은 자세의 관절 주름", "Folds at many bent joints", "03_sitting.html", "#s1", "관절마다 두께 × 각으로 남는 천을 비교"),
 ("concept/anchor-fold", "Concept", "고정 주름(단추)", "Anchor folds at a button", "03_sitting.html", "#s2", "단추가 붙잡은 점에서 퍼지는 당김 주름"),
 ("concept/stiff-fabric", "Concept", "빳빳한 천과 깃 잇기", "Stiff fabric and hidden lines", "03_sitting.html", "#s3", "단단할수록 주름이 적고 굵게 꺾인다"),
 ("concept/pleat-spread", "Concept", "퍼진 주름치마", "Spreading pleats", "03_sitting.html", "#s4", "주름 하나의 폭 = 둘레 ÷ 주름 개수"),
 ("method/depth-order", "Method", "겹침 순서와 깊이 지도", "Depth ordering", "03_sitting.html", "#s5", "앞 물체가 뒤 물체에 그림자를 드리운다"),
 ("concept/light-direction", "Concept", "광원 방향과 그림자", "Light direction", "04_light_dir.html", "#s1", "그림자는 빛의 반대쪽 면"),
 ("concept/under-light", "Concept", "아래에서 오는 빛", "Under-lighting", "04_light_dir.html", "#s2", "아랫면이 밝고 윗면이 어둡다"),
 ("concept/side-cast", "Concept", "옆 빛과 팔 그림자", "Side light and cast shadow offset", "04_light_dir.html", "#s3", "밀린 거리 = 앞뒤 거리 × tan(각)"),
 ("concept/lit-fraction", "Concept", "위에서 본 광원 각도", "Visible lit fraction of a cylinder", "04_light_dir.html", "#s4", "보이는 밝은 폭 = (1 + cos φ) ÷ 2"),
 ("method/relighting", "Method", "노멀 지도로 다시 조명", "Normal-map relighting", "04_light_dir.html", "#s5", "밝기 = max(0, 면 방향 · 빛 방향)"),
 ("application/practice", "Application", "실전 연습장", "Practice simulator", "practice/index.html", "#contact", "접점·프릴·조명·숙제 순서를 직접 운영해 본다"),
 ("analogy/clothespin", "Analogy", "빨래집게", "Clothespin", "01_standing.html", "#s1", "집게가 곧 접점이다"),
 ("analogy/curtain", "Analogy", "커튼 물결", "Curtain waves", "02_frills.html", "#s1", "봉보다 긴 천이 물결이 된다"),
 ("analogy/fan", "Analogy", "접이식 부채", "Folding fan", "03_sitting.html", "#s4", "개수는 그대로, 끝으로 갈수록 넓어진다"),
 ("analogy/sundial", "Analogy", "해시계", "Sundial", "04_light_dir.html", "#s5", "면은 그대로, 빛만 움직인다"),
]
KG_EDGES = [("concept/contact-point","motivates","concept/bend-difference"),("concept/bend-difference","motivates","concept/peak-direction"),
 ("concept/peak-direction","motivates","method/big-form-first"),("method/big-form-first","motivates","concept/step-shadow"),
 ("concept/contact-point","motivates","concept/gather-ratio"),("concept/gather-ratio","motivates","concept/cinch"),("concept/cinch","motivates","method/coarse-to-fine"),
 ("method/coarse-to-fine","motivates","method/paired-guides"),("method/paired-guides","motivates","concept/mixed-shadow"),("concept/step-shadow","explains","concept/mixed-shadow"),
 ("concept/bend-difference","explains","concept/sitting-joints"),("concept/sitting-joints","motivates","concept/anchor-fold"),("concept/anchor-fold","motivates","concept/stiff-fabric"),
 ("concept/stiff-fabric","motivates","concept/pleat-spread"),("concept/pleat-spread","motivates","method/depth-order"),("concept/mixed-shadow","explains","method/depth-order"),
 ("method/big-form-first","motivates","concept/light-direction"),("concept/light-direction","motivates","concept/under-light"),("concept/under-light","motivates","concept/side-cast"),
 ("concept/side-cast","motivates","concept/lit-fraction"),("concept/lit-fraction","motivates","method/relighting"),("method/depth-order","explains","concept/side-cast"),
 ("concept/contact-point","usedIn","application/practice"),("concept/gather-ratio","usedIn","application/practice"),("concept/lit-fraction","usedIn","application/practice"),
 ("analogy/clothespin","explains","concept/contact-point"),("analogy/curtain","explains","concept/gather-ratio"),("analogy/fan","explains","concept/pleat-spread"),("analogy/sundial","explains","method/relighting")]
REFS = [
 dict(id="date_2018_wrinkles", title="デジタルツールで描く！服のシワと影の描き方", author="ダテナオト", year=2018, note="マイナビ出版. 3장 실천편(p.131~143)과 출판사 특전 PDF의 연습 구성(서 있는 자세·주름 많은 옷·앉은 자세·광원 방향별 그림자)을 참고. 그림·문장·사진·도식은 옮기지 않고 연구실 캐릭터와 실험으로 새로 구성"),
 dict(id="lambert_1760", title="Photometria (Lambert's cosine law)", author="Johann Heinrich Lambert", year=1760, note="면의 밝기 = cos θ = 면 방향 · 빛 방향. https://en.wikipedia.org/wiki/Lambert%27s_cosine_law"),
 dict(id="cao_2017_openpose", title="Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields", author="Zhe Cao, Tomas Simon, Shih-En Wei, Yaser Sheikh", year=2017, note="CVPR 2017. arXiv:1611.08050 — 관절점(포즈) 추정, 접점과 관절 가이드의 배경"),
 dict(id="zhang_2023_controlnet", title="Adding Conditional Control to Text-to-Image Diffusion Models", author="Lvmin Zhang, Anyi Rao, Maneesh Agrawala", year=2023, note="ICCV 2023. arXiv:2302.05543 — 포즈·깊이 지도 가이드"),
 dict(id="zhang_2025_iclight", title="Scaling In-the-Wild Training for Diffusion-based Illumination Harmonization and Editing by Imposing Consistent Light Transport", author="Lvmin Zhang, Anyi Rao, Maneesh Agrawala", year=2025, note="ICLR 2025 (IC-Light) — AI 다시 조명"),
 dict(id="ho_2020_ddpm", title="Denoising Diffusion Probabilistic Models", author="Jonathan Ho, Ajay Jain, Pieter Abbeel", year=2020, note="NeurIPS 2020. arXiv:2006.11239 — 큰 구조부터 그려 나가는 확산 모델"),
 dict(id="jakobsen_2001_verlet", title="Advanced Character Physics", author="Thomas Jakobsen", year=2001, note="GDC 2001 — 실험의 점과 막대(베를레) 천 계산"),
]

def kg_block(page, pages):
    nodes = [dict(id="lab:" + i, type=t, label=dict(ko=ko, en=en), page=p, anchor=a, definition=dict(ko=d), source="lab:work/structure_first_drawing_02")
             for i, t, ko, en, p, a, d in KG if p in pages]
    ids = {n["id"] for n in nodes}
    edges = [dict(s="lab:" + s, p=p, o="lab:" + o) for s, p, o in KG_EDGES if "lab:" + s in ids and "lab:" + o in ids]
    raw = dict(version="1.3", page=page, series=SERIES, nodes=nodes, edges=edges)
    ld = {"@context": {"@vocab": "urn:lab:", "skos": "http://www.w3.org/2004/02/skos/core#", "schema": "https://schema.org/"},
          "@graph": [{"@id": "urn:" + n["id"], "@type": n["type"], "skos:prefLabel": [{"@value": n["label"]["ko"], "@language": "ko"}, {"@value": n["label"]["en"], "@language": "en"}],
                      "skos:definition": n["definition"]["ko"], "schema:url": SITE + n["page"] + n["anchor"]} for n in nodes]}
    meta = dict(title=page, series=SERIES, creator=[dict(name="안상선", role="author", affiliation="(주)M-Robo")], date=DATE, version=VER, license="캐릭터·그림 무단 사용 금지")
    J = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    return f"""<section id="kg"><div class="wrap"><h2>지식 색인 — 이 페이지에서 찾아보기</h2>
<p class="muted">이 페이지에 나온 개념·방법·비유·쓰임을 모았습니다. 검색하고, "설명 보러 가기"로 본문에 돌아갑니다.</p><div id="kg-mount"></div></div></section>
<section id="export"><div class="wrap"><h2>온톨로지·서지 꾸러미 — 파일로 내려받기</h2>
<p class="muted">지식 색인을 출처와 함께 파일로 내려받습니다. 서지 관리는 BibTeX·RIS, 온톨로지 편집은 Turtle, 그래프 도구는 CSV, 여러 페이지 합치기는 kg.json입니다.</p><div id="export-mount"></div></div></section>
<script type="application/json" id="kg-raw">{J(raw)}</script>
<script type="application/ld+json" id="kg-ld">{J(ld)}</script>
<script type="application/json" id="refs-csl">{J(REFS)}</script>
<script type="application/json" id="page-meta">{J(meta)}</script>
"""

FOOT_LINKS = [("index.html", "목차")] + [(P["file"], f"{P['no']}부") for P in PARTS] + [("practice/index.html", "5부 실전 연습장")]

def footer(pre=""):
    links = " · ".join(f'<a href="{pre}{h}">{E(t)}</a>' for h, t in FOOT_LINKS) + f' · <a href="{REPO}">저장소</a> · <a href="{BASE}">기초편</a>'
    refs = "".join(f"<tr><td>[{i+1}]</td><td>{E(r['author'])} ({r['year']}). {E(r['title'])}</td><td>{E(r['note'])}</td></tr>" for i, r in enumerate(REFS))
    return f"""<footer><div class="wrap">
<h3>출처·참고</h3>
<div class="tbl"><table><thead><tr><th>#</th><th>자료</th><th>이 시리즈에서 쓴 곳</th></tr></thead><tbody>{refs}</tbody></table></div>
<h3>예시값·설명용 숫자</h3>
<p>팔·무릎 두께, 굽힌 각도, 개더 비율, 치마 둘레, 단차 높이, 광원 각도, 평가단 점수는 모두 원리를 보이기 위한 예시값입니다. 실제 몸과 옷, 그림 도구의 값은 저마다 다릅니다.</p>
<p>연습용 선화·사진은 원서에 실려 있습니다. 이 페이지는 원서의 그림·사진을 옮기지 않으며, 연습할 때는 원서나 직접 찍은 사진을 곁에 두세요. 그림 속 인물은 모두 연구실의 가상 캐릭터입니다.</p>
<p>캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다. 캐릭터 그림: <a href="{CHARREPO}">fruitfly-lab-expressions</a>.</p>
<p>글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p>
<p>{links}</p>
</div></footer>
<script src="{pre}assets/panels.js"></script>
</body></html>
"""

def seen_box(no, x):
    if (no, x["id"]) not in SEEN or not has_img(x["b_key"]):
        return ""
    v, lines = SEEN[(no, x["id"])]
    col = {"예상대로": "var(--green)", "일부": "var(--orange)"}.get(v, "var(--red)")
    return f'<div class="box"><b>4 · 실제 결과 — <span style="color:{col}">{E(v)}</span></b><ul style="margin:6px 0 0;padding-left:20px">' + "".join(f"<li>{E(t)}</li>" for t in lines) + "</ul></div>"

def retry_box(no, x, ar):
    r = RETRY.get((no, x["id"]))
    if not r:
        return ""
    pid = f"rt{no}{x['id']}"; got = has_img(r["key"])
    return f"""<div class="panel" style="border-color:var(--orange)"><div class="ph"><b>6 · 다시 시도 — 1차 결과는 위에 그대로 두었습니다</b><small>방법: {E(r['how'])}</small></div>
<p><b>왜 다시 하나</b> — {E(r['why'])}</p>
<p class="hint">새 대화를 열고 <a href="assets/img/{r['attach']}.webp" download>이 그림</a>을 첨부한 뒤 아래 문장을 보냅니다. 부분 수정 기능이 있으면 바꿀 곳만 칠하고 보냅니다.</p>
<div class="promptbox"><pre id="{pid}">{E(r['prompt'])}</pre><button type="button" class="btn mk-copy" data-for="{pid}">복사하기</button></div>
<div class="promptbox"><b>그래도 약하면 같은 대화에서 한 줄 더</b><pre id="{pid}m">{E(r['more'])}</pre><button type="button" class="btn mk-copy" data-for="{pid}m">복사하기</button></div>
<div class="pair"><div>{art(x['b_key'], "1차 결과 — " + x['title'], ar, "1차 결과(실패, 그대로 둠)")}</div><div>{art(r['key'], "2차 결과 — " + x['title'], ar, "2차 결과" + ("(실제로 만든 그림, 새 대화에서 한 번)" if got else " — 그림을 받으면 실제 결과로 바뀝니다"))}</div></div>{retry_seen(no, x, got)}{retry3_box(no, x, ar)}</div>"""

def retry3_box(no, x, ar):
    r = RETRY3.get((no, x["id"]))
    if not r:
        return ""
    pid = f"rt3{no}{x['id']}"; got = has_img(r["key"]); r2 = RETRY[(no, x["id"])]["key"]
    return f"""<div class="panel" style="border-color:var(--orange);margin-top:14px"><div class="ph"><b>7 · 한 번 더(3차) — 1·2차 결과는 그대로 둡니다</b><small>방법: {E(r['how'])}</small></div>
<p><b>왜 한 번 더 하나</b> — {E(r['why'])}</p>
<p class="hint">새 대화를 열고 <a href="assets/img/{r['attach']}.webp" download>이 그림(A, 얼룩 없음)</a>을 첨부합니다. 편집 화면에서 부분 수정(브러시)으로 허리끈과 그 위아래 손바닥 폭만 칠한 뒤 아래 문장을 보냅니다.</p>
<div class="promptbox"><b>부분 수정용 문장</b><pre id="{pid}">{E(r['prompt'])}</pre><button type="button" class="btn mk-copy" data-for="{pid}">복사하기</button></div>
<details class="promptbox"><summary>부분 수정 기능이 없을 때 — 그림 전체 편집용 문장</summary><pre id="{pid}w">{E(r['whole'])}</pre><button type="button" class="btn mk-copy" data-for="{pid}w">복사하기</button></details>
<div class="promptbox"><b>그래도 약하면 같은 대화에서 한 줄 더</b><pre id="{pid}m">{E(r['more'])}</pre><button type="button" class="btn mk-copy" data-for="{pid}m">복사하기</button></div>
<div class="pair"><div>{art(r2, "2차 결과 — " + x['title'], ar, "2차 결과(일부, 그대로 둠)")}</div><div>{art(r['key'], "3차 결과 — " + x['title'], ar, "3차 결과" + ("(실제로 만든 그림, 부분 수정)" if got else " — 그림을 받으면 실제 결과로 바뀝니다"))}</div></div>{seen3(no, x, got)}</div>"""

def seen3(no, x, got):
    if not got or (no, x["id"]) not in RETRY3_SEEN:
        return ""
    v, lines = RETRY3_SEEN[(no, x["id"])]
    return f'<div class="box"><b>3차 결과 — <span style="color:var(--orange)">{E(v)}</span></b> <small class="muted">(1차: {E(SEEN[(no, x["id"])][0])} · 2차: {E(RETRY_SEEN[(no, x["id"])][0])})</small><ul style="margin:6px 0 0;padding-left:20px">' + "".join(f"<li>{E(t)}</li>" for t in lines) + "</ul></div>"

def retry_seen(no, x, got):
    if not got or (no, x["id"]) not in RETRY_SEEN:
        return ""
    v, lines = RETRY_SEEN[(no, x["id"])]
    col = "var(--green)" if "예상대로" in v else "var(--orange)"
    return f'<div class="box"><b>2차 결과 — <span style="color:{col}">{E(v)}</span></b> <small class="muted">(1차: {E(SEEN[(no, x["id"])][0])})</small><ul style="margin:6px 0 0;padding-left:20px">' + "".join(f"<li>{E(t)}</li>" for t in lines) + "</ul></div>"

def mk_block(no, k, x):
    who = PCHAR[x["model"]][0]; ak = a_key(x["a"]); ap = a_prompt(x["a"])
    ar = "4/3" if no == 3 and x["id"] == "x1" else ("4/3" if ak.startswith("pr3") else "2/3")
    links = " · ".join(f'<a href="#{sid}">{E(t)}</a>' for sid, t in x["steps"])
    ex = "".join(f"<li>{E(t)}</li>" for t in x["expect"])
    ck = "".join(f'<li><label><input type="checkbox" class="pl-ok"> {E(t)}</label> <a href="{h}" class="muted">({E(dict(x["steps"]).get(h[1:], "원리 보기"))})</a></li>' for t, h in x["checks"])
    pid = f"mk{no}{x['id']}"
    got = has_img(x["b_key"])
    return f"""<div class="panel mk" id="{pid}"><div class="ph"><b>실습 {no}-{k} · {E(x['title'])}</b><small>연결: {links}</small></div>
<p><b>목표</b> — {E(x['goal'])}</p>
<div class="box"><b>준비</b> — ① 이미지 AI(이 시리즈는 Genspark)에서 <b>새 대화</b>를 엽니다. ② 같은 인물로 나오게 <a href="assets/refs/{x['ref']}_anime_base.png" download>{E(who)} 기준 전신 그림</a>을 내려받아 첨부합니다. ③ A를 건너뛰고 B만 해 보려면 <a href="assets/img/{ak}.webp" download>A 결과 그림</a>을 내려받아 첨부하고 B 문장만 보냅니다.</div>
<h4>1 · A 프롬프트 — 이 페이지 그림을 실제로 만든 요청문 그대로</h4>
<div class="promptbox"><pre id="{pid}a">{E(ap)}</pre><button type="button" class="btn mk-copy" data-for="{pid}a">복사하기</button></div>
<h4>2 · B 문장 — 같은 대화에 이어서, 원리 하나만 바꾸기</h4>
<div class="promptbox"><pre id="{pid}b">{E(x['b'])}</pre><button type="button" class="btn mk-copy" data-for="{pid}b">복사하기</button></div>
<h4>3 · 예상 결과 — 이렇게 바뀌면 성공</h4><ol>{ex}</ol>
<div class="pair"><div>{art(ak, "A 결과 — " + x['title'], ar, "A 결과(실제로 만든 그림)")}</div><div>{art(x['b_key'], "B 결과 — " + x['title'], ar, "B 결과" + ("(실제로 만든 그림, 같은 대화에서 B 문장 한 번)" if got else " — 그림을 받으면 실제 결과로 바뀝니다"))}</div></div>
{seen_box(no, x)}<h4>5 · 결과에서 확인할 것</h4><ul class="pl-list" style="list-style:none;padding-left:0;margin:0">{ck}</ul><p class="hint"><span class="pl-score">0 / 3</span></p>
<div class="box"><b>주의할 점</b> — {E(x['caution'])} 한 번의 요청에 여러 변화를 넣지 않습니다. 차이가 약하면 새 대화에서 A부터 다시 만들어 봅니다.</div>{retry_box(no, x, ar)}</div>
"""

def prompt_section(P):
    L = PL[P["no"]]; no = P["no"]
    who = PCHAR[L["model"]][0]
    sel = ""
    if L.get("models"):
        sel += '<label>모델 <select class="pl-sel">' + "".join(f'<option data-frag="{E(PCHAR[m][1])}"{" selected" if m == L["model"] else ""}>{E(PCHAR[m][0])}</option>' for m in L["models"]) + '</select></label>'
        sel += '<label>광원 <select class="pl-sel">' + "".join(f'<option data-frag="{E(en)}"{" selected" if i == 2 else ""}>{E(ko)} ({E(st)})</option>' for i, (ko, st, en) in enumerate(L["lights"])) + '</select></label>'
        head = f"{L['pose']}\n{PSTYLE}"
    else:
        head = f"{L['pose']}\n{PSTYLE}\n{PCHAR[L['model']][1]}"
    chks = "".join(f'<label><input type="checkbox" class="pl-chk" data-frag="{E(en)}"{"" if "다시 조명" in ko else " checked"}> {E(ko)} <small class="muted">({E(st)})</small></label>' for ko, st, en in L["frags"])
    checks = "".join(f'<li><label><input type="checkbox" class="pl-ok"> {E(c)}</label></li>' for c in L["checks"])
    a, b = L["pair"]; note, ar = PAIR_NOTE[no]; arc = {"2:3": "2/3", "4:3": "4/3"}[ar]
    ex = L["example"]; ex_prompt = "\n".join(["Character illustration.", DBODY, "Character: " + DBODYS[ex][0], DBODYS[ex][1], DARW, DNEG])
    ex_alt = [st["img"][1] for PP in PARTS for st in PP["steps"] if st["img"][0] == ex][0]
    return f"""<section id="prompt"><div class="wrap"><span class="roomno">{no}부 · 프롬프트 실습</span><h2>프롬프트로 직접 만들어 보기 — {E(who)}</h2>
{talk([("doctor", "e07", "배운 다섯 단계를 이제 말로 적어 이미지 AI에게 맡겨 보자. 원리를 적은 요청문과 안 적은 요청문은 결과가 다르다."), ("jupanbot", "e16", "'걸작, 아주 자세하게'만 쓰면 다 됩니다!"), ("fruitfly", "e09", "접점과 광원을 적지 않으면 AI도 아무 데나 주름을 넣지 않을까?")])}
<div class="box"><b>순서</b> — ① 아래에서 넣을 원리를 고릅니다. ② 완성된 요청문을 복사해 이미지 AI(이 시리즈는 Genspark)에 붙여 넣고, 같은 인물로 나오게 기초편의 {E(who)} 기준 전신 그림을 함께 올립니다. ③ 나온 그림을 점검표로 확인합니다. ④ 틀린 곳은 고치기 문장으로 <b>한 번에 하나씩</b> 고칩니다.</div>
<h3>실습 두 가지 — A로 만들고, B로 원리 하나만 바꾸기</h3>
<p class="muted">각 실습은 이 페이지 그림을 실제로 만든 요청문(A)에서 출발해, 원리 하나만 바꾼 문장(B)을 같은 대화에 이어 붙입니다. A와 B를 나란히 놓고 무엇이 달라졌는지 확인하는 것이 목표입니다.</p>
{"".join(mk_block(no, i + 1, x) for i, x in enumerate(EX[no]))}<div class="box"><b>여덟 실습을 모아 보면</b> — {E(MK_LESSON)}<p style="margin:8px 0 0">{E(RETRY_LESSON)}</p></div>
<h3>내 요청문 조립하기 — 원리를 골라 새로 만들기</h3>
<div class="panel plab" data-head="{E(head)}" data-tail="{E(PNEG)}"><div class="ph"><b>요청문 조립</b><small>체크한 원리만 들어갑니다</small></div>
<div class="ctrl">{sel}{chks}</div>
<div class="promptbox"><b>완성된 요청문 (영어 — 이 시리즈 그림은 영어 요청문으로 만들었습니다)</b><pre class="pl-out" aria-live="polite"></pre><button type="button" class="btn pl-copy">복사하기</button> <span class="hint pl-n"></span></div>
<details class="promptbox"><summary>비교용 — 주판봇식 요청문(원리 없음)</summary><pre>{E(L['naive'])}</pre></details></div>
<h3>같은 인물, 다른 요청문 — 실제로 나온 결과</h3><p class="muted">왼쪽은 주판봇식 요청문, 오른쪽은 위에서 조립한 요청문으로 Genspark에서 받은 첫 결과입니다. 고르지 않고 그대로 실었습니다.</p>
<div class="pair"><div>{art(a, "원리 없는 요청문으로 받은 " + who + "의 첫 결과", arc, "주판봇식 요청문 — 첫 결과")}</div><div>{art(b, "원리를 넣은 요청문으로 받은 " + who + "의 첫 결과", arc, "초파리식 요청문(위에서 조립) — 첫 결과")}</div></div>
<div class="box"><b>AI 판단 — 점검표로 본 이 결과</b><ul style="margin:6px 0 0;padding-left:20px">{"".join(f"<li>{E(x)}</li>" for x in PAIR_SEEN[no])}</ul>
<p style="margin:8px 0 0"><b>배울 점</b></p><ol style="margin:4px 0 0;padding-left:20px">{"".join(f"<li>{E(x)}</li>" for x in PAIR_LESSON)}</ol></div>
<div class="panel"><div class="ph"><b>결과 점검표 — AI 그림을 그대로 믿어도 될까?</b><small class="pl-score">0 / {len(L['checks'])}</small></div><ul class="pl-list" style="list-style:none;padding-left:0;margin:0">{checks}</ul>
<p class="hint">하나라도 '아니오'면 아래 고치기 문장을 쓰세요. 여러 곳을 한꺼번에 고치라고 하면 맞던 곳까지 바뀌기 쉽습니다.</p>
<div class="promptbox"><b>고치기 문장(같은 대화에서)</b><pre>{E(L['fix'])}</pre></div></div>
<details class="promptbox"><summary>이 페이지 그림을 실제로 만든 요청문 보기 — {E(ex)}</summary>{art(ex, ex_alt, "4/3" if ex.startswith("p3") else "2/3")}<pre>{E(ex_prompt)}</pre><p class="hint">빨간 화살표·동그라미 지시(Annotation 줄)는 설명용 표시를 넣으려고 붙인 것입니다. 일반 그림에는 빼세요.</p></details>
</div></section>
"""

def build_part(P):
    t = f"{SERIES} {P['no']}부 — {P['title']}"
    s = head(t, P["desc"], P["og"], P["file"])
    navl = [(f"#{x['id']}", f"{k+1}단계") for k, x in enumerate(P["steps"])]
    navl += [("#prompt", "프롬프트"), ("#judge", "평가"), ("#sum", "정리"), (P["next"][0], "다음 →")]
    s += nav(navl)
    s += cover(P["cover_key"], P["cover_cap"], P["cover_cast"])
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">{E(P['kicker'])}</span><h1>{E(P['title'])}</h1><p class="lead">{E(P['lead'])}</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section><div class="wrap">{three(*P['three'], ABBR)}</div></section>
<section><div class="wrap"><h2>오늘의 과제</h2>{talk(P['intro'])}<div class="box" style="margin-top:14px"><b>30초 복습</b> — {E(P['review'])} <a href="{BASE}">기초편 보기</a></div>{flow_strip(P['no'])}</div></section>
"""
    for k, st in enumerate(P["steps"]):
        s += step(P, k + 1, st)
    s += prompt_section(P)
    s += judge(P["judge"]) + summary(P) + outro(P)
    s += kg_block(P["file"].replace(".html", ""), [P["file"]])
    s += footer()
    open(os.path.join(ROOT, P["file"]), "w").write(s)

FLOW = [
 (1, "서 있는 자세", "주름 없는 선화에 무엇부터 넣어야 할지 모른다", "접점 → 관절 → 꼭대기 → 큰 그림자 → 단차"),
 (2, "주름 많은 옷", "접점·힘만으로는 프릴처럼 일부러 만든 주름을 설명 못 한다", "개더 비율·조임·큰 선·짝 장식·섞인 그림자"),
 (3, "앉은 자세", "서 있을 때 규칙만으로는 관절과 겹침이 많은 자세가 무너진다", "관절 각도·단추·소재·주름치마·겹침 순서"),
 (4, "광원 방향", "1~3부는 광원을 위쪽에 고정했다. 다른 조명에서는 그림자 자리가 막힌다", "방향·아래 빛·옆 빛·각도·다시 조명"),
 (5, "실전 연습장", "배운 것을 한 화면에서 함께 다뤄 본다", "접점 탐정·프릴 공방·조명실·숙제 책상"),
]
def flow_strip(cur=None, pre=""):
    files = {P["no"]: P["file"] for P in PARTS}
    files[5] = "practice/index.html"
    cells = []
    for n, t, _, _ in FLOW:
        mark = ' style="border-color:var(--orange);background:var(--orange-soft)"' if n == cur else ""
        cells.append(f'<a href="{pre}{files[n]}"{mark}><b>{n}부</b>{E(t)}</a>')
    return '<div class="flowgrid" style="grid-template-columns:repeat(auto-fit,minmax(130px,1fr));margin-top:16px">' + "".join(cells) + "</div>"

def build_index():
    t = f"{SERIES} — 주름과 그림자를 직접 넣어 보기"
    d = "주름 없는 선화에 접점 → 주름 → 그림자 순서로 직접 넣어 보는 실천편입니다. 서 있는 자세, 주름 많은 옷, 앉은 자세, 광원 방향별 그림자를 실험으로 익힙니다."
    s = head(t, d, "og_index.jpg", "index.html")
    s += nav([("#howto", "읽는 법"), ("#parts", "편 목록"), ("#map", "흐름"), ("#cast", "등장인물"), ("#source", "원리와 출처")])
    s += cover("cover_index", "연구실 아틀리에 · 주름 없는 선화 앞의 세 모델과 두 화가", [("fruitfly", "e09"), ("haru", "e01"), ("sia", "e13"), ("moa", "e19"), ("jupanbot", "e16")])
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">연구실 특별편 02 · 실천편</span>
<h1>구조 먼저 그리기 연구실 02<br>실천편 — 주름과 그림자를 직접 넣어 보기</h1>
<p class="lead">기초편에서 구조·빛·주름의 원리를 배웠다면, 이번에는 <b>주름 없는 선화</b>에 직접 넣어 봅니다. 순서는 늘 같습니다. <b>접점</b>을 찾고, <b>주름</b>을 넣고, <b>광원</b>을 정해 <b>그림자</b>를 칠합니다. 자세와 옷, 조명이 바뀌어도 이 순서는 그대로입니다.</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section><div class="wrap">{three("주름 없는 선화에 접점 → 주름 → 그림자 순서로 주름과 그림자를 넣는 연습을, 서 있는 자세·주름 많은 옷·앉은 자세·광원 방향별로 합니다.", "원리를 알아도 실제 그림에 넣는 순서를 모르면 손이 멈춥니다. 순서가 있으면 처음 보는 옷과 자세도 같은 방법으로 풀립니다.", "캐릭터 설정화·홍보 그림을 다듬거나, AI가 그린 옷 주름과 그림자를 검수하고 다시 요청할 때 씁니다.", ABBR)}</div></section>
<section id="howto"><div class="wrap"><h2>읽는 순서와 시간</h2><div class="box"><ul style="margin:0;padding-left:20px">
<li><b>처음부터 차례로</b>(권장): 부마다 실험을 눌러 보며 20~30분, 전체 2~3시간입니다.</li>
<li><b>기초편을 아직 안 봤다면</b>: 낱말이 낯설 때마다 <a href="{BASE}">기초편</a>의 2부(빛과 그림자)·3부(옷 주름)를 곁에 열어 두세요.</li>
<li><b>손으로 연습하려면</b>: 각 단계의 순서를 따라 원서의 연습 선화나 직접 찍은 사진 위에 그려 보세요. 마지막 5부 '숙제 책상'이 순서 점검표입니다.</li>
<li>각 부의 <b>프롬프트로 직접 만들어 보기</b>에는 실습이 두 개씩 있습니다. 이 페이지 그림을 실제로 만든 요청문(A)으로 그림을 만들고, 원리 하나만 바꾼 문장(B)을 이어 붙여 무엇이 달라지는지 확인합니다. 원리를 골라 내 요청문을 조립하는 상자도 있습니다.</li>
<li>각 부 끝의 <b>평가단 채점</b>은 이야기 속 예시 점수입니다. 확인 퀴즈와 실전 연습장 미션으로 스스로 점검하세요.</li></ul></div></div></section>
<section id="parts"><div class="wrap"><h2>편 목록</h2>
<p class="muted">모델은 하루·시아·모아, 화가는 주판봇과 초파리, 평가단은 X1·X2·X3, 해설은 박사입니다. 부마다 두 화가가 겨루고 평가단이 점수를 매깁니다.</p>
<div class="cards">
<a class="card" href="01_standing.html">{face("haru","e01")}<span class="n">1부 · 모델 하루</span><h3>서 있는 자세</h3><p>접점, 굽힌 관절, 꼭대기 방향, 큰 형체 그림자, 단차 그림자.</p></a>
<a class="card" href="02_frills.html">{face("sia","e13")}<span class="n">2부 · 모델 시아</span><h3>주름 많은 옷</h3><p>프릴(개더 비율), 조임, 큰 선 먼저, 짝 장식, 섞인 그림자.</p></a>
<a class="card" href="03_sitting.html">{face("moa","e19")}<span class="n">3부 · 모델 모아</span><h3>앉은 자세</h3><p>관절 각도, 단추 고정 주름, 빳빳한 천, 퍼진 주름치마, 겹침 순서.</p></a>
<a class="card" href="04_light_dir.html">{face("haru","e19")}<span class="n">4부 · 모델 셋 모두</span><h3>광원 방향</h3><p>위·아래·옆·뒤 조명, 위에서 본 각도, 노멀 지도로 다시 조명.</p></a>
<a class="card" href="practice/index.html">{face("x2","e16")}<span class="n">5부 · 마지막 장</span><h3>실전 연습장</h3><p>접점 탐정·프릴 공방·조명실·숙제 책상을 직접 운영합니다.</p></a>
</div></div></section>
<section id="map"><div class="wrap"><h2>전체 흐름 — 1부부터 5부까지 이어지는 순서</h2>{flow_strip()}
<div class="tbl" style="margin-top:16px"><table><thead><tr><th>부</th><th>제목</th><th>이 부를 배우는 까닭</th><th>배우는 것</th></tr></thead><tbody>
{''.join(f"<tr><td>{n}</td><td>{E(t)}</td><td>{E(a)}</td><td>{E(b)}</td></tr>" for n, t, a, b in FLOW)}</tbody></table></div>
<div class="box" style="margin-top:16px"><b>어느 부에서나 같은 그리기 순서</b> — ① 광원 확인 → ② 접점 찍기 → ③ 큰 주름(관절·꼭대기·만든 주름) → ④ 큰 형체 그림자 → ⑤ 주름·단차 그림자 → ⑥ 떨어지는 그림자의 주인 확인. 4부에서 광원이 바뀌어도 ②~⑥은 그대로입니다.</div>
<p class="muted" style="margin-top:12px">원리를 먼저 보고 싶다면: <a href="{BASE}">기초편 — 구조 먼저 보는 캐릭터 그리기 연구실(1~7부)</a></p></div></section>
<section id="cast"><div class="wrap"><h2>등장인물</h2><div class="cast-grid">{''.join(f'<div class="who">{face(k, "e01" if k in ("haru","sia","moa") else "e13")}<b>{E(CH[k][0])}</b><span>{E(CH[k][1])}</span></div>' for k in ["doctor","haru","sia","moa","jupanbot","fruitfly","x1","x2","x3"])}</div></div></section>
<section id="source"><div class="wrap"><h2>원리와 출처</h2>
<p>연습의 구성(서 있는 자세 → 주름 많은 옷 → 앉은 자세 → 광원 방향별 그림자, 그리고 같은 왼쪽 광원도 각도에 따라 그림자가 다르다는 칼럼)은 다테 나오토의 작법서 『デジタルツールで描く！服のシワと影の描き方』(マイナビ) 3장 실천편과 출판사 특전 PDF를 참고했습니다. 숫자 식(두께 × 각, 개더 비율, tan, (1 + cos φ) ÷ 2, 내적)은 원리를 보이려고 이 페이지에서 덧붙인 것입니다.</p>
<p>AI와의 연결(포즈·깊이 가이드, 확산 모델, 다시 조명)은 아래 출처의 논문을 바탕으로 쉽게 풀었습니다. 그림은 연구실 캐릭터로 Genspark에서 새로 만들었습니다(표지 6장은 16비트 픽셀아트, 본문 20장은 애니풍). 그림 속 빨간 화살표·동그라미는 그 단계에서 볼 곳을 가리킵니다.</p></div></section>
"""
    s += kg_block("index", [P["file"] for P in PARTS] + ["practice/index.html"])
    s += footer()
    open(os.path.join(ROOT, "index.html"), "w").write(s)

def build_practice():
    pre = "../"
    t = f"{SERIES} 5부 — 실전 연습장"
    d = "접점 탐정(자세별 접점), 프릴 공방(개더 비율), 조명실(광원 각도와 밝은 폭), 숙제 책상(순서 점검과 요청문) 네 곳을 직접 운영하며 1~4부를 함께 연습합니다."
    s = head(t, d, "og_05.jpg", "practice/index.html", pre)
    s += nav([("#contact", "접점 탐정"), ("#frill", "프릴 공방"), ("#light", "조명실"), ("#homework", "숙제 책상"), ("#wrap", "마무리")], pre)
    s += cover("cover_05", "연구실 조종 책상 · 실전 연습장", [("haru", "e19"), ("doctor", "e16"), ("fruitfly", "e09"), ("jupanbot", "e16")], pre)
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">5부 · 마지막 장</span><h1>실전 연습장</h1>
<p class="lead">네 곳의 작업장을 직접 운영합니다. <span style="color:var(--green)">초록 조작판</span>은 주어진 환경, <span style="color:var(--blue)">파랑 조작판</span>은 내 결정입니다. 미션은 직접 조작해야 판정됩니다.</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section id="practice"><div class="wrap">
<div class="tabs" role="tablist"><button type="button" data-t="contact">접점 탐정</button><button type="button" data-t="frill">프릴 공방</button><button type="button" data-t="light">조명실</button><button type="button" data-t="homework">숙제 책상</button></div>
"""
    def sc(id_, title, situ, env, me, missions, back, extra_g1=""):
        ms = "".join(f"<li>{E(m)}</li>" for m in missions)
        bk = " · ".join(f'<a href="{pre}{h}">{E(t)}</a>' for h, t in back)
        return f"""<div class="scene" id="{id_}"><h2>{E(title)}</h2><div class="box"><b>상황</b> — {E(situ)}</div>
<div class="panel"><div class="ph"><b>조작판</b><small>초록 = 환경 · 파랑 = 내 결정</small></div>
<div class="ctrl ctl-env">{env}</div><div class="ctrl ctl-me">{me}</div>
<div class="board" aria-live="polite"></div>
<div class="pair"><div class="g1">{extra_g1}</div><div class="g2"></div></div>
<div class="talk"></div>
<h4>미션</h4><ol class="missions">{ms}</ol></div>
<p class="muted">배운 곳 다시 보기: {bk}</p></div>
"""
    SPOTS = ["어깨 꼭대기", "가슴 위", "허리에 얹은 손", "굽힌 팔꿈치", "앞으로 나온 무릎", "겨드랑이", "엉덩이", "잠근 단추", "무릎 뒤", "등 한가운데"]
    spots = "".join(f'<label><input type="checkbox" name="sp{i}"> {E(x)}</label>' for i, x in enumerate(SPOTS))
    s += sc("contact", "접점 탐정 — 자세마다 접점 찾기", "모델의 자세가 바뀌면 접점도 바뀝니다. 자세를 보고 천이 걸리거나 붙잡힌 곳을 모두 고르세요. 틀린 곳을 고르면 감점입니다.",
            '<label>모델 자세 <select name="pose"><option value="hip">서서 한 손 허리(하루)</option><option value="up">두 팔 위로(하루)</option><option value="sit">바닥에 앉기(모아, 블레이저)</option><option value="walk">걷기(시아)</option></select></label>',
            spots,
            ["'서서 한 손 허리'에서 틀린 고름 없이 접점 모두 찾기", "'바닥에 앉기'에서 틀린 고름 없이 접점 모두 찾기", "서로 다른 세 자세를 '등 한가운데'를 한 번도 고르지 않고 통과하기"],
            [("01_standing.html#s1", "1부 1단계 접점"), ("03_sitting.html#s1", "3부 1단계 관절")])
    s += sc("frill", "프릴 공방 — 물결 설계하기", "앞치마 밑단에 프릴을 답니다. 꿰맬 띠 길이와 천 두께는 주문으로 정해져 있고, 천 길이와 물결 폭은 내가 정합니다.",
            '<label>꿰맬 띠 길이(cm) <input type="range" name="band" min="40" max="100" step="5" value="60"></label><label>천 두께 <select name="thick"><option value="thin">얇은 천</option><option value="thick">두꺼운 천</option></select></label>',
            '<label>천 길이(cm) <input type="range" name="cloth" min="40" max="300" step="5" value="90"></label><label>물결 폭(cm) <input type="range" name="wave" min="2" max="10" step="1" value="5"></label>',
            ["개더 비율을 정확히 2.0으로 만들기", "물결 개수를 정확히 15개로 만들기", "비율은 그대로 두고 물결 폭만 두 배로 바꿔, 깊이도 두 배가 되는 것 확인하기"],
            [("02_frills.html#s1", "2부 1단계 프릴"), ("02_frills.html#s3", "2부 3단계 큰 선 먼저")])
    s += sc("light", "조명실 — 장면에 맞는 광원 놓기", "장면 주문에 맞게 광원을 놓습니다. 모델은 원기둥처럼 단순하게 봅니다. 위에서 본 광원 각도 φ와 광원 높이를 정하세요.",
            '<label>장면 주문 <select name="order"><option value="portrait">사진관 인물(밝은 폭 70~80%)</option><option value="stage">무대 바닥 조명(아래 빛)</option><option value="rim">역광 실루엣(밝은 폭 10% 이하)</option></select></label>',
            '<label>광원 각도 φ(°) <input type="range" name="phi" min="0" max="180" step="5" value="90"></label><label>광원 높이(°) <input type="range" name="elev" min="-60" max="80" step="5" value="30"></label><label>빛의 좌우 <select name="side"><option value="-1">왼쪽</option><option value="1">오른쪽</option></select></label>',
            ["밝은 폭을 75% ± 3%로 만들기", "광원 높이를 0 아래로 내려 아랫면이 윗면보다 밝게 하기", "밝은 폭 10% 이하의 역광 만들기"],
            [("04_light_dir.html#s2", "4부 2단계 아래 빛"), ("04_light_dir.html#s4", "4부 4단계 각도")])
    STEPS = ["광원 확인", "접점 찍기", "큰 주름(관절·꼭대기·만든 주름)", "큰 형체 그림자", "주름·단차 그림자", "떨어지는 그림자의 주인 확인"]
    btns = "".join(f'<button type="button" class="btn hw" data-k="{i}">{E(x)}</button>' for i, x in sorted(enumerate(STEPS), key=lambda p: [3, 0, 5, 2, 4, 1][p[0]]))
    s += sc("homework", "숙제 책상 — 순서대로 그리고 요청문 만들기", "연습 선화 한 장을 고르고, 그리는 순서를 단추로 차례대로 누르세요. 순서를 다 맞히면 같은 그림을 AI에게 요청하는 문장이 완성됩니다.",
            '<label>연습 그림 <select name="pic"><option value="haru_hoodie">하루 · 후드 집업, 한 손 허리</option><option value="sia_maid">시아 · 메이드복, 치마 끝 잡기</option><option value="moa_sit">모아 · 블레이저, 바닥에 앉기</option><option value="trio_walk">하루 · 반소매 셔츠, 걷기</option></select></label><label>광원 <select name="lt"><option value="top">위</option><option value="left">왼쪽 앞</option><option value="right">오른쪽</option><option value="below">아래</option></select></label>',
            f'<div style="width:100%"><p class="hint">아래 단추를 그리는 순서대로 누르세요(섞여 있습니다).</p><div class="opts">{btns}</div><button type="button" class="btn" data-reset="1" style="margin-top:8px">처음부터</button></div>',
            ["여섯 단계를 한 번도 틀리지 않고 순서대로 완성하기", "서로 다른 연습 그림 두 장으로 순서 완성하기", "'아래' 광원으로 완성해 요청문에 '턱 아래가 밝다'가 들어가게 하기"],
            [("01_standing.html#s4", "1부 4단계 큰 형체 먼저"), ("index.html#map", "어느 부에서나 같은 순서")],
            '<div class="promptbox"><b>완성된 요청문</b><pre aria-live="polite">순서를 끝까지 맞히면 요청문이 나타납니다.</pre><button type="button" class="btn copy">복사하기</button></div>')
    s += f"""</div></section>
<section id="wrap"><div class="wrap"><h2>마무리 — 네 작업장의 공통 질문</h2>
<div class="box"><p>접점 탐정에서 찾은 점은 주름의 출발점이고, 프릴 공방의 비율은 만든 주름의 깊이이며, 조명실의 각도는 그림자의 넓이입니다. 숙제 책상은 이 셋을 한 장의 그림에 차례로 넣는 순서입니다. 네 곳을 하나로 잇는 질문은 이것입니다: <b>"광원과 접점을 먼저 정했는가, 그리고 큰 것부터 작은 것 순서로 넣었는가?"</b></p>
<p class="hint">한계: 이 연습장의 천·조명 계산은 원리를 보이기 위해 크게 단순화했습니다. 숫자는 교육용 예시이며, 실제 옷·그림 도구·렌더러의 값과 다릅니다.</p></div>
<div class="next"><a href="{pre}04_light_dir.html">← 4부 광원 방향</a><a href="{pre}index.html">목차로</a></div></div></section>
"""
    s += kg_block("practice_index", ["practice/index.html"])
    s += footer(pre)
    open(os.path.join(ROOT, "practice", "index.html"), "w").write(s)

if __name__ == "__main__":
    build_index()
    for P in PARTS:
        build_part(P)
    build_practice()
    print("built", len(PARTS) + 2, "pages")


# ── 분야 뼈대 다시 걸기 (kg/rehang.json, ai-lab-retrofit 15장) ──
# 빌드가 페이지를 다시 쓴 뒤, 덧씌우기를 kg-raw·kg-ld에 다시 적용한다. 파일이 없으면 아무것도 하지 않는다.
if __name__ == "__main__":
    import os as _os, sys as _sys, subprocess as _sp
    _r = _os.path.dirname(_os.path.abspath(__file__))
    for _i in range(3):
        if _os.path.exists(_os.path.join(_r, "kg", "rehang.json")): break
        _r = _os.path.dirname(_r)
    if _os.path.exists(_os.path.join(_r, "kg", "rehang.json")):
        _sp.run([_sys.executable, _os.path.join(_r, "kg", "rehang.py"), "apply", _r])
