# -*- coding: utf-8 -*-
"""부마다 '프롬프트로 직접 만들어 보기' 절의 재료.
frags: (한국어 이름, 배운 단계, 영어 조각) — 체크하면 요청문에 들어간다.
naive: 주판봇식 요청문(원리 없음) · pair: 같은 인물을 두 요청문으로 만든 비교 그림 키."""

STYLE = "High-quality anime illustration, clean lineart, two-tone cel shading, plain white background, a young adult woman in her early twenties, modest outfit exactly as described."
NEG = "No text, no letters, no numbers, no logos, no watermark, no exaggerated body proportions, not resembling any famous anime character."
CHAR = {
 "haru": ("하루", "Character: Haru — long straight pink hair with navy streaks and a thick navy streak down the center of the bangs, two round hair buns on top of the head, big blue eyes, "
                  "lavender zip-up hoodie over a white t-shirt, gray-blue jogger pants, lavender slip-on sneakers."),
 "sia": ("시아", "Character: Sia — long straight jet-black hair, calm gray eyes, small silver drop earrings, no headdress, knee-length charcoal-black maid dress with puffed short sleeves, "
                 "white high collar with a large gray bow, white frilled apron, layered white petticoat ruffles, white over-knee socks, black strap shoes."),
 "moa": ("모아", "Character: Moa — long ash-beige wavy hair, white frilled maid headband with a thin white ribbon over the LEFT ear, amber eyes, camel wool blazer with two buttons over a white shirt "
                 "with a red and navy plaid bow tie, dark navy pleated skirt, navy knee socks, brown loafers."),
}

