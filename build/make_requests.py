# -*- coding: utf-8 -*-
"""Genspark 그림 요청 꾸러미(docs/image_requests) 만들기. 페이지의 그림 자리(art/cover 키)와 일치시킨다."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
from content_a import P1, P2
from content_b import P3, P4
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "docs", "image_requests")
PIX = ("Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2–3 tone shading, small highlights; "
       "no smooth gradients, no painterly, vector, watercolor or 3D look.\nMatch the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.\n"
       "Bright daytime laboratory mood, clean white walls and white floor, soft natural sunlight, light lavender, mint and pink accents.")
CAST = {
 "fly": "the Fruit Fly researcher (tiny cartoon fruit fly, large red compound eyes, retro dark blue helmet with a yellow-white stripe, colorful dangling cables, tiny white lab coat, translucent wings)",
 "bot": "AbaBot (boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, small tank treads)",
 "doc": "the Professor (chibi male scientist, dark charcoal spiky hair with a white streak at the front, very thick black eyebrows, teal rectangular glasses, white lab coat over a black vest and black tie)",
 "haru": "Haru (lab assistant girl, long straight pink hair with navy streaks and a thick navy streak down the center of the bangs, two round hair buns on top, blue eyes, lavender zip-up hoodie, gray-blue jogger pants, lavender slip-on sneakers; lab coat off today)",
 "sia": "Sia (maid intern, long straight jet-black hair, no headdress, gray eyes, silver drop earrings, knee-length charcoal-black maid dress with puffed short sleeves, large gray bow at the collar, white frilled apron, layered white petticoat ruffles, white over-knee socks)",
 "moa": "Moa (maid intern, long ash-beige wavy hair, white frilled maid headband with a white ribbon over the LEFT ear, amber eyes, camel blazer, red and navy plaid bow tie, dark navy pleated skirt, navy knee socks, brown loafers)",
 "judges": "three small cute dark navy silhouette judges with white dot eyes (one with a pink side-ponytail bow, one with a beret and teal-glinting round glasses, one with a cat-ear hood and yellow pompoms) holding blank score paddles",
}
SAFE = "Composition: every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); bottom-left corner plain and bright."
NOPIX = "No text, no letters, no numbers, no logos, no weapons, no real brands."
BODY = ("High-quality anime illustration, clean confident lineart, two-tone cel shading with soft lavender-gray shadows, plain white background, "
        "natural proportions of young adults in their early twenties, modest outfit exactly as described.")
NEG = "No text, no letters, no numbers, no logos, no watermark, no revealing clothing, no exaggerated body proportions, not resembling any famous anime character, no pixel art."
ARW = "Annotation marks drawn on top: only simple red hand-drawn arrows, red circles and red dashed lines — absolutely no words or numbers."
HARU = ("Haru (match the attached reference p5_haru_anime exactly for face and hair): long straight pink hair reaching the waist with navy blue streaks including a thick navy streak down the center of the bangs, "
        "two round slightly messy hair buns on top of the head, a small ahoge, big bright blue eyes. For this lesson her lab coat is off: lavender zip-up hoodie with white drawstrings over a white t-shirt, "
        "gray-blue jogger pants with ribbed ankle cuffs, lavender slip-on sneakers.")
SIA = ("Sia (match the attached reference p5_sia_anime exactly for face and hair): long straight jet-black hair reaching the waist with side-swept bangs, calm gray eyes, small silver drop earrings, no headdress. "
       "For this lesson a frillier knee-length variant of her charcoal-black maid dress: puffed short sleeves with white frilled armbands tied with thin ribbons, white high collar with a large soft gray bow, "
       "white frilled apron with ruffled shoulder straps and a waist tie bowed at the back, layered white petticoat ruffles at the hem, white over-knee socks, black strap shoes.")
MOA = ("Moa (match the attached reference p5_moa_anime exactly for face and hair): long ash-beige hair with soft wavy ends and neat bangs, white frilled maid headband with a thin white ribbon over the LEFT ear, amber-brown eyes. "
       "For this lesson: camel wool blazer with two front buttons and flap pockets over a white shirt with a red and navy plaid bow tie, dark navy pleated skirt, dark navy knee socks, brown loafers. The blazer fabric is stiff.")

COVERS = [
 ("cover_index", "index.html", "목차", "낮의 아틀리에, 큰 빈 캔버스 앞에 하루·시아·모아가 각자 자세를 잡고 초파리와 주판봇이 붓을 든 장면",
  "Scene: a sunny corner of the laboratory turned into an art studio; a big blank canvas on an easel in the center seen from the side; three models on a low posing platform: "
  "Haru standing with one hand on her hip, Sia in her frilly maid dress lightly holding the hem of her skirt, Moa sitting on a floor mat in her blazer with her legs folded to one side and one hand on the floor.\n"
  "Characters:\n  " + CAST["fly"] + ", on the left, holding a red pencil and pointing at the models' shoulders;\n  " + CAST["bot"] + ", on the right, holding a huge brush dripping with zigzag strokes;\n  "
  + CAST["doc"] + ", at the back center holding up a small desk lamp;\n  " + CAST["judges"] + ", sitting at a small table in the back right.\nMood: the first day of hands-on practice, friendly rivalry."),
 ("cover_01", "01_standing.html", "1부 서 있는 자세", "한 손을 허리에 얹은 하루 앞에서 초파리가 캔버스의 선화에 동그라미 다섯 개를 찍는 장면",
  "Scene: " + CAST["haru"] + " stands on the posing platform with one hand on her hip and one knee slightly forward. On the easel, a clean line drawing of her with five small orange circles marked at the shoulder, chest, the hand on the hip, the bent elbow and the knee.\n"
  "Characters:\n  " + CAST["fly"] + ", carefully placing the orange circles;\n  " + CAST["bot"] + ", impatiently scribbling many random zigzag lines on a second canvas;\n  " + CAST["doc"] + ", nodding with arms crossed.\nMood: calm focus, 'find the contact points first'."),
 ("cover_02", "02_frills.html", "2부 주름 많은 옷", "프릴 많은 메이드복의 시아 앞에서 초파리는 종 모양 큰 선부터, 주판봇은 레이스 리본에 엉킨 장면",
  "Scene: " + CAST["sia"] + " stands calmly on the platform, lightly holding the hem of her frilly skirt. On the left easel, a large simple bell-shaped outline of the skirt drawn first in one red line.\n"
  "Characters:\n  " + CAST["fly"] + ", drawing the big bell outline;\n  " + CAST["bot"] + ", comically tangled in long white lace ribbons and frills;\n  " + CAST["doc"] + ", holding a measuring tape and a curtain sample.\nMood: playful, 'big shape first, lace last'."),
 ("cover_03", "03_sitting.html", "3부 앉은 자세", "바닥 매트에 앉은 블레이저 차림의 모아, 치마가 부채처럼 퍼지고 박사가 접이식 부채를 펼쳐 보이는 장면",
  "Scene: " + CAST["moa"] + " sits on a white floor mat with her legs folded to one side and one hand on the floor, her pleated skirt spreading out like a fan.\n"
  "Characters:\n  " + CAST["doc"] + ", opening a folding paper fan to compare it with the skirt;\n  " + CAST["fly"] + ", stacking four colored paper cut-outs (hand, blazer, skirt, legs) in front-to-back order;\n  " + CAST["bot"] + ", painting the skirt with straight parallel lines.\nMood: cozy, careful observation."),
 ("cover_04", "04_light_dir.html", "4부 광원 방향", "같은 자세의 하루·시아·모아를 위·아래·옆 조명이 각각 비추고 하루가 조명 조종판을 잡은 장면",
  "Scene: three spotlights on stands: one above, one low on the floor, one from the side. " + CAST["sia"] + " is lit from below, " + CAST["moa"] + " is lit from the right side, and in the center "
  + CAST["haru"] + " holds a small lighting control board while lit from above; each figure's shadow side is clearly opposite its lamp.\nCharacters:\n  " + CAST["fly"] + ", pointing at the shadow sides;\n  " + CAST["bot"] + ", painting every shadow at the lower right no matter the lamp.\nMood: theatrical but bright daytime."),
 ("cover_05", "practice/index.html", "5부 실전 연습장", "연구실 조종 책상의 빈 화면 네 개 앞에 하루·박사·초파리·주판봇이 모인 장면",
  "Scene: a wide laboratory control desk with four blank screens (one showing small dots on a figure, one a wavy frill line, one a circle with a lamp, one a checklist of six empty boxes — all without any letters).\n"
  "Characters:\n  " + CAST["haru"] + " at the center operating the desk;\n  " + CAST["doc"] + ", leaning over with a smile;\n  " + CAST["fly"] + ", on the left screen;\n  " + CAST["bot"] + ", on the right, excited.\nMood: final practice day, energetic."),
]
BODYS = {
 "p1_haru_contacts": (HARU, "Full body, standing in a three-quarter view, right hand resting on her hip so the elbow is bent outward, left arm relaxed, left knee slightly forward. Clean line art with flat light fills and NO folds or shadows on the clothes yet (a 'no wrinkles' base drawing). "
                     "Five red circles mark the contact points: the top of the shoulder, the top of the chest, the hand pressing the hoodie at the hip, the outside of the bent elbow, and the front of the forward knee."),
 "p1_haru_bend_detail": (HARU, "Close-up of the bent arm resting on the hip: the elbow is bent about 90 degrees. On the outside of the elbow the sleeve shows long stretched tension folds; on the inside of the elbow short overlapping compression folds bunch up. Red arrows show the outside stretching and the inside gathering."),
 "p1_haru_arm_up": (HARU, "Full body, one hand raised to touch the side of her head, the other arm relaxed. Soft light from above. The hoodie folds on the chest point toward the top of the chest; the jogger pants show folds spreading from one point at the crotch area in a radial pattern. Red arrows trace these fold directions."),
 "p1_haru_shadow_order": (HARU, "The same standing pose (hand on hip) shown four times side by side: 1) clean line art with no folds, 2) line art with folds, 3) only big form shadows added (the chest treated as a sphere, the legs as cylinders, light from above-left), 4) finished with small fold shadows added only on the lit side. Same scale and position in all four."),
 "p1_haru_small_steps": (HARU, "Two close-ups side by side of the hoodie front pocket, the ribbed hoodie hem and the pants pocket under light from above: left without any shadow under the edges (looks flat), right with a thin dark cast-shadow band under the pocket edge, under the ribbed hem and under the pants pocket flap (looks layered). A thin red line points along each shadow band."),
 "p2_sia_frill_made": (SIA, "Full body, standing calmly facing three-quarter view, both hands lightly holding the hem of the skirt. Two kinds of folds are marked: the sewn-in frills (apron ruffles, petticoat ruffles, sleeve armband frills) circled in red dashed lines, and the pose-made folds (at the elbows and the waist tie) circled in blue."),
 "p2_sia_cinch": (SIA, "Close-up of the waist tie and one puffed sleeve armband: the fabric above and below each tie gathers toward the tied line. Red arrows point from above and from below toward the tied lines."),
 "p2_sia_coarse_fine": (SIA, "The skirt and apron of Sia drawn three times side by side at the same size: 1) only one big red bell-shaped outline, 2) the outline with medium waves and main folds, 3) fully finished with small frill ruffles and lace edges. The big red outline stays identical in all three."),
 "p2_sia_pairs": (SIA, "Upper body, her body tilted about 10 degrees to one side. Red dashed lines connect each pair of ornaments: the two puffed shoulders, the pairs of apron buttons, and the two ends of the apron tie; all red lines are parallel and tilted with the body."),
 "p2_sia_mixed_shadow": (SIA, "Full body, light from above-left. The puffed skirt casts a shadow on her thighs whose lower edge follows the wavy frill shape; the legs also have their own rounded form shadow on the right side. Outline the cast shadow with a red line and the form shadow with a blue line."),
 "p3_moa_sitting_joints": (MOA, "Full body, sitting on a white floor mat with her legs folded to one side (knees bent sharply), leaning slightly, one hand on the floor beside her. Folds gather strongly at the knees and hips, only a little at the nearly straight elbow. Small red circles mark the hip, the knees and the elbow."),
 "p3_moa_button_folds": (MOA, "Close-up of the buttoned blazer front while she sits leaning slightly forward: short tension folds spread out radially from the fastened button toward her sides and chest. Red arrows radiate from the button."),
 "p3_moa_blazer_vs_shirt": (MOA, "Close-up of her sleeve while sitting: the stiff blazer sleeve shows only a few thick, angular folds, while the soft white shirt cuff peeking out shows many small fine wrinkles. A red dashed line continues the blazer collar around the back of her neck to show that the two lapels connect behind."),
 "p3_moa_pleats_fan": (MOA, "Seen from slightly above, sitting on the floor mat: her pleated skirt spreads out like an open folding fan, narrow pleats at the waist widening toward the hem on the floor. Red lines follow a few pleat lines from the waist to the hem."),
 "p3_moa_depth_map": (MOA, "Two images side by side of the same sitting pose: left, clean line art with cel shadows where the hand casts a shadow on the blazer, the blazer hem on the skirt and the skirt on the legs; right, the same picture as a grayscale depth map (near parts white, far parts dark), no lines."),
 "p4_trio_four_lights": (HARU, "The same standing pose (hand on hip) shown four times side by side, each with one light source marked by a small yellow sun icon: light from above, light from below, light from the left, light from the right. In each, the shadow side is exactly opposite the sun icon."),
 "p4_sia_below_light": (SIA, "Full body, lit by a single lamp on the floor in front of her (under-lighting): the underside of the chin, the underside of the arms and the underside of the apron are bright, while the tops of the shoulders, the top of the head and the area above the eyebrows are in shadow; her tall cast shadow rises on the wall behind her. Calm, slightly mysterious mood but still a bright white studio."),
 "p4_moa_side_light": (MOA, "Full body, standing, a canvas shoulder bag on her left shoulder and her right forearm raised in front of her chest holding the strap, strong light from her right side. The left half of her body is in form shadow; her raised forearm and the bag cast shadows onto her torso that are shifted to the side. Outline the cast shadows in red and the form shadow edge in blue."),
 "p4_trio_angle_column": (SIA, "Two scenes of Sia side by side, both lit from her left: left scene with the light from the front-left (about 60 degrees), so about three quarters of her visible body is lit; right scene with the light from the back-left (about 120 degrees), so only about one quarter is lit. Next to each, a small top-down circle with a dot for the nose and a yellow arrow showing the light direction."),
 "p4_haru_normal_relight": (HARU, "Four panels side by side of the same half-body pose: 1) flat-colored line art without shadows, 2) its normal map (smooth red-green-blue gradients showing surface directions, no lines), 3) relit with warm morning light from the upper left, 4) relit with orange evening light from the right. The face and outfit identical in all panels."),
}
RATIO = {"16/9": "16:9", "2/3": "2:3", "4/3": "4:3"}
def imgs():
    out = []
    for P in (P1, P2, P3, P4):
        for s in P["steps"]:
            k, alt, ar = s["img"]; out.append((k, P["file"], f"{P['no']}부 {s['id']}", RATIO[ar], alt))
    return out
IM = imgs()
assert set(k for k, *_ in IM) == set(BODYS), set(k for k, *_ in IM) ^ set(BODYS)
SLUG = {"D01": "covers_A", "D02": "covers_B", "D03": "portrait_A", "D04": "portrait_B", "D05": "sitting_4x3", "D06": "haru_16x9", "D07": "sia_16x9", "D08": "moa_16x9"}
CONV = [("D01", "표지 A", ["cover_index", "cover_01", "cover_02"]), ("D02", "표지 B", ["cover_03", "cover_04", "cover_05"]),
        ("D03", "세로 전신 2:3 (하루·시아)", ["p1_haru_contacts", "p1_haru_arm_up", "p2_sia_frill_made", "p2_sia_mixed_shadow"]),
        ("D04", "세로 전신 2:3 (빛)", ["p4_sia_below_light", "p4_moa_side_light"]), ("D05", "4:3 앉은 모아", ["p3_moa_sitting_joints", "p3_moa_pleats_fan"]),
        ("D06", "16:9 하루", ["p1_haru_bend_detail", "p1_haru_shadow_order", "p1_haru_small_steps", "p4_haru_normal_relight", "p4_trio_four_lights"]),
        ("D07", "16:9 시아", ["p2_sia_cinch", "p2_sia_coarse_fine", "p2_sia_pairs", "p4_trio_angle_column"]),
        ("D08", "16:9 모아", ["p3_moa_button_folds", "p3_moa_blazer_vs_shirt", "p3_moa_depth_map"])]
allk = [k for _, _, ks in CONV for k in ks]; assert len(allk) == len(set(allk)) == 26, len(allk)
os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
rows = []; info = {k: (p, part, ratio, alt) for k, p, part, ratio, alt in IM}
for k, page, part, alt, _ in COVERS: info[k] = (page, part, "16:9", alt)
for cid, name, keys in CONV:
    pix = cid in ("D01", "D02"); ratio = "16:9" if pix else info[keys[0]][2]
    who = [x for x in ("haru", "sia", "moa") if any(x in k or (x == "haru" and k == "p4_trio_four_lights") or (x == "sia" and k == "p4_trio_angle_column") for k in keys)]
    att = "refs/ 전부(픽셀 캐릭터 얼굴 그림 + 기초편 표지)" if pix else ", ".join(f"refs/p5_{w}_anime.png" for w in who) + " · 앞 대화에서 받은 그림이 있으면 함께"
    md = [f"# {cid} · {name} — " + ", ".join(keys), "", f"**첨부:** {att}", "", "**Genspark에 먼저 붙여 넣기 ↓**", "```"]
    if pix:
        md += ["웹페이지 맨 위에 거는 표지 그림을 한 장씩 차례로 만들어 줘.", "- 비율 16:9, 가로 1920px 이상", "- 그림체는 반드시 16비트 RPG풍 픽셀아트 (네모 픽셀이 보이게, 매끈한 일러스트·벡터·수채화·3D 금지)",
               "- 배경은 흰색·밝은 낮 연구실", "- 첨부한 참고 그림의 캐릭터를 같은 외형으로 (하루는 오늘 실험복을 벗고 라벤더 후드 집업)", "- 그림 안에 글자·숫자·로고 금지, 캔버스·화면은 비워 둘 것", "아래 영어 프롬프트를 하나씩 써 줘."]
    else:
        md += ["첨부한 애니풍 기준 전신 그림의 인물을 같은 얼굴·머리로, 이번 연습용 의상을 입혀 그려 줘.", f"- 비율 {ratio}, 긴 변 1536px 이상, 흰 배경", "- 애니풍 셀 채색(그림자는 연한 보라 회색 한 단계)",
               "- 세 사람 모두 20대 초반 성인, 노출 없음, 자연스러운 체형", "- 표시는 빨간 화살표·동그라미·점선만, 글자·숫자 절대 금지", "- 유명 애니 캐릭터처럼 보이지 않게", "아래 영어 프롬프트를 하나씩 써 줘."]
    md += ["```", ""]
    for i, k in enumerate(keys, 1):
        page, part, r, alt = info[k]
        rows.append([len(rows) + 1, cid, k, page, part, r, "pixel" if pix else "anime", ""])
        md += ["---", f"## {i}) {k}", f"alt(페이지 설명): {alt}", "```"]
        if pix:
            body = [c for c in COVERS if c[0] == k][0][4]
            md += ["Website top cover illustration, wide 16:9.", PIX, body, SAFE, NOPIX]
        else:
            ch, sc = BODYS[k]
            md += [f"Character illustration, {r}.", BODY, "Character: " + ch, sc, ARW, NEG]
        md += ["```", ""]
    open(os.path.join(D, "prompts", f"{cid}_{SLUG[cid]}.md"), "w").write("\n".join(md))
with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["order", "conversation", "file", "page", "part", "ratio", "style", "status"]); w.writerows(rows)
conv_rows = "\n".join(f"| {i+1} | `prompts/{cid}_{SLUG[cid]}.md` | {len(ks)} | {'16:9 픽셀' if cid in ('D01','D02') else info[ks[0]][2]} | {'refs 전부' if cid in ('D01','D02') else '해당 인물의 refs/p5_*_anime.png'} |" for i, (cid, name, ks) in enumerate(CONV))
open(os.path.join(D, "README.md"), "w").write(f"""# 그림 요청 꾸러미 — 구조 먼저 그리기 연구실 02 · 실천편

