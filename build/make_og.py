# -*- coding: utf-8 -*-
"""공유 미리보기(og) 그림을 만든다. 표지 그림(assets/img/cover_*.webp)이 들어오면 그것을 잘라 쓰고, 없으면 글자+캐릭터로 만든다."""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
ITEMS = [("og_index", "cover_index", "구조 먼저 그리기 연구실 02 · 실천편", "주름과 그림자를 직접 넣어 보기", ["fruitfly", "haru", "sia", "moa", "jupanbot"]),
 ("og_01", "cover_01", "1부 서 있는 자세", "접점에서 그림자까지", ["doctor", "haru", "fruitfly"]),
 ("og_02", "cover_02", "2부 주름 많은 옷", "프릴과 리본", ["doctor", "sia", "fruitfly"]),
 ("og_03", "cover_03", "3부 앉은 자세", "접히고 겹치는 옷", ["doctor", "moa", "fruitfly"]),
 ("og_04", "cover_04", "4부 광원 방향", "같은 선화, 다른 그림자", ["haru", "sia", "moa"]),
 ("og_05", "cover_05", "5부 실전 연습장", "접점·프릴·조명·숙제", ["haru", "doctor", "x1"])]
os.makedirs(os.path.join(ROOT, "assets", "og"), exist_ok=True)
for key, cover, t1, t2, cast in ITEMS:
    cp = os.path.join(ROOT, "assets", "img", cover + ".webp")
    if os.path.exists(cp):
        im = Image.open(cp).convert("RGB")  # 1920×1080 = 480×270 격자의 4배
        g = im.resize((480, 270), Image.NEAREST)  # 원래 픽셀 격자로
        im = g.crop((40, 30, 440, 240)).resize((1200, 630), Image.NEAREST)  # 400×210 → 정수배 3
    else:
        im = Image.new("RGB", (1200, 630), "#ffffff"); d = ImageDraw.Draw(im)
        for x in range(0, 1200, 40):
            for y in range(0, 630, 40):
                if (x // 40 + y // 40) % 2 == 0: d.rectangle([x, y, x + 39, y + 39], fill="#f3f6fa")
        d.rectangle([0, 0, 1200, 8], fill="#0f8f84")
        d.text((60, 70), t1, font=ImageFont.truetype(F, 58), fill="#16212b")
        d.text((60, 160), t2, font=ImageFont.truetype(F, 36), fill="#0f8f84")
        d.text((60, 560), "안상선 · ahnboat lab", font=ImageFont.truetype(F, 24), fill="#5b6874")
        for i, c in enumerate(cast):
            f = Image.open(os.path.join(ROOT, "assets", "chars", f"{c}_e01.webp")).convert("RGBA").resize((220, 220), Image.NEAREST)
            im.paste(f, (1200 - 60 - 230 * (len(cast) - i), 330), f)
    im.save(os.path.join(ROOT, "assets", "og", key + ".jpg"), quality=82)
print("og done")