PL = {
 1: dict(
  model="haru", ratio="2:3",
  pose="Full body, vertical 2:3. Pose: standing in a three-quarter view, right hand resting on her hip so the elbow bends outward, left arm relaxed, left knee slightly forward.",
  frags=[("접점에서 주름 시작", "1단계", "Folds start from the contact points: the tops of the shoulders, the top of the chest, the hand pressing the hoodie at the hip, the bent elbow and the forward knee."),
         ("굽힌 팔꿈치 안팎", "2단계", "At the bent elbow: long stretched folds on the outside, short bunched folds on the inside."),
         ("꼭대기를 향한 주름", "3단계", "Chest folds point toward the top of the chest; the fabric below it hangs loosely with a few soft drape folds."),
         ("큰 형체 그림자 먼저", "4단계", "Light from the upper left. Shade the big forms first — the chest as a sphere, the legs as cylinders — so the right side of the body is in shadow; small fold shadows only on the lit side."),
         ("단차 아래 그림자 띠", "5단계", "Thin cast-shadow bands under the hoodie pocket edge, under the ribbed hem and under the pants pocket.")],
  naive="anime girl with pink hair, purple hoodie, hand on hip, lots of wrinkles, detailed shading, masterpiece",
  checks=["주름이 접점(어깨·가슴 위·허리 손·팔꿈치·무릎)에서 시작하나", "굽힌 팔꿈치의 짧은 주름이 안쪽에 모였나", "가슴 주름이 꼭대기를 향하나",
          "그림자가 광원(왼쪽 위)의 반대쪽 절반에 한 덩어리로 있나", "주머니·밑단 아래에 얇은 그림자 띠가 있나", "정수리 번 2개와 앞머리 가운데 남색 줄이 그대로인가"],
  fix="Same character, same pose and style. Change only: put the short bunched folds on the INSIDE of the bent elbow and long stretched folds on the outside. Still no text.",
  pair=("pr1_haru_naive", "pr1_haru_guided"), example="p1_haru_contacts"),
 2: dict(
  model="sia", ratio="2:3",
  pose="Full body, vertical 2:3. Pose: standing calmly in a three-quarter view, both hands lightly holding the hem of her skirt.",
  frags=[("고른 깊이의 프릴", "1단계", "The apron hem and the petticoat have evenly deep gathered ruffles, as if the fabric were gathered to about twice the band length."),
         ("끈이 조인 곳의 주름", "2단계", "The waist tie and the sleeve bands cinch the fabric; short folds gather toward each tied line from above and from below."),
         ("큰 종 모양 윤곽", "3단계", "The skirt keeps one clean, symmetrical bell-shaped silhouette; ruffles and lace follow that big outline."),
         ("짝 장식은 나란히", "4단계", "Paired ornaments — both puffed shoulders, the pairs of apron buttons, the two ends of the apron tie — sit on parallel lines that follow the body's slight tilt."),
         ("물결 모양 떨어지는 그림자", "5단계", "Light from the upper left: the skirt casts a shadow on her thighs whose lower edge follows the wavy ruffle shape; the legs also have rounded form shadows on the right side.")],
  naive="cute anime maid girl, black hair, super frilly dress, lots of lace, ultra detailed, masterpiece",
  checks=["프릴 물결의 깊이가 한 띠 안에서 고른가", "허리끈 위아래에서 주름이 끈 쪽으로 모이나", "치마 전체가 반듯한 종 모양인가(한쪽으로 기울지 않나)",
          "어깨 프릴·단추 짝의 높이가 몸 기울기와 함께 맞나", "다리 위 그림자 끝이 프릴처럼 물결지나", "머리 장식이 없는가(시아의 고정값)"],
  fix="Same character, same pose and style. Change only: make the cast shadow on her thighs follow the wavy ruffle edge of the skirt instead of a straight line. Still no text.",
  pair=("pr2_sia_naive", "pr2_sia_guided"), example="p2_sia_mixed_shadow"),
 3: dict(
  model="moa", ratio="4:3",
  pose="Full body, 4:3. Pose: sitting on a white floor mat with her legs folded to one side, leaning slightly, one hand on the floor beside her.",
  frags=[("많이 굽은 관절에 주름", "1단계", "Strong bunched folds at the sharply bent knees and hips; only a few at the nearly straight elbow."),
         ("단추에서 퍼지는 주름", "2단계", "The fastened blazer button holds the fabric; short tension folds radiate from the button toward her sides."),
         ("빳빳한 블레이저", "3단계", "The blazer is stiff wool with few thick, angular folds; the shirt cuff shows small soft wrinkles; the collar continues around the back of the neck."),
         ("부채처럼 퍼진 주름치마", "4단계", "The pleated skirt fans out on the floor like an open folding fan: narrow pleats at the waist widening toward the hem."),
         ("앞뒤 겹침과 그림자", "5단계", "Clear front-to-back order: the hand in front, then the blazer hem, the skirt and the folded legs; each front layer casts a shadow on the layer behind it.")],
  naive="anime girl sitting on the floor, blazer and pleated skirt, many wrinkles everywhere, detailed, masterpiece",
  checks=["무릎·고관절 주름이 팔꿈치보다 많은가", "잠근 단추에서 주름이 퍼지나", "블레이저가 니트처럼 잘게 구겨지지 않았나",
          "주름치마가 밑단으로 갈수록 넓게 퍼지나", "바닥 짚은 손이 치마보다 앞에 있나", "흰 리본이 왼쪽 귀 위에 있나"],
  fix="Same character, same pose and style. Change only: make the blazer stiffer — fewer, thicker, more angular folds — while the shirt cuff keeps small soft wrinkles. Still no text.",
  pair=("pr3_moa_naive", "pr3_moa_guided"), example="p3_moa_pleats_fan"),
 4: dict(
  model="haru", ratio="2:3", models=["haru", "sia", "moa"],
  pose="Full body, vertical 2:3. Pose: standing in a three-quarter view, a canvas shoulder bag on one shoulder, the near forearm raised in front of the chest holding the strap.",
  lights=[("위", "1단계", "Single light source from directly above: the tops of the head and shoulders are bright, the underside of the chin and the arms are in shadow."),
          ("아래(바닥 조명)", "2단계", "Single light source low on the floor in front (under-lighting): the underside of the chin and the arms are bright, the tops of the shoulders and the area above the eyebrows are in shadow."),
          ("왼쪽 앞 60°", "4단계", "Single light source from the front-left at about 60 degrees seen from above, slightly high: about three quarters of the visible body is lit, the right quarter is in shadow."),
          ("왼쪽 뒤 120°", "4단계", "Single light source from the back-left at about 120 degrees seen from above: only about one quarter of the visible body, along the left edge, is lit."),
          ("오른쪽 바로 옆", "1단계", "Single light source directly from her right side: the right half of the body is lit, the left half is in shadow.")],
  frags=[("팔·가방이 드리우는 그림자", "3단계", "The raised forearm and the shoulder bag cast shadows onto the torso, shifted away from the light."),
         ("광원 하나만", "1단계", "Only one light source; every shadow sits on the side opposite that light, consistently on the face, clothes and legs."),
         ("다시 조명(그림 첨부)", "5단계", "Relight only: keep the line art, pose and flat colors identical to the attached image; first remove all original highlights and shadows, then shade again for the new light.")],
  naive="anime girl, dramatic lighting, cinematic shadows, masterpiece",
  checks=["그림자가 모두 광원의 반대쪽에 있나", "아래 조명이면 턱 아래·팔 아래가 밝은가", "밝은 폭이 고른 각도와 맞나(60°면 약 4분의 3)",
          "팔·가방 그림자가 몸통에 옆으로 밀려 있나", "다시 조명했다면 원래 그림의 하이라이트가 남지 않았나", "인물의 고정값(머리·의상)이 그대로인가"],
  fix="Same character, same pose and style. Change only the lighting: one light source from {선택한 방향}; move every shadow to the opposite side. Still no text.",
  pair=("pr4_haru_naive", "pr4_haru_guided"), example="p4_moa_side_light"),
}