저장소: `adminmrobo/structure_first_drawing_lab_02` (페이지는 이미 동작합니다 — 그림 자리는 '그림 준비 중'으로 비어 있음)
만드는 도구: Genspark 이미지 · 받은 뒤 `checklist.csv`의 이름으로 저장해 zip으로 돌려주시면 됩니다. 모두 **26장**(표지 6 + 본문 20)입니다.

## 1. 이번 편의 그림 규칙
| 항목 | 규칙 |
|---|---|
| 그림체 | **표지 6장은 16비트 RPG 픽셀아트**(연구실 세계). **본문 20장은 애니풍 셀 채색**(이 시리즈만의 예외, 기초편과 같음) |
| 배경 | 흰색·밝은 낮 분위기 |
| 캐릭터 고정값 | `refs/p5_*_anime.png`(기초편 기준 전신)와 같은 얼굴·머리. 하루: 정수리 번 2개 + 앞머리 가운데 남색 줄 / 시아: 흑발·머리 장식 없음 / 모아: 흰 프릴 머리띠 + **왼쪽** 귀 위 흰 리본 |
| 이번 연습용 의상 | 하루: 실험복 벗고 라벤더 후드 집업 + 조거 바지 / 시아: 무릎 길이의 프릴 많은 메이드복 + 흰 오버니 양말 / 모아: 캐멀 블레이저 + 남색 주름치마 |
| 노출 | 노출·과장된 체형 금지, 세 사람 모두 20대 초반 성인 |
| 표시 | 빨간 화살표·동그라미·점선만. **글자·숫자 금지**(설명은 페이지 글이 맡습니다) |
| 원서 | 원서의 그림·사진을 첨부하거나 따라 그리게 하지 않습니다. 자세만 말로 정했습니다 |

## 2. 요청 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 그림 수 | 비율 | 첨부할 참고 그림 |
|---|---|---|---|---|
{conv_rows}

**D03(세로 전신)을 먼저** 받아 그림체를 확인한 뒤, 마음에 든 그림을 이후 대화에 참고 그림으로 함께 올려 주세요.

## 3. 저장 이름
`checklist.csv`의 `file` 열 이름 그대로(png 또는 jpg). 이름만 맞으면 제가 크기 변환·WebP·페이지 반영을 합니다.

## 4. 고칠 때 (같은 대화에서)
`Same character, same style and composition. Change only: {{고칠 점}}. Still no text.`

## 5. 돌려주는 법
- 한 번에 어려우면 **대화 단위(D01~D08)로 나눠** 여러 zip으로 주셔도 됩니다.
- 표지(cover_*)가 들어오면 공유 미리보기(og)도 표지에서 잘라 다시 만듭니다. 표지는 픽셀 격자를 찾아 정수배로만 키워 반영합니다.
""")
print("requests:", len(rows), "files", len(CONV))