# 비교 그림 8장 요청문(E01~E04)
PAIR_NOTE = {
 1: ("하루, 같은 자세 — 왼쪽은 원리 없는 요청문의 결과(주름이 아무 데나 흩어지고 팔꿈치 바깥에 몰림, 그림자가 양쪽에 같음), 오른쪽은 원리를 넣은 요청문의 결과", "2:3"),
 2: ("시아, 같은 자세 — 왼쪽은 레이스만 강조한 결과(치마가 한쪽으로 기울고 프릴 깊이가 들쭉날쭉, 다리 그림자 끝이 직선), 오른쪽은 원리를 넣은 결과", "2:3"),
 3: ("모아, 같은 앉은 자세 — 왼쪽은 원리 없는 결과(블레이저가 니트처럼 쭈글쭈글, 치마가 세로줄, 손이 치마 뒤로 묻힘), 오른쪽은 원리를 넣은 결과", "4:3"),
 4: ("하루, 같은 자세 — 왼쪽은 '극적인 조명'만 적은 결과(빛이 두 방향에서 오는 듯 그림자가 엇갈림), 오른쪽은 왼쪽 앞 60° 광원 하나를 적은 결과", "2:3"),
}
NAIVE_LOOK = {
 1: "Deliberately flawed result for teaching: wrinkles scattered randomly all over the hoodie, folds bunched on the OUTSIDE of the bent elbow, both legs equally shaded with no clear light direction.",
 2: "Deliberately flawed result for teaching: the skirt silhouette leans to one side, ruffles irregularly deep and flat in places, the cast shadow on the legs ends in a ruler-straight line.",
 3: "Deliberately flawed result for teaching: the blazer crumpled with many small knit-like wrinkles, the pleated skirt drawn as straight parallel vertical lines, the hand on the floor hidden behind the skirt.",
 4: "Deliberately flawed result for teaching: shadows contradict each other as if lit from two directions (face shaded on the left, clothes shaded on the right), no cast shadow from the arm or bag.",
}

# 실제로 받은 비교 그림을 점검표로 본 결과(2026-11-23 첫 결과) — 페이지의 'AI 판단' 재료
PAIR_SEEN = {
 1: ["두 장 모두 요청한 '집업 후드·조거 바지' 대신 기초편 기준 그림의 실험복·청바지가 나왔습니다. 첨부한 기준 그림의 옷이 요청문보다 강하게 따라온 것입니다.",
     "원리를 넣은 쪽이 팔꿈치 안쪽 주름이 조금 더 정리됐지만 차이는 작습니다. 왼쪽 위 광원의 큰 형체 그림자는 두 장 모두 약합니다."],
 2: ["원리 없는 쪽은 기준 그림처럼 긴소매·긴 치마로 돌아갔고, 원리를 넣은 쪽은 요청대로 반소매·무릎 길이입니다.",
     "원리를 넣은 쪽은 치마가 좌우 대칭인 종 모양이고 프릴 깊이도 고릅니다. 다만 5단계의 '다리 위 물결 모양 그림자'는 두 장 모두 빠졌습니다."],
 3: ["두 장 모두 블레이저가 아니라 니트 카디건이 나왔고, 원리 없는 쪽에는 기준 그림의 앞치마까지 따라왔습니다. 그래서 3단계 '빳빳한 천'은 이 그림으로 확인할 수 없습니다.",
     "원리를 넣은 쪽은 주름치마가 바닥으로 더 퍼지고, 손이 바닥을 짚은 모습이 분명해졌습니다."],
 4: ["'극적인 조명'만 적은 쪽은 오히려 그림자가 거의 없는 평평한 그림이 나왔습니다.",
     "원리를 넣은 쪽은 실험복이 다시 생겼고, '왼쪽 앞 60°, 4분의 3이 밝게'라는 그림자 넓이도 잘 지켜지지 않았습니다. 각도·넓이 같은 수치는 한 번에 잘 지켜지지 않는 사례입니다."],
}
PAIR_LESSON = ["첨부한 기준 그림의 옷이 요청문보다 강하게 따라옵니다. 옷을 바꿀 때는 얼굴만 자른 기준 그림을 올리거나, 'not wearing a lab coat'처럼 빼야 할 것을 함께 적습니다.",
               "'일부러 틀리게'나 '그림자 넓이 4분의 3' 같은 요청은 도구가 잘 지키지 않습니다. 고치기 문장으로 한 번에 하나씩 다시 요청합니다.",
               "결과는 매번 달라집니다. 원리를 적었다고 믿지 말고, 위 점검표로 직접 확인하는 것이 이 절의 목적입니다."]
